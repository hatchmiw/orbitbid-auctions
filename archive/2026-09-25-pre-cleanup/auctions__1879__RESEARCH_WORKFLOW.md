# Auction 1879 — evidence-first review workflow

## Current state (2026-09-24)
- **487** unique catalog records, **485** pictured and **2** without source photos (18284, 18583).
- All 485 pictured lots received an initial source-matched contact-sheet review; **20** have separately documented individual original-image inspection (106 originals). Do not conflate these levels.
- **290** earlier heuristic valuations have been restored to `historical_unverified_*` fields in the master and prior watchlist. They are historical notes, **not** researched prices or bids.
- **0** active researched valuations currently meet the evidence gate. Prior active price fields stay empty until documented comparable research.
- Existing temporary split artifacts from workflow run **36087642169** remain unexpired as last checked 2026-09-24, with expected expiry around 2026-10-07. No image downloads or image commits for this workflow change.
- Prior research notes are retained in `market-research.md` and prior visual notes in batch reports and `full-image-price-review.md`.

## Single authoritative dataset

`catalog-review.csv` is the only editable per-lot master. The `provisional-watchlist.csv` is **legacy historical context**, not an active bidding sheet. `researched-watchlist.csv`, `research-queue.csv` and `GENERATED_STATUS.md` are **generated views**, not independently edited sources. Regenerate with:

```sh
python scripts/build_auction_review.py 1879 --check
python scripts/build_auction_review.py 1879
```

The generator rejects duplicate IDs, missing columns, incorrect catalog count, active price ranges without `market_research_status=Research verified`, or verified prices without evidence URLs, explanatory notes and UTC research date. It never modifies the master or photos.

## Research workflow

1. **Prioritize once:** assign `priority` High, Medium, Low or Untriaged based on potential demand, likely practical use, resale logistics and risk. Do not assume priority is proof of value.
2. **Reuse prior visual findings:** reopen existing artifact originals only to resolve identity, condition, part numbers, missing parts or consequential defects. Preserve contact-sheet versus full-original-photo status. No repetitive whole-catalog inspection.
3. **Evidence first:** collect dated completed-sale links for matching model, quantity and comparable condition. Record limitations, adjustments, freight and uncertainty in `market_research_notes`; store source URLs in `market_evidence_urls` and UTC date in `market_research_date_utc`. Asking listings may inform context but **do not** establish completed-sale value. If evidence is insufficient, leave active price and hammer fields blank and explain why.
4. **Only then price:** researched gross resale low/high and conditional maximum hammer are separate active columns. The bid ceiling must explicitly account for buyer premium, taxes, fees, pickup/transport, repair allowance, and margin. Safety-critical unknowns receive no positive bid ceiling absent necessary verification.
5. **Checkpoint every 10 lots researched:** commit only the master, research log and regenerated views; log exact lot IDs, evidence links and remaining uncertainties. Do not treat queue selection, photo availability, asking prices, or a workflow run as completed research.
6. **Live bids are separate:** refresh via the existing price-refresh workflow and preserve timestamp; never treat the 2026-09-24 snapshot as live. Do not overwrite researched values during refresh.

## Next work
Triage the 487 lots by resale/personal-use priority using existing photo findings. Start with the highest-priority identifiable equipment and tools, then complete exact-model sold-comparable research. The four lots in `market-research.md` have documented preliminary searches but **no** validated active value. Do not re-research completed exact-match evidence without reason.

## Historical source and SOP
SOP blob read: `06b3b2712120244f06adcf067464fdbc63f48c86`. Split-artifact source run `36087642169`, derived from full photo run `36039298628`. Preserve all prior batch notes, source URLs and historic estimates; do not commit images or ZIPs.

## Required photo-retrieval clarification (2026-09-25)

Read root `AUCTION_REVIEW_SOP.md` and `AGENTS.md` at **every** execution. The proven Pioneer method works for OrbitBid: use the GitHub connector's `download_workflow_artifact` action to obtain **existing** Actions artifact ZIPs, extract exact lot JPGs, verify provenance and pass the actual image bytes to vision. The full 1879 ZIP (artifact `10825787468`, 1.55 GB) exceeds the connector's 512 MiB per-download cap; this is not a general binary limitation. Existing smaller artifacts are documented in the SOP; batch-07 artifact `10844646656` was successfully downloaded on September 25. Check all artifact expiry and lot coverage on each continuation. For batches without a suitable small artifact, use the existing artifact-only splitting workflow **after verifying its inputs**, rather than redownloading OrbitBid originals. If a departure from the SOP is necessary, discuss it with the user **before** changing methods. No new photos or ZIPs in Git; no all-original-image-complete claim without seeing every original for that lot.
