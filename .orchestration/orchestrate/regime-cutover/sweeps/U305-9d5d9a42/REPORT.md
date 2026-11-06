# Security audit report: dotfiles at 9d5d9a42ec4e8c485d1a5dda29e96c7b2c4f3213

## 1. Run, scope and limits

**Candidate validation is incomplete.** One candidate survived the hunt, the same one run-11 recorded at 1ddd42c9 and run-12 to run-17 carried. No fresh independent verifier is available on this seat: the platform's delegation tool and eval kernel are denied by policy. Under the skill's rule the candidate stays an unvalidated ledger candidate. It is **not a finding**, and `findings.json` holds no record. `run-metadata.json` records `run_status: "incomplete"` with reason `candidate_validation_incomplete`.

**What changed since run-17.** The only commit since run-17's head d1919112 is 9d5d9a42 (U272g, "hcom-seat keys each exemption to one rendered row by position and reads slot existence through a checked stat"). It touches the lever, the deployed copy, the pin and `tests/unit/test_hcom_seat_dsh.py`; the docs page and the README are unchanged.
- **Position-keyed tags.** A structural tag now names one rendered row by its list and position, and applies only while the row there is byte-equal to the path the lever rendered (`tag_row` and `row_tag`, `hcom-seat:1810-1841`; set at `:1725-1728`, `:1754`, `:1761-1769`, `:1801-1805`). `DSH_HOME` (row 2) and `~/.omp/run` (write row 4) carry no tag whatever they are spelled.
- **Checked existence reads.** `slots_remove` reads each slot through `path_presence`, one `/usr/bin/stat` without `-L` whose status and message are read (`:2357-2402`). A failure other than "No such file or directory" refuses, naming the slot.

The updater, `Makefile` and the DSH profile are byte-identical to run-17's head, so the candidate stands at this head's lever lines (`hcom-seat:1494`, `:1720-1749`).

**Corrections to run-17.** The PR 697 round-5 audit (verdict U272f-d1919112) found two gaps at run-17's head that run-17 did not:
1. **Tags keyed by spelling widened the exemption.** Run-17 checked that only the own profile carried the `profile` tag and concluded the exemption could not widen. But tags were keyed by rendered spelling. So `DSH_HOME=~/.omp/profiles`, or a `~/.omp/run` linked there, was rendered in the tagged spelling, inherited the own-profile exemption and **put the whole profiles directory into allowWrite** (P1 `:1863`). U272g's position-keyed tags close it (test `test_hcom_seat_dsh.py:871`).
2. **An unsearchable `.state` hid a slot that remained.** A `.state` of mode 000 made `[[ -e ]]` and `[[ -L ]]` read the slot as absent, so the launch exited 0 with the slot behind (P2 `:2347`). `path_presence` closes it (test `:932`).

That makes ten gaps on this branch, plus one test gap, found by the PR's own audits and not by this seat's sweeps: three in run-14, three in run-15, two in run-17 and two here. Read this run as an advisory second pass, not as clearance.

**New at this head (hardening note 1).** `path_presence` treats a path as absent only when the stat error text is the English "No such file or directory", and the lever does not pin the locale for that stat. On a host whose stat messages are translated, the absent slot after a good removal would refuse, so every dsh launch would end 2. It fails closed, so this is an availability defect, not a widening. It is not verified on Linux.

| Fingerprint | Ledger unit | Record for a verifier |
|---|---|---|
| `dsh-seat/DSH_HOME-write-root/host-pnpm-install-outside-srt` | `scripts/orchestrator/hcom-seat#seat_write_roots-dsh` | `agents/parent-hunter/scratch/unvalidated-candidate.json` (schema-shaped `needs_validation`, validated with `validate-findings.cjs`; line fields re-mapped to this head) |

### 1a. The unvalidated candidate (not a finding)

