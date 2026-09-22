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


def discover_lot_ids(session: requests.Session, auction_id: str) -> tuple[list[int], list[str]]:
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

        html = response.text
        page_ids = [int(x) for x in re.findall(r"/lot/(\d+)(?:/|[?\"'])", html)]
        if not page_ids:
            page_ids = [int(x) for x in re.findall(r"/lot/(\d+)", html)]

        unique_page_ids: list[int] = []
        page_seen: set[int] = set()
        for lot_id in page_ids:
            if lot_id not in page_seen:
                page_seen.add(lot_id)
                unique_page_ids.append(lot_id)

        fresh = [lot_id for lot_id in unique_page_ids if lot_id not in seen]
        print(f"Catalog page {page}: {len(unique_page_ids)} lot links, {len(fresh)} new")

        if fresh:
            page_urls.append(url)
            for lot_id in fresh:
                seen.add(lot_id)
                all_ids.append(lot_id)
        else:
            break

        time.sleep(PAGE_DELAY_SECONDS)

    if not all_ids:
        raise RuntimeError(
            "No OrbitBid lot IDs were discovered. The catalog markup may have changed "
            "or the auction may not be publicly accessible."
        )

    return all_ids, page_urls


def fetch_lot(session: requests.Session, internal_id: int) -> dict[str, Any]:
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "x-client-host": "bid.orbitbid.com",
        "x-client-token": CLIENT_TOKEN,
        "x-operation-name": "getPublicLot",
        "origin": "https://bid.orbitbid.com",
        "referer": "https://bid.orbitbid.com/",
    }
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


def make_summary(data: dict[str, Any]) -> str:
    lines = [
        f"# OrbitBid Auction {data['auction_id']}",
        "",
        f"- Retrieved: {data['retrieved_at']}",
        f"- Source: {data['source_url']}",
        f"- Catalog lots discovered: {data['total_discovered']}",
        f"- Lots retrieved: {data['total_retrieved']}",
        f"- Errors: {data['total_errors']}",
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
                f"- End time: {lot.get('end_time') or ''}",
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
                clean(lot.get("title")),
            ]
        )
    return output.getvalue()


def make_readme(data: dict[str, Any]) -> str:
    return f"""# OrbitBid Auction {data['auction_id']}

Automated snapshot of OrbitBid auction **{data['auction_id']}**.

- Source: {data['source_url']}
- Retrieved: {data['retrieved_at']}
- Catalog lots discovered: {data['total_discovered']}
- Lots retrieved: {data['total_retrieved']}
- Retrieval errors: {data['total_errors']}

## Files

- `summary.md` — readable lot-by-lot snapshot with source photo links
- `summary.csv` — compact lot index
- `lots.json` — complete structured data used by the photo mirroring workflow
- `photos/` — created by the separate **Mirror auction photos** GitHub Action

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
    (auction_dir / "README.md").write_text(make_readme(data), encoding="utf-8")

    print(
        f"DONE — {len(lots)} lots retrieved, {len(errors)} errors. "
        f"Wrote {auction_dir}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
