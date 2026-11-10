# U353b round 2 of U353: every seat row denies the Router's credential root for read, and `router-gh` is the only credential source gh sees

GOAL
The round-1 audit of PR 724 (verdicts/U353-8791100f.md, class credential-boundary) found two P1s. (1) hcom-seat:430: the credential root `<DSH_HOME>/router-credentials` is granted to the router row for read and denied to the dsh row, but the orchestrator and worker rows carry no deny of it, and srt allows reads by default, so an omp seat reads `router-credentials/gh/hosts.yml` once the operator's plaintext login is there; the Router-only guarantee breaks. (2) router-gh:97: `GH_CONFIG_DIR` points gh at the credential root, but gh's Keychain lookup for `github.com` is host-wide and srt permits securityd, so with the operator's GitHub login in the Keychain an empty credential root authenticates as the operator instead of refusing the pre-token Source save. Two P2s inside the lever `router-settings-apply` fall inside this round's lines: the urllib opener honours proxies and follows redirects off loopback (:268), and the Source is enabled before the safe mode is saved (:401). Order 49: one fix round with reproducing tests first, then one audit.

SCOPE
The same branch `feat/m26-stage-b-router-settings-and-credential-root` and PR 724; the tree is `/tmp/dotfiles-wt/U353` at 8791100f (clean). May write: `scripts/orchestrator/hcom-seat` and its copy (the credential root in every role's `denyRead` except the router row's; the router row keeps its read grant; `denyWrite` for every row as today), `scripts/orchestrator/router-gh` and its copy (the wrapper reads the token itself from `<root>/gh/hosts.yml` (the `oauth_token` of `github.com`, the file 0600 and a regular file of this user, else refused by name with exit 2 and no gh run), passes it to gh as `GH_TOKEN` with `GH_CONFIG_DIR` still the root, so gh never consults the Keychain; an absent or empty token is a refusal, never a fallback), `scripts/orchestrator/router-settings-apply` and its copy (an opener built from `ProxyHandler({})` with no redirect handler, the host held to `127.0.0.1`; `eval` saved before `source:github` is enabled), `tests/unit/test_hcom_seat_dsh.py` and `tests/unit/test_hcom_seat.py` (the orchestrator and worker rows deny the credential root), `tests/unit/test_router_settings_apply.py` (the wrapper's refusals and `GH_TOKEN`; the opener's proxy and redirect refusals; the save order), `scripts/orchestrator/README.md` and `docs/engagement-handout.md` (one sentence each where they describe the wrapper), the pins through the generator, and the body `../U353-pr-body.md` (`## Round 2`; the Threat table gains one row per changed path, the round-1 P2 at tests:1). Not: acp-broker (PR 720's branch); the Router's Executor; the operator's account.

CONTEXT
hcom-seat's role table (:419-424) and the `cred_root_grant` cell U353 added (read `cred_root_hold`, the render and the judge tags); the omp roles' deny lists (`seat_settings_render`, the shared deny table) where `~/.local/state/dsh-router` was listed before U353 moved the root; `router-gh` (97 lines) and `router-settings-apply` (423 lines) as written at 8791100f; gh's credential resolution order (environment `GH_TOKEN` first, then the config directory's `hosts.yml`, then the Keychain on macOS: GitHub's `gh auth` documentation and `gh help environment`); `tests/unit/test_hcom_seat.py`'s fixtures for the omp roles' settings.

DATA SHAPE
One deny row in every role but router; one token source for the Router's gh (a file the wrapper reads and holds); one loopback-only opener; one save order (mode first).

CHANGE
1. Tests first, red at 8791100f: (a) the orchestrator and worker settings carry the credential root in `denyRead` (and the dsh row still does; the router row does not); (b) `router-gh` with an empty root refuses by name and runs no gh (a fake gh on PATH records nothing); with a `hosts.yml` holding a token it runs gh with `GH_TOKEN` set to that token and `GH_CONFIG_DIR` the root; a link or a group-readable `hosts.yml` is refused; (c) `router-settings-apply` against the fake API with `HTTP_PROXY` set in the environment reaches the loopback port directly; a `302` from the fake API is a refusal naming it; the `PUT` of `eval` precedes the `PUT` of `source:github` in the fake's log. 2. The three levers; the pins. 3. `uv run --with pyyaml python -m unittest tests.unit.test_hcom_seat_dsh tests.unit.test_hcom_seat tests.unit.test_router_settings_apply tests.unit.test_dsh_profile tests.unit.test_generate_agent_configs -v` OK. 4. shellcheck, shfmt, ruff (CI form), prettier (CI form), lint-comparisons, render-check, validate-agent-assets: all 0; cmp of every pair 0. 5. Commit `fix(router): every seat row denies the credential root, router-gh is the only credential source gh sees, the settings writer stays on loopback and saves the mode first (regime-cutover U353b)` with the trailer. 6. The body.

ACCEPTANCE
1. Tests (a), (b), (c) named with red and green lines. 2. The five modules OK with counts. 3. The lints 0; cmp 0; the pins equal `shasum -a 256` of the sources. 4. `git diff --stat 8791100f HEAD` pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator pushes, and the one audit, the sweep and CI follow.

CLOSURE
remove

TRUST
TRUST: the unit trusts gh's documented credential order (`GH_TOKEN` first) as the reason the Keychain is never consulted, srt's deny rows as the omp seats' boundary, and the fake Management API as the proof of the save order and the loopback-only transport.

TIMEBOX
60 minutes.

FORBIDDEN
No read grant of the credential root to any role but router; no token in any file of the repository or the store; no network beyond the loopback fake; no push; no `gh` call against GitHub; no pin edited by hand; no rebase; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u353b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U353`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U353b-progress.txt`; final report to `../U353b-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the three tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46, 49); `verdicts/U353-8791100f.md`; the U353 brief; `handouts/m25-agent-github-account.md`.
