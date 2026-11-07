# U322d round 4 of U322: the resolver read has its injection, a separate /private/tmp/claude is denied on Linux too, and the table carries every changed path with a selector

GOAL
The round-3 audit of PR 718 (`verdicts/U322c-0fc4740b.md`, correct) left three findings at or above the threshold and one filed P1 that this round closes before the merge. P2 (`scripts/update-agent-assets.sh:1914`, f10 s3): the resolver read of `build_under_srt` (the physical path of the deny root's parent, the `pwd -P` that derives srt's second temporary spelling) has no failure-injection test; the six `pwd -P` injections and the failed-dirname test do not reach it. P2 (`tests/unit/test_sandbox_portability.py:62`, f10 s2): the threat table has no rows for `tests/unit/test_sandbox_portability.py` and `tests/unit/test_network_bounds.py`, which round 3 changed (an exemption re-keyed, an allowance row added). P2 (`docs/deepseek-harness.md:60`, f10 s2): the docs and fixture rows are `closed` on prettier and a fixture helper's name, neither a regression selector. P1 filed (`:1940`, f1 s5): on Linux, when `/private/tmp/claude` exists as a directory separate from `/tmp/claude` (no link between them), srt grants writes to it and the deny list names only the spelling `pwd -P` derived from `/tmp`, so the two-root guarantee has a third root there.

SCOPE
The same branch `fix/dsh-harness-build-under-srt` and PR 718; the tree is `/tmp/dotfiles-wt/U322` at 0fc4740b. May write: `scripts/update-agent-assets.sh` (`build_under_srt` only), `tests/unit/test_update_agent_assets.py`, `tests/unit/test_sandbox_portability.py` only if the allowance row must change for the new deny word, and the body `../U322d-pr-body.md` (the round-3 body `/tmp/dotfiles-wt/U322c-pr-body.final.md` plus `## Round 4` and the corrected table). Not: any other file.

CONTEXT
Read the verdict whole (its Reproduced section names how the auditor confirmed srt grants an existing `/private/tmp/claude` on Linux). Read `build_under_srt` at 0fc4740b: the `deny_write` array, the `tmp_real` derivation and its refusal, the injection form the round-2 tests use for the other producers (a fake `pwd` or a wrapped function through `BASH_ENV`, read them). The portability guard's allowance table (`ALLOWED_TMP` in `tests/unit/test_sandbox_portability.py`) keys exact (file, word) pairs; a second literal word in the updater needs its own row with the same reason, or the second spelling is derived without a literal (prefer deriving: `/private/tmp/claude` is `/private` + the `/tmp/claude` word, so build it from the one word with a string operation and deny it when `[ -d /private/tmp ]` or unconditionally).

DATA SHAPE
`deny_write` names srt's implicit grants in every spelling the kernel may see: the literal `/tmp/claude`, its `pwd -P` form when `/tmp` is a link, and `/private/tmp/claude` whenever `/private/tmp` exists as a directory (Linux hosts with such a directory, macOS where it is the physical `/tmp`), each entry once (deduplicated), plus `~/.npm/_logs` in HOME's physical form; the derivation of the second spelling reads its producer's status and refuses by name on failure. Every producer of `build_under_srt` has a failure injection whose refusal names it, the resolver read included. The threat table has one row per changed path (the two test modules included), each closed row naming a test selector that fails against the round the row closes, the docs row `closed` by a test that reads the paragraph (a one-assertion test in the updater's module that the docs paragraph names `srt` and `build_under_srt`) or `out-of-scope` naming U333.

CHANGE
1. The deny list: add the `/private/tmp/claude` spelling as DATA SHAPE says, deduplicated; a test with a fake `pwd -P` answering `/tmp` and a fixture `/private/tmp` directory asserts both spellings in `denyWrite`; a test where `/private/tmp` is absent asserts no such entry. 2. A failure injection for the resolver read (the `cd` or `pwd -P` of the deny root's parent) refusing by name with nothing run. 3. The table: rows for `tests/unit/test_sandbox_portability.py` (risk: an allowance that widens the guard beyond the one word; closed by the guard test with the exact table) and `tests/unit/test_network_bounds.py` (risk: a stale or widened exemption; closed by `test_no_exemption_is_stale` and the canonical-bound case); the docs row closed by the new one-assertion test or out-of-scope naming U333; the fixture rows naming the tests that use the fixture. 4. `uv run --with pyyaml python -m unittest tests.unit.test_update_agent_assets tests.unit.test_network_bounds tests.unit.test_sandbox_portability -v`; `make shellcheck`; `shfmt -i 4 -sr -d scripts/update-agent-assets.sh`; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`. 5. Commit `fix(updater): the harness build denies srt's second temporary spelling on Linux too and every resolver read has its injection (regime-cutover U322d)` with the trailer. 6. The body: `## Round 4` naming the four findings and the fixes; the table as CHANGE 3; `Program-Unit: regime-cutover/U322` once and the footer.

ACCEPTANCE
1. The three test modules OK (counts pasted; the new tests named). 2. The two new deny tests and the resolver injection fail against 0fc4740b's updater (the round-2 form) and pass on the head (outputs pasted). 3. shellcheck 0; shfmt 0; ruff 0; lint-comparisons 0. 4. The table has one row per changed path of `git diff --name-only origin/main HEAD` (the list and the rows pasted) and every closed row names a selector (grep pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; CI on the pushed head is the coordinator's check.

CLOSURE
remove

TRUST
TRUST: the unit trusts srt 0.0.81's implicit-grant list as the auditor read it from the installed source (both temporary spellings and the npm log directory) and the dsh role's deny list; it changes the deny list and the tests only.

TIMEBOX
40 minutes.

FORBIDDEN
No second literal temporary word unless the guard's table gains its row with the same reason; no behaviour change beyond the deny entry and the refusal; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u322d/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U322`. The worktree is yours alone; no other worker enters it while you run.
- Progress line at `../U322d-progress.txt`; final report to `../U322d-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), `git diff --stat 0fc4740b HEAD`, the ACCEPTANCE lines with their outputs, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46); `verdicts/U322c-0fc4740b.md`; the U322, U322b and U322c briefs.
