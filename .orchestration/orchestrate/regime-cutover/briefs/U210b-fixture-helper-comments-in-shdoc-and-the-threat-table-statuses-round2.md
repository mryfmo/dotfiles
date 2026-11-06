# U210b the misc.bats fixture helpers carry shdoc comments and the PR body's Threat table uses the three allowed statuses (round 2 of U210)

GOAL
Round 1 of U210 (PR 667, head 2567ba11, `verdicts/U210-2567ba11.md`) was `correct` with no blocking finding, and two items still stand between that head and its merge. (a) Codex thread 4483881479 (P1, frequency 10, severity 1, weight 10, so not `filed`): the comment blocks of the new fixture helpers `fake_snap` and `path_keeping_sudo` in `tests/install/ubuntu/client/misc.bats` are prose where `AGENTS.md:20-23` (Comment Policy) asks for shdoc-compatible annotations on shell comments that a change adds or updates; the `setup` block this head added is prose too. (b) The round-1 verdict's P2 at weight 20 (`misc.bats:42`, body-only): the PR body's Threat table rows use the statuses `mitigated`, `contained`, `accepted` and `removed`, where `AGENTS.md:70` allows `closed` (evidence names the test selector that fails without the fix), `residual` (names the control that mitigates) or `out-of-scope` (names the unit that owns the risk). This round converts the three comment blocks to shdoc and rewrites the table; no command line of the file changes.

SCOPE
The PR branch `test/misc-bats-fake-snap`, continued from 2567ba11 (your tree's `origin/main` is that head). May write: the comment lines of `tests/install/ubuntu/client/misc.bats` (lines beginning with `#` after optional blanks) and the body file beside your tree, `../U210b-pr-body.md`. Nothing else: no line of the file that is not a comment, no other file.

CONTEXT
Measured 2026-11-05 at 2567ba11. The three prose blocks: `misc.bats:7-10` above `function setup()`, `:24-27` above `function fake_snap()`, `:39-41` above `function path_keeping_sudo()`. The `teardown` block at `:18-19` is unchanged since main (`origin/main:tests/install/ubuntu/client/misc.bats:11-12`) and is not named by the thread; leave it as it is. The repository's bats files already carry shdoc in four places, for example `tests/install/ubuntu/client/ghostty.bats:82-84` (`# @description ...`, `# @arg $1 string ...`, `# @arg $@ string ...`). shdoc tags in use in this repository: `@description`, `@arg`, `@set`, `@stdout`, `@exitcode`, `@example`. `fake_snap` takes `$1`, the command the generated snap runs after logging, whose status is the fake's; it writes `${BATS_TEST_TMPDIR}/bin/snap`. `path_keeping_sudo` takes no argument, writes `${BATS_TEST_TMPDIR}/bin/sudo`, and returns 1 with a message on stderr when no `sudo` is on PATH. `setup` sources the script, writes both fakes and puts their bin first on PATH. The current body is `../U210-pr-body.md` (read-only); its Threat table has four rows (three for the file, one `orchestrator effect`). The tests that fail when the fixture is lost are `[ubuntu-client] misc` (asserts one recorded `snap install chromium`, and `dpkg -s` for every package after the real apt install through the PATH-keeping sudo) and `[ubuntu-client] main reaches the fixture's snap and returns its status, never the host's` (status 99, three recorded calls). The real chromium install is exercised by the `public-bootstrap (ubuntu-24.04, client)` and `(ubuntu-26.04, client)` legs, a control outside this file.

CHANGE
1. Convert the `setup`, `fake_snap` and `path_keeping_sudo` comment blocks to shdoc: `# @description` lines carrying the same why the prose carries now (the store stall of 2026-11-05, why the fake is a program and not a function, why the log path is written into the script, why sudo needs the wrapper), `# @arg $1 string ...` for `fake_snap`, `# @noargs` or nothing for the two without arguments, `# @stdout`/`# @stderr` only where the function writes there, `# @exitcode 1 ...` for `path_keeping_sudo`'s refusal, and `# @set PATH ...` for `setup`. Keep every sentence a why the code cannot show; no phase narration.
2. No other line changes: every `-` or `+` line of `git diff origin/main -- tests/install/ubuntu/client/misc.bats` is a comment line.
3. The body `../U210b-pr-body.md`, from `../U210-pr-body.md`: the Threat table keeps its four rows and each row's status becomes one of `closed`, `residual`, `out-of-scope` with the evidence the rule asks for (a `closed` row names the test selector that fails without the fix, a `residual` row names the control that mitigates the risk, an `out-of-scope` row names the owning unit); the Summary gains one sentence on the shdoc comments; the Verification section gains `Round 2 (U210b)` with the ACCEPTANCE lines; `Program-Unit: regime-cutover/U210` stays the last line. The words `mitigated`, `contained`, `accepted` and `removed` appear in no table row.

ACCEPTANCE
1. `git diff --stat origin/main` names `tests/install/ubuntu/client/misc.bats` alone. 2. `git diff origin/main -- tests/install/ubuntu/client/misc.bats | grep '^[-+][^-+]' | grep -v '^[-+][[:space:]]*#'` prints nothing (paste the command and its exit status 1). 3. `grep -c '^# @' tests/install/ubuntu/client/misc.bats` prints 8 or more (paste the number), and `grep -n '^# @' tests/install/ubuntu/client/misc.bats` is pasted whole. 4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0. 5. `grep -c '^| .* | \(closed\|residual\|out-of-scope\) | ' ../U210b-pr-body.md` prints 4 and `grep -c '^| .* | \(mitigated\|contained\|accepted\|removed\) | ' ../U210b-pr-body.md` prints 0 (paste both).

VERIFY
The commands of ACCEPTANCE in the worker's tree with their result lines pasted into the body's Verification section; CI's `test (ubuntu-24.04, client)` leg on the new head is the proof that the file still parses and passes (the coordinator reads it).

CLOSURE
remove

TRUST
TRUST: the unit trusts the round-1 head 2567ba11 as the code under its comments, the shdoc tag set the repository already uses as the comment form, and the Audit section's three statuses as the table's vocabulary; it changes no command line, no test assertion and no installer, and reads no network.

TIMEBOX
20 minutes.

FORBIDDEN
No change to a non-comment line of `tests/install/ubuntu/client/misc.bats`; no other file; no local bats run; no network read; no push; no `gh` call; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/U210b`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print `7a5f435887f613fe2be5b9f6f4a01d2b9a39a48e  -`.
- Progress line beside your tree (`../U210b-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole new PR body beside your tree (`../U210b-pr-body.md`) per CHANGE 3.
- Comments explain a non-obvious why only, no phase narration.

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 35); `verdicts/U210-2567ba11.md`; `briefs/U210-misc-bats-never-reaches-the-snap-store.md`; `AGENTS.md:20-23` and the Audit section's threat-table bullet; Codex thread 4483881479 on PR 667.
