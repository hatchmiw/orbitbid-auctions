#!/usr/bin/env python3
"""Export a public OrbitBid auction directly from GitHub Actions.

Usage:
    python scripts/export_orbitbid.py 1879

Writes:
    auctions/<auction_id>/README.md
    auctions/<auction_id>/summary.md
    auctions/<auction_id>/summary.csv
    auctions/<auction_id>/lots.json

The script discovers OrbitBid's internal lot IDs from the public auction
catalog, then retrieves each lot through OrbitBid's public GraphQL endpoint.
No bidder login or personal account token is used.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from curl_cffi import requests

CATALOG_URL = "https://bid.orbitbid.com/"
GRAPHQL_URL = "https://oas3.oasbid.com/__graphql__"
CLIENT_TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpZCI6MiwibmFtZSI6InB1YmxpYyIsImlhdCI6MTc5MDAwMjU0OH0."
    "QAXWKPsNUMzLm-kGZh3V3UI_8Cn8Jzm2WqX02qZRcOY"
)
PAGE_SIZE = 60
MAX_PAGES = 200
LOT_DELAY_SECONDS = 0.20
PAGE_DELAY_SECONDS = 0.10
BATCH_PAUSE_EVERY = 20
BATCH_PAUSE_SECONDS = 1.0
MAX_CLOSE_SPAN_SECONDS = 2 * 24 * 60 * 60

LOT_QUERY = r"""
query getPublicLot($id: Int!, $increment_view: Boolean) {
  lot: getPublicLot(id: $id, increment_view: $increment_view) {
    id item_number title subtitle description amount max_amount bid_count
    status live_status prebid_start_time start_time end_time offer_end_time
    has_reserve has_reserve_met
    premium { id name type amount cash_discount }
    expenses { id name type amount is_taxable }
    location {
      id display_name address1 address2 city zip_code
      state { id code }
    }
    images { id small_path large_path metadata }
    fields { id type label value other_value }
    terms { id stub name display_name value }
  }
}
"""


def clean(value: Any) -> str:
    return " ".join(str(value or "").split())


def md_escape(value: Any) -> str:
    return clean(value).replace("<", "&lt;").replace(">", "&gt;")


def normalized_lot_number(item_number: Any, internal_id: int) -> str:
    value = clean(item_number)
    if not value:
        return str(internal_id)
    return re.sub(r"^1-", "", value)


def epoch_to_iso(value: Any) -> str:
    if value in (None, "", 0, "0"):
        return ""
    try:
        number = int(float(value))
    except (TypeError, ValueError):
        return ""
    if number > 10_000_000_000:
        number //= 1000
    try:
        return datetime.fromtimestamp(number, tz=timezone.utc).isoformat().replace("+00:00", "Z")
    except (OverflowError, OSError, ValueError):
        return ""


def append_price_history(
    auction_dir: Path,
    snapshot_at: str,
    lots: list[dict[str, Any]],
    snapshot_type: str,
) -> None:
    history_path = auction_dir / "price-history.csv"
    new_file = not history_path.exists() or history_path.stat().st_size == 0

    with history_path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        if new_file:
            writer.writerow(
                [
                    "snapshot_at",
                    "snapshot_type",
                    "lot",
                    "internal_id",
                    "current_bid",
                    "bid_count",
                    "status",
                    "live_status",
                    "end_time",
                    "end_time_utc",
                ]
            )
        for lot in lots:
            writer.writerow(
                [
                    snapshot_at,
                    snapshot_type,
                    lot.get("requested_lot_number"),
                    lot.get("internal_id"),
                    lot.get("amount"),
                    lot.get("bid_count"),
                    lot.get("status"),
                    lot.get("live_status"),
                    lot.get("end_time"),
                    epoch_to_iso(lot.get("end_time")),
                ]
            )


def build_session() -> requests.Session:
    session = requests.Session(impersonate="chrome")
    session.headers.update(
        {
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }
    )
    return session


class MainLotLinkParser(HTMLParser):
    """Collect OrbitBid lot links from the catalog's main content only."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._main_depth = 0
        self.ids: list[int] = []
        self._seen: set[int] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "main":
            self._main_depth += 1
            return
        if self._main_depth <= 0 or tag != "a":
            return

        href = ""
        for name, value in attrs:
            if name.lower() == "href" and value:
                href = value
                break

        match = re.search(r"/lot/(\d+)(?:/|$|[?#])", href)
        if not match:
            return

        lot_id = int(match.group(1))
        if lot_id not in self._seen:
            self._seen.add(lot_id)
            self.ids.append(lot_id)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "main" and self._main_depth > 0:
            self._main_depth -= 1


