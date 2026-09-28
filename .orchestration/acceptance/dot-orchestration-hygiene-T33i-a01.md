# AGMSG-ACCEPTANCE dot-orchestration-hygiene-T33i-a01

RESULT 2026-09-28T22:06:36Z from claude-standard-dot-a005 (worker-c): status=ready_for_review, PR #204 head 18c7164a2455493657cca5dfd8f5e4f1b7409d52, branch fix/orchestration-hygiene-T33i from origin/main 013b3d6.

## Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- Scope: 7 files (+228/−8), all allowed. `validate-agent-assets.py --mask-secrets <files>`: line-level mirror of the committed-secret scan (allowed placeholders stripped before matching, `SECRET_PATTERN` and scan coverage unchanged, whole-text final pass for cross-line matches, exit 2 on a missing file, `masked <n> match(es) in <file>` per file). `herdr-agents --audit`: masks the transcript and last-message file after the exit marker and BEFORE the exit check and the verdict gate (lines 958 → 962 → 989), only when `DIR/scripts/validate-agent-assets.py` exists; a masking failure warns and names the file. Rule/SKILL: boundary-commit validation bullet (both), task-authoring discipline (a)(b)(c) in Playbook step 3. README: Understand-Anything 2.9.7 coverage-gap note and the masking sentence in the `--audit` paragraph.
- Orchestrator re-derivation at 18c7164: new validator and audit tests pass; `shellcheck -x` clean; `--mask-secrets` on the exact pre-masking evidence that turned main red (`git show 04746ca:…T33c…audit-rev2.md`) masks exactly 2 matches and the scan is clean afterwards; 518 unit tests OK; mutation baselines pasted (validator 3/3 and herdr 2/3 failing on the old code); the worker also self-checked its own artifacts with the new mode; PR CI 12/12 pass.
- CompactionDB: T33i decision present in the main-checkout DB.
- Refutation attempts found no correctness, security, or omission issue; live E2E of the mask step below.

## Pre-merge Codex audit (head 18c7164, VISIBLE LANE via codex exec) — `Audit verdict: incorrect`

1. **P1 (high)** — the mask step executes `DIR/scripts/validate-agent-assets.py` outside the read-only sandbox before the verdict, so "a malicious changeset can run arbitrary code and rewrite the evidence or final verdict". Orchestrator disposition: PARTIALLY REFUTED — in this lane `DIR` is the orchestrator's main worktree and the reviewed commit is only fetched, never checked out there, so the masker is trusted repo code at HEAD, not reviewed content. The residual is real whenever DIR sits at the audited commit or carries uncommitted changes to the validator → ACCEPTED as a hardening: guard on `git -C DIR rev-parse HEAD` ≠ audited sha and a clean validator file, else skip masking and fail closed; document the assumption.
2. **P2 (high)** — a masking failure is swallowed (`|| printf`), so an audit can end `correct` with unredacted evidence; the auditor replayed it. ACCEPTED: print `Audit verdict: unmasked` and exit 1 before the gate.

**Decision on revision 1: REVISE** (both items in one round; the P1 residual and P2 were the orchestrator's task text — "skip silently otherwise" and no failure semantics were specified).

## Revision 2 — REVISE (2026-09-29)

RESULT 22:34:22Z: head bb190d5f0dfe68820e7be37a21f250baaf8c4b9c (+117/−10). Fail-closed `Audit verdict: unmasked` on mask failure / missing python3 / refused masker; trust guard (DIR HEAD == audited sha, validator untracked or modified). Orchestrator: 25 audit tests OK at bb190d5, `shellcheck -x` clean, baseline shows both guard tests failing on 18c7164, 521 unit tests OK, CI 12/12 pass; CompactionDB base + rev2 addendum records present.

Visible-lane Codex audit of bb190d5 (`-audit-rev2.md`): `Verdict: incorrect`, one **P2** — deleting the tracked validator from the working tree makes the `-f` test false and takes the "repository has no validator" exception, so unredacted evidence can pass; reproduced with mocked git metadata. Orchestrator: CONFIRMED (the exception must come from git tracking, not the filesystem). ACCEPTED → revision 3: skip masking only when the path is not tracked at HEAD; tracked-but-missing fails closed; deleted-validator test.

**Decision on revision 2: REVISE.**

## Revision 3 — review in progress (2026-09-29)

RESULT 22:50:37Z: head 19941426f261f79ca66fd9556bac457f57688f8f (+1 commit). Mask exception now decided from git: skip only when `ls-files --error-unmatch` fails AND `HEAD:` lacks the validator AND nothing is on disk; tracked-but-missing (unlinked or `git rm`), untracked copy, changed vs HEAD, or DIR at the audited commit → `unmasked`, exit 1. Orchestrator: audit tests OK at 1994142, `shellcheck -x` clean, baseline vs bb190d5 shows both `deleted`/`removed-from-index` cases failing on the old code, CI 12/12 pass.

Lane incident: two `herdr-agents --audit 1994142` runs were refused ("audit pane wJ:p5 is busy") although `process-info` showed the pane's zsh as the only foreground process and `recent-unwrapped` ended at the prompt; the `visible` snapshot of the (recreated, background) audit tab was stale. Fallback per README: headless `codex --profile audit exec --sandbox read-only -C DIR -o <file>.last.md '<same prompt>'` recorded in `-audit-rev3.md`. Lane defect tasked as dot-audit-pane-prompt-detect-T33j-a01 (busy check from the foreground process, not a visible-snapshot regex).

## Revision 3 — ACCEPTED (2026-09-29)

Headless Codex audit of 1994142 (`-audit-rev3.md`, same prompt and `-o` channel as the lane): `Verdict: correct` — "the guard correctly rejects both filesystem deletion and staged removal of a tracked validator; regression tests cover both cases; documentation matches." No findings.

### Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-orchestration-hygiene-T33i-a01-receipt.md (resolved review-scope approval record r_7dcfaa, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-orchestration-hygiene-T33i-a01-crit.json).

**Decision: ACCEPTED.** Merge #204 --squash (no --delete-branch while worker-c holds the branch); deploy with a full `chezmoi apply` (rules, SKILL, herdr-agents are $HOME targets; the validator is repo-only); live E2E of the mask step on the next audit run (the T33j fix is needed before the visible lane reliably reuses the recreated pane); then dispatch T33j, then T19 revision 3.

[memory:decision] T33i accepted 2026-09-29: audit evidence is masked by `validate-agent-assets.py --mask-secrets` inside `herdr-agents --audit` before the verdict gate, failing closed (`unmasked`) whenever masking cannot be trusted or fails; boundary commits are preceded by `make validate-agent-assets` with a real exit check; task authoring grounds allowed_files by grep, verifies CLI constraints by execution, and presumes auditor findings right until refuted. PR #204 squash-merged.

cost: n/a (worker report gives no token figures)
