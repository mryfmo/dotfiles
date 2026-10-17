# Sandbox record

All commands stayed in the worker worktree and managed writable roots, without escalation. New script execution in validation uses only SEAT_ARGS_PS/SEAT_ARGS_LSOF fixture binaries, temporary HOME/profile records and stub identities/storage/GitHub data. No actual ps/lsof, worker process/pane, re-seat, runtime/profile generation, task dispatch, graph update, memory promotion or main-checkout write.

UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache on uv commands. Git fixture signing is disabled only in the test process environment. Branch creation is --no-track; no shared Git config changes. Commit uses process-local commit.gpgsign=false because the sandbox cannot read the signing key; push uses the established one-command HTTPS identity rewrite. No approval escalation or classifier bypass. No Plan Mode/Crit server or local Bats.
