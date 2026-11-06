# Architecture: dotfiles at 88d53ce1 (scoped to unit U227b, round 4 U227e)

## Product, principals and resources

A personal dotfiles repository.

**The kit's DSH profile.** `scripts/generate-agent-configs.py` renders the profile `thak` into `home/dot_dsh/profiles/thak/{cordis.patch.yml,package.json}` from `home/dot_agents/agent-config.yaml`, and chezmoi deploys it to `~/.dsh/profiles/thak`.

**The updater.** `scripts/update-agent-assets.sh`'s `update_deepseek_harness` installs the pinned DSH under `DSH_HOME` on an opted-in host. Since U226 it builds with the pinned commit as `DSH_CLIENT_COMMIT_HASH`. Since U227b it links the `dsh-omp-gateway` plugin into the profile.

**Principals.** The operator, who owns `~`, `DSH_HOME` and the profile; pull-request authors, behind review and CI; and the DSH process and its plugins.

**Resources.** The operator's account, the operator's Claude login inside omp, and the install tree.

## The change under hunt (main d2389a05..88d53ce1, the nine U227b files)

The U227b content is unchanged since run-7's round-3 head (`git diff 1d23154b HEAD` shows no change to the profile files or `test_dsh_profile.py`). Round 4 (U227e) merges main d2389a05, which brings U226 (#674, the DSH build-commit input) and U224 (#673, which removes Understand-Anything). Three files were resolved in the conflict.

**Line numbers at this head.** U224's removal shifts the updater, so:
- **Updater link step:**
  - plugin, profile and `node_modules` checks at `update-agent-assets.sh:1905-1938`;
  - `dsh_link_plugin` at `:1804-1841`;
  - convergence calls at `:2020`, `:2106`, `:2109`;
  - `dsh_record` at `:1796-1798`.
- **U226's controls:**
  - the `DSH_COMMIT` refusal at `:1849-1852`;
  - the build export at `:2093`;
  - the manifest's `ref_commit` and render constant (`agent-config.yaml:1358`, `:1382`);
  - the constant itself (`scripts/lib/installer-pins.sh:37`).
- **Generator:** `DSH_*` constants at `generate-agent-configs.py:164-174`, checks at `:237-243`, renderer at `:2245-2307`.
- **Manifest dsh rows:** `agent-config.yaml:544-590`.

## The plugin is still not in this head

`home/dot_dsh/plugins/omp-gateway` belongs to U240, whose head 2256b56c is not an ancestor, and `git ls-tree` lists only `home/dot_dsh/profiles`. So the updater's refusal (`:1905-1908`) holds on every opted-in host until U240 merges.

## Comparable baseline

A package manager's `link:` dependency, plus an installer that writes the same symlink itself, guarded by physical-path containment and `rename(2)`.

## Trust boundaries and strongest controls

- **Manifest to rendered rows.** Constants, a strict model regex, and the CI drift check.
- **Profile author to child command.** The same principal; the plugin's defaults apply.
- **`DSH_HOME` layout to the link.** Every input resolved physically under `DSH_HOME`, a non-symlink at the link name refused, and atomic relinks.
- **Manifest commit to the build (U226, kept by the merge).** A 40-hex refusal before any read, the sha256-pinned archive, and a prefix-assigned build environment.

## Prior coverage

- **run-7** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-7`, source 1d23154b) is the U227b round-3 sweep. Its six units are re-checked here with re-mapped lines.
- **run-8** (source 1a4d712f) is the newest ledger and is carried for every other unit. Its five U249 units are absent at this head (changed source).

No prior run holds a finding.

## Output directory

The brief names `run-8`, which holds the U264 sweep. This run writes to `run-9` and leaves `run-8` untouched.

## Companion selection

Selected:
- `DESKTOP-MOBILE-AND-LOCAL-IPC.md`: privileged-helper, local-file and install-path blocks.
- `SUPPLY-CHAIN-AND-RELEASE.md`: plugin trust, and the mutable-build-input block for the merge resolution.

Every other companion is excluded with its reason in the ledger.

## Execution and independence limits of this run

No target code ran, by task rule. The delegation tool (Task) and eval kernel are denied by policy on this seat, so every phase ran in the parent. `run-metadata.json` records the run as incomplete for that reason.
