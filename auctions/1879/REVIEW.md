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

## September 28 ignored-lot second-pass checkpoint

**Authoritative state used:** complete price-history snapshot `2026-09-28T15:28:43.487070Z` (487/487 lots) and imported OrbitBid watchlist captured `2026-09-28T15:23:01.021Z` (81 matched auction-1879 lots, 0 unmatched). The whole 487-lot catalog was screened against current bid, bid count, prior priority, current personal-watchlist membership, existing photo findings and existing research. At this snapshot, 338 lots were at $15 or less and 283 of those were not on the personal watchlist; cheap/no-bid status was used only as a discovery signal, not as a recommendation.

### New detailed second-pass inspections
Source-verified original JPGs were individually reopened from the existing Actions artifacts for **18162, 18224, 18279, 18281, 18288, 18314, 18327, 18502 and 18518**. Their findings and new market/replacement-cost evidence are recorded in `catalog-review.csv` at commit `7eb670457992d91c80f6ac4236ddab587d076bd9`, followed by added market evidence for 18468, 18501, 18530, 18537, 18590, 18192 and 18195 at commit `702752891996007c05c9febd00b98a4a934cb3d8`. Existing individual-original inspections of 18143, 18160, 18161 and 30-1332 were reused rather than repeated.

Material findings that changed the ignored-lot screen:
- **18502 hitch pins** contains substantial farm/trailer hardware, including a sealed Lawson 50-count package of 1/4 x 4 Hammerlock cotter pins plus heavier hitch/clevis pins.
- **18518 tubing** contains multiple partial coils of identifiable Tectran 1928 SAE J844 Type B 1/2-inch air-brake tubing. Unknown age prevents assuming highway brake-service suitability, but replacement/shop utility is real.
- **18288 hose** contains meaningful lengths of SAE 100R4-class suction/return hose and other heavy hose; new replacement cost is high, but old service history prevents valuing it as certified pressure hose.
- **18327 80 x 48 steel mesh drag** is substantially intact despite uniform rust and is credible for grading/smoothing personal-use projects; tow hardware remains uncertain.
- **18224 Ramco RH5000** is a substantial truck-jib frame/base but lacks the hydraulic lifting component; value is as a repair/fabrication base, not a proven 5,000-lb crane.
- **18314 quick-attach jib** is a heavy adjustable/telescoping fabricated boom with hook and receiver structure, but fitment and rated capacity are not established.
- **18162 blast pot** has visibly deteriorated closure/seal rubber and aged hose, materially reducing it to rebuild/parts status unless pressure-vessel integrity is verified.
- **18279** is more than scrap grease buckets: a retractable reel, multiple pumps and hoses are present, though dirty and untested.
- **18281** has three manual transfer-pump assemblies rather than a single low-value pump.

### Current ignored-lot opportunity set

The second pass promotes the following non-watchlisted or previously low-priority lots for decision review, subject to the exact hammer ceilings in the user-facing analysis: **18115, 18143, 18160, 18161, 18189, 18192, 18195, 18224, 18279, 18281, 18288, 18314, 18468, 18501, 18502, 18518, 18530, 18537, 18569, 18577, 18590 and 30-1332**. Lot **18327** remains on the personal watchlist and is retained as a personal-use target.

Safety-critical or condition-limited items remain deliberately discounted: old lifting/rigging gear, unverified jack stands, aged air-brake components intended for highway service, old pressure-vessel equipment and damaged/unknown hydraulic lifting equipment are not valued as rated serviceable equipment.

**Resume point:** re-read the newest complete price snapshot before bidding and compare each surviving target to its conditional hammer ceiling. Do not re-download or re-inspect the second-pass originals above unless new evidence creates a specific question.

## September 28 combined personal-watchlist + ignored-lot decision set

The current imported personal OrbitBid watchlist has **81 auction-1879 lots**. The September 28 ignored/deprioritized second pass produced **31 candidates**, with only **18327** already present on the personal watchlist, for a raw union of **111 unique lots**. Do not use 111 as the practical bidding list.

