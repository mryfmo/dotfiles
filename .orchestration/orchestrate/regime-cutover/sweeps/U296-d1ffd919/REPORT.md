# Security audit report: dotfiles at d1ffd91939e4d069b01d0e4d467c12eff971a944

## 1. Run, scope and limits

**Candidate validation is incomplete.** One candidate survived the hunt, the same one run-11 recorded at 1ddd42c9 and run-12 to run-14 carried. No fresh independent verifier is available on this seat: the platform's delegation tool and eval kernel are denied by policy. Under the skill's rule the candidate stays an unvalidated ledger candidate. It is **not a finding**, and `findings.json` holds no record. `run-metadata.json` records `run_status: "incomplete"` with reason `candidate_validation_incomplete`.

**What changed since run-14.** The only commit since run-14's head 5b950a97 is d1ffd919 (U272e, "hcom-seat derives the dsh role's write-root refusal from the rendered deny table"). It touches the lever, the deployed copy, the pin, `docs/deepseek-harness.md` and `tests/unit/test_hcom_seat_dsh.py`:
- **One producer for the settings lists.** `seat_settings_render` (`hcom-seat:1681-1788`) renders them, and for the `dsh` role it runs before anything is made, in a dry run too (`:1958-1961`). `seat_sandbox_write` only writes them out.
- **The write-root refusal reads that table.** `dsh_write_roots_check` (`:1822-1848`) refuses a `DSH_HOME`, state slot or scratch cwd that is, contains or lies inside any final denyRead or denyWrite path. The inherited worker denies are included. Every deny path is resolved by `physical_each` (`:1388-1410`) and the decision is by identity (`write_root_outside_denies`, `:1790-1820`). This replaces U272d's `dsh_home_check`.
- **The records row is physical** (`:1661-1664`).
- **`slots_remove` resets owner modes before `rm -rf` and fails closed** (`:2309-2331`). A slot that remains ends the launch 2, whatever dsh returned (`:2367-2373`).

The updater, `Makefile`, the DSH profile and the README are byte-identical, so the candidate stands at this head's lever lines (`hcom-seat:1493`, `:1715-1744`).

**Corrections to run-14.** The PR 697 round-3 audit (verdict U272d-5b950a97) found three gaps at run-14's head that run-14 did not:
1. **`DSH_HOME=~/.aws` or `~/.omp/agent` was accepted.** These are deny paths the `dsh` role inherits from the worker, and srt re-opens an allowed path under a deny of the same or a wider spelling. Run-14's deny-row unit checked `DSH_HOME` against the role's own row only. U272e's refusal now reads the whole rendered table.
2. **The records row was not physical.** A `.orchestration` that is a link into `DSH_HOME` hid its ancestry from the identity check. U272e resolves it.
3. **A mode-000 directory that dsh left kept `rm -rf` out of the state slot** while the launch still exited 0. Run-14 covered only the signal path. U272e resets the modes first and fails closed.

These follow the three gaps run-14 corrected in run-11 to run-13. Six of the gaps on this branch were found by the PR's own audits and not by this seat's single-reviewer sweeps. Section 7 says so again.

| Fingerprint | Ledger unit | Record for a verifier |
|---|---|---|
| `dsh-seat/DSH_HOME-write-root/host-pnpm-install-outside-srt` | `scripts/orchestrator/hcom-seat#seat_write_roots-dsh` | `agents/parent-hunter/scratch/unvalidated-candidate.json` (schema-shaped `needs_validation`, validated with `validate-findings.cjs`; line fields re-mapped to this head) |

### 1a. The unvalidated candidate (not a finding)

**What it claims.** U272's `dsh` role contains the DeepSeek harness under srt. The write roots of that containment include all of `DSH_HOME` (`scripts/orchestrator/hcom-seat:1493`). No write deny applies under it: the rendered write denies (`:1715-1744`, plus the deny row at `:1783`) all lie outside `DSH_HOME`, and U272e refuses a `DSH_HOME` that overlaps one. The contained session has a command tool, because the kit profile disables DSH's own `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9`).

