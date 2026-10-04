# Acceptance: dotfiles-T69-protocol-docs-unification-a01

- **Decision:** ACCEPTED. PR #253 squash-merged to `main` as `04bce61b`; final head `d9bbd800d2b87f4575fcd64d9791447cc84be35e`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, two dispositions below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 14:33Z).
- **Worker:** `claude-standard-dot-a006` (worker-d, wY:p2). task_rev verified at dispatch and at each revise round (the file grew by the round sections and addenda; the worker re-hashed it each time).
- **Exemption declared:** acceptance and final integration (thread resolution after fix verification, sweep, evidence, audit invocation, gate, merge, ACCEPTANCE).
- **Plan reference:** Phase 2, dotfiles-T69 (first principle of the program: the written protocol matches the practiced one). Depends on T64, T67, T68 (all merged) and carries the parallel-execution invariant text from T88.

## What was accepted (PR #253, final head `d9bbd800d2b87f4575fcd64d9791447cc84be35e`; 12 files, +89/−23)

- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: Worker Playbook gains the Bot wait after the final push (`gh pr checks --watch`, paginated `pulls/<n>/reviews` filtered to `user.type == "Bot"` and the final head, 15-minute cap, `bot: none` otherwise, P0/P1 fixed before RESULT); step 2 creates branches without `.git/config` writes (`--no-track`, push without `-u`, `gh pr create --head`); step 4 states the Claude-seat GitHub exception as the round-2 addendum words it (the domain allowance exists, `gh`/`git push` still fail inside the sandbox, T97 ends the exception) plus the two documented out-of-sandbox cases. Orchestrator Playbook step 10 is the acceptance order sweep → task-level audit of the final head (`herdr-agents --audit <sha> --task <id>`, headless `codex <audit profile args> exec --sandbox read-only …` otherwise, masker run from the trusted main checkout) → acceptance record with `audit-finding:` dispositions when `incorrect` → gate with `AUDIT_EVIDENCE` (and `AUDIT_DISPOSITIONS`) → merge → ACCEPTANCE; the per-commit pre-screen sentence is gone; the parallel-execution invariant (independent tasks dispatched together, ≤3 workers, pairwise-disjoint `allowed_files`, acceptance in arrival order, same-file tasks serial) is written in the SKILL and the rule.
- `home/dot_config/claude/rules/agmsg-orchestration.md`, `model-selection.md`, `pr-integration.md` (boundary-PR exception: thread replies and resolution instead of a sweep JSON, the next boundary commit names the PR), `AGENTS.md`, `home/dot_config/codex/AGENTS.md`, `README.md`, `gh-first-workflow/SKILL.md`: every `codex --profile audit review --commit` reference replaced by the SKILL pointer or the `--audit --task` form; `<task>-audit.md` → `<task>-audit-<sha7>.md`.
- `executable_herdr-agents`: the two stale stderr hints (1133 pane-less summary, 2159 no-workspace `--audit`) now point at the SKILL's headless form; string-only changes with their `tests/unit/test_herdr_agents.py` pins (ruff-formatted in d9bbd800).
- `tests/unit/test_agmsg_orchestration_docs.py`: parity strings for `--audit`, `--task`, `-audit-<sha7>.md`, `AUDIT_EVIDENCE`, the Bot-wait phrase and the parallel-execution clause in both the rule and the SKILL; asserts `review --commit` is absent from AGENTS.md, README.md, the rule, the SKILL and model-selection.md.

## Decisions taken during the rounds

