# AGMSG-TASK dotfiles-T122-codify-bot-ci-root-cause-a01

Drafted 2026-10-09 by the orchestrator seat (`claude-deep-dot`, w4:p1). Codifies the operator's standing instruction of 2026-10-09 (given during T118, carried so far only in task files T118 Amendment, T119, T120): every Codex Bot finding and CI failure on a PR is fixed at its root cause in that PR. Kind: prose in the shared SKILL, one Claude rule file and `AGENTS.md`; no code; Claude seat allowed (precedent T113, `claude-standard-dot-a005`, edited the same SKILL and rule file). Files are disjoint from T119 and T120, so it may run concurrently on a second worker.

## Changes, stated once

1. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, Worker Playbook step 15 (the CI and Codex Bot wait): add, as sub-bullets after the existing ones, the standing instruction verbatim in substance: every Bot finding and every CI failure on the PR is fixed at its root cause in the PR itself; a `not-applicable` is reserved for a finding that is factually wrong, and the worker proposes it with the refuting command and output in the RESULT (`threads=<id>-proposed-not-applicable:<reason>(validation-<section>)`), never replies on or resolves the thread; a finding on the task's own wording is still fixed in the PR; "out of scope" is not a disposition for a finding on files the PR touches: the worker reports the scope gap and the orchestrator amends the allowed files; the reviews are rechecked once more right before the RESULT.
2. Same file, Orchestrator Playbook step 10, the sweep sub-step: the orchestrator verifies every proposed `not-applicable` with its own reproduction before resolving the thread, probing each sub-case the finding names (T118 example: "cache absent **or stale**" needed two probes); the orchestrator alone replies on and resolves Bot threads, pasting the refuting command and output in the reply; the sweep JSON disposition names the reply id and the validation section. A `fixed:<sha>` disposition is verified in the diff of that sha, not taken from the RESULT.
3. `home/dot_config/claude/rules/pr-integration.md`, second bullet: after "Stopgaps, suppressions, or "later" are not dispositions", add: `A "not-applicable" needs a refutation pasted in the thread (the command and its output); out of scope is reported as a scope gap, never written as a disposition.`
4. `AGENTS.md`, "Agent Review Evidence", last bullet: append one sentence pointing at the rule: `Every Bot finding and CI failure is fixed at its root cause in the PR; see home/dot_config/claude/rules/pr-integration.md for the only accepted not-applicable.`
5. Tests: if `tests/unit` has a test that pins the SKILL or rule wording (grep `pr-integration` and `Worker Playbook` under `tests/`), extend it with one assertion for the new sentence; otherwise state that no test pins this prose.

Forbidden: anything else; any code file; README; `make update`; thread resolution.

[memory:decision] dotfiles-T122 (orchestrator 2026-10-09): Bot and CI findings are fixed at their root cause in the PR; `not-applicable` only for a factually wrong finding, refuted with a pasted command and output, verified by the orchestrator's own reproduction per named sub-case; the orchestrator alone replies on and resolves threads; scope gaps are reported, never dispositioned.

## Repo / branch

A free worker worktree (`.claude/worktrees/worker-d` if T119/T120 occupy worker-c): `git fetch origin`; `git switch -c docs/codify-bot-ci-root-cause --no-track origin/main`.

## Allowed files

`home/dot_agents/skills/agmsg-orchestration/SKILL.md` (steps 15 and 10 only), `home/dot_config/claude/rules/pr-integration.md`, `AGENTS.md` (the one sentence), plus the one pinned-wording test if it exists (name it in the report). Artifacts at the standard `dotfiles-T122-codify-bot-ci-root-cause-a01` paths in the main checkout, masked.

## Validation commands (paste verbatim output, whole)

```
git diff --stat origin/main
mise x node npm:prettier -- prettier --check AGENTS.md home/dot_config/claude/rules/pr-integration.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2
make render-check; echo "rc=$?"
make unit-test 2>&1 | tail -3
gh pr checks <pr>
```

## Completion

PR to `main` (English title `docs(regime): fix every Bot and CI finding at its root cause in the PR`, English body with the operator's instruction and the four edits; attribution footer), CI green, Bot wait per the SKILL (this rule applies to this PR too), artifacts, the CompactionDB `memory add` of the decision line, then `AGMSG-RESULT v1 task_id=dotfiles-T122-codify-bot-ci-root-cause-a01` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=10.