Using the complete price snapshot `2026-09-28T15:28:43.487070Z`, the practical **active focus set is 32 lots** with a combined current hammer of **$340**. That dollar sum is descriptive only; it is not an auction budget and does not imply pursuing every lot to a ceiling.

| Functional group | Active focus lots |
|---|---|
| Farm / property / material handling | 18101 ($10), 18115 ($5), 18118 ($10), 18327 ($15) |
| Pipe / fabrication / shop equipment | 18140 ($5), 18156 ($5), 18530 ($5), 18570 ($5), 18577 ($5) |
| Power tools / portable shop tools | 18189 ($10), 18192 ($10), 18193 ($20), 18206 ($5), 18211 ($55), 18439 ($20), 18468 ($5) |
| Hydraulic / grease / service tools | 18161 ($5), 18203 ($5), 18440 ($25) |
| Hardware / consumables / organizers | 18501 ($5), 18502 ($5), 18518 ($5), 18544 ($10), 18545 ($35), 18558 ($5), 18561 ($5), 18563 ($5), 18564 ($15), 18573 ($10) |
| Truck / trailer / electrical stock | 18578 ($5), 30-1332 ($5) |
| Vintage storage / parts-value wildcard | 18590 ($5) |

### De-duplication rules for bidding

- **Grease/transfer equipment:** favor 18161 over 18160 at the same $5 neighborhood because 18161 includes two rolling setups; treat 18279 and 18281 as backups/opportunistic additions rather than buying every pump lot.
- **Benches/shop stations:** 18530 is the vise-centered target; 18577 is the bench-plus-tool-content target. 18103 becomes secondary unless its included steel stock is specifically needed. Buying both 18530 and 18577 can still make sense because their value propositions differ.
- **Truck/trailer lighting:** 18578 is the more direct personal-use lot; 30-1332 has the better mixed-parts/minibar angle. Do not chase both merely because both are cheap.
- **Pipe tools:** 18140 plus 18156 cover most practical pipe-wrench/threading needs. 18143 is secondary unless the chain wrench itself is specifically valuable.
- **Portable grinders/drills:** 18189, 18192, 18193, 18206 and 18468 overlap enough that they should compete for spending rather than all being automatic buys. Preserve 18193 for the Hole Hawg's unique use and 18468 for the low-bid Ingersoll-Rand upside.
- **Hardware organizers:** 18544, 18558, 18561, 18563, 18564 and 18573 remain complementary. 18545 is still useful but is already $35, so it should be judged against the cheaper organizers before adding more hardware inventory.
- **Large/high-dollar watched equipment:** 18123, 18124, 18125, 18128, 18134 and 18541 remain on the personal watchlist but are no longer part of the cheap overlooked-opportunity sweep at their current bids. Treat each as a separate deliberate equipment purchase.
- **Safety-sensitive load gear:** old chain, binders, hoists, jack stands, pressure equipment and similar lots remain condition-dependent. Low price alone does not promote them into the active focus set.

### Working ceilings already established in current decision work

| Lot | Working max hammer | Note |
|---|---:|---|
| 18115 | $70 | Honda GX140 compactor; function still uncertain |
| 18161 | $50 | two grease-pump setups |
| 18189 | $50 | three Metabo grinders + repairable Makita |
| 18192 | $40 | Milwaukee Sawzall + 5211 grinder |
| 18327 | $65 | personal-use steel mesh drag |
| 18468 | $45 | two Ingersoll-Rand impacts; model/function verification matters |
| 18501 | $35 | Band-It tool + banding |
| 18502 | $35 | bulk hitch/retaining hardware |
| 18518 | $30 | Tectran/other tubing; not assumed road-brake serviceable |
| 18530 | $75 | long bench + rough 5-inch Wilton vise + hose reel |
| 18577 | $60 | steel bench + assorted included shop tools |
| 18590 | $60 | Borg-Warner cabinet + vintage parts/display stock |
| 30-1332 | $30 | mixed truck/equipment lighting stock |
| 18573 | $50 | carried-forward practical-use ceiling from prior decision work |

Lots in the active focus set without a value in this table do **not** yet have a newly evidence-supported combined ceiling; do not substitute the withdrawn historical heuristic values in the master.

