# U301 the four macOS installers find the ci-runner helper by parameter expansion and read the source's status

GOAL
On `origin/main` 2b2415f6 the four macOS installers source `scripts/lib/ci-runner.sh` through a command substitution, `source "$(dirname "${BASH_SOURCE[0]}")/../../../scripts/lib/ci-runner.sh"` (`install/macos/common/brew.sh:19-23`, `dependencies.sh:16-20`, `docker.sh:14-18`, `misc.sh:14-18`): the producer's status is lost in the source line (standing order 21), the defect U297c removed from the Ubuntu client installer (`install/ubuntu/client/misc.sh:14-30`, PR 705 head 03cde233: the helper's directory is a parameter expansion, an unreadable helper refuses naming its path, `source ... || exit 2`). The round-2 P3 of PR 705 (units.tsv row U301) stays open in the Ubuntu form too: a readable helper whose source returns non-zero exits 2 with an empty stderr while the Contract promises the path is named. Five guards, one shape.

SCOPE
Branch `fix/macos-installers-ci-runner-helper` from `origin/main`; the tree is `/tmp/dotfiles-wt/U301` (created by the coordinator). May write: the four macOS installers above, `install/ubuntu/client/misc.sh` (the failed-source branch's stderr line only), the unit-test module that covers the Ubuntu guard (find it with `rg -n 'ci-runner helper unreadable' tests`), a new test for the five-guard identity in that module, and the body `../U301-pr-body.md`. Not: `scripts/lib/ci-runner.sh`, the chezmoi templates under `home/.chezmoiscripts/`, any other installer.

CONTEXT
Read the Ubuntu guard whole (`install/ubuntu/client/misc.sh:14-30`) and its tests; the chezmoi templates include `scripts/lib/ci-runner.sh` before each installer, so the guard runs only on a direct run (a test, an operator's shell). The snap-unavailable test of the Ubuntu installer runs the file with an empty PATH, which is why the directory is a parameter expansion and not `dirname`. The five installers are included standalone, so the guard cannot move into a shared file without the same sourcing problem: it stays inline, byte-identical across the five files except each file's own path in its messages, and a test pins that identity so the next installer copies the right shape.

DATA SHAPE
One guard block, identical in the five installers except the installer's own path in its two messages (helper unreadable; helper failed to source); a test that reads the five blocks and asserts they are equal after that substitution.

CHANGE
1. The four macOS installers take the Ubuntu guard verbatim, with their own `install/macos/common/<name>.sh` in the message and the same relative helper path.
2. In all five, the failed-source branch prints `<installer>: ci-runner helper failed to source: <path>` to stderr before `exit 2` (the P3 of PR 705).
3. Tests, in the module that covers the Ubuntu guard: for each of the five files, an unreadable helper exits 2 with the unreadable message naming the path; a helper that returns non-zero on source exits 2 with the failed-to-source message naming the path; a direct run with an empty PATH still defines `is_ci_runner`. One test asserts the five guard blocks are identical modulo the file name.
4. The body: Summary, Contract (the guard shape, what it refuses, Left out: the chezmoi-rendered path never runs the guard), Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest <the module found in SCOPE> tests.unit.test_scratch_git -v` OK (counts pasted; the new tests named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
4. `bash -n` of the five installers exit 0, and one direct run of each macOS installer with an unreadable helper path pasted (exit 2, the message).

VERIFY
ACCEPTANCE pasted into the body's Verification section.

CLOSURE
remove

TRUST
TRUST: the unit trusts the repository tree's helper at the path relative to the installer and the shell's own function table; it reads no other state, no network, no credential, and runs no package manager.

TIMEBOX
40 minutes.

FORBIDDEN
No change to `scripts/lib/ci-runner.sh` or to any chezmoi template; no `brew` call; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u301/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U301` and the coordinator fetches it by path.
- Progress line at `../U301-progress.txt` after every step; first edit within ten minutes. Final report to `../U301-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only; shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Laziness Protocol: one guard shape, copied, pinned by a test; Fix Root Causes: the command substitution goes, no retry).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against the merge base, no fetch), the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `units.tsv` rows U297c and U301; `install/ubuntu/client/misc.sh:14-30`.
