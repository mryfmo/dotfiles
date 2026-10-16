---
format: 2
task_id: dotfiles-T128-doctor-codex-trust-review-a01
kind: review
security: false
---

# AGMSG-TASK dotfiles-T128-doctor-codex-trust-review-a01 — confirm the task text `dotfiles-T128-doctor-codex-trust-a01` (review seat half; Codex headless runs the same check in parallel)

Drafted 2026-10-15 by the orchestrator seat (the bus time of the TASK line is the dispatch time). The reviewed file is `.orchestration/tasks/dotfiles-T128-doctor-codex-trust-a01.md` (untracked; its sha256 is the `doctor_task_sha256` of the TASK line), plan 022 T11: the doctor compares the Codex config against the canonical clone's trust entry wherever it runs, asking `chezmoi source-path`, with a WARN fallback. One round, fixed stop condition.

## Stop condition

1. Item 1 describes the change correctly against `scripts/check-agent-runtime.py` on `origin/main` (`same_modified` at lines 107 to 131 setting `CHEZMOI_SOURCE_DIR` to `SOURCE_ROOT`; the Codex config comparison in `check()` around line 797; the WARN convention of `is_warning` and the `WARN:` line appended to the failures list at line 270) and against `home/dot_codex/modify_private_config.toml` on `origin/main` (`source_dir()` reads `CHEZMOI_SOURCE_DIR`, its parent is the working tree the trust entry names): the three edits are the function, the keyword parameter with its default keeping every existing call unchanged, and the one call site; the failure modes follow (present and answering, absent or failing, a non-directory answer); the WARN line is counted as a warning, not an error. The reviewer replays `chezmoi source-path` from its seat and reports the answer.
2. Item 2's two test names appear verbatim (the first in the closed row); the cases distinguish the Codex comparison from the others (the recorded `source_dir` per source), cover the `None` fallback with exactly one WARN line, and the four failing answers of `canonical_source_dir`, in the module's style (module attributes patched and restored; `subprocess.run` patched, no real chezmoi).
3. The threat table has one row per `allowed_files` entry, the chezmoi-binary row as the non-path control, the generic rows verbatim from `.orchestration/templates/task-short.md`, and the new-scripts row saying no new script; no sentence states an unlanded mechanism as present; the Completion clause is plan 020 step 4's with correction C-50's small-P2 revise rule and the D2 replay; the cap sentence reads outside `tests/` and outside `.orchestration/`; `allowed_files` is pairwise-disjoint from every in-flight task (the chain-review follow-up's `scripts/orchestrator/*`, the seat-liveness task's boundary check and launcher, the settings-hook dedupe task's modify script and test, the pane-open follow-up's hook and rule: none names the two files).
4. The file passes C1 to C10 and C7b (the orchestrator pasted `dotfiles-T128-doctor-codex-trust-a01.md: OK`), the mask check (`masked 0 match(es)`), and its four premises replay from this checkout (`origin/main` fetched): `2`, `0`, `1`, `52`.

## Output

`.orchestration/validation/dotfiles-T128-doctor-codex-trust-review-a01.md`: the usual header with the sha256, findings (`P0`–`P3`, confidence, `file:line`, one line each), one line `Task-file verdict: dotfiles-T128-doctor-codex-trust-a01: confirm|revise`. Forbidden: editing tracked files, branches, commits, pushes, PRs. RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T128-doctor-codex-trust-review-a01 round=1 verdict=confirm|revise doctor_task_sha256=<sha> validation=<path>`.

## Withdrawn (2026-10-15T06:57:32Z)

The reviewed task was withdrawn before dispatch (its premise does not hold; see its record). No verdict is needed.
