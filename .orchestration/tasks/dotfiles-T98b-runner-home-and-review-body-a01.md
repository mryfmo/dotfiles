# AGMSG-TASK dotfiles-T98b-runner-home-and-review-body-a01

Drafted 2026-10-05 09:15Z by the orchestrator seat from two lessons of this session (boundary PR #279 first push failed CI; T98 round-1 audit). Kind: validator plus tests plus SKILL prose; no boundary source.

## Objective

1. **GitHub runner homes are machine-independent forms.** In `scripts/validate-agent-assets.py` (`compiled_home_path_pattern`), add `~` and `~` as forms that match anywhere (no leading boundary, like a multi-segment `$HOME`), so a workstation's masker rewrites a glued runner path (`..F~/.ssh/id`, as quoted from Actions logs or an auditor's example) exactly as the runner's own scan flags it, and the `.orchestration` scan on any machine flags it too. Keep every other form unchanged. Tests: `F~/.ssh/id` → `F~/.ssh/id` and `x~/y` → `x~/y` under `HOME=~`; `~/x` and `~/x` are ordinary account forms (boundary applies). Re-run the masker over tracked `.orchestration` files; commit a mechanical re-mask separately with verbatim output if anything changes (the #279 files were already masked under `HOME=~`, so probably nothing).
2. **Review-body findings.** The Codex Bot sometimes places a `P[0-3]` finding in the review body (with a blob link) instead of an inline thread (T98: review 5411302667). In `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: Worker Playbook step 15 lists review-body findings (a review whose body contains a P badge) alongside top-level inline comments and fixes or dispositions them the same way; Orchestrator Playbook step 10.4 says a `review` sweep item whose body carries a P badge is a finding with its own `fixed:`/`not-applicable:` disposition, never a container. Pin both sentences in `tests/unit/test_agmsg_orchestration_docs.py`. The rule file stays unedited (budget).
3. **Boundary step.** In the SKILL's boundary-commit bullet add one sentence: before the boundary commit, run the masker over the pending files and `make validate-agent-assets`; with item 1 in place no `HOME=~` re-run is needed, say so only if you remove an existing mention of it (none exists today).

Forbidden: changing `SECRET_PATTERN` or the credential scan; editing the rule file; touching `home/dot_local/bin/**`; `make update`/`apply`; thread resolution; local bats.

[memory:decision] dotfiles-T98b (orchestrator 2026-10-05): `~` and `~` are machine-independent anywhere-forms of the home-path masker and scan, and Bot review-body findings are swept and dispositioned like inline threads (Worker step 15, Orchestrator step 10.4).

## Repo / branch

- Work ONLY in your own worktree (worker-c). `git fetch origin`; `git switch -c fix/runner-home-and-review-body --no-track origin/main` (main at 58f7594f or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.

## Allowed files

- `scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `tests/unit/test_agmsg_orchestration_docs.py`, `.orchestration/**` only for a mechanical re-mask commit.
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T98b-runner-home-and-review-body-a01.md` (main checkout; mask them before RESULT).

## Validation commands (paste verbatim output)

```
git diff origin/main --stat | tail -5
uv run --no-project python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs 2>&1 | tail -3
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
HOME=~ UV_CACHE_DIR=$HOME/.cache/uv uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
wc -w home/dot_config/claude/rules/agmsg-orchestration.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```
(For the `HOME=~` line, substitute your real home for `$HOME` in `UV_CACHE_DIR` before running.)

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL (diff head only, timestamped; end on a quota notice and record it); fix P0/P1 findings, inline or review-body; do not resolve threads.
3. Artifacts at the exact expected paths, masked; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` with the `[memory:decision]` text; paste the command and the returned id.
5. `AGMSG-RESULT v1 task_id=dotfiles-T98b` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=25.

### PONG decision 1 (orchestrator, 2026-10-05 09:52Z) — audit of 70f060e7: two artifact corrections, no push

1. **Sandbox record (P2):** writing the five artifacts into the main checkout's `.orchestration/` and masking them ran outside the sandbox. From a worktree sandbox the main checkout is not writable, so a Claude seat has always done this through the permission gate, as the CompactionDB `memory add` already is in Worker Playbook step 4; the SKILL does not yet list the artifact writes. Correct the sandbox record to name that gated write as the reason (the same class as the documented `memory add` exception) rather than an undocumented action. The orchestrator records the SKILL gap as a follow-up for the next docs task.
2. **Report `cost:` line (P3):** replace "one commit, one CI round; about 10 turns" with `cost: n/a` (no observed token or cost figures); keep the commit/CI facts elsewhere in the report if you want them.

Edit only those two files, re-mask them, and answer with `AGMSG-PONG v1 task_id=dotfiles-T98b status=corrected …` (no new RESULT, no push).
