# U217 the two remaining prose comment blocks of misc.bats (run_install_chromium, teardown) become shdoc

GOAL
The U210 round-3 verdict (`verdicts/U210-59937063-round3.md`, P3 at weight 10, dispositioned `residual unit=U217`) found the `run_install_chromium` comment block of `tests/install/ubuntu/client/misc.bats` still prose where `AGENTS.md:20-23` (Comment Policy) asks for shdoc-compatible annotations; the `teardown` block above `function teardown()` is prose too (unchanged since U41 and U46, never raised, converted here so the file has one comment form). This unit converts those two blocks to shdoc and changes nothing else.

SCOPE
A new branch `test/misc-bats-shdoc-comments` from `origin/main` a3ca0f2c (your tree is already on it). May write: the comment lines of `tests/install/ubuntu/client/misc.bats` (lines beginning with `#` after optional blanks) above `function teardown()` and `function run_install_chromium()`, and the body file beside your tree, `../U217-pr-body.md`. Nothing else: no line of the file that is not a comment, no other file, no other comment block.

CONTEXT
Measured 2026-11-06 at a3ca0f2c. `misc.bats:21-22` is the teardown block (two prose lines on why only a real install removes packages, U41 and U46); `misc.bats:144` is the one-line run_install_chromium block (sudo as a pass-through, the fixture's fake snap first on PATH, the given environment). The three blocks U210b converted (`:7-13` setup, `:27-31` fake_snap, `:43-49` path_keeping_sudo) are the file's shdoc precedent: `# @description`, continuation lines indented by three spaces after `#`, `# @noargs`, `# @arg $1 string ...`, `# @set`, `# @stderr`, `# @exitcode`. `run_install_chromium` takes `$@` as environment assignments (`run env "$@" ...` or equivalent; read the function) and runs `install_chromium` through `run`; `teardown` takes no argument and calls `remove_real_packages`.

CHANGE
1. Convert the two blocks to shdoc: `# @description` carrying the same why the prose carries now, `# @noargs` for `teardown`, `# @arg $@ string ...` for `run_install_chromium` naming what the arguments are and where they go. No phase narration; every sentence a why the code cannot show.
2. No other line changes: every `-` or `+` line of `git diff origin/main -- tests/install/ubuntu/client/misc.bats` is a comment line.
3. The body `../U217-pr-body.md`: Summary (the two blocks, the U210 round-3 P3 this closes, no command line changes), Contract (guarantee: every comment block above a function in the file is shdoc; leaves out: the test behaviour, which is unchanged; `TRUST:` sentence: the unit trusts the file's commands as U210 left them and the shdoc tag set the file already uses, changes no command line and reads no network), a Threat table with four columns `row | risk | status | evidence` and one row for the file (risk: a comment edit changes a command line; status `closed`; evidence: the ACCEPTANCE 2 command prints nothing, and the CI `test (ubuntu-24.04, client)` leg runs the unchanged cases) plus an `orchestrator effect` row (status `closed`: the U210 residual row at `misc.bats:144` closes with this unit's merge), Verification with the ACCEPTANCE lines, the footer `Program-Unit: regime-cutover/U217`.

ACCEPTANCE
1. `git diff --stat origin/main` names `tests/install/ubuntu/client/misc.bats` alone. 2. `git diff origin/main -- tests/install/ubuntu/client/misc.bats | grep '^[-+][^-+]' | grep -v '^[-+][[:space:]]*#'` prints nothing (paste the command and its exit status 1). 3. `grep -c '^# @description' tests/install/ubuntu/client/misc.bats` prints 5 (paste the number), and `grep -n '^# @' tests/install/ubuntu/client/misc.bats` is pasted whole. 4. `grep -c '^#' tests/install/ubuntu/client/misc.bats` printed before and after (paste both). 5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.

VERIFY
The commands of ACCEPTANCE in the worker's tree with their result lines pasted into the body's Verification section; CI's `test (ubuntu-24.04, client)` leg on the head is the proof that the file still parses and passes (the coordinator reads it).

CLOSURE
remove

TRUST
TRUST: the unit trusts the file's commands as U210 left them at a3ca0f2c and the shdoc tag set the file already uses as the comment form; it changes no command line, no assertion and no installer, and reads no network.

TIMEBOX
15 minutes.

FORBIDDEN
No change to a non-comment line of `tests/install/ubuntu/client/misc.bats`; no change to the three blocks U210b converted; no other file; no local bats run; no network read; no push; no `gh` call; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/U217`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print `7a5f435887f613fe2be5b9f6f4a01d2b9a39a48e  -`.
- Progress line beside your tree (`../U217-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole PR body beside your tree (`../U217-pr-body.md`) per CHANGE 3.
- Comments explain a non-obvious why only, no phase narration.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 35); `verdicts/U210-59937063-round3.md`; `briefs/U210b-fixture-helper-comments-in-shdoc-and-the-threat-table-statuses-round2.md`; `AGENTS.md:20-23`.
