# Sandbox and execution boundary

All worker commands ran inside the Codex workspace-write sandbox. No escalation, broader permission, host-only execution, merge, deployment, browser review or review publication was attempted. Worktree writes are limited to the three allowed source/test files and this artifact directory. Git objects/refs/logs and this worktree's Git administration are enumerated writable roots. The agmsg skill authorizes task messages; provided scripts and agmsg-dispatch were used, not direct storage access.

Worklogs use this task directory because .agents is read-only; timestamped plan/todo/learn files remain uncommitted. Required task/report/validation/sandbox/learning/measure/autoskill and worker review evidence must be committed before RESULT. Unrelated existing untracked predecessor artifacts and cache directories are preserved and excluded from the fresh PR. The task snapshot is byte-identical and must not be masked or edited.

Current task prerequisites were checked through the fixed github.com repository API: #435 merged true; pinned main60a6fb2b324d0381c4a6e539b37c650105154a7e; decoded canonical design SHA2563086424908f103ca8bd9ab7f0498930e382e620508756dcc304b12725e0bd797. Ref, contents, base64 decode and exact grep stages each succeeded. Local refs supply checkout data, not publication or approval authority.

Fixtures use real temporary Git repositories, private absolute temporary caches, the actual isolated native Python/uv launch, synthetic tokens observed only by SHA256 and API responses with no live authority. Actual local bindings are Python3.15.0 and3.12.15 plus uv0.13.1. Both deterministic and native case-insensitive filesystem controls were exercised; native-case-insensitive=True on this host. Windows/native case-sensitive platform coverage is not claimed. No local Bats run occurred.

Checker defenses begin after PATH-selected mise/uv and cached dependencies execute. The unchanged parent retains PATH/shared cache and may already have executed attacker-controlled input. Resolver validation, absolute-cache syntax and fallback warnings do not close that boundary. Parent dispatch hardening is owned by dotfiles-T133-loop-limits-a01, executable binding by dotfiles-T133-trusted-entrypoint-binding-a01, resolver/private cache by dotfiles-T133-ci-efficiency-followup-a04. Shared UID, credentials, cache poisoning and concurrent same-UID replacement remain owned residuals; this task establishes no host isolation.

No Crit daemon or plan session was started. crit status --json showed daemon.running=false, sessions=[], review_file_exists=false. A fresh-context independent review and worker receipt are saved under the worker evidence names; four findings were resolved after the owner recorded re-plan:glob-filter worker:d0ad49f:1-4. The agent review gate passes. It supplies no integration authority or final security audit. A separate downstream fixture migration blocker is reported rather than editing tests/unit/test_regime_ci.py outside allowed_files or weakening retained C13.

The root assigned that fixture migration to dotfiles-T133-regime-ci-fixture-grammar-a01 and authorized publication/CI on2026-10-20T04:29:33Z with its red disclosed; the worker performs no update-branch. Round2 removed token-bearing env argv in favor of direct validated-binary execution with the same clean env mapping. Synthetic argument observations and a fresh security-profile worker review verify that repair; source395/test562 additions22 deletions. No credential-isolation or parent-boundary claim follows.

## Owner2754 authorized runtime rebuild, blocked by unavailable network

The old temporary parent-bin and Python312 installation disappeared. Owner2754 classifies that environment loss as no review/correction round and authorizes the same native-uv/CPython3.12.15 temporary reconstruction. The new mode0700 parent bindings directory was successfully created at /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/a012-a05-runtime-ze2fbz0e/parent-bin. Its symlinks target the original /usr/bin/git, /bin/bash, native uv0.13.1 and GitHub CLI2.102.0; it changes no production caller/environment or boundary claim.

Python install uses an explicit TMPDIR-local install directory and --no-bin, so no optional home-bin alias write is attempted. Actual install exit1: download could not resolve github.com after uv's internal three retries. No alternative downloader, tool, network route, broader permission or retry was attempted. Complete command/output follows. Required Python312/module/mutation proofs and commit/push/CI remain held; only the R4 changed-file lint regression is currently verified after this patch.