def catalog_lot_ids_from_html(html: str) -> list[int]:
    parser = MainLotLinkParser()
    parser.feed(html)
    parser.close()
    return parser.ids


def graph_query_headers(operation_name: str) -> dict[str, str]:
    return {
        "accept": "*/*",
        "content-type": "application/json",
        "x-client-host": "bid.orbitbid.com",
        "x-client-token": CLIENT_TOKEN,
        "x-operation-name": operation_name,
        "origin": "https://bid.orbitbid.com",
        "referer": "https://bid.orbitbid.com/",
    }


def probe_frontend_graphql_operations(
    session: requests.Session, script_srcs: list[str]
) -> None:
    """Inspect public frontend bundles for GraphQL operation names when discovery breaks."""
    found: set[str] = set()
    for src in script_srcs:
        if "d1ljvnrgb7j023.cloudfront.net" not in src or not src.endswith(".js"):
            continue
        try:
            response = session.get(src, timeout=30)
            if response.status_code != 200:
                continue
            body = response.text
        except Exception:
            continue

        for name in re.findall(r"\b(?:query|mutation)\s+([A-Za-z_][A-Za-z0-9_]*)", body):
            if re.search(r"(auction|lot|catalog|item)", name, re.I):
                found.add(name)

        for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]{4,60}", body):
            if re.search(r"(Public.*(?:Auction|Lot)|(?:Auction|Lot).*Public|AuctionLots|LotsByAuction)", token, re.I):
                found.add(token)

        if "getPublicLot" in body:
            for match in re.finditer("getPublicLot", body):
                start = max(0, match.start() - 500)
                end = min(len(body), match.end() + 1000)
                snippet = re.sub(r"\s+", " ", body[start:end])
                print(f"Frontend bundle context near getPublicLot ({src}): {snippet}", file=sys.stderr)
                break

    print(
        "Frontend GraphQL/catalog operation candidates: " + repr(sorted(found)[:200]),
        file=sys.stderr,
    )


def probe_public_query_fields(session: requests.Session) -> None:
    """Print public GraphQL query names for diagnostics when catalog HTML is only an app shell."""
    query = """
    query OrbitBidSchemaProbe {
      __schema {
        queryType {
          fields {
            name
            args {
              name
              type { kind name ofType { kind name } }
            }
          }
        }
      }
    }
    """
    try:
        response = session.post(
            GRAPHQL_URL,
            headers=graph_query_headers("OrbitBidSchemaProbe"),
            json={"operationName": "OrbitBidSchemaProbe", "variables": {}, "query": query},
            timeout=30,
        )
        if response.status_code != 200:
            print(f"GraphQL schema probe failed: HTTP {response.status_code}", file=sys.stderr)
            return
        payload = response.json()
        if payload.get("errors"):
            print(
                "GraphQL schema probe errors: "
                + json.dumps(payload["errors"], ensure_ascii=False),
                file=sys.stderr,
            )
            return
        fields = (((payload.get("data") or {}).get("__schema") or {}).get("queryType") or {}).get("fields") or []
        names = [field.get("name", "") for field in fields]
        likely = [name for name in names if re.search(r"(auction|lot|catalog)", name, re.I)]
        print("Public GraphQL query fields matching auction/lot/catalog:", likely, file=sys.stderr)
    except Exception as exc:
        print(f"GraphQL schema probe failed: {exc}", file=sys.stderr)


