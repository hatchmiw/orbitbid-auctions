#!/usr/bin/env python3
"""Import a sanitized OrbitBid Watch List capture.

The input is intentionally limited to OrbitBid internal lot IDs plus capture
metadata. Authentication credentials, cookies, tokens, bidder identity, card
text, max bids, auto bids, and other authenticated account data are neither
needed nor persisted.

Usage:
    python scripts/import_orbitbid_watchlist.py orbitbid-watchlist.json
    cat orbitbid-watchlist.json | python scripts/import_orbitbid_watchlist.py --stdin
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "orbitbid-watchlist-v1"
SOURCE_HOST = "bid.orbitbid.com"
DEFAULT_OUTPUT = Path("watchlists/orbitbid.json")
MAX_LOTS = 20_000


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def validate_capture(payload: dict[str, Any]) -> tuple[str, list[int]]:
    if payload.get("schema") != SCHEMA:
        raise ValueError(f"Expected schema {SCHEMA!r}.")
    if payload.get("source_host") != SOURCE_HOST:
        raise ValueError(f"Expected source_host {SOURCE_HOST!r}.")

    captured_at = payload.get("captured_at")
    if not isinstance(captured_at, str) or not captured_at.strip():
        raise ValueError("captured_at is required.")

    raw_ids = payload.get("lot_ids")
    if not isinstance(raw_ids, list) or not raw_ids:
        raise ValueError("lot_ids must be a non-empty list.")
    if len(raw_ids) > MAX_LOTS:
        raise ValueError(f"Refusing capture with more than {MAX_LOTS} lot IDs.")

    ids: list[int] = []
    seen: set[int] = set()
    for raw in raw_ids:
        if isinstance(raw, bool):
            raise ValueError("Boolean value is not a valid lot ID.")
        try:
            lot_id = int(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid lot ID: {raw!r}") from exc
        if lot_id <= 0:
            raise ValueError(f"Invalid lot ID: {lot_id}")
        if lot_id not in seen:
            seen.add(lot_id)
            ids.append(lot_id)

    ids.sort()
    return captured_at.strip(), ids


def saved_lot_index(root: Path) -> dict[int, list[dict[str, str]]]:
    index: dict[int, list[dict[str, str]]] = {}
    auctions_dir = root / "auctions"
    if not auctions_dir.exists():
        return index

    for path in sorted(auctions_dir.glob("*/lots.json")):
        auction_id = path.parent.name
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        for lot in data.get("lots") or []:
            internal_id = lot.get("internal_id") or lot.get("id")
            try:
                internal_id = int(internal_id)
            except (TypeError, ValueError):
                continue

            entry = {
                "auction_id": str(auction_id),
                "lot": str(lot.get("requested_lot_number") or lot.get("item_number") or ""),
                "title": str(lot.get("title") or ""),
            }
            index.setdefault(internal_id, []).append(entry)

    return index


def existing_first_seen(output: Path) -> dict[int, str]:
    if not output.exists():
        return {}
    try:
        data = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    result: dict[int, str] = {}
    for lot in data.get("lots") or []:
        try:
            lot_id = int(lot.get("internal_id"))
        except (TypeError, ValueError):
            continue
        first_seen = lot.get("first_seen_at")
        if isinstance(first_seen, str) and first_seen:
            result[lot_id] = first_seen
    return result


def build_import(
    payload: dict[str, Any],
    *,
    root: Path,
    output: Path,
    imported_at: str | None = None,
) -> dict[str, Any]:
    captured_at, lot_ids = validate_capture(payload)
    index = saved_lot_index(root)
    first_seen = existing_first_seen(output)
    imported_at = imported_at or utc_now()

    lots = []
    matched = 0
    for lot_id in lot_ids:
        saved = index.get(lot_id, [])
        if saved:
            matched += 1
        lots.append(
            {
                "internal_id": lot_id,
                "first_seen_at": first_seen.get(lot_id, captured_at),
                "last_seen_at": captured_at,
                "saved_lots": saved,
            }
        )

    return {
        "schema": SCHEMA,
        "captured_at": captured_at,
        "imported_at": imported_at,
        "source_host": SOURCE_HOST,
        "total_lots": len(lots),
        "matched_saved_lots": matched,
        "unmatched_lots": len(lots) - matched,
        "lots": lots,
    }


def read_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.stdin:
        raw = sys.stdin.read()
    else:
        raw = Path(args.input).read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Watch-list capture must be a JSON object.")
    return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="Path to sanitized Watch List JSON.")
    parser.add_argument("--stdin", action="store_true", help="Read sanitized Watch List JSON from stdin.")
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Canonical output path.")
    args = parser.parse_args()
    if bool(args.input) == bool(args.stdin):
        parser.error("Provide exactly one input path or --stdin.")
    return args


def main() -> int:
    args = parse_args()
    root = Path(args.root)
    output = Path(args.output)
    if not output.is_absolute():
        output = root / output

    payload = read_payload(args)
    data = build_import(payload, root=root, output=output)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(
        f"Imported {data['total_lots']} watched OrbitBid lots: "
        f"{data['matched_saved_lots']} matched saved auction lots, "
        f"{data['unmatched_lots']} not yet present in saved auctions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
