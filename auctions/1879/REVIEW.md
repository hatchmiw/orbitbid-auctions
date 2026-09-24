# OrbitBid 1879 — auction review checkpoint

**Pass completed:** all 487 catalog descriptions triaged; 120 conditionally priced watchlist lots; **120 distinct lots / 884 source-verified current-catalog photos** now inspected across batches 01–03. The original bid snapshot is September 24, 2026, 17:32:58 UTC. This photo review did not refresh current bids.

**Not completed:** photographic visual inspection of 365 remaining pictured lots (plus 2 with no source photos), in-person functional and safety inspection, exact-item sold comps for most lots and a live-price refresh. This is not yet the full 487-lot visual appraisal.

## Completed visual-inspection batches

- [Batch 01](visual-review-batch-01.md): 40 lots, 246 original catalog images inspected; [source-verified sheets](review-previews/README.md).
- [Batch 02](visual-review-batch-02.md): 40 more lots, 352 images inspected; [source-verified sheets](review-previews/batch-02/README.md).
- [Batch 03](visual-review-batch-03.md): 40 more lots, 286 images inspected, including all 7 pending watchlist candidates and 33 new candidates; [source-verified sheets](review-previews/batch-03/README.md).
- **120 pictured lots visually reviewed / 884 source images**; 365 pictured lots pending; two have no source photographs.

## Files

- [catalog-review.csv](catalog-review.csv): all 487 lots and descriptions; now 120 per-lot visual notes, value/cap scenarios and permanent source-verified sheet links.
- [provisional-watchlist.csv](provisional-watchlist.csv): 120 provisional conditional candidates (expanded from 87), all visually reviewed in the three batches; includes individual image findings and link to each permanent review sheet.
- [all-lots-review.md](all-lots-review.md): readable per-lot review table for every lot.
- [summary.md](summary.md): original unabridged descriptions and every source photo link.
- [price-history.csv](price-history.csv): existing timestamped price history (not altered here).

## Valuation method and limits

Gross resale ranges are illustrative used-market **working-condition scenarios**, not verified current sold prices for these exact lots. They exclude resale commissions, shipping, cleaning and repairs. Provisional caps are **maximum hammer bids** only if functional/condition checks pass; no bid is justified solely because it is below the cap. The initial source catalog often shows a $5 opening amount, which is not evidence of low closing demand. Buyer premium, Michigan sales tax if applicable, any storage/transport expenses and time to resell must be added separately, using the auction's current official terms. Heavy equipment and untested industrial machinery are intentionally not assigned general-purpose caps unless there is a specific candidate with substantial further inspection requirements.

## Photo integrity

Every image for the 120 selected lots was freshly downloaded from the same current 487-lot `lots.json` snapshot and checked against the corresponding current source URL. Each batch has a separate committed contact-sheet folder and manifest. All three manifests have zero download errors and share the identical source snapshot SHA-256 (`742507505b3eb69a766896306994a8cdfccbb2727d0fa89b8f082597d809c088`). Historical or mismatched photos were not reused. The full-resolution original photo cache remains temporary in GitHub Actions; the three batches' compact sheets are permanent in GitHub. Lots **18284** and **18583** have no original catalog photographs.

## Resumption checkpoint

1. **Committed and verified:** full 487-lot catalog, 120 preliminary watchlist estimates, and batches 01–03 covering **120 different lots and 884 photographs**. Their 3 separate verified contact sheet folders are in `review-previews/` and every assessed lot's notes and caps are reflected in both review CSVs and the readable all-lots report.
2. **Next:** work through the remaining 365 photographed catalog lots in non-overlapping batches. Prioritize useful tools, workshop consumables and practical farm equipment. Two photo-free lots need in-person description confirmation.
3. **Before auction close:** independently check current bids and high-value sold-market comps, calculate premium/tax/transport and physically test safety-critical and mechanical items. No automatic full review is running in the background.

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
