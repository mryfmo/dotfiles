# Security audit report: dotfiles at 5b950a97028205f7430a7c9f36f74b91a79e88c8

## 1. Run, scope and limits

**Candidate validation is incomplete.** One candidate survived the hunt, the same one run-11 recorded at 1ddd42c9 and run-12 and run-13 carried. No fresh independent verifier is available on this seat: the platform's delegation tool and eval kernel are denied by policy. Under the skill's rule the candidate stays an unvalidated ledger candidate. It is **not a finding**, and `findings.json` holds no record. `run-metadata.json` records `run_status: "incomplete"` with reason `candidate_validation_incomplete`.

**What changed since run-13.** The only commit since run-13's head 976fd6cd is 5b950a97 (U272d, "hcom-seat states the dsh role's containment as denies by physical path"). It touches the lever, the deployed copy, the pin, `docs/deepseek-harness.md` and `tests/unit/test_hcom_seat_dsh.py`, and adds four things:
- **The deny row** `dsh_deny_paths` (`hcom-seat:1592-1650`). It lists the physical paths of the checkout's git directory and git common directory, every linked worktree's `.git`, the hcom store and every existing `~/.local/state/hcom-*` store, `<checkout>/.orchestration` and every other seat's directory. All of them go into denyRead and denyWrite (`:1972-1975`).
- **The `DSH_HOME` refusal** `dsh_home_check` (`:1652-1666`). It runs by identity before the overlap check and before anything is made (`:1758-1767`).
- **The signal trap.** It covers HUP, INT and TERM, and the normal exit runs the same removal (`slots_remove`, `foreground_signal`, `:2211-2235`).
- **The clock producer** `utc_stamp` (`:208-216`).

The updater, `Makefile` and the DSH profile are byte-identical, so the candidate stands at the re-mapped lever lines `hcom-seat:1467` and `:1913-1937`.

**Corrections to run-11, run-12 and run-13.** The PR 697 round-2 audit found three gaps at 976fd6cd that my earlier sweeps of this branch did not:
1. **Run-13 said U272c "closes" the dsh session's reads of the bus store and the records. That was wrong.** srt's read policy is deny-then-allow over an explicit list, and everything the list does not name is readable. So removing the `dsh` role's grants denied nothing. The worker's deny names `~/.local/state/hcom` only (`hcom-seat:1939-1942`), so this host's program store `~/.local/state/hcom-regime` stayed readable from inside the dsh sandbox. A git common directory outside `~/Workspace` and the records would have been readable too. U272d's deny row closes this.
2. **`DSH_HOME=<checkout>/.git` was admitted.** It passed the overlap check's exemption for the omp roles' own `.git` and became an allowRead and allowWrite root, so the session could have altered objects and refs. Run-11 to run-13 recorded "a DSH_HOME inside a protected path is refused by the overlap invariant" without seeing the exemption. U272d's `dsh_home_check` closes it.
3. **A SIGHUP to the launch's process group left both per-launch slots behind.** Run-11 to run-13 covered only the normal exit. U272d's trap closes it.

This run checks each fix at this head (section 2 and the ledger).

| Fingerprint | Ledger unit | Record for a verifier |
|---|---|---|
| `dsh-seat/DSH_HOME-write-root/host-pnpm-install-outside-srt` | `scripts/orchestrator/hcom-seat#seat_write_roots-dsh` | `agents/parent-hunter/scratch/unvalidated-candidate.json` (schema-shaped `needs_validation`, validated with `validate-findings.cjs`; line fields re-mapped to this head) |

### 1a. The unvalidated candidate (not a finding)

**What it claims.** U272's `dsh` role contains the DeepSeek harness under srt. The write roots of that containment include all of `DSH_HOME` (`scripts/orchestrator/hcom-seat:1467`). No write deny applies under it (`:1913-1937`): U272d's deny row adds write denies only for paths outside `DSH_HOME`, and refuses a `DSH_HOME` that holds one. The contained session has a command tool, because the kit profile disables DSH's own `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9`).

Outside srt, the operator's `make update` first runs `chezmoi apply` (`Makefile:124`), which restores only the managed profile files. On its install path the updater then runs `(cd "${DSH_HOME}/profiles/thak" && mise exec -- pnpm install)` as the operator, with no `--ignore-pnpmfile` or `--ignore-scripts` (`scripts/update-agent-assets.sh:2102`).

