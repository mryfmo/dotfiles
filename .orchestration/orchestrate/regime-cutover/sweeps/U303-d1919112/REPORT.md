# Security audit report: dotfiles at d191911256d88f4a71ebde559500353dbc4d1e19

## 1. Run, scope and limits

**Candidate validation is incomplete.** One candidate survived the hunt, the same one run-11 recorded at 1ddd42c9 and run-12 to run-15 carried. No fresh independent verifier is available on this seat: the platform's delegation tool and eval kernel are denied by policy. Under the skill's rule the candidate stays an unvalidated ledger candidate. It is **not a finding**, and `findings.json` holds no record. `run-metadata.json` records `run_status: "incomplete"` with reason `candidate_validation_incomplete`.

**What changed since run-15.** Run-15 swept this branch at d1ffd919 (U272e); run-16 swept another branch. The only commit since d1ffd919 is d1919112 (U272f, "hcom-seat judges the dsh role's rendered grants against its rendered denies"). It touches the lever, the deployed copy, the pin, `docs/deepseek-harness.md` and two test modules:
- **One judge over the rendered rows.** `settings_judge` (`hcom-seat:1824-1873`) replaces U272e's input list. It judges every rendered allowRead and allowWrite row against every rendered denyRead and denyWrite row, by physical path and identity, before anything is made (`:1984-1988`).
- **Tagged exemptions only.** A pair is exempt only when both rows carry the same structural tag and the grant lies where it is rendered (`:1863`). The tags are attached where the rows are rendered (`tag_rows`, `:1797-1809`; `:1719`, `:1728`, `:1753-1755`, `:1760-1764`).
- **The signal handler reads the removal's status.** It ends 2, naming a slot that remains (`:2359-2378`).
- **`physical_each` joins the producers' failure injection** (`tests/unit/test_hcom_seat.py`).

The updater, `Makefile`, the DSH profile and the README are byte-identical to d1ffd919, so the candidate stands at this head's lever lines (`hcom-seat:1493`, `:1720-1748`).

**Corrections to run-15.** The PR 697 round-4 audit (verdict U272e-d1ffd919) found two gaps that run-15 read and did not flag:
1. **A linked profile root was granted write.** Run-15 wrote that the fixed write roots `~/.omp/profiles/dsh` and `~/.omp/run` lay outside U272e's check, and called the first "by design". It did not see that a profile root linked to `~/.aws` re-opens what it links to, with allowWrite (P1 `:1835`). U272f's judge reads every rendered grant, so that root now refuses (test `test_hcom_seat_dsh.py:706`).
2. **The signal handler ignored the removal's status.** Run-15 recorded it as sound. But under `set -e` a failed removal ended the handler before the signal was restored, and the launch exited 1 with the slot behind (P2 `:2340`). U272f closes it (test `:828`).

The audit's third item, `physical_each` without failure injection (P2 `:1399`), is a test gap that run-15 did not raise either.

That makes eight gaps on this branch, plus this test gap, found by the PR's own audits and not by this seat's sweeps (three in run-14, three in run-15, two here). Read this run as an advisory second pass, not as clearance.

| Fingerprint | Ledger unit | Record for a verifier |
|---|---|---|
| `dsh-seat/DSH_HOME-write-root/host-pnpm-install-outside-srt` | `scripts/orchestrator/hcom-seat#seat_write_roots-dsh` | `agents/parent-hunter/scratch/unvalidated-candidate.json` (schema-shaped `needs_validation`, validated with `validate-findings.cjs`; line fields re-mapped to this head) |

### 1a. The unvalidated candidate (not a finding)

**What it claims.** U272's `dsh` role contains the DeepSeek harness under srt. The write roots of that containment include all of `DSH_HOME` (`scripts/orchestrator/hcom-seat:1493`). No write deny applies under it: the rendered write denies (`:1720-1748`, plus the deny row at `:1790`) all lie outside `DSH_HOME`, and U272f refuses any grant that overlaps a rendered deny. The contained session has a command tool, because the kit profile disables DSH's own `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9`).

