# AGMSG-TASK dot-orchestration-hygiene-T33i-a01

## Objective

Codify three lessons from the 2026-09-28 remediation batch and add one
mechanical guard, so they stop living only in orchestrator memory
(`.orchestration/learning/rule_candidates/audit-evidence-secret-validator.md`,
acceptance records T33b/T33e/T33f).

1. **Secret masking of audit evidence (mechanical).** Audit transcripts tee'd by
   `herdr-agents --audit` contain reviewed content and tool output; quoted
   `*_token: <quoted value masked for the repo secret validator>` schema fields tripped `validate-agent-assets.py`'s
   `SECRET_PATTERN` and turned main red (04746ca/e8cf7e1). Single source of
   truth: add a `--mask-secrets <file>...` mode to `scripts/validate-agent-assets.py`
   that rewrites each `SECRET_PATTERN` match in the given files to
   `<redacted:secret-pattern>` in place and prints `masked <n> match(es) in <file>`
   per file (exit 0; exit 2 on a missing file). Then, in `herdr-agents --audit`,
   after the exit marker and before printing the verdict, run
   `python3 DIR/scripts/validate-agent-assets.py --mask-secrets <evidence> <evidence>.last.md`
   when that script exists under DIR (skip silently otherwise) and print its
   output; the verdict gate runs on the masked last-message file (masking never
   touches a `Verdict:` line). Tests: validator mode (masks, counts, leaves
   other text, exit codes) with a mutation baseline; herdr-agents fake harness
   asserts the mask call and its placement before the gate.
2. **Boundary-commit validation (rule text).** Claude rule
   `home/dot_config/claude/rules/agmsg-orchestration.md` and the SKILL
   ("Review and integration invariants"): before every `.orchestration`
   boundary commit the orchestrator runs `make validate-agent-assets` and
   branches on its real exit status (never through a pipe); a failure is fixed
   before pushing.
3. **Task-authoring discipline (rule text, SKILL "Orchestrator Playbook" step 3).**
   (a) `allowed_files` is grounded by grepping the repository for every
   touch point named in the task (tests that pin call sequences, mirrors,
   fixtures) before dispatch; (b) a CLI constraint asserted in a task is
   verified by executing the real command in a safe form, not by reading
   `--help` (the `codex review --commit … [PROMPT]` conflict was missed that
   way); (c) an auditor finding that contradicts the orchestrator's review is
   presumed right until refuted with evidence (T33f).
4. **Understand-Anything plugin gaps (README note).** In the README
   Understand-Anything paragraph add two sentences: plugin 2.9.7's
   `merge-batch-graphs.py` drops `tested_by` edges from `.bats` tests and from
   non-`file:` production nodes, and `extract-structure.mjs` misses shell
   functions with a subshell body; a full rebuild therefore under-reports test
   coverage until upstream fixes land (operator decides on filing issues).

[memory:decision] T33i: audit evidence is secret-masked by
`validate-agent-assets.py --mask-secrets` inside `herdr-agents --audit`
before the verdict gate; the orchestrator validates agent assets (real exit
status) before every boundary commit; task authoring grounds allowed_files by
grep, verifies CLI constraints by execution, and presumes auditor findings
right until refuted; the README records the Understand-Anything 2.9.7 coverage
gaps (operator 2026-09-28).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c fix/orchestration-hygiene-T33i origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG.

## Allowed files

- `scripts/validate-agent-assets.py`
- `home/dot_local/bin/common/executable_herdr-agents`
- `home/dot_config/claude/rules/agmsg-orchestration.md`
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`
- `README.md`
- `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_herdr_agents.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-orchestration-hygiene-T33i-a01.md` (main checkout)

## Forbidden actions

- Changing `SECRET_PATTERN` itself or the committed-secret scan's coverage;
  running a real audit or codex; creating herdr tabs/panes; touching
  AGENTS.md, model_profiles, permgate, hooks configs, `reviews/ADH_Integrated_Plan/`;
  merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
shellcheck -x home/dot_local/bin/common/executable_herdr-agents
shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the mutation baseline) and the PR number/head SHA; quote each
   added rule sentence in the report.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
   Live E2E (a real `--audit` run showing the mask step) is orchestrator-side.
