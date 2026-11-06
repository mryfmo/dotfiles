# U232 the kit's DeepSeek harness profile mounts no official-API web search

GOAL
The security-audit sweep of the U227 head (run-51, `sweeps/U227-785658d1/findings.json`, lead `dsh-profile:web-search-routes-to-the-official-api`) read the composed thak tree: the base bundle mounts `web` with `searchProvider: deepseek-official` and the plugins `web-search-deepseek` and `web-deepseek-api`, each with `apiKeyEnv: DEEPSEEK_API_KEY`. The kit patch disables the official LLM adapters (`llm-deepseek`, `llm-deepseek-account`) but not these, so once a turn runs (U227) a model-chosen web search reaches the official DeepSeek API whenever that variable is set, against PRD open question 7's default (the official API off). This unit makes the renderer disable the two official web plugins in the kit patch, the same form as the LLM rows, with a test, so the harness has no official-API egress path by default. Web fetch over plain HTTP (`web-fetch-http`) stays; it goes through the seat's srt network allowlist, not the official API.

SCOPE
A new branch `feat/dsh-profile-no-official-web-search` from `origin/main` at the head the TASK names (after U227 merges). May write: `scripts/generate-agent-configs.py` (`render_dsh_profile_patch` only), `tests/unit/test_dsh_profile.py`, the regenerated `home/dot_dsh/profiles/thak/cordis.patch.yml`, and the body file `/tmp/claude/U232/U232-pr-body.md`. Not: the updater, the asset entry, any other renderer.

CONTEXT
Measured 2026-11-06 with `DSH_HOME=~/.dsh ~/.dsh/bin/dsh --profile thak --dump-config` at dsh-v0.2.1-rc.5 (407 lines): rows `- id: web` (`config: searchProvider: deepseek-official, fetchProvider: http`), `- id: web-search-deepseek` (`@deepseek-ai/dsh-web-search-deepseek`, `apiKeyEnv: DEEPSEEK_API_KEY`), `- id: web-deepseek-api` (`@deepseek-ai/dsh-web-deepseek-api`, `apiKeyEnv: DEEPSEEK_API_KEY`), `- id: web-fetch-http`, `- id: tool-web` (`fetch: true, searchTimeoutMs: 60000`). The renderer (`scripts/generate-agent-configs.py`, `render_dsh_profile_patch`) emits `- id: <row>` / `  disabled: true` for the LLM rows; the test module reads the rendered patch as text and splits it into top-level `- id:` blocks. Read `packages/web/web` (or the base bundle's `cordis.patch.yml`) in the installed tree `~/.dsh/dsh/current/packages/` (read-only) to confirm what `tool-web` does when `searchProvider` names a provider no plugin registers, and cite the file and line in the body; if a search request then errors instead of silently falling back to another provider, that is the acceptable behaviour (no egress); if it falls back to something that reaches a network host, say which and set `searchProvider` to a value that registers nothing.

CHANGE
1. Renderer: after the `bash-sandbox` row, emit `- id: web-search-deepseek` / `  disabled: true` and `- id: web-deepseek-api` / `  disabled: true`; leave `web`, `web-fetch-http` and `tool-web` as the base mounts them unless CONTEXT's reading shows a fallback that reaches a host, in which case also emit the `web` row with the `searchProvider` value CONTEXT's reading justifies.
2. Regenerate the patch; `make render-check` clean.
3. Tests: the patch disables exactly those two ids (each block `disabled: true`, each present once); no row of the patch names `DEEPSEEK_API_KEY`; the existing tests still pass.
4. The body: Summary (the sweep lead, the rows, the reading of CONTEXT with its citation), Contract (guarantee: no row of the kit patch leaves an official-API web plugin enabled; leaves out: the Router preset of M-26, srt network allowlists, the LLM routes), a Threat table `row | risk | status | evidence` with one row per changed path, one for the non-path control (the disabled ids), and an `orchestrator effect` row, each `closed` with the ACCEPTANCE command, and `Program-Unit: regime-cutover/U232`.

ACCEPTANCE
1. `grep -n -A1 '^- id: web-search-deepseek\|^- id: web-deepseek-api' home/dot_dsh/profiles/thak/cordis.patch.yml` prints the two blocks with `disabled: true`.
2. `grep -c DEEPSEEK_API_KEY home/dot_dsh/profiles/thak/cordis.patch.yml` prints 0.
3. `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0, no diff.
4. `uv run python -m unittest tests.unit.test_dsh_profile tests.unit.test_scratch_git` OK (paste the count).
5. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
6. The body cites the upstream file and line for CONTEXT's reading.

VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section. The composed-tree proof (`dsh --profile thak --dump-config` showing both rows `disabled: true`) is the coordinator's step after the merge and the host apply, recorded in the store.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the pinned harness's base bundle ids as read from its installed source and the renderer's existing disabled-row form; it adds two rows and a test, reads no network at test time, and changes no route, key or sandbox setting.

TIMEBOX
30 minutes.

FORBIDDEN
No hand edit of the rendered patch; no change to the updater, the asset entry, `hcom-seat` or another renderer; no API key anywhere; no local bats; no network read beyond the installed tree under `~/.dsh/dsh/current/` (read-only); no push; no `gh` call; no mention of any private design directory in files, commits or the PR body; none of the words in `.orchestration/orchestrate/regime-cutover/redact-words.txt` and no absolute home directory in tracked files or the PR body (write `~/...`).

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `preferences.md` lines 23 to 46 in the store)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree. Never `git stash`. Before you report, `git -C ~/Workspace/dotfiles status --porcelain=v1 --untracked-files=all -- . ':!.orchestration/orchestrate' | shasum` must print the value the TASK line carries.
- Progress line in `/tmp/claude/U232/U232-progress.txt` every ten minutes at most.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Write the whole PR body at `/tmp/claude/U232/U232-pr-body.md` per CHANGE 4.
- Comments explain a non-obvious why only, no phase narration.

REPORT
Status, head sha (40 hex), `git diff --stat origin/main`, the ACCEPTANCE result lines, the upstream citation, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 42); `AGENTS.md` (Comment Policy, Test Policy, Audit); `sweeps/U227-785658d1/findings.json`; `briefs/U227-dsh-profile-selects-the-kit-route-model.md`.
