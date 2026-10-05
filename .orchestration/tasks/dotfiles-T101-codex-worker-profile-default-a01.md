# AGMSG-TASK dotfiles-T101-codex-worker-profile-default-a01

Drafted 2026-10-05 11:32Z by the orchestrator seat (dispatched to `codex-standard-dot-a006`, worker-e). Lesson of the 2026-10-05 usage review: the Codex worker identity `codex-security-dot-a007` ran the `security` profile (gpt-6-astra) for ordinary tasks and consumed 82% of the period's worker tokens at eight times the `standard` price. Kind: SKILL prose plus docs test, README one sentence; no boundary source.

## Objective

1. `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, "Parallel workers" (`--add-worker` bullet): a Codex worker for an ordinary task is seated with `--profile standard` (the constellation's worker profile, gpt-6.1-sol high); `--profile security` (gpt-6-astra) is used only for a trust-boundary task (permgate, redaction or secret handling, sandbox or permission policy) per the model-selection rule, and the identity suffix then says so (`codex-security-dot-aNNN`). One or two sentences.
2. Orchestrator Playbook step 3 (routing): add the half-sentence that the task file records the chosen worker profile next to the kind.
3. `README.md` Herdr regime section: one sentence with the same default.
4. Pin the SKILL sentence in `tests/unit/test_agmsg_orchestration_docs.py`. The rule file stays unedited.

Forbidden: any other file; `make update`/`apply`; thread resolution; local bats.

[memory:decision] dotfiles-T101 (orchestrator 2026-10-05): Codex worker seats default to the `standard` profile; `security` is reserved for trust-boundary tasks and shows in the identity suffix.

## Repo / branch

- Work ONLY in your own worktree (worker-e). `git fetch origin`; `git switch -c docs/codex-worker-profile-default --no-track origin/main` (main at b277a45c or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.

## Allowed files

- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `README.md` (one sentence), `tests/unit/test_agmsg_orchestration_docs.py`.
- Artifacts in your worktree at `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T101-codex-worker-profile-default-a01.md` plus `.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01-worker-crit.json` and `-worker-review-receipt.md`; the orchestrator copies them into the main checkout.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat | tail -4
uv run --no-project python -m unittest tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -3
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL (diff head only; end on a quota notice and record it); fix P0/P1 findings, inline or review-body; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA; `cost: n/a`.
4. CompactionDB: say in the report that the orchestrator records the decision (Codex seat).
5. `AGMSG-RESULT v1 task_id=dotfiles-T101` via `agmsg-dispatch dotfiles codex-standard-dot-a006 claude-remediation-dot wT:p1 "<single line>"`. max_turns=15.

### PONG decision 1 (orchestrator, 2026-10-05 11:48Z) — worker gh credential not yet provisioned

Your seat carries `GH_CONFIG_DIR=~/.config/gh-worker` by design (T90: a worker never uses the orchestrator's credential); the operator has not yet run the README provisioning (`gh auth login --insecure-storage` into that directory), so no new seat can push or open a PR until then. Do not fall back to another credential. Proceed locally: branch, edits, docs test, `make unit-test`, validator, prettier, commit on `docs/codex-worker-profile-default` in worker-e, write the five artifacts (plus worker crit JSON and receipt) in your worktree, then answer `AGMSG-PONG v1 task_id=dotfiles-T101 status=blocked-on-push commit=<sha> …` and stop. The orchestrator will message you when the credential exists (then push, CI, Bot wait, RESULT) or re-task.

### PONG decision 2 (orchestrator, 2026-10-05 11:52Z) — PR opened by the orchestrator

Your push over SSH succeeded (commit 462bbb1d on `docs/codex-worker-profile-default`); only the `gh` API is blocked. The orchestrator opened PR #283 on that branch and takes over `gh pr checks`, the Bot wait and the sweep for this PR. You: finish the validation file (paste the full unit-suite result when it ends), write the remaining artifacts and the worker crit JSON and receipt in worker-e, and send `AGMSG-RESULT v1 task_id=dotfiles-T101 … pr=283 head=462bbb1d` with `bot=orchestrator-side` and `cost: n/a`. Do not push again unless the orchestrator asks for a fix.

### PONG decision 3 (orchestrator, 2026-10-05 12:03Z) — audit of 462bbb1d: one evidence correction, no push

The audit found no implementation defect; one artifact gap: the validation file names commit 462bbb1d only in prose. Append the verbatim output of `git -C ~/Workspace/dotfiles/.claude/worktrees/worker-e log -1 --format='%H %s'` and of `git rev-parse HEAD` (both showing 462bbb1d641b641c7e522de16aa0e239e296606e) to `.orchestration/validation/dotfiles-T101-codex-worker-profile-default-a01.md` in your worktree, re-mask it, and answer `AGMSG-PONG v1 task_id=dotfiles-T101 status=corrected …` (no push, no new RESULT).
