# Security audit report: dotfiles at 6bc0c2cbd44a76901c33acc36458518a300cb2ab

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U240 change d1ecd495..6bc0c2cbd44a76901c33acc36458518a300cb2ab (branch `feat/dsh-omp-gateway-adapter`): 16 files under `home/dot_dsh/plugins/omp-gateway/`. Since the U240-2256b56c sweep there are two commits:
- **5f159044 (U250):** adds `test/use-cases.test.mjs`, with 47 automated items.
- **6bc0c2cb:** rewrites `proof/run-proof.mjs`. It adds the `--case` selector, a constant `CASES` table with expected-output predicates, a per-case model overlay, and a second provider route in the scratch profile.

Every other plugin file is byte-identical to 2256b56c. The brief's CONTEXT names `git diff --name-only c4195463 HEAD` (one file) as the change. At this head it lists 17 files: the 16 plugin files and `tests/unit/test_validate_agent_assets.py`, which d1ecd495..HEAD does not touch. I followed the GOAL. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Source ref.** The checkout was clean at the head both before and after the run (`preflight.txt`, `validation.txt`).

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. By task rule, no target code, test, stub or proof runner was executed.

**Independence gap.** The platform's delegation tool (Task) and eval kernel are denied by policy on this seat. The Phase 1 reconnaissance launch was refused with "blocked by user policy". So reconnaissance, the hunter wave and both critics ran in the parent (`parent-hunter`), and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** This seat has no earlier run. I carried the store's U240-2256b56c sweep records (`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/sweeps/U240-2256b56c`, run dotfiles-run-5, source 2256b56c, 33 units, 0 findings).
- **Same source.** Its seven covered U240 units whose source is unchanged are re-checked at this head as `prior_covered_same_source`. Their line references hold, and U250's items now add evidence to each.
- **Changed source.** The proof-runner and stub/fixtures/tests units are re-checked as `prior_covered_changed_source`, with their lines re-mapped.
- **New units.** Two are added: the test's dsh-llm resolution, and the proof's cases and provider routes.
- **Out of scope.** Its 24 out-of-scope units carry over as `prior_out_of_scope`.
- **Findings.** No prior record of any verdict exists, so there are no carried confirmations and no changed-source revalidations of a finding.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. Each of the brief's questions:

- **Child command and environment rows.** Unchanged since 2256b56c.
  - The child is spawned with an argv array and no shell (`gateway-client.mjs:132`), with only the allowlisted environment names (`:26-33`). The defaults hold no credential name (`config.mjs:4-7`).
  - The rows come from the operator's own profile.
  - U250 items f2, f6 and f7 pin the allowlist and the row checks (`test/use-cases.test.mjs:632-649`, `:694-713`, `:715-729`).
- **JSON-line parser.** Each request is one `JSON.stringify` line (`gateway-client.mjs:107`) on a private pipe. A reply needs the ready line first, an integer ID and status, and a pending ID. Any violation kills the child (`:183-217`). U250 d4, d5, d9 and d10 exercise each guard against a live child (`test/use-cases.test.mjs:446-533`).
- **Abort and exit paths.** Unchanged.
  - `#kill` forgets the child before signalling it (`gateway-client.mjs:226-233`).
  - Every kill follows a `#fail` that has already rejected the pending requests and the gate (`:219-224`, `:155-158`).
  - The `error`, `close` and stdout handlers are identity-guarded (`:161`, `:167`, `:178`).
  - U250 d2, d6 and d8 cover the ready timeout, abort, and close-then-respawn.
- **What the proof runner writes, and where.** It writes only fixed names under a fresh `mkdtemp` home, or under the operator's `--home` (`proof/run-proof.mjs:29-59`, `:82-86`, `:92-93`). The round-4 additions:
  - The new per-case files are `<case>-model.patch.yml` (`:83`), whose `<case>` must be a `CASES` key (`:123-125`), and `turn-N.stdout`/`.stderr` from constant titles (`:92-93`).
  - `rmSync` is never recursive (`:40`, `:103`).
  - The U250 tests write only under one `mkdtemp` scratch (`test/use-cases.test.mjs:23`).
- **Can user content forge or escape the `<dsh-system>` block?** No.
  - The block is a separate text block built only from system sources (`translate.mjs:20`, `:24-28`, `:185-190`). User text blocks stay separate.
  - No `system` field is sent (`:49`), so a forged block carries the same user-turn provenance as the real one. No code reads the tag.
  - U250 c5 (`test/use-cases.test.mjs:385-396`) pins that a forged tag in user text stays a separate user block, with and without system text.

## 3. Confirmed findings

None.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None. See `NEEDS-VALIDATION.md` for the one carried note that would become a lead under a different loading profile.

| Title | Trace | Blocker | Local next step | Owner-observed check |
|---|---|---|---|---|
| — | — | — | — | — |

