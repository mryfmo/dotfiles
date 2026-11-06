# Security audit report: dotfiles at 1a4d712f040bd811af284f1cd99a269945d7c14a

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U249 change against the merged main, cf68daf67..1a4d712f040bd811af284f1cd99a269945d7c14a (branch `feat/brief-check-ci-gates`). It touches six files:
- `scripts/orchestrator/brief-check.py`
- its deployed copy `home/dot_local/bin/common/executable_brief-check.py`
- the manifest pin in `home/dot_agents/agent-config.yaml`
- `scripts/generated-agent-outputs.json`
- one README paragraph in `scripts/orchestrator/README.md`
- `tests/unit/test_brief_check.py`

Round 2 (effff558..1a4d712f) merges main (which now holds U254, #691) and rewords one docstring line, `brief-check.py:31`, which used to spell a temporary-directory path. The deployed copy and the pin move with it. No code line changes, so every code line number is the same as in run-4.

The brief names `d1ecd495` as the base and `git diff --name-only c4195463 HEAD` (29 paths) as the change. The diff against the merged main is exactly the GOAL's six files, so I hunted those. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Output directory.** The brief names `run-4`, which already held the U255 sweep of the U249 round-1 head effff558. This run writes to `run-8` and leaves `run-4` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran. The deployed copy and the pin were compared over committed blobs (`git cat-file`, `cmp`, `shasum`).

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** Two runs are carried:
- **run-4** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-4`, source effff558) is the U249 round-1 sweep. Its five units are re-checked here: four as `prior_covered_changed_source` (`brief-check.py`, its copy and the pin changed), and one as `prior_covered_same_source` (the tests and the README).
- **run-7** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-7`, source 1d23154b) is the newest ledger and carries every other unit. Its six U227b units are absent at this head and carry as `prior_covered_changed_source`, out of scope; its other 32 units carry as `prior_out_of_scope`.

The brief calls run-3 the U249 head, but run-3 swept U240. No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. The checker is a deterministic gate that the coordinator runs over briefs the coordinator writes. No lower-trust principal supplies brief text, so the rule's limits are process limits, not boundary crossings.

**Can a crafted brief satisfy the rule without naming a gate?** Only by using a gate's wording. Each gate term is escaped and matched as a whole word in either class (`brief-check.py:267-278`, `:287`, `:414-423`), so partial or misspelled words do not count. But a sentence that merely mentions a gate (for example "no unittest run") satisfies it. The docstring states this limit: whether a gate ran is the pasted lines, read by the coordinator (`:35`).

**Can it crash the checker into an exit the levers misread?** No:
- the new functions index nothing that can be empty (`:378-388`, `:405-411`, `:414-423`);
- the patterns are fixed literal alternations;
- unreadable or ungrammatical briefs exit 2 (`:464-471`);
- exit 0 is reached only by an explicit return with no reasons (`:475`).

**The deployed copy's pin.** The source, the deployed copy, the manifest pin (`home/dot_agents/agent-config.yaml:894`) and the generated-outputs record (`scripts/generated-agent-outputs.json:403`) all carry sha256 `7be650074d4b159f9bd7e85a0a6e0515d0b35285b8b2d2dd8fc881f1bbc7af3c`. The self-check refuses any other bytes (`:79-121`).

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
- Explicit exemptions for absolute, home, parent and `$VAR` paths and for bare words, matching the sweep-brief shape. That is why this U264 brief itself needs no gate.
- Round 2's docstring fix removes a spelled temporary-directory path that the repository's portability guard refuses, without changing any rule.
- A byte-identical deployed copy, held to its sha256 pin by the script's own self-check.
- Tests cover every lint gate beside every test gate, each class alone, the sweep shape, and a missing ACCEPTANCE (`tests/unit/test_brief_check.py:478-531`).

## 7. Coverage summary

From `coverage-ledger.json` (43 units):

| Status | Units |
|---|---|
| covered | 5 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 38 |

The five covered units are run-4's U249 units, re-checked at this head, each owned by `parent-hunter` with source checks:
1. the ACCEPTANCE gate rule (business logic);
2. SCOPE repository-path detection (business logic);
3. exit codes on malformed briefs (wildcard);
4. the deployed copy and pin (generated-source provenance);
5. the tests and README (obvious things).

The 38 out-of-scope units are carried from run-7: its six U227b units, whose source is absent here, and its 32 other out-of-scope units. Among those 32 are the U254 timezone units: U254 is now in this head through the merged main, but it is outside the U249 change and was swept in run-6.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Neither was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