**Current action:** use the 32-lot focus set as the combined working list. Retain the rest of the 111-lot union as secondary/background opportunities and promote them only when price, condition or a specific project creates a reason.

## September 28 auction-day buying plan — 12:28 PM EDT refresh

**Price basis:** repository refresh `2026-09-28T16:28:54.455208Z`, 487/487 lots refreshed with zero errors. The 32-lot focus set totals **$345 hammer at current bids**, while the sum of every individual ceiling is **$1,595**. The ceiling sum is intentionally *not* a budget; it only defines where each lot stops making sense individually.

### Total-spend structure

Use **$350 hammer as the planned target**, with a **$450 hammer hard cap** only if unusually strong lots remain below their good-buy levels after earlier losses free budget. Do not spend toward the cap merely because capacity remains. Buyer premium and tax are additional; auction 1879's exact premium has not been independently verified in this review, so keep the working budget in hammer dollars until terms are confirmed.

Suggested allocation:
- **Up to $120:** Milwaukee 18211 reserve. If it is lost early, that reserve returns to the general pool.
- **About $150:** direct farm/shop property utility (compactor, drag, benches, bandsaw, grease equipment, steel/pipe tools).
- **About $80:** hardware/consumables/organizers.
- **About $50:** opportunistic resale/wildcards.
These are flexible envelopes, not mandatory spending quotas.

### Tier A — actively pursue if still under ceiling

| Lot | Current | Max hammer | Role / overlap rule |
|---|---:|---:|---|
| 18211 | $55 | **$120** | Milwaukee M18 3/4 impact + driver + batteries/charger; strongest portable-tool value. |
| 18573 | $10 | **$80** | Huot drill cabinet + large drill-bit inventory; strong shop utility/resale. |
| 18101 | $10 | **$75** | Cantilever rack + fabrication steel. Buy for material utility; removal is the constraint. |
| 18530 | $5 | **$75** | Long bench + 5-inch Wilton vise + hose reel. Prefer over 18103 unless steel stock is specifically wanted. |
| 18115 | $5 | **$70** | Honda GX140 compactor; direct property-use candidate, repair risk accepted. |
| 18327 | $15 | **$65** | Steel mesh drag; direct Morley yard/grading use. |
| 18570 | $10 | **$60** | Johnson horizontal bandsaw; only because current price leaves room for guide/alignment repair. |
| 18577 | $5 | **$60** | Steel bench + included tools. Can coexist with 18530 because contents/value proposition differ. |
| 18590 | $5 | **$60** | Borg-Warner cabinet/Tung-Sol stock; collector/storage wildcard. |
| 18161 | $5 | **$50** | Two grease-pump setups; preferred grease-equipment lot. |
| 18468 | $5 | **$45** | Two Ingersoll-Rand impacts; do not assume 2235 value until model/function verified. |
| 18140 | $5 | **$45** | Ridgid 36/24 + Fuller 18 pipe wrenches; practical shop/farm tools. |
| 18561 | $5 | **$45** | Hitch balls/clevises/hooks/eyelets/threaded rod; contents-only but strong farm utility. |
| 18502 | $5 | **$35** | Hitch/retaining pins including sealed Lawson stock; cheap consumable hardware. |
| 18518 | $5 | **$30** | Tectran/other tubing; shop use, not assumed safe for highway air-brake service. |

**Tier A current hammer total: $150.** Even if all fifteen were won at current prices, most of the planned budget would remain for competition and later lots.

### Tier B — buy only when price remains favorable or Tier A losses free budget

