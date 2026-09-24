# OrbitBid 1879 — auction review checkpoint

**Pass completed:** all 487 catalog descriptions triaged, 87 provisional priced lots, and **80 distinct lots / 598 original catalog photographs** fully examined using separate current-source verified contact sheets. The two batches share the identical current `lots.json` snapshot SHA-256. Price snapshot retrieved September 24, 2026, 17:32:58 UTC; prices have not been refreshed here.

**Not completed:** the other 405 photographed lots, on-site functional and safety inspection, exact-item sold comps and live bid refresh. Two lots lack photos. Do not describe this as a complete 487-lot photographic appraisal.

## Completed visual-inspection batches

- [Batch 01](visual-review-batch-01.md): 40 lots, 246 current-source images and revised condition-specific notes; [verified contact sheets](review-previews/README.md).
- [Batch 02](visual-review-batch-02.md): 40 additional lots, 352 source-verified images and revised provisional caps; [verified batch 02 sheets](review-previews/batch-02/README.md).
- **80 reviewed / 485 pictured lots**; 405 pictured lots remain and two have no source images.

## Files

- [catalog-review.csv](catalog-review.csv): 487 lot rows, complete source IDs and descriptions; 80 individual visual notes, provisional valuations and permanent verified contact-sheet links.
- [provisional-watchlist.csv](provisional-watchlist.csv): 87 provisional conditional candidates, including 80 visually reviewed in the two current-source batches.
- [all-lots-review.md](all-lots-review.md): readable per-lot review table for every lot.
- [summary.md](summary.md): original unabridged descriptions and every source photo link.
- [price-history.csv](price-history.csv): existing timestamped price history (not altered here).

## Valuation method and limits

Gross resale ranges are illustrative used-market **working-condition scenarios**, not verified current sold prices for these exact lots. They exclude resale commissions, shipping, cleaning and repairs. Provisional caps are **maximum hammer bids** only if functional/condition checks pass; no bid is justified solely because it is below the cap. The initial source catalog often shows a $5 opening amount, which is not evidence of low closing demand. Buyer premium, Michigan sales tax if applicable, any storage/transport expenses and time to resell must be added separately, using the auction's current official terms. Heavy equipment and untested industrial machinery are intentionally not assigned general-purpose caps unless there is a specific candidate with substantial further inspection requirements.

## Photo integrity

Every image was downloaded independently from the current 487-lot snapshot in a GitHub Action and verified against its source URL; *no historic photo folders were reused*. The 40 sheets from batch 01 remain separate from the 40 sheets from batch 02, with both provenance manifests committed. The original full-resolution photographs remain temporary under the GitHub Actions retention policy. Two lots lack source images: **18284 and 18583**.

## Resumption checkpoint

1. **Done and committed:** 487 catalog rows, 87 provisional watchlist candidates; batches 01 and 02 cover 80 distinct lots and 598 verified source photographs, with descriptions, revised caps and risk notes in both CSV files.
2. **Next:** inspect all current-source photographs for the remaining **405 pictured lots**, document source-specific findings, update the CSVs and preserve prior image sheets. Avoid overlapping new batch IDs.
3. **Before the close:** refresh all current lot bids and check hard sold-market comparables, then validate buyer premium, moving costs, equipment function and personal-use priorities. Never infer item condition solely from thumbnails.

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
