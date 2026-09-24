# OrbitBid Auction 1879

Automated snapshot of OrbitBid auction **1879**.

- Source: https://bid.orbitbid.com/?items=all&auction_id=1879&display=grid&limit=60&page=1
- Retrieved: 2026-09-24T17:32:58.214789Z
- Catalog lots discovered: 487
- Lots retrieved: 487
- Retrieval errors: 0

## Review files

- [REVIEW.md](REVIEW.md) — catalog-review coverage, limitations and resume checkpoint
- [catalog-review.csv](catalog-review.csv) — entire 487-lot first-pass review, including image links and conditional ranges where provided
- [provisional-watchlist.csv](provisional-watchlist.csv) — preliminarily priced candidates and conditional maximum hammer bids
- [all-lots-review.md](all-lots-review.md) — readable notes for all 487 lots

## Files

- `summary.md` — readable lot-by-lot snapshot with source photo links
- `summary.csv` — compact current lot index with readable UTC closing times
- `lots.json` — complete structured data used by the photo mirroring workflow
- `price-history.csv` — timestamped bid/bid-count history from exports and price refreshes
- Photos and review sheets live in a temporary GitHub Actions artifact; original image URLs remain in `summary.md`

This export uses OrbitBid's public auction catalog and public lot endpoint. It does not use a bidder login or personal account token.
