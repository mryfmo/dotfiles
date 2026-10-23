---
id: M-20261021-02
date: 2026-10-21
classes: [unsound-guard-spec, records-form]
severity: P1
---

# Boundary 26 carried 91 unmasked evidence files, a secret-pattern match and five files with NUL bytes

**What happened.** The records PR #447 (c1566ff5, 319 files) was assembled by hand (tar copy from the main checkout) instead of through `scripts/orchestrator/boundary.sh`, so the masker and `make validate-agent-assets` never ran before the push. The pre-push check that was supposed to count home paths used `xargs -a`, a flag macOS xargs lacks; the command failed and printed `home-path files: 0`, a false measurement. GitHub's `validate` check failed on four heads (c1566ff5, 3f15c423, cea358ea, e15dd575); the Codex Bot posted a P1 on the unmasked paths. Four follow-up commits masked 91 files, one secret-pattern literal and five files holding NUL bytes before 75828c96 passed.

**What the rules say.** AGENTS.md "Orchestration records": `.orchestration/**` is reviewed for secrets and home-directory paths. boundary.sh (plan 007 T718, C-13) masks the copies and runs the validator before committing. C-40: a new guard is probed once with a failing input before anything relies on it.

**Why the rules did not fire.** The boundary was hand-assembled because boundary.sh collects every `.orchestration` change and queues `gh pr merge --auto`, neither of which fit this boundary (explicit file list, no auto-merge); the hand-written replacement skipped the masking step and its guard was never probed.

**Mechanism.** `boundary-list.sh` (glue, re-plan v2 R0-10): explicit list only, task texts verified against the bus hash before copy, before commit and before push, records masked, validator required, 150-file / 5 MB caps, no auto-merge; its three refusal rules were probed with failing inputs on 2026-10-21 10:01 JST before first use. The repository version is task R1-8 of the re-plan (the records-sync lineage) with the same rules and tests.
