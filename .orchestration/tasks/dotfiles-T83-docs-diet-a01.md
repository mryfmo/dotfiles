# AGMSG-TASK dotfiles-T83-docs-diet-a01

Drafted 2026-10-05 by the orchestrator seat from the approved correction plan (Phase 6, dotfiles-T83). Depends on T69, T77, T78, T81, T82 and T86 (all merged or in their final round). Prose-only; disjoint from T84 (manifest/generator) except README, where T84 adds one sentence in the herdr-agents section (prose rule: non-overlapping sections, the later PR updates its branch). Dispatch when T82 and T86 have merged.

## Objective

Principle 6: rules carry invariants, the SKILL carries procedure, every fact lives in one place, and the always-loaded text fits the budget.

1. **`home/dot_config/claude/rules/agmsg-orchestration.md` ≤ 450 words, invariants only:** activation (bus available or operator asks → invoke the `agmsg-orchestration` skill; opt-out only by the operator); every repository mutation goes to a seated worker whose kind is the manifest's (never write "Codex worker"); "no worker" is never an opt-out; acceptance, adversarial RESULT review and `make require-crit-review` are orchestrator-only; agent-to-agent permission approval is forbidden; `main` only through a PR merged by the orchestrator (REST merge after activation, `gh pr merge --squash` before); the Stop checklist is `make check-regime-boundary`; worker identities register at their worktree path; parallel tasks need pairwise-disjoint `allowed_files` (code files serial, prose sections concurrent); the seat-capability routing rule in one sentence with a pointer to the SKILL section. Everything procedural (seat lock, writable roots, wake paths, poke/send/inbox, audit lane, blocker evidence, pane-less start, GitHub-call exception, update-branch handling) moves to the SKILL, in sections the rule names.
2. **Always-loaded budget:** the eight Claude rule files under `home/dot_config/claude/rules/` total ≤ 1800 words (`wc -w`), achieved by the same move (procedure → SKILL or README) in `model-selection.md`, `pr-integration.md`, `crit-review.md`, `compactiondb.md`, `understand-anything.md`, `ponytail.md`, `ask-user-question.md`; keep the tokens the tests pin (`model_profiles`, `express-explorer`, `review`, `AGMSG_RESOLVE_PROJECT=0 join.sh <team> <name> <type> <worktree>`, `poke.sh`, `send.sh`, `--body-file`, `agmsg-dispatch`, `13 =`, `inbox.sh`, `gh pr merge --squash`).
3. **Facts in one place:** the audit command (pair: `herdr-agents --audit <sha> --task <id>`; headless: `codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md '<prompt>'`) appears once, in the SKILL's task-level audit bullet; `AGENTS.md` (Audit section), `README.md` (both mentions), `model-selection.md`, the rule and the SKILL's other mentions point there. The gate command appears once in SKILL step 10; `gh-first-workflow/SKILL.md` step 8 and the README PR-integration example become pointers (edit `tests/unit/test_pr_feedback.py` so it pins the pointer, not the literal). The Worker Playbook step 4 sandbox exception reads "until the worker gh credential is provisioned on this host (README operator phase, T90/T90b)" and names the three commands once.
4. **Session lessons into the SKILL:** reference lookups for VERIFY items use the WebFetch tool, not Bash `curl`; fetch and fast-forward inside the sandbox, push and `gh` through the exception; the orchestrator's update-branch order (CI → sweep → audit); Bot wait on the diff head only, waived for pure update-branch heads; artifact transfer from a Codex seat's worktree; the `audit-finding:` disposition line format and the "no deferral as a disposition" rule.
5. **Stop checklist:** add "review `uv run .claude/hooks/contextdb_cli.py memory candidates --limit 20`; `memory promote <id> --scope project` or leave" to the SKILL's Stop checklist; the README gains the "operator phase and `make update`" definition (T70) and a `codex-orchestrate` pointer in the regime section.
6. **Python invocation wording:** every `python3 .claude/hooks/contextdb_cli.py …` in `CLAUDE.md`, `AGENTS.md`, the SKILL, the rules and `home/dot_config/codex/AGENTS.md` becomes `uv run .claude/hooks/contextdb_cli.py …` (the enforce-uv hook now denies `python3`); keep `CLAUDE.md` a shim (`@AGENTS.md` + the CompactionDB block only).
7. **Dead prose:** remove the `plans/005-*` agent-fanout references and the `.gitignore` `.agents/runs/` line (T77 left them); decide the three nix plan documents (T78 notes): move them under `docs/history/` with their note or delete them, one sentence of rationale in the report.
8. **Tests (`tests/unit/test_agmsg_orchestration_docs.py`, `tests/unit/test_pr_feedback.py`):** the RULE test asserts the invariant phrases; the SKILL test asserts the mechanics tokens; forbidden phrases: the existing three + "Codex worker" (rule and SKILL only; `model-selection.md`'s security-profile sentence keeps its wording) + `audit review --commit` (rule, SKILL, README, AGENTS.md, model-selection.md); the word budgets (rule ≤ 450, eight rules ≤ 1800) are asserted.

Forbidden: any code outside the two test files; `home/dot_local/bin/**`; `scripts/**`; the manifest; hooks; permissions.

[memory:decision] dotfiles-T83 (operator 2026-10-03): the agmsg-orchestration rule holds only invariants (≤ 450 words) and the eight always-loaded Claude rules fit 1800 words; procedure lives in the SKILL, the audit and gate commands appear once, the Python entry points say `uv run`, and the Stop checklist reviews CompactionDB memory candidates.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c docs/rule-diet --no-track origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_config/claude/rules/*.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_agents/skills/gh-first-workflow/SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `home/dot_config/codex/AGENTS.md`, `plans/005-*.md`, `docs/plans/nix-*.md` (move or delete), `plans/004-harden-and-lock-the-supply-chain.md` (the note), `.gitignore` (the one line), `tests/unit/test_agmsg_orchestration_docs.py`, `tests/unit/test_pr_feedback.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T83-docs-diet-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
wc -w home/dot_config/claude/rules/agmsg-orchestration.md; cat home/dot_config/claude/rules/*.md | wc -w
grep -rn "audit review --commit" home README.md AGENTS.md; echo "rc=$?"
grep -rn "python3 .claude/hooks" CLAUDE.md AGENTS.md home/dot_agents/skills home/dot_config; echo "rc=$?"
uv run python -m unittest tests.unit.test_agmsg_orchestration_docs tests.unit.test_pr_feedback -v 2>&1 | tail -5
make unit-test 2>&1 | tail -3
make validate-agent-assets
mise x node npm:prettier -- prettier --check README.md AGENTS.md CLAUDE.md home/dot_config/claude/rules/*.md home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_agents/skills/gh-first-workflow/SKILL.md home/dot_config/codex/AGENTS.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: Bot wait per the SKILL (diff head only, timestamped); fix P0/P1 inline findings; do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `uv run .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` with the `[memory:decision]` text; paste command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T83` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=40.

## Dispatch

- 2026-10-05 11:25Z to `claude-standard-dot-a005` (worker-c, wT:p2) after T84 merged as 51c57f19; T69, T77, T78, T81, T82, T84, T85, T86 are on `main`. Branch from `origin/main` 51c57f19 or later with `--no-track`. Runs in parallel with T81b (a007, vendor tree + manifest pin + validator; disjoint from your files). Use `uv run` for every Python invocation (the enforce-uv hook denies `python3`). Re-measure the current word counts first and keep the per-file budgets in the report.
