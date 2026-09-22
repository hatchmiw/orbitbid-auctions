# OrbitBid Auctions

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
6. Photos and `review.jpg` sheets are stored in a temporary Actions artifact named:
   - `orbitbid-<auction-id>-photos`

The rendered-catalog exporter includes a mixed-auction safety check so a suspicious catalog result fails instead of silently committing unrelated OrbitBid lots.

## Photo retention

Photo artifacts are temporary.

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

This is the preferred way to update live prices for auction **1970** (Mid Michigan Greenhouses) or any other already-saved auction.

## Troubleshooting workflows

- **Export OrbitBid auction** — older metadata-only exporter; retained for troubleshooting.
- **Mirror auction photos** — rebuilds a temporary photo + review-sheet artifact from an existing `lots.json`.
- **Build auction contact sheets** — legacy helper for photo folders already present in the repository.
- **Purge expired OrbitBid photos** — can be manually triggered instead of waiting for its six-hour schedule.

## Notes

- No bidder password or personal OrbitBid login credential is stored in this repository.
- The permanent `lots.json` snapshot contains original OrbitBid image URLs, allowing high-resolution source images to be revisited even after temporary mirrors expire.
- `orbitbid-exporter.js` remains as a browser-console fallback/debugging tool; it is no longer the normal workflow.
