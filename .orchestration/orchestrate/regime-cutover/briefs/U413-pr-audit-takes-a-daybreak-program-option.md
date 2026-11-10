# U413 pr-audit.sh takes `--cyber-program daybreak_blue`, which runs the audit turn under the Daybreak Blue program on gpt-6-sol, for a unit whose content the standard program's classifier refuses

GOAL
PR 720 (U343e, head fd94feae, the acp-broker lever) cannot be audited by the installed lever: under the account's Daybreak approval (attempts 1 to 5, 2026-11-07 to 11-09) the turn ended on the hardware-key gate, and under `--cyber-access-program standard` (U407, attempt 6 at 2026-11-09 23:51Z) it ended on `This content was flagged for possible cybersecurity risk ... confirm that the access_programs.cyber parameter is set to the appropriate tier` after 97,319 tokens, while codex ran the broker's tests. Measured 23:5xZ after the operator's new `codex login`: `--cyber-access-program daybreak_blue` is refused on gpt-6.1-sol (`403 Daybreak isn't available for this model`) and answers on gpt-6-sol, both for a one-word turn and for a static review of the 720 diff with sandbox-boundary findings and no hardware-key message (/tmp/u343-probe2/answer.txt). OpenAI's Daybreak troubleshooting page names gpt-6-sol and gpt-6-luna as the Daybreak Blue models. So the lever needs one option: `--cyber-program <standard|daybreak_blue>`, default `standard` (every audit since U407), and `daybreak_blue` runs the turn with `--cyber-access-program daybreak_blue -c model="gpt-6-sol"` for the units whose content the standard classifier refuses. The coordinator passes it per run and records it in the audit row's verifier text.

SCOPE
A new branch `feat/pr-audit-daybreak-program-option` from origin/main 305d4f53b; the tree is the worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U413` (clean, made by worker-worktree.sh). May write: `scripts/orchestrator/pr-audit.sh` and its copy `home/dot_local/bin/common/executable_pr-audit.sh`, `tests/unit/test_pr_audit.py`, `scripts/orchestrator/README.md` (the pr-audit.sh paragraph: one sentence on the option), the pin through `scripts/generate-agent-configs.py` (never by hand) and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U413-pr-body.md`. Non-goals: the audit config template `home/dot_agents/codex-audit/config.toml` (its model stays gpt-6.1-sol for the standard program), the `codex sandbox` probes, every other lever.

CONTEXT
`scripts/orchestrator/pr-audit.sh` at 305d4f53b: the header's `@option` block (lines 120 on) names `--records <dir>`; the invocation at lines 1619-1621 passes `--cyber-access-program standard` after `--ignore-rules`; the header's quoted line and the U407 sentence are at lines 72-79. Argument parsing: find where `--records` is read and add the option beside it with the same refusal style (exit 2 on a value outside the two words, exit 2 when the value is missing). `tests/unit/test_pr_audit.py:268-274` pins `exec_argv` for the default run and `:300-302` asserts the probes carry no program flag. codex-cli 0.166.0: `--cyber-access-program <standard|daybreak_blue|daybreak_red>`; `-c model="gpt-6-sol"` is a config override that `--strict-config` accepts (model is a known key; the scratch config.toml's own `model` line is overridden for the run). Standing order 21: the option's value is read as one of two words, anything else refused.

DATA SHAPE
One option with two literal values. `standard` (default): the exec argv as today. `daybreak_blue`: the exec argv with `--cyber-access-program daybreak_blue -c model="gpt-6-sol"` in the place of `--cyber-access-program standard`; the model name is a literal in the lever beside the program name (one table of two rows: program, model override or none), never read from the environment or the manifest. The probes are unchanged in both cases.

CHANGE
1. Tests first, red at 305d4f53b: (a) `pr-audit.sh --cyber-program daybreak_blue <pr>` makes the exec argv carry `--cyber-access-program daybreak_blue -c model="gpt-6-sol"` and no `standard`; the probes still carry no program flag; (b) `--cyber-program red` (any other word) and `--cyber-program` without a value are refused with exit 2 before any codex call (the fixture records none); (c) the default run's argv is unchanged (the existing assertion). Paste the red lines.
2. The lever: the option, the two-row table, the invocation built from it; the header gains an `@option --cyber-program <standard|daybreak_blue>` line and one sentence after the U407 sentence saying when daybreak_blue is used (a unit whose content the standard classifier refuses; measured on U343, 2026-11-09) and that it needs the operator's Codex session to carry the account's hardware key. Copy to `home/dot_local/bin/common/executable_pr-audit.sh` (`cmp` 0).
3. Regenerate the pin (`make render-check` form); `scripts/ci/producer-status-check.sh scripts/orchestrator/pr-audit.sh` exits 0 with no output. README: one sentence.
4. Body at `/tmp/dotfiles-wt/U413-pr-body.md`: Summary (attempts 1 to 6 and the probes; five sentences), Contract (the DATA SHAPE), Threat table with five columns (Path or effect, Change, Risk and bound, Status, Evidence; one row per changed path with status closed and the Verification line as evidence; one effect row: a daybreak_blue audit runs the model under reduced cyber safeguards for the audit turn alone, inside the same read-only permission profile and sandbox probes, status residual with the first daybreak_blue audit of PR 720 as its measurement), Verification (ACCEPTANCE pasted), `Program-Unit: regime-cutover/U413` once at the end.

ACCEPTANCE
1. The red lines of tests (a) and (b) at 305d4f53b (`/tmp/u413/red.txt`) and their green lines at the head, pasted. 2. `python -m unittest tests.unit.test_pr_audit tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs` OK with counts, pasted. 3. `scripts/ci/run-on-lint-files.sh` (shfmt, ruff format, prettier as the Makefile lint target runs them) exit 0, `make render-check` exit 0, `scripts/ci/producer-status-check.sh scripts/orchestrator/pr-audit.sh` exit 0 with no output, `cmp` of the lever and its copy exit 0, pasted. 4. `git diff --stat 305d4f53b HEAD` pasted; only the lever, its copy, the test module, the README, the manifest and the generated outputs in it. 5. `grep -c -- 'daybreak_blue' scripts/orchestrator/pr-audit.sh` prints 3 or more (the header, the table, the refusal), pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator fetches the head by path, pushes the branch, opens the pull request with the body, and the one audit (standard, the installed lever), the sweep and CI follow. After the merge and `make deploy-kit`: `pr-audit.sh --cyber-program daybreak_blue --records <store> 720` answers with a verdict, the unit's goal check (standing order 42).

CLOSURE
allowlist

TRUST
TRUST: the unit trusts codex-cli's documented flag and config override, OpenAI's Daybreak page for the model names, and the 23:5xZ probes as the evidence that daybreak_blue on gpt-6-sol answers for U343's content under the operator's session; the option's values are an exact two-word table, anything else refused; it changes no permission profile, no template and no probe.

TIMEBOX
30 minutes.

FORBIDDEN
No change to `home/dot_agents/codex-audit/config.toml`; no environment variable or manifest key for the program or the model; no third program value; no change to the `codex sandbox` probes; no `# producer-status: allow` comment; no pin edited by hand; no push; no rebase; no `git stash`; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u413/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U413`. The repository is yours alone; your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U413-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U413-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 42, 44, 46, 49); operator decision G18; the U407 brief; the decisions rows 2026-11-09T05:37:11Z, 23:51:45Z and 23:55:15Z.
