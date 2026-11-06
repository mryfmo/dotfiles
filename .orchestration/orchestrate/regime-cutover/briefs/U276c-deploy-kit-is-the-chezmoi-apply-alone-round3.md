# U276c round 3 of U276: `make deploy-kit` is the chezmoi apply of the kit roots and nothing else

GOAL
Two audits of PR 698 (`verdicts/U276-49108595.md`, `verdicts/U276b-837d5996.md`) found the same class twice: the asset step borrowed `scripts/update-agent-assets.sh`, first whole (it rewrites the operator's Codex config), then function by function (the functions fail open outside the updater's `main`: `update_compactiondb` returns 0 after `rsync` or `manifest_record` fails because `PIN_FAILURES` is checked only at `main`'s end; `manifest_prune_retired` suppresses failures; a linked `~/.agents/compactiondb` destination writes outside the roots; `update_deepseek_harness` may auto-install mise tools). The mechanism-change row of 2026-11-06T12:5xZ withdraws the premise. This round removes the asset step: `deploy-kit` applies the kit roots' chezmoi targets and does nothing else, and its contract says so. Pinned asset refreshes are the updater's job under its own contract (U283, a separate unit). The round also closes the two findings that are deploy-kit's own: pending names must be members of the managed kit set (P2 at `:194`), and the physical-path reads (`pwd -P` of HOME and each root) need failure injection (P3).

SCOPE
The existing branch `feat/make-deploy-kit` at 837d599641eed7066a0eea3d46d994830a463311 in `/tmp/dotfiles-wt/U276` (the PR is 698). May write: `scripts/deploy-kit.sh`, `tests/unit/test_deploy_kit.py`, `scripts/update-agent-assets.sh` only to revert this branch's change to it (`git diff origin/main -- scripts/update-agent-assets.sh` must be empty after), `README.md` (the deploy-kit paragraph), and the body `../U276-pr-body.md` (a Round 3 section; the Contract, Threat table and Summary rewritten for the narrower lever). Not: the `update` target, any updater function, any `home/` file.

DATA SHAPE
One table, the kit root table (three physical roots). The script: physical roots (refuse a link or a missing root, with failure injection on every `pwd -P`), `chezmoi managed` and `chezmoi status` restricted to the roots with `--refresh-externals=never`, a pending set that is the intersection of the status rows and the managed set (a name outside the managed set refuses, naming it), two-sided drift refused, `chezmoi apply --refresh-externals=never <names>`, `chezmoi verify` over the applied names, the applied list printed, exit 0; `--dry-run` prints the pending list and refusals and applies nothing. No call of `update-agent-assets.sh`, no function table.

CHANGE
1. Remove the asset step, the function table and the updater's whitelist change; the README paragraph says what the lever does and names the updater as the separate step for pinned assets.
2. Membership: every pending name is checked against the managed kit set before apply; a name outside it refuses.
3. Failure injection for every `pwd -P` read (HOME and each root) and for a root that is a link or missing; the existing tests stay minus those of the removed step.
4. Measurement on this host, read-only: `scripts/deploy-kit.sh --dry-run` pasted.
5. The body: Summary (three rounds, the mechanism-change row, why the asset step is gone), Contract (the guarantees of the narrower lever), Threat table with one row per changed path and the test that pins each control, Verification (ACCEPTANCE pasted), Round 3 section quoting the seven round-2 findings with each one's disposition here (fixed here, or moved to U283 with the finding quoted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_deploy_kit tests.unit.test_scratch_git` OK (paste the count; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
3. `git diff origin/main --stat -- scripts/update-agent-assets.sh` prints nothing; `grep -c 'update-agent-assets' scripts/deploy-kit.sh` prints 0.
4. The CHANGE 4 dry run pasted.
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator runs `make deploy-kit` after the merge and records the applied list and the Codex config's unchanged digest in `decisions.tsv`.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts chezmoi's target-restricted status and verify as the drift oracle and the root table as the boundary; it applies nothing on this host (dry run only), runs no updater function, reads no credential and opens no network.

TIMEBOX
40 minutes.

FORBIDDEN
No `chezmoi apply` without `--dry-run` on this host; no run of any `update_*` function; no edit under `home/`; no change to the `update` target; no write under `~/.local`, `~/.agents`, `~/.dsh`, `~/.codex`, `~/.claude`; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command you run yourself (standing order 46: output to a file under `/tmp/u276c/`, then read it); inside the script a pipe only with `set -o pipefail` and the status read.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U276` and the coordinator fetches it by path.
- Progress line at `../U276c-progress.txt` every ten minutes at most; first edit within ten minutes. Final report to `../U276c-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Subtract Before You Add; Laziness Protocol; Boundary Discipline).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the dry run's pending count, the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 30, 33, 34, 36, 44, 46, 48); `gates.md` G-26; the two verdicts of PR 698; the mechanism-change row of 2026-11-06T12:5xZ; `AGENTS.md` (Test Policy).
