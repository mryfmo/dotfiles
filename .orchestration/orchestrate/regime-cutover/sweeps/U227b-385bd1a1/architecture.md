# Architecture: dotfiles, scoped to b49be338..385bd1a1 (U227b)

## Product, principals, protected resources

A dotfiles repository rendered by chezmoi. On an operator's host:

- `make update` runs `scripts/update-agent-assets.sh`.
- Its `update_deepseek_harness` step installs the pinned DeepSeek harness (DSH) under `$DSH_HOME`, which must physically be `~/.dsh`. It does so only on an opted-in host, and nothing starts the harness.
- chezmoi renders the kit's DSH profile, `thak`, from `home/dot_agents/agent-config.yaml` through `scripts/generate-agent-configs.py` into `~/.dsh/profiles/thak`: a `cordis.patch.yml` over the base bundles, and a `package.json`.

Protected resources:

- the operator's Claude login, which the new route reaches through a child `omp auth-gateway stdio`
- the absence of API keys, since the earlier route used `OLLAMA_API_KEY`
- the operator's home

Principals:

- **The operator.** Owns the manifest, the rendered profile and `~/.dsh`.
- **The harness.** Third-party code, pinned by tag and sha256.
- **The gateway plugin.** It sits at `$DSH_HOME/plugins/omp-gateway`; its source is the U240 commits, which are not in this head.
- **The repositories the harness works in.** Lower trust, but they reach none of the changed code paths.

## Comparable baseline

None source-grounded.

## Stack and limits

- A Python generator, a YAML manifest, Bash `update-agent-assets.sh`, pnpm from mise for the profile's plugins, and `unittest` tests.
- This run is source-only; no target code is executed.

## Entry surfaces and paths in scope

- **The rendered gateway row** (`cordis.patch.yml:16-27`): `command: omp`, `args: [auth-gateway, stdio]`, `providers: [claude-bridge]`, and models `claude-bridge/<id>`. There is no `env` and no `cwd`. It is written from constants (`generate-agent-configs.py:171-174`, 2291-2296), and the model ids are restricted by `DSH_MODEL_RE` (167).
- **The `agent-default-model` row** (11-14): the interactive profile's dsh model on `claude-bridge` (2254-2256, 2281-2284).
- **The withdrawn `llm-pi-ai` Ollama provider** (`baseURL https://ollama.com/v1`, `apiKeyEnv OLLAMA_API_KEY`), now gone. The validator admits only `route: omp-gateway` (164).
- **`package.json`**: `dsh-omp-gateway: link:../../plugins/omp-gateway` beside the pinned hooks plugin (14-15).
- **The updater's plugin link**:
  - Refusals before any download: the plugin directory (2032-2035), a symlinked or non-directory `node_modules` (2036-2039), and a non-symlink at the link path (2040-2043).
  - `dsh_link_plugin` (1971-1977) writes `ln -sfn ../../../plugins/omp-gateway` at `profiles/thak/node_modules/dsh-omp-gateway`. It runs on the install (2211), the repair (2214) and the already-installed exit (2125).

## Trust boundaries and their strongest controls

| Boundary | Strongest control |
| --- | --- |
| Manifest into rendered profile | The validator's regexes and route set, and constant command and args. |
| Profile into the harness's plugin loader | The row names a fixed command and no environment or working directory. |
| Filesystem state into the link step | Type checks before the write, `-n` on `ln`, a fixed relative target, and the DSH_HOME physical-path check. |
| Credential exposure | The key route is removed. |

## Starting paths

`home/dot_dsh/profiles/thak/cordis.patch.yml`, `home/dot_dsh/profiles/thak/package.json`, `scripts/generate-agent-configs.py`, `scripts/update-agent-assets.sh`, `home/dot_agents/agent-config.yaml`, `tests/unit/test_dsh_profile.py`, `tests/unit/test_update_agent_assets.py`.

## Prior coverage

run-4 (U247, the U244 head `d1fd54ba`) left 34 units, all carried with the same IDs as `out_of_scope`. U244 is not in this head. There are no prior records.

## Companion selection

- **ATTACK-CLASSES.md:** Injection (the rendered row), Business logic (the model rows, tests), Cryptography and secrets (the withdrawn key route), Resource and file handling (the symlink step), Obvious things.
- **SUPPLY-CHAIN-AND-RELEASE.md:** Plugin and extension trust expansion (the `link:` plugin), with Core discipline, Universal moves and Validation rules.
- **Excluded:** AI, local IPC, cloud and web companions, with reasons in the ledger.
