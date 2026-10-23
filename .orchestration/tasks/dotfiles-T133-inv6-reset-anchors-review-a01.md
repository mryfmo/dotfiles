---
format: 2
task_id: dotfiles-T133-inv6-reset-anchors-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T133-inv6-reset-anchors-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T133-inv6-reset-anchors-review-a01 — INV-6 reset anchors for the plan 024 lineages (batch review)

Drafted 2026-10-20T14:39Z by the orchestrator seat (plan 006 A3 / V3a). `make check-regime-boundary` (2026-10-20T14:36Z) reports an INV-6 S2 line for every lineage below: each was reset to its redesign by a TASK line with `reset_of=` but without the reset record and the accepting RESULT of another context, so the thresholds stay reported. You are that other context for all twelve. Read only: compute each hash yourself (`shasum -a 256` on the main checkout's file, `~/Workspace/dotfiles/.orchestration/tasks/<new>.md`), check the front matter's `reset_of`, read the predecessor's acceptance record (`~/Workspace/dotfiles/.orchestration/acceptance/<old>.md`) for the findings that forced the reset and confirm the redesign answers them and widens no permission or trust boundary; change no file, dispatch nothing.

## Lineages

1. `dotfiles-T133-python-pin-a01` -> `dotfiles-T133-python-pin-a02` (revises 4, amendments 2; a02 merged as #437): `.orchestration/tasks/dotfiles-T133-python-pin-a02.md` at sha256 `95c7e7c7bf0007e2da931017867883cd60ad47b9b7f40226595a03cdd37d92c6`; its front matter must name `reset_of: [dotfiles-T133-python-pin-a01]`; RESULT round=1.
2. `dotfiles-T133-regime-ci-fixture-grammar-a01` -> `dotfiles-T133-regime-ci-fixture-grammar-a02` (amendments 2, questions 2; a02 merged as #441): `.orchestration/tasks/dotfiles-T133-regime-ci-fixture-grammar-a02.md` at sha256 `fd9ff2123d96bebdabfea725bcc7c8412b3f1275bbaac2858da143d9a0ff1303`; its front matter must name `reset_of: [dotfiles-T133-regime-ci-fixture-grammar-a01]`; RESULT round=2.
3. `dotfiles-T133-result-precheck-a01` -> `dotfiles-T133-result-precheck-a02` (amendments 2, questions 2 (P1-5)): `.orchestration/tasks/dotfiles-T133-result-precheck-a02.md` at sha256 `fda18e21e738bb222a50ebd29be302fa009fd1a2822b660311abe81aa1397e61`; its front matter must name `reset_of: [dotfiles-T133-result-precheck-a01]`; RESULT round=3.
4. `dotfiles-T133-result-precheck-a02` -> `dotfiles-T133-result-precheck-a03` (reset chain of P1-5): `.orchestration/tasks/dotfiles-T133-result-precheck-a03.md` at sha256 `d8048ef508676f65c5eaee82cc69a9f83f04b4418ed3e61bb9e4803d5c0a32ba`; its front matter must name `reset_of: [dotfiles-T133-result-precheck-a02]`; RESULT round=4.
5. `dotfiles-T133-result-precheck-a03` -> `dotfiles-T133-result-precheck-a04` (reset chain of P1-5; a04 is PR #411): `.orchestration/tasks/dotfiles-T133-result-precheck-a04.md` at sha256 `e52afb631043154c08f3bda8d217edd299ccd6d97b6fb72aa88b8e12f7328700`; its front matter must name `reset_of: [dotfiles-T133-result-precheck-a03]`; RESULT round=5.
6. `dotfiles-T133-task-generator-plan-check-a02` -> `dotfiles-T133-task-generator-plan-check-a03` (revises 2 (P1-12)): `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a03.md` at sha256 `1dd4538ac9edf5f35d55ddb585e7911d4e6e7fe9fcfd5692524101b060fb7e3c`; its front matter must name `reset_of: [dotfiles-T133-task-generator-plan-check-a02]`; RESULT round=6.
7. `dotfiles-T133-task-generator-plan-check-a03` -> `dotfiles-T133-task-generator-plan-check-a04` (amendments 3 (P1-12)): `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a04.md` at sha256 `b325fe161c1e2cab2183cc0f8110ad185153b6cde15dbeaf9b894d5efe9e3e0c`; its front matter must name `reset_of: [dotfiles-T133-task-generator-plan-check-a03]`; RESULT round=7.
8. `dotfiles-T133-task-generator-plan-check-a05-checker` -> `dotfiles-T133-task-generator-plan-check-a06-checker` (amendments 2, questions 2; a06 is PR #440): `.orchestration/tasks/dotfiles-T133-task-generator-plan-check-a06-checker.md` at sha256 `b9e04cb9b2fdb9d4fea9f8f93eec3a88de55b72d5114797103c98e9784b572af`; its front matter must name `reset_of: [dotfiles-T133-task-generator-plan-check-a05-checker]`; RESULT round=8.
9. `dotfiles-T133-permission-guard-gate-a01` -> `dotfiles-T133-permission-guard-gate-a02` (questions 3 (P1-14)): `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a02.md` at sha256 `8623badb987ae8c4c5f66a3ac3ab1bfefb1e347e878c31ae6317eba726f6b1d4`; its front matter must name `reset_of: [dotfiles-T133-permission-guard-gate-a01]`; RESULT round=9.
10. `dotfiles-T133-permission-guard-gate-a03` -> `dotfiles-T133-permission-guard-gate-a04` (questions 2 (P1-14)): `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a04.md` at sha256 `17a1795fbbafe55339dfa28b8c5a7d779408e615c1679262a591b9030ebef0cb`; its front matter must name `reset_of: [dotfiles-T133-permission-guard-gate-a03]`; RESULT round=10.
11. `dotfiles-T133-ci-efficiency-a01` -> `dotfiles-T133-ci-efficiency-a02` (amendments 2 (P1-3)): `.orchestration/tasks/dotfiles-T133-ci-efficiency-a02.md` at sha256 `684257319a5b9b5f5c67fe5852aedd76fd5b9db4bb4f5a1ff0b928a0ad61ab98`; its front matter must name `reset_of: [dotfiles-T133-ci-efficiency-a01]`; RESULT round=11.
12. `dotfiles-T133-ci-efficiency-followup-a02` -> `dotfiles-T133-ci-efficiency-followup-a04` (revises 2, amendments 2 (P1-3); a04 text not yet dispatched, its file bytes are the design): `.orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md` at sha256 `3eba74bfa6104d3c89aeb0e57e823b87da672863d844fe04855031d918d5c975`; its front matter must name `reset_of: [dotfiles-T133-ci-efficiency-followup-a02]`; RESULT round=12.

## Output

`.orchestration/dotfiles-T133-inv6-reset-anchors-review-a01/review.md` in your worktree: one section per lineage with the hash you computed and one line per check (ok, or the finding with file:line). Then one RESULT per lineage, in the order above, `AGMSG-RESULT v1 task_id=dotfiles-T133-inv6-reset-anchors-review-a01 status=ready_for_review round=<n> verdict=accept design_sha256=<sha> lineage=<old> review=.orchestration/dotfiles-T133-inv6-reset-anchors-review-a01/review.md` when the lineage's checks hold, or `verdict=reject` with the findings in the file. No PR, no commit, no push. The twelve RESULTs of this review task are expected; its acceptance record carries `pr=none`.
