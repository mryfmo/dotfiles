---
format: 2
task_id: dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01 — INV-6 reset anchor review of dotfiles-T133-worker-cap-hookspath-a01

Drafted 2026-10-20T14:07Z by the orchestrator seat (plan 006 A3 / V3a: a reached INV-6 threshold is silenced only by a design-reset record whose redesign the review of another context accepted). `dotfiles-T133-worker-cap-hookspath-a01` reached S2 (amendments 3 (INV-6 S2)); its redesign `dotfiles-T133-worker-cap-hookspath-a02` (`.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md`, `reset_of: [dotfiles-T133-worker-cap-hookspath-a01]`) was written and dispatched without the reset record and the accepting RESULT, so `make check-regime-boundary` still reports the S2 line (measured 2026-10-20T14:01Z).

## What to review

1. `.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a02.md` at sha256 `661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4` is the file you judge; compute the hash yourself (`shasum -a 256`) and stop with `verdict=reject` if it differs.
2. Its front matter names `reset_of: [dotfiles-T133-worker-cap-hookspath-a01]`; its items and threat table answer the findings that forced the reset, as `.orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01.md` records them (read the record's chronology lines around the reset decision and the carried rows); nothing in the redesign widens permissions or trust boundaries beyond `dotfiles-T133-worker-cap-hookspath-a01`.
3. The redesign is dispatched already (the live lineage, in progress); your review changes no file and dispatches nothing. Read only.

## Output

`.orchestration/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01/review.md`: the hash you computed, one line per item above (ok, or the finding with file:line), and the verdict. Then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01 status=ready_for_review verdict=accept design_sha256=661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4 review=.orchestration/dotfiles-T133-worker-cap-hookspath-a01-redesign-review-a01/review.md` when every item holds, or `... verdict=reject design_sha256=661c44fddb8e38a33dac80674572c5ea31e5abfbd3230542a86e4f47c1e5bcf4 review=...` with the findings in the file. No PR, no commit, no push; the orchestrator writes the reset record from your RESULT.
