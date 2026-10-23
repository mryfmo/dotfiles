# U2b pi-claude-bridge asset: verifier fix round — brief

GOAL
Bring PR #461 (`feat/pi-claude-bridge-asset`, head 9a795960 plus one `gh pr update-branch` merge commit, current head 9b23e86d) to mergeable: fix the verifier's three P1 findings (CI red) and the P2 (over-wide patch 01) at root cause, keep the install reproducible, and leave CI green.

SCOPE
Exclusive worktree on the existing branch `feat/pi-claude-bridge-asset` (fetch from origin; you are its only writer now). May write: `scripts/update-agent-assets.sh`, `home/dot_agents/assets/pi-claude-bridge/**` (patches, bun.lock, README if present), `tests/unit/test_pi_claude_bridge_asset.py`, `tests/unit/test_asset_manifest.py`, `tests/unit/test_runtime_health.py`, `docs/pi-claude-bridge.md`, and the `assets.pi-claude-bridge` entry in `home/dot_agents/agent-config.yaml` only if the patch list or hashes change. Nothing else.

CONTEXT (read first)
- Verdict `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/verdicts/U2-9a795960.md`: F1 P1 `tests/unit/test_asset_manifest.py:223` expects 17 `manifest_record "` calls, the new installer step makes 18 (add `update_pi_claude_bridge` to the tuple at 204-221, count 18); F2 P1 `tests/unit/test_runtime_health.py:110-124` stub list lacks the new step so `main` prints `Skipping pi-claude-bridge: bun command not found.` and breaks the exact-stdout assertion (add `update_pi_claude_bridge() { :; }` to the stubs, keep the message in the sibling convention); F3 P1 `scripts/update-agent-assets.sh:1113` `patch -p1 -s` without `-F0` lets GNU patch apply a stale-context patch with fuzz and exit 0 (CI ubuntu `test_a_failed_check_…` `1 != 0`) while Apple patch refuses (add `-F0`; make the failing-patch test assert the refusal on both); F4 P2 `patches/01-omp-shim-exports.patch:16-17,25-27` the `keyHint` and `buildSessionContext` hunks are not load-blockers (omp's shim `export * from "../index"` at `src/extensibility/legacy-pi-coding-agent-shim.ts:1607`; U1 runtime export dump lines 253 and 507 list both), and the `buildSessionContext` hunk drops AskClaude's session context on a false `shortcut:` premise: trim patch 01 to the `formatSkillsForPrompt` hunk only, regenerate its sha256 in the manifest/receipt, and prove with the gap check (`gap-check.ts` against fresh shim export dumps: 0 MISSING) and the scratch-HOME load check (`Not logged in · Please run /login`, no `Failed to load extension`) that the trimmed set still loads.
- The original brief `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/briefs/U2-bridge-asset.md` and the U2 report (receipt: tarball sha256 8d582b2f…, patches 01-04, bun.lock 2a63e7c8…, SDK 0.3.309). U2's levers under `/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/c41e04d3-e780-4783-ab71-7087367e91c9/scratchpad/{make-patches.py,dryrun.sh,dryrun-final.sh}`.
- Measured by the operator on the real host (pilot-facts #G1..#G1-3): the bridge route answers PONG and executes bridged tool calls with patch v1; patch 04 (`settingSources: []`) is unmeasured on the real login (the operator's step is pending) and stays in the set.
- Git: push over HTTPS with `git push https://github.com:443/mryfmo/dotfiles.git <branch>` and a gh-token askpass if the global SSH rewrite blocks you (standing order 19 amendment).

ACCEPTANCE
1. `uv run --no-project --with pytest -m pytest tests/unit/test_pi_claude_bridge_asset.py tests/unit/test_asset_manifest.py tests/unit/test_runtime_health.py -q` passes (paste the summary); the failing-patch test proves `-F0` (a patch with shifted context is refused, exit non-zero, nothing installed).
2. Patch 01 trimmed; manifest/receipt hashes updated; `uv run --python 3.12 --no-project --with pyyaml scripts/validate-agent-assets.py` (or the version available) passes (paste).
3. Scratch-HOME install twice + `check_pi_claude_bridge` (paste the receipt and the check tail); gap check 0 MISSING (paste).
4. Push; CI green on the new head except nothing (the `regime` check now passes on program PRs); paste `gh pr checks 461`.

VERIFY
Commands above. Network: `registry.npmjs.org`, `api.github.com`, `github.com` only. Never the real `~/.omp`, `~/.claude`, `~/.local/lib/omp-extensions`.

TIMEBOX
45 minutes.

FORBIDDEN
No edits outside SCOPE, no `model_profiles` lines, no merge, no rebase, no force-push, no history rewrite.

REPORT
≤ 150 words: head sha, PR link, CI state, test summary, the new patch 01 sha256, deviations.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (19 lines) before any command.
