# Architecture: dotfiles at 1faa81f1 (U434 round 2, U434b, feat/router-profile-acp-subagent, PR 757)

## Product and principals

- **The repository** is a dotfiles kit with the regime-cutover seat levers. `hcom-seat` launches each agent seat inside srt 0.0.81 with settings it renders. `acp-broker` runs outside every seat and starts omp workers for the Router. `make update` (chezmoi apply, then `scripts/update-agent-assets.sh`) installs pinned assets, the dsh harness and the dsh-superagent plugin with the router profile's dependencies among them.
- **The operator** runs `hcom-seat` and `make update` from a terminal, outside every seat. The updater runs each third-party build inside its own srt settings (`build_under_srt`).
- **The Router** (the dsh superagent of the router row) runs inside srt and reads GitHub-authored input; it is the lowest-trust principal here. Its write roots include `DSH_HOME` (hcom-seat:2324-2327), where the deployed router profile lives.
- **Protected resources**: the checkout and its git state, the seats root, the hcom stores, the operator's Claude Code state, the credential stores, the manifest pins.

## The change under review

- **Round 1 (5b99f2c3..8c3cfec2, run-76):** the Router profile's `subagent-acp` insert and `tool-subagent` row, acp-seat's `--repo`/`--ref` defaults, hcom-seat's `ACP_BROKER_SOCK` export, the two pins. No boundary crossing (run-76; carried).
- **Round 2 (8c3cfec2..1faa81f1, 6 paths, +183 -18):** `home/dot_dsh/profiles/router/package.json:17` declares `@deepseek-ai/dsh-subagent-acp` as `link:../../dsh/current/packages/subagent/subagent-acp` (rendered by scripts/generate-agent-configs.py:195-196, :2506). On its already-installed exit, `update_dsh_superagent` reads the dependency names of the deployed package.json and re-runs `pnpm install` in the router profile under `build_under_srt` when one has no node_modules entry (scripts/update-agent-assets.sh:2713-2725, :2830-2845). Three test modules change.

## Trust boundaries the hunt reads

- **Router-writable inputs to an operator-run install**: the deployed package.json and node_modules lie in DSH_HOME, the Router's write root; the install runs when the operator runs make update.
- **The install's sandbox**: the registry host alone, writes to the profile and the pnpm store, and the read denies of update-agent-assets.sh:1985-1988, which are not the Router's (the router row also denies every `~/.local/state/hcom-*` store, hcom-seat:2510-2523).
- **The linked package**: the harness step's digest-verified tree behind `dsh/current`, loaded by dsh inside the Router's sandbox.
- **Round 1's boundaries** (Router to broker, Router to worker, depth, environment, pins) are run-76's, carried.

## Entry surfaces and paths

- A Router write under DSH_HOME/profiles/router (package.json, node_modules), read by the next make update.
- The Router's subagent tool call and its connection to the broker socket (run-76).

## Prior coverage

- Base: run-76 (8c3cfec2). 231 units at this head: 114 covered, 23 candidate, 94 out_of_scope. Changed-source units: 23.
- No same-source confirmed record exists to exclude: run-76's findings.json is empty and its 22 leads are unvalidated candidates.
- The code architecture of the levers is in run-73's to run-76's `architecture.md`; this file names what U434b adds.

## Companion selection

- `SUPPLY-CHAIN-AND-RELEASE.md`: a profile dependency, an updater install and its sandbox.
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: a lower-trust local writer feeding a higher-trust local process (the updater).
- `AI-AND-LLM.md`: the Router's subagent route (round 1, carried).
- Not selected: no browser, cloud, tenant, native code, wire protocol to a shared service or HTTP flow is in the change.