| Lot | Current | Max hammer | Decision rule |
|---|---:|---:|---|
| 18439 | $20 | **$60** | Snap-On PH3050A + chisels; good only while materially below functional-tool resale. |
| 18189 | $10 | **$50** | Metabo grinder lot; secondary to 18211/18468 in portable-tool spending. |
| 18193 | $20 | **$50** | Milwaukee Hole Hawg; preserve because its high-torque use is distinct from ordinary drills. |
| 18544 | $10 | **$50** | Electrical/keys/lugs organizers. |
| 18440 | $25 | **$45** | RTD33; already over halfway to ceiling, so don't chase. |
| 18118 | $10 | **$40** | Ramco 5000 hoist; safety/unknown hydraulic hold keep this low. |
| 18156 | $5 | **$40** | Pipe threading/cutting assortment; complements 18140 if still cheap. |
| 18192 | $10 | **$40** | Sawzall + grinder; secondary portable-tool purchase. |
| 18564 | $15 | **$40** | Hose-clamp racks; current price is okay but don't chase commodity inventory. |
| 18203 | $5 | **$35** | Porta-power-type hydraulic kit; unknown brand/capacity/seals. |
| 18501 | $5 | **$35** | Band-It tool/stock; model-dependent upside. |
| 18563 | $5 | **$35** | Organizers + fittings/misc drawer contents. |
| 18206 | $5 | **$30** | Heavy drills/bits; deprioritize if 18193 is won. |
| 30-1332 | $5 | **$30** | Mixed lighting + Star minibar; choose against 18578 rather than automatically buying both. |
| 18578 | $5 | **$25** | Truck/trailer lighting; direct utility but overlaps 30-1332. |
| 18558 | $5 | **$20** | Bolts/nuts + bench grinder; organizers excluded. |
| 18545 | $35 | **$55** | Metric/socket-cap/roll-pin organizers. Still viable, but highest current percentage of ceiling in the hardware group; cheaper hardware lots come first. |

### Close-time sequence and reallocation

- **6:00 PM EDT:** 30-1332 and the 181xx lots. This is where steel, compactor, grease equipment, pipe tools and several power tools resolve.
- **6:30 PM EDT:** 18203, 18206 and especially **18211**. Do not spend the Milwaukee reserve before this group closes.
- **7:00 PM EDT:** 18439/18440/18468 and early 185xx hardware/shop lots. Reallocate money from earlier losses here.
- **7:30 PM EDT:** 18570, 18573, 18577, 18578 and 18590. This is a strong late cluster; preserve at least **$100-$150 of unused hammer capacity** for it if possible.
- **8:00 PM EDT:** 18327 steel mesh drag. Because it has a known personal project, keep its **$65 ceiling** available rather than exhausting the budget at 7:30.

### Hard substitution rules

1. **Grease equipment:** 18161 first; do not add 18160/18279/18281 unless 18161 is lost or they stay essentially giveaway-price.
2. **Drills:** 18193 first for high-torque work; 18206 only if cheap or 18193 is lost.
3. **General portable tools:** 18211 first, then 18468; grinders/Sawzall are secondary.
4. **Pipe tooling:** 18140 first; add 18156 only at a clear bargain.
5. **Truck lighting:** choose 30-1332 vs. 18578 based on final price; buying both is acceptable only if both stay very low.
6. **Hardware cabinets:** prioritize cheap specialized inventory (18502, 18518, 18561, 18563) before chasing 18545 above its current $35.
7. **Benches:** 18530 and 18577 may both be bought because one is vise/reel-centered and one is tool-content-centered; 18103 becomes the fallback unless its fabrication steel is the reason to buy.
8. **Budget discipline:** another bidder never changes a ceiling. Losing a lot increases available budget; it does not increase the value of the remaining lots.

### Market anchors used for the new ceilings

- Milwaukee 2864-20 used examples sold around **$249.99**, while new tool-only retail is currently around **$429**. This supports the $120 auction ceiling for 18211 after discounting batteries/tools for unknown condition.
- Ridgid 36-inch pipe wrench replacement pricing is roughly **$209-$254**, with 24-inch around **$119**, supporting a low $45 ceiling on the worn three-wrench 18140 lot.
- New portable hydraulic body/ram kits are roughly **$180-$270+**, supporting only a $35 ceiling on the unidentified old 18203 kit because seals, hose and capacity are unverified.
- New basic 4x6 horizontal metal bandsaws are roughly **$350**, supporting a $60 repair-risk ceiling on 18570, which currently cuts crooked.
- Commercial metric socket-cap/retaining-hardware assortments range from roughly **$50 into the hundreds**, supporting 18545's $55 ceiling while recognizing unknown fill.
- Commercial 100-piece hose-clamp/rack assortments can run roughly **$180-$280**, though inexpensive commodity kits are far cheaper; this wide quality spread is why 18564 stops at $40.
- A lot of three vintage Huot drill cabinets sold for **$125** in June 2026; 18573 includes one Huot cabinet plus substantial drill-bit inventory, supporting an $80 ceiling after condition discount.

