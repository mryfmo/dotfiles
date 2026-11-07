# U318b round 2 of U318: seat-login-preflight `--check` validates the directory chain, the printed command is shell-quoted, and the login-command producer's status is read

GOAL
The round-1 audit of PR 714 (`verdicts/U318-e0dd8cc2.md`, merged as 561511c7) filed three findings under the weight threshold in `scripts/orchestrator/seat-login-preflight`, each a defect of the U318 lever at its merged head: (1) `--check` (line 333 at e0dd8cc2) validates only the `claude` leaf of `<seats-root>/.state/claude`, so a linked `.state` parent reaches another directory and a regular file at `.state` is reported `absent` with exit 0, while profile mode validates all three components; (2) profile mode (line 293) prints the operator command with `REGIME_SEATS_ROOT`'s value unquoted, so a seats root holding a space splits the promised command into wrong arguments; (3) the command substitution of `claude_login_command` (line 331) has its status unread, so an injected failure (exit 9) reads as an ordinary absence with an empty command (standing order 21: every producer's status read). This unit fixes the three in one head.

SCOPE
A new branch `fix/seat-login-preflight-chain-quoting-status` from `origin/main` 247d890d; the tree is `/tmp/dotfiles-wt/U318b`. May write: `scripts/orchestrator/seat-login-preflight`, its deployed copy `home/dot_local/bin/common/executable_seat-login-preflight` (byte-identical), `tests/unit/test_remote_host_logins.py` (the `PreflightTest` class), and the regenerated `home/dot_agents/agent-config.yaml` and `scripts/generated-agent-outputs.json` (the lever's pin, by `uv run python scripts/generate-agent-configs.py` only, never by hand), and the body `../U318b-pr-body.md`. Not: `hcom-seat`, any other lever, any doc.

CONTEXT
Read the verdict file `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/verdicts/U318-e0dd8cc2.md` whole (the three findings and the Reproduced section name the scratch fixtures the auditor used). Read `scripts/orchestrator/seat-login-preflight` whole: `claude_config_dir` derives the directory, profile mode validates `<seats-root>`, `.state` and `claude` as three components (each a directory of this user and no link, or absent), `--check` validates the leaf only, `claude_login_command` prints the operator command, and the substitution at line 331 reads it. The U318 tests are in `tests/unit/test_remote_host_logins.py` (`PreflightTest`, 21 tests; `tests/unit/test_hcom_seat.py` `TokenExportTest` 3 tests); they run the lever from the checkout under a scratch HOME with a fake `claude` on PATH.

DATA SHAPE
One validation of a three-component path (`<seats-root>`, `.state`, `claude`), shared by profile mode and `--check`: each component absent, or a directory of this user that is no link; a link, a regular file or another user's directory refuses naming the component. The printed command is one line whose `CLAUDE_CONFIG_DIR=` assignment is shell-quoted (`printf %q` or single quotes with the quote-escape), the same form in the laptop and the `BROWSER=regime-open-url` SSH variants. The producer call reads its status: `cmd=$(claude_login_command) || refuse "..."`.

CHANGE
1. Extract the three-component validation into one function both modes call; `--check` calls it without creating anything and reports `absent` only when every component is absent or a directory, refusing (exit 2, the component named) on a link, a regular file or another user's directory. 2. Quote the `CLAUDE_CONFIG_DIR=<dir>` assignment in every printed command form; a seats root with a space, a quote or a `$` round-trips through `eval` of the printed line to the same directory (test it that way). 3. Read the status of the `claude_login_command` substitution and refuse naming the producer when it fails; keep every other producer in the touched lines checked too. 4. Tests in `PreflightTest`: a linked `.state` parent under `--check` refuses naming `.state`; a regular file at `.state` refuses; a seats root with a space prints a command whose `eval` sets `CLAUDE_CONFIG_DIR` to the exact directory; an injected failure of `claude_login_command` (overlay the function through the test's extracted-function harness, as the U318 tests inject) refuses naming it and prints no empty command. 5. `cmp` the two copies; `uv run python scripts/generate-agent-configs.py` then `make render-check`; `make shellcheck`; `shfmt -d` on the lever; `uv run ruff format --check`; `scripts/ci/lint-comparisons.sh --changed`. 6. Commit `fix(seat-login): the preflight check validates the directory chain, quotes the printed command and reads its producer's status (regime-cutover U318b)` with the trailer. 7. The body: `## Summary`, `## Contract` (TRUST line), `## Threat table` (`row | risk | status | evidence`; every closed row names a test selector; the preflight's exit paths and the printed command as rows), `## Verification` with every ACCEPTANCE line pasted; one line `Program-Unit: regime-cutover/U318` (the parent unit, standing order 24) and the `Generated with [Claude Code]` footer.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_remote_host_logins tests.unit.test_hcom_seat -v` OK (count pasted; the four new tests named). 2. `cmp` exit 0; `make render-check` exit 0; `uv run python scripts/validate-agent-assets.py` exit 0. 3. `make shellcheck` 0; `shfmt -d scripts/orchestrator/seat-login-preflight` 0; `uv run ruff format --check` 0. 4. `scripts/ci/lint-comparisons.sh --changed` 0. 5. On a scratch HOME under `/tmp/u318b/`: `--check` with `.state` a link to another directory exits 2 naming `.state`; with `.state` a regular file exits 2; with `REGIME_SEATS_ROOT='/tmp/u318b/a b'` profile mode prints a command whose `eval` sets the variable to `/tmp/u318b/a b/.state/claude` (pasted); the injected producer failure exits 2 naming `claude_login_command` and prints no `CLAUDE_CONFIG_DIR=` line.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report.

CLOSURE
remove

TRUST
TRUST: the unit trusts the U318 design (one shared claude.ai login directory per host under `<seats-root>/.state/claude`) and changes only the preflight's validation, quoting and status reads; it reads no credential, logs in nowhere, runs no seat.

TIMEBOX
45 minutes.

FORBIDDEN
No change to `hcom-seat`; no doc change; no network; no push; no `gh` call; no edit of the pins by hand; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u318b/`, then read it); no real `claude auth login`.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U318b`.
- Progress line at `../U318b-progress.txt`; final report to `../U318b-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the files changed with `git diff --stat origin/main HEAD`, the ACCEPTANCE lines with their outputs, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46); `verdicts/U318-e0dd8cc2.md`; the U318 brief `briefs/U318-seat-login-is-one-claude-ai-login-per-host-in-a-shared-seats-config-directory.md`.
