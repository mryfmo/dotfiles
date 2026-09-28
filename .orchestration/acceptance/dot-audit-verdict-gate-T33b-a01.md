# AGMSG-ACCEPTANCE dot-audit-verdict-gate-T33b-a01

## Revision 1 — REVISE (2026-09-28)

RESULT 2026-09-28T05:05:28Z from claude-standard-dot-a005 (worker-c): status=ready_for_review, PR #197 head 05f689bcfadce47154e3fc4a3df965975a021e40, branch fix/audit-verdict-gate from origin/main 4e112fd.

### Adversarial review (orchestrator, from origin refs)

- Scope: 4 files (+97/−9), all allowed. Prompt passed as one `%q` word after `--commit`; gate reads the evidence file; AGENTS.md verdict line tightened; README updated; 17 audit tests, mutation baseline 7/17 FAIL against origin/main; 490+ unit tests OK; CI 12/12 pass. CompactionDB 4c1c333d present.
- Orchestrator finding (before the audit landed): the `Review blocked` substring match runs over the whole evidence file, which contains tool output with repository text (T32 live evidence: 16 lines of `AUDIT-EXIT` from a diff; the audit of this very PR: 12 lines containing `Review blocked` from its README/tests). The merge commit of this PR would fail its own live E2E as a false `blocked`. The worker disclosed the choice ("errs toward fail-closed") — the task text prescribed the substring match, so the defect originates in the orchestrator's task detailing.

### Pre-merge Codex audit (head 05f689b, VISIBLE LANE)

Evidence `.orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit.md`.
1. **P1** — codex 0.157.1 rejects `--commit` together with `[PROMPT]` (`error: the argument '--commit <SHA>' cannot be used with '[PROMPT]'`, exit 2). Orchestrator reproduced on the real CLI. Every audit through the merged script would fail before reviewing. Root cause: revision-1 task text asserted the PROMPT was supported after reading `codex review --help`, which lists both but not their conflict; the worker could not verify (codex invocation forbidden) and said so. ACCEPTED → drop the prompt; AGENTS.md Audit section (tightened in this PR) is the only instruction channel; a missing verdict still exits 1.
2. **P2** — parse the verdict only from the final assistant response (the last `codex` transcript block), not the whole file; both false-`correct` (fixture in an exec block) and false-`blocked` (commit message quoting the phrase) reproduce. ACCEPTED; matches the orchestrator's own finding above.

**Decision: REVISE (one consolidated round, revision 2 dispatched).** Both defects trace to the orchestrator's task text, recorded here as such.

## Revision 2 — REVISE (2026-09-28)

RESULT 06:19:20Z: revision 2, head 1c87ba0d463a84ba4337fb9998b1d5f6d6ece33b. Orchestrator review: PROMPT fully removed (`git grep` clean, pasted); parser reads the last `codex` transcript block; 16 audit tests re-run OK at 1c87ba0 in the orchestrator-review worktree; mutation baseline vs 05f689b pasted; 491 unit tests OK; CI 12/12 pass; the extractor run by the orchestrator against two real transcripts isolates the final message; CompactionDB rev1 record retracted and 2b00aef2 added.

