# U297 the public-bootstrap check does not fail on the runner's chromium snap

GOAL
Three times today (PR 701 run 42234090626, PR 703 runs 42236571195 and its re-run) the required check `public-bootstrap (ubuntu-24.04, client)` failed in `.chezmoiscripts/ubuntu/50-client-install-misc.sh` with `install_chromium: snap install chromium timed out after 600 s (SNAP_INSTALL_TIMEOUT); snapd may still finish it (snap changes)`, exit 124, `chezmoi apply failed`. The chromium snap is a desktop convenience of the client profile; its install on a GitHub runner waits on an automatic snapd restart the runner image performs, and the kit's pull requests do not change it. A required check that a third-party snap decides blocks every merge of the program (standing order 47's cycle depends on merges landing). This unit makes the bootstrap check independent of that snap on CI: either the client misc script skips the chromium snap when `CI=true` (recording the skip as a line the check prints), or the snap install is retried with a bounded wait and a non-fatal outcome on the runner only, with the operator's real host behaviour unchanged.

SCOPE
A new branch `ci/public-bootstrap-chromium-snap` from `origin/main` (your tree is `/tmp/dotfiles-wt/U297`). May write: `home/.chezmoiscripts/ubuntu/50-client-install-misc.sh` (or the misc installer it sources under `home/` or `scripts/`), its tests (`tests/unit/test_*misc*.py` or where the installer is tested; find by grep for `install_chromium`), `.github/workflows/public-bootstrap.yaml` only if the skip is a workflow variable, `docs/` where the client misc installs are listed, and the body `../U297-pr-body.md`. Not: the other snaps, the operator's host behaviour (a real `make update` on the Ubuntu host must still install chromium).

CONTEXT
Read the script's `install_chromium` function and `SNAP_INSTALL_TIMEOUT`, the public-bootstrap workflow (`.github/workflows/public-bootstrap.yaml`: which profiles it runs, what environment it sets, `CI=true` is GitHub's default), the earlier snapd-related decisions in the store (`grep -n snapd decisions.tsv`, U63 and G11 rows), and the three job logs' tail as quoted above. Prefer the skip on CI (Laziness Protocol): the check proves the bootstrap path, not the snap store's availability; a skipped snap on CI is a printed line, never a silent pass. The operator's host: unchanged; if the kit has a doctor row for chromium, it still reports an absent chromium on a real host.

DATA SHAPE
One condition at the chromium step: `CI=true` (GitHub's variable) skips the snap with a printed `install_chromium: skipped on CI (snap store)` line; every other environment runs it as today. A test with the installer's fake `snap` recorder: under `CI=true` no `snap install chromium` call and the skip line printed; without `CI` the call happens; the timeout path unchanged.

CHANGE
1. The condition and the line; the test.
2. The body: Summary (the three failures with run ids), Contract (the bootstrap check no longer depends on the snap store; the operator's host unchanged), Threat table, Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest <the installer's test module>` OK (paste the count; the new test named).
2. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
3. `bash -n` on the changed script exit 0; `grep -n 'skipped on CI' <script>` prints the line.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section. CI's public-bootstrap legs on the PR are the coordinator's evidence.

CLOSURE
remove

TRUST
TRUST: the unit trusts GitHub's `CI` variable as the runner marker and changes one install step's behaviour there only; it runs no snap, reads no credential and opens no network.

TIMEBOX
30 minutes.

FORBIDDEN
No change to the operator's host behaviour (no skip without `CI`); no other install step touched; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u297/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U297` and the coordinator fetches it by path.
- Progress line at `../U297-progress.txt`; final report to `../U297-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Shell comments are English shdoc. Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Laziness Protocol).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the condition in one line, the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); the three job logs (runs 42234090626, 42236571195); `gates.md` G11; `AGENTS.md` (Test Policy).
