# dotfiles-T96-codex-worker-gpt61-sol-high-a01 — learning triage

1. **Model availability under the ChatGPT login changes over time.**
   - On 2026-10-01 the T48 probe recorded that `gpt-6.1-sol` was rejected with "400 … not supported when using Codex with a ChatGPT account". On 2026-10-05 the same model answered under the same login through the deployed `audit` profile.
   - Auth-path claims in rules and README should cite a dated live probe and be re-probed when a model moves between seats, rather than carried forward.
   - The probe needs no ad-hoc model flags: `codex --profile <name> exec --sandbox read-only --skip-git-repo-check '<one-word prompt>'` against an already-deployed profile that runs the model.
2. **Task line hints can point at the wrong pin.** The task named validator line ~74 as the audit pin, but that line is `ADH_PROFILE`. The audit pin is at ~686. Re-reading the code before editing caught it (the orchestrator confirmed: leave ADH).
3. **`model-profiles.env` holds only `--profile <name>` arguments**, so a model change regenerates just the per-profile Codex modify scripts.
