# WP-M: Require verbatim validation output in worker RESULT evidence

task_id: WP-M
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

## Background

During WP-L acceptance review, the first AGMSG-RESULT claimed a CompactionDB `memory add` had been executed and cited a decision ID that did not exist in the store; the claim was only corrected after a `status=revise` round. The operator approved hardening the task/worker contract so execution claims must be backed by pasted command output.

[memory:decision] Worker RESULT evidence must contain the verbatim output of every validation command actually executed; any identifier a report claims to have created must appear in that pasted output, and a claim without its pasted output is treated as unexecuted.

## Goal

Edit `home/dot_agents/skills/agmsg-orchestration/SKILL.md` with two minimal changes:

1. In the "Message Contract v1" section, insert the following paragraph immediately AFTER the paragraph beginning "RESULT reports must mark durable facts" (keep that paragraph unchanged):

```markdown
RESULT validation files must contain the verbatim output of every validation command actually executed — not summaries or PASS labels alone — and any identifier the report claims to have created (commit hash, PR number, CompactionDB memory/decision ID) must appear in that pasted output. A claim without its pasted output is treated as unexecuted and grounds for `status=revise`.
```

2. In the "Worker Playbook" section, replace step 6, currently exactly:

```markdown
6. Put command outputs and validation evidence in `expected_validation_file`.
```

with:

```markdown
6. Put the verbatim output of every validation command in `expected_validation_file`; every identifier your report claims to have created must appear in that output.
```

No other edits. Match surrounding formatting; do not re-wrap neighboring text.

## Git / PR workflow

Follow repo AGENTS.md: branch `chore/agmsg-validation-evidence` from up-to-date `main`, commit, push, open a PR in English (suggested title: `chore(skills): require verbatim validation output in worker RESULT evidence`). Check GitHub Actions CI; fix until green. Do not run bats locally. If the crit guard requires review, follow AGENTS.md "Agent Review Evidence".

## Allowed files (edit boundary)

home/dot_agents/skills/agmsg-orchestration/SKILL.md, plus your artifact paths, worklog files under .agents/worklog/codex/, and crit review evidence files if required.

## Forbidden actions

Merging the PR; chezmoi apply; editing any other file; dependency changes; running bats locally; touching rendered targets under `$HOME` outside the repo.

## Validation

Per the very rule this task introduces, `.orchestration/validation/WP-M.txt` must contain verbatim outputs of:

1. `git diff main -- home/dot_agents/skills/agmsg-orchestration/SKILL.md` (exactly the two specified changes)
2. `git status --porcelain` after commit
3. PR URL and CI check results (all green)
4. The CompactionDB command: `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] fact above>"` followed by a `memory search` showing the created record and its ID

## Expected artifacts

- report: .orchestration/reports/WP-M.md
- validation: .orchestration/validation/WP-M.txt
- sandbox: .orchestration/sandboxes/WP-M.md
- learning: .orchestration/learning/WP-M.md
- autoskill: .orchestration/autoskill/runs/WP-M.md (record "not-used" if unused)

## Done signal

AGMSG-RESULT v1 with status=ready_for_review (or blocked with report). max_turns=20. Include a `cost:` line in the report.
