# Learning triage: dotfiles-T129-audit-inherit-replan-json-a01

These are candidates only; nothing is promoted.

1. [memory:failure] On this host the gate suite (`tests/unit/test_require_crit_review.py`) fails 132 tests on an unmodified `origin/main`: its `setUp` runs a bare `git init` and `git commit`, and the global git config signs commits with a key that is absent and sets no `init.defaultBranch`. Run it with `GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=init.defaultBranch GIT_CONFIG_VALUE_0=main GIT_CONFIG_KEY_1=commit.gpgsign GIT_CONFIG_VALUE_1=false`, CI's settings; `git rebase` in a seat needs the same signing override, or its commit step fails with `failed to write commit object`.
2. [memory:decision] A fact several tools read lives in one structured place (here the record block's `replans` object), validated by its writer and refused by its reader when malformed; no tool parses a prose line, so two tokenizers cannot disagree.
3. [memory:decision] An inherited artefact keeps the marker of the run it came from, so a second inheritance does not move the ids its ledger rows carry.