**Current stop condition:** the 32 focus lots now all have active conditional hammer ceilings in `catalog-review.csv`. Before live bidding, re-read the newest price snapshot and remove any lot already at/over its ceiling; otherwise follow the close-time and substitution rules above.

## September 28 — today-only bid activation plan (6:24 PM EDT snapshot)

**Price basis:** complete refresh `2026-09-28T22:24:09.068695Z`, 487/487 lots, zero refresh errors.

The objective today is **not** to activate every individually defensible maximum. Use early hidden-max bidding only on unique/high-confidence targets where winning all active max bids would still fit the overall spend structure. Preserve flexibility on overlapping and lower-priority lots until tomorrow.

### Activate max bid today

| Lot | Current | Max hammer | Reason |
|---|---:|---:|---|
| **18211** | $65 | **$120** | Full 7-original photo review completed; 2864-20, 2757-series driver, XC5.0, HO XC6.0, third M18 battery and charger confirmed. Unique strong target. |
| **18327** | $15 | **$65** | Full 4-original review completed; specific property/grading use; little substitute dependency. |

These two create only **$185 worst-case hammer exposure** and are the cleanest candidates for early hidden maximums.

### Strong targets, but wait today

| Lot | Current | Max hammer | Why wait rather than activate now |
|---|---:|---:|---|
| **18115** | $10 | $70 | Strong property-use candidate, but only prior visual/contact-sheet review; preserve early-group flexibility and reassess latest price tomorrow. |
| **18530** | $5 | $75 | Bench + Wilton vise remains strong, but prior batch review rather than fresh individual-original pass; late enough to review/reallocate tomorrow. |
| **18161** | $5 | $50 | Excellent cheap grease-equipment alternative, but not necessary to tie up budget a day early. |
| **18573** | $10 | $80 | Strong late-closing drill-storage/bit lot; preserve budget until earlier lots resolve. |
| **18577** | $20 | $60 | Still attractive after moving from $5 to $20, but overlaps shop-bench spending and closes late. |
| **18468** | $5 | $45 | Excellent low-price upside, but exact second impact/model/function uncertainty remains; wait. |
| **18140** | $25 | $45 | Useful pipe wrenches but now over half of ceiling; no advantage to activating early. |
| **18156** | $5 | $40 | Cheap threading/cutting tools; overlaps the pipe-tool category and should remain dormant until tomorrow. |
| **18189** | $10 | $50 | Grinder lot is secondary to 18211/18468 portable-tool spending. |
| **18192** | $10 | $40 | Sawzall/grinder secondary portable-tool purchase. |
| **18193** | $20 | $50 | Hole Hawg has distinct use but is not budget-critical today. |
| **18203** | $10 | $35 | Hydraulic kit remains condition/seal dependent. |
| **18206** | $5 | $30 | Redundant with stronger drill opportunities. |
| **18212** | $5 | $25 | Full original review confirms speculative vintage/parts value, not ready-use communications equipment. Cheap opportunity tomorrow only. |
| **18440** | $25 | $45 | Already >55% of ceiling; no need to show additional activity today. |
| **18501** | $5 | $35 | Band-It opportunity, but lower priority. |
| **18502** | $10 | $35 | Useful hardware; no reason to tie budget early. |
| **18518** | $5 | $30 | Useful tubing but lower priority/non-safety use only. |
| **18544** | $10 | $50 | Hardware-organizer inventory; wait for budget picture. |
| **18545** | $35 | $55 | Already close enough to ceiling that it should not receive an early max. |
| **18561** | $5 | $45 | Strong farm hardware utility; late enough to preserve flexibility. |
| **18563** | $5 | $35 | Mixed organizer/fitting inventory; lower priority. |
| **18564** | $15 | $40 | Commodity hose-clamp inventory; don't activate early. |
| **18570** | $15 | $60 | Bandsaw repair/alignment risk; late close and nonessential. |
| **18578** | $5 | $25 | Overlaps 30-1332 lighting stock. |
| **18590** | $5 | $60 | Collector/storage wildcard; wait until late budget is known. |
| **30-1332** | $5 | $30 | Lighting stock overlaps 18578; choose later. |
| **18558** | $5 | $20 | Low-priority clutter/bench-grinder lot; only consider if still giveaway-price. |

