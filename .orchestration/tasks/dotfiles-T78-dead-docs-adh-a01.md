# AGMSG-TASK dotfiles-T78-dead-docs-adh-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 4, dotfiles-T78; operator decision: ADH leaves dotfiles). Dispatch after T88 (PR #243, SKILL.md) has merged; the other files are disjoint from in-flight tasks.

## Objective

Principle 9: documents that nothing reads, and the ADH clauses the operator removed from this repository's scope.

1. **`AGENTS.md`**: delete the "ADH (autonomous-dev-harness)" section (lines 16-21). Nothing else in that file changes.
2. **`reviews/ADH_Integrated_Plan/**`**: delete the directory (it is the ADH V4 input baseline, no longer this repository's concern); drop the `"!reviews/**"` exclusion in `.coderabbit.yaml:11` if nothing else lives under `reviews/` afterwards (confirm with `git ls-files reviews`).
3. **Hermes / learn_index prose**: `home/dot_agents/skills/agmsg-orchestration/SKILL.md:3` (description), `:16` ("adopts only the Hermes Skill Subset ideas …"), `:174` (`learn_index.md`) and `:199` ("Do not install Hermes Agents runtime"); `home/dot_config/codex/AGENTS.md:9` (`learn_index.md` read step). Delete the Hermes references and the `learn_index.md` obligations; no `learn_index.md` exists in this repository (`git ls-files | grep learn_index` → confirm empty).
4. **`.github/copilot-instructions.md`**: delete (no tooling reads it here; Copilot is not part of the harness).
5. **`home/dot_claude/commands/commit.md`**: lines 19-118 duplicate the Conventional Commit rules in `home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md`; replace them with one pointer line to that file so the rules live in one place. `plans/README.md:18` likewise points to that file if it restates the rules.
6. Stale nix prose from T74 (`docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md`): add one dated note at the top of each saying the flake was removed in #247 and the commands below no longer apply; do not rewrite the bodies (T83 decides their fate).

Forbidden: rule files under `home/dot_config/claude/rules/`; `README.md`; the `adh` model profile and its validators (T79); any code.

[memory:decision] dotfiles-T78 (operator 2026-10-03): the ADH clauses and `reviews/ADH_Integrated_Plan/` leave dotfiles, the Hermes and `learn_index.md` references are deleted, `.github/copilot-instructions.md` is deleted, and the Conventional Commit rules live only in `gh-first-workflow/references/gh-git-rules.md`.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c chore/dead-docs-adh origin/main` (the commit that merged #243 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `AGENTS.md`, `reviews/**` (delete), `.coderabbit.yaml`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (the four lines named), `home/dot_config/codex/AGENTS.md` (line 9), `.github/copilot-instructions.md` (delete), `home/dot_claude/commands/commit.md`, `plans/README.md`, `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md` (one note each), `tests/unit/test_agmsg_orchestration_docs.py` (only if it pins the deleted phrases)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T78-dead-docs-adh-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -rln "Hermes\|learn_index\|ADH" AGENTS.md home/dot_agents/skills home/dot_config/codex ; echo "rc=$?"
test ! -d reviews/ADH_Integrated_Plan && echo "reviews gone"
test ! -f .github/copilot-instructions.md && echo "copilot gone"
grep -rl "Conventional Commit" --include='*.md' . | grep -v '^./.orchestration\|^./.agents\|^./.ua\|worktrees'
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check AGENTS.md home/dot_claude/commands/commit.md plans/README.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if Plan Mode was used.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T78` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## Dispatch

- 2026-10-05 02:00Z to `claude-standard-dot-a006` (worker-d, wY:p2) after its T77 acceptance. T88 (#243), T69 (#253) and T97 (#258) are on `main`; branch from the commit that merged #258 or later with `git switch -c chore/dead-docs-adh --no-track origin/main`. The SKILL.md line numbers in item 3 predate T69/T97; locate the four passages by their quoted text. T90 (Codex seat, in flight) edits SKILL.md's Orchestrator Playbook step 10 only; your item-3 passages are elsewhere, so the later PR takes `gh pr update-branch`. `tests/unit/test_agmsg_orchestration_docs.py` may pin the Hermes phrases; adjust only those assertions.

### PONG decision (orchestrator, 2026-10-05 02:15Z)

1. `.prettierignore` joins allowed_files for the one `reviews/` line: drop it together with the `.coderabbit.yaml` exclusion (both become dead with the directory).
2. `home/dot_config/codex/AGENTS.md`: delete the whole "セッション開始時の learn 確認" section (heading plus its three bullets) as the minimal coherent unit, as you proposed.
