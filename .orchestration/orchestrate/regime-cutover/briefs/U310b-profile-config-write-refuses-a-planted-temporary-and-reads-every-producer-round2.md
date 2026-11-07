# U310b round 2 of U310: the profile config write refuses a planted temporary file and reads every producer's status

GOAL
The round-1 audit of PR 708 (head e92b4970, `verdicts/U310-e92b4970.md`) returned one P1 and five lower findings on the profile config placement U310 added to `hcom-seat`:
- P1 `scripts/orchestrator/hcom-seat:2104`: `profile_config_write` writes through `config.yml.tmp.<launcher pid>` with a shell redirection and then `mv`s it; the profile directory is dsh-writable, so a planted symlink at that predictable name is followed by the redirection (unsandboxed) and then installed as the config. The auditor's scratch launch overwrote `~/.omp/agent/config.yml` and exited 0.
- P2 `:2069`: the existence test reads a mode-000 `agent/` as absent (dry run exit 0, decision `absent`), against the linked-config refusal and standing order 21.
- P2 `:2075`: the `cmp` decision checks only `cmp`'s status; the process-substitution producer's status is discarded (an injected `printf` exit 74 with no output made an empty target compare equal and chose `keep`).
- P2 `tests/unit/test_hcom_seat_dsh.py:1070`: no failure injection of an overlay read failure or a `cmp` error.
- P2 the body's threat table omits `scripts/generated-agent-outputs.json` and closes the docs and orchestrator-effect rows without a failing selector.
- P3 `:2115`: `profile_config_check` runs after the private tool-directory mkdir, so a bad overlay on a fresh HOME still creates directories while the Contract promises refusal before any directory is made.
Every finding is fixed in this round (order 35: the P2s are cheap and the P3 is an ordering move).

SCOPE
The same branch `feat/dsh-role-profile-route` and PR 708; the tree is `/tmp/dotfiles-wt/U310b` at e92b4970 (created by the coordinator). May write: `scripts/orchestrator/hcom-seat` and its generated copy `home/dot_local/bin/common/executable_hcom-seat` (byte-identical, regenerated), the lever pins by regeneration (`home/dot_agents/agent-config.yaml`, `scripts/generated-agent-outputs.json`), `tests/unit/test_hcom_seat_dsh.py`, and the body `../U310b-pr-body.md` (the full body for PR 708, the round-1 body as the base at `/tmp/dotfiles-wt/U310-pr-body.final.md`). Not: the generator, the manifest beyond the pin rows, the omp roles' rendered settings and launch lines (byte-identical to main, the existing test holds them), the docs.

CONTEXT
Read `profile_config_check` and `profile_config_write` whole and the round-1 tests. The dsh role's write-root judge already refuses a linked `agent/` or `config.yml`; the hole is the temporary file: its name is predictable, its directory is writable by the role's own process, and the redirection runs in the launcher outside srt. The kit's precedent for a write into a role-writable directory is the sandbox settings writer (`settings_write`, the per-launch slot) and U272's "physical path, identity" rule: write through a descriptor opened with `O_EXCL` on a name nobody can predict, under a directory the launcher owns, then rename. In bash that is `mktemp` in the target directory (random suffix, 0600, `O_EXCL`), a `test -L` and `test -f` on the returned path before and after the write (a link is refused), and `mv -f` only when the inode read back equals the one `mktemp` made. Every existence read distinguishes a failed read from an absence (standing order 21): `[ -e ]` on a path under an unsearchable directory is false for both, so test the parent's searchability first (`[ -d ] && [ -x ]`) and refuse when the parent exists and is not searchable. The `cmp` decision reads both producers' statuses: write the overlay's canonical rendering to a launcher-owned temporary file with its own status check, then `cmp` two regular files, no process substitution. The P3: move `profile_config_check` before `tools_dir` creation (or whatever mkdir precedes it at `:2115`); the dry-run test that today permits those mkdirs asserts no mkdir instead.

