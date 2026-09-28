# OrbitBid Auctions

**Required before any auction review or workflow change:** [AUCTION_REVIEW_SOP.md](AUCTION_REVIEW_SOP.md) and [AGENTS.md](AGENTS.md). The SOP requires reuse of existing temporary photo artifacts before any new download. Batch review must not commit images.


Public working repository for OrbitBid auction research.

## Normal workflow: one button

1. Open **Actions → Run OrbitBid Auction**.
2. Click **Run workflow**.
3. Enter the OrbitBid auction ID.
4. GitHub renders the auction catalog in Chromium, exports the lot metadata, downloads the photos, and builds the per-lot review sheets.
5. Permanent metadata is committed under `auctions/<auction-id>/`:
   - `README.md`
   - `summary.md`
   - `summary.csv`
   - `lots.json`
   - `price-history.csv`
6. Photos and `review.jpg` sheets are stored in a temporary Actions artifact named:
   - `orbitbid-<auction-id>-photos`

The rendered-catalog exporter includes a mixed-auction safety check so a suspicious catalog result fails instead of silently committing unrelated OrbitBid lots.

## Photo retention

Photo artifacts are temporary. The 1879 source-verified batch review also uploads original photos and per-lot review sheets to a temporary Actions artifact, rather than committing them to the repository. Previous committed review-preview images are removed from the current branch; old Git history may still contain them.

- The retention deadline is based on the **latest scheduled lot closing time in the auction + 7 days**.
- It is not based on when the GitHub workflow was run.
- **Purge expired OrbitBid photos** runs every six hours and removes expired artifacts.
- It also removes any legacy `auctions/<id>/photos/` folders committed by the older workflow.
- Permanent metadata and original OrbitBid image URLs remain after cleanup.

GitHub artifact retention is capped at 90 days. For auctions more than 90 days from closing, rerun the workflow closer to the sale if the photos are still needed.

## Refresh current prices without touching photos

For an auction that has already been imported:

1. Open **Actions → Refresh OrbitBid prices**.
2. Enter the saved OrbitBid auction ID.
3. Run the workflow.

This workflow reads the known internal OrbitBid lot IDs already saved in `lots.json`, refreshes the current bid/status data, and commits updated metadata only. It does **not** rediscover the catalog and does **not** download or change any photos.

Each refresh appends one timestamped row per lot to `price-history.csv`, preserving the bid amount and bid count from that moment. `summary.csv` also includes human-readable UTC closing-time columns alongside OrbitBid's raw timestamps.

Price refreshes are also scheduled automatically for saved auctions:

- **Hourly** before auction day, at minute 7 of each hour.
- **Every 10 minutes** on any America/Detroit calendar day containing a scheduled lot close.
- The 10-minute cadence continues through a **six-hour grace period after the final scheduled lot close**, including across local midnight.
- After final close + six hours, that auction is automatically excluded from scheduled refreshes.
- Manual **Refresh OrbitBid prices** runs remain available at any time for a specific saved auction.

The scheduler derives close times from each saved auction's `lots.json`, so newly imported auctions do not require hard-coded dates or auction IDs.

## Import my authenticated OrbitBid Watch List

The Watch List is captured in the signed-in browser, but authentication data never leaves the browser.

1. Sign in to OrbitBid and open **Watch List**.
2. Run the root `orbitbid-watchlist-exporter.js` in the browser console.
3. The exporter collects only OrbitBid internal lot IDs and a capture timestamp. It does not read/export cookies, login/session tokens, bidder identity, card text, max bids or auto bids.
4. Copy the compact JSON produced by the exporter.
5. Run **Actions → Import OrbitBid Watch List** and paste that JSON.

The importer writes `watchlists/orbitbid.json` and cross-references each watched internal lot ID against all saved `auctions/*/lots.json` records. Public bid/title/photo data stays in the existing auction files, so price refreshes continue unchanged and there is no duplicate bid-history pipeline.

This repository is public. The imported Watch List file exposes **which lot IDs are personally watched**, even though it contains no login credentials or private bid amounts. See [watchlists/README.md](watchlists/README.md) before importing.

This membership layer is separate from `catalog-review.csv`: a lot may independently be personally watched, an analysis/research candidate, or an opportunity discovered by screening without overwriting the other classifications.

## Troubleshooting workflows

- **Export OrbitBid auction** — older metadata-only exporter; retained for troubleshooting.
- **Mirror auction photos** — rebuilds a temporary photo + review-sheet artifact from an existing `lots.json`.
- **Build auction contact sheets** — legacy helper for photo folders already present in the repository.
- **Purge expired OrbitBid photos** — can be manually triggered instead of waiting for its six-hour schedule.

## Notes

- No bidder password or personal OrbitBid login credential is stored in this repository.
- The permanent `lots.json` snapshot contains original OrbitBid image URLs, allowing high-resolution source images to be revisited even after temporary mirrors expire.
- `orbitbid-exporter.js` remains as a browser-console fallback/debugging tool; it is no longer the normal workflow.

## Required procedure for opportunity-first auction research

Before every auction task, read [AGENTS.md](AGENTS.md), [AUCTION_REVIEW_SOP.md](AUCTION_REVIEW_SOP.md), the auction's current `REVIEW.md`, the master catalog and the relevant workflow. Screen the entire catalog using metadata and existing preliminary photo notes. **Individually inspect every original JPG only for shortlisted research candidates**; do not misrepresent contact-sheet screening as full-original inspection. Reuse the verified GitHub Actions artifact ZIP download → extract exact lot JPGs method. The connector's ZIP artifact download limit is 512 MiB; reuse existing split artifacts or the documented artifact-only splitting workflow. Never commit photos, ZIPs or contact sheets. Record evidence-backed completed sales and produce a small actionable shortlist before expanding research.

## Review records and archived procedures

The sole editable per-lot review master is `auctions/<id>/catalog-review.csv`; `lots.json` is the source catalog. Current auction status and the exact resume checkpoint belong in `auctions/<id>/REVIEW.md`. Generated research queues, watchlists and status reports are derived from the master. Historical review reports are evidence, not competing completion ledgers. The superseded SOP and redundant auction 1879 reports are retained under [`archive/2026-09-25-pre-cleanup`](archive/2026-09-25-pre-cleanup/). The fixed pre-cleanup recovery branch is `archive/pre-sop-cleanup-2026-09-25` at commit `02b8ef03d88c7a4f31788fef13043252ace6ec0e`.

