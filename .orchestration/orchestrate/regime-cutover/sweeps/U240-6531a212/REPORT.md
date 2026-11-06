# Security audit report: dotfiles at 6531a212d627314f8aa843e4d9f18cf63c76da35

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U240 change d1ecd495..6531a212d627314f8aa843e4d9f18cf63c76da35 (branch `feat/dsh-omp-gateway-adapter`): 15 files under `home/dot_dsh/plugins/omp-gateway/`. Round 2 (dc336b67..6531a212) changes `translate.mjs` and its test, and removes the shebang lines of `proof/run-proof.mjs` and `stub-gateway.mjs`.

The brief's CONTEXT again names `git diff --name-only c4195463 HEAD` as the change. I followed the GOAL's description. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code, test or proof runner was executed: the task forbids it, and the seat provides no empty allowlisted environment or resource limits.

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** I carried run-2 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-2`, source dc336b67, 0 findings).
- Its eight covered U240 units were re-checked at this head with re-mapped lines. Five read files that round 2 changed, so they carry as `prior_covered_changed_source`; three carry as `prior_covered_same_source`.
- Its 19 out-of-scope units carry as `prior_out_of_scope`.
- There are no carried confirmations and no needs-validation records.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. The round-1 design holds at this head:
- the child gets an allowlisted environment and is spawned with an argv array and no shell;
- each request is one `JSON.stringify` line on a private pipe;
- replies must match an outstanding ID, or the child is killed;
- tool calls are translated, not executed;
- no profile loads the plugin.

**Can user content forge or escape the `<dsh-system>` block?** Neither yields a boundary crossing.
- `foldSystem` (`translate.mjs:180-185`) builds the block as a separate text block, only from `options.system` and system-role rows (`:20`, `:24-28`). User text blocks stay separate JSON blocks, so they can neither enter the block nor close it.
- Since no `system` field is sent (`:49`), the block is itself user-turn text. A user or tool text that spells `<dsh-system>` carries exactly the provenance the real block has, and no more.
- System text that contains `</dsh-system>` only moves the rest of its own text down to plain user text, never up.
- No code reads the tag. It is defined at `:10`, and only the writer (`:181`) and the test use it. The model's interpretation is the only consumer, and the AI companion's core discipline does not count persuasion without a deterministic control as a boundary failure.

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

1. **The tag is not a trust boundary.** With no `system` field, DSH's own instructions, and any project instruction text DSH puts into its system prompt, reach the model with user-turn provenance under the gateway's preset prompt. If any code ever treats a `<dsh-system>` block as authoritative, it must accept the block only from the leading position the adapter writes, and the adapter would then need to escape the tag in user and tool text. (New in round 2.)
2. **Error text forwards gateway output.** Error messages carry the gateway child's stderr tail (up to 4096 bytes) and up to 200 characters of an unparseable stdout line into `LlmError` (`gateway-client.mjs:168`, `:189`; `index.mjs:49`). Keep the tail out before any session-log-uploading profile loads the plugin. (Carried.)
3. **Abort is all-or-nothing.** Aborting one request kills the shared child and rejects every concurrent request of the same client (`gateway-client.mjs:91-94`, `:219-224`). (Carried.)
4. **`close()` has no deadline** (`gateway-client.mjs:121-128`). (Carried.)
5. **No line-length bound** on stdout lines from the child (`gateway-client.mjs:177`). (Carried.)
6. **The proof runs without DSH's command sandbox.** The scratch profile disables `bash-sandbox` (`proof/run-proof.mjs:41`) and passes `dsh` the full environment (`:63`). (Carried, lines re-mapped.)

### Positive patterns

- The fold builds its block only from system sources, and mutates only arrays that `toMessagesBody` itself built, never DSH's history objects (`translate.mjs:165-170`, `:180-185`, `:194-201`).
- Four tests pin the fold's shapes (`test/translate.test.mjs:62-127`).
- The round-1 controls (argv spawn, environment allowlist, `JSON.stringify` framing, strict ID correlation) are unchanged.

### Outside the target

DSH's tool dispatch, approval and sandboxing, and its system-prompt assembly, are upstream code and were not reviewed here.

## 7. Coverage summary

From `coverage-ledger.json` (28 units):

| Status | Units |
|---|---|
| covered | 9 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 19 |

The covered units are the eight re-checked run-2 plugin units plus the new `<dsh-system>` fold unit (AI/LLM: prompt role and provenance confusion), each owned by `parent-hunter` with source checks. The 19 out-of-scope units are carried from run-2.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Neither was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
