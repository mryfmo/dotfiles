---
format: 2
task_id: dotfiles-T133-pre-send-check-a01-redesign-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T133-pre-send-check-a01-redesign-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T133-pre-send-check-a01-redesign-review-a01 — INV-6 reset anchor review of dotfiles-T133-pre-send-check-a01

Drafted 2026-10-20T14:20Z by the orchestrator seat (plan 006 A3 / V3a). `dotfiles-T133-pre-send-check-a01` (PR #442, worker claude-standard-dot-a008) spent its round 1 and its one revise round; the local review of the round-2 head 11584e19 re-opened the round-1 class (checker excerpts can expose secret fragments, P1) with two P2, so the lineage goes back to design as `dotfiles-T133-pre-send-check-a02` (`.orchestration/tasks/dotfiles-T133-pre-send-check-a02.md`, `reset_of: [dotfiles-T133-pre-send-check-a01]`): no substring of the task text or of the checker's output ever reaches the preflight's output (rule names and line numbers only), the secret pattern runs over the complete text, fences are parsed completely before selection, the task id comes from parsed YAML. PR #442 continues under a02 from 11584e19.

## What to review

1. `.orchestration/tasks/dotfiles-T133-pre-send-check-a02.md` at sha256 `438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95`: compute it yourself (`shasum -a 256`) and stop with `verdict=reject` if it differs.
2. Its items close the six findings of the two local reviews (`.orchestration/validation/dotfiles-T133-pre-send-check-a01-local-review-d067910.md` and `…-09e2e95.md`) by design, not by patch: name the item that closes each finding in your review; each new rule has a `closed:` selector; the output-suppression test asserts that a secret-shaped token and its 8-character substrings are absent from stdout and stderr; nothing widens permissions or trust boundaries beyond a01; caps 90/220 and the C-107 sentence are intact.
3. Read only: change no file, dispatch nothing.

## Output

`.orchestration/dotfiles-T133-pre-send-check-a01-redesign-review-a01/review.md` in your worktree: the hash you computed, one line per item (ok, or the finding with file:line), the verdict. Then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T133-pre-send-check-a01-redesign-review-a01 status=ready_for_review verdict=accept design_sha256=438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95 review=.orchestration/dotfiles-T133-pre-send-check-a01-redesign-review-a01/review.md`, or `verdict=reject` with the findings in the file. No PR, no commit, no push.
