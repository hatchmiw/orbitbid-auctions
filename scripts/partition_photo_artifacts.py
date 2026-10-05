#!/usr/bin/env python3
"""Partition temporary OrbitBid photos into connector-sized artifacts.

Reads:
    auctions/<auction_id>/photos/
    auctions/<auction_id>/photos/manifest.json

Writes:
    .artifact-staging/<auction_id>/review-sheets/
    .artifact-staging/<auction_id>/photos-001/ ...
    auctions/<auction_id>/photo-artifact-index.json

Only the JSON index is intended to be committed. The staging directory and
auction photo workspace are ignored by Git and should be deleted after upload.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from mirror_photos import lot_sort_key

DEFAULT_TARGET_MIB = 275
DEFAULT_HARD_MAX_MIB = 450
MAX_UPLOAD_SHARDS = 20


def mib(value: float) -> int:
    return int(value * 1024 * 1024)


def safe_link_or_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, target)
    except OSError:
        shutil.copy2(source, target)


def file_bytes(paths: Iterable[Path]) -> int:
    return sum(path.stat().st_size for path in paths if path.is_file())


def lot_payload_files(lot_dir: Path) -> list[Path]:
    files = sorted(
        [
            path
            for path in lot_dir.iterdir()
            if path.is_file() and (path.suffix.lower() == ".jpg" or path.name == "README.md")
        ],
        key=lambda path: path.name,
    )
    return files


def lot_original_photo_files(lot_dir: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in lot_dir.glob("*.jpg")
            if path.name not in {"review.jpg", "contact.jpg"}
        ],
        key=lambda path: path.name,
    )


def plan_shards(
    lots: list[tuple[str, int]],
    target_bytes: int,
    hard_max_bytes: int,
) -> list[list[tuple[str, int]]]:
    """Greedily group whole lots without splitting a lot between artifacts."""
    if target_bytes <= 0 or hard_max_bytes <= 0 or target_bytes > hard_max_bytes:
        raise ValueError("Invalid shard size limits")

    shards: list[list[tuple[str, int]]] = []
    current: list[tuple[str, int]] = []
    current_bytes = 0

    for lot, size in lots:
        if size > hard_max_bytes:
            raise ValueError(
                f"Lot {lot} is {size} bytes, above the hard artifact ceiling "
                f"of {hard_max_bytes} bytes"
            )

        if current and current_bytes + size > target_bytes:
            shards.append(current)
            current = []
            current_bytes = 0

        current.append((lot, size))
        current_bytes += size

    if current:
        shards.append(current)

    return shards


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("auction_id")
    parser.add_argument("--target-mib", type=float, default=DEFAULT_TARGET_MIB)
    parser.add_argument("--hard-max-mib", type=float, default=DEFAULT_HARD_MAX_MIB)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--cleanup-at", default="")
    args = parser.parse_args()

    auction_id = str(args.auction_id).strip()
    photo_root = Path("auctions") / auction_id / "photos"
    manifest_path = photo_root / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Missing {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("error_count"):
        raise SystemExit("Cannot partition a photo mirror containing download errors")

    staging_root = Path(".artifact-staging") / auction_id
    if staging_root.exists():
        shutil.rmtree(staging_root)
    staging_root.mkdir(parents=True)

    lot_dirs = sorted(
        [path for path in photo_root.iterdir() if path.is_dir()],
        key=lambda path: lot_sort_key(path.name),
    )

    lot_sizes: list[tuple[str, int]] = []
    lot_original_counts: dict[str, int] = {}
    for lot_dir in lot_dirs:
        originals = lot_original_photo_files(lot_dir)
        if not originals:
            continue
        payload = lot_payload_files(lot_dir)
        size = file_bytes(payload)
        lot_sizes.append((lot_dir.name, size))
        lot_original_counts[lot_dir.name] = len(originals)

    target_bytes = mib(args.target_mib)
    hard_max_bytes = mib(args.hard_max_mib)
    shards = plan_shards(lot_sizes, target_bytes, hard_max_bytes)
    if len(shards) > MAX_UPLOAD_SHARDS:
        raise SystemExit(
            f"Partition requires {len(shards)} shards but the workflow supports "
            f"at most {MAX_UPLOAD_SHARDS}. Lower photo resolution or raise the workflow shard capacity."
        )

    review_root = staging_root / "review-sheets"
    review_lots: list[str] = []
    review_bytes = 0
    for lot_dir in lot_dirs:
        review = lot_dir / "review.jpg"
        if not review.is_file():
            continue
        target = review_root / lot_dir.name / "review.jpg"
        safe_link_or_copy(review, target)
        review_lots.append(lot_dir.name)
        review_bytes += review.stat().st_size

    review_manifest = {
        "auction_id": int(auction_id) if auction_id.isdigit() else auction_id,
        "artifact_name": f"orbitbid-{auction_id}-review-sheets",
        "lots": review_lots,
        "lot_count": len(review_lots),
        "bytes": review_bytes,
    }
    review_root.mkdir(parents=True, exist_ok=True)
    (review_root / "manifest.json").write_text(
        json.dumps(review_manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    shard_rows = []
    lot_to_artifact: dict[str, str] = {}

    for shard_number, planned in enumerate(shards, start=1):
        artifact_name = f"orbitbid-{auction_id}-photos-{shard_number:03d}"
        shard_root = staging_root / f"photos-{shard_number:03d}"
        selected_lots = [lot for lot, _ in planned]
        shard_bytes = 0
        shard_photo_count = 0

        for lot in selected_lots:
            source_dir = photo_root / lot
            target_dir = shard_root / lot
            for source in lot_payload_files(source_dir):
                safe_link_or_copy(source, target_dir / source.name)
                shard_bytes += source.stat().st_size
            shard_photo_count += lot_original_counts[lot]
            lot_to_artifact[lot] = artifact_name

        if shard_bytes > hard_max_bytes:
            raise SystemExit(
                f"{artifact_name} is {shard_bytes} bytes, above the hard ceiling "
                f"of {hard_max_bytes} bytes"
            )

        shard_manifest = {
            "auction_id": int(auction_id) if auction_id.isdigit() else auction_id,
            "artifact_name": artifact_name,
            "shard_number": shard_number,
            "lots": selected_lots,
            "lot_count": len(selected_lots),
            "photo_count": shard_photo_count,
            "bytes": shard_bytes,
        }
        shard_root.mkdir(parents=True, exist_ok=True)
        (shard_root / "manifest.json").write_text(
            json.dumps(shard_manifest, indent=2) + "\n",
            encoding="utf-8",
        )
        shard_rows.append(shard_manifest)

    indexed_lots = set(lot_to_artifact)
    expected_lots = {lot for lot, _ in lot_sizes}
    if indexed_lots != expected_lots:
        raise SystemExit(
            f"Artifact index mismatch: {len(expected_lots-indexed_lots)} missing, "
            f"{len(indexed_lots-expected_lots)} extra"
        )

    total_originals = sum(lot_original_counts.values())
    if total_originals != int(manifest.get("photo_count") or 0):
        raise SystemExit(
            f"Photo count mismatch: source manifest={manifest.get('photo_count')} "
            f"partitioned={total_originals}"
        )

    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    index = {
        "version": 1,
        "auction_id": int(auction_id) if auction_id.isdigit() else auction_id,
        "generated_at": generated_at,
        "workflow_run_id": int(args.run_id) if str(args.run_id).isdigit() else args.run_id,
        "cleanup_at": args.cleanup_at or None,
        "retention_policy": "temporary GitHub Actions artifacts; delete after final auction close plus 7 days",
        "connector_download_hard_limit_mib": 512,
        "shard_target_mib": args.target_mib,
        "shard_hard_max_mib": args.hard_max_mib,
        "source_photo_count": total_originals,
        "review_sheets": review_manifest,
        "photo_shards": shard_rows,
        "lot_to_artifact": lot_to_artifact,
    }

    index_path = Path("auctions") / auction_id / "photo-artifact-index.json"
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    print(
        f"Prepared {len(shards)} original-photo artifacts for {len(indexed_lots)} lots "
        f"and one review-sheet artifact for {len(review_lots)} lots."
    )
    for row in shard_rows:
        print(
            f"{row['artifact_name']}: {row['lot_count']} lots, "
            f"{row['photo_count']} originals, {row['bytes'] / 1024 / 1024:.1f} MiB"
        )
    print(
        f"{review_manifest['artifact_name']}: {len(review_lots)} sheets, "
        f"{review_bytes / 1024 / 1024:.1f} MiB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
