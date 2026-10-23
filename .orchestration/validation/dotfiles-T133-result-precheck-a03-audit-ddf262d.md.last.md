- [P2] high implementation scripts/orchestrator/result-precheck.sh:103 — `--blob HEAD:../../victim` escapes the temporary scan directory. Shell redirection truncates `$TMPDIR/victim` before `git show` rejects the path; validate traversal segments before creating the destination.
- [P2] high implementation scripts/orchestrator/result-precheck.sh:235 — If proof-worktree creation fails, `set -e` exits before log masking. The EXIT trap removes only temporary work files, leaving captured check output—including possible credentials—unmasked under `.orchestration/`.
- [P2] high orchestration .orchestration/acceptance/dotfiles-T133-result-precheck-a03.md:90 — The final branch update retains precheck evidence for `024ba0eb`, although `ddf262d` changes paths outside this task’s evidence directory. The final-head checker explicitly rejects that ancestry; the earlier deferral does not satisfy the task’s evidence requirement.

INV-6: holds .orchestration/dotfiles-T133-result-precheck-a03/revise.yaml:4 — One amendment and one revise are recorded, below the reset thresholds.

Orchestration findings: 1

Verified [PR 411](https://github.com/mryfmo/dotfiles/pull/411) CI success, task-copy identity, log hashes, and both change caps. Nothing modified.
Not rerun: local test suites or live hooks; file truncation, unmasked logs, and stale final-head evidence remain unresolved.

Verdict: incorrect