- Round 1 (audit of d31dc32d `incorrect`, 1): Bot-wait phrasing and headless masker provenance; fixed in 4656f19f.
- Round 2 (audit of 4656f19f `incorrect`, 3): facts in one place (AGENTS.md, README audit sentences, model-selection.md, gh-first step 8 → pointers), T93 masked-evidence wording, Worker Playbook step 4 vs reality; fixed in 6b060ac4 and c2660469. Addendum 1 fixed the step-4 wording (allowance exists); addendum 2 added the Codex branch-creation sentence; both landed in fdb938ad.
- Round 3 (Codex P2 4177767259 and the audit of 6b060ac4 `incorrect`, 6): the second stale `herdr-agents` string (0b65a2ec + d9bbd800), exact final-head validation invocations with rc. Of the six round-2-head findings, two were already covered by fdb938ad, one was the orchestrator's own stale sweep snapshot (re-swept on the final head), one (gh-first step 8 keeps the gate literal) is accepted: `tests/unit/test_pr_feedback.py:407` pins that literal in both skills and is outside `allowed_files`; T83 consolidates.
- `gh-first-workflow/SKILL.md` step 8 and `README.md:952-958` keep a gate example next to their step-10 pointer; T83 (docs diet, facts in one place) owns their removal.

## Orchestrator re-derivation

- Read every round's diff (`git diff origin/main d9bbd800`, the fdb938ad and 0b65a2ec..d9bbd800 commits in full). Confirmed `grep -rn "review --commit" AGENTS.md README.md home/` is empty at the head, that both `herdr-agents` hints carry the SKILL pointer, that the SKILL step-4 text matches the addendum wording and that the step-2 sentence carries the three commands plus the `config.lock` note.
- Verified each of the 14 Codex threads' fix commit is an ancestor of d9bbd800 before resolving it (4e83dd8d ×4, 3c6a3cb2 ×3, d31dc32d ×3, 4656f19f ×3, 0b65a2ec ×1).
- CI green on d9bbd800 (13 checks; the docs-only diff skips the test matrix as designed); branch up to date with `main` 2ad504e3; no Bot review on the final head within the worker's window (14:00:25Z–14:15:25Z).

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, d31dc32d (round 1) | incorrect (1) → fixed in 4656f19f |
| task-level, 4656f19f (round 2) | incorrect (3) → fixed in 6b060ac4/c2660469/fdb938ad |
| task-level, 6b060ac4 (round 2 head) | incorrect (6) → two fixed in fdb938ad, one fixed in 0b65a2ec/d9bbd800, three dispositioned above |
| task-level, final head d9bbd800 | incorrect (2) → dispositions below |

audit-finding: 1 `README.md:956` repeats the gate's variable list instead of citing SKILL step 10 → not-applicable:task item 3 lists README:952 among the gate-command locations that must carry the audit variables, so updating the existing PR-integration example (which now also cites step 10 in its comment) is the specified change; round 2 scoped pointer replacement to the two audit sentences, and T83 owns removing worked examples
audit-finding: 2 the final-head validation block pipes `make …` through `tail` while claiming unpiped exit statuses and pastes TSV after a bare `--json` → not-applicable:evidence-presentation finding; the claimed results are corroborated independently by the final head's CI (Unit test and formatting jobs green on d9bbd800) and by the orchestrator's own reading of the diff, and the task's product files are unaffected

- Codex Bot: 14 threads over the PR's life, all fixed and resolved (see re-derivation); the last, 4177767259 on `herdr-agents:2159`, fixed in 0b65a2ec, replied (4178037606) and resolved by the orchestrator.
- Sweep (head d9bbd800): 52 items, 14 `fixed:<sha>` (4e83dd8d ×4, 3c6a3cb2 ×3, d31dc32d ×3, 4656f19f ×3, 0b65a2ec ×1), 38 `not-applicable` (5 Codex review containers, 14 orchestrator review containers, 14 orchestrator reply comments, 1 CodeRabbit summary, 1 CodeRabbit status, 3 macOS capacity notices). Masked copy: `.orchestration/validation/dotfiles-T69-protocol-docs-unification-a01-pr-feedback.json`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Follow-ups

- T97 (Codex a007): its two-sentence residual (step-4 sentence and rule bullet) is dispatched now that this PR has merged.
- T96 waits for T76 (shared `agent-config.yaml`/validator files); T78 waits for T97 (shared SKILL.md).
- T83 consolidates the remaining gate examples (gh-first step 8, README PR-integration block) and shrinks the rule.

## CompactionDB

- Worker decision: see the report's `[memory:decision]`; orchestrator consolidation `24ff13ec-0285-49d5-bb68-0053c9013c6f`.
