# Acceptance: dotfiles-T111-project-map-subagent-a01

- **Decision:** ACCEPTED. PR #299 squash-merged to `main` as `cf557f25` (2026-10-07 01:00Z) with `gh pr merge 299 --squash --match-head-commit 2e15d4aa…`; head `2e15d4aa` (round 2). Gate passed at that head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 00:59Z). Earlier: REVISE ROUND 2 dispatched 2026-10-07 00:23Z (round-1 audit: the rendered agent body still limited writes to `.project-map/` and `.gitignore`). Earlier: REVISE ROUND 1 dispatched 2026-10-06 23:47Z (round-0 audit: SKILL.md write boundary vs. style memory; prototype evidence paste; two findings dispositioned by the orchestrator). RESULT received 2026-10-06 23:41Z (PR #299, head `0c1d280b`), round 1 at 00:19Z (`32e7742a`), round 2 at 00:54Z (`2e15d4aa`).
- **Worker:** `claude-standard-dot-a005` (worker-c, re-seated by `herdr-agents --restart-worker` at w1A:p2 after the previous pane wT:p2 had gone). PING/PONG before dispatch (22:51Z/22:52Z).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping; the pane-repair control-plane commands (`herdr-agents --attach`, `--restart-worker`).
- **Origin:** operator request (chat, 2026-10-07): a `project-map` subagent that draws one double-click HTML project map, built only from mechanisms the repository already has. The operator rejected, in turn, a hand-written `~/.claude/agents/*.md`, a new `home/dot_agents/subagents/` body directory, and a new `map` model profile ("dotfilesの構成のまま"; "model_profiles は変更しません"), and decided that `model_profiles.review.claude` becomes `claude-fable-5-1 / high`.

## What is under acceptance (PR #299, head `2e15d4aa`)

- `home/dot_agents/agent-config.yaml`: `review.claude` is `claude-fable-5-1 / high`; nothing else changes. Rendered into `model-profiles.env`.
- `scripts/generate-agent-configs.py`: `render_claude_project_map_agent()` borrows `model_profiles.standard.claude` and renders `home/dot_claude/agents/project-map.md` (memory: user; skills project-map, dataviz, artifact-design; tools Read/Glob/Grep/Bash/Write/Edit; body naming the three permitted writes). Test assertions added.
- Shared skill `home/dot_agents/skills/project-map/` (SKILL.md, agents/openai.yaml) with the generator's symlink templates under `home/dot_claude/skills/project-map/`.
- Rule `home/dot_config/claude/rules/project-map.md` with `home/dot_claude/rules/symlink_project-map.md.tmpl`; README generated-outputs line; `.gitignore` `.project-map/`.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, 0c1d280b (round-0 head) | incorrect (4): P2 `symlink_openai.yaml.tmpl` outside the allowlist; P2 `dataviz`/`artifact-design` not in the repository; P2 SKILL.md write boundary forbids the style-memory save; P3 prototype claims without pasted output → findings 1–2 dispositioned below, 3–4 → revise round 1 |
| task-level, 32e7742a (round-1 head) | incorrect (1): P2 the rendered agent body still limits writes to `.project-map/` and `.gitignore` → revise round 2 |
| task-level, 2e15d4aa (round-2 head) | correct (no findings; all 13 paths within the amended allowlist, artifacts present, evidence matches the final head). The `herdr-agents --audit` wrapper refused its masking step because the main checkout sat, by the orchestrator's error, detached at the audited commit (reflog 09:55 JST); the orchestrator restored `main` (8e9bd072, validator unchanged) and ran `validate-agent-assets.py --mask-secrets` on both audit files from that trusted checkout. |

audit-finding: 1 (0c1d280b) `home/dot_claude/skills/project-map/agents/symlink_openai.yaml.tmpl` committed outside `allowed_files` → not-applicable:the generator's `claude_skill_symlink_outputs()` mirrors every file of a shared skill, so this template is the output of the allowed `agents/openai.yaml` (gh-first-workflow carries the same file); the task's allowlist was amended in revise round 1 and the round-2 audit confirms all paths within it
audit-finding: 2 (0c1d280b) `dataviz` and `artifact-design` declared as preloaded skills but absent from the repository → not-applicable:both are Claude Code bundled skills, not repository files; the orchestrator's diagnostic run of the installed `project-map` agent showed both present in its context, loaded from `/tmp/claude-1000/bundled-skills/2.1.292/…`
audit-finding: 3 (0c1d280b) SKILL.md write boundary forbids the MEMORY.md style save → fixed:32e7742a (memory-write bullet; artifact-design precedence sentence), re-audited at 32e7742a and 2e15d4aa
audit-finding: 4 (0c1d280b) prototype claims in the report lack pasted output → fixed:32e7742a (validation file "Item 4" section: stat, sed, MEMORY.md, PR-body grep, NEED_STYLE/style.md grep, memory directory listing), re-audited
audit-finding: 5 (32e7742a) rendered agent body still limits writes to `.project-map/` and `.gitignore` → fixed:2e15d4aa (renderer body names the three permitted writes; regenerated), re-audited at 2e15d4aa with `Verdict: correct`

- Sweep (re-run at every head; final at 2e15d4aa): `.orchestration/validation/dotfiles-T111-project-map-subagent-a01-pr-feedback.json`, 7 items, all `not-applicable`: Codex quota notice; Codex review summary of the security review of 8c9e85e7 (completed, no finding; no Codex review ran on the later heads); CodeRabbit skip summary and status; 3 macOS runner capacity notices. No review thread on the PR. Crit evidence `…-crit.json` (3 orchestrator review records) / `…-review-receipt.md`; worker-side `…-worker-crit.json` (3 P3, approve) / `…-worker-review-receipt.md`.

## Notes for the operator

- The skill appends `.project-map/` to a repository's tracked `.gitignore` when missing (operator's verbatim design; the worker flagged it as a P3 design note). The canonical clone's uncommitted draft chose the global git ignore (`home/dot_config/git/ignore`) instead.
- The canonical clone `~/.local/share/chezmoi` holds an uncommitted parallel draft of project-map (a `map` profile, four untracked files, `effort: medium`, `NEED_STYLE`, `frontend-design` preload) that was already applied to the host at 07:51/08:14 JST. The orchestrator did not touch it. `make update` there needs the draft removed first; the pending `make upgrade` pins travel separately as a worker PR.
- After `chezmoi apply`, the first `project-map` run may answer `STYLE-NEEDED` once, because the prototype's memory stores the style in `style.md` rather than as `style:`/`accent:` keys.

## Parallelism

- Single task, single worker; no wave table.

## CompactionDB

- Worker decisions `133c2f01-1b73-4238-8cd6-78640b67843e` and `7727698a-48d8-406d-84c4-29833f1f5364` (main checkout, by a005). Orchestrator consolidation `9b9dedc4-0b23-4e85-80e4-0d5df737cec8`.

cost: n/a
