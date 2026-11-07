# U370: the harness page names the third write root, router-gh's header names the right control, and router-settings-apply's manifest and self-file reads fail closed under a committed test

GOAL
Three residual rows from this morning's units, each small and each in a file no open unit touches. (1) dispositions.tsv 2026-11-07T11:49:01Z (U363, docs): `docs/deepseek-harness.md:108-109` says `build_under_srt`'s `allowWrite` is the build directory and `~/.dsh/.pnpm-store` alone; since PR 726 (U363) the third row is pnpm's store operation lock directory `<physical /tmp>/pnpm-store-operation-locks-<uid>` (0700, made before the run, a planted entry refused). (2) The U353d worker's deviation: `scripts/orchestrator/router-gh:12` still says the login lives in the file "because the Keychain is not readable under srt"; the handout (:53) and the README were corrected in U353d (srt's macOS baseline allows `com.apple.securityd.xpc`; the control is router-gh's file-only token source with `GH_TOKEN` set), and the header must say the same. (3) verdicts/U353-747995da.md P2 `tests/unit/test_lever_self_check.py:150`: router-settings-apply's manifest read and self-file read refuse with exit 2 when they fail (the auditor's ad hoc injections confirmed it), but no committed test forces either failure; standing order 21 asks for the committed test. The router-gh `/usr/bin/stat` producer (the other round-4 P2) stays residual: it is called by its absolute name on purpose and the kit adds no test-only hook to a lever.

SCOPE
A new branch from origin/main (ff286680 or later), one pull request. May write: `docs/deepseek-harness.md` (the allowWrite sentence), `scripts/orchestrator/router-gh` and its copy `home/dot_local/bin/common/executable_router-gh` (the header comment at :11-13 only; no code line), `tests/unit/test_lever_self_check.py` and, if the writer's tests live there, `tests/unit/test_router_settings_apply.py` (the two failure-injection tests), the pins through `scripts/generate-agent-configs.py` (never by hand) and whatever it regenerates, and the PR body. Non-goals: no code change in any lever; no change to hcom-seat; no new test hook in a lever.

CONTEXT
`scripts/update-agent-assets.sh` `build_under_srt` as merged (PR 726: the third allowWrite row, its making and refusal); `docs/deepseek-harness.md:99-119`; `router-gh:1-30` (the header) and `docs/engagement-handout.md:53` (the corrected sentence to mirror); `router-settings-apply`'s `lever_self_check` (how it reads the manifest and its own file, what each failure refuses with); `tests/unit/test_lever_self_check.py` (LEVERS, the pinned-copy and altered-byte tests, how a lever is run under a fixture HOME and manifest); `preferences.md` standing orders 5, 21, 46.

DATA SHAPE
One sentence per docs file naming the same three write roots the code renders; one header paragraph that names the control the code implements; two failure-injection tests, each forcing one read to fail (an unreadable manifest; an unreadable self file, or a self file path that is a directory) and asserting exit 2 and a refusal naming the file, nothing else run.

CHANGE
1. Tests first, red on the branch point: (a) in `test_lever_self_check.py`, router-settings-apply under a fixture whose manifest is unreadable (mode 000 under a non-root harness; skip with a reason as root) exits 2 naming the manifest; (b) router-settings-apply whose own file cannot be read for hashing (the self path unreadable or replaced by a directory, whichever the lever's reader lets the test force without a hook) exits 2 naming the file; a docs assertion that `docs/deepseek-harness.md` names `pnpm-store-operation-locks` beside the two other write roots, and that `router-gh` no longer says the Keychain is "not readable under srt". 2. The two sentences; the header paragraph; the copy; the pin. 3. Green: `uv run --offline --with pyyaml python -m unittest tests.unit.test_lever_self_check tests.unit.test_router_settings_apply tests.unit.test_update_agent_assets -v` to `/tmp/u370/full.txt`; lints (shellcheck, shfmt, ruff format --check, prettier, lint-comparisons over the changed paths, render-check, validate-agent-assets); cmp of router-gh and its copy; the pin equal to `shasum -a 256` of the source. 4. One commit; the body with Summary, Contract, Threat table (one row per changed path), Verification (ACCEPTANCE pasted) and `Program-Unit: regime-cutover/U370` once at the end.

ACCEPTANCE
1. Tests (a), (b) and the docs assertion named with red lines at the branch point (`/tmp/u370/red.txt`) and green lines at the head. 2. The three modules OK with counts under `python -m unittest`. 3. Every lint 0 (`run-on-lint-files.sh` for shellcheck, shfmt, ruff and prettier; `make render-check`; `lint-comparisons --changed`); cmp 0; the pin equals `shasum -a 256` of the source. 4. `git diff --stat origin/main HEAD` pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator pushes and opens the pull request, and the one audit, the sweep and CI follow.

CLOSURE
remove

TRUST
TRUST: the unit trusts the merged `build_under_srt` as the source of the three write roots it documents, the handout's corrected sentence (U353d, verdict U353-318f268d P2) as the control router-gh's header mirrors, and the lever's own refusal text as what the two tests assert.

TIMEBOX
35 minutes.

FORBIDDEN
No code line of any lever changed; no test-only hook or environment switch added to a lever; no token in any file; no network; no push; no pin edited by hand; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u370/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U370`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U370-progress.txt`; final report to `../U370-report.txt`; the body at `../U370-pr-body.md`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 5, 21, 24, 27, 29, 34, 44, 46, 49); `verdicts/U353-747995da.md`; `verdicts/U353-318f268d.md`; `dispositions.tsv` rows of 2026-11-07T11:49:01Z and 13:56:57Z; the U363 and U353d briefs.
