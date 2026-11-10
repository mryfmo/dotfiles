# U354: `build_under_srt` resolves srt through `mise which`, never the mise shim, so the harness and superagent builds run on a real host

GOAL
On the macOS laptop at main 6ad1be23 (after `make deploy-kit`), `DSH_HOME=~/.dsh scripts/update-agent-assets.sh update_dsh_superagent` fails before any build: `mise ERROR Config files in ~/.config/mise/config.toml are not trusted` and then `update_dsh_superagent: the sandbox canary did not run under srt` (measured 2026-11-07T08:43Z and 08:47Z, /tmp/u317-stageA-install2.txt). Cause, reproduced in isolation: the updater's `main` prepends `~/.local/share/mise/shims` to PATH before every step (scripts/update-agent-assets.sh:3519 for a single step, :3529 for the full run), so `build_under_srt`'s `srt="$(type -P srt)"` (:1854) resolves to the mise shim `~/.local/share/mise/shims/srt`, not the binary; the shim is then started by `/usr/bin/env -i ... XDG_CONFIG_HOME=<store>/xdg-config XDG_STATE_HOME=<store>/xdg-state ... "${srt}"` (:1993-2000), and the shim's mise, with its trust store redirected into the empty store, refuses the global config and exits 1 (`~/.local/share/mise/shims/srt --version` under exactly that environment exits 1 with the same message; the binary `mise which srt` answers, `~/.local/share/mise/installs/npm-anthropic-ai-sandbox-runtime/0.0.81/bin/srt`, exits 0 with `0.0.81` under it). Every `build_under_srt` caller fails the same way on a real host: `update_deepseek_harness` (U322, the canary at :2408) and `update_dsh_superagent` (U317, :2664). CI never saw it because the tests fake srt on PATH. The fix is the one `build_under_srt` already applies to pnpm and node: resolve srt through `MISE_EXEC_AUTO_INSTALL=false mise which srt` with its status read, and hold it to an executable regular file; the second `type -P srt` precheck (:2765, update_dsh_superagent) takes the same producer.

SCOPE
A new branch `fix/build-under-srt-resolves-srt-through-mise` from main 6ad1be23; the tree is `/tmp/dotfiles-wt/U354`. May write: `scripts/update-agent-assets.sh` (the two srt resolutions and their header sentences), `tests/unit/test_update_agent_assets.py` (the build_under_srt harness and the superagent precheck test), `docs/reference/` only if generated from the header, and the body. Not: PATH handling in `main`; the shim; anything else.

CONTEXT
The harness `run_build_under_srt`-style helper in tests/unit/test_update_agent_assets.py (near line 1037: `stubs = 'mise() { case "$1" in which) printf "%s\\n" "$HOME/bin/$2"; ...'`) stubs `mise which <tool>` to `$HOME/bin/<tool>` and puts a fake srt on PATH. The regression test puts two fakes in place: a `srt` first on PATH that behaves as the shim does (exits 1 printing `mise ERROR Config files in ... are not trusted` when `XDG_STATE_HOME` is not `$HOME/.local/state`, else execs the real fake) and the fake `$HOME/bin/srt` the stubbed `mise which srt` names; at main the run fails with the shim's message, at the head the run uses `$HOME/bin/srt` and succeeds, and the settings and command it records are unchanged. A `mise which srt` that fails is a refusal naming the pin, the message of :1855 reworded for the producer.

DATA SHAPE
Three producers of the same shape in `build_under_srt` (srt, pnpm, node), each `mise which` with the status read and the answer held to an absolute executable regular file; no `type -P srt` remains in the updater (`grep -c 'type -P srt' scripts/update-agent-assets.sh` is 0).

CHANGE
1. The regression test first, red at 6ad1be23. 2. The two resolutions. 3. `uv run --with pyyaml python -m unittest tests.unit.test_update_agent_assets tests.unit.test_network_bounds tests.unit.test_runtime_health tests.unit.test_asset_manifest -v` OK. 4. `make shellcheck`; `shfmt -i 4 -sr -d scripts/update-agent-assets.sh`; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`; `make render-check`. 5. Commit `fix(updater): build_under_srt resolves srt through mise which, never the shim the updater puts first on PATH (regime-cutover U354)` with the trailer. 6. The body: Summary (the measured failure and its cause), Contract, Threat table (one row per changed path; the srt producer row cites the regression test), Verification; `Program-Unit: regime-cutover/U354` once.

ACCEPTANCE
1. The regression test named with its red line at 6ad1be23 and its green line at the head. 2. `grep -c 'type -P srt' scripts/update-agent-assets.sh` is 0; `grep -c 'mise which srt' scripts/update-agent-assets.sh` is 2 or more. 3. The four test modules OK with counts. 4. The five lints 0. 5. `git diff --stat 6ad1be23 HEAD` pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator reruns `DSH_HOME=~/.dsh scripts/update-agent-assets.sh update_dsh_superagent` on the laptop after the merge and the deploy, which is the real-surface proof.

CLOSURE
remove

TRUST
TRUST: the unit trusts `mise which` as the producer of a pinned tool's path, as build_under_srt already does for pnpm and node, and trusts mise's shim behaviour as measured on this host.

TIMEBOX
40 minutes.

FORBIDDEN
No change to the updater's PATH handling or to the shim; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u354/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U354`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U354-progress.txt`; final report to `../U354-report.txt`; body at `../U354-pr-body.md`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the regression test's name with its red and green lines, the grep counts, the ACCEPTANCE lines. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46, 49); the U322 and U322b briefs; `scripts/update-agent-assets.sh:1786-1829` (build_under_srt's contract) and `:3510-3530` (main's PATH line).
