# AGMSG-TASK dotfiles-T98c-claude-seat-artifact-write-exception-a01

Drafted 2026-10-05 09:56Z by the orchestrator seat from the T98b audit finding 1. Kind: SKILL prose plus its docs test; no boundary source.

## Objective

A Claude worker seat's worktree sandbox cannot write the main checkout's `.orchestration/`, so writing its five artifacts there and masking them has always gone through the permission gate, while Worker Playbook step 4 lists only `gh`/`git push`/authenticated `git fetch`, `agmsg-dispatch` and the main-checkout CompactionDB `memory add` as gated exceptions. Make the artifact write an explicitly documented exception of the same class:

1. In `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, Worker Playbook step 4 ("Two documented cases run outside the sandbox too: …"): extend to three cases, adding "writing the task's artifacts at their expected main-checkout paths and masking them with the repository masker, because the main checkout is not writable from a worktree sandbox". Step 5 (artifact paths) gets a half-sentence cross-reference ("a Claude seat writes them through the permission gate, step 4"). Keep the Codex-seat convention (write in the worktree, orchestrator copies) unchanged.
2. Pin the new sentence in `tests/unit/test_agmsg_orchestration_docs.py` (`test_skill_carries_the_session_lessons` or the step-4 group).
3. No other change. The rule file stays unedited (429/450 words).

Forbidden: any file other than the two above; `make update`/`apply`; thread resolution; local bats.

[memory:decision] dotfiles-T98c (orchestrator 2026-10-05): a Claude worker seat writes and masks its main-checkout artifacts through the permission gate as a documented Worker Playbook step 4 exception, the same class as the CompactionDB memory add.

## Repo / branch

- Work ONLY in your own worktree (worker-c). `git fetch origin`; `git switch -c docs/claude-seat-artifact-write-exception --no-track origin/main` (main at 7f5b9b9d or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.

## Allowed files

- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `tests/unit/test_agmsg_orchestration_docs.py`.
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T98c-claude-seat-artifact-write-exception-a01.md` (main checkout, through the gate as the exception you are documenting; mask them before RESULT; `cost: n/a`).

## Validation commands (paste verbatim output)

```
git diff origin/main --stat | tail -4
uv run --no-project python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
wc -w home/dot_config/claude/rules/agmsg-orchestration.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL (diff head only, timestamped; end on a quota notice and record it); fix P0/P1 findings, inline or review-body; do not resolve threads.
3. Artifacts at the exact expected paths, masked; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` with the `[memory:decision]` text; paste the command and the returned id.
5. `AGMSG-RESULT v1 task_id=dotfiles-T98c` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"`. `cost: n/a`. max_turns=15.

### PONG decision 1 (orchestrator, 2026-10-05 10:09Z) — audit of d1751647: two artifact corrections, no push

1. **Sandbox record line 3 (P2):** it says Ruff ran, but the validation file has no Ruff command or output. Either paste the verbatim `ruff` command and output into the validation file (re-run it on the head if the original output is gone) or remove the claim.
2. **Report line 7 (P3):** the Codex quota notice was posted at `09:54:09Z`; `09:54:14Z` is CodeRabbit's comment. Correct the timestamp.

Edit only those files, re-mask them, and answer with `AGMSG-PONG v1 task_id=dotfiles-T98c status=corrected …` (no new RESULT, no push).
