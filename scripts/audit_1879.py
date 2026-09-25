#!/usr/bin/env python3
"""Read-only, reproducible audit of OrbitBid 1879 review completion.

Do not infer original-image inspection from contact sheets, artifacts or filenames.
Do not treat historical estimates as researched prices.
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "auctions" / "1879"
MASTER = DIR / "catalog-review.csv"
HIST = ("historical_unverified_resale_low_usd", "historical_unverified_resale_high_usd", "historical_unverified_max_hammer_usd")
ACTIVE = ("indicative_resale_low_usd", "indicative_resale_high_usd", "conditional_max_hammer_usd")


def audit():
    with MASTER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, strict=True)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)) or len(fields) != 26:
            raise ValueError("Master must have 26 unique columns")
        rows = list(reader)
    if len(rows) != 487 or len({r["lot"] for r in rows}) != 487:
        raise ValueError("Master must have exactly 487 unique lots")
    for row in rows:
        if None in row or len(row) != 26:
            raise ValueError("Malformed record for lot " + str(row.get("lot")))
        if any(row[k].strip() for k in ACTIVE):
            if row["market_research_status"] != "Research verified" or not all(
                row[k].strip() for k in ("market_evidence_urls", "market_research_notes", "market_research_date_utc", *ACTIVE)
            ):
                raise ValueError("Unsupported active valuation for lot " + row["lot"])
    no_photo = [r["lot"] for r in rows if int(r["photo_count"]) == 0]
    if set(no_photo) != {"18284", "18583"}:
        raise ValueError("Unexpected no-photo lot IDs: " + repr(no_photo))
    documented = [r["lot"] for r in rows if r["photo_review_status"] == "Original photos examined (10-lot full-image pass)"]
    additional_claims = [r["lot"] for r in rows if "all " in r["photo_review_status"].lower() and "original" in r["photo_review_status"].lower() and "individually inspected" in r["photo_review_status"].lower()]
    original = documented + additional_claims
    # Explicit original-photo status is the minimum criterion; evidence still needs
    # checking against the per-lot notes and actual source images.
    contact = [r["lot"] for r in rows if "contact sheet" in r["photo_review_status"].lower()]
    verified = [r["lot"] for r in rows if r["market_research_status"] == "Research verified"]
    historical = [r["lot"] for r in rows if any(r[k].strip() for k in HIST)]
    report = {
        "catalog_lots": len(rows),
        "pictured_lots": len(rows) - len(no_photo),
        "no_photo_lots": no_photo,
        "documented_original_inspections": len(documented),
        "documented_original_lot_ids": documented,
        "additional_original_inspection_claims_pending_provenance": len(additional_claims),
        "additional_claim_lot_ids": additional_claims,
        "original_image_status_claims": len(original),
        "original_image_status_lot_ids": original,
        "contact_sheet_status_lots": len(contact),
        "market_verified_lots": len(verified),
        "market_verified_lot_ids": verified,
        "historical_unverified_estimate_lots": len(historical),
        "remaining_without_independently_documented_original_inspection": len(rows) - len(no_photo) - len(documented),
        "remaining_without_any_original_inspection_status_claim": len(rows) - len(no_photo) - len(original),
        "remaining_market_research": len(rows) - len(verified),
        "photo_status_distribution": dict(Counter(r["photo_review_status"] for r in rows)),
    }
    return report


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
