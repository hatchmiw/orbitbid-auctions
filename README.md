# OrbitBid Auctions

Public working repository for OrbitBid auction research.

## GitHub workflow

The normal workflow now runs entirely inside GitHub. You do not need to open the OrbitBid site, use DevTools, paste JavaScript, download a ZIP, or manually move the export files.

### 1. Export an auction

1. Open this repository on GitHub.
2. Open **Actions**.
3. Select **Export OrbitBid auction**.
4. Click **Run workflow**.
5. Enter the OrbitBid `auction_id` and run it.

The workflow discovers the auction's actual internal lot IDs from the public OrbitBid catalog, retrieves the public lot records, and commits these files automatically:

- `auctions/<auction-id>/README.md`
- `auctions/<auction-id>/summary.md`
- `auctions/<auction-id>/summary.csv`
- `auctions/<auction-id>/lots.json`

Skipped public lot numbers and unusual lot numbers are handled by catalog discovery rather than by assuming a consecutive lot-number range.

### 2. Mirror the auction photos

After the export succeeds:

1. Open **Actions**.
2. Select **Mirror auction photos**.
3. Click **Run workflow**.
4. Enter the same OrbitBid `auction_id`.
5. Run it.

The photo workflow reads `auctions/<auction-id>/lots.json`, downloads the public auction photos, normalizes them for the repository, and commits them under:

- `auctions/<auction-id>/photos/`

### 3. Build contact sheets when needed

Run **Build auction contact sheets** with the same auction ID after the photos have been mirrored. It creates the per-lot `review.jpg` files used for faster visual review.

## What the exporter uses

- OrbitBid's public auction catalog to discover the actual lot IDs.
- OrbitBid's public lot GraphQL endpoint to retrieve titles, descriptions, bids, fields, timing, and image URLs.
- No bidder login or personal OrbitBid account token.

## Legacy browser exporter

`orbitbid-exporter.js` remains in the repository as a fallback/debugging tool, but it is no longer the normal workflow.