So a `.pnpmfile.cjs` that the contained session plants in `~/.dsh/profiles/thak` survives into that install. pnpm loads such a file by default, so it would run as the operator **outside the sandbox** at the next harness install.

The lever's hazard account covers only the lever itself:
- tools planted under `DSH_HOME` are refused (`hcom-seat:832-836`);
- `bin/dsh` never runs outside srt (`README.md:142`).

The docs' "the dsh runtime is never executed outside srt" (`docs/deepseek-harness.md:47`) does not extend to code the runtime can write.

The harness trees `DSH_HOME/dsh/<tag>.*`, built outside srt (`update-agent-assets.sh:2093`), sit in the same writable root. Reaching them needs a narrower race with a contained session that is running at the same time.

**Why it is not confirmed.** Three blockers remain:
1. pnpm's default `.pnpmfile.cjs` loading for the version mise provides is package-manager behaviour that is not visible in this repository.
2. Whether srt 0.0.81 lets the contained session create that file under its write root is sandbox behaviour that is not visible either.
3. No independent verifier has re-checked the trace.

No code ran here, by task rule.

**Local plan for a verifier.** Sandboxed, network off:
1. Make a fixture `DSH_HOME` whose `profiles/thak` holds a `.pnpmfile.cjs` that writes a marker. Run the updater's exact command with `--offline` and check for the marker.
2. Run `hcom-seat dsh --home <fixture> -- <a write of that file>` and check whether srt allows the write.

**Smallest fix.** Either change closes the path:
- narrow the `dsh` role's write roots to the runtime state DSH writes, or deny writes inside srt to `DSH_HOME/bin`, `DSH_HOME/dsh`, `DSH_HOME/profiles` and `DSH_HOME/plugins`. U272d's deny row is the natural place for those rows;
- run the profile install with `--ignore-pnpmfile --ignore-scripts`, and refuse unmanaged files in `profiles/thak` before it.

### 1b. Scope and limits

**This is also a partial pass.** It is a scoped run.

**Profile and scope.** The profile is `standard`, with two readings of a brief that contradicts itself, as U275's, U279's and U286's did:
- **U272:** the head's own change, 8f31cf5c..5b950a97. That is `scripts/orchestrator/hcom-seat`'s `dsh` role and its deployed copy, the pin, the generated-outputs record, the README, `docs/deepseek-harness.md` and two test modules, through U272b, U272c and U272d. The brief's branch and file name (`U292-…-u272d-head`) name U272.
- **U227b:** the hunt list the brief's GOAL and CONTEXT name, re-checked at this head, where U227b is merged (#686).

The brief also names `d1ecd495` as the base and `c4195463..HEAD` (29 paths) as the change, and calls run-6 the U227b head; run-6 swept U254. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Output directory.** The brief names `run-8`, which holds the U264 sweep. This run writes to `run-14` and leaves `run-8` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Spent: zero delegated agents; reconnaissance, hunting and both critics ran in the parent.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran. Line numbers for the carried units come from a `git diff -U0 976fd6cd HEAD` map and were spot-checked against the file (`agents/parent-hunter/scratch/linemap.cjs`).

