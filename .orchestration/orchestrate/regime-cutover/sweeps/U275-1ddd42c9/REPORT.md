# Security audit report: dotfiles at 1ddd42c95107521f2ca8fabeda5b35cf9c410559

## 1. Run, scope and limits

**Candidate validation is incomplete.** One candidate survived the hunt, and no fresh independent verifier is available on this seat: the platform's delegation tool and eval kernel are denied by policy. Under the skill's rule the candidate stays an unvalidated ledger candidate. It is **not a finding**, and `findings.json` holds no record. `run-metadata.json` records `run_status: "incomplete"` with reason `candidate_validation_incomplete`.

| Fingerprint | Ledger unit | Record for a verifier |
|---|---|---|
| `dsh-seat/DSH_HOME-write-root/host-pnpm-install-outside-srt` | `scripts/orchestrator/hcom-seat#seat_write_roots-dsh` | `agents/parent-hunter/scratch/unvalidated-candidate.json` (schema-shaped `needs_validation`, validated with `validate-findings.cjs`) |

### 1a. The unvalidated candidate (not a finding)

**What it claims.** U272's `dsh` role contains the DeepSeek harness under srt. The write roots of that containment include all of `DSH_HOME` (`scripts/orchestrator/hcom-seat:1449`), and no write deny applies under it (`:1812-1836`). The contained session has a command tool, because the kit profile disables DSH's own `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9`).

Outside srt, the operator's `make update` first runs `chezmoi apply` (`Makefile:124`), which restores only the managed profile files. On its install path the updater then runs `(cd "${DSH_HOME}/profiles/thak" && mise exec -- pnpm install)` as the operator, with no `--ignore-pnpmfile` or `--ignore-scripts` (`scripts/update-agent-assets.sh:2102`).

So a `.pnpmfile.cjs` that the contained session plants in `~/.dsh/profiles/thak` survives into that install. pnpm loads such a file by default, so it would run as the operator **outside the sandbox** at the next harness install.

The lever's hazard account covers only the lever itself: tools planted under `DSH_HOME` are refused (`:814-818`), and `bin/dsh` never runs outside srt (`README.md:142`). The docs' "the dsh runtime is never executed outside srt" (`docs/deepseek-harness.md:30`) does not extend to code the runtime can write.

The harness trees `DSH_HOME/dsh/<tag>.*`, built outside srt (`update-agent-assets.sh:2093`), sit in the same writable root. That is a narrower race with a contained session running at the same time.

**Why it is not confirmed.** Three blockers remain:
1. pnpm's default `.pnpmfile.cjs` loading for the version mise provides is package-manager behaviour that is not visible in this repository.
2. Whether srt 0.0.81 lets the contained session create that file under its write root is sandbox behaviour that is not visible either.
3. No independent verifier has re-checked the trace.

No code ran here, by task rule.

**Local plan for a verifier.** Sandboxed, network off:
1. Make a fixture `DSH_HOME` whose `profiles/thak` holds a `.pnpmfile.cjs` that writes a marker. Run the updater's exact command with `--offline` and check for the marker.
2. Run `hcom-seat dsh --home <fixture> -- <a write of that file>` and check whether srt allows the write.

**Smallest fix.** Either change closes the path:
- narrow the `dsh` role's write roots to the runtime state DSH writes, or deny writes inside srt to `DSH_HOME/bin`, `DSH_HOME/dsh`, `DSH_HOME/profiles` and `DSH_HOME/plugins`;
- run the profile install with `--ignore-pnpmfile --ignore-scripts`, and refuse unmanaged files in `profiles/thak` before it.

### 1b. Scope and limits

**This is also a partial pass.** It is a scoped run.

**Profile and scope.** The profile is `standard`, with two readings of a brief that contradicts itself:
- **U272:** the head's own change, 8f31cf5c..1ddd42c9 (`scripts/orchestrator/hcom-seat`'s `dsh` role and its deployed copy, the pin, the generated-outputs record, the README, `docs/deepseek-harness.md` and two test modules). The brief's file name, branch and head commit name U272.
- **U227b:** the hunt list the brief's GOAL and CONTEXT name, re-checked at this head, where U227b is merged (#686).

The brief also names `d1ecd495` as the base and `c4195463..HEAD` (29 paths) as the change, and calls run-6 the U227b head; run-6 swept U254. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Output directory.** The brief names `run-8`, which holds the U264 sweep. This run writes to `run-11` and leaves `run-8` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Spent: zero delegated agents; reconnaissance, hunting and both critics ran in the parent.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran.

**Prior runs.**
- **run-9** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-9`, source 88d53ce1) supplies the seven U227b units, re-checked as same-source.
- **run-10** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-10`, source 87652899) is the newest ledger and is carried.

No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

Apart from the candidate above, the `dsh` role's rows hold:
- **Options and argv.** The role table refuses mixed options. The name and profile are regex-bound. `DSH_HOME` and `bin/dsh` are resolved physically, and arguments after `--` pass as argv (`hcom-seat:236-258`, `:298-301`, `:1707-1720`).
- **Environment.** Only the listed names reach the shim, under `env -i`. The caller's token is added at the launch alone, never printed (`:2001-2009`, `:2106-2108`).
- **Per-launch slots.** They are never reused, created under umask 077, and removed after dsh exits, with no link followed (`:1424-1429`, `:1789-1800`, `:2099-2111`).
- **Copy and pin.** One blob, sha256 `8f7f2024ea38949d1ebcb09047a6c84f0f8c9990c6de4d3b915c0927af61ac72` (`agent-config.yaml:861`, `scripts/generated-agent-outputs.json:432`).

The U227b hunt list (the rendered rows, the link step, no key or Ollama row, the U226 merge) holds at this head as in run-9: the files are unchanged apart from three pin lines.

## 3. Confirmed findings

None. The one candidate is unvalidated (section 1a) and is not a finding.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None as a final record. The candidate in section 1a would be a `needs_validation` record once an independent verifier re-checks it. Until then it is an unvalidated ledger candidate.

## 6. Hardening notes and positive patterns

### Hardening

1. **Merge ordering (carried from run-7 and run-9, now closed).** The note that the U227b profile depends on the U240 plugin no longer applies: both are merged (#679, #686).
2. **The sandbox holds the operator's login token** (carried pattern). The token enters the contained session's environment, as for every omp seat, behind the worker's read denies and domain list.

### Positive patterns

- One role table, so every difference from the worker seat sits in a few named rows.
- `DSH_HOME` among the protected roots before any tool resolves.
- `bin/dsh` resolved physically and never probed outside srt.
- Strict `env -i`.
- Per-launch slots that are never reused and are cleaned up.

## 7. Coverage summary

From `coverage-ledger.json` (54 units):

| Status | Units |
|---|---|
| covered | 11 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered:** four new U272 units, plus run-9's seven U227b units re-checked.
- **Candidate:** the write-root unit.
- **Out of scope:** run-10's units, including the five U244 units, which are merged and unchanged here.

**Critic results.** Neither the post-wave critic nor the final-clean critic accepted further work. Neither was an independent agent, so this is a single-reviewer coverage statement with one unvalidated candidate.
