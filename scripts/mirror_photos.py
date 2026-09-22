#!/usr/bin/env python3
"""
Mirror OrbitBid lot photos into this GitHub repository.

Usage:
    python scripts/mirror_photos.py 1970

Reads:
    auctions/<auction_id>/lots.json

Writes:
    auctions/<auction_id>/photos/<lot>/01.jpg ...
    auctions/<auction_id>/photos/<lot>/README.md
    auctions/<auction_id>/photos/manifest.json
    auctions/<auction_id>/photos/README.md

The original OrbitBid CloudFront URL is preserved in the manifest.
Mirrored images are normalized to JPEG at up to 2048 px on the long edge
to keep the repository usable while retaining enough detail for inspection.
"""

from __future__ import annotations

import io
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from PIL import Image, ImageOps

MAX_EDGE = 2048
JPEG_QUALITY = 88
WORKERS = 6
RETRIES = 3
USER_AGENT = "Mozilla/5.0 OrbitBidAuctionMirror/1.0"


def download_bytes(url: str) -> bytes:
    last_error = None
    for attempt in range(1, RETRIES + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                },
            )
            with urllib.request.urlopen(req, timeout=45) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            if attempt < RETRIES:
                time.sleep(attempt * 2)
    raise RuntimeError(f"Failed after {RETRIES} attempts: {url} ({last_error})")


def normalize_image(raw: bytes, output_path: Path) -> dict:
    with Image.open(io.BytesIO(raw)) as image:
        source_width, source_height = image.size
        image = ImageOps.exif_transpose(image)

        if image.mode not in ("RGB", "L"):
            # Auction photos do not need transparency. Flatten onto white.
            if "A" in image.getbands():
                background = Image.new("RGB", image.size, "white")
                alpha = image.getchannel("A")
                background.paste(image.convert("RGB"), mask=alpha)
                image = background
            else:
                image = image.convert("RGB")
        elif image.mode == "L":
            image = image.convert("RGB")

        image.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        width, height = image.size

        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(
            output_path,
            format="JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True,
        )

    return {
        "source_width": source_width,
        "source_height": source_height,
        "width": width,
        "height": height,
        "bytes": output_path.stat().st_size,
    }


def mirror_one(task: dict) -> dict:
    output_path = task["output_path"]

    if output_path.exists() and output_path.stat().st_size > 0:
        with Image.open(output_path) as image:
            width, height = image.size
        return {
            **task,
            "status": "existing",
            "width": width,
            "height": height,
            "bytes": output_path.stat().st_size,
        }

    raw = download_bytes(task["source_url"])
    meta = normalize_image(raw, output_path)
    return {**task, **meta, "status": "downloaded"}


def clean(value) -> str:
    return " ".join(str(value or "").split())


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/mirror_photos.py <auction_id>", file=sys.stderr)
        return 2

    auction_id = str(sys.argv[1]).strip()
    auction_dir = Path("auctions") / auction_id
    lots_path = auction_dir / "lots.json"

    if not lots_path.exists():
        print(f"Missing {lots_path}", file=sys.stderr)
        return 2

    with lots_path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)

    lots = data.get("lots", [])
    photo_root = auction_dir / "photos"
    photo_root.mkdir(parents=True, exist_ok=True)

    tasks = []
    for lot in lots:
        lot_number = str(lot.get("requested_lot_number") or lot.get("item_number") or lot.get("id"))
        for index, image in enumerate(lot.get("images") or [], start=1):
            source_url = image.get("large_path") or image.get("small_path")
            if not source_url:
                continue
            tasks.append(
                {
                    "lot": lot_number,
                    "index": index,
                    "source_url": source_url,
                    "output_path": photo_root / lot_number / f"{index:02d}.jpg",
                    "source_image_id": image.get("id"),
                }
            )

    print(f"Auction {auction_id}: {len(lots)} lots, {len(tasks)} photos")

    results = []
    errors = []

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(mirror_one, task): task for task in tasks}
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(
                    f"[{result['status']}] lot {result['lot']} photo "
                    f"{result['index']:02d} -> {result['output_path']}"
                )
            except Exception as exc:
                errors.append(
                    {
                        "lot": task["lot"],
                        "index": task["index"],
                        "source_url": task["source_url"],
                        "error": str(exc),
                    }
                )
                print(
                    f"[ERROR] lot {task['lot']} photo {task['index']:02d}: {exc}",
                    file=sys.stderr,
                )

    results.sort(key=lambda x: (int(x["lot"]), x["index"]))

    lots_by_number = {
        str(lot.get("requested_lot_number") or lot.get("item_number") or lot.get("id")): lot
        for lot in lots
    }

    # Per-lot README files.
    for lot_number, lot in lots_by_number.items():
        lot_results = [r for r in results if r["lot"] == lot_number]
        if not lot_results:
            continue

        lines = [
            f"# Lot {lot_number}",
            "",
            clean(lot.get("title")),
            "",
            f"- Snapshot bid: ${lot.get('amount', '')}",
            f"- Bid count: {lot.get('bid_count', '')}",
            f"- Mirrored photos: {len(lot_results)}",
            "",
        ]

        for r in lot_results:
            filename = Path(r["output_path"]).name
            lines += [
                f"## Photo {r['index']}",
                "",
                f"![Lot {lot_number} photo {r['index']}]({filename})",
                "",
                f"[Original OrbitBid image]({r['source_url']})",
                "",
            ]

        lot_readme = photo_root / lot_number / "README.md"
        lot_readme.write_text("\n".join(lines), encoding="utf-8")

    manifest = {
        "auction_id": int(auction_id) if auction_id.isdigit() else auction_id,
        "source_snapshot": str(lots_path),
        "lot_count": len(lots),
        "photo_count": len(results),
        "error_count": len(errors),
        "max_edge": MAX_EDGE,
        "jpeg_quality": JPEG_QUALITY,
        "photos": [
            {
                "lot": r["lot"],
                "index": r["index"],
                "source_image_id": r.get("source_image_id"),
                "source_url": r["source_url"],
                "repo_path": str(r["output_path"]).replace("\\", "/"),
                "width": r.get("width"),
                "height": r.get("height"),
                "bytes": r.get("bytes"),
            }
            for r in results
        ],
        "errors": errors,
    }

    (photo_root / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    index_lines = [
        f"# Auction {auction_id} Photo Mirror",
        "",
        f"- Lots in snapshot: {len(lots)}",
        f"- Photos mirrored: {len(results)}",
        f"- Errors: {len(errors)}",
        "",
        "Each lot below has its own folder and gallery page.",
        "",
    ]

    for lot in lots:
        lot_number = str(lot.get("requested_lot_number") or lot.get("item_number") or lot.get("id"))
        count = sum(1 for r in results if r["lot"] == lot_number)
        if not count:
            continue
        title = clean(lot.get("title"))
        index_lines.append(
            f"- [Lot {lot_number}](./{lot_number}/README.md) — {count} photos — {title}"
        )

    (photo_root / "README.md").write_text(
        "\n".join(index_lines) + "\n",
        encoding="utf-8",
    )

    print("")
    print(f"DONE: {len(results)} photos mirrored; {len(errors)} errors.")
    if errors:
        print("See photos/manifest.json for failures.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
