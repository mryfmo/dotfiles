# Report: dotfiles-T124-wave3b-audit-grammar-a01

- Seat: `claude-standard-dot-a003` (Claude Code, profile `standard`) in `.claude/worktrees/worker-f`, seated by `herdr-agents --add-worker` (bring-up PING `bringup-1791624759-97717` answered `alive`).
- Branch `feat/audit-grammar` from `origin/main` `d29ce4c1` (`git switch -c feat/audit-grammar --no-track origin/main`); PR #314 (`feat(audit): fixed finding grammar, orchestrator artifacts in scope, invariant lines`), one commit, head `2ee71f807371daad9cbc14109a8f5b848d8ed900`. Pushed with the authorized form of the task's Push form section.
- Task file read in full with its design (`dotfiles-T124-design-gate-and-reset-rule-a01.md`), the round-3 receipt, wave 1's task for the standing Bot/CI and sandbox-conduct sections, and Amendments 1, 2 and the Push form section.

## What changed

1. `home/dot_local/bin/common/executable_herdr-agents`, `--audit <sha> --task <id>` only (the per-commit prompt is unchanged, Amendment 1):
   - (a) one finding grammar, stated once in the prompt: `[P<0-3>] <high|medium|low> <specification|implementation|evidence|orchestration|conformance> <path:line|-> <rationale>`, with a one-line definition of each category. Dimension (1) "specification conformance" became the category `specification`, so it cannot be confused with the new `conformance` category.
   - (b) scope sentence: the orchestrator as well as the worker; the task file with its amendments, the acceptance record, the PR-feedback sweep, and the design task file and receipts named under `design_review` when the task names them. `orchestration` covers task wording, scope decisions, dispositions and acceptance claims; `conformance` covers deviations from the regime process. The design file is named in prose, not parsed from the front matter: the auditor reads the task file anyway, and a YAML parse in bash would be new code nothing tests.
   - (c) a `format: 2` task (front matter between the opening and closing `---`, `format: 2` as an integer, the same rule as wave 1's `validate-task.py`) adds: "before the verdict line, write one line per invariant id of the task front matter, `INV-n: holds|violated <path:line>`, then the line `Orchestration findings: <count>`". Placing them before the verdict keeps the wrapper's last-line verdict parse intact.
   - (d) inputs, each named only when present: `.orchestration/acceptance/<id>.md` "as it stands (earlier rounds' dispositions and the PR-feedback dispositions)" and `.orchestration/validation/<id>-permgate.jsonl` (the path is my reading of the design's "`<task>-permgate.jsonl` into the audit's input list", next to `<id>-pr-feedback.json`; wave 2b must write it there or change this line).
   - (e) after the verdict source is read (`.last.md`, or the transcript fallback), a `format: 2` task prints `WARN: herdr-agents: format 2 task <id>: the audit output has no INV-n: holds|violated line.` and/or `... no Orchestration findings: line.` to stderr; the exit status stays verdict-only.
   - The `--task` help text (shdoc `@option` and the usage text) names the new inputs and the warning.
2. `AGENTS.md` Audit: scope includes the task's orchestration artifacts; the auditor's standing over the orchestrator's and the worker's mistakes (operator direction 2026-10-10); the grammar with the five categories, one line each; the INV and count lines for `format: 2` tasks; the lock (`orchestration`/`conformance` at P0–P2 released only by an operator waiver or a design reset; the orchestrator cannot disposition them); the verdict line unchanged.
3. SKILL, task-level audit bullet: the headless sub-bullet names the two new inputs and asks for the findings "in the grammar and categories of the AGENTS.md Audit section (the repository's statement of the finding grammar)", plus the INV and count lines for `format: 2`. **One sibling sub-bullet also changed**, "Run either form from a clean tree": its parenthetical list of the untracked evidence an audit may see gained "acceptance record, permgate extract". Without it, the acceptance record the prompt now names would itself be a clean-tree violation. It sits in the same task-level audit bullet, outside wave 1's hunks; I flag it because the task says "no other SKILL section".
4. `README.md` (Amendment 2): the `--task` paragraph names the new inputs and points at the AGENTS.md Audit grammar instead of restating the old one.
5. `tests/unit/test_herdr_agents.py` (Amendment 1): only the expected prompt string of `test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff`.
6. `tests/unit/test_herdr_agents_audit.py` (new, 8 tests). It loads the fake-herdr harness from `test_herdr_agents.py` by path under a private name and defines `load_tests`, so discovery runs only these 8 and not the inherited suite again (`make unit-test` shows `test_herdr_agents_audit` 8 times). Each rule was removed in a scratch `git archive` copy and its test failed (validation §5).

## Invariants

- INV-7 (this wave's part): grammar with five categories (prompt and AGENTS.md), the acceptance record as an input, the `Orchestration findings:` line for `format: 2`, the lock in AGENTS.md. Not this wave: "unparsable lines make the audit blocked" and the lock's enforcement are the gate's (waves 2a and 2b); AGENTS.md does not claim the gate already does it.
- INV-4 (this wave's part): the prompt asks for `INV-n: holds|violated <path:line>`, and the wrapper warns when none is present. The gate's `blocked`/`incorrect` handling is wave 2a's.

## Notes for the orchestrator

- `scripts/validate-task.py` is not on `origin/main` (wave 1 unmerged), so Worker Playbook step 1's validator run was not possible; the task file was read by hand.
- The per-commit prompt (no `--task`) still says "Follow the Audit section of AGENTS.md exactly … report each finding as `[P0-P3] confidence file:line rationale`", which now differs from the AGENTS.md grammar. Amendment 1 kept it unchanged; the gate rejects per-commit audits.
- The validation item "herdr-agents --audit --dry-run" has no such flag and the wrapper writes no prompt file; adding one is outside the task. The prompt for this task's real file was captured through the fake-herdr harness (validation §6).
- Scope gaps raised by PONG and resolved: the exact-prompt test (Amendment 1), the README paragraph (Amendment 2), the push (Push form section).
- Known limit of the `format: 2` check (`executable_herdr-agents:1903-1905`): it matches `^format:[[:space:]]*2[[:space:]]*$` inside the front matter, so `format: 2  # comment` (YAML integer 2, which wave 1's validator counts as format 2) reads as legacy, and the prompt then omits the INV and count request; quoted `format: "2"` is legacy in both. No task file uses a trailing comment there; the gate's own parse (wave 2a) is the authority.
- Understand-Anything hook: did not fire in this session.
- plan-mode-used: no.

## CompactionDB

The task file carries no `[memory:decision]` line, so the decision recorded is this wave's outcome. Command (main checkout, outside the sandbox through the permission gate; validation §9 pastes it with its output):

```
cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content '[memory:decision] dotfiles-T124 wave 3b (worker claude-standard-dot-a003, 2026-10-10, PR 314): the task-level audit prompt (herdr-agents --audit <sha> --task <id>) states one finding grammar … the per-commit prompt is unchanged.'
```

Printed id: `5e920c65-befb-4173-a7f7-9e29868e289a`. No read-back: from the worktree sandbox the main checkout's DB cannot be opened (`contextdb: [Errno 1] Operation not permitted`), and a search outside the sandbox is not a step 4 case.

## CI and Bot

- CI: 14 of 14 checks pass on `2ee71f80` (validation §7).
- Bot: the Codex code review (completed 2026-10-10T09:59:27Z) and security review (10:01:11Z) of `2ee71f8` finished with no findings: the connector's summary comment and its 👍 reaction at 10:01:15Z, with no review object, no review comment and no thread. The SKILL's 15-minute loop, which matches review objects, ended `bot: none` at 10:18:54Z (validation §8). CodeRabbit skipped (automatic reviews disabled).
- Threads: none. Nothing to fix or disposition; I resolved nothing.
- Local suite: `make unit-test` at the committed head fails 75 test ids, the same set `origin/main` fails in this sandbox (validation §3); every audit test passes (§1, §2).

cost: n/a
