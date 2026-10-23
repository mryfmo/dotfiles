---
format: 2
task_id: dotfiles-T129-pstack-asset-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T129-pstack-asset-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T129-pstack-asset-review-a01 — independent review of the pstack asset text (plan 023 PR G)

Rewritten 2026-10-22T04:50Z by the orchestrator seat for the resumed text (the 2026-10-17 round was a Codex-half review of the round-2 text; this is the one-round task-file review of the agmsg-orchestration SKILL on the re-anchored bytes).

## What to review

1. `.orchestration/tasks/dotfiles-T129-pstack-asset-a01.md` at sha256 `82f4073fd0157489004c2040a745a63d13082552c325d77ef86eb60f9cd756e0` (129 lines) is the file you judge; compute the hash yourself and stop with `verdict=reject` if it differs.
2. No contradiction with plan 023 PR G (`.orchestration/plans/023-omp-hcom-migration.md`, "G. pstack as a tracked asset"): only `pstack/` is taken, the three manifest groups, the pin by tree hash, the updater seam, the runtime receipt, the CI step.
3. The premises hold: every line of the `## Checks` block is a pasted command with its output and exit status (generated at canonical main d06d94fd); the five premise outputs match the claims in the front matter; `after:` names the merged assets-omp-hcom lineage and gh-binding a02 (shared `home/dot_agents/agent-config.yaml`).
4. `allowed_files` covers every touch point the items name (manifest, updater, runtime check, workflow step, the two tests); a touch point outside the seven entries is a reject.
5. The threat table's shape rules by hand: every `closed:` selector is `tests/<file>::<name>`, every `residual:` payload a sentence of at least 20 characters with an owner, one row per allowed_files entry and per non-path control and per orchestrator effect.
6. Amendment 1 changes only what it says (dependency, updater drift note, pin wording, the item-9 cache sentence); no item is widened.
7. Read only; no file changed, nothing dispatched, no network write.

## Output

`.orchestration/dotfiles-T129-pstack-asset-review-a01/review.md` with the hash, one line per item and the verdict, then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T129-pstack-asset-review-a01 status=ready_for_review round=1 verdict=accept|reject design_file=.orchestration/tasks/dotfiles-T129-pstack-asset-a01.md design_sha256=<the hash you computed> findings=<n> report=.orchestration/dotfiles-T129-pstack-asset-review-a01/review.md`, sent with `agmsg-dispatch dotfiles-conformance claude-standard-dot-a011 claude-deep-dot wW:p1 '<that line>'`. A reject names each failing item with the line.
