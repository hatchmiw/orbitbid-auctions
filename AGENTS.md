# Repository instructions for auction-review agents

Before **every** auction research, photo-inspection, valuation, workflow edit or resumed batch, read and follow [AUCTION_REVIEW_SOP.md](AUCTION_REVIEW_SOP.md), the root README, the relevant `auctions/<id>/REVIEW.md` and the applicable workflow YAML. Do not rely on prior chat memory as the authoritative state.

**Critical:** reuse existing temporary GitHub Actions photo artifacts before downloading anything. Never commit auction photos or contact sheets to Git. Confirm artifact contents, image provenance and existing reviewed lot IDs before starting a batch. Update text-only checkpoints on each completed pass. If the artifact is missing or expired, document that and only then use the minimum necessary recovery download.

When resuming, state the SOP version/commit consulted and the artifact/run or reason for recovery. If a task conflicts with the SOP, ask for clarification rather than silently changing photo retention or review status.

## Mandatory retrieval and no-improvisation rule (2026-09-25)

Before **every** OrbitBid task, including resumed work, read the root SOP, this file, root README, auction REVIEW and relevant workflow YAML. For photos, use the SOP's **GitHub `download_workflow_artifact` → ZIP extraction → source/lot verification → actual original JPG vision** procedure, proven by the Pioneer runbook. The generic GitHub fetch tool does not download Actions artifact ZIPs. The connector's 512 MiB per-artifact limit requires existing smaller split artifacts; auction 1879's batch-07 ZIP was successfully downloaded, and split batches 08–13 exist. Do not describe this as a general binary-download restriction.

**Follow the documented SOP rather than improvising.** If its normal path fails, verify the failure, check its artifact-only split/recovery procedure, and **discuss any further change of approach with the user before implementing it**. Do not silently request manual uploads, redownload source photos, create permanent image copies, substitute contact sheets for full originals, or change review scope. Record the SOP commit read, artifact IDs, source-photo verification and completed lot IDs in each durable checkpoint.
