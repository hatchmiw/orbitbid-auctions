# OrbitBid auction bootstrap requests

Creating or updating a numeric request file in this directory starts the normal
**Run OrbitBid Auction** GitHub Actions workflow for that auction.

## File format

Use the auction ID as the filename:

```text
auction-requests/1920.txt
```

The file contents are informational only. A short note such as the request time,
reason, or requester is enough.

## How it works

1. A push that adds or modifies `auction-requests/<auction_id>.txt` starts
   `.github/workflows/bootstrap-orbitbid-auction.yml`.
2. The bootstrap workflow validates the numeric auction ID from the filename.
3. It dispatches the existing `run-orbitbid-auction.yml` workflow with that
   auction ID.
4. The normal ingestion workflow then exports metadata, commits the permanent
   auction files, mirrors temporary source photos, builds review sheets, verifies
   them, and uploads the temporary photo artifact.

To run the same auction again later, update the contents of its existing request
file. The manual **Actions → Run OrbitBid Auction** workflow remains available as
a fallback.
