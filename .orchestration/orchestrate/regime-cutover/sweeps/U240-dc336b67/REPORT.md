# Security audit report: dotfiles at dc336b67ebe6456c976716288b9587555d802922

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U240 diff d1ecd495..dc336b67ebe6456c976716288b9587555d802922 (branch `feat/dsh-omp-gateway-adapter`). The diff adds 15 files under `home/dot_dsh/plugins/omp-gateway/` and changes no existing file.

The brief's CONTEXT names `git diff --name-only c4195463 HEAD` as the change, but at this head that command lists 16 paths, not the U240 change. I followed the GOAL's description. Every other top-level directory and the root files are `out_of_scope` ledger units, and no coverage claim is made for them.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code, test or proof runner was executed: the task forbids it, and the seat provides no empty allowlisted environment or resource limits.

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** I carried run-1 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-1`, source 0b475694). That run swept U226, not U240 as the brief's CONTEXT says. This head descends from d1ecd495, which does not contain U226, so:
- run-1's six covered units carry as `prior_covered_changed_source` and stay out of scope (their source is absent here);
- its 13 out-of-scope units carry as `prior_out_of_scope`.

run-1 holds no finding of any verdict, so there are no carried confirmations and no revalidation targets.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives the scoped hunt over the omp-gateway plugin. The design keeps the credential inside omp:
- the child gets only an allowlisted set of environment names;
- it is spawned with an argv array and no shell;
- requests are single `JSON.stringify` lines on a private pipe to a child this client spawned itself;
- replies must match an outstanding integer ID, or the child is killed.

Model tool calls are translated, not executed. No profile at this head loads the plugin. The only loader is the proof runner's scratch profile, which is an operator command.

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

These are not findings: none has a lower-trust principal crossing a boundary at this head.

### Hardening

1. **Error text forwards gateway output.** Error messages carry the gateway child's stderr tail (up to 4096 bytes; `gateway-client.mjs:9`, `:168`, `:237-240`) and up to 200 characters of an unparseable stdout line (`:189`) into `LlmError` (`index.mjs:49`). Before any profile that uploads session logs loads this plugin, keep the tail out of the message, or bound it to known-safe fields.
2. **Abort is all-or-nothing.** Aborting one request kills the shared child and rejects every concurrent request of the same client (`gateway-client.mjs:91-94`, `:219-224`). This is same-process availability only.
3. **`close()` has no deadline.** It waits for the child to exit after stdin EOF with no time limit (`gateway-client.mjs:121-128`), so a gateway that ignores EOF would hang plugin disposal. A bounded wait followed by SIGTERM closes that.
4. **No line-length bound.** `readline` places no limit on line length from the child's stdout (`gateway-client.mjs:177`). The child is the operator's own process, so this is robustness only.
5. **The proof runs without DSH's command sandbox.** The proof runner's scratch profile disables `bash-sandbox` (`proof/run-proof.mjs:42`) and passes `dsh` the full environment (`:64`). With `--command omp`, it drives the real model through headless turns with no command sandbox. The prompts are fixed and the operator runs it; keeping the sandbox on for real-gateway runs would narrow it.

### Positive patterns

- argv spawn without a shell, and an environment allowlist whose defaults name no credential variable (`config.mjs:4-7`, `gateway-client.mjs:26-33`, `:132`).
- Request framing through `JSON.stringify`, so content cannot add a line (`:107`). A ready gate, then strict ID correlation, and any protocol violation kills the child (`:183-217`).
- Typed role mapping with no parsing of text for roles. Unknown reply blocks are dropped rather than guessed (`translate.mjs:12-92`).
- The proof runner writes only under a fresh `mkdtemp` home (or the operator's `--home`), using fixed names, and removes nothing recursively (`proof/run-proof.mjs:19-47`, `:75-78`).

### Outside the target

The adapter's tool calls land in DSH's own tool dispatch, approval and sandbox. That is upstream code and was not reviewed here.

## 7. Coverage summary

From `coverage-ledger.json` (27 units):

| Status | Units |
|---|---|
| covered | 8 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 19 |

The eight covered units are all new, all under `home/dot_dsh/plugins/omp-gateway`, each owned by `parent-hunter` with source checks:
1. config to spawn (injection);
2. the JSON-line protocol and reply correlation (protocols and local IPC);
3. lifecycle: abort, timeout, exit and close (business logic);
4. error text (secrets in errors);
5. translation and tool calls (AI/LLM);
6. proof-runner writes (resource and file handling);
7. deployment and loading (plugin trust, supply chain);
8. stub, fixtures and tests (obvious things).

The 19 out-of-scope units are run-1's six changed-source units and its 13 out-of-scope units: `.claude`, `.github`, `.orchestration`, `.ua`, `docs`, `home` (outside the plugin directory), `install`, `plans`, `scripts`, `tests`, `vendor`, the root files, and the build-environment unit.

**Excluded companions.** Web/auth, client-side, cloud, resource exhaustion, data isolation and memory safety are excluded, each with its reason in every unit.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Neither was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