Outside srt, the operator's `make update` first runs `chezmoi apply` (`Makefile:124`), which restores only the managed profile files. On its install path the updater then runs `(cd "${DSH_HOME}/profiles/thak" && mise exec -- pnpm install)` as the operator, with no `--ignore-pnpmfile` or `--ignore-scripts` (`scripts/update-agent-assets.sh:2102`).

So a `.pnpmfile.cjs` that the contained session plants in `~/.dsh/profiles/thak` survives into that install. pnpm loads such a file by default, so it would run as the operator **outside the sandbox** at the next harness install.

The lever's hazard account covers only the lever itself:
- tools planted under `DSH_HOME` are refused (`hcom-seat:836-838`);
- `bin/dsh` never runs outside srt (`README.md:142`).

The docs' "the dsh runtime is never executed outside srt" (`docs/deepseek-harness.md:52`) does not extend to code the runtime can write.

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
- narrow the `dsh` role's write roots to the runtime state DSH writes, or deny writes inside srt to `DSH_HOME/bin`, `DSH_HOME/dsh`, `DSH_HOME/profiles` and `DSH_HOME/plugins`. `seat_settings_render`'s dsh row is the natural place for those rows; note that U272e's refusal would then need those rows in `slot_rows`, or an equivalent exemption for `DSH_HOME`;
- run the profile install with `--ignore-pnpmfile --ignore-scripts`, and refuse unmanaged files in `profiles/thak` before it.

### 1b. Scope and limits

**This is also a partial pass.** It is a scoped run.

**Profile and scope.** The profile is `standard`, with two readings of a brief that contradicts itself, as the four before it did:
- **U272:** the head's own change, 8f31cf5c..d1ffd919. That is `scripts/orchestrator/hcom-seat`'s `dsh` role and its deployed copy, the pin, the generated-outputs record, the README, `docs/deepseek-harness.md` and two test modules, through U272b to U272e. The brief's branch and file name (`U296-…-u272e-head`) name U272.
- **U227b:** the hunt list the brief's GOAL and CONTEXT name, re-checked at this head, where U227b is merged (#686).

The brief also names `d1ecd495` as the base and `c4195463..HEAD` (29 paths) as the change, and calls run-6 the U227b head; run-6 swept U254. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Output directory.** The brief names `run-8`, which holds the U264 sweep. This run writes to `run-15` and leaves `run-8` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Spent: zero delegated agents; reconnaissance, hunting and both critics ran in the parent.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran. Every lever unit's check text was rewritten with this head's line numbers, read from the file.

