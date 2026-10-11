---
format: 2
task_id: dotfiles-T124-wave3b-audit-grammar-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round4.md
  design: .orchestration/tasks/dotfiles-T126-regime-v2-a01.md
allowed_files:
  - home/dot_local/bin/common/executable_herdr-agents
  - AGENTS.md
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - tests/unit/test_herdr_agents_audit.py
  - scripts/audit-head.sh
  - scripts/schemas/audit.json
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/unit/test_herdr_agents.py
  - README.md
invariants:
  INV-4: "the task-level audit is a headless, read-only, schema-validated run (codex exec --output-schema in a detached worktree; the fallback claude -p --json-schema runs with --bare and an API key, or, without one, under the managed hooks, which W2 shows harmless in a detached worktree) started automatically when CI is green on a pushed head and a Codex Bot review of that head exists, at most once per RESULT head; its JSON lists findings {priority, confidence, category in {specification, implementation, evidence, orchestration, conformance}, path, line, rationale} and a per-invariant map {holds|violated|not_applicable, path:line}; the orchestrator's task file, amendments, acceptance record and dispositions are in its input set; the runner records the JSON's sha256 in agmsg history under an audit identity (AGMSG-AUDIT v1 task_id= head= sha256=) before the gate reads it, and the gate requires that record for the audited head"
---

# AGMSG-TASK dotfiles-T124-wave3b-audit-grammar-a01 — T124 wave 3b: the audit prompt, its inputs and the finding grammar

