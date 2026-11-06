# Security audit: dotfiles at 385bd1a1e169dc6f2fcef31f521036e69b6eb24d (U227b head)

## 1. Run, scope and limits

**This is a partial and incomplete pass.**

| Item | Value |
| --- | --- |
| Profile | `standard` |
| Scope | Scoped to the U227b commit, `b49be338..385bd1a1`: 9 paths, +425 −102, the brief's own figures. |
| Out of scope | Every other area is recorded `out_of_scope` in the coverage ledger. |
| Source ref | `385bd1a1`, clean worktree. |
| Budget | None set. |
| Execution | Source review only. The brief forbids executing target code, so every check is `method: source`. |

**Brief corrections.**

- The brief names `d1ecd495` as the base. The head's parent is `b49be338` (U241 landed on main after `d1ecd495`), and `d1ecd495..HEAD` adds U241's test file.
- The CONTEXT line `git diff --name-only c4195463 HEAD` is the U224 sweep's text and was not used.
- The brief calls run-4 the U227b head. run-4 is this seat's previous run, but it swept U244 (`d1fd54ba`).

**Prior run.**

- run-4's 34 units are carried with the same IDs as `out_of_scope`.
- Its 8 U244 units cover source that is not in this head; the lever here still carries the brief reading. Its other 26 were already out of scope.
- There is no prior record.

**Incomplete, `run_status: "incomplete"`, reason `independent_agents_unavailable`.**

- The seat's tool policy denies the Task tool, so no reconnaissance, hunter, critic or verifier agent ran. The parent did reconnaissance and hunting itself.
- The hunt produced no candidate, so no validation was owed. But the mandatory critics did not run, so this report makes **no clean-coverage claim**.

## 2. Security posture

The change removes the API-key route: the Ollama provider with `apiKeyEnv OLLAMA_API_KEY` is gone from the renderer, the rendered profile and the manifest.

**The new gateway row is static configuration.** It sets the command `omp` with `auth-gateway stdio`, one provider and the model list, and has no `env` or `cwd`. The generator writes the command from constants, and the manifest's only input, the model ids, is restricted to `claude-` plus a launcher-safe tail. A writer of the profile is the operator.

**The updater's plugin link writes one relative symlink at a fixed path.** Before anything is downloaded, it refuses three states:

- a plugin path that is not a directory
- a `node_modules` that is a symlink or not a directory
- a non-symlink at the link name

`ln -sfn` replaces an existing symlink without following it, so every run converges on the same link.

**Answers to the brief's three questions:**

1. The rendered rows give a profile writer nothing beyond the fixed login command.
2. A pre-existing path at the link name is replaced only when it is a symlink, and refused otherwise.
3. No key or Ollama row survives.

## 3. Confirmed findings

None.

## 4. Confirmed finding details

None.

## 5. Needs validation

None.

## 6. Hardening notes and positive patterns

These are not findings.

Hardening notes:

- **Plugin provenance and merge order.** The link target `$DSH_HOME/plugins/omp-gateway` is accepted as any directory, with no pin or digest. The manifest note says chezmoi deploys it, but its source (the U240 commits) is not in this head, so at this head nothing in the tree deploys it. On an opted-in host, every `make update` stops at the refusal (update-agent-assets.sh:2032-2035, exit 1) until that directory exists, and whatever directory sits there is then linked and loaded. Only the operator writes that path, so this is not a boundary violation. It does argue for landing U240 first, and for giving the plugin the kit's usual pinned provenance.
- **Bare command name.** `command: omp` is resolved by the harness process's PATH when the plugin spawns it. An absolute path would pin which binary receives the login. The adapter's spawn code is not in this head, so its resolution rule is not source-visible here.

Positive patterns:

- The validator refuses the withdrawn route and Ollama-form ids, so a regression fails the render.
- The default model must come from the interactive profile.
- The link step's checks run before any download, and its failure leaves current, the wrapper, the trees and the receipt untouched (tested).
- The removed tests are replaced by tests of the new route, including one that asserts no API key or Ollama route stands in the rendered files.

## 7. Coverage summary (coverage-ledger.json, 41 units)

| Ledger status | Count | Units |
| --- | --- | --- |
| covered | 7 | All in scope: the gateway row, the manifest model rows, the withdrawn key route, the plugin link step, the `link:` dependency, the tests, and obvious things over the diff. |
| candidate | 0 | — |
| blocked | 0 | — |
| deferred | 0 | — |
| out_of_scope | 34 | Carried from run-4: 8 U244 units, 14 U224 units, and 12 area units, namely `.claude`, `.github`, `.orchestration`, `.ua`, `docs`, `install`, `plans`, `vendor`, the unchanged paths of `home`, `scripts` and `tests`, and the root files. |

- **Excluded companions:** AI-AND-LLM, DESKTOP-MOBILE-AND-LOCAL-IPC, CLOUD-AND-DEPLOYMENT and WEB-PROTOCOL-AND-AUTH, with reasons in the ledger.
- **Critic result:** no independent critic ran. No clean-coverage claim is made.
