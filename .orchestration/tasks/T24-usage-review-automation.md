# T24: Mechanize the usage measurement/review loop (snapshot, report, due-date, CCR gate)

## Objective

The model-profile plan defines measurement-based review (+7d/+14d) but it is
entirely manual today. Automate the MEASUREMENT side end-to-end — capture,
comparison, threshold verdicts, and review-due reminders — while keeping the
actual `model_profiles` change human-gated (PR only). Also mechanize the CCR
adoption-gate check inside `make upgrade`.

## Deliverables

### 1. `scripts/usage-snapshot.sh` (bash, shdoc comments)

- Writes `ccusage weekly --json` and `ccusage daily --json` into
  `.agents/worklog/claude/usage/<YYYYMMDD>.json` as one JSON object
  `{"captured_at": ..., "weekly": ..., "daily": ...}` (same shape as the
  existing `20260723-baseline.json`).
- Idempotent per day: if today's file exists, exit 0 without rewriting.
- Fails soft (exit 0 with a WARN line) when `ccusage` is unavailable, so a
  scheduled run never spams errors on a machine without it.

### 2. `scripts/usage-report.py` (python, uv-run compatible, unit-tested)

- Inputs: the usage directory; baseline = oldest snapshot (or an explicit
  `--baseline` path, default `.agents/worklog/claude/usage/20260723-baseline.json`),
  latest = newest snapshot.
- Computes per model family: input/output/cache-read totals, output-token
  share, cache-read ratio, and the deltas vs baseline. Parse defensively —
  ccusage JSON shape may vary; unknown fields must not crash the report
  (fixture-driven tests define the supported shape).
- Emits the pre-defined verdict lines (thresholds from the accepted plan,
  encode as constants at the top of the script):
  - `REVIEW DUE (+7d)` / `REVIEW DUE (+14d)` when the baseline is at least
    7/14 days older than today and no `review-<date>.md` note exists in the
    usage directory for that window.
  - `interactive-downgrade-candidate: yes|no` — yes when the Claude Fable
    family holds the largest non-cache (input+output) share among Claude
    models in the latest snapshot. Print the numbers used.
  - Always prints: "quality side (rework/review misses) is manual — decide
    via PR, never automatically".
- Exit code 0 always (it is a report, not a gate).

### 3. Makefile targets

- `usage-snapshot`: runs the shell script.
- `usage-report`: `uv run python scripts/usage-report.py`.

### 4. Weekly automation (macOS launchd)

- A chezmoi-managed LaunchAgent plist (label
  `com.mryfmo.dotfiles.usage-snapshot`) that runs
  `make -C /Users/mryfmo/Workspace/dotfiles usage-snapshot usage-report`
  weekly (Monday 09:00), logging stdout/err to
  `~/.config/dotfiles/usage-review.log`.
- Follow the repo's existing pattern for installing LaunchAgents if one
  exists (search `install/macos` and chezmoi scripts first); if there is no
  precedent, add the plist under `home/Library/LaunchAgents/` (chezmoi target
  `~/Library/LaunchAgents/...`) and document the one-time
  `launchctl bootstrap gui/$(id -u) <plist>` step in README's lifecycle
  section instead of inventing a new run-once mechanism.
- Do NOT run launchctl yourself; documenting the load step is sufficient.
  The orchestrator will load it at final integration.

### 5. CCR gate notice in `make upgrade`

- In `scripts/upgrade-tools.sh`, add a non-blocking notice step (WARN-level,
  never a required failure) that, when `gh` is available, prints:
  - `CCR gate G1 (#1115): <state>` from
    `gh api repos/musistudio/claude-code-router/issues/1115 --jq .state`
  - `CCR latest release: <tag>` from
    `gh api repos/musistudio/claude-code-router/releases/latest --jq .tag_name`
  - a reminder line that G2/G3 need manual one-source verification before any
    canary.
- Network failure or missing gh must not fail the upgrade (optional warning
  at most).

## Tests

- New `tests/unit/test_usage_review.py`: fixture snapshots (small synthetic
  JSON) covering: idempotent snapshot skip, report share/delta math, REVIEW
  DUE emission at +7d/+14d, downgrade-candidate yes/no, malformed snapshot
  tolerated with a WARN.
- Extend `tests/unit/test_runtime_health.py` upgrade fixtures only if the
  upgrade-tools change breaks existing assertions; the CCR notice must be
  skipped cleanly when the stubbed `gh` is absent.
- `make unit-test`, `make validate-agent-assets`,
  `uv run --with pyyaml scripts/generate-agent-configs.py --check`,
  `shellcheck`/`shfmt --indent 4 --space-redirects` on the new shell script —
  all green. No local bats.

## Boundaries

- The report must NOT edit `home/dot_agents/agent-config.yaml` or any profile
  value. Automation ends at verdict lines; changes remain human-gated PRs.
- No new dependencies (stdlib + existing tools only). No secrets in logs.
- Branch `feat/usage-review-automation` from origin/main in a separate
  worktree; single or two commits, English Conventional Commit; PR English;
  CI green; do NOT merge before AGMSG-ACCEPTANCE next_action=merge; after
  acceptance merge + ff-only main sync as in T22/T23.

## Expected artifacts

- report: .orchestration/reports/T24-usage-review-automation.md
- validation: .orchestration/validation/T24-usage-review-automation.txt
- sandbox: .orchestration/sandboxes/T24-usage-review-automation.md
- learning: .orchestration/learning/T24-usage-review-automation.md
- autoskill: .orchestration/autoskill/runs/T24-usage-review-automation.md

## Done signal

AGMSG-RESULT v1 status=ready_for_review. max_turns=40