def discover_lot_ids(session: requests.Session, auction_id: str) -> tuple[list[int], list[str]]:
    """Discover lot IDs without launching a browser.

    OrbitBid currently server-renders the auction catalog. Restricting extraction
    to links inside <main> avoids the unrelated lot links that can appear in the
    surrounding application shell.
    """

    all_ids: list[int] = []
    seen: set[int] = set()
    page_urls: list[str] = []

    for page in range(1, MAX_PAGES + 1):
        params = {
            "items": "all",
            "auction_id": auction_id,
            "display": "grid",
            "limit": str(PAGE_SIZE),
            "page": str(page),
        }
        url = f"{CATALOG_URL}?{urlencode(params)}"
        response = session.get(url, timeout=45)
        if response.status_code != 200:
            raise RuntimeError(f"Catalog page {page} failed: HTTP {response.status_code}")

        page_ids = catalog_lot_ids_from_html(response.text)
        fresh = [lot_id for lot_id in page_ids if lot_id not in seen]
        print(
            f"Catalog page {page}: {len(page_ids)} main-content lot links, "
            f"{len(fresh)} new"
        )

        if page == 1 and not page_ids:
            print(
                f"Catalog diagnostic: status={response.status_code} "
                f"final_url={response.url} bytes={len(response.content)}",
                file=sys.stderr,
            )
            compact = clean(response.text)
            print(f"Catalog diagnostic body prefix: {compact[:1500]}", file=sys.stderr)
            script_srcs = re.findall(r'<script[^>]+src=["\\\']([^"\\\']+)', response.text, re.I)
            print(f"Catalog diagnostic script sources: {script_srcs[:20]}", file=sys.stderr)
            probe_frontend_graphql_operations(session, script_srcs)
            probe_public_query_fields(session)
            raise RuntimeError(
                "No OrbitBid lot links were found inside the catalog main content. "
                "Refusing to scrape unrelated application-shell links."
            )

        if not fresh:
            break

        page_urls.append(url)
        for lot_id in fresh:
            seen.add(lot_id)
            all_ids.append(lot_id)

        time.sleep(PAGE_DELAY_SECONDS)

    if not all_ids:
        raise RuntimeError(
            "No OrbitBid lot IDs were discovered. The catalog markup may have changed "
            "or the auction may not be publicly accessible."
        )

    return all_ids, page_urls

def fetch_lot(session: requests.Session, internal_id: int) -> dict[str, Any]:
    headers = graph_query_headers("getPublicLot")
    payload = {
        "operationName": "getPublicLot",
        "variables": {"id": internal_id, "increment_view": False},
        "query": LOT_QUERY,
    }

    response = session.post(GRAPHQL_URL, headers=headers, json=payload, timeout=45)
    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code}")

    data = response.json()
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False))

    lot = (data.get("data") or {}).get("lot")
    if not lot:
        raise RuntimeError("No lot returned")

    lot_number = normalized_lot_number(lot.get("item_number"), internal_id)
    return {
        "requested_lot_number": lot_number,
        "internal_id": internal_id,
        **lot,
        "photo_count": len(lot.get("images") or []),
    }


def validate_lot_set(lots: list[dict[str, Any]]) -> None:
    """Reject an obviously mixed-auction discovery before files are written."""

    closes: list[int] = []
    for lot in lots:
        for key in ("end_time", "offer_end_time"):
            raw = lot.get(key)
            if raw in (None, "", 0, "0"):
                continue
            try:
                value = int(float(raw))
            except (TypeError, ValueError):
                continue
            if value > 10_000_000_000:
                value //= 1000
            closes.append(value)

    if not closes:
        raise RuntimeError(
            "No scheduled closing times were returned; refusing to write an "
            "unverifiable auction snapshot."
        )

    span = max(closes) - min(closes)
    if span > MAX_CLOSE_SPAN_SECONDS:
        raise RuntimeError(
            "Mixed-auction safety check failed: lot close times span "
            f"{span / 86400:.1f} days. Nothing will be written."
        )



