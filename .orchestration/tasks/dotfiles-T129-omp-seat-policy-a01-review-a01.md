---
format: 2
task_id: dotfiles-T129-omp-seat-policy-a01-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T129-omp-seat-policy-a01-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T129-omp-seat-policy-a01-review-a01 — independent review of the omp seat-policy text (plan 023 PR B stage 2)

Drafted 2026-10-22T08:42Z by the orchestrator seat on the D-024-87 critical path. The text renders every omp seat's command policy and context-maintenance settings from one manifest block into two per-role `--config` overlays; it uses omp 18.11.3's documented settings only (no hook code), quoted with fetch times in `.agents/worklog/orchestrator-glue/b2-c2-facts.md` (read it as context, judge the text). The text declares security: true, so C-80 runs beside your review; you judge it as a task-file review, one round per revision.

## What to review

Amendment 3 (2026-10-22T09:33Z, the C-59 re-plan of class pattern-shape): the text specifies behaviour (Item 4's classification table) and ships the reference matcher (Item 2) as the only oracle; Item 1's lists are starting data the worker reshapes; the validator keeps no shape rule; a residual row names the pilot check against live omp. Judge the new bytes under the same five items, reading item 3's "verifiability" as: can the worker make the table pass and prove it, and does the text avoid prescribing the rule language's surface. The hash below is the new one.

Amendment 2 (2026-10-22T09:05Z): your round-2 F4 is answered: the pattern shape rule is stated (no literal space between an inner `*` and its token) and enforced by the validator; the `gh api` method and field patterns take the shape `*gh api* -X POST*`; `curl`/`wget` pipes have two-sided forms; Item 4's matcher test adds the flag-first, compound and false-positive spellings; a `bash_deny.first` rule `*gh pr merge*--admin*` precedes the allow (your P3). Judge the new bytes under the same five items; the hash below is the new one.

Amendment 1 (2026-10-22T08:52Z): your round-1 findings are answered: F1 the eight gh api field spellings are in `common` and every pattern carries wildcards on both sides, with the bypass spellings (env prefix, endpoint-first, field forms, `git -c … push`) named in the orchestrator test; F2 `gh pr update-branch` is in `common` and the worker test asserts it; F3 the orchestrator overlay carries an ordered allow for `gh pr merge * --squash --match-head-commit *` and the claim about ready/comment scripts is gone; P3: Item 0 queries B-1's model ids, a residual row covers the non-Bash denies, the validator refuses `prompt`, README lines 17-27. Judge the new bytes under the same five items; the hash below is the new one.

1. `.orchestration/tasks/dotfiles-T129-omp-seat-policy-a01.md` at sha256 `136bd6ee734d2acebcd5267ce9d419a3cc5755a24834f0a8b3697f36cfb59f71` is the file you judge (110 lines); compute the hash yourself and stop with `verdict=reject` if it differs.
2. Design fidelity: Items 1-4 meet plan 024 B stage 2 ("gh 書込拒否", the 600k handoff, policy as generated data) with `deny` rules only (never `prompt`, which fails headless); the `common` list covers every `deny` and `ask` entry of the Claude manifest's `claude.permissions` (the Checks block counts 42 `Bash(` lines at main) except those a worker legitimately runs, and the orchestrator-only list adds exactly the writes the orchestrator performs through repository scripts; the compaction keys and values match the plan's intent; nothing in the text starts a seat, writes under `~/.omp` or adds a TypeScript hook.
3. Official grounding: every omp key the text names exists in omp 18.11.3's settings, approval-mode and compaction documentation with the semantics the text states (first matching rule wins, `*` wildcard, deny matches a segment of a compound command, deny absolute in yolo, `tools.approval.eval`, strict `--config` overlays, `thresholdTokens`, `methodOrder`, `handoffSaveToDisk`); re-fetch at least the settings page at tag v18.11.3 (unauthenticated GitHub API calls are rate-limited this hour; one fetch suffices); Item 0 makes the two unknowns (the live default values and the models' context windows) observable without a seat start; the caps sentence is the regime verifier's form; red/green is required per selector.
4. Threat table and metadata: one row per allowed_files entry, per non-path control (approval is not containment, headless prompt, the `--config` seam, hcom's `omp_args` precedence, in-process effects, workflow inputs, metadata, separators, new scripts) and per orchestrator effect; a closed row's selector is defined in Item 4; a residual row's control mitigates its risk and names an owner that exists (this task; the C-2 task id appears as the consumer of the overlays, not as an owner); the `private_` source paths keep 0700/0600; the Checks block is pasted command output only.
5. Read only; no file changed, nothing dispatched.

## Output

`.orchestration/dotfiles-T129-omp-seat-policy-a01-review-a01/review.md` with the hash, one line per item and the verdict, then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T129-omp-seat-policy-a01-review-a01 status=ready_for_review verdict=accept design_file=.orchestration/tasks/dotfiles-T129-omp-seat-policy-a01.md design_sha256=136bd6ee734d2acebcd5267ce9d419a3cc5755a24834f0a8b3697f36cfb59f71 review=.orchestration/dotfiles-T129-omp-seat-policy-a01-review-a01/review.md`, or the same with `verdict=reject` and the findings in the file.
