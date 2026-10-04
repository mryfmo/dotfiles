# Acceptance: dotfiles-T68-gate-audit-evidence-a01

- **Decision:** ACCEPTED after two revise rounds (one code, one artifacts-only). PR #246 squash-merged to `main` as `f32f33a0`; final head `4fe3427f293897fdd17b9cbde940713ae310dec5` (substantive commits abf9933f, 83074eea, 22efc32c, 46f14681, 5168613a; base 138e6a72; update-branch merges 3ba270d6 onto 8922f13b and 4fe3427f onto 312fef3f). Merged without `--delete-branch`; worker-d holds `feat/gate-audit-evidence`.
- **Worker:** `claude-standard-dot-a006` (worker-d). task_rev chain (`3959867c…`, `fcbe596a…`, `7d991601…` unhashed at the time and stated so, round-1 and round-2 revs `de14890f…`) verified in the validation file. Parallel wave with T88 (same worker, sequential), T65/T92 (a007), T75/T91/T74/T71 (a005).
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 2, dotfiles-T68 (principle 10 / §2b-6: acceptance without a task-level audit is stopped mechanically).

## What was accepted (`scripts/require-crit-review.py`, its test, the pr-integration rule bullet and its Codex mirror)

- With `BASE`, a review-triggering diff that is not `.orchestration`-only also requires `AUDIT_EVIDENCE`: repo-local under `.orchestration/validation/`, named `<task>-audit-<sha7..40>.md` with the feedback JSON's `<task>` and a sha prefix of HEAD, checked on the given and the link-resolved name.
- The verdict comes only from codex's final message `<audit>.md.last.md`, which must exist with content; its resolved name must be this audit's own companion (same task, sha prefix of HEAD). The transcript fallback was removed in round 1 after the task-level audit of 3ba270d6 showed it accepts quoted text and a symlinked companion.
- `correct` passes; `blocked`/missing fail; `incorrect` needs ≥1 `[P0-P3]` finding and `AUDIT_DISPOSITIONS` under `.orchestration/acceptance/` with exactly one numbered `audit-finding: <n> … not-applicable:<≥20 chars>` line per finding; `fixed:` is rejected because it moves the head.
- Rule bullet and Codex mirror name `herdr-agents --audit <head-sha> --task <task>` and the contract above. 69 tests.

## Decisions taken during the rounds

- PONG 1: the Codex AGENTS.md gate bullet joined the allowed files (Japanese mirror of the rule). PONG 2: root AGENTS.md:51, the SKILL step 10, the gh-first-workflow step 8 and the Makefile comment are rewritten by T69, not here (SKILL also in flight on this worker's T88 branch).
- Round 1 (task-level audit of 3ba270d6, incorrect): companion symlink to another task's audit passed (P1), transcript fallback accepted quoted text (P1), empty companion fell back (P2), CompactionDB command recorded as a placeholder (P3) → companion name bound to task and HEAD, `.last.md` required, fallback deleted, real command pasted. The Bot's request to restore the fallback (4176238899) is refused by decision.
- Round 2 (task-level audit of 5168613a, incorrect on evidence only): learning note stale, task_rev verification outputs missing → artifacts corrected, head unchanged; re-audit `correct`.
- Update-branch onto 312fef3f (T91) produced head 4fe3427f; its task-level audit and the Bot each raised the provenance point below.

## Orchestrator re-derivation

- Read every hunk of the gate at 3ba270d6 and the round-1 diff; traced `audit_errors` → `audit_name_error` → companion checks → verdict → `audit_disposition_errors`, and the `.orchestration`-only exemption through `paths`. The gate at this PR's own head is the one that ran for its integration, so the new requirement was exercised live here.
- Consequence accepted: from this merge on, every code PR needs a task-level audit of its final head, including after each `gh pr update-branch`; the repo copy of `herdr-agents --audit --task` produces it until `make update` deploys T67.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 4fe3427f | incorrect (2) → both not-applicable below |
| task-level, 5168613a (after artifact corrections) | correct |
| task-level, 5168613a (first pass, kept as `.round1`) | incorrect (2 evidence points, corrected) |
| task-level, 3ba270d6 | incorrect (4) → fixed in 5168613a |

audit-finding: 1 forged `.last.md` with the right name and `Verdict: correct` is accepted → not-applicable:the gate validates the shape of evidence, not its provenance, by documented design (AGENTS.md "Agent Review Evidence": process evidence, not reviewer authentication); it runs in the orchestrator's own review checkout on evidence the orchestrator produced with `herdr-agents --audit --task` and copied there itself, never on branch content; authenticating the audit run is a separate design and merge authority is being separated by account in dotfiles-T90
audit-finding: 2 evidence files named the previous head 5168613a and lacked the new Bot thread → not-applicable:the auditor read the pre-update snapshot; the sweep, receipt and this record were re-collected at 4fe3427f after the audit ran, the new P1 thread 4176326182 is dispositioned as finding 1 and resolved, and the gate at 4fe3427f checks the re-collected evidence
- Codex Bot: eleven threads over the PR; eight fixed in-PR (83074eea, 22efc32c, 46f14681), three not-applicable (T69 owns the other gate mentions; the transcript fallback stays removed; provenance is documented design), all replied and resolved. Sweep (head 4fe3427f): all items dispositioned, no failure or warning items. Gate at 4fe3427f with `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS=<this record>`: exit 0 ("Audit evidence accepted") once the two `audit-finding:` lines were written at line start, since the gate skips a bulleted line; evidence copies removed.

## Follow-ups

- dotfiles-T93: the gate compares feedback bodies after secret masking; NUL bytes in `.orchestration` text fail the scan instead of skipping.
- dotfiles-T69: the remaining gate mentions and the acceptance order (sweep → task-level audit of the final head → record → gate → merge → ACCEPTANCE).
- Provenance of audit evidence (signed verdict or trusted invocation from inside the gate): design question for the operator, not a task yet.

## CompactionDB

- Worker decision `5a73b2dc-d0e5-42aa-b935-87078b55547a`; cited. Orchestrator amendment: the verdict source is `.last.md` only (no transcript fallback) and `audit-finding:` disposition lines are numbered and start at column one.
