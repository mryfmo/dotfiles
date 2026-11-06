# U272b round 1b of U272: the dsh role tests pass the committed-secret scan

GOAL
PR 697 (U272, head 1ddd42c9) fails the `validate` CI check: `scripts/validate-agent-assets.py` reports two findings of the `generic-token` rule in `tests/unit/test_hcom_seat_dsh.py` at lines 249 and 349, both the quoted assignment `CLAUDE_CODE_OAUTH_<redacted:secret-pattern>

SCOPE
The existing branch `feat/hcom-seat-dsh-role` at 1ddd42c95107521f2ca8fabeda5b35cf9c410559 in `/tmp/dotfiles-wt/U272` (the PR is 697). May write: `tests/unit/test_hcom_seat_dsh.py` and the body `../U272-pr-body.md` (one line under Verification naming this round). Not: `scripts/validate-agent-assets.py`, its `SECRET_ALLOWLIST`, any other file.

CONTEXT
Read `scripts/validate-agent-assets.py` lines 190 to 330 (the assignment rules and the allowlist contract) and the top of `tests/unit/test_hcom_seat_dsh.py` for the existing constants. An allowlist row is the wrong tool here (the allowlist is for a legitimate line that must carry a token-like literal; a test fixture can be renamed).

DATA SHAPE
One module constant, `CALLER_OAUTH_VALUE = "caller-value-u272"` (or the same pattern as `FAKE_OAUTH_VALUE`), beside the existing constants; the two call sites pass `CLAUDE_CODE_OAUTH_TOKEN=CALLER_OAUTH_VALUE`; the assertion that the caller's value reached the shim (if any) compares against the constant.

CHANGE
1. The constant and the two call sites; no other edit.
2. Run the scanner locally as CI does: `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0 (paste the tail).
3. Commit on top of 1ddd42c9; add the round line to the body.

ACCEPTANCE
1. `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
2. `uv run python -m unittest tests.unit.test_hcom_seat_dsh tests.unit.test_hcom_seat` OK (paste the count).
3. `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0.
4. `git diff 1ddd42c9 --stat` shows one file.

VERIFY
ACCEPTANCE pasted into the body. CI's `validate` check on the PR is the coordinator's evidence.

CLOSURE
remove

TRUST
TRUST: the unit trusts the scanner's rule as the boundary and renames a test fixture; it changes no production code and reads no credential.

TIMEBOX
15 minutes.

FORBIDDEN
No allowlist row; no change outside the one test file and the body line; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u272b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U272` and the coordinator fetches it by path.
- Progress line at `../U272b-progress.txt`; final report to `../U272b-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Laziness Protocol: the smallest change that passes the gate).

REPORT
Status, head sha (40 hex), files changed, the ACCEPTANCE result lines, deviations. Under 8 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); `scripts/validate-agent-assets.py` (the secret scan contract); PR 697.
