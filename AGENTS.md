# Repository instructions for auction-review agents

Before **every** auction research, photo-inspection, valuation, workflow edit or resumed batch, read and follow [AUCTION_REVIEW_SOP.md](AUCTION_REVIEW_SOP.md), the root README, the relevant `auctions/<id>/REVIEW.md` and the applicable workflow YAML. Do not rely on prior chat memory as the authoritative state.

**Critical:** reuse existing temporary GitHub Actions photo artifacts before downloading anything. Never commit auction photos or contact sheets to Git. Confirm artifact contents, image provenance and existing reviewed lot IDs before starting a batch. Update text-only checkpoints on each completed pass. If the artifact is missing or expired, document that and only then use the minimum necessary recovery download.

When resuming, state the SOP version/commit consulted and the artifact/run or reason for recovery. If a task conflicts with the SOP, ask for clarification rather than silently changing photo retention or review status.
