# T28: Remove the ccgate mise package and deploy permgate live

## Objective

permgate (PR #92, merged as `4e761ba`) replaced ccgate; the ccgate package was
retained only for historical metrics, which are now recorded in
`home/dot_agents/permgate-policy.yaml` (`sources` counts and `metrics` block).
Remove the ccgate package and its install lifecycle, then run the managed
lifecycle so permgate is actually deployed (it is NOT live yet: no
`~/.local/bin/common/permgate`, no PermissionRequest hook in live settings,
no decisions.jsonl).

## Scope

1. `home/dot_mise/config.toml`: drop `"aqua:tak848/ccgate" = "0.9.5"`.
2. `scripts/update-agent-assets.sh`: remove `CCGATE_MISE_TOOL`,
   `ensure_ccgate_cli`, and its call site; keep shdoc comments consistent.
3. `docs/reference/scripts/update-agent-assets.md`: drop the ccgate section.
4. `README.md`: replace "The ccgate package remains installed only for
   historical metrics and is not wired to either hook." with a sentence that
   ccgate is fully removed and its metrics are preserved in the permgate
   policy provenance.
5. `tests/install/common/lifecycle.bats`: flip the three assertions that
   currently REQUIRE the ccgate pin/update/version lines to assert ABSENCE
   (`! grep`); keep the existing negative assertions and `.chezmoiremove`
   checks.
6. `home/dot_agents/permgate-policy.yaml`: remove `ccgate` from the
   `known-version-check` allow regex command list (a removed binary must not
   stay auto-allowable). Keep the `metrics` provenance block and the
   `sources` counts unchanged (historical record).
7. KEEP: `MANAGED_PERMISSION_EXECUTABLES` "ccgate" entry in
   `home/dot_claude/modify_private_settings.json`, the ccgate regression
   tests in tests/unit/, `scripts/validate-agent-assets.py` ccgate
   prohibitions, and `.chezmoiremove` entries — these prevent resurrection.
8. Live removal + deploy: run the managed lifecycle (`make update` or the
   equivalent chezmoi apply + update-agent-assets path), then
   `mise uninstall aqua:tak848/ccgate` (or prune) so the binary is gone.

## Live verification (required)

- `command -v ccgate` fails afterwards; `mise ls` shows no ccgate.
- `~/.local/bin/common/permgate` exists and is executable;
  `~/.claude/settings.json` contains the managed PermissionRequest hook;
  `~/.codex/config.toml` contains `[[hooks.PermissionRequest]]` with
  `permgate codex`.
- Fixture smoke on the LIVE install: pipe the three fixture payloads
  (clearly-safe read, clearly-dangerous, ambiguous) into
  `permgate claude` and `permgate codex`; show decisions and the appended
  `~/.local/state/permgate/decisions.jsonl` lines in the validation artifact.
  Do NOT flip llm_enabled (both providers stay shadow).
- Existing deny/ask safety rules in live settings untouched.

## Constraints

- Branch `chore/remove-ccgate` from `origin/main` in a separate worktree,
  English Conventional commit + PR, CI green; no merge before
  AGMSG-ACCEPTANCE next_action=merge.
- Forbidden: enabling llm_enabled, touching model profiles, unrelated
  cleanups, local bats runs.
- `make unit-test`, `make validate-agent-assets`,
  `uv run --with pyyaml scripts/generate-agent-configs.py --check`,
  shellcheck/shfmt all green.

## Expected artifacts

- report: .orchestration/reports/T28-ccgate-removal-permgate-deploy.md
- validation: .orchestration/validation/T28-ccgate-removal-permgate-deploy.txt
- sandbox: .orchestration/sandboxes/T28-ccgate-removal-permgate-deploy.md
- learning: .orchestration/learning/T28-ccgate-removal-permgate-deploy.md
- autoskill: .orchestration/autoskill/runs/T28-ccgate-removal-permgate-deploy.md

## Done signal

AGMSG-RESULT v1 status=ready_for_review with PR number and head SHA.
max_turns=40
