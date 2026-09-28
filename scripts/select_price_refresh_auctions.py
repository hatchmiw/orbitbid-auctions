#!/usr/bin/env python3
"""Select saved OrbitBid auctions that should receive a scheduled price refresh.

Hourly mode refreshes every saved auction until six hours after its final
scheduled lot close. Auction-day mode refreshes only auctions whose final
scheduled close falls on today's America/Detroit calendar date.

Output is one auction ID per line. Manual workflow dispatch does not use this
selector.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

AUCTIONS_DIR = Path("auctions")
LOCAL_TZ = ZoneInfo("America/Detroit")
POST_CLOSE_HOURS = 6


def lot_close_timestamp(lot: dict) -> int | None:
    values = []
    for key in ("end_time", "offer_end_time"):
        value = lot.get(key)
        if value in (None, ""):
            continue
        try:
            values.append(int(value))
        except (TypeError, ValueError):
            pass
    return max(values) if values else None


def auction_close_timestamps(path: Path) -> list[int]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    return [
        ts
        for lot in (data.get("lots") or [])
        if (ts := lot_close_timestamp(lot)) is not None
    ]


def select(mode: str, now_ts: int) -> list[str]:
    now_utc = datetime.fromtimestamp(now_ts, timezone.utc)
    now_local_date = now_utc.astimezone(LOCAL_TZ).date()
    cutoff_seconds = POST_CLOSE_HOURS * 3600
    selected = []

    if not AUCTIONS_DIR.exists():
        return selected

    for path in sorted(AUCTIONS_DIR.glob("*/lots.json")):
        auction_id = path.parent.name
        close_times = auction_close_timestamps(path)
        if not close_times:
            print(f"Skipping {auction_id}: no valid lot close time", file=__import__("sys").stderr)
            continue

        final_close_ts = max(close_times)
        if now_ts > final_close_ts + cutoff_seconds:
            continue

        if mode == "auction-day":
            close_local_dates = {
                datetime.fromtimestamp(ts, timezone.utc).astimezone(LOCAL_TZ).date()
                for ts in close_times
            }
            # Any day with a scheduled lot close gets the 10-minute cadence.
            # Keep that cadence through the post-final-close grace period even
            # when the six-hour window crosses local midnight.
            in_post_close_grace = final_close_ts <= now_ts <= final_close_ts + cutoff_seconds
            if now_local_date not in close_local_dates and not in_post_close_grace:
                continue

        selected.append(auction_id)

    return selected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("hourly", "auction-day"))
    parser.add_argument("--now", type=int, default=int(time.time()), help="Unix timestamp for tests/debugging")
    args = parser.parse_args()

    for auction_id in select(args.mode, args.now):
        print(auction_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
