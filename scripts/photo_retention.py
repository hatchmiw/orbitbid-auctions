#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

KEEP_AFTER_CLOSE = timedelta(days=7)
MAX_ARTIFACT_RETENTION_DAYS = 90


def epoch_value(raw):
    if raw in (None, "", 0, "0"):
        return None
    try:
        value = int(float(raw))
    except (TypeError, ValueError):
        return None
    if value > 10_000_000_000:
        value //= 1000
    return value


def load_info(lots_path: Path):
    data = json.loads(lots_path.read_text(encoding="utf-8"))
    auction_id = str(data.get("auction_id") or lots_path.parent.name)

    closes = []
    for lot in data.get("lots") or []:
        for key in ("end_time", "offer_end_time"):
            value = epoch_value(lot.get(key))
            if value is not None:
                closes.append(value)

    if not closes:
        raise ValueError("No OrbitBid lot closing timestamps found")

    close = datetime.fromtimestamp(max(closes), tz=timezone.utc)
    cleanup = close + KEEP_AFTER_CLOSE
    return auction_id, close, cleanup


def one_auction(auction_id: str) -> int:
    lots_path = Path("auctions") / auction_id / "lots.json"
    if not lots_path.exists():
        print(f"Missing {lots_path}", file=sys.stderr)
        return 2

    _, close, cleanup = load_info(lots_path)
    now = datetime.now(timezone.utc)
    seconds = (cleanup - now).total_seconds()
    days = max(1, math.ceil(seconds / 86400))
    retention_days = min(days, MAX_ARTIFACT_RETENTION_DAYS)
    expired = now >= cleanup

    print(f"expired={'true' if expired else 'false'}")
    print(f"cleanup_at={cleanup.isoformat()}")
    print(f"retention_days={retention_days}")
    print(f"auction_close={close.isoformat()}")
    return 0


def due_auctions() -> int:
    now = datetime.now(timezone.utc)
    for lots_path in sorted(Path("auctions").glob("*/lots.json")):
        try:
            auction_id, _, cleanup = load_info(lots_path)
        except Exception as exc:
            print(f"WARNING: {lots_path}: {exc}", file=sys.stderr)
            continue
        if now >= cleanup:
            print(auction_id)
    return 0


def main() -> int:
    if len(sys.argv) == 2 and sys.argv[1] == "--due":
        return due_auctions()
    if len(sys.argv) == 2:
        return one_auction(sys.argv[1].strip())
    print("Usage: photo_retention.py <auction_id> | --due", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
