---
reviewed_at: 2026-10-11T02:49:10Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@3572107047ffd67012ac494d6d3ca4bb4100bd564e9ea1b78f3942f2c39435ca
task: dotfiles-T128-task-review-a201-a01
round: 1
files:
  - dotfiles-T128-ci-skip-orchestration-a01@1535efa3619206ac (prefix; full hash in the TASK line)
  - dotfiles-T128-v1-task-schema-a01@e858224cb37ed045
  - dotfiles-T128-v1b-pr-caps-a01@6e761ddab5ed238d
  - dotfiles-T128-v1c-regime-ci-check-a01@f8c4227ad4c69565
  - dotfiles-T128-v2-audit-schema-and-runner-a01@7ccc9a20ebc325fd
  - dotfiles-T128-v1-task-schema-contract-a01@50205b724bd4e78f
  - dotfiles-T128-v2-audit-schema-and-runner-contract-a01@070b68f43be82541
  - dotfiles-T128-process-rules-a01@6c4d233c180ba86e
verdicts:
  dotfiles-T128-ci-skip-orchestration-a01: "revise: A-1 step gating wording, A-2 schedule and push behaviour of the changes job"
  dotfiles-T128-v1-task-schema-a01: ready
  dotfiles-T128-v1b-pr-caps-a01: ready
  dotfiles-T128-v1c-regime-ci-check-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-a01: ready
  dotfiles-T128-v1-task-schema-contract-a01: ready
  dotfiles-T128-v2-audit-schema-and-runner-contract-a01: ready
  dotfiles-T128-process-rules-a01: ready
---

# Task-file review: A201 (ci-skip-orchestration) in full, seven files as pointer confirmation

Design v15 at 35721070. PyYAML check: every file's invariant equals v15 byte for byte (process-rules carries none, by design), every pointer names the round-15 receipt, every hash matches the TASK line; each -contract-a01 id resolves to its implementing entry. V0 is not in this round (in flight, pointer round 13, INV-12 v13 until its amendment).

## A201 (dotfiles-T128-ci-skip-orchestration-a01): revise

1. Design: implements INV-2 v15's CI clause, verbatim, map [INV-2]; design tier by its workflow paths and lists each changed workflow, as INV-1's refusal requires; after V0, which also edits test.yaml, so the shared file is sequential. No contradiction.
2. Premises: premise 1's sed half holds (test.yaml:5-6); its gh half and premise 2 are unverifiable from this seat. The seven contexts it names agree with the SKILL's seven required checks and leave macos.yaml and ubuntu.yaml out, which answers round 14's note.
3. allowed_files: complete for the two workflows and the test module. Touch point to name for the worker: tests/unit/test_workflow_security.py pins every uses: to a full commit SHA, exact top-level permissions per workflow file and persist-credentials: false on every checkout without an exemption, so the new changes job in remote.yaml copies test.yaml's checkout step verbatim and adds no job-level permissions. .github/workflows/agent-assets.yml is listed but item 1 says validate keeps running unchanged; drop it from allowed_files or say what changes there (an unchanged listed file is harmless under INV-1's (c) but reads as scope).
4. One invariant.
5. Worker questions INV-4 would otherwise produce:
   - A-1: item 1 says each bootstrap job gates on "a first step that exits early, not a job-level if". A step that exits 0 does not stop the steps after it; the mechanism that keeps a required context reporting is a step-level if: on every heavy step keyed to the changes output, which is what test.yaml does and what item 2's test asserts. Rewrite the sentence to that.
   - A-2: remote.yaml also runs on push and schedule. The changes job must say what it outputs there: push compares before and after as test.yaml does, and a schedule run has no diff and must run the bootstrap in full (output true). One sentence.
6. Contradictions: none beyond A-1. Note: the dormant contract PR dotfiles-T128-ci-skip-orchestration-contract-a01 that the First-commit section requires has no task file yet; it needs one and its own one-round review before A201 dispatches, since the contract merges first.

## The seven pointer files: ready

Pointer and sentence only; nothing else moved against the round-19 and contracts-round-3 bytes beyond the INV-2 v15 sentence in V1b, which is the expected change.
