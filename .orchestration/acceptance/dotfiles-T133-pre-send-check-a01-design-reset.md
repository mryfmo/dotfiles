---
format: 2
reset_of: dotfiles-T133-pre-send-check-a01
redesign_task: dotfiles-T133-pre-send-check-a02
design_sha256: 438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95
redesign_source: dotfiles-T133-pre-send-check-a01-redesign-review-a01
redesign_seat: claude-standard-dot-a011 (standard profile, a context other than the task's author; the review profile authored the a02 text)
reason: "INV-6 on dotfiles-T133-pre-send-check-a01 (PR #442): round 1 and the one revise round spent; the local review of the round-2 head 11584e19 re-opened the round-1 class (checker excerpts can expose secret fragments, P1) with two P2; no third worker round on a mechanism PR, so the lineage goes back to design (2026-10-20T14:06Z)."
---

# Design reset: dotfiles-T133-pre-send-check-a01 (PR #442), anchored 2026-10-20

- **What stops:** the a01 specification (redaction of matches). PR #442, the worker claude-standard-dot-a008 and the branch continue under `dotfiles-T133-pre-send-check-a02` from head 11584e19.
- **Why a reset:** the round-1 revise allowed redaction or suppression; the worker chose redaction, and the round-2 review showed PyYAML's clipped excerpts carry credential fragments past the pattern. The a02 design: no substring of the task text or of the checker's output ever reaches the preflight's output (rule names and line numbers only), the secret pattern runs over the complete text, fences are parsed completely before selection, the task id comes from parsed YAML.
- **Redesign:** `.orchestration/tasks/dotfiles-T133-pre-send-check-a02.md` at sha256 `438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95` (review profile; self cap 120 -> 130 by the orchestrator), `reset_of: [dotfiles-T133-pre-send-check-a01]`.
- **Anchor:** RESULT of `dotfiles-T133-pre-send-check-a01-redesign-review-a01` by claude-standard-dot-a011 at 2026-10-20T14:21:51Z: `verdict=accept design_sha256=438089b8b9eb46db347e724913c1d4070d575df5091e3ea4a7e1d4b46412bf95`, review at `.orchestration/dotfiles-T133-pre-send-check-a01-redesign-review-a01/review.md` (copied from the worker's worktree by the orchestrator).
- **Waiver:** none.