Outside srt, the operator's `make update` first runs `chezmoi apply` (`Makefile:124`), which restores only the managed profile files. On its install path the updater then runs `(cd "${DSH_HOME}/profiles/thak" && mise exec -- pnpm install)` as the operator, with no `--ignore-pnpmfile` or `--ignore-scripts` (`scripts/update-agent-assets.sh:2102` on this branch; `:2151` on `main`, where U276b added `MISE_EXEC_AUTO_INSTALL=false`).

So a `.pnpmfile.cjs` that the contained session plants in `~/.dsh/profiles/thak` survives into that install. pnpm loads such a file by default, so it would run as the operator **outside the sandbox** at the next harness install.

The lever's hazard account covers only the lever itself:
- tools planted under `DSH_HOME` are refused (`hcom-seat:836-838`);
- `bin/dsh` never runs outside srt (`README.md:142`).

The docs' "the dsh runtime is never executed outside srt" (`docs/deepseek-harness.md:55`) does not extend to code the runtime can write.

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
- Narrow the `dsh` role's write roots to the runtime state DSH writes, or deny writes inside srt to `DSH_HOME/bin`, `DSH_HOME/dsh`, `DSH_HOME/profiles` and `DSH_HOME/plugins`. Under U272f such denies need their own structural tag paired with the `DSH_HOME` grant, or the judge refuses every launch (`DSH_HOME` would contain them).
- Run the profile install with `--ignore-pnpmfile --ignore-scripts`, and refuse unmanaged files in `profiles/thak` before it.

### 1b. Scope and limits

**This is also a partial pass.** It is a scoped run.