**Prior runs.**
- **run-14** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-14`, source 5b950a97) is the sweep of the previous U272 head. All of its 56 units are carried and re-checked here: seven covered units same-source, the six covered units that read the lever changed-source (rewritten, with the corrections above), the candidate still a candidate, and 42 out of scope. One new unit covers U272e's write-root refusal.

Its own priors (run-13, run-12, run-11, run-9's U227b units, run-10's ledger) come with it. No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

Apart from the candidate above, the `dsh` role's rows hold at this head:
- **Write-root refusal (U272e).** `DSH_HOME`, the state slot and the scratch cwd are each checked against every rendered deny path, the inherited ones included, by physical path and identity, before anything is made and in a dry run too (`hcom-seat:1790-1848`, `:1958-1961`; tests `test_hcom_seat_dsh.py:512`, `:602`, `:653`). The slot's and cwd's own rows (`slot_rows`, `:1724`, `:1752-1757`) are exempt by exact rendered spelling, so an omission refuses and never admits. `physical_each` fails closed per record (`:1388-1410`).
- **Deny row.** Every git, hcom and record path the lever computes is denied for read and for write by its physical path, the records row included (`:1618-1679`, `:1780-1786`). The residuals are named (`docs/deepseek-harness.md:34-35`).
- **Read grants.** U272c's `allowRead` row is unchanged (`:1784-1785`).
- **Options and argv.** The role table refuses mixed options. The name and profile are regex-bound. `DSH_HOME` and `bin/dsh` are resolved physically, and arguments after `--` pass as argv (`:257-278`, `:318-321`, `:1943-1947`, `:2003-2004`).
- **Environment.** Only the listed names reach the shim, under `env -i`. The caller's token is added at the launch alone and never printed (`:2219-2227`, `:2364-2366`).
- **Per-launch slots.** They are never reused (`:1469-1473`) and are created under umask 077 (`:2066-2076`). They are removed on exit and on HUP, INT and TERM with modes reset, and no link is followed. A slot that remains fails the launch (`:2309-2373`; tests `:551`, `:681`). The stamp comes from `utc_stamp` (`:210-218`; test `:566`).
- **Copy and pin.** One blob, `de22c7eb`, sha256 `e2e9bc0c6af7c8fde2d05952b25798c49a956b12ab8c5158d89beb7d15cae56a` (`agent-config.yaml:861`, `scripts/generated-agent-outputs.json:432`).
- **The omp roles' settings** are byte-identical to 52873a37, 976fd6cd and 5b950a97 (test `:247`). They now come from the same renderer, at `:2350`.

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

1. **The dsh session keeps the worker's GitHub reach** (carried from run-14; deny-row unit). srt's read policy is a deny list, so the dsh session reads everything in `~` that no deny names, and `~/.config/gh`, the GitHub credential path the gh helper uses, is in no deny. The domain list also keeps `github.com` and `api.github.com` (`hcom-seat:2089-2092`), and the shim sets an HTTPS push URL (`:2100-2111`, `:2176-2178`). So wherever the gh token is readable inside srt, the unsigned developer-preview harness gets the operator's GitHub write access, as a worker seat has by design. U272e does not change this. If the `dsh` role needs no push, deny `~/.config/gh` in its row and drop the GitHub write domains. This is not verified: where the token is stored on this host is a credential store this run may not read.
2. **Cleanup while a sandboxed process may still run** (new; per-launch slots unit). `slots_remove` runs once the foreground child has ended. But a process the session started in the background may outlive dsh, if srt does not end the sandbox's process tree; that is not verified on srt 0.0.81. Such a process keeps write access to the state slot and could race the operator's `chmod -R` and `rm -rf` walk, for example by swapping a directory for a link mid-walk. Renaming the slot out of the write root first (into the write-denied `.sandbox`, for instance) and removing it there would close that window.
3. **Slots after a refusal** (carried from run-14). A `refuse()` inside `seat_sandbox_write` after the slots are made (the settings, shim and wrapper writes) still exits without `slots_remove`. The leftovers are empty, mode 0700 and never reused, so this is hygiene only.
4. **The sandbox holds the operator's login token** (carried pattern). The token enters the contained session's environment, as for every omp seat, behind the read denies and domain list (`:2159-2167`).

### Positive patterns

- One renderer for the settings lists, read both by the refusal and by the settings file, so the two cannot drift.
- Containment stated as denies by physical path, matching how srt actually reads its policy, with the residuals named in the docs.
- Input-derived write roots checked by identity against every deny path before anything is made.
- Fail-closed producers (`physical_each`, `utc_stamp`) and a fail-closed slot removal.
- `bin/dsh` resolved physically and never probed outside srt.
- Strict `env -i`.

## 7. Coverage summary

From `coverage-ledger.json` (57 units):

| Status | Units |
|---|---|
| covered | 14 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered:** run-14's thirteen covered units, all re-checked at this head (the six that read the lever are changed-source and carry the corrections above), and the new U272e write-root refusal unit.
- **Candidate:** the write-root unit.
- **Out of scope:** run-14's out-of-scope units, including the five U244 units, which are merged and unchanged here.

**Critic results.** Neither the post-wave critic nor the final-clean critic accepted further work. Neither was an independent agent. This is a single-reviewer coverage statement with one unvalidated candidate, and across run-11 to run-14 the PR's own audits found six gaps this seat missed. Read it as an advisory second pass, not as clearance.