## 6. Hardening notes and positive patterns

These are not findings: none has a lower-trust principal crossing a boundary at this head.

### Hardening

1. **The test suite imports DSH from outside the repository (new).** `test/use-cases.test.mjs:29-38` maps `@deepseek-ai/dsh-llm` to whatever file `DSH_LLM_PACKAGE` names, or to `~/.dsh/dsh/current/.../index.js`. `node --test .` (`package.json:19`) therefore runs that code with the operator's authority. Both inputs are the operator's own. A diagnostic that prints the resolved path would make the input visible in test output.
2. **The proof has a second route (new).** The proof profile registers the adapter for `openai-siwc` as well as `claude-bridge` (`proof/run-proof.mjs:57`). Its `siwc` case (`:25`) sends an `openai-siwc/gpt-6-astra` turn to whatever `--command` names. Against the real gateway that turn is expected to answer 404. If the gateway ever served that ID, the case would spend the operator's quota and then fail its predicate.
3. **The U250 scratch directory is left behind (new).** It is never removed (`test/use-cases.test.mjs:23`). Its logs hold the dummy request bodies, the child's environment names and the child's cwd (the operator's home path for f3), but no values.
4. **The stderr handler is unguarded** (carried). It is the one child handler that does not check identity (`gateway-client.mjs:174-176`). After a kill and respawn, the old child's late stderr can appear in the new child's `GATEWAY_EXIT` message. A `this.#child === child` guard would close it.
5. **`close()` doesn't wait** (carried). It waits for `close` with no deadline (`:121-128`), and returns at once for a killed and forgotten child (`:226-233`). A bounded wait followed by SIGKILL would close both gaps.
6. **The tag is not a trust boundary** (carried). DSH's system text reaches the model with user-turn provenance. A future reader that trusts `<dsh-system>` would have to take it only from the leading position, and would need tag escaping in user and tool text.
7. **Error text forwards gateway output** (carried, now asserted). The stderr tail and up to 200 characters of an unparseable line reach `LlmError` (`:168`, `:189`; `index.mjs:49`). U250 d3 (`test/use-cases.test.mjs:437-444`) now asserts the tail in the message. Drop the tail, and change d3 with it, before any session-log-uploading profile loads the plugin.
8. **Abort is all-or-nothing** (carried). Aborting one request kills the shared child and fails every concurrent request (`:91-94`, `:219-224`).
9. **No line-length bound** on the child's stdout (`:177`) (carried).
10. **The proof runs without DSH's command sandbox** (carried). The scratch profile disables `bash-sandbox` (`proof/run-proof.mjs:53`) and passes `dsh` the full environment (`:91`). Round 4's `loop3` case (`:24`) adds a third tool-calling prompt.

### Positive patterns

- `--case` is allowlisted with `Object.hasOwn` over a constant table, so no flag text reaches a file name or `dsh` argv (`proof/run-proof.mjs:123-125`).
- The proof's exit code now needs each case's expected output, not only the exit status (`:71-80`).
- The U250 items exercise every protocol guard and lifecycle path against a live child, using only the stub or an inline scripted gateway.
- The scripted child logs environment names, not values (`test/use-cases.test.mjs:58`).
- Static tests: a credential-shape scan of the plugin's files, an import allowlist with a scan for network calls, and an `lsof` check for listening sockets (`:757-792`).
- Carried: forget-before-kill with identity-guarded handlers, `EMPTY_RESPONSE`, an environment allowlist with no credential defaults, and the forged-tag tests.

### Outside the target

DSH's tool dispatch, approval, sandbox and system-prompt assembly are upstream code, and so is the omp gateway. Neither was reviewed here.

## 7. Coverage summary

From `coverage-ledger.json` (35 units):

| Status | Units |
|---|---|
| covered | 11 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 24 |

The 11 covered units are all owned by `parent-hunter`, with source checks at this head:
- **Same source (7):**
  1. plugin loading;
  2. config to spawn;
  3. lifecycle;
  4. error text;
  5. the JSON-line protocol;
  6. the `<dsh-system>` fold;
  7. translation.
- **Changed source (2):** proof-runner writes, and stub/fixtures/tests.
- **New (2):** the test's dsh-llm resolution, and the proof's cases and provider routes.

The 24 out-of-scope units are:
- the top-level directories `.claude`, `.github`, `.orchestration`, `.ua`, `docs`, `home` outside the plugin, `install`, `plans`, `scripts`, `tests` and `vendor`;
- the repository root files;
- the carried units for the brief-check, asset-pin and generator surfaces of earlier units (U226 and U249), which are not part of this change.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work.
- The post-wave critic checked every changed path, both new surfaces, and every brief question against a unit.
- The final-clean critic found no planned unit left.

Neither critic was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
