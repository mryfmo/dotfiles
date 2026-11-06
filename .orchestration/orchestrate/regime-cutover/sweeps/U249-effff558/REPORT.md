# Security audit report: dotfiles at effff558445ded75c7d7dd6855086b4490d21133

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U249 change b49be338..effff558445ded75c7d7dd6855086b4490d21133 (branch `feat/brief-check-ci-gates`). That is one commit touching six files:
- `scripts/orchestrator/brief-check.py`
- its deployed copy `home/dot_local/bin/common/executable_brief-check.py`
- the manifest pin in `home/dot_agents/agent-config.yaml`
- `scripts/generated-agent-outputs.json`
- one README paragraph in `scripts/orchestrator/README.md`
- `tests/unit/test_brief_check.py`

The brief names `d1ecd495` as the base and `git diff --name-only c4195463 HEAD` (29 paths) as the change. The head's parent is b49be338 (main after U241), so I hunted the U249 commit alone, which matches the GOAL's six files. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran. The deployed copy and the pin were compared over committed blobs (`git cat-file`, `cmp`, `shasum`).

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** I carried run-3 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-3`, source 6531a212). That run swept U240, which is absent at this head, so:
- its nine covered omp-gateway units carry as `prior_covered_changed_source` and stay out of scope;
- its 19 out-of-scope units carry as `prior_out_of_scope`.

run-3 holds no finding.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. The checker is a deterministic gate that the coordinator runs over briefs the coordinator writes. No lower-trust principal supplies brief text, so the rule's limits are process limits, not boundary crossings.

**Can a crafted brief satisfy the rule without naming a gate?** Only by using a gate's wording. Each gate term is escaped and matched as a whole word in either class (`brief-check.py:267-278`, `:287`, `:414-423`), so partial or misspelled words do not count. But a sentence that merely mentions a gate (for example "no unittest run") satisfies it. The docstring states this limit: whether a gate ran is the pasted lines, read by the coordinator (`:35`).

**Can it crash the checker into an exit the levers misread?** No:
- the new functions index nothing that can be empty (`:378-388`, `:405-411`, `:414-423`);
- the patterns are fixed literal alternations;
- unreadable or ungrammatical briefs exit 2 (`:464-471`);
- exit 0 is reached only by an explicit return with no reasons (`:475`).

**The deployed copy's pin.** The source, the deployed copy, the manifest pin (`home/dot_agents/agent-config.yaml:894`) and the generated-outputs record (`scripts/generated-agent-outputs.json:403`) all carry sha256 `14015d643313a2af2794c8488ec8bf7bc460c2417eeb9b3478a6fe7a2fefd92d`. The self-check refuses any other bytes (`:79-121`).

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

1. **The gate rule is word presence** (`brief-check.py:414-423`). An ACCEPTANCE sentence that names a gate in order to say it is not run satisfies the rule. Requiring the term at the start of a numbered item, or inside a backticked command span, would tie it to a command the worker actually runs.
2. **Only backticked, whitespace-free SCOPE spans switch the rule on** (`brief-check.py:378-388`). A repository path written in prose, or in a backticked span that holds a space, leaves the rule off.
3. **A crash looks like a refusal.** An uncaught exception exits 1, the refusal code, with a traceback but no reason line (`brief-check.py:478-479`). That fails closed. Catching `Exception` in `main` and returning 2 would reserve 1 for judged refusals.

### Positive patterns

- Escaped, whole-word, compiled gate patterns, with each class kept separate.
- Explicit exemptions for absolute, home, parent and `$VAR` paths and for bare words, matching the sweep-brief shape. That is why this U255 brief itself needs no gate.
- A byte-identical deployed copy, held to its sha256 pin by the script's own self-check.
- Tests cover every lint gate beside every test gate, each class alone, the sweep shape, and a missing ACCEPTANCE (`tests/unit/test_brief_check.py:478-531`).

## 7. Coverage summary

From `coverage-ledger.json` (33 units):

| Status | Units |
|---|---|
| covered | 5 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 28 |

The five covered units are all new, each owned by `parent-hunter` with source checks:
1. the ACCEPTANCE gate rule (business logic);
2. SCOPE repository-path detection (business logic);
3. exit codes on malformed briefs (wildcard);
4. the deployed copy and pin (generated-source provenance);
5. the tests and README (obvious things).

The 28 out-of-scope units are carried from run-3: its nine omp-gateway units, whose source is absent here, and its 19 out-of-scope units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Neither was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
