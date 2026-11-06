# Security audit report: dotfiles at 50dd240c43f6984ffc9c8b9c6aafd09fda4bb2ba

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U254 change b49be338..50dd240c43f6984ffc9c8b9c6aafd09fda4bb2ba (branch `fix/server-timezone-step-on-a-runner`). That is one commit touching `install/ubuntu/server/setup_timezone.sh` and `tests/install/ubuntu/server/setup_timezone.bats`.

The brief names `d1ecd495` as the base and `c4195463..HEAD` (29 paths) as the change. The head's parent is b49be338 (main after U241), so I hunted the U254 commit alone, which matches the GOAL's two files. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Output directory.** The brief names `run-5`, which already held the U258 sweep of 2256b56c. This run writes to `run-6` and leaves `run-5` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran, and the bats test was read, not run (AGENTS.md Test Policy).

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.** I carried run-5 (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-5`, source 2256b56c, U240), the newest ledger. The brief names run-3, but run-5 already carries every unit of run-1 to run-4. U240 is absent at this head, so run-5's nine covered U240 units carry as `prior_covered_changed_source` and stay out of scope. No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. The step sets the server's timezone, which is configuration, not a security control, and no later step relies on it.

**Can a host be made to look like a runner and skip the zone?** Yes, by exporting `GITHUB_ACTIONS` (`setup_timezone.sh:36-39`). But that variable comes from the operator's own bootstrap environment, so only a principal that already controls that environment can set it. The only effect is that the zone stays as it was. The skip removes a privileged write and adds none.

**Can a crafted `/etc/localtime` target make the suffix test lie?** Yes: any resolved path that ends in `/Asia/Tokyo` passes (`:45`). But `/etc/localtime` is root-owned, so only a principal with the step's own authority can craft it, and the only effect of the lie is that the step leaves the link alone. When the step does write, it writes the fixed target `/usr/share/zoneinfo/Asia/Tokyo` at the fixed path `/etc/localtime` with `ln -snf` (`:51`), which replaces the link itself. No resolved path decides where the write lands.

**The sudo lines that remain** (`:51`, `:52`, `:54`) use only the literal `TZ`, assigned at `:34` (so the environment cannot set it), and other literals. `ln` now quotes its target.

**The test's fakes** define `sudo` and `readlink` as shell functions that log or print. No case reaches a real sudo or writes `/etc` (`setup_timezone.bats:12-23`).

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

1. **The idempotence check is incomplete.** The already-configured branch also skips the `tzdata` install (`setup_timezone.sh:45-48`, `:54`). `readlink -f` resolves a dangling link whose last component is missing, so a link naming `/usr/share/zoneinfo/Asia/Tokyo` on a host without `tzdata` reads as already set, and `tzdata` is never installed. `/etc/timezone` is never compared either. Testing that the resolved file exists, and that `/etc/timezone` holds the zone, would make the check complete.
2. **The runner signal is broad.** Any shell that exports `GITHUB_ACTIONS`, such as a local `act` run or a leftover variable, skips the step with only its one line (`:36-39`). Also checking `RUNNER_ENVIRONMENT=github-hosted` would narrow the signal to hosted runners.

### Positive patterns

- A privileged write removed on runners.
- An idempotent second run.
- A quoted `ln` target.
- `DEBIAN_FRONTEND` passed as a sudo argument, because `env_reset` would drop it.
- Tests that assert the exact sudo argv without running sudo.

## 7. Coverage summary

From `coverage-ledger.json` (37 units):

| Status | Units |
|---|---|
| covered | 4 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 33 |

The four covered units are all new, each owned by `parent-hunter` with source checks:
1. the `GITHUB_ACTIONS` skip (business logic);
2. `/etc/localtime` resolution (resource and file handling, local file ownership);
3. the remaining sudo lines (injection);
4. the test fakes and wiring (obvious things).

The 33 out-of-scope units are carried from run-5: its nine U240 units (changed source) and its 24 out-of-scope units.

**Critic results.** Neither the post-wave critic nor the final-clean critic found work. Neither was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
