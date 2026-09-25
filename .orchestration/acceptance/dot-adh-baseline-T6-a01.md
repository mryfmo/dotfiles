# Acceptance: dot-adh-baseline-T6-a01

## Revision 1

status: revise — the stop was over-conservative (my step-5 wording): scanning is fine as long as validators pass and the baseline stays unmodified. Instruction: run `make unit-test` and `validate-agent-assets.py` unchanged in the worktree; if green, `git add reviews` and RESULT; if red, paste the exact output and stop (no exclusions without orchestrator decision).

## Result

status: accepted — 198 files staged, byte-identical to the main copy (diff -rq), 197 checksums OK, no .DS_Store, validator OK, diff check OK (orchestrator re-verified). Committed as docs(adh) and opened as a PR.
