# U322c round 3 of U322: the three repository lints the ubuntu-26.04 leg fails

GOAL
PR 718's Unit test run 42339245827 fails `test (ubuntu-26.04, client)` (job 128303025182) on three repository lints the U322 change tripped and U322b did not reach (its worker committed before the failure names arrived): the canonical-bound case of `test_network_bounds.NetworkBoundTest` (its method name joins the two download tools' names with `_and_`, then `_line_carries_the_canonical_bound_or_is_exempted`) (`scripts/update-agent-assets.sh:2017`, a download line without the canonical bound), `test_network_bounds.NetworkBoundTest.test_no_exemption_is_stale` (an exemption for the same file no longer matching its line), and `test_sandbox_portability.SandboxPortabilityTest.test_tracked_scripts_pass_both_guards` (`scripts/update-agent-assets.sh:1886`, a literal temporary path the portability guard forbids). The FAIL blocks with their assertions are in `/tmp/u322b/ci-failures.txt` (50 lines; the line numbers are those of 2feb0446, the round-1 head; find the same lines at a2916b37).

SCOPE
The same branch `fix/dsh-harness-build-under-srt` and PR 718; the tree is `/tmp/dotfiles-wt/U322` at a2916b37. May write: `scripts/update-agent-assets.sh` (the lines the three lints name and nothing else), `tests/unit/test_network_bounds.py` only if an exemption entry must move (never a new exemption for a line that can carry the bound), and the body `../U322c-pr-body.md` (the round-2 body `/tmp/dotfiles-wt/U322b-pr-body.final.md` plus a `## Round 3` paragraph). Not: any behaviour change, any other file.

CONTEXT
Read the two test modules to learn the rules: the network-bounds test wants every download invocation (the two tools it names) to carry the canonical bound flags (read the test's `CANONICAL` or equivalent constant) or to be listed in its exemption table with the exact line text; the portability guard forbids a hard-coded `/tmp` (use `${TMPDIR:-/tmp}` or the pattern the guard accepts, read `scripts/ci/` or the test for the accepted form). The lines at a2916b37: the download line near `:2017` of round 1, and the temporary path near `:1886` of round 1.

DATA SHAPE
Three one-line changes: the download line carries the canonical bound; the stale exemption entry is updated or removed so it matches a real line or none; the temporary path follows the guard's accepted form. No behaviour of `build_under_srt` changes (the tests of U322 and U322b keep passing).

CHANGE
1. Fix the three lines. 2. `uv run --with pyyaml python -m unittest tests.unit.test_network_bounds tests.unit.test_sandbox_portability tests.unit.test_update_agent_assets -v` OK. 3. `make shellcheck`; `shfmt -i 4 -sr -d scripts/update-agent-assets.sh`; `scripts/lint-comparisons.py --changed`. 4. Commit `fix(updater): the harness build's download line carries the canonical bound and its temporary path follows the portability guard (regime-cutover U322c)` with the trailer. 5. The body: the round-2 body plus `## Round 3` (the three lints, the three lines); `Program-Unit: regime-cutover/U322` once and the footer.

ACCEPTANCE
1. The three test modules OK (counts pasted; the three failing tests named as passing). 2. `git diff --stat a2916b37 HEAD` shows the updater (and the test module only if an exemption moved) (pasted). 3. shellcheck 0; shfmt 0; lint-comparisons 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; CI on the pushed head is the coordinator's check.

CLOSURE
remove

TRUST
TRUST: the unit trusts the repository's two lints (the network-bounds test and the portability guard) as the rule the three lines must satisfy; it changes no behaviour.

TIMEBOX
20 minutes.

FORBIDDEN
No new exemption for a line that can carry the bound; no behaviour change; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u322c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U322`.
- Progress line at `../U322c-progress.txt`; final report to `../U322c-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the three lines before and after, the ACCEPTANCE lines. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46); `decisions.tsv` row 2026-11-07T01:01:00Z (the test_pr_audit class, which this is not); the U322 and U322b briefs.
