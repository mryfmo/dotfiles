---
format: 2
task_id: dotfiles-T128-v2-audit-schema-and-runner-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round4.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - schemas/audit.json
  - scripts/audit-head.sh
  - Makefile
  - AGENTS.md
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/unit/test_audit_head.py
  - tests/unit/test_agmsg_orchestration_docs.py
invariants:
  INV-5: "the task-level audit is a headless read-only run (codex exec --output-schema schemas/audit.json in a detached worktree at the head; fallback claude -p --json-schema --permission-mode plan limited to the worktree and the .orchestration directory) started when CI is green and the Codex Bot has reviewed the head or 15 minutes have passed without a Bot review (recorded as bot: none), at most once per RESULT head, pooled two at a time; the gate accepts an audit of an earlier head only when git diff --quiet <audited head> <HEAD> -- . ':!.orchestration' holds (an evidence-only revision), otherwise a new audit is required; its input includes the task's invariants and premises, the worker's evidence, the orchestrator's task file, amendments, acceptance record with its dispositions, the head's pr-feedback JSON and the previous round's audit JSON; the schema lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and the per-invariant map before the verdict, and the prompt asks for the rationale before each verdict; the runner, under the identity claude-audit-dot-h001 or codex-audit-dot-h001 on the orchestrator's host, records the JSON's sha256 in agmsg history (AGMSG-AUDIT v1 task_id= head= sha256= auditor=) before the gate reads it, an anchor that prevents edits after the record and not fabrication before it; the gate reads the verdict and categories from the JSON, and orchestration and conformance findings at P0-P2 accept only an operator waiver or a design reset, never not-applicable"
premises:
  - claim: "codex exec --output-schema is a strict server-side JSON schema and exec's approval policy is set with -c, not -a or --full-auto, on codex-cli 0.161.0"
    command: "codex exec --help | grep -E 'output-schema|sandbox'; codex exec --full-auto 2>&1 | head -1"
    output: "--output-schema <FILE>; -s, --sandbox <read-only|workspace-write|danger-full-access>; error: unexpected argument '--full-auto' found"
  - claim: "the current audit wrapper builds a prose prompt and reads the verdict by regex from the .last.md; PR 314's schema already lists the INV-5 field set"
    command: "grep -n 'Verdict: correct' home/dot_local/bin/common/executable_herdr-agents | head -2; git show origin/feat/audit-grammar:scripts/schemas/audit.json | head -30"
    output: "executable_herdr-agents:127 and :1946 match; the prose prompt is built at :1946 and run at :1954-1960, the verdict is read by regex (require-crit-review.py:30-31 AUDIT_VERDICT); audit.json: findings[], invariants{}, verdict, orchestration_findings"
  - claim: "the gate today requires the transcript <id>-audit-<sha7>.md to exist and reads the verdict from its .last.md companion, so the runner writes both plus the JSON until V2b"
    command: "grep -n 'audit' scripts/require-crit-review.py | sed -n '1,4p'; sed -n 636,657p scripts/require-crit-review.py | grep -c last"
    output: "audit_name_error and the .last.md read at lines 636-657"
  - claim: "check-regime-boundary.sh flags any identity registered under .claude/worktrees/ as a seated worker, so the audit identity joins, sends and leaves inside one run"
    command: "sed -n 100,103p scripts/check-regime-boundary.sh"
    output: "violations+=(\"worker still seated at ${worktree} (herdr-agents --remove-worker ${worktree})\")"
  - claim: "the SKILL's bounded Bot wait (15 minutes, then bot: none) is the existing rule the runner reuses"
    command: "grep -n '15 minutes' home/dot_agents/skills/agmsg-orchestration/SKILL.md | head -2"
    output: "Worker Playbook step 15: Repeat until a review of the final head appears or 15 minutes pass; the report records the latter as bot: none"
---

# AGMSG-TASK dotfiles-T128-v2-audit-schema-and-runner-a01 — regime v3 wave V2: schema-validated headless audit runner

