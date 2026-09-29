# Auction research agent instructions

Read [AUCTION_REVIEW_SOP.md](AUCTION_REVIEW_SOP.md), the root README, the auction's current `REVIEW.md` and its master catalog before starting. The goal is **useful bidding research**, not exhaustive per-lot original-photo inspection.

1. Rapidly screen the whole catalog using existing descriptions, source photographs and prior contact-sheet notes. Distinguish screening from detailed inspection.
2. Investigate promising lots first, including both personal-use and resale opportunities. For selected candidates, inspect every original photograph individually and research matching dated completed sales. No made-up valuations, bid ceilings or completion claims.
3. Deliver a small, evidence-backed shortlist for the user's review before expanding to more candidates. Preserve the entire catalog and all historical estimates, but keep unverified historical values out of active bid recommendations.
4. Commit completed candidate inspection and research findings to the one master CSV immediately; save screening work in small batches. Verify each write. Do not commit JPGs, ZIPs or contact sheets, duplicate prior inspections, or create parallel checkpoint reports.
5. Continue working after commits until the agreed deliverable is reached or a genuine tool/execution limit intervenes. Keep the exact next research candidate and any blocker in the auction's `REVIEW.md`. Never imply unattended work continues without an actual running workflow.


## Open tooling TODOs

### Make original-photo retrieval direct and reusable

Replace the current selected-photo recovery process that requires editing workflow YAML, committing the edit, triggering a run, unpacking the monolithic full-auction artifact, and re-uploading a temporary selection.

Requirements:
- Use a generic retrieval utility whose workflow definition does **not** change for each request.
- Accept auction_id and one or more lot_ids as runtime inputs.
- Keep a durable manifest/index mapping each auction lot to its original-photo storage location.
- Use predictable artifact/file naming independent of the specific lot requested.
- For future auction ingestion, prefer original-photo storage split into individually retrievable lot archives or reasonably sized lot groups rather than one monolithic full-auction artifact.
- If practical, provide a script/API retrieval path that can fetch a lot's originals directly without starting a GitHub Actions runner.
- Preserve the existing rule that original JPGs are temporary research inputs and are not committed to the repository.
- Document the retrieval command/workflow in the root README and AUCTION_REVIEW_SOP.md once implemented.

**Done when:** an agent can request original photos for an arbitrary previously ingested lot using only auction ID + lot ID(s), without modifying or committing workflow files, and can immediately inspect the returned original-resolution images.
