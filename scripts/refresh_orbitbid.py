#!/usr/bin/env python3
"""Refresh changing OrbitBid lot data for an already-saved auction.

Usage:
    python scripts/refresh_orbitbid.py 1970

Reads the internal lot IDs already stored in auctions/<id>/lots.json, so it
cannot accidentally discover unrelated auctions. Photos are never downloaded
or modified.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import export_orbitbid as base


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/refresh_orbitbid.py <auction_id>", file=sys.stderr)
        return 2

    auction_id = sys.argv[1].strip()
    path = Path("auctions") / auction_id / "lots.json"
    if not path.exists():
        print(f"Missing {path}", file=sys.stderr)
        return 2

    old = json.loads(path.read_text(encoding="utf-8"))
    old_lots = old.get("lots") or []
    if not old_lots:
        raise RuntimeError("Saved auction contains no lots.")

    session = base.build_session()
    refreshed = []
    errors = []

    for index, old_lot in enumerate(old_lots, start=1):
        internal_id = old_lot.get("internal_id") or old_lot.get("id")
        if not internal_id:
            errors.append({"internal_id": None, "error": "Missing internal ID"})
            continue
        try:
            lot = base.fetch_lot(session, int(internal_id))
            refreshed.append(lot)
            print(
                f"[{index}/{len(old_lots)}] lot {lot['requested_lot_number']} "
                f"bid={lot.get('amount')} bids={lot.get('bid_count')}"
            )
        except Exception as exc:
            # Preserve the old record rather than dropping a lot from the snapshot.
            refreshed.append(old_lot)
            errors.append({"internal_id": internal_id, "error": str(exc)})
            print(f"[ERROR] internal ID {internal_id}: {exc}", file=sys.stderr)

        time.sleep(base.LOT_DELAY_SECONDS)
        if index % base.BATCH_PAUSE_EVERY == 0:
            time.sleep(base.BATCH_PAUSE_SECONDS)

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    data = dict(old)
    # Older browser-export snapshots (including auction 1970) predate some
    # metadata keys used by the GitHub exporter. Supply compatible defaults
    # without rediscovering the auction catalog.
    data.setdefault(
        "source_url",
        f"https://bid.orbitbid.com/?items=all&auction_id={auction_id}&display=grid&limit=60&page=1",
    )
    data.setdefault("total_discovered", len(old_lots))
    data.setdefault("catalog_pages", [data["source_url"]])
    data["retrieved_at"] = now
    data["last_price_refresh_at"] = now
    data["total_retrieved"] = len(refreshed)
    data["total_errors"] = len(errors)
    data["lots"] = refreshed
    data["errors"] = errors

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (path.parent / "summary.md").write_text(base.make_summary(data), encoding="utf-8")
    (path.parent / "summary.csv").write_text(base.make_csv(refreshed), encoding="utf-8", newline="")
    base.append_price_history(path.parent, now, refreshed, "refresh")
    (path.parent / "README.md").write_text(base.make_readme(data), encoding="utf-8")

    print(f"DONE — refreshed {len(refreshed)} saved lots; {len(errors)} errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
