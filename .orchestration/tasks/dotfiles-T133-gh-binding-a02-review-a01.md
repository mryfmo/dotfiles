---
format: 2
task_id: dotfiles-T133-gh-binding-a02-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T133-gh-binding-a02-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T133-gh-binding-a02-review-a01 — independent review of the gh-binding a02 text

Drafted 2026-10-22T01:19Z by the orchestrator seat. `dotfiles-T133-gh-binding-a02` is the reset of `dotfiles-T133-gh-binding-a01` (two C-80 rounds, 3bf2a79 and 6486b79, stopped at S-R5; the remaining findings were the gate's gh descendants `scripts/require-crit-review.py:519/615` and `scripts/pr-feedback.py:84`). The a02 text passed C-80 at c761dc8 (unpopulated) and again at c0a7dae7 after the orchestrator pasted the Checks block with a bound-executable, enumerated-environment measurement of canonical main. This is the one-round task-file review of the agmsg-orchestration SKILL ("A task-file review is one round with a fixed stop condition").

## What to review

1. `.orchestration/tasks/dotfiles-T133-gh-binding-a02.md` at sha256 `c0a7dae7d7e10974669ebd2e21b79907a5b5c5e84016d308b9d4fa8bce73c3df` (131 lines) is the file you judge; compute the hash yourself and stop with `verdict=reject` if it differs.
2. No contradiction with the design: `.orchestration/plans/024-design-quality.md` section 5.14 items 2-4 and 9 (cited by number, not restated); the pin, declaration, consumer binding and minimal-environment items must not contradict them.
3. The premises hold: every line of the `## Checks` block is pasted command output (canonical main 7da0cdfa and the design digest from a private bare clone with the real git binary in an enumerated environment; the mise pin line; the installed gh version; the interpreter bindings; items 1 and 2 observations); a claim without its command is a reject.
4. `allowed_files` covers every touch point grep finds for the six routes the text names: `pick gh` or `gh ` in `scripts/orchestrator/chain-integrate.sh`, `scripts/orchestrator/orch-gate.sh`, `scripts/orchestrator/local-review.sh`; `gh` calls in `scripts/require-crit-review.py` (lines 519 and 615) and `scripts/pr-feedback.py` (line 84); the four test modules; the declaration in `home/dot_agents/agent-config.yaml` and its validator `scripts/validate-agent-assets.py`; the pin in `home/dot_mise/config.toml`. A touch point outside the eight entries is a reject.
5. The threat table's three shape rules by hand: every `closed:` selector has the form `tests/<file>::<Class>::<test>` for a test the PR will add; every `out-of-scope:` owner is a task id; every `residual:` payload is a sentence of at least 20 characters naming `dotfiles-T133-gh-binding-followup-a01` or `dotfiles-T133-trusted-entrypoint-binding-a01`; one row per allowed_files entry (the `scripts/orchestrator/*.sh` wildcard: one row per concrete file), one per non-path control, one per orchestrator effect.
6. The text carries no `invariants` key, so no invariant entry is required.
7. Read only; no file changed, nothing dispatched, no network write.

## Output

`.orchestration/dotfiles-T133-gh-binding-a02-review-a01/review.md` with the hash, one line per item and the verdict, then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T133-gh-binding-a02-review-a01 status=ready_for_review round=1 verdict=accept|reject design_file=.orchestration/tasks/dotfiles-T133-gh-binding-a02.md design_sha256=<the hash you computed> findings=<n> report=.orchestration/dotfiles-T133-gh-binding-a02-review-a01/review.md`, sent with `agmsg-dispatch dotfiles-conformance claude-standard-dot-a011 claude-deep-dot wW:p1 '<that line>'`. A reject names each failing item with the line.
