# Acceptance — dot-ubuntu-fix-T1-a01

Decision: accepted (after 3 small revise cycles)
Date: 2026-09-21
Reviewer: claude-deep-dot (A1 orchestrator)

Scope: unblock README Ubuntu bootstrap on fresh machines + Japanese
environment. All findings were reproduced facts from real runs on a fresh
Ubuntu 26.04 arm64 VM (evidence: .orchestration/validation/ and VM logs).

Delivered: no interactive gh login in bootstrap; mise v2026.9.12 pin fixing
uv/yazi bin resolution (before/after VM proof); busybox/ubuntu-standard
removal fixed; LANG respect + ja_JP.UTF-8 generation (client+server) +
language-pack-ja/fonts-noto-cjk/fonts-noto-color-emoji/ibus-mozc on client;
non-tty age guard; pinned GitHub host key; docker keyring --batch --yes
idempotency; standard source guard in ssh.sh; README notes; bats updates.

Verification: A4 re-ran shellcheck/shfmt/bash -n/supply-chain unit (17) —
green. Branch E2E on fresh VM users: server EXIT=0, client EXIT=0 (rerun
path with existing keyring also EXIT=0). Japanese outcomes measured on the
E2E machines (ja_JP.utf8 present; packages installed; uv executes).
PR #160 CI: ALL-GREEN (bats via GitHub Actions per repo policy).

Observed once, not reproduced: chezmoi builtin-git "non-fast-forward
update" on a rerun; tracked as a watch item, not blocking.

cost: n/a
