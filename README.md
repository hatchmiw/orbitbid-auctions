# OrbitBid Auctions

Public working repository for OrbitBid auction research.

## Workflow

1. Open the OrbitBid auction page in Chrome.
2. Open DevTools → Console.
3. Run the launcher below.
4. The latest exporter is loaded from this repository.
5. The exporter downloads:
   - `summary.md`
   - `lots.json`
   - `summary.csv`
6. Put those files under `auctions/<auction-id>/`.

## Console launcher

```javascript
fetch(
  "https://raw.githubusercontent.com/hatchmiw/orbitbid-auctions/main/orbitbid-exporter.js?ts=" + Date.now()
)
  .then(r => {
    if (!r.ok) throw new Error(`Exporter load failed: HTTP ${r.status}`);
    return r.text();
  })
  .then(code => {
    console.log("Loaded OrbitBid exporter from GitHub.");
    (0, eval)(code);
  })
  .catch(err => console.error("EXPORTER ERROR:", err));
```

## Current auction

- Auction ID: **1970**
- Current exporter range: **9926–9985**
- Lots 9900–9925 are intentionally excluded for today's review because they are conduit lots.

## Notes

- Auction data is a snapshot at the time the exporter is run.
- Full-resolution image URLs are included in `summary.md` and `lots.json`.
- No personal OrbitBid login token is stored in this repository.
- The exporter uses OrbitBid's public lot endpoint and public client token.