**What it claims.** U272's `dsh` role contains the DeepSeek harness under srt. The write roots of that containment include all of `DSH_HOME` (`scripts/orchestrator/hcom-seat:1494`). No write deny applies under it: the rendered write denies (`:1720-1749`, plus the deny row at `:1794`) all lie outside `DSH_HOME`, and the judge refuses any grant that overlaps a rendered deny. The contained session has a command tool, because the kit profile disables DSH's own `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9`).

Outside srt, the operator's `make update` first runs `chezmoi apply` (`Makefile:124`), which restores only the managed profile files. On its install path the updater then runs `(cd "${DSH_HOME}/profiles/thak" && mise exec -- pnpm install)` as the operator, with no `--ignore-pnpmfile` or `--ignore-scripts` (`scripts/update-agent-assets.sh:2102` on this branch; `:2151` on `main`).

So a `.pnpmfile.cjs` that the contained session plants in `~/.dsh/profiles/thak` survives into that install. pnpm loads such a file by default, so it would run as the operator **outside the sandbox** at the next harness install.

The lever's hazard account covers only the lever itself:
- tools planted under `DSH_HOME` are refused (`hcom-seat:837-839`);
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
- Narrow the `dsh` role's write roots to the runtime state DSH writes, or deny writes inside srt to `DSH_HOME/bin`, `DSH_HOME/dsh`, `DSH_HOME/profiles` and `DSH_HOME/plugins`. Under the judge, such denies need a tag of their own (`tag_row`) paired with `DSH_HOME`'s grant row, or every launch refuses, because `DSH_HOME` would contain them.
- Run the profile install with `--ignore-pnpmfile --ignore-scripts`, and refuse unmanaged files in `profiles/thak` before it.

### 1b. Scope and limits

**This is also a partial pass.** It is a scoped run.

