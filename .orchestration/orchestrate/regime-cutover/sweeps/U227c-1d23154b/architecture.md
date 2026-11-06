# Architecture: dotfiles at 1d23154b (scoped to unit U227b, round 3 U227c)

## Product, principals and resources

A personal dotfiles repository.

**The kit's DSH profile.** `scripts/generate-agent-configs.py` renders the profile `thak` into `home/dot_dsh/profiles/thak/{cordis.patch.yml,package.json}` from the manifest `home/dot_agents/agent-config.yaml`. chezmoi deploys it to `~/.dsh/profiles/thak`.

**The updater.** `scripts/update-agent-assets.sh`'s `update_deepseek_harness` installs the pinned DSH under `DSH_HOME` on a host whose operator opted in. U227b adds a step that links the `dsh-omp-gateway` plugin into the profile's `node_modules`.

**Principals.** The operator, who owns `~`, `DSH_HOME` and the profile, and runs `make update`; pull-request authors, behind review and CI (the validator runs the generator `--check`); and the DSH process with its plugins.

**Resources.** The operator's account (code DSH loads), the operator's Claude login inside omp, and the install tree under `DSH_HOME`.

## The change under hunt (b49be338..1d23154b: U227b 385bd1a1, U227c 1d23154b)

- **Manifest.** Every `model_profiles` dsh row becomes `{ model: claude-..., route: omp-gateway }` (`agent-config.yaml:552-598`).
- **Generator.** `DSH_ROUTES = ("omp-gateway",)` (`generate-agent-configs.py:164`). `DSH_MODEL_RE` requires `claude-` plus the launcher-safe form (`:165-167`, `:237-243`). The `DSH_GATEWAY_*` constants are at `:171-174`. `render_dsh_profile_patch` (`:2239-2301`) emits:
  - an `agent-default-model` row (provider `claude-bridge`, the interactive profile's model);
  - an insert row `omp-gateway` / `dsh-omp-gateway` with `command: omp`, `args: [auth-gateway, stdio]`, `providers: [claude-bridge]`, and the models;
  - the `link:` dependency in `package.json`.

  The Ollama provider block and the API-key route are removed.
- **Rendered profile.** `cordis.patch.yml:2-10` turns off session-log upload, `llm-deepseek`, `llm-deepseek-account` and `bash-sandbox`. Lines `:11-27` are the default-model and gateway rows. `package.json:15` holds `"dsh-omp-gateway": "link:../../plugins/omp-gateway"`.
- **Updater.** Before any download, it requires `DSH_HOME/plugins/omp-gateway` and `profiles/thak` to be directories whose physical paths lie under `DSH_HOME`'s (`update-agent-assets.sh:2073-2098`). It refuses a `node_modules` that is a symlink or not a directory, and a non-symlink at the link name (`:2099-2106`). `dsh_link_plugin` (`:1978-2015`):
  1. re-reads `node_modules` physically;
  2. computes a relative target with `os.path.relpath`;
  3. writes `${link}.tmp.$$`;
  4. renames it over the link with `os.replace`;
  5. checks that the link resolves.

  It runs on the already-installed exit (`:2188`), the fresh install (`:2274`) and repair mode (`:2277`), and the receipt records it (`:1971`).
- **Tests.** In `tests/unit/test_update_agent_assets.py`, `test_dsh_profile.py`, `test_validate_agent_assets.py`, and `test_network_bounds.py:402`.

## The plugin is not in this head

`home/dot_dsh/plugins/omp-gateway` is U240's, and U240's head 2256b56c is not an ancestor. `git ls-tree` lists only the two profile files under `home/dot_dsh`. On every opted-in host, the updater's refusal (`:2073-2076`) holds until U240 merges.

## Comparable baseline

The pattern is a package manager's `link:` dependency, plus an installer that writes the same symlink itself. Its usual risks are a link that escapes its tree, and a non-atomic relink. The step handles both: physical-path containment, and `rename(2)`.

## Trust boundaries and strongest controls

- **Manifest to rendered rows.** Constants, a strict model regex, and the CI drift check.
- **Profile author to child command.** The same principal (the operator's own file). The plugin's environment allowlist and default `cwd` apply.
- **`DSH_HOME` layout to the link.** Every input is resolved physically and must sit under `DSH_HOME`, a non-symlink at the link name is refused, and relinks are atomic.
- **Plugin absence.** It fails closed: nothing is installed.

## Prior coverage

run-6 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-6`, source 50dd240c, U254) is carried. U254 is absent at this head, so its four units carry as changed-source, out-of-scope units, and its 33 out-of-scope units carry. No prior run holds a finding.

## Companion selection

Selected:
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: privileged-helper, local-file and install-path blocks for the rows and the link step.
- `SUPPLY-CHAIN-AND-RELEASE.md`: plugin trust for the `link:` dependency.

Every other companion is excluded with its reason in the ledger.

## Execution and independence limits of this run

No target code ran, by task rule. The delegation tool (Task) and eval kernel are denied by policy on this seat, so every phase ran in the parent. `run-metadata.json` records the run as incomplete for that reason.
