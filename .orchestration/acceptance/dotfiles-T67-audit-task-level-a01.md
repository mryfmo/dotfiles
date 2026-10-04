# Acceptance: dotfiles-T67-audit-task-level-a01

- **Decision:** ACCEPTED. PR #242 squash-merged to `main` as `57885db1` (final head `9476141f9d0d5405a0bf0d53f8a8c261e9ddf385`; substantive commits 28373e27 and 9476141f; update-branch merge 58f5677a; base `3a0816e6`). Merged without `--delete-branch`; worker-c holds `feat/audit-task-level`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `df653369…` matched.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** Phase 2, dotfiles-T67 (principle 10 / §2b: task-level auditor, one run per final head). Operator's parallel-execution decision names this as the main efficiency lever.

## What was accepted (3 files, +188/−11)

- `herdr-agents --audit <sha> --task <id>`: id validated as one path segment (explicit empty refused); `.orchestration/tasks/<id>.md` and `git merge-base origin/main <sha>` required before any Herdr call (exit 2 with the path / a fetch hint); report/validation/sandbox named as `<id>.md` or `<id>.txt` (Codex P1 fixed in 9476141f), `<id>-pr-feedback.json` when present; prompt = three dimensions (specification conformance, implementation, evidence reality) over `git diff <base> <sha>`, naming the Bot's code-review and security-review threads as inputs; default output `<id>-audit-<sha7>.md`; no-task path, exit-marker, masker trust guard and verdict regex unchanged. README audit section documents the one-audit-per-final-head rule.
- Tests: four new tests plus two subtests, each failing against the old launcher; 726 unit tests OK.

## Audit / Bot / sweep / gate

| commit | verdict | findings → disposition |
|---|---|---|
| 28373e27 | incorrect | P2 `.md`-only artifact discovery → fixed:9476141f |
| 9476141f | correct | — |

- Codex Bot: 1 P1 thread (same finding) fixed in 9476141f, replied and resolved; thumbs-up on 28373e27 and 9476141f. Sweep (head 9476141f): 9 items, 0 failure/warning, all dispositioned. Gate at 9476141f exit 0 with evidence copies, copies removed.

## CompactionDB

- Worker decision `0de2f024-59c6-48dd-ba90-b85a669cc0cc`; cited.

## Procedure change from here

- After the operator's `make update` deploys the launcher, every acceptance runs `herdr-agents --audit <final head> --task <id> <main DIR>` once (per-commit audits only as a fallback when a head verdict is `incorrect` and the commit split matters). T68 adds the gate check for the audit file; T69 writes the procedure into the SKILL.

## Note

- Sandbox artifact: the main checkout holds a 0-byte read-only `.git/config.lock` (the sandbox's write-deny mount point); unsandboxed git config writes there fail (`push -u` warns, the push lands). Plain `git push` is unaffected.