**Profile and scope.** The profile is `standard`, with the brief's two readings:
- **U272:** the head's own change, 8f31cf5c..9d5d9a42, through U272b to U272g. The brief's branch and file name (`U305-…-u272g-head`) name U272; its GOAL and CONTEXT are the U227b template.
- **U227b:** the hunt list, re-checked at this head, where U227b is merged (#686). Its files are byte-identical to d1919112.

The brief names `d1ecd495` as the base and run-6 as the set to carry; run-6 swept U254. Every other top-level directory and the root files are `out_of_scope` units, and no coverage claim is made for them.

**Output directory.** The brief names `run-8`, which holds the U264 sweep. This run writes to `run-18` and leaves `run-8` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Spent: zero delegated agents; every phase ran in the parent.

**Execution.** Source only; no target code ran. Every lever unit's check text was rewritten with this head's line numbers, read from the file. The lever blob was hashed by its object id.

**Prior runs.**
- **run-17** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-17`, source d1919112) is the previous U272 head's sweep. All of its 57 units are carried and re-checked:
  - seven covered units same-source;
  - the seven covered units that read the lever changed-source, rewritten with the corrections above;
  - the candidate, still a candidate;
  - 42 out of scope.

Its own priors (run-15 back to run-9, and run-10) come with it. No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

Apart from the candidate above, the `dsh` role's rows hold at this head:
- **The judge.** Every rendered grant is judged against every rendered deny, by physical path and identity, before anything is made and in a dry run too (`hcom-seat:1843-1894`, `:2005-2009`). The exemptions are pinned to rows 0, 1 and 3 of the two grant lists and to the named deny rows, and each lapses when the row there is not the path rendered at that position or the grant is a link. Row positions match `seat_write_roots`' order (`:1491-1496`) and the dsh allowRead row (`:1795-1796`). Tests: `test_hcom_seat_dsh.py:515`, `:605`, `:656`, `:707`, `:754`, `:871`.
- **Deny row.** Every git, hcom and record path the lever computes is denied for read and for write by its physical path (`:1619-1680`, `:1793-1794`). The residuals are named (`docs/deepseek-harness.md:37-38`).
- **Read grants.** U272c's row is unchanged (`:1795-1796`).
- **Options and argv.** The role table refuses mixed options. The name and profile are regex-bound. `DSH_HOME` and `bin/dsh` are resolved physically, and arguments after `--` pass as argv (`:258-279`, `:319-322`, `:1989-1993`, `:2051-2052`).
- **Environment.** Only the listed names reach the shim, under `env -i`. The caller's token is added at the launch alone and never printed (`:2267-2275`, `:2443-2445`).
- **Per-launch slots.** They are never reused (`:1470-1474`) and are created under umask 077 (`:2114-2124`). They are removed with modes reset and no link followed, and their existence is read through a checked stat. A slot that remains, or that cannot be read, ends the launch 2 on the normal exit and under a signal (`:2357-2452`).
- **Copy and pin.** One blob, `38401bbf`, sha256 `5e1b92b20b9306f0e03c5a79a1c06e0d7ba8c499d7b9c7a1a9e980a8eef22eed` (`agent-config.yaml:861`, `scripts/generated-agent-outputs.json:432`).
- **The omp roles' settings** are byte-identical to the five earlier heads (test `:250`).

The U227b hunt list holds at this head as in run-9 to run-17.

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

1. **The slot presence read depends on the message language** (new; per-launch slots unit). `path_presence` (`hcom-seat:2365-2376`) counts a path as absent only when the stat error contains the English "No such file or directory". The lever pins `LC_ALL=C` elsewhere (`:645`, `:684`, `:1303`) but not for this stat. On a host whose stat messages are translated, for example GNU coreutils under the `ja` locale the Ubuntu client profile installs `language-pack-ja` for, the second presence read after a good removal would print the translated text and refuse. Every dsh launch there would end 2 naming a slot that is gone. It fails closed; not verified on Linux. A `local LC_ALL=C` in `path_presence`, as `pointer_value` has, would make the test locale-independent.
2. **The dsh session keeps the worker's GitHub reach** (carried). `~/.config/gh` is in no deny, and the domain list keeps `github.com` and `api.github.com` (`:2137-2140`), with the HTTPS push URL the shim sets (`:2148-2159`, `:2224-2226`). If the `dsh` role needs no push, deny `~/.config/gh` and drop the GitHub write domains. Not verified: the token's storage is a credential store this run may not read.
3. **`~/.omp/run` is shared with every other omp session** (carried from run-17). It is a `dsh` write root (`:1494`) holding the session-owner locks and daemon records the operator's own omp and the other seats read. A contained session can delete or rewrite them; the reach is denial of service or lock confusion; not verified.
4. **Cleanup while a sandboxed process may still run** (carried). A background process that outlives dsh could race the operator's `chmod -R` and `rm -rf` walk of the state slot; not verified on srt 0.0.81.
5. **Slots after a refusal** (carried). A `refuse()` inside `seat_sandbox_write` after the slots are made (the settings write `:2145-2147`, the shim install `:2232-2234`) exits without `slots_remove`. Hygiene only.
6. **The sandbox holds the operator's login token** (carried pattern, `:2207-2215`).

### Positive patterns

- One judge over the rendered settings, with exemptions pinned to named rows and void when the row drifts or a link moves it.
- Containment stated as denies by physical path, with the residuals named in the docs.
- Fail-closed producers and existence reads.

## 7. Coverage summary

From `coverage-ledger.json` (57 units):

| Status | Units |
|---|---|
| covered | 14 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered:** run-17's fourteen covered units, all re-checked at this head. The seven that read the lever are changed-source and carry the corrections above.
- **Candidate:** the write-root unit.
- **Out of scope:** run-17's out-of-scope units.

**Critic results.** Neither the post-wave critic nor the final-clean critic accepted further work. Neither was an independent agent. This is a single-reviewer coverage statement with one unvalidated candidate, and the PR's own audits have found ten gaps on this branch, and one test gap, that this seat missed.