DRAFT; dispatched after the T128 design accept, concurrently with V1 (file-disjoint since the V1 split: V1 touches no prose; the SKILL edit here is V2's alone). Known drift to record at acceptance: `executable_herdr-agents` (forbidden here) keeps advertising the old headless command until the wave that touches it. Implements T128 INV-5's runner side only; the gate's reading of the JSON is V2b. Design tier. Claude seat, `.claude/worktrees/worker-f`, branch `feat/audit-runner` from `origin/main`.

## Ponytail constraints (binding)

- Reuse PR #314's `scripts/schemas/audit.json` (`git show origin/feat/audit-grammar:scripts/schemas/audit.json`) moved to `schemas/audit.json`, reordered so `findings` and `invariants` precede `verdict`; its pre-push hardening (evidence staged only once masked; the `claude -p` fallback limited to the worktree and `.orchestration`) carried over. Do not reuse its 555-line `audit-head.sh`; write a runner under 120 lines around `codex exec`, `claude -p`, `git worktree add --detach`, `shasum`, `send.sh --body-file`. No daemon, no watcher: `make audit-head PR=<n> TASK=<id>` waits with `gh pr checks <n> --watch` and the SKILL's Bot list loop (15 minutes, `bot: none`), then runs the audit once for the head.
- Size caps: 15 files, 500 added lines outside tests/ and .orchestration/ (self-measure as in V1).
- One deterministic fact per round.

## What to build

1. `schemas/audit.json`: `findings[]` of `{priority: P0|P1|P2|P3, confidence: high|medium|low, category: specification|implementation|evidence|orchestration|conformance, path, line (integer or null), rationale}`, `invariants` object `INV-n -> {status: holds|violated|not_applicable, path, line}` (not_applicable refused for task invariants by the gate in V2b), `orchestration_findings` integer, `verdict: correct|incorrect|blocked`, `additionalProperties: false`; property order findings, invariants, orchestration_findings, verdict.
2. `scripts/audit-head.sh <head-sha> --task <id> [--pr <n>]`: refuse unless the main checkout has no tracked change (`git status --porcelain --untracked-files=no` empty; untracked `.orchestration` files are normal); `git worktree add --detach .claude/worktrees/audit-<sha7> <sha>` (an existing `audit-<sha7>` is reused only when `git -C <it> rev-parse HEAD` equals the full sha and `git status --porcelain --untracked-files=all` is empty, otherwise it is removed and recreated; at most two `audit-*` worktrees, otherwise exit 3 `pool full`); build the prompt from the main checkout's files: the task file and its amendments, `.orchestration/<id>/` on the head (worker evidence), `.orchestration/acceptance/<id>.md` and `.orchestration/validation/<id>-pr-feedback.json` when present, the previous audit JSON for the task when present, and `AGENTS.md`'s Audit section by reference; ask for reasoning in each `rationale` before the verdict; run `codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> exec --sandbox read-only -C <worktree> --output-schema schemas/audit.json -o <out>.json '<prompt>'` with `-c approval_policy=never`; on a nonzero exit or missing JSON run the fallback `claude <MODEL_PROFILE_AUDIT_CLAUDE_ARGS> -p --permission-mode plan --json-schema "$(cat schemas/audit.json)" --output-format json --max-budget-usd <process_tiers.<tier>.audit_budget_usd when the manifest has it, else the constant 5> --add-dir <worktree>` from inside the detached worktree, with `--bare` when `ANTHROPIC_API_KEY` is set and otherwise `--settings '{"disableAllHooks": true}'` (project and user hooks off; managed hooks stay and are harmless in a worktree under `.claude/worktrees/`, where the agmsg SessionStart skips and the Stop gate finds no identity), and extract `structured_output`; validate the JSON against the schema (`uv run --no-project --with jsonschema`); write three files under `.orchestration/validation/`: `<id>-audit-<sha7>.md` (the codex or claude transcript through `tee`, as the pane form does), `<id>-audit-<sha7>.md.last.md` (rendered from the JSON, last line `Verdict: <verdict>`; the gate reads this pair today, V2b switches it to the JSON) and `<id>-audit-<sha7>.json`; mask the three files with the repository masker first, then compute the JSON's sha256 from the masked file (the hash in history must equal the committed bytes); `AGMSG_RESOLVE_PROJECT=0 join.sh dotfiles-conformance <codex|claude>-audit-dot-h001 <type> <worktree>`, `send.sh dotfiles-conformance <that identity> claude-deep-dot --body-file <file>` with `AGMSG-AUDIT v1 task_id=<id> head=<sha> sha256=<json sha256> auditor=<codex|claude>`, then `leave.sh dotfiles-conformance <that identity>` (the sender name stays in history; no identity may remain under `.claude/worktrees/`, which `check-regime-boundary.sh` flags); remove the worktree; exit 0 on `correct`, 1 otherwise, 2 on `blocked`. shdoc header.
3. `Makefile`: `audit-head` target (`PR`, `TASK`, optional `HEAD`): `gh pr checks $(PR) --watch --fail-fast`, then the Bot loop from the SKILL (as a small shell block in the recipe or a 20-line helper inside `audit-head.sh --wait`), then `scripts/audit-head.sh`. No daemon.
4. `AGENTS.md` Audit section: replace the prose finding grammar with the schema reference (fields, five categories with one-line definitions), the auditor's standing over the orchestrator's artifacts (task wording, amendments, dispositions, acceptance claims are `orchestration`; process deviations `conformance`), the locks (orchestration/conformance at P0-P2 released only by an operator waiver or a design reset), rationale before verdict, and the `AGMSG-AUDIT` record. Keep the verdict line sentence for the rendered file.
5. SKILL task-level audit bullet: one headless form, `make audit-head PR=<n> TASK=<id>`; `tests/unit/test_agmsg_orchestration_docs.py` line 21's `HEADLESS_AUDIT` constant follows. No other SKILL section.
6. `tests/unit/test_audit_head.py` (stdlib `unittest`; bare `uv run python` cannot import jsonschema, so schema checks run through the runner or `uv run --no-project --with jsonschema` as a subprocess): schema accepts a good document and rejects a missing key, an unknown category, an invariant status outside the enum; with a fake `codex` that emits a valid document the runner writes the transcript, the `.last.md` and the JSON, joins, records the sha256 line (fake `join.sh`, `send.sh` and `leave.sh` capturing their arguments) and leaves, and exits by verdict; with a fake `codex` that fails, the fake `claude` fallback runs and the record names it; the pool refuses a third worktree; the worktree is detached at the sha; masking runs. Each fails when its rule is removed.

## Validation

the module under pytest; `shellcheck scripts/audit-head.sh`; `prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md`; the size measurement; `invariant: INV-5 → …` lines. The two real model runs are the orchestrator's after the PR is green (one `codex` run on your head, one with `codex` hidden from `PATH`), pasted into the acceptance record.

## First commit

Copy this task file to `.orchestration/dotfiles-T128-v2-audit-schema-and-runner-a01/task.md`; evidence files go under that directory on the branch.

## Completion

Draft PR within 30 minutes (`feat(audit): schema-validated headless audit runner with an agmsg record`), CI, Bot wait, artifacts, `memory add`, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=12. Forbidden: `scripts/require-crit-review.py`, `executable_herdr-agents`, anything else; `make update`; thread resolution; a second hand-written parser.
