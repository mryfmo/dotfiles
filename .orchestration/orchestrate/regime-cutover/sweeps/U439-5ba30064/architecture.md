# Architecture: dotfiles at 5ba30064 (U434 round 3, U434c, feat/router-profile-acp-subagent, PR 757)

## Product and principals

- **The repository** is a dotfiles kit with the regime-cutover seat levers. `hcom-seat` launches each agent seat inside srt 0.0.81 with settings it renders. `acp-broker` runs outside every seat and starts omp workers for the Router. `make update` (chezmoi apply, then `scripts/update-agent-assets.sh`) installs pinned assets, the router profile's dependencies among them.
- **The operator** runs `hcom-seat` and `make update` from a terminal, outside every seat. The updater runs third-party builds inside its own srt settings (`build_under_srt`).
- **The Router** (the dsh superagent of the router row) runs inside srt and reads GitHub-authored input; it is the lowest-trust principal here. `DSH_HOME`, where the deployed router profile lives, is one of its write roots (hcom-seat:2324-2327).
- **Protected resources**: the checkout and its git state, the seats root, the hcom stores, the operator's Claude Code state, the credential stores, the manifest pins.

## The change under review

- **Round 1 (5b99f2c3..8c3cfec2, run-76):** the subagent-acp insert and tool-subagent row, acp-seat's defaults, the ACP_BROKER_SOCK export, the pins. No boundary crossing (carried).
- **Round 2 (8c3cfec2..1faa81f1, run-77):** the plugin as a link: dependency, and the updater's profile-install rerun on the deployed package.json's dependency names. One unvalidated lead (carried).
- **Round 3 (1faa81f1..5ba30064, 6 paths, +101 -8):** the tool-subagent row gains `disabled: false` (home/dot_dsh/profiles/router/cordis.patch.yml:32, rendered by scripts/generate-agent-configs.py:2547-2552), and the dependency reader refuses a file that is not a JSON object with an object dependency table (scripts/update-agent-assets.sh:2713-2740). Three test modules change.

## Trust boundaries the hunt reads

- **The enabled subagent tool**: Router subagent calls become broker workers by default; the broker judges each header and reads the repository inside the Router's own sandbox.
- **The reader**: a Router-writable file parsed in an operator-run step; it must fail closed and echo nothing.
- **Round 2's boundary** (Router-writable inputs to an operator-run install whose sandbox reads more than the Router may) is carried as the open lead.

## Prior coverage

- Base: run-77 (1faa81f1). 234 units at this head: 117 covered, 23 candidate, 94 out_of_scope. Changed-source units: 25.
- No same-source confirmed record exists to exclude: run-77's findings.json is empty and its 23 leads are unvalidated candidates.
- The levers' code architecture is in run-73's to run-77's `architecture.md`; this file names what U434c adds.

## Companion selection

- `AI-AND-LLM.md`: the enabled model-driven subagent tool.
- `SUPPLY-CHAIN-AND-RELEASE.md`: the updater's reader and install.
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: the Router-to-broker route (carried).
- Not selected: no browser, cloud, tenant, native code, wire protocol to a shared service or HTTP flow is in the change.
