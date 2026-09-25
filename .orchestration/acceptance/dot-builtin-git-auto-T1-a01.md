# Acceptance — dot-builtin-git-auto-T1-a01

Decision: accepted
Date: 2026-09-21
Reviewer: claude-deep-dot (A1 orchestrator)

setup.sh now passes --use-builtin-git auto to chezmoi init and update,
matching the upstream default (builtin git only when git is absent).
Grounding: chezmoi docs (useBuiltinGit default auto), twpayne/chezmoi#4647
(maintainer: builtin git weaker than real git), go-git#358 (spurious
non-fast-forward pull), plus one observed occurrence during #160 E2E.

Verification: VM proof of both paths (git-present uses system git via
logging wrapper; git-absent still bootstraps via builtin git); statics
green (A4 re-run); bats assertion updated; PR #161 CI ALL-GREEN.

This closes watch item (1) from the Ubuntu bootstrap acceptance record.

cost: n/a
