# OrbitBid 1879 — opportunity-first research

**Governing procedure:** [SOP v3](../../AUCTION_REVIEW_SOP.md). The sole editable per-lot master is [catalog-review.csv](catalog-review.csv); [lots.json](lots.json) is source metadata. This auction closes in stages on September 29–30, 2026 per the imported catalog. Verify exact lot close times and refresh current bids before bidding; the stored bid snapshot is not live.

## Current scope and progress
- **487 catalog lots**, **485 pictured**, **2 without photographs** (18284, 18583). All pictured lots were previously covered by initial contact-sheet screening. This is *screened*, not *fully inspected*.
- The master currently records **43 individual-original-photo inspections**: 20 earlier documented inspections, nine subsequently reconciled by Work, and 14 further Work inspections. Do not repeat these unless source evidence reveals a material defect.
- **93 high-priority, 104 medium-priority and 290 low-priority screening classifications** already exist in the master. They are discovery filters, not rankings of investment quality. The first shortlist is a working research queue, not ten established opportunities.
- **Zero active evidence-verified valuations** currently exist. As of September 25, **all ten first-queue candidates have additional source-backed completed-sale research committed in the master**; none has yet passed the new candidate-level original-photo/condition verification or received a defensible active bid ceiling. Preserve the 290 withdrawn heuristic estimates solely in historical fields. Prior source investigations and limited sold evidence remain in [market-research.md](market-research.md).
- The latest individual-photo inspection commit previously verified was lot **18145** (nine originals), commit `39f606e29710e3dc7d63fc8732ca6e1add7e25aa`. Because review is now opportunity-first, the next lot is the highest-value *unresolved research candidate*, not automatically 18146.

## Initial research leads — non-exhaustive; continue screening all 487 lots
These were the first ten leads, not a target or stopping condition. Continue through all 93 high-priority and 104 medium-priority screened lots and revisit overlooked low-priority lots where warranted. Do not promote a candidate to `ready for user review` until its actual photo inspection and adequate market evidence are documented.

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

## September 25 research checkpoint

The first research pass on **the initial ten leads** is saved in `catalog-review.csv` (commits `dabd72b68aab3307bae6c6b58ad78ea93bc99c9b` and `6863adfe7cb6023068bea9789416cd6111c4ba09`). Each now has cited completed-sale or related-sale evidence and an explicit comparability/condition gap. The 487-row, 26-column master was validated on both saves. **Research pass does not mean candidate ready:** individual-original inspection, operating condition, final comparable selection and buyer-premium-adjusted bid ceiling are outstanding. Do not redo these searches without a specific reason. The September 25 continuation added research for five more Snap-on leads: 18400, 18404, 18406, 18409 and 18416 (commit `d691847301954f5b84ffa1a36efe18eca5b9d7f0`). Next: inspect promising candidates' originals individually and evaluate actual lot condition; keep screening the remaining catalog and do not stop at a lot count or checkpoint.

## Immediate deliverable
1. Investigate **all worthwhile candidates found through full-catalog screening** with original-photo inspection, matching dated completed-sale evidence, current bid timestamp, realistic value range, conditional bid ceiling where justified, and outstanding questions.
2. Commit each completed candidate's inspection or researched valuation immediately to the master. Maintain one concise opportunity shortlist; do not create competing batch reports.
3. Refresh auction bids using the existing updater and make the shortlist easy for the user to review before the relevant lot close times.
4. Track four distinct metrics: catalog screened, selected original-photo inspected, market-researched, and ready for user review. Never equate one with another.

## Existing photo artifacts
Full source run `36039298628`, artifact `10825787468` (1.55 GB; connector cap 512 MiB). Batch 07: run `36087152300`, artifact `10844646656`. Split batches 08–13: run `36087642169`, IDs `10844397014`, `10844157362`, `10844052609`, `10844227160`, `10844526785`, `10843977621`. Recheck availability/expiry; reuse existing split artifacts and the documented artifact-only recovery workflow. Never commit photos.

## Historical evidence
Existing batch reports and [full-image-price-review.md](full-image-price-review.md) are evidence, not competing completion ledgers. Superseded procedures and duplicate checkpoint reports are preserved in [the cleanup archive](../../archive/2026-09-25-pre-cleanup/). This scope supersedes the former demand to individually inspect and value all 487 lots before presenting opportunities.


## September 25 shortlist screening — opportunity-first

The master catalog contains 487 lots: 93 high, 104 medium, 290 low. Existing original-photo findings and market notes inform this SCREEN; it does not assert fresh original-photo verification or live bids. Ranking below prioritizes portable, identifiable, locally marketable tools, then larger equipment with higher testing and pickup risk. The remaining high- and medium-priority lots are not automatically excluded.

### Ranked first-pass opportunities