### Do not bid / crossed off at current price

| Lot | Current | Prior ceiling / issue | Action |
|---|---:|---|---|
| **18101** | **$150** | $75 ceiling | **No bid.** Jumped $55→$150 in the latest hour and is now 2× our ceiling. |
| **18439** | **$105** | $60 ceiling | **No bid.** Snap-On air hammer is already far past the researched stop. |
| **18541** | **$245** | Reappraisal supports market plausibility but no active ceiling | **No new bid today.** If already high bidder, leave it alone. Revisit only after confirming whether the photographed floor coils/conduit boxes are included. If all photographed contents are included, a roughly $250–$300 personal-use range may be defensible; do not chase above that without better footage/content confirmation. |
| **18118** | **$30** | $40 ceiling, safety-critical engine hoist | **No max today.** Only $10 of headroom remains; reconsider tomorrow only if the hoist is specifically needed. |

### Today's exposure rule

Placing only the **18211 $120** and **18327 $65** hidden maximums creates **$185 maximum hammer exposure**. This preserves at least **$165 of the $350 planned target** for tomorrow's early and late clusters, while still gaining the earlier-max tie advantage on the two targets with the strongest completed analysis.

If additional source-photo checks today upgrade 18115 or 18530 to the same confidence level, either can be activated then, but avoid having total simultaneously active maximums materially above the $350 planned target without deliberately raising the budget.

## September 28 — shortlist individual-original photo audit

The following 17 active shortlist lots are now confirmed at the **individual-original JPG** review standard, not merely contact-sheet or batch screening:

`18115, 18530, 18161, 18573, 18577, 18468, 18156, 18189, 18193, 18203, 18206, 18440, 18502, 18501, 18544, 18545, 30-1332`.

The September 28 upgrade reopened **100 original JPGs** across the 13 lots that had previously only been batch/contact-sheet reviewed. Four lots (18161, 18203, 18502 and 30-1332) already had individual-original inspection and were not repeated unnecessarily.

Material changes from the upgraded originals:
- **18115:** serious catalog/photo identity ambiguity. Source photos do not cleanly show the cataloged Honda GX140 20x16 plate compactor and separately show a Honda GX160 and unrelated equipment. Previous $70 ceiling is withdrawn; temporary ceiling **$25 pending clarification**.
- **18468:** one impact is clearly an Ingersoll-Rand **2235 TITANIUM** and appears consistent with the common 1/2-inch family rather than the cataloged 3/8-inch drive. Ceiling increased **$45 → $60**, still untested.
- **18501:** full photos confirm genuine BAND-IT tensioning tool, BAND-IT JR adapter and substantial band/clamp stock. Ceiling increased **$35 → $45**.
- **18544:** three organizer stacks are substantially stocked with keys, cable ties, terminals, battery lugs, heat-shrink, pigtails and clamps. Ceiling increased **$50 → $75**.
- **18545:** three organizer stacks are materially stocked with metric/standard fasteners, socket-head screws, studs, retaining rings, spring pins, set screws and self-drilling/binding-head screws. Ceiling increased **$55 → $80**.
- **18530:** vise/reel remain attractive but bench top is badly deteriorated around the vise; **$75 retained**.
- **18573, 18577, 18156, 18189, 18193, 18206 and 18440:** originals support the existing active ceilings; detailed findings are in `catalog-review.csv`.

**30-1332 is a valid auction-1879 lot**, OrbitBid item number `1-30-1332`, internal ID `1799881`, titled “5 boxes of truck and equipment lights, grommets, etc.” Its non-18xxx numbering is why it is easy to miss in the catalog. Five originals were individually inspected on September 25.

## September 28 — complete 34-lot shortlist original-photo standard

The **entire 34-lot working shortlist is now individually reviewed from every original source JPG**. This is no longer a mixed contact-sheet/batch-screening shortlist.

