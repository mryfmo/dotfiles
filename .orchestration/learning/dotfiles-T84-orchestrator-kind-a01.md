# Learning: dotfiles-T84-orchestrator-kind-a01

- **Anchor a "currently" README check on a string only the new sentence has.** `worker_kind` and `orchestrator_kind` are both `claude`, so a check for ``(currently `claude`;`` alone would pass on the old sentence.
- **Grep every test that rewrites the README fixture.** `test_agent_manifest_requires_readme_to_document_restart_worker` replaces the README, so a new README requirement has to appear there too.
- **Run pinned ruff by its binary path from the repository root.** `mise -C <scratch> x ruff` resolves relative paths in the scratch directory, and ruff skips absolute paths under `.claude/`. `$(mise -C <scratch> which ruff)` works from the repo root.
- **Revise round 1: a new sentence can weaken a check that is already there.** I anchored the new orchestrator check but left the existing worker check on the bare ``(currently `<kind>`;``. The new sentence then satisfied that check. When adding text that contains a token another check matches, re-anchor that check too and add a test that pits the two sentences against each other.
- **Paste the executed command, not an echoed label.** The CompactionDB header line was an `echo` of a placeholder. Evidence needs the literal invocation and a readback.
