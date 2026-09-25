# OrbitBid 1879 — auction review checkpoint

**Execution instructions:** read [the repository auction review SOP](../../AUCTION_REVIEW_SOP.md) and [agent instructions](../../AGENTS.md) before every continuation. Reuse an existing temporary photo artifact; do not redownload or commit photos for each batch. The historical `review-previews/` links below may point to images removed from the current branch.


## Latest durable checkpoint (batch 07)

- **280 distinct pictured lots inspected:** batches 01–05 (200), batch 06 (40) and batch 07 (40). Batch 07 used all 257 source-verified photos via temporary artifact `10844646656`, workflow run `36087152300`, inspected as per-lot composite contact sheets. Batch 06 used 336 source-verified photos. Neither batch 06 nor 07 has evidence-backed resale ranges or bid ceilings yet.
- **Master catalog merged:** `catalog-review.csv` still has 487 rows; the 80 photo-specific findings from batches 06–07 have been added by unique lot ID, without duplicating the 200 existing valued rows. The provisional watchlist still contains the 200 previously valued lots.
- **205 pictured lots remain uninspected**, plus two entries without photographs (18284 and 18583). The original complete temporary auction artifact `orbitbid-1879-photos` is available from run `36039298628` (artifact `10825787468`). It is too large for direct connector download, so [the artifact-only splitting workflow](../../.github/workflows/review-from-existing-artifact.yml) prepares batches 08–13 from that **existing** artifact; no OrbitBid photo re-download or image commit is required. Verify the workflow succeeds and download each small artifact before marking any remaining lots inspected.
- [Batch 07 findings](visual-review-batch-07.md); [batch 06 findings](visual-review-batch-06-partial.md). Historical `review-previews/` links below were removed from the current branch; use temporary artifacts instead.

**Historical checkpoint (before batch 07):** all 487 catalog entries triaged; **240 distinct pictured lots** visually inspected in six source-verified batches (1499 photographs in the first five batches; batch 06 source-photo count recorded in its manifest); 200 provisional watchlist valuations and conditional hammer ceilings. Source bid snapshot is September 24, 2026, 17:32:58 UTC; no live bid refresh was done by this photo workflow.

**Batch 06 photo inspection complete:** all 40 queued source-verified contact sheets have been inspected and documented in [batch-06 visual report](visual-review-batch-06-partial.md). Completed batches 01–05 remain unchanged. These 40 findings still require evidence-backed resale ranges, conditional bid ceilings and merging into the 200-row watchlist.

**Not completed:** source-photo visual review of 245 pictured lots beyond batch 06, confirmation of two photo-free entries, physical operation and safety checks, exact-match sold comps for most candidates and live bid refresh. This is not yet a complete 487-lot photographic appraisal.

## Completed visual-inspection batches

- [Batch 01](visual-review-batch-01.md): 40 distinct lots and 246 verified catalog images; [contact sheets](review-previews/README.md).
- [Batch 02](visual-review-batch-02.md): 40 distinct lots and 352 verified catalog images; [contact sheets](review-previews/batch-02/README.md).
- [Batch 03](visual-review-batch-03.md): 40 distinct lots and 286 verified catalog images; [contact sheets](review-previews/batch-03/README.md).
- [Batch 04](visual-review-batch-04.md): 40 distinct lots and 301 verified catalog images; [contact sheets](review-previews/batch-04/README.md).
- [Batch 05](visual-review-batch-05.md): 40 distinct lots and 314 verified catalog images; [contact sheets](review-previews/batch-05/README.md).
- **200 lots / 1499 photographs fully reviewed in completed batches**; 40 additional batch-06 lots have photo-specific findings (240 pictured lots inspected in total), 245 pictured lots still awaiting visual inspection, and two catalog entries have no photos.

## Files

- [batch-07-queue.md](batch-07-queue.md): next 40 distinct catalog lots, selected only; no batch-07 photos inspected yet.

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
2. **Next:** [Batch 07 queue](batch-07-queue.md) selects the next 40 non-overlapping lots (257 expected source photos). The batch is selected, not visually inspected; verify and inspect all source photos in the existing temporary artifact before writing findings. Batch 06's 40 visual findings still need consolidation into the master CSV and valuation. Maintain photo provenance and original batch sheets; never conflate adjacent auction lot tags.
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
