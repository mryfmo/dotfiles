# Acceptance: dot-herdr-sheldon-T1-a01

status: revise
date: 2026-09-25
reviewer: claude-deep-dot (orchestrator, adversarial review)
cost: n/a

## Findings

- F1 (Makefile herdr reload protocol_mismatch tolerance + lifecycle.bats + README lifecycle text): correct; fixture trace shows both branches; applies cleanly onto origin/main (c5193e4).
- F2 (sheldon `client/ubuntu.toml` inline guarded source + setup.bats assertion): SUPERSEDED. origin/main 82d4961 "fix(sheldon): drop dead ubuntu-command local plugin" already emptied that file. The worker diff no longer applies (`git apply --check` fails on ubuntu.toml) and the new setup.bats test would fail against the empty file.
- Worktree base is 788ba3b; main is now c5193e4 (74 commits). The README hunk at ~L289 (herdr-agents attach description) conflicts with d004ddb/4d4767b (worker kind from manifest).

## next_action

After finishing dot-update-convergence-T1-a01: rebase `fix/herdr-reload-and-sheldon-client` work onto origin/main; drop the ubuntu.toml and setup.bats changes (superseded); re-merge the README hunks against the current text; re-run the reload fixture trace and unit suite; re-send AGMSG-RESULT.
