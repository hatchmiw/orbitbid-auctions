# Auction research agent instructions

Read [AUCTION_REVIEW_SOP.md](AUCTION_REVIEW_SOP.md), the root README, the auction's current `REVIEW.md` and its master catalog before starting. The goal is **useful bidding research**, not exhaustive per-lot original-photo inspection.

1. Rapidly screen the whole catalog using existing descriptions, source photographs and prior contact-sheet notes. Distinguish screening from detailed inspection.
2. Investigate promising lots first, including both personal-use and resale opportunities. For selected candidates, inspect every original photograph individually and research matching dated completed sales. No made-up valuations, bid ceilings or completion claims.
3. Deliver a small, evidence-backed shortlist for the user's review before expanding to more candidates. Preserve the entire catalog and all historical estimates, but keep unverified historical values out of active bid recommendations.
4. Commit completed candidate inspection and research findings to the one master CSV immediately; save screening work in small batches. Verify each write. Do not commit JPGs, ZIPs or contact sheets, duplicate prior inspections, or create parallel checkpoint reports.
5. Continue working after commits until the agreed deliverable is reached or a genuine tool/execution limit intervenes. Keep the exact next research candidate and any blocker in the auction's `REVIEW.md`. Never imply unattended work continues without an actual running workflow.


## Photo artifact retrieval

New auction ingestions use temporary, connector-sized photo artifacts rather than one monolithic archive.

- Download `orbitbid-<auction-id>-review-sheets` for whole-catalog screening.
- Read `auctions/<auction-id>/photo-artifact-index.json` to map any pictured lot to its numbered `orbitbid-<auction-id>-photos-NNN` artifact.
- Download only the shard(s) covering shortlisted lots, then inspect every JPG for those lots individually.
- Photo artifacts are temporary and follow final auction close + 7 days retention. JPGs, ZIPs and contact sheets must never be committed.
- Older monolithic artifacts may still use **Extract OrbitBid photo subset** as a recovery helper, but new ingestion should not create monolithic photo artifacts.

The ingestion workflow targets 275 MiB per numbered photo shard and rejects any shard above 450 MiB so connector downloads remain below the 512 MiB limit.
