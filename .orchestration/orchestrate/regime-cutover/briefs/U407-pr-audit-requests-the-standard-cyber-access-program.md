# U407 pr-audit.sh requests Codex's standard cyber access program, so an account approved for Daybreak audits without a hardware-key session

GOAL
Four audit runs of PR 720 (U343, 2026-11-07 11:05Z to 11:50Z and 2026-11-09 02:32Z to 02:39Z) ended on `You're approved for Daybreak Blue, but this response cannot be shown as this session was not authenticated with one of your authorized hardware keys`, each after about 100,000 tokens, and the pull request has waited on the operator since. Measured 2026-11-09 03:52Z (decisions row 03:55:41Z): `codex exec --cyber-access-program standard` over the PR 720 diff, with the same ChatGPT login, ephemeral and read-only, answered in full. codex-cli 0.166.0 documents the flag (`--cyber-access-program <PROGRAM>`, values standard, daybreak_blue, daybreak_red; omitted, the account's approval applies to the turn), and `--strict-config` refuses a config key of that name (`unknown configuration field cyber_access_program`), so the flag is the one form. The audit route never needs Daybreak: it reads a diff and writes a verdict. After this unit the lever's codex exec line carries `--cyber-access-program standard`, the audit of PR 720 runs, and the operator's hardware-key step is gone (standing order 48).

SCOPE
A new branch `fix/pr-audit-standard-cyber-program` from origin/main 57e5345a1; the tree is the worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U407` (clean, made by worker-worktree.sh). May write: `scripts/orchestrator/pr-audit.sh` and its copy `home/dot_local/bin/common/executable_pr-audit.sh`, `tests/unit/test_pr_audit.py`, `scripts/orchestrator/README.md` (the pr-audit.sh paragraph, if it quotes the codex line), the pin through `scripts/generate-agent-configs.py` (never by hand) and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U407-pr-body.md`. Non-goals: the audit config template `home/dot_agents/codex-audit/config.toml` (no such key exists), every other lever, the fixture `tests/fixtures/pr-audit/fake-codex.py` unless the new argument makes it refuse (read it first; it records argv and should need no change).

CONTEXT
`scripts/orchestrator/pr-audit.sh` at 57e5345a1: lines 1616-1617 are the codex exec invocation through `codex_scratch` (`exec --strict-config --skip-git-repo-check --ephemeral --ignore-rules -C <cwd> --output-schema <schema> -o <verdict JSON> -`); lines 72-76 of the header quote that line and explain `--ignore-rules` and the absent `--ignore-user-config`. `tests/unit/test_pr_audit.py:268-274` pins the exact argv of the exec call (`exec_argv`) through the fixture's recorded calls. The two `codex sandbox` probe calls (lines 269, 300-301) are not turns and take no program flag. The flag applies to the turn alone; the ChatGPT login (operator decision G18) and the scratch config are unchanged.

DATA SHAPE
One argument list, fixed: `exec --strict-config --skip-git-repo-check --ephemeral --ignore-rules --cyber-access-program standard -C <cwd> --output-schema <schema> -o <verdict JSON> -`. The flag's value is the literal `standard`, never read from the environment or the manifest.

CHANGE
1. Test first, red at 57e5345a1: `tests/unit/test_pr_audit.py` `exec_argv` (line 271) gains `"--cyber-access-program", "standard"` after `--ignore-rules`; the assertion at line 273 then fails at 57e5345a1. Paste the red line. Add one assertion that neither `codex sandbox` call carries `--cyber-access-program` (the probes are not turns).
2. `scripts/orchestrator/pr-audit.sh`: add `--cyber-access-program standard` after `--ignore-rules` on line 1616-1617; update the header's quoted line (72-73) and add one sentence after the `--ignore-user-config` sentence: the standard program is requested so an account approved for Daybreak is not gated on a hardware-key session for a turn that needs no Daybreak (measured 2026-11-09, U407). Copy to `home/dot_local/bin/common/executable_pr-audit.sh` (`cmp` 0).
3. Regenerate the pin (`make render-check` form); `scripts/ci/producer-status-check.sh scripts/orchestrator/pr-audit.sh` exits 0 with no output.
4. Body at `/tmp/dotfiles-wt/U407-pr-body.md`: Summary (the four refusals, the probe, the flag; five sentences), Contract (the DATA SHAPE), Threat table (one row per changed path: the lever, its copy, the test module, the README if changed, the manifest and generated outputs; one effect row: the audit's model turn runs under the standard safeguards, not Daybreak, so a cyber-classified refusal is possible and surfaces as codex exit 1 as today, with the controls unchanged: the scratch config, the read-only permission profile, the sandbox probes), Verification (ACCEPTANCE pasted), `Program-Unit: regime-cutover/U407` once at the end.

ACCEPTANCE
1. The red line at 57e5345a1 (`/tmp/u407/red.txt`) and the green line at the head for the argv test, pasted. 2. `python -m unittest tests.unit.test_pr_audit tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs` OK with counts, pasted. 3. `scripts/ci/run-on-lint-files.sh` (the three lint checks of the Makefile lint target: shfmt, ruff format, prettier) exit 0, `make render-check` exit 0, `scripts/ci/producer-status-check.sh scripts/orchestrator/pr-audit.sh` exit 0 with no output, `cmp scripts/orchestrator/pr-audit.sh home/dot_local/bin/common/executable_pr-audit.sh` exit 0, pasted. 4. `git diff --stat 57e5345a1 HEAD` pasted; only the lever, its copy, the test module, the README if changed, the manifest and the generated outputs in it. 5. `grep -c -- '--cyber-access-program standard' scripts/orchestrator/pr-audit.sh` prints 2 (the header's quote and the invocation), pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes the branch, opens the pull request with the body, and the one audit (run by the coordinator with the new lever from the worker tree, since the installed lever is the one that fails), the sweep and CI follow (standing order 49). After the merge and `make deploy-kit`: `pr-audit.sh --records <store> 720` answers with a verdict, the unit's goal check (standing order 42).

CLOSURE
remove

TRUST
TRUST: the unit trusts codex-cli's documented flag and the probe of 2026-11-09 as the evidence that the standard program answers the audit's content, the fixture's fake codex as the argv recorder, and operator decision G18 (the ChatGPT login, kept); it changes no permission profile, no config template and no probe, and it reads nothing new.

TIMEBOX
25 minutes.

FORBIDDEN
No change to `home/dot_agents/codex-audit/config.toml`; no new environment variable or manifest key for the program value; no change to the `codex sandbox` probes; no `# producer-status: allow` comment; no pin edited by hand; no push; no rebase; no `git stash`; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u407/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U407`. The repository is yours alone; your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U407-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U407-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the test with its red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 42, 44, 46, 49); operator decision G18 (2026-10-26); the decisions rows 2026-11-07T11:50:20Z, 2026-11-09T02:40:01Z, 02:40:41Z and 03:55:41Z; `handoff/09-plan-fastest-build-then-tests-2026-11-07.md` section 4.
