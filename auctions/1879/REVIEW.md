# OrbitBid 1879 — opportunity-first research

**Governing procedure:** [SOP v3](../../AUCTION_REVIEW_SOP.md). The sole editable per-lot master is [catalog-review.csv](catalog-review.csv); [lots.json](lots.json) is source metadata. This auction closes in stages on September 29–30, 2026 per the imported catalog. Verify exact lot close times and refresh current bids before bidding; the stored bid snapshot is not live.

## Current scope and progress
- **487 catalog lots**, **485 pictured**, **2 without photographs** (18284, 18583). All pictured lots were previously covered by initial contact-sheet screening. This is *screened*, not *fully inspected*.
- The master currently records **43 individual-original-photo inspections**: 20 earlier documented inspections, nine subsequently reconciled by Work, and 14 further Work inspections. Do not repeat these unless source evidence reveals a material defect.
- **93 high-priority, 104 medium-priority and 290 low-priority screening classifications** already exist in the master. They are discovery filters, not rankings of investment quality. The first shortlist is a working research queue, not ten established opportunities.
- **Zero active evidence-verified valuations** currently exist. Preserve the 290 withdrawn heuristic estimates solely in historical fields. Prior source investigations and limited sold evidence remain in [market-research.md](market-research.md).
- The latest individual-photo inspection commit previously verified was lot **18145** (nine originals), commit `39f606e29710e3dc7d63fc8732ca6e1add7e25aa`. Because review is now opportunity-first, the next lot is the highest-value *unresolved research candidate*, not automatically 18146.

## First research queue — candidates, not bidding recommendations
Investigate these ten leads, using existing notes first. Do not promote a candidate to `ready for user review` until its actual photo inspection and adequate market evidence are documented.

| Lot | Lead | Why investigate / decisive question |
|---|---|---|
| 18439 | Snap-On PH3050A air hammer with chisels | Existing exact-model historical sales and recent listing context; verify tool operation, chisel count and matched recent sold prices. |
| 18440 | Snap-On RTD33 thread-restoring kit | Existing historical $60 completed auction; verify actual case contents and recent exact-kit sold transactions. |
| 18110 | Two Blue Point shop carts | Identify exact models, drawer function and missing components; research local used cart demand and pickup. |
| 18115 | Honda GX140 plate compactor | Verify engine starts and exciter condition; find same-class completed used-equipment sales. |
| 18118 | Ramco Shop Hand 5000 engine hoist | Inspect ram leaks, load-rating label and completeness; compare local used engine-hoist sales. |
| 18123 | Miller AED-200LE welder/generator | Confirm engine, generator and welding output; identify completed sales with comparable running status. |
| 18122 | Tool box with assorted hand tools | Identify included brands, actual quantities and sellable components; compare realistic local mixed-tool lots. |
| 18127 | Oxygen/acetylene torch cart setup | Verify cylinder ownership/inclusion, regulators and hose condition; research comparable safe used sets. |
| 18130 | Miller Dimension 650 welding power source | Confirm three-phase power requirements, test status and industrial resale/pickup demand. |
| 18114 | Hobart 6-261 tow-behind generator | Verify model/specification, engine condition, trailer condition and transport; research matched sold equipment. |

These are research leads selected from existing high-priority screening, **not** verified profitable lots. Expand to other high-priority and overlooked medium-priority lots if any lead fails its investigation. Separate personal-use value from resale value.

## Immediate deliverable
1. Produce the first **10 genuinely investigated candidates** (or fewer if evidence cannot support ten) with original-photo inspection, matching dated completed-sale evidence, current bid timestamp, realistic value range, conditional bid ceiling where justified, and outstanding questions.
2. Commit each completed candidate's inspection or researched valuation immediately to the master. Maintain one concise opportunity shortlist; do not create competing batch reports.
3. Refresh auction bids using the existing updater and make the shortlist easy for the user to review before the relevant lot close times.
4. Track four distinct metrics: catalog screened, selected original-photo inspected, market-researched, and ready for user review. Never equate one with another.

## Existing photo artifacts
Full source run `36039298628`, artifact `10825787468` (1.55 GB; connector cap 512 MiB). Batch 07: run `36087152300`, artifact `10844646656`. Split batches 08–13: run `36087642169`, IDs `10844397014`, `10844157362`, `10844052609`, `10844227160`, `10844526785`, `10843977621`. Recheck availability/expiry; reuse existing split artifacts and the documented artifact-only recovery workflow. Never commit photos.

## Historical evidence
Existing batch reports and [full-image-price-review.md](full-image-price-review.md) are evidence, not competing completion ledgers. Superseded procedures and duplicate checkpoint reports are preserved in [the cleanup archive](../../archive/2026-09-25-pre-cleanup/). This scope supersedes the former demand to individually inspect and value all 487 lots before presenting opportunities.