1. **18400** Snap-on two-part cabinet — high gross-value potential; verify actual two-unit inclusion, slides, locks, model, and moving costs. Historic comparable 10-drawer cabinets $825–850, not exact matches.
2. **18404** Snap-on impact sockets — count actual 3/8- and 1/2-drive pieces and inspect drive-end wear; separate resaleable sets.
3. **18406** Snap-on deep impact sets — verify each metric size, missing pieces and impact-rated markings.
4. **18421** Snap-on 10–19mm wrench set — check completeness and wear; portable, broad local demand.
5. **18417** Snap-on combination/stubby wrench assortment — verify exact counts and duplicates.
6. **18410** Snap-on 1/4-inch cased socket kit — identify missing recesses, ratchet condition and exact model.
7. **18424** Snap-on angle-head wrenches — specialty demand; check sizes and rust.
8. **18426** four extra-large Snap-on long wrenches — useful high-dollar singles, slower buyers.
9. **18428** two Snap-on dial torque wrenches — calibration and dial operation essential.
10. **18440** Snap-on RTD33 thread-restoring kit — check every insert against factory inventory.
11. **18441** Snap-on A257 bushing-driver set — inspect every numbered driver.
12. **18442** multiple Snap-on extractor cases — count bits and inspect breakage.
13. **18451** Snap-on plier/cutter assortment — inspect jaws and pivot wear.
14. **18453** oversized Snap-on 3/4- and 1-inch ratchets — verify function; narrower buyer pool.
15. **18211** Milwaukee M18 impact and other tool — battery health and exact models crucial.
16. **18439** Snap-on PH3050A air hammer and chisels — verify retainer, air motor and usable bits.
17. **18123** Miller AEAD-200LE welder/generator — exact-model sold $687.50 Aug 2025, but $110 Sep 2026 with difficult removal; test running/weld/AC output.
18. **18115** Honda GX140 plate compactor — verify clutch, exciter and actual operation.
19. **18118** Ramco Shop Hand 5000 hoist — inspect hydraulic hold, casters and welds.
20. **18110** two Blue Point shop carts — inspect drawers, wheels, missing accessories.
21. **18173** DeWalt DCGG571 grease gun — no batteries noted; test with compatible battery.
22. **18193** Milwaukee Hole Hawg — check gears, chuck, cord and auxiliary handle.
23. **18575** Snap-on bench vise — jaw damage and dismantling costs reduce attractiveness.
24. **18597** heavy-duty impact socket collection — high shipping weight, identify branded pieces.
25. **18127** torch cart — oxygen tank only, no acetylene cylinder; verify ownership and regulators.
26. **18416** Snap-on crowfoot heads — count sizes and duplicates, identify sets.

### Secondary high-priority candidates — retain, not rejected

Snap-on sockets, ratchets, extensions and wrenches: 18401–18403, 18405, 18407–18409, 18411–18415, 18418–18420, 18422–18423, 18425, 18427. Other Snap-on specialty hand and air tools: 18429–18438, 18443–18450, 18452. Equipment and mixed tools: 18114, 18122, 18124–18126, 18130, 18138, 18140–18142, 18152, 18189, 18192, 18487–18488, 18522. Other high-priority lots remain in the master; all 104 medium-priority lots remain available for promotion.

### Dated completed-sale anchors

- Sep 16 2026: mixed Snap-on socket/ratchet/tool drawer sold $240 (Aumann); https://bids.aumannauctions.com/auctions/48160/lot/7897233-assorted-tool-set-including-snap-on-sockets-ratchets-and-extensions-in-red-chest
- Sep 21 2026: assorted Snap-on 1/4-drive sockets with metal toolbox sold $175, 15% buyer premium (HiBid); https://greatlakes.hibid.com/lot/322075693/asst-snap-on-1-4-drive-sae-sockets-and-metal
- Sep 16 2026: 11 Snap-on SAE combination wrenches $155.25, eight 3/8-drive ratchets $178.25, 31 3/8-drive sockets $155.25 (HiBid); https://hibid.com/www.heretn.com/catalog/764003/16-september-single-owner-online-auction
- Aug 27 2025: Miller AEAD-200LE $687.50 (Purple Wave); https://www.purplewave.com/auction/250827/item/DX7182/Miller-AEAD-200LE-Torches%2C_Welders_and_Plasma_Cutters-Welder_%28Manual%29-Iowa
- Sep 22 2026: Miller AEAD-200LE $110 with difficult mezzanine removal (HiBid); https://hibid.com/www.heretn.com/lot/321781537/miller-aead-200le

**No active bid ceilings yet.** These are screening ranks, not verified margins. Original-photo inspection, condition-adjusted exact-model market comps, buyer premium, sales costs and live bid refresh remain necessary before bid recommendations.