Visible-lane Codex audit of 1c87ba0 (evidence `-audit-rev2.md`): **P2** — the extractor resets on every exact `codex` line and stops at `tokens used`, so a final message quoting a fenced transcript (`codex` / `Verdict: correct` / `tokens used`) followed by the real `Verdict: incorrect` passes the gate; reproduced by the auditor with the commit's exact awk program. Orchestrator: confirmed as a real weakness (quoting this script's own test fixtures in a review is plausible). The revision-2 task text specified the `tokens used` stop, so the defect again originates in the task detailing. ACCEPTED → revision 3: region = after the LAST `codex` header with no `tokens used` stop; the LAST whole-line verdict wins; `Review blocked` only when no verdict line exists; residual (auditor's own final message is trusted) documented.

**Decision on revision 2: REVISE (revision 3 dispatched).**

## Revision 3 — ACCEPTED (2026-09-28)

RESULT 06:44:36Z: revision 3, head a5caef87d266ac8b812c43f53be624d7d5efed75, one commit a5caef8 (script + README). Region = after the last `codex` header, no `tokens used` stop; last whole-line verdict wins; `^Review blocked` only when no verdict line; residual sentence in README. 16 audit tests re-run OK at a5caef8 (orchestrator-review worktree); mutation baseline vs 1c87ba0 shows cases j (quoted transcript then `Verdict: incorrect`) and k (`Review blocked` mid-text then `Verdict: correct`) failing on the old parser; 491 unit tests OK on the second run (permgate bench flake, third occurrence, T33d queued); CI 12/12 pass. CompactionDB rev2 record retracted, 4f05242e current.

Visible-lane Codex audit of a5caef8 (`-audit-rev3.md`): "No actionable defects introduced; the parser matches the documented last-verdict behavior; all 11 committed verdict fixtures passed in isolation." No findings to disposition.

### Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-audit-verdict-gate-T33b-a01-receipt.md (resolved review-scope approval record r_7b523f, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-audit-verdict-gate-T33b-a01-crit.json).

**Decision: ACCEPTED.** Merge #197 --squash (no --delete-branch while worker-c holds the branch); deploy the script with a single-target `chezmoi apply` from the canonical clone; live E2E `herdr-agents --audit <merge-sha>` through the verdict gate — the first observation of whether gpt-6-astra emits the `Verdict:` line under the tightened AGENTS.md (a `missing` result is the designed fail-closed outcome and is recorded, not hidden).

[memory:decision] T33b accepted 2026-09-28: herdr-agents --audit gates on the auditor's verdict — region after the last codex transcript header, last whole-line `Verdict: correct|incorrect|blocked` wins, `Review blocked` counts only without a verdict line, anything but correct exits 1 even when codex exits 0; no review PROMPT (codex 0.157.1 rejects it with --commit), AGENTS.md Audit is the only instruction channel and requires the exact final verdict line. PR #197 squash-merged.

cost: n/a (worker report gives no token figures)

### Live E2E (orchestrator, pair workspace wJ, script deployed via single-target chezmoi apply after merge 1d0883f)

`herdr-agents --audit 1d0883f --out .orchestration/validation/dot-audit-verdict-gate-T33b-a01-live-e2e.md --timeout 560` → audit tab reused (tabs unchanged), real gpt-6-astra audit 1m33s, `Audit exit: 0`, **`Audit verdict: missing`, exit 1**. The gate worked exactly as designed: the auditor's final message contained no whole-line `Verdict:` even under the tightened AGENTS.md Audit section. Observation: 6 of 6 live audits so far omit the verdict line, so the AGENTS.md channel alone does not steer `codex review`'s built-in output format; until that is fixed every visible-lane audit will end `missing` and the orchestrator judges the evidence manually (the pre-T33b status quo, now made explicit instead of a silent `Audit exit: 0`).

Post-merge live audit finding on 1d0883f (dispositioned): **P2** — a quoted `Verdict: correct` inside a fenced example with no concluding verdict is accepted (the documented residual, but the auditor's stricter reading is right: the verdict should be the message's concluding non-blank line). ACCEPTED → folded into the follow-up task with the instruction-channel fix.

Follow-up (dot-audit-exec-channel-T33e-a01): replace `codex review --commit` by `codex exec` with an explicit prompt (AGENTS.md Audit section + `git show <sha>` scope) and `--output-last-message <file>` as the structured final-message channel, so the verdict instruction actually reaches the model and the gate parses a file that contains only the final message (concluding-line rule). T33b's acceptance stands: its deliverable — fail closed on a non-assessed or verdict-less audit — is verified live.