Drafted 2026-10-10 by the orchestrator seat. Wave 3b of the accepted T124 design (read `.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md` in full, with its three review receipts and the addendum). Runs concurrently with wave 1 (`feat/task-validator`, worker-c): files are disjoint; the SKILL overlap is confined to the headless-audit bullet (SKILL step 10, the line that today reads `[P0-P3] confidence dimension file:line rationale`) and the Audit paragraph, not the task-authoring sections wave 1 edits; your tests live in a new file `tests/unit/test_herdr_agents_audit.py`, never in `test_herdr_agents.py` (wave 1's). Kind: code; Claude seat.

## What to build (prompt and wrapper only; the gate's parsing is wave 2a)

1. `home/dot_local/bin/common/executable_herdr-agents`, the `--audit` prompt: (a) the finding grammar, stated once and required: `[P<0-3>] <high|medium|low> <specification|implementation|evidence|orchestration|conformance> <path:line|-> <rationale>`; (b) the auditor's scope now includes the orchestrator's artifacts: the task file with its amendments, the acceptance record as it stands (earlier rounds' dispositions and the PR-feedback dispositions), the sweep JSON, the design task file and its review receipts when the task names one; findings on task wording, scope decisions, dispositions and acceptance claims are `orchestration`; process deviations are `conformance`; (c) for a `format: 2` task, one line per invariant id `INV-n: holds|violated <path:line>` and a closing line `Orchestration findings: <count>` before the verdict; (d) the input list adds `.orchestration/acceptance/<task id>.md` and, when present, `<task id>-permgate.jsonl` (wave 2b writes it; the prompt names it as optional until then); (e) the wrapper's `.last.md` parse stays verdict-only (the gate does the strict parse in wave 2a) but prints a warning when a `format: 2` task's output lacks any `INV-n:` line or the `Orchestration findings:` line, so the pair path shows the gap early.
2. `AGENTS.md` Audit section: the grammar, the five categories with one-line definitions, the auditor's standing to find the orchestrator's and the worker's mistakes (operator direction 2026-10-10), the INV lines and the count line for `format: 2` tasks, the lock (orchestration/conformance at P0–P2 are released only by an operator waiver or a design reset; the orchestrator cannot disposition them), and the verdict line as today. The headless prompt in the SKILL cites this section instead of restating the grammar.
3. SKILL: the headless-audit bullet in step 10 cites AGENTS.md Audit and names the grammar's location; no other SKILL section.
4. Tests (`tests/unit/test_herdr_agents_audit.py`, new): the generated prompt contains the grammar line, the five categories, the acceptance-record input when the file exists, the permgate extract when present, the INV and count requirements for a `format: 2` task and not for a legacy one; the wrapper warning fires on a `.last.md` lacking the lines and stays silent when they are present. Each test fails when its rule is removed.

Forbidden: anything else; `scripts/require-crit-review.py`; `tests/unit/test_herdr_agents.py`; the SKILL's task-authoring sections; `make update`; thread resolution. Standing instruction on Bot/CI findings and the sandbox-conduct section of wave 1 apply verbatim.

## Repo / branch

`.claude/worktrees/worker-f`: `git fetch origin`; `git switch -c feat/audit-grammar --no-track origin/main`.

## Validation commands

```
uv run python -m unittest tests.unit.test_herdr_agents_audit 2>&1 | tail -3
make unit-test 2>&1 | tail -3
shellcheck home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
mise x node npm:prettier -- prettier --check AGENTS.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2
<a generated audit prompt for this task (herdr-agents --audit --dry-run or the prompt file it writes), pasted whole>
gh pr checks <pr>
```

## Completion

PR to `main` (English title `feat(audit): fixed finding grammar, orchestrator artifacts in scope, invariant lines`), CI green, Bot wait, artifacts at the standard paths (masked with the repository masker), memory add with the command and output pasted, validation lines `invariant: INV-4 → …` and `invariant: INV-7 → …`, `AGMSG-RESULT v1 task_id=dotfiles-T124-wave3b-audit-grammar-a01` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=12.

## Amendment 1 (orchestrator, 2026-10-10) — one test hunk, per-commit prompt unchanged

Both defaults accepted. `tests/unit/test_herdr_agents.py` joins `allowed_files` for the single hunk `test_audit_task_inlines_the_task_inputs_and_the_merge_base_diff` (lines ~4321–4354): the expected prompt string only. Wave 1's only hunk in that file is one added test near line 2834, so the hunks are disjoint; the orchestrator allows the shared code file on that basis and the later of the two PRs takes `gh pr update-branch`. The per-commit `AUDIT_PROMPT` (lines 43–52) stays unchanged: the gate rejects per-commit audits and items 1b–1e are task-level. Push now.

## Amendment 2 (orchestrator, 2026-10-10) — README paragraph, front matter corrected

Default accepted: `README.md` joins `allowed_files` for the one paragraph at ~920–932 (the `herdr-agents --task` description: inputs, the fixed grammar, pointing at AGENTS.md Audit); wave 1's README hunk is near line 373, so the hunks are disjoint and the later PR takes `gh pr update-branch`. The front matter `allowed_files` now lists `tests/unit/test_herdr_agents.py` (Amendment 1) and `README.md` (this amendment); the validator of wave 1 will read the front matter, so the list and the prose must agree from now on.

## Push form (orchestrator, 2026-10-10)

The host SSH agent holds no identity and the global git config rewrites pushes to SSH, so the authorized push form (used by every task since T118) is: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles <branch>` (gh keyring login; no config file change). Use it for every push; it is not a rework of a refusal, it is the documented form.

## Concurrency note (orchestrator, 2026-10-10)

Three in-flight tasks touch `tests/unit/test_herdr_agents.py` in disjoint hunks (wave 1 near 2834, T120 at 1823, wave 3b at 4321) and two touch `home/dot_local/bin/common/executable_herdr-agents` in disjoint regions (T120: the claude-code shadow heal near 2048; wave 3b: the audit prompt). This is an orchestrator exception to the pairwise-disjoint code-file rule, taken for throughput and recorded in each acceptance record; merge order is by readiness, and every later PR takes `gh pr update-branch` and re-runs CI, the Bot wait and the gate on the merged head. A real conflict blocks only that PR.

## Amendment 3 (orchestrator, 2026-10-10) — redirected to T126 W2: a schema-validated audit instead of a prose grammar

The operator asked for the approach to be re-planned on the tools' documented capabilities (design `.orchestration/tasks/dotfiles-T126-regime-v2-a01.md`, "What the research established" and "W2"). Both runtimes validate output against a JSON schema (`codex exec --output-schema <file>`, `claude -p --output-format json --json-schema <schema>`), so the audit's verdict becomes a JSON document and nothing parses prose. Keep what you built for the prompt's scope (orchestrator artifacts, the acceptance record and `<task>-permgate.jsonl` as inputs, the auditor's standing); replace the grammar and the wrapper warning with:

1. `schemas/audit.json` (new, under `scripts/schemas/` or `schemas/`, name it in the report): `{verdict: correct|incorrect|blocked, findings: [{priority: P0..P3, confidence: high|medium|low, category: specification|implementation|evidence|orchestration|conformance, path: string|null, line: integer|null, rationale: string}], invariants: {INV-n: {status: holds|violated|not_applicable, path: string|null, line: integer|null, note: string}}, orchestration_findings: integer, not_checked: [string], summary: string}` with `additionalProperties: false` and `required` on every top-level key; `invariants` keys come from the task file (empty object for a legacy task).
2. `scripts/audit-head.sh <sha> --task <id> [--worktree <path>] [--out <path>]` (new): creates or reuses a detached worktree at `<sha>` under `.claude/worktrees/audit-<sha7>` (never the main checkout, never the set-aside dance), assembles the input list as the current prompt does, runs `codex exec --sandbox read-only --profile audit --output-schema <schema> --output-last-message <out>.json -C <worktree>` with the prompt, and on a non-zero exit or a schema failure falls back to `claude -p --permission-mode plan --output-format json --json-schema <schema> --max-budget-usd <from the tier table, default 5>` in the same worktree, recording which auditor ran; writes `<task>-audit-<sha7>.json` (the schema-valid document) and renders `<task>-audit-<sha7>.md.last.md` from it (one line per finding in the familiar form, the invariant map, the verdict line) so the existing gate keeps working until W5 reads the JSON; exits 0 for `correct`, 1 for `incorrect`, 2 for `blocked`. Two audits may run concurrently (distinct worktrees); a lock per sha prevents a duplicate for the same head.
3. `executable_herdr-agents --audit` delegates to `audit-head.sh` (the audit tab becomes optional: it may tail the output, it no longer serializes audits).
4. `AGENTS.md` Audit section: the schema (fields and categories with one-line definitions), the auditor's standing over the orchestrator's artifacts, the locks (orchestration/conformance at P0–P2 are released only by an operator waiver or a design reset), and that the auditor writes JSON, not prose; the headless prompt in the SKILL points here. The grammar sentences you wrote are replaced by the schema reference.
5. Tests (`tests/unit/test_herdr_agents_audit.py`): the schema validates a good document and rejects a missing key, an unknown category, an invariant status outside the enum; `audit-head.sh` with a fake `codex` that emits a valid document renders the `.last.md` and exits by verdict; with a fake `codex` that fails, the fake `claude` fallback runs and the record names it; the lock refuses a second run for the same sha; the worktree is detached at the sha. Each fails when its rule is removed.

`allowed_files` adds `scripts/audit-head.sh`, `schemas/audit.json` (or `scripts/schemas/audit.json`), and the PR title becomes `feat(audit): schema-validated headless audits in detached worktrees, orchestrator artifacts in scope`. The README paragraph (Amendment 2) describes the schema instead of the grammar. Rebase nothing; add commits on `feat/audit-grammar`. Push, CI, Bot wait, `AGMSG-RESULT … round=1`.

## Hold (orchestrator, 2026-10-10, minutes after Amendment 3)

Amendment 3 rode on a design (T126) that has no review receipt yet. Hold: draft `schemas/audit.json` if you wish, but do not implement `audit-head.sh`, the `herdr-agents --audit` delegation or the AGENTS.md rewrite until the orchestrator sends the T126 verdict; keep the branch as it is otherwise. If the verdict is `revise` on the schema shape, the schema follows the revised design.

## Hold released (orchestrator, 2026-10-10 10:4xZ) — Amendment 3 proceeds as T126 W2

T126 (regime v2) was accepted in design review round 3 (`.orchestration/validation/dotfiles-T126-regime-v2-a01-design-review-round3.md`, canonical hash `503eea51…`). Amendment 3 stands, with three precisions from the accepted design and its reviews:
1. `audit-head.sh` publishes the audit JSON's sha256 to agmsg history before anyone reads it: it joins (or reuses) an audit identity `claude-audit-dot-h001`/`codex-audit-dot-h001` at the detached worktree path with `AGMSG_RESOLVE_PROJECT=0 join.sh`, and sends `AGMSG-AUDIT v1 task_id=<id> head=<sha> sha256=<json sha256> auditor=<codex|claude>` with `send.sh --body-file` to `claude-deep-dot`; the `.last.md` rendering carries the same sha256 in its header. (T126 INV-4.)
2. The `claude -p` fallback runs with `--bare` when an API key is present (`ANTHROPIC_API_KEY`), otherwise without `--bare` under the managed hooks, and the validation shows one fallback run in a detached worktree with the hooks' output, demonstrating they do no harm there (T126 INV-4; the hooks page says `disableAllHooks` does not disable managed hooks, so do not rely on it).
3. The `herdr-agents --audit` delegation: keep the pane-run, marker, masking and verdict mechanics the 33 existing tests pin, and have the tab's run call `audit-head.sh` for the model invocation only; if that cannot be done inside Amendment 1's one-hunk limit on `test_herdr_agents.py`, split the delegation into its own follow-up PR (W2b) and ship the schema, `audit-head.sh`, AGENTS.md and the new test file in this one. Say which in the report.
Push, CI, Bot wait, `AGMSG-RESULT … round=1` (a new RESULT for the new head; message 194 is superseded).

## Amendment 4 (orchestrator, 2026-10-10) — front matter caught up; defaults accepted

(1) W2b accepted: `herdr-agents` stays as it is on the branch; the delegation is its own follow-up task (`dotfiles-T126-w2b-herdr-audit-delegation-a01`, drafted). (2) Front matter updated: `design_review` now names the T126 design and its round-3 receipt, `invariants` is T126's INV-4 (the W2 scope; the gate parse is W5), `allowed_files` adds `scripts/audit-head.sh` and `scripts/schemas/audit.json`; map your validation's `invariant:` line to INV-4. (3) The two real model runs are the orchestrator's, after the PR is green: the task-level audit of the head through the branch's `audit-head.sh`, and one run with `codex` hidden from PATH to force the `claude -p` fallback; their output is pasted into the acceptance record and your validation stays on fakes and offline schema checks. Precision 2's "show the managed hooks harmless" is satisfied by that orchestrator run.

## Amendment 5 (orchestrator, 2026-10-10) — scope-gap 3

Default accepted: `tests/unit/test_agmsg_orchestration_docs.py` joins `allowed_files` for the `HEADLESS_AUDIT` constant on line 21 only, now `scripts/audit-head.sh <head-sha> --task <id>`, with the same single-source rule (the form appears exactly once, in the SKILL's task-level audit bullet). One headless form; the manual `codex exec` line goes.