def make_summary(data: dict[str, Any]) -> str:
    refreshed = bool(data.get("last_price_refresh_at"))
    if refreshed:
        status_lines = [
            f"- Price refresh: {data['retrieved_at']}",
            f"- Source: {data['source_url']}",
            f"- Saved lots refreshed: {data['total_retrieved']}",
            f"- Refresh errors: {data['total_errors']}",
        ]
    else:
        status_lines = [
            f"- Retrieved: {data['retrieved_at']}",
            f"- Source: {data['source_url']}",
            f"- Catalog lots discovered: {data['total_discovered']}",
            f"- Lots retrieved: {data['total_retrieved']}",
            f"- Errors: {data['total_errors']}",
        ]

    lines = [
        f"# OrbitBid Auction {data['auction_id']}",
        "",
        *status_lines,
        "",
    ]

    for lot in data["lots"]:
        lines.extend(
            [
                "---",
                "",
                f"## Lot {lot['requested_lot_number']} — {md_escape(lot.get('title'))}",
                "",
                f"- OrbitBid item number: {md_escape(lot.get('item_number'))}",
                f"- Internal ID: {lot['internal_id']}",
                f"- Current bid: ${lot.get('amount') if lot.get('amount') is not None else ''}",
                f"- Bid count: {lot.get('bid_count') if lot.get('bid_count') is not None else ''}",
                f"- Photo count: {lot.get('photo_count', 0)}",
                f"- End time (UTC): {epoch_to_iso(lot.get('end_time'))}",
                "",
            ]
        )

        description = clean(lot.get("description"))
        if description:
            lines.extend([f"**Description:** {md_escape(description)}", ""])

        fields = lot.get("fields") or []
        if fields:
            lines.extend(["**Fields:**", ""])
            for field in fields:
                value = clean(field.get("value") or field.get("other_value"))
                label = clean(field.get("label"))
                if label or value:
                    lines.append(f"- {md_escape(label)}: {md_escape(value)}")
            lines.append("")

        images = lot.get("images") or []
        if images:
            lines.extend(["**Photos:**", ""])
            for index, image in enumerate(images, start=1):
                url = image.get("large_path") or image.get("small_path")
                if url:
                    lines.append(f"- [Photo {index}]({url})")
            lines.append("")

    if data["errors"]:
        lines.extend(["---", "", "## Retrieval errors", ""])
        for error in data["errors"]:
            lines.append(f"- Internal ID {error['internal_id']}: {md_escape(error['error'])}")
        lines.append("")

    return "\n".join(lines)


def make_csv(lots: list[dict[str, Any]]) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(
        [
            "lot",
            "item_number",
            "internal_id",
            "current_bid",
            "bid_count",
            "photo_count",
            "status",
            "live_status",
            "end_time",
            "end_time_utc",
            "offer_end_time",
            "offer_end_time_utc",
            "title",
        ]
    )
    for lot in lots:
        writer.writerow(
            [
                lot.get("requested_lot_number"),
                lot.get("item_number"),
                lot.get("internal_id"),
                lot.get("amount"),
                lot.get("bid_count"),
                lot.get("photo_count"),
                lot.get("status"),
                lot.get("live_status"),
                lot.get("end_time"),
                epoch_to_iso(lot.get("end_time")),
                lot.get("offer_end_time"),
                epoch_to_iso(lot.get("offer_end_time")),
                clean(lot.get("title")),
            ]
        )
    return output.getvalue()