- **34 / 34 shortlist lots:** individual-original review complete.
- **248 / 248 source JPGs across those 34 lots:** individually inspected.
- The final 11 upgrades were: `18118, 18140, 18192, 18439, 18558, 18561, 18563, 18564, 18570, 18578, 18590` (82 originals).
- Detailed per-lot findings and active conditional hammer ceilings are in `catalog-review.csv`.

Material changes from the final 11-lot upgrade:
- **18558:** dense bolts/nuts/hardware contents plus RAM bench grinder are stronger than prior contact-sheet shorthand; ceiling **$20 → $30**. Wood organizer remains excluded.
- **18561:** substantial hitch/fabrication hardware inventory confirmed; ceiling **$45 → $60**. Old hooks/eyes/rigging are not assumed certified for lifting.
- **18563:** catalog explicitly includes the contents of the wood workbench drawers in addition to the two organizers; originals confirm meaningful springs, fittings, specialty tools and hardware; ceiling **$35 → $50**.
- **18564:** two display racks hold dozens of hose clamps across many sizes; ceiling **$40 → $50**.
- **18578:** originals confirm multiple packaged Maxxima LED lamps, Grote/Wagner/Philips/NAPA lighting and several RETRAC mirrors; ceiling **$25 → $45**, still coordinated against 30-1332.
- **18590:** Borg-Warner illustrated automotive-parts cabinet plus Tung-Sol display and mixed vintage contents have stronger collector/display value than prior shorthand; ceiling **$60 → $75**.
- **18118, 18140, 18192, 18439 and 18570:** full originals support the existing ceilings; no increase made.
- **18439** remains over its $60 ceiling at the latest known bid despite the improved photo certainty.

This checkpoint supersedes earlier statements that some shortlist lots were only contact-sheet or batch-reviewed. Any future shortlist recommendation should use the individual-original findings in the current master.



## September 29 — quick full-auction price rescreen and active shortlist

