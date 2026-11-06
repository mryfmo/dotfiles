# U297c round 2 of U297: the installer finds the ci-runner helper without an external command, and reads the source's status

GOAL
The round-1 audit of PR 705 (U297, head cf951b62; `verdicts/U297-cf951b62.md`) found one P1 and one P2 at `install/ubuntu/client/misc.sh:17`: the new `source` of `scripts/lib/ci-runner.sh` computes the helper's directory with `$(dirname ...)`, and the existing bats case for an unavailable `snap` runs the installer with an empty PATH on purpose, so the head exits 1 while sourcing (every Ubuntu client test leg would fail); and the `source` line masks `dirname`'s exit status (a `dirname` that prints the right path and exits 73 still yields success, against standing order 21). This round resolves the helper's path by parameter expansion (`${BASH_SOURCE[0]%/*}`, with the one-component case handled) so no external command runs before the helper is sourced, reads the source's status and fails closed with the helper's path named, and adds the failure-injection test the rule requires (an unreadable or absent helper refuses; the empty-PATH case passes as before).

SCOPE
The existing branch `ci/public-bootstrap-chromium-snap` at cf951b6224803b062091e61ea121c8a02bc0c6ed in `/tmp/dotfiles-wt/U297` (the PR is 705). May write: `install/ubuntu/client/misc.sh`, the chezmoi template that includes it (`home/.chezmoiscripts/ubuntu/*50-client-install-misc.sh.tmpl`, only if the include shape must change), `tests/install/ubuntu/client/misc.bats`, `tests/unit/test_ci_runner.py`, and the body `../U297-pr-body.md` (a Round 2 section). Not: `scripts/lib/ci-runner.sh` itself, the other installers.

CONTEXT
Read the verdict's Findings and Reproduced sections, the installer's first 30 lines, the bats case that empties PATH (`grep -n 'PATH=' tests/install/ubuntu/client/misc.bats`), and how the chezmoi template includes the two files (the rendered script is one file: the helper's functions may already be inline there, in which case the installer's `source` must be conditional on running unrendered, or the helper's definition must be reachable in both forms; measure which by rendering as the round-1 agent did, `/tmp/u297/` holds its outputs).

DATA SHAPE
One guarded source at the top of the installer: the helper path from `${BASH_SOURCE[0]}` by parameter expansion, `[ -r "$helper" ] || { echo "...: ci-runner helper unreadable: $helper" >&2; exit 2; }`, then `source "$helper" || exit 2`; if the rendered template already inlines the helper, the installer defines a fallback only when `is_ci_runner` is not yet a function (`declare -F is_ci_runner`), so both forms work. Tests: the empty-PATH bats case passes; a unit (or bats) case with the helper made unreadable refuses with the path; the runner-skip and host cases from round 1 stay.

CHANGE
1. The guarded source per DATA SHAPE.
2. Tests per DATA SHAPE.
3. The body's Round 2 section quoting the two findings, the change, the tests; ACCEPTANCE pasted.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_ci_runner tests.unit.test_network_bounds tests.unit.test_scratch_git` OK (paste the count; the new test named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
3. A plain-bash reproduction of the empty-PATH case (as the auditor did: `PATH= bash install/ubuntu/client/misc.sh` with a fake snap absent) exits as the base does, pasted; `grep -c 'dirname' install/ubuntu/client/misc.sh` prints 0 for the new line.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. CI's Ubuntu test legs and public-bootstrap legs on the PR are the coordinator's evidence.

CLOSURE
remove

TRUST
TRUST: the unit trusts bash parameter expansion as the one path resolution before the helper is sourced; it runs no snap, reads no credential and opens no network.

TIMEBOX
25 minutes.

FORBIDDEN
No change to `scripts/lib/ci-runner.sh`; no external command before the helper is sourced; no change to the operator's host behaviour; no local bats beyond reading the file (policy keeps bats off the worker host; the unit test is the local gate); no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u297c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U297` and the coordinator fetches it by path.
- Progress line at `../U297c-progress.txt`; final report to `../U297c-report.txt` before you end; deliverables beside the worktree under `/tmp/dotfiles-wt/`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Shell comments are English shdoc. Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes; Laziness Protocol).

REPORT
Status, head sha (40 hex), files changed, the ACCEPTANCE result lines, deviations. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); `verdicts/U297-cf951b62.md`; `briefs/U297-*.md`.
