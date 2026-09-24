# OrbitBid 1879 — auction review checkpoint

**Pass completed:** all 487 catalog descriptions categorized and annotated. 87 lots have **provisional, description-based** illustrative gross resale ranges and conditional maximum **hammer bids**. Original snapshot retrieved September 24, 2026, at 17:32:58 UTC. Bids may have changed; use price-history and live site for current prices.

**Not completed:** a photo-by-photo inspection of all lots, condition verification, and lot-specific sold-comparables validation. **Do not treat this as a completed full appraisal or photo audit.** The photos/review sheets are retained in the temporary GitHub Actions artifact `orbitbid-1879-photos`; original source links for each image are preserved in [summary.md](summary.md). These temporary photos are intentionally not committed to permanent Git history.

## Files

- [catalog-review.csv](catalog-review.csv): all 487 lots, one record per lot; source photos, catalog bids, review flags and individually assigned catalog-category notes. Empty valuation fields mean **unpriced**, not worthless.
- [provisional-watchlist.csv](provisional-watchlist.csv): 87 preliminary candidates, conservative provisional caps **subject to image, condition and comparable-sale review**.
- [all-lots-review.md](all-lots-review.md): readable per-lot review table for every lot.
- [summary.md](summary.md): original unabridged descriptions and every source photo link.
- [price-history.csv](price-history.csv): existing timestamped price history (not altered here).

## Valuation method and limits

Gross resale ranges are illustrative used-market **working-condition scenarios**, not verified current sold prices for these exact lots. They exclude resale commissions, shipping, cleaning and repairs. Provisional caps are **maximum hammer bids** only if functional/condition checks pass; no bid is justified solely because it is below the cap. The initial source catalog often shows a $5 opening amount, which is not evidence of low closing demand. Buyer premium, Michigan sales tax if applicable, any storage/transport expenses and time to resell must be added separately, using the auction's current official terms. Heavy equipment and untested industrial machinery are intentionally not assigned general-purpose caps unless there is a specific candidate with substantial further inspection requirements.

## Photo integrity

The earlier photo contamination has been addressed by separate image-manifest verification in the workflow, but **this review has not independently inspected the full archive**. The absence of committed photo folders is expected under the current temporary-artifact retention policy. There are two entries with no catalog photos: 18284, 18583.

## Resumption checkpoint

1. All 487 catalog rows are retained in `catalog-review.csv`; do **not** redo the import or accidentally replace it with a smaller partial set.
2. Open `provisional-watchlist.csv`, inspect **every image** for each candidate using `summary.md` or the latest verified Actions artifact, and document image findings in `catalog-review.csv`.
3. Verify sold comps and exact models for high-priority candidates; adjust all rough valuation ranges/caps. Update bid prices independently closer to sale.
4. Only after 487 image reviews (or explicit not-reviewed exceptions) should this be called a full visual review.

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
