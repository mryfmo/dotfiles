# Security audit report: dotfiles at 2256b56c83975cef17d8058ede5660c25f6cf35f

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U240 change d1ecd495..2256b56c83975cef17d8058ede5660c25f6cf35f (branch `feat/dsh-omp-gateway-adapter`): 15 files under `home/dot_dsh/plugins/omp-gateway/`. Since the run-3 sweep at 6531a212 there are two commits:
- **aa788c82:** the proof's patch row drops its environment override.
- **2256b56c:** `#kill` forgets the child before signalling it; `EMPTY_RESPONSE` for an empty reply; forged-tag and protocol-guard tests.

The brief's CONTEXT again names `git diff --name-only c4195463 HEAD` as the change, and calls run-4 the U240 head; run-4 actually swept U249. I followed the GOAL. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code, test or proof runner was executed.

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** I carried run-4 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-4`, source effff558).
- Its five brief-check units carry as changed-source, out-of-scope units, because U249 is absent here.
- The nine U240 units it held out of scope are back in scope and re-checked at this head with re-mapped lines.
- Its other 19 out-of-scope units carry over.

No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. Each of the brief's questions:

- **Child command and environment rows.** The child is spawned with an argv array and no shell (`gateway-client.mjs:132`), with only the allowlisted environment names (`:26-33`). The proof now uses the plugin's defaults (`config.mjs:4-7`, `proof/run-proof.mjs:44`), none of which is a credential variable. The rows come from the operator's own profile.
- **JSON-line parser.** Each request is one `JSON.stringify` line (`:107`) on a private pipe. Replies need the ready line first, an integer ID and status, and a pending ID; any violation kills the child (`:183-217`). Round 3 adds tests for each guard (`test/gateway-client.test.mjs:142-203`).
- **Abort and exit paths.** Round 3's forget-before-kill (`:226-233`) is sound:
  - every `#kill` follows a `#fail` that has already rejected the pending requests and the gate, which also clears the ready timer (`:155-158`, `:219-224`);
  - the old child's `error`, `close` and stdout handlers check that it is still the current child (`:161`, `:167`, `:178`), so its late events cannot touch the new child's requests;
  - no stray ready timer can fire against the new child.
- **What the proof runner writes, and where.** Only fixed names under a fresh `mkdtemp` home, or the operator's `--home` (`proof/run-proof.mjs:18-46`, `:63-65`, `:74-77`). `rmSync` is never recursive.
- **Can user content forge or escape the `<dsh-system>` block?** No. The block is a separate text block built only from system sources (`translate.mjs:20`, `:24-28`, `:185-190`). User text blocks stay separate. With no `system` field sent (`:49`), a forged block carries the same user-turn provenance as the real one. No code reads the tag (`:10`, `:186`). Round-3 tests pin that a forged tag in user text stays user text, with and without system text (`test/translate.test.mjs:129-153`).

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

1. **The stderr handler is unguarded (new in round 3).** It is the one child handler that does not check identity (`gateway-client.mjs:174-176`). After a kill and respawn, the old child's late stderr is appended to the tail `#ensureChild` reset for the new child (`:134`), so a later `GATEWAY_EXIT` message can quote the old child. A `this.#child === child` guard, as on stdout (`:178`), would close it.
2. **`close()` doesn't wait (extended in round 3).** It waits for `close` with no deadline (`:121-128`), and since round 3 it returns at once for a child that was killed and forgotten (`:226-233`). A gateway that ignores stdin EOF hangs disposal, and one that ignores SIGTERM outlives it. A bounded wait followed by SIGKILL would close both.
3. **The tag is not a trust boundary** (carried). DSH's system text reaches the model with user-turn provenance. A future reader that trusts `<dsh-system>` would have to take it only from the leading position, and would need tag escaping in user and tool text.
4. **Error text forwards gateway output** (carried). The stderr tail and up to 200 characters of an unparseable line reach `LlmError` (`:168`, `:189`; `index.mjs:49`). Drop the tail before any session-log-uploading profile loads the plugin.
5. **Abort is all-or-nothing** (carried). Aborting one request kills the shared child and fails every concurrent request (`:91-94`, `:219-224`).
6. **No line-length bound** on the child's stdout (`:177`) (carried).
7. **The proof runs without DSH's command sandbox** (carried). The scratch profile disables `bash-sandbox` and passes `dsh` the full environment (`proof/run-proof.mjs:41`, `:63`).

### Positive patterns

- Forget-before-kill, with identity-guarded `error`, `close` and stdout handlers.
- `EMPTY_RESPONSE` on a degenerate reply (`translate.mjs:72-76`).
- In-process failure injection for every protocol guard.
- Forged-tag tests.
- An environment allowlist with no credential defaults.

### Outside the target

DSH's tool dispatch, approval, sandbox and system-prompt assembly are upstream code and were not reviewed here.

## 7. Coverage summary

From `coverage-ledger.json` (33 units):

| Status | Units |
|---|---|
| covered | 9 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 24 |

The nine covered units are all U240 units re-checked at this head, each owned by `parent-hunter` with source checks:
1. config to spawn;
2. the JSON-line protocol;
3. lifecycle;
4. error text;
5. translation;
6. the `<dsh-system>` fold;
7. proof-runner writes;
8. plugin loading;
9. stub, fixtures and tests.

The 24 out-of-scope units are run-4's five U249 units (changed source) and its 19 out-of-scope units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Neither was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
