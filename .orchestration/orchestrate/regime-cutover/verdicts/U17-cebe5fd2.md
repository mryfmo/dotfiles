# U17 verdict, head cebe5fd23835cb840f83fcfb535a6e53a735bbc9 (PR #485, round 2, U17c documentation round)

Orchestrator seat `orchestrator-zero` (O2, lane A). Round 1 (head eec0e215, `incorrect`, two audit findings equal to the Codex comments, D-024-148) is in `U17-eec0e215.md`; this round adds only what changed.

## U17c (TASK id=1324 to `worker-mugo`, RESULT row 1442)

- Commit cebe5fd2 `docs(claude): the sandbox secret guard's two limits under D-024-148`. Diff eec0e215..cebe5fd2: `README.md` (+11/-1), `home/dot_agents/agent-config.yaml` (+5 comment lines). The rendered template and every rule are unchanged (the diff touches no other file); `scripts/generate-agent-configs.py --check` in a `git archive` copy → `generated agent configs are up to date`.
- Text added (the explicit deployment contract the audit asked for): the sandbox layer covers sandboxed runs only; under auto mode with `allowUnsandboxedCommands: true` a failed command may be retried outside the sandbox after the classifier, where only the tool-layer Read/Edit rules apply and those do not reach arbitrary Python or Node reads; an `ask` rule for that retry is the D-024-148 follow-up decided with the operator. `denyRead` is home-anchored, so managed hosts keep project checkouts under `$HOME` (deployment restriction) until the root-anchored form is measured on the Linux host.
- `gh pr view 485 --json headRefOid` → `cebe5fd23835cb840f83fcfb535a6e53a735bbc9`, `mergeStateStatus: CLEAN`, 9 files unchanged in set.
- Check runs on cebe5fd2: GitGuardian, public-bootstrap ×3, regime, test ×4, validate, all `completed success` (10/10).
- Orchestrator spot-check of the eec0e215 copy (code unchanged since): `test_validate_agent_assets -k deny -k deny_read -k credential` → `Ran 2 tests OK`; `test_generate_agent_configs -k sandbox_renders -k LinuxGlobWarningParser -k deny_rules` → `Ran 4 tests OK`. The local `validate-agent-assets.py` run did not finish in 600 s in this seat's sandbox (`error: interrupted`); CI's `validate` check on both heads is the authoritative run.

## Step 4 (audit seat `audit-tomo`)

Worktree positioned at cebe5fd2, clean. TASK id=1452 → VERDICT row 1473 `verdict=correct head=cebe5fd23835cb840f83fcfb535a6e53a735bbc9 findings=0`.

## Deployment note

This head deploys on macOS through step 7 (`make update` after U17 lands). A Linux-host `make update` of these settings waits for U31 part 1 (O2-addendum, bus row 1180), which renders the lever allow rules darwin-only; the two residuals of D-024-148 are recorded in the README and the manifest comment.

## Verdict for cebe5fd2

`correct`: merge with `gh pr merge 485 --squash --match-head-commit cebe5fd23835cb840f83fcfb535a6e53a735bbc9`.