DATA SHAPE
One write path for the placed config: `mktemp "${agent_dir}/.config.yml.XXXXXX"` (0600, O_EXCL, launcher-owned name), refuse if the path is a link or not a regular file, write, re-check link and regular file and inode, `mv -f` onto `config.yml`. One read discipline for every existence decision in the placement: searchable parent first, then the file test, a failed read refused by name. One comparison: two regular files through `cmp`, each producer's status read.

CHANGE
1. `profile_config_write`: the `mktemp` temporary in the profile's `agent/` with the checks above; a planted symlink or regular file at any predictable name has no effect because no predictable name is used; the function refuses (exit 2, naming the path) when `mktemp` fails, when the temporary is not a regular non-link file before or after the write, or when `mv` fails; the temporary is removed on every refusal.
2. `profile_config_check`: the parent-searchability test before every `-e`/`-L`/`-f`; an unsearchable `~/.omp/profiles/dsh` or `agent/` refuses naming the directory; the canonical overlay rendering goes to a launcher-owned temporary file with its status read; `cmp` compares two regular files and both producers' statuses decide.
3. Ordering: `profile_config_check` runs before any directory creation of the launch (the tool directory included); the dry-run test asserts no mkdir on a bad overlay.
4. Tests (`tests/unit/test_hcom_seat_dsh.py`): a planted symlink at the old predictable name `config.yml.tmp.$$` and at any `.config.yml.*` name is left alone and the real config lands (the symlink target unchanged, asserted by content and inode); a mode-000 `agent/` refuses naming it; an unreadable overlay refuses; an injected `cmp` failure (a `cmp` shim on PATH returning 2 without output) refuses rather than choosing keep; a `mktemp` failure refuses; the fresh-HOME bad-overlay dry run creates no directory. Each test is a failure injection the user would hit (standing order 21).
5. The body: the round-1 body plus a Round 2 paragraph quoting the six findings and their fixes, the threat table gaining a `scripts/generated-agent-outputs.json` row and, for every `closed` row, the test selector that fails without the fix (the docs row becomes `residual` with the test that pins the sentence, or `out-of-scope` naming the docs, since a doc line has no failing test), and the Verification section with ACCEPTANCE pasted.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_generate_agent_configs tests.unit.test_scratch_git` OK (paste the count; the new tests named).
2. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0; `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
3. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. The auditor's reproduction re-run against the new head on a scratch host under `/tmp/u310b/`: a symlink planted at `~/.omp/profiles/dsh/agent/config.yml.tmp.<pid>` pointing at a scratch default-profile config; after the launch the target file is byte-identical to before and `agent/config.yml` is a regular file equal to the overlay (pasted); the mode-000 `agent/` dry run exits 2 naming the directory (pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section; the coordinator re-runs item 5 on the pushed head.

CLOSURE
remove

TRUST
TRUST: the unit trusts the manifest's extension allow-list and the seat overlays' shape, and the launcher-owned temporary name `mktemp` returns inside the role's profile; it writes only inside the role's own profile at launch, follows no link, reads no credential and changes no omp role's rendered settings.

TIMEBOX
60 minutes.

FORBIDDEN
No write under the real `~/.omp`, `~/.dsh`, `~/.agents`, `~/.local/state/omp-seats`, `~/Workspace` (scratch HOME under `/tmp/u310b/` only); no change to the generator or the docs; no change to the omp roles' settings or launch flags; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u310b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U310b` and the coordinator fetches it by path.
- Progress line at `../U310b-progress.txt` after every step; first edit within ten minutes. Final report to `../U310b-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only; shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes: the predictable name goes, no check bolted onto it; Boundary Discipline: one write path, one read discipline).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against e92b4970), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 35, 36, 41, 42, 44, 46); `verdicts/U310-e92b4970.md`; `briefs/U310-dsh-role-provisions-its-omp-profile-with-the-bridge-route.md`; `briefs/U272e-dsh-home-refusal-derived-from-the-rendered-deny-table-round4.md` (physical path, identity).
