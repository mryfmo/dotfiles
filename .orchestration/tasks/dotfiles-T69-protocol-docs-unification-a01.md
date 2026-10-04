# AGMSG-TASK dotfiles-T69-protocol-docs-unification-a01

Drafted 2026-10-04 by the orchestrator seat from the approved correction plan (Phase 2, dotfiles-T69). Depends on T64 (merged a575b3cc), T67 (57885db1), T68 (PR #246) and T88 (PR #243: parallel rule and SKILL step 14). Dispatch only after #246 and #243 are both merged, to the worker that holds neither branch dirty. Line numbers below are from `main` 138e6a72 and shift after those merges; locate by text.

## Objective

Make the written protocol match what the tooling does after T64/T67/T68, with every fact in one place and the two docs tests pinning parity.

1. **Audit command is `herdr-agents --audit <sha> --task <id>`.** `codex --profile audit review --commit <sha>` is still named in `AGENTS.md:55`, `README.md:292` and `:559`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md:22` and `:65`, `home/dot_config/claude/rules/agmsg-orchestration.md:8`, `home/dot_config/claude/rules/model-selection.md:3`; `README.md:784` already explains why `review --commit` is not used. Name the pair form once in the SKILL (`herdr-agents --audit <head-sha> --task <id> [--out …] <main DIR>`, output `.orchestration/validation/<id>-audit-<sha7>.md`, verdict in `.last.md`) and the headless form once beside it (`codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <repo> -o <out>.last.md '<prompt>'`); every other location points to that SKILL section instead of restating the command. The stderr string in `home/dot_local/bin/common/executable_herdr-agents:1133` changes the same way (string only; no code).
2. **One audit per task on the final head.** Delete the per-commit pre-screen sentences (`SKILL.md:65`, rule `agmsg-orchestration.md:9`); say that a task-level audit of the final head covers the whole PR diff (`git diff <merge-base> <head>`), that a new push needs a new audit, and that the orchestrator dispositions every `[P0-P3]` finding in the acceptance record (`fixed:<sha>` needs a fresh audit of that sha; `not-applicable:<reason ≥ 20 chars>` is checked by the gate, T68).
3. **Gate command with audit evidence** (the T68 thread 4175981346 locations): root `AGENTS.md:51`, `SKILL.md:137` (Orchestrator Playbook step 10), `home/dot_agents/skills/gh-first-workflow/SKILL.md:26`, the `Makefile` comment above `require-crit-review`, `README.md:339-347` and `:952`, `home/dot_config/codex/AGENTS.md:33-35` all show the gate without `AUDIT_EVIDENCE`. Step 10 becomes the single procedure: `scripts/pr-feedback.py` sweep → `herdr-agents --audit <head> --task <id>` → acceptance record (with `audit-finding:` dispositions when the verdict is `incorrect`) → `BASE=origin/main PR_FEEDBACK_EVIDENCE=… AUDIT_EVIDENCE=… [AUDIT_DISPOSITIONS=…] AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` → `gh pr merge --squash` → `AGMSG-ACCEPTANCE`; the other locations cite step 10 and the pr-integration rule rather than repeating the variable list.
4. **Worker Bot-wait procedure** (Worker Playbook, after the final push): `gh pr checks <pr> --watch`; then list `gh api repos/{owner}/{repo}/pulls/<n>/reviews --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'` and the top-level `pulls/<n>/comments` rows (`in_reply_to_id == null`) until a review of the final head appears or 15 minutes pass (`bot: none` in the report); a 👍 reaction alone is not evidence of a review; fix P0/P1 inline findings with a fix commit and start over; the RESULT names every unresolved thread id with `fixed:<sha>` or a proposed `not-applicable:<reason>`; the worker resolves no thread. (VERIFY the REST field names against the GitHub docs and paste.)
5. **Boundary PR** (`orchestration/boundary-<date>[-n]`, merged with `gh pr merge --squash --auto`): the agmsg-orchestration rule already describes it; add one line to `home/dot_config/claude/rules/pr-integration.md` saying that a boundary PR needs no sweep JSON and no audit, that each Bot thread on it receives a disposition reply and is resolved, and that the next boundary commit message names the PR; mirror the same line in `home/dot_config/codex/AGENTS.md` "PR 統合".
6. **Tests:** `tests/unit/test_agmsg_orchestration_docs.py` gains parity strings for items 1-4 (`--audit`, `--task`, `-audit-<sha7>.md`, `AUDIT_EVIDENCE`, `in_reply_to_id`, the Bot-wait phrase) in both the rule and the SKILL, and asserts `review --commit` is absent from `AGENTS.md`, `README.md`, the rule, the SKILL and `model-selection.md` (except `README.md:784`'s explanatory sentence, if it survives, which may say `codex review --commit` is not used). Keep the `model_profiles` / `express-explorer` / `review` tokens in `model-selection.md:3` intact.

Forbidden: any code change other than the one stderr string in `executable_herdr-agents`; `scripts/require-crit-review.py`; `README.md` beyond the lines named above (T83 owns the diet); the parallel-execution and step-14 text T88 just landed (cite, do not rewrite).

[memory:decision] dotfiles-T69 (operator 2026-10-03): the written protocol names one audit per task on the final head via `herdr-agents --audit <sha> --task <id>` (headless `codex … exec --sandbox read-only` otherwise), the acceptance order sweep → audit → acceptance record → gate with `AUDIT_EVIDENCE` → merge → ACCEPTANCE, the worker's Bot-wait by listing reviews of the final head, and the boundary PR as a sweep-free, audit-free exception; `codex --profile audit review --commit` is no longer written anywhere.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c docs/protocol-unification origin/main` (the commit that merged #246 and #243, or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md`, `home/dot_config/claude/rules/model-selection.md`, `home/dot_config/claude/rules/pr-integration.md`, `AGENTS.md`, `README.md` (named lines), `home/dot_config/codex/AGENTS.md`, `home/dot_agents/skills/gh-first-workflow/SKILL.md`, `Makefile` (comment only), `home/dot_local/bin/common/executable_herdr-agents` (the one string), `tests/unit/test_agmsg_orchestration_docs.py`, `tests/unit/test_herdr_agents.py` (only if the string is pinned)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T69-protocol-docs-unification-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
grep -rn "review --commit" AGENTS.md README.md home/dot_config home/dot_agents home/dot_local/bin/common/executable_herdr-agents Makefile ; echo "rc=$?"
grep -rln "AUDIT_EVIDENCE" AGENTS.md README.md Makefile home/dot_agents/skills home/dot_config
uv run python -m unittest tests.unit.test_agmsg_orchestration_docs tests.unit.test_herdr_agents 2>&1 | tail -3
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check README.md AGENTS.md home/dot_config/claude/rules/*.md home/dot_agents/skills/agmsg-orchestration/SKILL.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push, follow item 4 yourself (it is the procedure you are writing); close your crit server if Plan Mode opened one (`crit stop`, confirm with `pgrep -fl 'crit _serve'`, report `crit-cleanup-pending=<pid>` if one survives); do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## Dispatch

- 2026-10-04 14:20Z to `claude-standard-dot-a006` (worker-d, wY:p2) after its T88 acceptance (PR #243 merged as febd0cb7; T68 merged as f32f33a0). Branch from `origin/main` febd0cb7 or later; keep the earlier branches untouched. Line numbers in the task predate T88 and T68: locate by text. The T88 rule/SKILL text (parallel execution, routing by boundary, step 14) is cited, never rewritten. Also fold in: the acceptance order now includes the task-level audit after every `gh pr update-branch`, `audit-finding:` lines start at column one, and evidence JSON may be masked (T93, pending) — write what main has at your branch point and name T93 if it has not merged.

## Revise round 1 (orchestrator, 2026-10-04 16:40Z) — task-level audit of d31dc32d is `incorrect`

1. **P2, headless audit command.** The SKILL's headless form keeps an old `<out>.last.md` and loses codex's exit status through `tee`, so a failed rerun could present an earlier `Verdict: correct`. Write it the way the pair implementation behaves: `rm -f <out> <out>.last.md` first, run with `set -o pipefail` (or capture codex's status with `${PIPESTATUS[0]}`), treat a non-zero codex exit as "no audit" (nothing to gate; rerun), and only then mask both files. One bullet.

One commit; `gh pr update-branch 253` if `main` moved (c6b348ba now); CI; Bot (paginated listing per your own step 15); RESULT. Standing directive applies.