````text
Owner2754 authorizes rebuilding missing temporary validation runtime; environment loss, no correction round.
Created mode0700 temporary directory /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/a012-a05-runtime-ze2fbz0e and parent-bin; symlinks to exact original native executables:
{
  "git": "/usr/bin/git",
  "uv": "~/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv",
  "gh": "~/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh",
  "bash": "/bin/bash"
}
Command: ~/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv --no-config --cache-dir ~/Workspace/dotfiles/.claude/worktrees/worker-g/.uv-cache python install --install-dir /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/a012-a05-runtime-ze2fbz0e/python --no-bin 3.12.15
error: Failed to install cpython-3.12.15-macos-aarch64-none
  cause: Request failed after 3 retries in 5.5s
  cause: Failed to download `https://github.com/astral-sh/python-build-standalone/releases/download/20261013/cpython-3.12.15%2B20261013-aarch64-apple-darwin-install_only_stripped.tar.gz`
  cause: error sending request for url (https://github.com/astral-sh/python-build-standalone/releases/download/20261013/cpython-3.12.15%2B20261013-aarch64-apple-darwin-install_only_stripped.tar.gz)
  cause: client error (Connect)
  cause: dns error
  cause: failed to lookup address information: nodename nor servname provided, or not known

exit=1

````

## Owner2757 supplied native Python312 binding

Owner2757 provided native host tool-manager Python3.12.15, no worker download. Absolute selected interpreter ~/.local/share/mise/installs/python/3.12.15/bin/python3.12; SHA256 3274dde21f9767655564d093e63c9a5faacefbf1d41bc1e6bf8b6f6e5a441903; rebuilt runtime link /private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/a012-a05-runtime-ze2fbz0e/parent-bin/python3.12. Probe exit0:
~/.local/share/mise/installs/python/3.12.15/bin/python3.12
3.12.15 (main, Oct 14 2026, 00:55:37) [Clang 23.1.3 ]

The host installation was performed by the orchestrator under its machine-hygiene exemption; this worker did not install outside the sandbox or download through another route. Both module suites and mutation proofs now use the validated native absolute interpreter or existing native315. Rebuilt parent-bin remains only fixture orchestration, no production launch change or parent-boundary closure.

## Post-publication transport disposition2761 (working-tree observation)

At2026-10-20T06:34:55Z the orchestrator reported that the rendered Codex sandbox has network_access=false (agent-config.yaml:115), while design5.14 item10 specifies true; a separate manifest task follows#431. This worker's native git push actually exited128 with github.com DNS resolution failure. No retry, alternate tool/route, broader permission or worker-side out-of-sandbox command occurred.

Under the orchestrator's interim integration exemption, the orchestrator transported the already committed branch head cedc7f5f4c6e211645aad344d9149de1c44e9b95 to tools/task-generator-plan-check-a05-checker / PR440 without changing any worker commit. This remote publication is reported by the orchestrator, not independently queried by the network-restricted worker. CI runs on that head and the orchestrator reads the results. Disposition2761 explicitly requests RESULT now at this exact head, naming the six separate RegimeCiTest reds owned by#441 and GitGuardian's synthetic-digest refutation. This overrides the worker's earlier wait-for-CI/transport hold; no new-head CI success or completed Bot review is asserted.

This section is a post-head observation, left as a working-tree-only update so the requested cedc7f5f head stays unchanged. All required original artifacts were committed in that head; the orchestrator can carry this observation in integration records. No merge, update-branch, feedback-thread resolution, final task audit, security acceptance or integration approval is performed by this worker.

Revise1 owner2768: all three security fixes and test writes remain in allowed files; original native315/312 and private fixture seeds reused, no network attempt. Unicode-sensitive identity is modeled, not native Linux. New source396/test613add22del; local commit/PONG only, root transport/CI under D-024-36. No caller/startup/cache/host-isolation claim.

Final revise1 local observations: clean selected-tree assets actually exit0 at6af61298778a0d3d52042e1568acefa3cc084218 with source/test hashes verified; refreshed worker gate actually exit0 with saved/read current JSON+receipt. Subsequent edits only record these results and measurements. Local commit/PONG follows owner2768; no new-head CI pass or integration approval is asserted.