**Price basis:** latest successful scheduled refresh run checked at 2026-09-29T01:54:58Z. The repository price snapshot remains 2026-09-29T01:24:16Z because subsequent successful refreshes produced no committed price changes. Auction terms remain as-is/where-is, 13% buyer premium (10% with qualifying cash/cashier's check/wire), and 10-minute dynamic extensions.

The active shortlist below supersedes earlier active-list sections. Lots already over their ceilings remain historical review records but are not active targets.

New/revised targets from this rescreen:
- **18123 Miller AEAD-200LE welder/generator — max $325 hammer.** Ten original JPGs reviewed from GitHub artifact run 36509368869. Complete-looking Onan-powered AC/DC stick welder/generator, substantial leads, cart, 120/240V auxiliary generation; operation unknown. Recent unknown-condition AEAD-200LE comp $522.50. Treat 18125 as substitute, not additive.
- **18125 Lincoln Idealarc 250 — max $175 hammer.** Eight original JPGs reviewed. Nameplate confirms 230/460V, 70/35A, 60Hz, **single phase**. Complete-looking AC/DC stick machine with heavy leads/cart; operation unknown. Substitute if 18123 is lost or Miller exceeds ceiling.
- **18388 Turner Tillage ~10-ft offset disc — provisional max $125 hammer pending transport/fit/use confirmation.** Full-auction price rescreen found it at only $10. High farm/property utility potential, but it is not yet at the same photo/market-review confidence as the established shortlist; do not raise beyond provisional ceiling without reviewing originals.
- **18133 new boxed Predator 212cc engine — max $65 hammer.** At $35 in current snapshot; useful replacement-power inventory but commodity item, so ceiling remains conservative.

Current active ceilings:
18115 $25; 18118 $40; 18123 $325; 18125 $175; 18133 $65; 18140 $45; 18156 $40; 18161 $50; 18189 $50; 18192 $40; 18193 $50; 18203 $35; 18206 $30; 18211 $120; 18212 $25; 18327 $65; 18388 $125 provisional; 18468 $60; 18501 $45; 18502 $35; 18518 $30; 18530 $75; 18558 $30; 18561 $60; 18563 $50; 18564 $50; 18570 $60; 18573 $80; 18577 $60; 18578 $45; 18590 $75; 30-1332 $30.

Substitution/budget note: 18123 and 18125 are alternatives. The $325 Miller ceiling is an item-specific value ceiling, not authorization to exceed the prior overall auction spending target; aggregate exposure must be reassessed as lots resolve. 18578 and 30-1332 remain substitutes unless both stay exceptionally cheap. 18193 remains preferred over 18206 for heavy drilling.


### Lot 18388 — original-photo review completed (September 29)

All **9 original source JPGs** from artifact run 36516141629 were inspected individually.

- Confirmed older **Turner Tillage** pull-type offset disc, cataloged at approximately 10 ft.
- Heavy welded/bolted frame appears substantially complete with both disc gangs present.
- Gang blades show broad surface rust and wear but no obvious wholesale missing gang/blade section in the nine views.
- Frame has extensive weathering/lichen consistent with long outdoor storage, but no obvious catastrophic main-frame break is visible.
- Hitch/drawbar hardware is present. Adjustment/transport hardware is old and should be expected to need freeing/lubrication.
- The implement is deeply overgrown, so bearing freedom, gang seizure, bent axles, hidden weld repairs, and underside/frame condition cannot be verified from photos.
- Several loose disc blades are stacked on top; treat them as possible spares only, not evidence that the installed gangs are defective.
- This is a heavy older farm implement, not a light compact-tractor 3-point disc; tractor horsepower/weight and transport logistics must be confirmed before use.

**Bid ceiling:** raise provisional $125 to **$250 hammer** as an item-value ceiling, because the originals show a substantially complete heavy offset disc rather than scrap. Keep the ceiling conservative for unknown bearings/gang condition and removal logistics. This remains subordinate to tractor compatibility and the overall auction budget.


## September 29 — auction-morning price checkpoint (7:51 AM EDT)

**Price basis:** successful scheduled refresh `2026-09-29T11:51:10.446918Z`, 487/487 lots, zero refresh errors.

Decision/status changes:
- **18388 Turner offset disc: SKIP.** The prior $250 figure remains an underlying item-value conclusion from the completed nine-original review, but transport/removal of the approximately 10-ft wheel-less implement is not worthwhile. Remove it from the active bidding shortlist.
- **18118 RAMCO Shop Hand 5000: OUT.** Current bid $75 exceeds the established $40 hard ceiling. Do not raise the ceiling merely because bidding increased.
- **18440 Snap-On RTD33: OUT** at $55 versus $45 ceiling.
- **18544 electrical/hardware organizers: OUT** at $200 versus $75 ceiling.
- **18545 fastener organizers: OUT** at $135 versus $80 ceiling.
- Existing out lots remain out: **18101** $155 versus $75 and **18439** $115 versus $60.
- **18123 Miller AEAD-200LE** remains the primary welder target at $165 / $325 max; **18125 Lincoln Idealarc 250** is the substitute at $115 / $175 max. Do not budget both maxima as additive purchases.
- **18161 grease-pump pair** remains exceptionally cheap at $5 / $50 max; under roughly $25 remains especially attractive.
- **18211 Milwaukee M18 lot** remains $65 / $120 max and a strong target.
- **18327 steel mesh drag** remains $20 / $65 max and retains direct personal-use value.
- Master consistency fix: established ceilings for 18123 ($325), 18125 ($175) and 18133 ($65) are now populated in `catalog-review.csv`; these are not new valuation changes.

Full-auction movement rescreen: meaningful upward moves are concentrated in already-expensive heavy equipment and several tool/hardware lots. No previously ignored/deprioritized lot became newly attractive *because of price movement*; OrbitBid bids only moved upward. Several still-cheap high/medium screening lots remain research possibilities, but none is promoted to an active target without adequate existing evidence or new market research.

Morning strategy remains budget/substitution driven: protect the Miller/Lincoln alternative relationship, favor 18161 while cheap, keep 18211 reserve intact for 6:30, use 7:00 hardware/tool opportunities only if earlier targets are lost, preserve late capacity for 18573/18590/18561 and related low-price lots, and retain the $65 drag ceiling for 8:00.
