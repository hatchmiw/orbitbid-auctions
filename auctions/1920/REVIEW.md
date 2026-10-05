# OrbitBid 1920 — Creviston Trucking retirement liquidation review

**Governing procedure:** [SOP v3](../../AUCTION_REVIEW_SOP.md). The editable per-lot master is [catalog-review.csv](catalog-review.csv); `lots.json` will be the source catalog after ingestion.

## Scope and decision rules

- **Primary objective:** personal-use opportunities first; resale only when the spread is unusually compelling after fees, pickup burden, repair risk and selling effort.
- Screen the **entire auction catalog** once. Do not stop at an arbitrary batch size.
- Use contact/review sheets for rapid whole-catalog screening only. For shortlisted candidates, inspect **every original source JPG individually** before final condition conclusions.
- Research dated completed sales for shortlisted lots before assigning active resale ranges or hammer ceilings.
- Do not treat placeholder/current early bids as market values.
- Preserve separate states for whole-catalog screening, original-photo inspection, market research and live-bid decision.

## Auction facts verified from OrbitBid

- Auction: **Creviston Trucking Inc. Retirement Liquidation Auction**
- Auction ID: **1920**
- Location: **6001 Kennedy Ave, Hammond, IN 46323**
- Scheduled end: **October 6, 2026**
- Inspection: **October 5–6, 10:00 a.m.–5:00 p.m. CT**
- Removal: **October 7–9, 9:00 a.m.–5:00 p.m. CT**, except where an individual lot specifies otherwise.
- Buyer premium: **13%**, reduced to **10%** when the invoice is paid in full by cash, cashier's check or wire transfer.
- Auction-stated sales tax: **7%**, applied to the hammer plus buyer premium.
- Approximate all-in multiplier before title/transport costs:
  - qualifying 10% premium payment: **hammer × 1.177**
  - 13% premium payment: **hammer × 1.2091**
- No loading dock. Forklift is stated to be available during removal on a first-come, first-served basis.
- Buyer is responsible for disassembly, loading, packaging and shipping.
- Titled items carry separate title/broker processing requirements and fees.

## Catalog profile

This is a trucking-company liquidation. OrbitBid highlights roughly 20 semi tractors, 21 straight/box trucks, 20 semi-trailers, support vehicles, shop equipment, tires, truck parts and office contents.

The full catalog must be ingested before screening counts or completion claims are made.

## Initial screening seeds — not yet recommendations

Public OrbitBid pages already identify several categories worth checking carefully once the catalog/photo artifact is available:

### Personal-use / shop-fit candidates
- **1-17859** — Dayton bench grinder with steel table.
- **1-17860** — Enerpac porta-power pump/bottle; catalog says pump may need repair.
- **1-17861** — OTC king-pin wall-mount tooling with hand pump/accessories.
- **1-17863** — Matco hydraulic porta power.
- **1-17864** — Ridgid 16-gallon shop vacuum.
- **1-18651** — Milwaukee 7-1/4 in. corded circular saw with case.
- **1-18652** — Milwaukee 18-gauge corded shear.
- **1-18654** — large assorted hand-tool lot.
- **1-18671** — Associated 100/75A charger with 375A engine-start function.
- **1-18672** — Auto Specialties D8200 heavy-duty hydraulic transmission jack; catalog says working.
- **1-18674** — Sunex 1 in. pneumatic impact + Chicago Pneumatic 1/2 in. impact.
- **1-18675** — pullers and C-clamps.
- **1-18678** — extension cords, halogen lights and bulbs.
- **1-18679 / 1-18684** — steel shop-cart lots.
- **1-18682** — pair of 10-ton pin-style jack stands.
- **1-17884** — large assorted hardware lot.
- **1-17886** — Bessey 6 in. vise with metal shop table.
- **1-17887** — Delta/Rockwell bench drill press with Huot drill index.

### Larger / capital-intensive candidates
- **1-10020** — 2011 New Holland L223 skid steer, 716 hours showing, enclosed cab, 2-speed and 72 in. bucket. Catalog notes **delayed removal**. Treat hour reading and mechanical condition as unverified until photos/video/inspection are reviewed.

### Bargain/resale-only possibilities
- **1-17853** — four new Firestone FS591 295/75R22.5 16-ply truck tires.
- **1-18685** — approximately 42 new Global rubber wheel chocks.
- **1-17125** — Ariens 2-stage electric-start snowblower; catalog says runs/operates.
- Truck-parts lots such as **1-17890 / 1-17891 / 1-17892** may have value only if identification, quantity and realistic local resale justify the handling burden.

These are only seeds from publicly indexed pages. They do **not** replace the whole-catalog screen.

## Setup state

- [x] Auction-specific review record created.
- [x] Master `catalog-review.csv` initialized.
- [x] Push-trigger bootstrap installed and verified.
- [x] Direct public catalog API ingestion installed and verified.
- [x] Complete metadata export committed for auction 1920.
- [x] Temporary source-photo/review artifact `orbitbid-1920-photos` created.
- [ ] Populate the master from the ingested catalog.
- [ ] Complete whole-catalog screen.
- [ ] Build candidate queue.
- [ ] Individually inspect originals and research completed sales for each candidate.
- [ ] Produce actionable shortlist and live-bid ceilings where evidence supports them.

## Exact next action / blocker

Ingestion is complete. Resume from the committed auction 1920 metadata and the existing `orbitbid-1920-photos` artifact. The next task is to populate `catalog-review.csv` from the source catalog and perform the whole-catalog opportunity screen. Do not re-scrape the catalog or create a parallel review ledger.
