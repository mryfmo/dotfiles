# AGMSG-ACCEPTANCE dot-audit-pane-prompt-detect-T33j-a01

RESULT 2026-09-29T00:00:41Z from claude-standard-dot-a005 (worker-c): status=ready_for_review, PR #205 head 4b88402f2c8108d926f6720980dff387f16d9139, branch fix/audit-pane-prompt-detect from origin/main d7a5947.

## Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- Scope: 3 files (+110/−15), all allowed. `wait_for_shell_prompt` now treats `process-info` as authoritative: a single foreground process that is the pane's shell (pid == `shell_pid`, or a known shell name) means idle, with no snapshot regex; a non-shell/child foreground process still fails bounded (busy/stuck/exit-dialog paths for the worker pane unchanged). A drawn prompt is required only where a newly created pane needs it (`prompt` argument: pane splits, worker starts, and the first use of a newly created audit tab), read from `recent-unwrapped` with trailing blank lines dropped; without process-info the prompt text alone decides. README sentence added.
- Orchestrator re-derivation at 4b88402: full `test_herdr_agents` module OK (126 tests); `shellcheck -x` clean; mutation baseline pasted — the stale-visible-snapshot, no-process-info fallback, and new-tab-prompt cases fail on the unmodified script; 525 unit tests OK; PR CI 12/12 pass including macOS.
- Root-cause match: the incident (`visible` snapshot of the recreated background audit tab showing stale transcript lines while `process-info` reported only zsh) is exactly the case the new primary check covers.
- CompactionDB: T33j decision present in the main-checkout DB.
- Refutation attempts found no correctness, security, or omission issue; live E2E on the reused pane wJ:p5 below.

## Pre-merge Codex audit (head 4b88402) — headless fallback

The installed (pre-fix) lane refused the reused pane wJ:p5 again ("busy (not at a shell prompt)") — the exact defect under review — so the audit ran headless with the lane's prompt and `-o` channel: `Verdict: correct` — "the changes preserve busy-process rejection and fresh-pane prompt checks; seven in-memory behavior checks passed." Evidence `.orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-audit.md` (+ `.last.md`, masked with `--mask-secrets`: 0 matches).

## Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-receipt.md (resolved review-scope approval record r_00ff01, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-audit-pane-prompt-detect-T33j-a01-crit.json).

**Decision: ACCEPTED.** Merge #205 --squash (no --delete-branch while worker-c holds the branch); deploy with a single-target `chezmoi apply ~/.local/bin/common/herdr-agents`; live E2E: `herdr-agents --audit <merge-sha>` on the reused pane wJ:p5 that the old check refused — recorded below.

[memory:decision] T33j accepted 2026-09-29: herdr-agents decides "audit pane busy" from the pane's foreground process (the pane's shell alone means free), requires a drawn prompt only for newly created panes/tabs and reads it from recent-unwrapped, so stale visible snapshots of background tabs no longer block the audit lane. PR #205 squash-merged.

cost: n/a (worker report gives no token figures)

### Live E2E (orchestrator, pair workspace wJ, script deployed via single-target chezmoi apply after merge ca21c30)

- Run 1: `herdr-agents --audit ca21c30` on the reused pane wJ:p5 (the pane the old check refused twice) → busy check passed, audit ran 2m08s, tabs unchanged, auditor `Verdict: correct`; but the T33i trust guard refused the masker because DIR's HEAD *was* the audited commit (main had just pulled the merge) → `Audit verdict: unmasked`, exit 1. Correct guard behavior; wrong orchestrator target choice. Evidence masked manually afterwards (0 matches). Procedure change recorded in orchestrator memory: live E2E audits the PR head sha, never the merge commit DIR sits at.
- Run 2: `herdr-agents --audit 4b88402` (PR head; identical content, different sha) on the same pane → busy check passed, mask step ran (`masked 0 match(es)` in both files), **`Audit verdict: correct`, exit 0**, tabs unchanged. First fully green end-to-end run of the lane with masking and verdict gate together. Acceptance criterion met.
