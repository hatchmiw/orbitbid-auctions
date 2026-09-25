# OrbitBid 1879 — current authoritative review status

**Governing procedure:** [OrbitBid SOP v2](../../AUCTION_REVIEW_SOP.md). Per-lot master: [catalog-review.csv](catalog-review.csv). Source catalog and original photo URLs: [lots.json](lots.json). Do not edit generated views or repeat documented inspections.

## Reconciled status — 2026-09-25 cleanup
- **487 unique catalog lots**; **485 pictured**; **2 no-photo lots**: 18284 and 18583.
- All 485 pictured lots have **initial contact-sheet-level findings** in the master or historical batch reports. Contact-sheet review does not satisfy the requested individual-original review.
- **20 distinct pictured lots** have original-image inspections documented in [full-image-price-review.md](full-image-price-review.md), covering **106 originals**: 18457, 18458, 18463, 18467, 18469, 18471, 18472, 18473, 30-1329, 30-1330, 18474, 18475, 18476, 18477, 18478, 18479, 18480, 18482, 18483, 18484. These 20 already have `Original photos examined (10-lot full-image pass)` in the master. Do **not** re-inspect or double-count lot 18457: the duplicate September 25 standalone checkpoint was archived after comparison; it repeated the same five originals and added no necessary distinct completion record.
- **Nine additional master rows claim** `All N original JPGs individually inspected 2026-09-25`: 18100, 18103, 18106, 18131, 18135, 18160, 18203, 18214, 18222. Their individual original-image evidence/provenance has **not** been reconciled to a separate inspection report in this cleanup. Treat as **nine claims requiring verification**, not nine newly certified completions.
- Therefore **20 independently documented** full-original inspections; **29 master status claims**; **465 pictured lots** not independently documented as complete until the nine claims are verified (potentially **456** if all nine are confirmed).
- **290 historical heuristic estimates** retained only in `historical_unverified_*` fields; **0 active evidence-verified valuations**. Preliminary research for 18439, 18440, 18608, 18556, 18548 and 18287 remains in [market-research.md](market-research.md). No unsupported active bid ceilings.
- Existing source bid snapshot is 2026-09-24 17:32:58 UTC; it is not live.

## Artifact reuse
Full source run `36039298628`, artifact `10825787468` (1.55 GB, above 512 MiB connector limit). Batch 07 run `36087152300`, artifact `10844646656`. Split batches 08–13 run `36087642169`: artifact IDs `10844397014`, `10844157362`, `10844052609`, `10844227160`, `10844526785`, `10843977621`. They were unexpired when last checked September 25 and were expected to expire around October 7; **recheck** before use. Batch 08 ZIP has been downloaded previously. For batches 01–06 first locate existing smaller artifacts; if needed split the already-mirrored full archive using `.github/workflows/review-from-existing-artifact.yml`, without a new OrbitBid download.

## Exact resume checkpoint
1. Before inspecting any more photos, reconcile the nine original-image claims against original image counts and actual prior inspection evidence. Do not repeat the 20 documented lots.
2. For the remaining lot IDs, inspect **every original JPG individually**, merge findings directly into the master and validate/commit after every 20 newly completed lots, then continue.
3. Research all required lots using matching dated completed-sale evidence; record insufficient-evidence cases without inventing prices. Preserve previous research.
4. Regenerate `research-queue.csv`, `researched-watchlist.csv` and `GENERATED_STATUS.md` using `python scripts/build_auction_review.py 1879`; validate with `--check`.
5. Do not stop at a checkpoint; stop only at full verified completion or a genuine execution/tool blocker, with exact last/next lot and photo recorded here.

## Archived, non-authoritative history
Previous SOP, old completion narrative, old research workflow and duplicate 18457 checkpoint are preserved under [archive/2026-09-25-pre-cleanup](../../archive/2026-09-25-pre-cleanup/). Existing batch reports and [full-image-price-review.md](full-image-price-review.md) remain historical evidence, not separate editable completion ledgers. The withdrawn provisional watchlist is archived at [`1879__provisional-watchlist.csv`](../../archive/2026-09-25-pre-cleanup/1879__provisional-watchlist.csv) and is **not** a bidding sheet.