def make_readme(data: dict[str, Any]) -> str:
    refreshed = bool(data.get("last_price_refresh_at"))
    if refreshed:
        status = (
            f"- Source: {data['source_url']}\n"
            f"- Last price refresh: {data['retrieved_at']}\n"
            f"- Saved lots refreshed: {data['total_retrieved']}\n"
            f"- Refresh errors: {data['total_errors']}"
        )
    else:
        status = (
            f"- Source: {data['source_url']}\n"
            f"- Retrieved: {data['retrieved_at']}\n"
            f"- Catalog lots discovered: {data['total_discovered']}\n"
            f"- Lots retrieved: {data['total_retrieved']}\n"
            f"- Retrieval errors: {data['total_errors']}"
        )

    return f"""# OrbitBid Auction {data['auction_id']}

Automated snapshot of OrbitBid auction **{data['auction_id']}**.

{status}

## Files

- `summary.md` — readable lot-by-lot snapshot with source photo links
- `summary.csv` — compact current lot index with readable UTC closing times
- `lots.json` — complete structured data used by the photo mirroring workflow
- `price-history.csv` — timestamped bid/bid-count history from exports and price refreshes
- `photos/` — created temporarily by the photo workflow and one-button auction workflow

This export uses OrbitBid's public auction catalog and public lot endpoint. It does not use a bidder login or personal account token.
"""


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/export_orbitbid.py <auction_id>", file=sys.stderr)
        return 2

    auction_id = str(sys.argv[1]).strip()
    if not auction_id.isdigit() or int(auction_id) <= 0:
        print("auction_id must be a positive integer", file=sys.stderr)
        return 2

    source_url = (
        f"{CATALOG_URL}?items=all&auction_id={auction_id}"
        f"&display=grid&limit={PAGE_SIZE}&page=1"
    )

    session = build_session()
    print(f"OrbitBid {auction_id}: discovering catalog lots...")
    lot_ids, catalog_pages = discover_lot_ids(session, auction_id)
    print(f"OrbitBid {auction_id}: discovered {len(lot_ids)} unique lot IDs")

    lots: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for index, internal_id in enumerate(lot_ids, start=1):
        try:
            lot = fetch_lot(session, internal_id)
            lots.append(lot)
            print(
                f"[{index}/{len(lot_ids)}] OK lot {lot['requested_lot_number']} "
                f"| ID {internal_id} | {lot['photo_count']} photos"
            )
        except Exception as exc:
            errors.append({"internal_id": internal_id, "error": str(exc)})
            print(f"[{index}/{len(lot_ids)}] ERROR ID {internal_id}: {exc}", file=sys.stderr)

        time.sleep(LOT_DELAY_SECONDS)
        if index % BATCH_PAUSE_EVERY == 0:
            time.sleep(BATCH_PAUSE_SECONDS)

    if errors:
        raise RuntimeError(
            f"Lot-detail retrieval was incomplete: {len(errors)} of {len(lot_ids)} "
            "catalog lots failed. Refusing to write a partial auction snapshot."
        )

    validate_lot_set(lots)

    retrieved_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    data = {
        "auction_id": int(auction_id),
        "source_url": source_url,
        "catalog_pages": catalog_pages,
        "retrieved_at": retrieved_at,
        "total_discovered": len(lot_ids),
        "total_retrieved": len(lots),
        "total_errors": len(errors),
        "lots": lots,
        "errors": errors,
    }

    if not lots:
        raise RuntimeError("No lot details were retrieved; refusing to write an empty auction snapshot.")

    auction_dir = Path("auctions") / auction_id
    auction_dir.mkdir(parents=True, exist_ok=True)

    (auction_dir / "lots.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (auction_dir / "summary.md").write_text(make_summary(data), encoding="utf-8")
    (auction_dir / "summary.csv").write_text(make_csv(lots), encoding="utf-8", newline="")
    append_price_history(auction_dir, retrieved_at, lots, "export")
    (auction_dir / "README.md").write_text(make_readme(data), encoding="utf-8")

    print(
        f"DONE — {len(lots)} lots retrieved, {len(errors)} errors. "
        f"Wrote {auction_dir}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
