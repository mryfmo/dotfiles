# Learning triage: dotfiles-T128-regime-counters-a01

Candidates only; nothing promoted.

1. [memory:decision] The design-review RESULT that accepts a redesign carries the review task's `task_id` (dotfiles-T128-design-review-a01), not the redesign task's (dotfiles-T128-regime-v3-a01), so a reset anchor binds the hash to the redesign task's file content (sha256 of `.orchestration/tasks/<redesign_task>.md`), not to the RESULT's `task_id`. Applies to V3a's gate, which reads the same reset records. Candidate for the reset-record format (a `design_sha256:` front-matter line).
2. [memory:decision] Acceptance records need a machine-readable `pr=<n>` line for the INV-6 merged-PR anchor; "PR #312" inline is not read. Candidate for the acceptance-record template / accept-task.py (INV-9).
3. [memory:failure] A Claude worker push in this repo needs `GIT_CONFIG_GLOBAL=/dev/null` plus the gh credential helper: the global `pushInsteadOf` rewrites HTTPS to SSH and the sandboxed seat has no SSH key; a username in the URL (`https://user@github.com/...`) makes the gh helper answer nothing. Candidate for Worker Playbook step 2 (push mechanics).
4. [memory:failure] Unit tests that `git commit` in a fixture fail in a Claude seat's sandbox (global SSH signing, `~/.ssh/id_ed25519*` read-denied): 78 tests on `origin/main` alike. `GIT_CONFIG_GLOBAL=/dev/null make unit-test` is the local workaround; a candidate rule is for test fixtures to pass `-c commit.gpgsign=false` (as test_check_regime_boundary.py does).
5. CI's shfmt runs `-i 4 -sr` (no `-ci`); a local `shfmt -d` without those flags passes code CI rejects. Candidate: name `shfmt -i 4 -sr -d` in the task validation template.
6. Under INV-6's literal rule every review round is a RESULT, so review tasks cross `revises >= 2` routinely (dotfiles-T128-design-review-a01: 26). For the orchestrator: whether review tasks are in scope of the reset rule is a design question (INV-7), not a counter change.