**Profile and scope.** The profile is `standard`, with the brief's two readings:
- **U272:** the head's own change, 8f31cf5c..d1919112, through U272b to U272f. The brief's branch and file name (`U303-…-u272f-head`) name U272; its GOAL and CONTEXT are the U227b template.
- **U227b:** the hunt list, re-checked at this head, where U227b is merged (#686). Its files are byte-identical to d1ffd919.

The brief names `d1ecd495` as the base and run-6 as the set to carry; run-6 swept U254. Every other top-level directory and the root files are `out_of_scope` units, and no coverage claim is made for them.

**Output directory.** The brief names `run-8`, which holds the U264 sweep. This run writes to `run-17` and leaves `run-8` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Spent: zero delegated agents; every phase ran in the parent.

**Execution.** Source only; no target code ran. Every lever unit's check text was rewritten with this head's line numbers, read from the file. This host's dsh grant roots were listed to confirm none is a link, so the judge admits the normal launch here.

**Prior runs.**
- **run-15** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-15`, source d1ffd919) is the last sweep of a U272 head. All of its 57 units are carried and re-checked:
  - seven covered units same-source;
  - the seven covered units that read the lever changed-source, rewritten with the corrections above;
  - the candidate, still a candidate;
  - 42 out of scope.
- run-16 swept U297 on another branch and is not carried here.

No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

Apart from the candidate above, the `dsh` role's rows hold at this head:
- **The judge (U272f).** Every rendered grant is judged against every rendered deny, by physical path and identity, before anything is made and in a dry run too (`hcom-seat:1824-1873`, `:1984-1988`). The exemptions are the tagged own-slot and own-profile pairs, and only while the grant is not a link elsewhere. The `.sandbox` deny is untagged. Tests: `test_hcom_seat_dsh.py:514`, `:604`, `:655`, `:706`, `:753`.
- **Deny row.** Every git, hcom and record path the lever computes is denied for read and for write by its physical path (`:1618-1679`, `:1787-1793`). The residuals are named (`docs/deepseek-harness.md:37-38`).
- **Read grants.** U272c's row is unchanged (`:1791-1792`). On this host none of its roots is a link.
- **Options and argv.** The role table refuses mixed options. The name and profile are regex-bound. `DSH_HOME` and `bin/dsh` are resolved physically, and arguments after `--` pass as argv (`:257-278`, `:318-321`, `:1968-1972`, `:2030-2031`).
- **Environment.** Only the listed names reach the shim, under `env -i`. The caller's token is added at the launch alone and never printed (`:2246-2254`, `:2399-2401`).
- **Per-launch slots.** They are never reused (`:1469-1473`) and are created under umask 077 (`:2093-2103`). They are removed with modes reset and no link followed. A slot that remains ends the launch 2, on the normal exit and now under a signal too (`:2336-2410`).
- **Copy and pin.** One blob, `a2c84c40`, sha256 `0480fbd3d8aaecbf574113ee9563f526399c5909b6047eeaa5d806511cd85fe5` (`agent-config.yaml:861`, `scripts/generated-agent-outputs.json:432`).
- **The omp roles' settings** are byte-identical to the four earlier heads (test `:249`).

The U227b hunt list holds at this head as in run-9 to run-15.

## 3. Confirmed findings

None. The one candidate is unvalidated (section 1a) and is not a finding.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None as a final record. The candidate in section 1a would be a `needs_validation` record once an independent verifier re-checks it.

## 6. Hardening notes and positive patterns

### Hardening

1. **The dsh session keeps the worker's GitHub reach** (carried; deny-row unit). `~/.config/gh` is in no deny, and the domain list keeps `github.com` and `api.github.com` (`hcom-seat:2116-2119`), with the HTTPS push URL the shim sets (`:2127-2138`, `:2203-2205`). Wherever the gh token is readable inside srt, the unsigned preview harness gets the operator's GitHub write access. If the `dsh` role needs no push, deny `~/.config/gh` and drop the GitHub write domains. Not verified: the token's storage is a credential store this run may not read.
2. **`~/.omp/run` is shared with every other omp session** (new; per-launch slots unit). It is a `dsh` write root (`:1493`). It holds the omp session-owner locks and daemon records (`session-owners/`, `daemons/`) that the operator's own omp and the other seats read outside the dsh sandbox. A contained dsh session can delete or rewrite them. With no unix socket and no local binding it cannot stand in for a daemon, so the reach is denial of service or lock confusion; not verified. If the login child needs no shared lease, a per-role run directory or a `dsh` row without `~/.omp/run` would keep the session off the other seats' state.
3. **Cleanup while a sandboxed process may still run** (carried). A background process that outlives dsh could race the operator's `chmod -R` and `rm -rf` walk of the state slot. Renaming the slot out of the write root before removal would close that window; not verified on srt 0.0.81.
4. **Slots after a refusal** (carried). A `refuse()` inside `seat_sandbox_write` after the slots are made (the settings write `:2124-2126`, the shim install `:2211-2213`) still exits without `slots_remove`. This is hygiene only.
5. **The sandbox holds the operator's login token** (carried pattern, `:2186-2194`).

### Positive patterns

- One judge over the rendered settings, with no separate list of inputs that can lack a member.
- Exemptions declared where the rows are rendered, and void when a link moves the grant.
- Containment stated as denies by physical path, with the residuals named in the docs.
- Fail-closed producers and a fail-closed slot removal, on every exit path but `refuse()`.

## 7. Coverage summary

From `coverage-ledger.json` (57 units):

| Status | Units |
|---|---|
| covered | 14 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered:** run-15's fourteen covered units, all re-checked at this head. The seven that read the lever are changed-source and carry the corrections above; the write-root refusal unit now describes U272f's judge.
- **Candidate:** the write-root unit.
- **Out of scope:** run-15's out-of-scope units.

**Critic results.** Neither the post-wave critic nor the final-clean critic accepted further work. Neither was an independent agent. This is a single-reviewer coverage statement with one unvalidated candidate, and the PR's own audits have found eight gaps on this branch, and one test gap, that this seat missed.
