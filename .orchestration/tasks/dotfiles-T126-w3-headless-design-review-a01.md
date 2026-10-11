---
format: 2
task_id: dotfiles-T126-w3-headless-design-review-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round4.md
  design: .orchestration/tasks/dotfiles-T126-regime-v2-a01.md
allowed_files:
  - scripts/design-review.sh
  - schemas/design-review.json
  - scripts/validate-task.py
  - tests/unit/test_design_review.py
  - tests/unit/test_validate_task.py
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - home/dot_config/claude/rules/agmsg-orchestration.md
  - home/dot_config/claude/rules/pr-integration.md
  - home/dot_config/claude/rules/model-selection.md
  - AGENTS.md
  - README.md
invariants:
  INV-2: "a design-tier task is dispatched only after a design review by a non-orchestrator -review- identity whose AGMSG-RESULT in agmsg history precedes the implementing TASK and carries the receipt path, the receipt file's sha256 and the canonical hash of the design keys; the gate compares all three; the receipt (markdown form of the T124 validator, or the JSON schema once W3 migrates the validator, both accepted) has every invariant accepted"
  INV-3: "a worker runs the validator at task start, writes the invariant tests before the implementation (checked by commit order: the first commit on the branch touches tests/), and is warned by its own Stop hook when 30 minutes pass after the TASK without a push; the validation file names, per invariant, the test and the file:line"
---

# AGMSG-TASK dotfiles-T126-w3-headless-design-review-a01 — T126 W3: the headless design review and the playbook text

Drafted 2026-10-10 by the orchestrator seat. Dispatched after W1 (PR #313) merges (the validator and the SKILL's task-authoring sections land there). Implements T126 INV-2's tooling and the playbook text of INV-3 and INV-6, and absorbs T124 wave 1b's prose items and T122. Read the T126 design and its three review receipts first; then the T124 receipts, which are the markdown form this task keeps accepting.

## What to build

1. `schemas/design-review.json`: `{design: string (path@sha256), reviewer: string, profile: string, reviewed_at: string, invariants: {INV-n: {verdict: accepted|rejected, reason: string}}, failure_modes_still_passing: [string], enforcement_points: [{invariant: string, earliest_mandatory: boolean, note: string}], document_findings: [string], verdict: accept|revise|reject}`, `additionalProperties: false`, `required` on every key.
2. `scripts/design-review.sh <design task file> [--runtime claude|codex] [--budget-usd N] [--out <receipt path>]`: creates a detached worktree at `origin/main` under `.claude/worktrees/review-<task id>` (the regime's hooks skip that path); joins agmsg as `claude-review-dot-h001` or `codex-review-dot-h001` at that worktree with `AGMSG_RESOLVE_PROJECT=0 join.sh` (reusing the identity when it exists); runs `claude -p --permission-mode plan --output-format json --json-schema schemas/design-review.json --max-budget-usd <N, default 3>` (with `--bare` when `ANTHROPIC_API_KEY` is set, otherwise without it under the managed hooks) or `codex exec --sandbox read-only --profile review --output-schema schemas/design-review.json --output-last-message <file>` with a prompt built from the design file, the T126 review questions (per-invariant verdicts, failure modes, earliest enforcement points, document findings) and the instruction to flag only findings that affect correctness or the stated invariants (the Claude Code best-practices caution against reviewer over-reporting); validates the output against the schema (`uv run --with jsonschema` or a stdlib check if jsonschema is unavailable offline); computes the canonical design hash with the validator's function; writes the receipt as JSON at `.orchestration/validation/<design task id>-design-review-<n>.json` plus a markdown rendering `…-design-review-<n>.md` in the T124 form; sends `AGMSG-RESULT v1 task_id=<design task id>-review status=ready_for_review verdict=<v> receipt=<json path> receipt_sha256=<sha256> design_hash=<canonical> runtime=<claude|codex> cost_usd=<from the JSON>` with `send.sh --body-file` to the orchestrator identity; exits 0 on `accept`, 1 on `revise`, 2 on `reject`, 3 on a schema or runtime failure. The orchestrator stays the one who dispatches the implementing TASK; the script never does.
3. `scripts/validate-task.py`: accept both receipt forms for `design_review.receipt` (the markdown form of W1 and the JSON form above): for JSON, `design` must end in the canonical hash, `reviewer` must not be the orchestrator identity, every invariant `accepted`, `verdict: accept`.
4. Playbook text (SKILL): Orchestrator Playbook step for the design gate (`design-review.sh` before any design-tier dispatch; the RESULT fields the gate will check in W5); Worker Playbook step 1 (validator at start), step 4 (the documented push form `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles <branch>`, the T119 sandbox example, the sandbox record's `permission_gated_commands: <n>` line), step 11 (the message contract gains `AGMSG-PONG v1 status=question`, counted by INV-6, and `AGMSG-AUDIT v1`), step 15 (the Bot/CI root-cause rule: every finding fixed at its root in the PR, `not-applicable` only for a factually wrong finding with the refuting command and output pasted, out of scope is a scope gap), Orchestrator step 10 (the orchestrator verifies a proposed `not-applicable` by its own reproduction per named sub-case and alone replies on and resolves threads; the boundary-commit lesson: never append to an `.orchestration` file `git status` shows absent, pull right after the boundary merge); `home/dot_config/claude/rules/agmsg-orchestration.md` (one line each for the design gate and the message contract), `pr-integration.md` (the not-applicable sentence), `model-selection.md` (the redesign-seat sentence and the corrected cache sentence: a model switch invalidates the prompt cache, an effort change keeps it on Fable 5.1; the `redesign` profile itself is W8), `AGENTS.md` "Agent Review Evidence" (one pointer sentence), README (one paragraph).
5. Tests: `tests/unit/test_design_review.py` with fakes for `claude`/`codex`/`join.sh`/`send.sh`: a good run writes both receipt forms, sends the RESULT with the three anchors and exits 0; a schema-invalid output exits 3 and sends nothing; `revise` exits 1; the identity is never the orchestrator's; the worktree is detached at `origin/main`; `--bare` only with the key. `tests/unit/test_validate_task.py`: both receipt forms accepted, a JSON receipt with a `rejected` invariant or a stale hash refused. Each fails when its rule is removed.

Forbidden: anything else; `scripts/require-crit-review.py`; `agent-stop-gate.sh`; `make update`; thread resolution. The standing Bot/CI rule and the sandbox conduct apply.

## Repo / branch

`.claude/worktrees/worker-c` (or whichever seat is free) after W1 merged: `git fetch origin`; `git switch -c feat/headless-design-review --no-track origin/main`. Push within 30 minutes of the TASK (a draft PR is enough); the first commit touches `tests/`.

## Completion

PR to `main` (English title `feat(regime): headless schema-validated design reviews, and the playbook text for the regime v2 gates`), CI green, Bot wait, worker artifacts under `.orchestration/<task id>/` committed on the branch before the final RESULT (INV-8 of T126 applies from this wave on), `invariant: INV-2 → …` and `invariant: INV-3 → …` lines in the validation, memory add with the command and output pasted, `AGMSG-RESULT v1 task_id=dotfiles-T126-w3-headless-design-review-a01`. max_turns=14.
