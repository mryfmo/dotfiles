---
{
  "audit_findings": [],
  "dispatch": [],
  "format": 1,
  "head": null,
  "ledger": [],
  "pr": 412,
  "replans": {},
  "searches": [],
  "task": "dotfiles-T129-anthropic-auth-route-check-followup-a07"
}
---

# Acceptance record: dotfiles-T129-anthropic-auth-route-check-followup-a07

Reset of the D lineage's a05 (PR #412, branch tools/anthropic-auth-route-structured, from 2b6fc7fc) after the security review of the rebase-repair head found a P1 (template-classification-gap) at the C-61 cap; the a05 record holds the decision and the class table. Text designed by the review-profile context (`.agents/worklog/orchestrator-glue/redesign/d-a07r2.md`, prompt `d-a07r2-redesign-prompt.md`): structured templates classified as their kind with inert placeholders for template directives and refusal on parse failure; list-container fences as top-level fences (the a06 row moves here); `make unit-test` installs PyYAML deterministically (Makefile in allowed_files); the a05 work, the redaction fix, the rebase repair and the evidence stay. Seat: a012 (Codex, worker-g). Advisory owner: dotfiles-T129-anthropic-auth-route-check-followup-a08 (written when the first row appears).

- 2026-10-19T07:23Z: redesign output (259 lines) installed as the task text; `task-consistency-check.py: OK`; C-80 review started.
- 2026-10-19T07:30Z: C-80 first review of the a07 text (`…-text-security-2707add.md`): `Verdict: incorrect`: P1 fixed git arguments do not sanitize discovery (an inherited GIT_INDEX_FILE naming a missing file makes ls-files return zero paths with exit 0 and the scan is skipped without refusal); P1 the template-parsing test cannot close 5.14 item 4 (no consumption binding); P1 the contract is cited from an uncommitted, unhashed path (the quoted sentences, not the path, must be normative); P2 symlink skipping is input filtering, not item 3's trusted-path control; P2 rows exist only for items 2 to 4, not 1 to 10. Root cause of the third P1 (mechanism): C-86 let a text bind its contract by path; the proper binding is inline quotation (C-88). Decision: revision by the review-profile context (prompt `d-a07r3-redesign-prompt.md`) with the five findings as items; C-80 again before dispatch.
text-security:2707add:1	git-discovery-env
text-security:2707add:2	consumption-binding
text-security:2707add:3	design-binding-by-path
text-security:2707add:4	trusted-path-control
text-security:2707add:5	threat-row-coverage
- 2026-10-19T08:23Z: C-80 second review (the a07r3 text; `…-text-security-*.md`, newest): `Verdict: incorrect`: P1 an explicit `--work-tree` makes `--show-toplevel` insufficient (a redirected `.git` pointer or symlink selects another index whose `home/` listing omits forbidden inputs); P2 the Completion clause is imported by path from the hold-playbook text, which is not on main (C-88 applies to every normative clause imported from a text not on origin/main). Decision: round 3 by the review-profile context (prompt `d-a07r4-redesign-prompt.md`): git metadata authentication (real `.git` directory, common-dir and git-dir realpath equality, core.worktree unset, listing cross-checked against a filesystem walk) and the Completion clause embedded verbatim.
text-security:a07-r2:1	git-metadata-trust
text-security:a07-r2:2	design-binding-by-path
- 2026-10-19T08:3xZ: sequencing (the project-map update of 17:27 JST flagged it): P1-15 amendment 2 added scripts/validate-agent-assets.py and tests/unit/test_validate_agent_assets.py to its allowed_files and P1-15 already edits the Makefile, so a07's three code files overlap an in-flight task (the pairwise-disjoint rule); the a07 text gains `after: [dotfiles-T133-worker-write-boundary-a01]` when its round-3 text is installed, and its design citation becomes `$HOME`-relative (C-86 amended). a012 holds until P1-15 merges.
- 2026-10-19T09:09Z: round-3 text (`d-a07r4.md`, 311 lines) installed: git metadata authentication (real `.git` directory, common-dir and git-dir realpath equality, `core.worktree` unset, the listing cross-checked against a filesystem walk) with its refusal tests; the Completion clause embedded verbatim (no import from a text off main); `after: [dotfiles-T133-worker-write-boundary-a01]` (shared code files); design path `$HOME`-relative. Checker OK; C-80 round 3 started.
- 2026-10-19T09:12:23Z: C-80 third review (`…-text-security-066254d.md`): `Verdict: incorrect` on one P1: the walk cross-check lets an untracked credential-bearing file be omitted when an uncommitted `.gitignore` rule in the working tree matches it (git reads working-tree patterns), with every metadata check passing. Class table: round 1 git-discovery-env (GIT_INDEX_FILE), round 2 git-metadata-trust (.git redirection), round 3 ignore-rule-trust — three rows of one family, trusting git to enumerate the inputs: INV-6 S1. Re-plan: the validator enumerates by walking the filesystem under the fixed roots home/ and install/ and scans every regular file (ignored and untracked included); git is consulted only to confirm the root; ignore rules are no exclusion authority (design 5.14 item 3 amended). Round 4 by the review-profile context (prompt `d-a07r5-redesign-prompt.md`).
text-security:066254d:1	ignore-rule-trust
re-plan: git-input-trust (3 rows: text-security:2707add:1, text-security:a07-r2:1, text-security:066254d:1) — specification: the a07 text let git enumerate the applied files; design: 5.14 item 3 now requires enumeration by filesystem walk under fixed roots with git only confirming the root; implementation: the round-4 text replaces the discovery item; verification: tests with a bogus GIT_INDEX_FILE, a redirected .git, and an untracked credential file hidden by an uncommitted .gitignore rule, each a finding.
- 2026-10-19T09:22Z: round-4 text (`d-a07r5.md`, 314 lines) installed: enumeration by filesystem walk under home/ and install/ (every regular file, ignored or untracked included; symlinks skipped and reported), git only confirms the root; tests for the hidden-by-.gitignore credential file, a bogus GIT_INDEX_FILE and a redirected .git; checker OK; C-80 round 4 started.
- 2026-10-19T09:25Z: C-80 fourth review of the a07 text (round-4 text, `…-text-security-05b8851.md`): `Verdict: correct`. The text waits for its prerequisite (`after: [dotfiles-T133-worker-write-boundary-a01]`: shared code files and D-024-20); a012 holds; dispatch with pasted counters once P1-15 merges.
- 2026-10-19T21:33:05Z: `after:` retargeted from the withdrawn dotfiles-T133-worker-write-boundary-a01 (PR #431 reset) to its reset successor dotfiles-T133-worker-write-boundary-a02; one line, same length, body unchanged (sha256 35bbd9fa1040… -> 3260aa6c9a32…; the C-80 verdict on the body stands); checker OK. Found by the project-map pass at 06:30 JST.
