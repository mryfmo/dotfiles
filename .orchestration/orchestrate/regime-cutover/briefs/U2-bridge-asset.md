# U2 bridge asset (W2d) — brief

GOAL
Make the patched pi-claude-bridge a reproducible, pinned asset of this repository that `make update` installs under a trusted path with its own `node_modules`, loads in omp 18.11.3 by `-e <dir>`, and is checked by a load-regression test that fails on any `Failed to load extension`. The seat launcher (U7) will pass `-e <install dir>`; the model mapping is U4's.

SCOPE
Exclusive worktree on a new branch `feat/pi-claude-bridge-asset` from `origin/main`. May write: `home/dot_agents/agent-config.yaml` (ONLY a new `assets.pi-claude-bridge` entry next to the omp/hcom entries, lines 516-547; U4 owns `model_profiles`), `home/dot_agents/assets/pi-claude-bridge/**` (patch files, a committed `bun.lock` if you choose the frozen-lockfile route, README), `scripts/update-agent-assets.sh` (new functions `update_pi_claude_bridge`, `check_pi_claude_bridge`, wired like `update_omp`/`update_hcom`), `scripts/validate-agent-assets.py` (only what the new asset entry needs), `scripts/check-agent-runtime.py` (the load-regression check, if that is where runtime checks live; read it first), `tests/unit/test_pi_claude_bridge_asset.py`, `docs/pi-claude-bridge.md`. Nothing else.

CONTEXT (read first, in this order)
- `~/Workspace/dotfiles/.orchestration/validation/025-pilot-bridge-unit-report.md` (U1, 122 lines): §1 instrument (the session path prints load errors, `omp models` never evaluates extensions), §2 forms, §3 root cause, §5 shipping form, §7 follow-ups F1-F5. Its tools under `/tmp/claude-501/u1-work/` (`run-form.sh`, `gap-check.py`, shim export dumps) are yours to reuse; `pkg-probe` there is the stubbed copy that loads.
- `~/Workspace/dotfiles/.orchestration/validation/025-pilot-bridge-omp-compat.patch` (69 lines, patch v1: `formatSkillsForPrompt` inlined, `keyText` for `keyHint`, AskClaude context dropped) and `~/Workspace/dotfiles/.orchestration/validation/025-pilot-facts.md` (#B1..#B3b, corrections).
- `~/Workspace/dotfiles/.orchestration/validation/025-v13-facts-20261023.md` §2, §2b (npm 0.9.3 integrity `sha512-5OM3X6QLX7Xsv86bD+yiWvQEHdlGdXnaY9DgZg6jG4jpnKiHQ2FZKYVRFHYmDAEccDPfeFwW+NFHnkb+BUM+6Q==`, shasum `fe28fda31af2ad448d9792fd453bbb60cad726dd`, tarball URL; the provider path's `query()` options incl. `settingSources` left at default).
- Existing asset mechanics: `home/dot_agents/agent-config.yaml` `assets:` (omp npm tarball with sha256, hcom PyPI wheel), `scripts/update-agent-assets.sh` (`update_omp`, `update_hcom`, verification steps), `scripts/validate-agent-assets.py`, `scripts/check-agent-runtime.py`, `Makefile` targets `update`, `doctor`. Follow their shape exactly (sha256 pins, receipts, idempotent install).
- Decisions: plan 025 v14 decision 30 (trusted path, now a directory loaded with `-e <dir>`), 37 (vendored-with-patch), 38 (remove the bridge's `timeout=120` injection into omp's bash tool argument; find it in `src/index.ts` or `src/mcp-server.ts` and cite the line), D-024-129 (bridge route), preferences.md.

DESIGN DEFAULTS (refine only with a stated reason; each refinement becomes a line in your report)
- Install dir: `~/.local/lib/omp-extensions/pi-claude-bridge/` (decision 30). Contents: the pinned tarball's `package/` with patches applied, plus `node_modules` installed by Bun from a committed lockfile (`bun install --production --frozen-lockfile` using `home/dot_agents/assets/pi-claude-bridge/bun.lock` that you generate once and commit) so the dependency set is pinned; record `@anthropic-ai/claude-agent-sdk` and `@anthropic-ai/claude-agent-sdk-darwin-arm64` versions in the receipt. If Bun cannot run in the installer's environment, say so with the error and propose the alternative.
- Patch v2 = patch v1 + `contentText` inlined into `src/transcript.ts` (upstream pi-ai 1.4.0 `dist/utils/text.js:2-9`, MIT; eight lines, as the U1 report §3 quotes) + decision 38 (timeout injection removed) + `settingSources: []` on the provider query path so the child Claude Code loads no user/project/local settings (no regime hooks, no `~/.claude` permissions; the claude.ai login is not a setting and still applies; alternative = a `PI_CODING_AGENT_DIR` skip in every hook; state why you keep or drop this default after reading the facts §2b `claudeMdExcludes` comment). Keep each change as a separate numbered patch file under `home/dot_agents/assets/pi-claude-bridge/patches/` applied in order; record each file's sha256 in the receipt.
- Load-regression check (F5): under `HOME=$TMPDIR/u2-home`, `omp --no-extensions -e <install dir> --no-session --model claude-bridge/claude-haiku-4-5 --max-time 60 -p "Reply with the single word PONG."` must print neither `Failed to load extension` on stderr nor in `$HOME/.omp/logs/*.log`; reaching `Not logged in · Please run /login` counts as loaded (the login is the operator's). Make it a function the `doctor` target can call, with a pasted sample run.
- Gap check: run U1's `gap-check.py` (or your port) against a fresh dump of omp's shim exports and fail the install when any value import of the bridge is missing; this is the guard for omp upgrades (F1).

ACCEPTANCE
1. `uv run --no-project scripts/validate-agent-assets.py` passes with the new entry (paste).
2. `scripts/update-agent-assets.sh update_pi_claude_bridge` under `HOME=$TMPDIR/u2-home` installs into `$HOME/.local/lib/omp-extensions/pi-claude-bridge/` reproducibly (run twice, second run is a no-op; paste both tails), with network only to `registry.npmjs.org`.
3. The load-regression check passes on that install (paste the session-path output ending in `Not logged in · Please run /login` or `PONG`).
4. Unit tests for the patch application (idempotent, sha256-checked) and the receipt pass (`uv run --no-project -m pytest tests/unit/test_pi_claude_bridge_asset.py -q`, paste).
5. `docs/pi-claude-bridge.md` explains the route, the patches (why each), the install dir, the launcher flag, the operator login step, and the fallbacks (`anthropic/` API key).
6. PR open, CI green, title `feat(assets): pi-claude-bridge as a pinned, patched omp extension (W2d)`, body per STANDING 14, ending with the receipt sample.

VERIFY
Commands in ACCEPTANCE; `shellcheck scripts/update-agent-assets.sh` if installed; `git diff --stat origin/main...HEAD`. Network: `registry.npmjs.org`, `api.github.com`, `github.com` only. Never write the real `~/.local/lib/omp-extensions`, `~/.omp`, `~/.claude`.

TIMEBOX
90 minutes.

FORBIDDEN
No edits outside SCOPE (in particular no `model_profiles` lines, no `scripts/orchestrator/**`), no login attempts, no merge, no rebase.

REPORT
≤ 250 words: branch, head sha, PR link, CI state, pasted receipt, the patch list with sha256, the settingSources decision and reason, deviations, follow-ups (including the exact `-e` flag string U7 must use).

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (16 lines) before any command.
