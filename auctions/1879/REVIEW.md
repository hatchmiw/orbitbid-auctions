# OrbitBid 1879 — current review checkpoint

**Read [the required auction SOP](../../AUCTION_REVIEW_SOP.md) and [agent instructions](../../AGENTS.md) before every continuation.** Existing temporary photo artifacts must be reused; do not re-download photographs or commit images for each review batch.

## Deeper original-image and price-review progress

- **20 of 485 pictured lots** have now received a separate review of all original source images (106 images) and broad conditional as-is resale/hammer estimates. These are the first two durable 10-lot checkpoints in [the full-image and price-review report](full-image-price-review.md). **465 pictured lots still require the deeper original-image pass.**
- Original 200 valuations from batches 01–05 are preserved; 30 additional lots now have provisional ranges (20 after a deeper original-photo pass, 10 based on existing source-verified composites). **No exact-match sold-comparable verification** has been established for these new ranges. The remaining 255 of the previously unvalued 285 pictured lots still lack price ranges. The 10 composite-priced lots remain in the 465-lot individual full-resolution review queue.
- The initial contact-sheet review of 485 lots remains complete but must not be described as full-resolution individual-image verification.

## Completed initial review

- **487 of 487 catalog lots accounted for**; **485 of 485 pictured lots** inspected at per-lot contact-sheet level across batches 01–13. **Zero pictured lots remain awaiting initial contact-sheet inspection.**
- Two lots have no source photographs: **18284** (partial hoist-line spools) and **18583** (boxed ESAB welding wire). Catalog-only triage; do not mark visually inspected.
- **200 lots** from batches 01–05 have existing conditional gross resale ranges and maximum hammer ceilings in [provisional-watchlist.csv](provisional-watchlist.csv). **285 more pictured lots** from batches 06–13 have photo-specific condition/identity findings but **not independently verified resale estimates or bid ceilings**. All 487 entries remain in [catalog-review.csv](catalog-review.csv), with no duplicate rows or duplicated valuations.
- [Final review status and research shortlist](FINAL_REVIEW_STATUS.md) summarizes findings and the remaining financial, mechanical and live-bid verification work.

## Visual reports

| Batch | Pictured lots | Review report |
|---|---:|---|
| 01 | 40 | [Batch 01](visual-review-batch-01.md) |
| 02 | 40 | [Batch 02](visual-review-batch-02.md) |
| 03 | 40 | [Batch 03](visual-review-batch-03.md) |
| 04 | 40 | [Batch 04](visual-review-batch-04.md) |
| 05 | 40 | [Batch 05](visual-review-batch-05.md) |
| 06 | 40 | [Batch 06](visual-review-batch-06-partial.md) |
| 07 | 40 | [Batch 07](visual-review-batch-07.md) |
| 08 | 40 | [Batch 08](visual-review-batch-08.md) |
| 09 | 40 | [Batch 09](visual-review-batch-09.md) |
| 10 | 40 | [Batch 10](visual-review-batch-10.md) |
| 11 | 40 | [Batch 11](visual-review-batch-11.md) |
| 12 | 40 | [Batch 12](visual-review-batch-12.md) |
| 13 | 5 | [Batch 13](visual-review-batch-13.md) |

## Artifact and provenance checkpoint

- Source: permanent complete [487-lot catalog](lots.json), original OrbitBid image URLs and the original temporary photo artifact `orbitbid-1879-photos`, successful run `36039298628`, artifact `10825787468`.
- Batch 07 used temporary artifact `10844646656`, run `36087152300`, covering 40 lots and 257 source photographs.
- Batches 08–13 reused the **existing** full-auction artifact via [artifact-only splitting workflow](../../.github/workflows/review-from-existing-artifact.yml), successful run `36087642169`. Six temporary artifacts cover the final 205 pictured lots in non-overlapping groups of 40/40/40/40/40/5; their manifest counts were verified. **No new OrbitBid image download** was needed for these six batches.
- Historic `review-previews/` images were removed from the current Git branch; some older batch-report links to them are obsolete. Consult temporary artifacts and permanent original image URLs instead. Do not restore committed images.

## What is and is not finished

**Finished:** all catalog entries triaged, all available lot photo contact sheets reviewed, individual visible-condition notes documented for all pictured lots, and the 487-row master catalog updated without repeating completed work.

**Still requiring separate verification before bidding:** exact sold comps and defensible price ceilings for the 285 newly inspected lots, fresh bid prices, buyer premium/tax, physical equipment tests, high-resolution close-ups for selected expensive machinery, and pickup/transport feasibility. Source bid snapshot is **2026-09-24 17:32:58 UTC**. Visual review is not proof of mechanical operation or safe lifting/pressure-vessel use.

**Next action:** refresh current auction prices and perform targeted sold-comparable and functional-condition research for shortlisted practical resale/personal-use lots, rather than repeating any initial photo inspections.
