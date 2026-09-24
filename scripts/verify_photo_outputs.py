#!/usr/bin/env python3
"""Verify that a mirrored OrbitBid photo artifact exactly matches lots.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def lot_number(lot: dict) -> str:
    return str(lot.get("requested_lot_number") or lot.get("item_number") or lot.get("id"))


def expected_photos(lots: list[dict]) -> list[tuple[str, int, str]]:
    expected = []
    for lot in lots:
        number = lot_number(lot)
        for index, image in enumerate(lot.get("images") or [], start=1):
            url = image.get("large_path") or image.get("small_path")
            if url:
                expected.append((number, index, url))
    return expected


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_photo_outputs.py <auction_id>")

    auction_id = sys.argv[1]
    auction_dir = Path("auctions") / auction_id
    lots_path = auction_dir / "lots.json"
    photo_root = auction_dir / "photos"
    manifest_path = photo_root / "manifest.json"

    if not lots_path.is_file() or not manifest_path.is_file():
        raise SystemExit("Missing lots.json or photos/manifest.json")

    data = json.loads(lots_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lots = data.get("lots") or []
    expected = expected_photos(lots)
    expected_set = set(expected)
    expected_dirs = {number for number, _, _ in expected}

    manifest_rows = manifest.get("photos") or []
    actual_set = {
        (str(row.get("lot")), int(row.get("index")), str(row.get("source_url")))
        for row in manifest_rows
    }

    problems = []
    if manifest.get("lot_count") != len(lots):
        problems.append(f"manifest lot_count={manifest.get('lot_count')} expected={len(lots)}")
    if manifest.get("photo_count") != len(expected):
        problems.append(f"manifest photo_count={manifest.get('photo_count')} expected={len(expected)}")
    if manifest.get("error_count"):
        problems.append(f"manifest error_count={manifest.get('error_count')}")
    if len(manifest_rows) != len(expected):
        problems.append(f"manifest rows={len(manifest_rows)} expected={len(expected)}")
    if actual_set != expected_set:
        missing = len(expected_set - actual_set)
        extra = len(actual_set - expected_set)
        problems.append(f"manifest photo mapping mismatch: {missing} missing, {extra} extra")

    actual_dirs = {p.name for p in photo_root.iterdir() if p.is_dir()}
    if actual_dirs != expected_dirs:
        missing = sorted(expected_dirs - actual_dirs)
        extra = sorted(actual_dirs - expected_dirs)
        problems.append(
            f"photo directory mismatch: {len(missing)} missing, {len(extra)} stale/extra"
        )

    missing_reviews = [
        number for number in sorted(expected_dirs)
        if not (photo_root / number / "review.jpg").is_file()
    ]
    if missing_reviews:
        problems.append(f"{len(missing_reviews)} lots are missing review.jpg")

    if problems:
        raise SystemExit("Photo artifact verification failed: " + "; ".join(problems))

    print(
        f"Verified clean photo artifact: {len(lots)} lots, "
        f"{len(expected)} photos, {len(expected_dirs)} review sheets."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
