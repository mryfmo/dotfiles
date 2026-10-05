# AGMSG-TASK dot-audit-pane-visibility-T32-a01

## Objective

Operator directive (2026-09-27): the auditor's work must be VISIBLE on herdr
like the worker's, instead of running headless inside the orchestrator's
shell. Give `herdr-agents` an `--audit` mode that runs the Codex audit in a
dedicated, visible pane of the pair workspace while preserving the auditor's
nature: orchestrator-invoked, read-only sandbox, NO agmsg identity, findings
are input and acceptance stays orchestrator-only.

Verified herdr facts (orchestrator, read-only, 2026-09-27): `herdr tab
create|list|get|rename|close` exist; `herdr pane run` executes text+Enter in
a pane; `pane wait-output --regex` and `pane read` exist. The attach-mode
ambiguity guard (`attach_panes_are_unambiguous`) evaluates panes on the
ORCHESTRATOR PANE'S TAB only (`panes_on_pane_tab`), so a separate audit tab
does not affect it — prove this with a test, do not weaken any guard.

[memory:decision] T32: herdr-agents --audit <commit> runs the Codex audit
visibly in a dedicated `audit` tab of the pair workspace (tee to the
validation evidence path; identity-less, read-only, orchestrator-invoked
unchanged); headless invocation remains the fallback without a herdr
workspace (operator 2026-09-27).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`, then
  `git switch -c feat/audit-pane-visibility origin/main`.
  (Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG.)
- If the worktree has uncommitted files, stop and report via AGMSG-PONG.

## Changes

### 1. `home/dot_local/bin/common/executable_herdr-agents` — `--audit` mode

- Usage: `herdr-agents --audit <commit-sha> [DIR]` (DIR defaults like the
  other modes). Exit 2 mirrors `--restart-worker` refusals when DIR has no
  managed workspace.
- Behavior:
  - Resolve the pair workspace via the existing `single_managed_workspace`
    pane-evidence lookup (reuse; do not duplicate).
  - Find or create a tab labeled `audit` in that workspace (`herdr tab
create` + rename per its CLI; reuse an existing audit tab's shell pane —
    exactly one audit pane, no unbounded tab growth).
  - In that pane, `herdr pane run` the audit:
    `codex --profile audit review --commit <sha> 2>&1 | tee <evidence-path>; printf 'AUDIT-EXIT:%s\n' $?`
    where `<evidence-path>` is an argument
    (`--out <path>`, default `.orchestration/validation/audit-<sha>.md` under
    DIR). Wait bounded for the `AUDIT-EXIT:` marker via `pane wait-output
--regex` (generous timeout flag with a sane default, e.g. 30m), then
    report the exit code and the evidence path on stdout; nonzero audit exit
    → nonzero herdr-agents exit.
  - The pane and tab STAY OPEN after the run (visibility is the point); a
    subsequent `--audit` reuses them.
- Guards: never create panes in the pair tab; never touch the worker pane;
  `attach_panes_are_unambiguous` and full-mode/duplicate-workspace guards
  unchanged (the audit tab must be invisible to them — covered by the
  tab-scoped filtering, prove with a test).
- shdoc English comments; README `--audit` paragraph (one short block:
  purpose, invocation, evidence path, that headless
  `codex --profile audit review` remains the fallback without herdr).

### 2. Rules text

- `home/dot_config/claude/rules/agmsg-orchestration.md`: amend the audit
  bullet: replace "pane-less" with "runs visibly in the pair workspace's
  dedicated audit tab via `herdr-agents --audit <sha>` when a herdr workspace
  exists (headless `codex --profile audit review` otherwise); still
  identity-less, read-only, orchestrator-invoked, under the acceptance
  exemption".
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: mirror the same
  clause in the carve-out sentence added by T30.

### 3. Tests — `tests/unit/test_herdr_agents.py`

Fake herdr gains `tab list/create/rename` handling as needed. Cases with a
mutation baseline (paste the FAILED run against the unmodified script):
(a) `--audit` creates the audit tab once and reuses it on a second run
(exactly one tab create across two invocations); (b) the audit command line
sent via `pane run` contains the profile invocation, the tee target, and the
exit marker; (c) nonzero `AUDIT-EXIT` propagates to a nonzero exit; (d) exit
2 without a managed workspace; (e) regression: an extra pane on a DIFFERENT
tab (the audit tab) does not break `--attach` order/ratio repair or the
full-mode duplicate guard (assert the existing guards still pass with an
audit tab present).

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `home/dot_config/claude/rules/agmsg-orchestration.md`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `README.md`
- `tests/unit/test_herdr_agents.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-audit-pane-visibility-T32-a01.md` (main checkout)

## Forbidden actions

- Running a real audit or any codex invocation; creating real herdr
  tabs/panes on this host; touching model_profiles, permgate, hooks configs,
  dependencies, validator/generator scripts, or `reviews/ADH_Integrated_Plan/`.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
   Watch CI to green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the mutation baseline) and the PR number/head SHA.
3. CompactionDB from the main checkout:
   `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T32: herdr-agents --audit <commit> runs the Codex audit visibly in a dedicated audit tab (tee to validation evidence, exit-marker wait, tab reused); auditor stays identity-less/read-only/orchestrator-invoked; headless invocation is the no-herdr fallback (operator 2026-09-27)"`
   — paste command and output.
4. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
   Live E2E (a real `--audit` run) is orchestrator-side at acceptance.
