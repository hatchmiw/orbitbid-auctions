# OrbitBid 1879 — auction review checkpoint

**Pass completed:** all 487 catalog entries triaged; **200 distinct pictured lots / 1499 current-source photographs** visually inspected in five independently verified batches; 200 provisional watchlist valuations and conditional hammer ceilings. Source bid snapshot is September 24, 2026, 17:32:58 UTC; no live bid refresh was done by this photo workflow.

**Batch 06 resumed:** sixteen of the 40 queued source-verified contact sheets have now been visually inspected and documented in [batch-06 partial report](visual-review-batch-06-partial.md); 24 queued batch-06 sheets still need inspection. Completed batches 01–05 remain unchanged. The 16 partial findings have not yet been assigned bid ceilings or merged into the 200-row watchlist.

**Not completed:** source-photo visual review of 277 remaining pictured lots (24 in the rest of batch 06 and 245 beyond it), confirmation of two photo-free entries, physical operation and safety checks, exact-match sold comps for most candidates and live bid refresh. This is not yet a complete 487-lot photographic appraisal.

## Completed visual-inspection batches

- [Batch 01](visual-review-batch-01.md): 40 distinct lots and 246 verified catalog images; [contact sheets](review-previews/README.md).
- [Batch 02](visual-review-batch-02.md): 40 distinct lots and 352 verified catalog images; [contact sheets](review-previews/batch-02/README.md).
- [Batch 03](visual-review-batch-03.md): 40 distinct lots and 286 verified catalog images; [contact sheets](review-previews/batch-03/README.md).
- [Batch 04](visual-review-batch-04.md): 40 distinct lots and 301 verified catalog images; [contact sheets](review-previews/batch-04/README.md).
- [Batch 05](visual-review-batch-05.md): 40 distinct lots and 314 verified catalog images; [contact sheets](review-previews/batch-05/README.md).
- **200 lots / 1499 photographs fully reviewed in completed batches**; 16 additional batch-06 lots have photo-specific findings (216 pictured lots inspected in total), 269 pictured lots still awaiting visual inspection, and two catalog entries have no photos.

## Files

- [catalog-review.csv](catalog-review.csv): all 487 catalog lots with 200 verified visual notes and permanent photo sheet links.
- [provisional-watchlist.csv](provisional-watchlist.csv): 200 conditionally priced candidates, all visually reviewed across batches 01–05.
- [all-lots-review.md](all-lots-review.md): readable per-lot review table for every lot.
- [summary.md](summary.md): original unabridged descriptions and every source photo link.
- [price-history.csv](price-history.csv): existing timestamped price history (not altered here).

## Valuation method and limits

Gross resale ranges are illustrative used-market **working-condition scenarios**, not verified current sold prices for these exact lots. They exclude resale commissions, shipping, cleaning and repairs. Provisional caps are **maximum hammer bids** only if functional/condition checks pass; no bid is justified solely because it is below the cap. The initial source catalog often shows a $5 opening amount, which is not evidence of low closing demand. Buyer premium, Michigan sales tax if applicable, any storage/transport expenses and time to resell must be added separately, using the auction's current official terms. Heavy equipment and untested industrial machinery are intentionally not assigned general-purpose caps unless there is a specific candidate with substantial further inspection requirements.

## Photo integrity

Each batch's 40 lot contact sheets were downloaded independently from the same current 487-lot `lots.json` source snapshot and source URL matched in a separate committed provenance manifest. All five manifests report zero errors and the same source SHA-256 (`742507505b3eb69a766896306994a8cdfccbb2727d0fa89b8f082597d809c088`). Earlier batches' files are preserved. Two catalog lots (18284, 18583) lack original photographs.

## Resumption checkpoint

1. **Done:** 487 catalog rows, 200 provisional watchlist rows, five separate batches with 200 distinct pictured lots and 1499 source-verified photos. Per-lot findings and provisional maximum hammer bids are in both CSVs and the readable batch reports.
2. **Next:** finish the 24 uninspected batch-06 contact sheets (16 of 40 documented in the partial report), then proceed to other unreviewed photographed lots in non-overlapping batches. Maintain photo provenance and original batch sheets; never conflate adjacent auction lot tags.
3. **Before the close:** refresh live bid prices, check exact sold comps and physically test safety-critical equipment; deduct premium, transport, repair and resale expenses from bid ceilings. No continuing background inspection is running.

## Catalog group counts

- General industrial surplus: 98
- Snap-On and mechanic tools: 67
- General shop tools: 57
- Power and hydraulics: 53
- Bulk materials and racking: 52
- Tires and wheels: 45
- Branded hand and power tools: 29
- Rigging and towing: 27
- Farm equipment: 21
- Heavy equipment and vehicles: 20
- Welding and gas: 18
