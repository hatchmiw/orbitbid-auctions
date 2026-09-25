#!/usr/bin/env python3
"""Auction 1879: validate the single master and derive non-destructive views.

No web scraping, image downloads, invented valuations, or changes to the master.
Run: python scripts/build_auction_review.py 1879
"""
import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ("historical_unverified_resale_low_usd", "historical_unverified_resale_high_usd", "historical_unverified_max_hammer_usd")
ACTIVE = ("indicative_resale_low_usd", "indicative_resale_high_usd", "conditional_max_hammer_usd")
EVIDENCE = ("market_research_status", "market_evidence_urls", "market_research_notes", "market_research_date_utc")
VERIFIED = "Research verified"

def read(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle, strict=True)
        header = next(reader, None)
        if not header or len(header) != len(set(header)):
            raise ValueError("Missing or duplicate CSV header fields")
        rows = []
        for line, values in enumerate(reader, start=2):
            if len(values) != len(header):
                raise ValueError(f"Malformed CSV record {line}: expected {len(header)} fields, got {len(values)}")
            rows.append(dict(zip(header, values)))
        return rows

def write(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def build(auction, check=False):
    directory = ROOT / "auctions" / str(auction)
    source = directory / "catalog-review.csv"
    rows = read(source)
    if not rows:
        raise ValueError("Empty master catalog")
    fields = list(rows[0])
    required = {"lot", "photo_count", "photo_review_status", "photo_findings", "review_note", "priority", *HISTORY, *ACTIVE, *EVIDENCE}
    if not required.issubset(fields):
        raise ValueError("Missing required columns: " + str(sorted(required - set(fields))))
    ids = [row["lot"] for row in rows]
    if any(not value for value in ids) or len(ids) != len(set(ids)):
        raise ValueError("Missing or duplicate lot IDs")
    if str(auction) == "1879" and len(rows) != 487:
        raise ValueError("Auction 1879 must have 487 unique lots")
    for row in rows:
        active = [row[col].strip() for col in ACTIVE]
        if any(active):
            if row["market_research_status"] != VERIFIED:
                raise ValueError("Unverified active price on lot " + row["lot"])
            if not row["market_evidence_urls"].strip() or not row["market_research_notes"].strip() or not row["market_research_date_utc"].strip():
                raise ValueError("Missing evidence, explanation or research date for lot " + row["lot"])
            if not all(active):
                raise ValueError("Incomplete active valuation on lot " + row["lot"])
            lo, hi, cap = map(float, active)
            if not (0 <= lo <= hi and cap >= 0):
                raise ValueError("Invalid value range or hammer ceiling for lot " + row["lot"])
        if row["market_research_status"] == VERIFIED and not all(active):
            raise ValueError("Verified status without complete researched valuation on lot " + row["lot"])
    historical = [row for row in rows if any(row[col].strip() for col in HISTORY)]
    researched = [row for row in rows if row["market_research_status"] == VERIFIED]
    research_queue = [row for row in rows if row["market_research_status"] != VERIFIED]
    priority_order = {"High": 0, "Medium": 1, "Low": 2, "Untriaged": 3}
    research_queue.sort(key=lambda row: (priority_order.get(row["priority"], 3), row["lot"]))
    if check:
        print(f"PASS: {len(rows)} unique lots; {len(historical)} historical estimates; {len(researched)} researched valuations; {len(research_queue)} pending")
        return
    write(directory / "researched-watchlist.csv", researched, fields)
    write(directory / "research-queue.csv", research_queue, fields)
    status = (
        "# Auction " + str(auction) + " — generated review status\\n\\n"
        + f"- Unique catalog lots: **{len(rows)}**\\n"
        + f"- Historical unverified estimates preserved: **{len(historical)}**\\n"
        + f"- Researched valuations with evidence: **{len(researched)}**\\n"
        + f"- Market research pending: **{len(research_queue)}**\\n"
        + f"- Initial contact-sheet/photo-status recorded: **{sum('inspected' in r['photo_review_status'].lower() or 'reviewed' in r['photo_review_status'].lower() for r in rows)}**\\n"
        + "- Historical estimates are not bid recommendations. Research-verified values require source URLs, notes and dates.\\n"
    ).replace("\\n", "\n")
    (directory / "GENERATED_STATUS.md").write_text(status, encoding="utf-8")
    print(f"Generated views for {len(rows)} lots; {len(researched)} researched and {len(research_queue)} pending")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("auction", type=int)
    parser.add_argument("--check", action="store_true", help="Validate only, without modifying any file")
    args = parser.parse_args()
    build(args.auction, args.check)
