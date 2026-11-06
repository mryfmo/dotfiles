# Security audit report: dotfiles at 1d23154b71932e74902cf9ac95b2eeaf7b055215

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U227b change b49be338..1d23154b71932e74902cf9ac95b2eeaf7b055215 (branch `feat/dsh-profile-login-route`): U227b at 385bd1a1 and U227c at 1d23154b, nine files.

The brief names `d1ecd495` as the base and `c4195463..HEAD` (29 paths) as the change, and calls run-6 the U227b head; run-6 swept U254. I hunted the two U227b/U227c commits. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran.

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** I carried run-6 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-6`, source 50dd240c). U254 is absent at this head, so its four units carry as changed-source, out-of-scope units, and its 33 out-of-scope units carry. No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. Each of the brief's questions:

**The rendered rows, as configuration an attacker who writes the profile could abuse.**
- `command` and `args` come from the constant `DSH_GATEWAY_COMMAND` (`generate-agent-configs.py:172`).
- Every model must match `claude-` plus the launcher-safe form (`:167`, `:237-241`), so no manifest value reaches the YAML with structure.
- The rendered row has no `env` and no `cwd` (`cordis.patch.yml:11-27`), so the plugin's environment allowlist and `homedir()` apply.
- Someone who can write `~/.dsh/profiles/thak` already decides which code DSH loads (the existing `!!js` `configPath` row is one example). The command row is that same operator authority, not a new boundary.

**The updater's symlink step: target, refusals, idempotence, and a pre-existing path at the link name.**
- The plugin directory, the profile and its `node_modules` are each resolved physically and must lie under `DSH_HOME`'s physical path (`update-agent-assets.sh:2073-2098`, `:1984-1994`).
- A `plugins/omp-gateway` linked outside `DSH_HOME` is refused with nothing installed.
- A directory or a file at the link name is refused and left alone (`:2103-2106`).
- A symlink at the link name is replaced by writing a temporary link and then calling `os.replace` (`:2000-2009`). `rename(2)` replaces the link itself and never follows it, so a failure leaves the previous link standing.
- The step converges on the already-installed exit, the fresh install and repair (`:2188`, `:2274`, `:2277`).

**That no key or Ollama row survives.**
- `DSH_ROUTES` is `omp-gateway` only (`generate-agent-configs.py:164`).
- Every dsh row names a `claude-` model on `omp-gateway` (`agent-config.yaml:552-598`).
- The rendered profile carries no providers block and disables both DeepSeek LLM rows (`cordis.patch.yml:2-10`).
- A case-insensitive search for `ollama`, `api key`, `apiKey`, `OLLAMA_` and `DEEPSEEK_API` finds no DSH row.

## 3. Confirmed findings

None.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None.

## 6. Hardening notes and positive patterns

These are not findings.

### Hardening

1. **Merge ordering.** The profile names a plugin this head does not deploy: `home/dot_dsh/plugins/omp-gateway` belongs to U240, which is not an ancestor. If U227b merges first:
   - `chezmoi apply` deploys a profile with `llm-deepseek` disabled and no gateway, so DSH reaches no model;
   - `make update`'s DSH step refuses with exit 1 on every opted-in host (`update-agent-assets.sh:2073-2076`).

   This fails closed, so it is availability only. U240 should merge first, or both together.
2. **Predictable temporary link name.** It is `${link}.tmp.$$` (`update-agent-assets.sh:2000`). It sits in the operator's own `node_modules` under `DSH_HOME`, and `rm -f` clears a stale one first. No other principal can place it.

### Positive patterns

- Physical-path containment for every input of the link step.
- Atomic relink by `rename(2)`.
- A refusal, never a removal, for a non-symlink at the link name.
- Convergence on every exit.
- Constants and a strict model regex for the rendered rows.
- The API-key and Ollama routes removed outright, not just disabled.
- Tests for each refusal (`tests/unit/test_update_agent_assets.py:966-1283`).

## 7. Coverage summary

From `coverage-ledger.json` (43 units):

| Status | Units |
|---|---|
| covered | 6 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 37 |

The six covered units are all new, each owned by `parent-hunter` with source checks:
1. the rendered gateway rows (injection);
2. the link target (resource and file handling, install-path trust);
3. the relink (business logic);
4. the withdrawn key routes (secrets);
5. the `link:` dependency and merge ordering (plugin trust);
6. the tests (obvious things).

The 37 out-of-scope units are carried from run-6.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Neither was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