**Prior runs.**
- **run-13** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-13`, source 976fd6cd) is the sweep of the previous U272 head. All of its 55 units are carried and re-checked here: seven covered units same-source, the five covered units that read the lever changed-source with their texts rewritten at this head's lines, the candidate still a candidate, and 42 out of scope. One new unit covers U272d's deny row.

Its own priors (run-12, run-11, run-9's U227b units, run-10's ledger) come with it. No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

Apart from the candidate above, the `dsh` role's rows hold at this head:
- **Deny row (U272d).** Every git, hcom and record path the lever computes is denied for read and for write by its physical path (`hcom-seat:1592-1650`, `:1972-1975`). `~/.local/state/hcom-regime` is now named. The lever's own `~/.local/state/hcom-seat` is excepted by identity, and on this host it holds only `tools/`. The paths must be clean (`:1647-1649`). Two residuals are named by the PR and the docs (`docs/deepseek-harness.md:29-30`): git directories the lever does not compute, and an `hcom-*` store created after the launch began, are not denied.
- **`DSH_HOME` refusal (U272d).** A `DSH_HOME` that is, contains or lies inside a denied path refuses by identity before the overlap check and before any mkdir, in a dry run too (`:1652-1666`, `:1758-1767`; test `test_hcom_seat_dsh.py:506`).
- **Read grants.** U272c's `allowRead` row is unchanged (`:1976-1977`), and none of its entries is, or is an ancestor of, a denied path.
- **Options and argv.** The role table refuses mixed options. The name and profile are regex-bound. `DSH_HOME` and `bin/dsh` are resolved physically, and arguments after `--` pass as argv (`:255-276`, `:316-319`, `:1763-1764`, `:1816-1817`).
- **Environment.** Only the listed names reach the shim, under `env -i`. The caller's token is added at the launch alone and never printed (`:2121-2129`, `:2249-2251`).
- **Per-launch slots.** They are never reused (`:1442-1447`) and are created under umask 077 (`:1890-1901`). Both the normal exit and the HUP/INT/TERM trap remove them, and the trap is installed before they are made and ends the lever by the same signal (`:2211-2236`, `:2252-2254`; test `:542`). The stamp comes from `utc_stamp`, which reads `/bin/date`'s status first and holds the result to its shape (`:208-216`; test `:557`).
- **Copy and pin.** One blob, `52f7e018`, sha256 `3c6efffdd1ab21dd0e92f89d6e44ce30b08b3b8d2fe8c9b60f4f6e31e36f3f8e` (`agent-config.yaml:861`, `scripts/generated-agent-outputs.json:432`).
- **The omp roles' settings** are byte-identical to both earlier heads (test `:241`), and their rows (`:1962-1971`) are untouched.

The U227b hunt list (the rendered rows, the link step, no key or Ollama row, the U226 merge) holds at this head as in run-9: its files are unchanged apart from the lever-pin lines.

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

1. **The dsh session keeps the worker's GitHub reach** (new; deny-row unit). srt's read policy is a deny list, so the dsh session reads everything in `~` that no deny names, and `~/.config/gh`, the GitHub credential path the gh helper uses, is in no deny. The domain list also keeps `github.com` and `api.github.com` (`hcom-seat:1991-1994`), and the shim sets an HTTPS push URL (`:2002-2013`, `:2078-2080`). So wherever the gh token is readable inside srt, the unsigned developer-preview harness gets the operator's GitHub write access, as a worker seat has by design. If the `dsh` role needs no push, deny `~/.config/gh` in its deny row and drop the GitHub write domains from its row. This is not verified: where the token is stored on this host is a credential store this run may not read.
2. **Slots after a refusal** (new; per-launch slots unit). `slots_remove` runs on the normal exit and on the three signals, but not on a `refuse()` inside `seat_sandbox_write` after the slots are made (for example `git_state_check`, `:1923`, or the settings write). The leftovers are empty, mode 0700 and never reused, so this is hygiene only.
3. **The sandbox holds the operator's login token** (carried pattern). The token enters the contained session's environment, as for every omp seat, behind the read denies and domain list (`:2061-2069`).

### Positive patterns

- One role table, so every difference from the worker seat sits in a few named rows.
- Containment stated as denies by physical path, matching how srt actually reads its policy, with the residual named in the docs.
- `DSH_HOME` checked by identity against every denied path before anything is made.
- `bin/dsh` resolved physically and never probed outside srt.
- Strict `env -i`.
- Per-launch slots that are never reused and are removed on exit and on hangup, interrupt or termination.
- A checked clock producer with failure-injection tests.

## 7. Coverage summary

From `coverage-ledger.json` (56 units):

| Status | Units |
|---|---|
| covered | 13 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered:** run-13's twelve covered units, all re-checked at this head (the five that read the lever are changed-source and carry the corrections above), and the new U272d deny-row unit.
- **Candidate:** the write-root unit.
- **Out of scope:** run-13's out-of-scope units, including the five U244 units, which are merged and unchanged here.

**Critic results.** Neither the post-wave critic nor the final-clean critic accepted further work. Neither was an independent agent, so this is a single-reviewer coverage statement with one unvalidated candidate, and the three corrections above show what a single reviewer missed on this branch.
