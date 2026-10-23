---
format: 2
task_id: dotfiles-T129-hcom-omp-seat-a01-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T129-hcom-omp-seat-a01-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T129-hcom-omp-seat-a01-review-a01 — independent review of the hcom omp-seat text (plan 023 PR C stage 2)

Drafted 2026-10-22T08:46Z by the orchestrator seat on the D-024-87 critical path. The text gives herdr-agents a third seat kind, omp, launched through hcom with the model from B-1's env line and the policy overlay from B-2, with fake-hcom tests only (no seat start, no live store). Facts with fetch times are in `.agents/worklog/orchestrator-glue/b2-c2-facts.md` (context; judge the text). security: true, so C-80 runs beside your review; one round per revision.

## What to review

Amendment 3 (2026-10-22T09:37Z, the C-59 re-plan of class reply-address): the reply route is C-1's contract (TASK sends `@<worker> --thread <team>` seed the thread; replies `--thread <team>` with no target; bus-history reads by thread; C-1 amendment 3 carries it with a two-direction fixture test); Item 2 cites it by task id and keeps the worker's half only. Judge the new bytes under the same five items; the hash below is the new one.

Amendment 2 (2026-10-22T09:08Z): your round-2 F4 is answered: the worker answers on the team thread (`hcom send --thread "$HCOM_TAG" --`), which C-1's bus-history reads by `msg_thread = team`, so an external orchestrator (`ext_<name>` until X) needs no `@` address; the `hcom list` fallback is gone; the omp_args refusal reads hcom's effective value (your P3); one selector added. Judge the new bytes under the same five items; the hash below is the new one.

Amendment 1 (2026-10-22T09:00Z): your round-1 findings are answered: F1 the SKILL answers the delivery's sender (hcom names it) and falls back to `hcom list --json` by directory, no undefined TASK field; F2 the launcher reads `config omp_args` and refuses to seat while it is non-empty, the row names that mechanism; F3 the launcher runs only C-1's digest-checked private hcom at `<DIR>/.agents/worklog/uv-tools/hcom/bin/hcom` and never `~/.local/bin/hcom`; readiness polls the list row before `events --idle`; the model value passes as rendered. Judge the new bytes under the same five items; the hash below is the new one.

1. `.orchestration/tasks/dotfiles-T129-hcom-omp-seat-a01.md` at sha256 `e0e4c80a0260a15d5dba32f3fcc02db244ea8d1d0c6ef84fce4def34bb2c9d2c` is the file you judge (105 lines); compute the hash yourself and stop with `verdict=reject` if it differs.
2. Design fidelity: Items 1-3 meet plan 024 C stage 2 ("hcom omp 着席", launch record, live arguments on --attach, idle through hcom events) without touching agmsg paths for claude and codex; the argv of Item 1 is complete and ordered (hcom flags, then omp args), each value passes the launcher's existing plain --flag value regex, and nothing reads omp_args or sets HCOM_DIR; the seat is found by directory and confirmed by `hcom events --idle`; the remove path uses a documented hcom command whose name Item 0 pastes rather than assumes; the deferred list names what X and later tasks own.
3. Official grounding and verifiability: every hcom, herdr and omp behaviour the text relies on is in the facts file with a quote (launch form and flags, the herdr terminal preset, the environment hcom sets, the list fields, `events --idle --wait` exit codes, `send @name --`, herdr's --kind omp, omp's --model and --config); the Checks block's observations agree with them (the deployed hcom is 0.7.30 while 0.7.31 is advertised: the manifest pin rules); each selector of Item 3 is a test name the worker can make red at main and green at the fix with fakes alone; the caps sentence is the regime verifier's form.
4. Threat table and metadata: one row per allowed_files entry, per non-path control (the hcom store, the seat environment and injected extension, the herdr preset, the notify server, in-process effects, workflow inputs, metadata, separators, new scripts) and per orchestrator effect; residual rows' controls mitigate their risks and name an owner that exists (this task); the X pilot is named where a fact can only be measured by a seat start; the Checks block is pasted command output only.
5. Read only; no file changed, nothing dispatched.

## Output

`.orchestration/dotfiles-T129-hcom-omp-seat-a01-review-a01/review.md` with the hash, one line per item and the verdict, then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T129-hcom-omp-seat-a01-review-a01 status=ready_for_review verdict=accept design_file=.orchestration/tasks/dotfiles-T129-hcom-omp-seat-a01.md design_sha256=e0e4c80a0260a15d5dba32f3fcc02db244ea8d1d0c6ef84fce4def34bb2c9d2c review=.orchestration/dotfiles-T129-hcom-omp-seat-a01-review-a01/review.md`, or the same with `verdict=reject` and the findings in the file.
