# Security audit report: dotfiles at d4046bdf99a10ac1b627ce4f4c972768e681f92e

## 1. Run, scope and limits

**The unvalidated candidate is now on `origin/main`.** U272 merged as #697 (`origin/main` 25427b91) while the candidate run-11 recorded was still unvalidated. Run-12 to run-18 each asked for it to be settled before U272 merged. It is therefore no longer a branch's merge gate: it is open on the default branch, on every host whose operator opts in to `DSH_HOME` and launches `hcom-seat dsh`. No fresh independent verifier is available on this seat (the delegation tool and eval kernel are denied by policy), so it stays an unvalidated ledger candidate and is **not a finding**. `findings.json` holds no record, and `run-metadata.json` records `run_status: "incomplete"` with reason `candidate_validation_incomplete`.

**What the head is.** d4046bdf is one commit, U306 ("the omp-gateway child inherits the launcher's OMP_PROFILE"), on `origin/main` 25427b91. The branch is `fix/omp-gateway-child-omp-profile`, and the brief's file name is `U309-…-u306-head`; its GOAL and CONTEXT are the U227b template again. U306 adds `OMP_PROFILE` to the omp-gateway plugin's default child environment list (`home/dot_dsh/plugins/omp-gateway/config.mjs:10-13`) and a recorder test. The first real dsh turn failed with `SQLITE_AUTH` because the child opened the denied `~/.omp/agent`.

**What else is on this main since run-18.**
- **U272 merged.** The lever, its deployed copy, the pin, `docs/deepseek-harness.md` and the dsh tests are byte-identical to run-18's head 9d5d9a42 (blob `38401bbf`). `scripts/orchestrator/README.md` differs by one line outside the dsh section.
- **U227f** disables the two base rows that read a DeepSeek API key (`cordis.patch.yml:9-12`). The bash-sandbox row moves to `:13-14`.
- **U283 and U276b** change the updater; the profile install is now `update-agent-assets.sh:2151`, with `MISE_EXEC_AUTO_INSTALL=false`. U276 adds `make deploy-kit`, which never runs the updater.

**Scope.** Three readings:
- **U306:** the head's own change, hunted as one new unit;
- **U272:** the merged `dsh` role, carried from run-18 and re-checked same-source;
- **U227b:** the hunt list the brief names, re-checked against `main`'s updater and profile.

**Profile.** `standard`, scoped, source only. No target code ran. The brief names `d1ecd495` as the base and run-6 as the set to carry; run-6 swept U254, so run-18 is carried. Every other top-level directory and the root files are `out_of_scope` units with no coverage claim.

**Output directory.** The brief names `run-8`, which holds the U264 sweep. This run writes to `run-19` and leaves `run-8` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Spent: zero delegated agents; every phase ran in the parent.

**Prior runs.**
- **run-18** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-18`, source 9d5d9a42) is the last U272 sweep. All 57 of its units are carried:
  - the seven lever units same-source, since the merged lever is byte-identical;
  - the U227b units re-mapped to `main`'s updater and profile: six changed-source, one same-source;
  - the candidate, still a candidate;
  - 42 out of scope.
- One new unit covers U306.

No prior run holds a finding. The PR's own audits found ten gaps and one test gap on U272 that this seat's sweeps missed (run-14 to run-18, section 1). Read this run as advisory.

**Deferred.** Nothing.

| Fingerprint | Ledger unit | Record for a verifier |
|---|---|---|
| `dsh-seat/DSH_HOME-write-root/host-pnpm-install-outside-srt` | `scripts/orchestrator/hcom-seat#seat_write_roots-dsh` | `agents/parent-hunter/scratch/unvalidated-candidate.json` (schema-shaped `needs_validation`, validated with `validate-findings.cjs`; line fields re-mapped to this head) |

### 1a. The unvalidated candidate (not a finding)

**What it claims.** The merged `dsh` role contains the DeepSeek harness under srt. The write roots of that containment include all of `DSH_HOME` (`scripts/orchestrator/hcom-seat:1494`). No write deny applies under it: the rendered write denies (`:1720-1749`, plus the deny row at `:1794`) all lie outside `DSH_HOME`, and the judge refuses any grant that overlaps a rendered deny. The contained session has a command tool, because the kit profile disables DSH's own `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:13-14`).

Outside srt, the operator's `make update` first runs `chezmoi apply` (`Makefile:124`), which restores only the managed profile files. It then runs the updater (`Makefile:133`). On its install path the updater runs `(cd "${DSH_HOME}/profiles/thak" && MISE_EXEC_AUTO_INSTALL=false mise exec -- pnpm install)` as the operator, with no `--ignore-pnpmfile` or `--ignore-scripts` (`scripts/update-agent-assets.sh:2151`).

So a `.pnpmfile.cjs` that the contained session plants in `~/.dsh/profiles/thak` survives into that install. pnpm loads such a file by default, so it would run as the operator **outside the sandbox** at the next harness install.

The lever's hazard account covers only the lever itself:
- tools planted under `DSH_HOME` are refused (`hcom-seat:837-839`);
- `bin/dsh` never runs outside srt (`README.md:142`).

The docs' "the dsh runtime is never executed outside srt" (`docs/deepseek-harness.md:55`) does not extend to code the runtime can write.

The harness trees `DSH_HOME/dsh/<tag>.*`, built outside srt (`update-agent-assets.sh:2142`), sit in the same writable root. Reaching them needs a narrower race with a contained session that is running at the same time.

**Why it is not confirmed.** Three blockers remain:
1. pnpm's default `.pnpmfile.cjs` loading for the version mise provides is package-manager behaviour that is not visible in this repository.
2. Whether srt 0.0.81 lets the contained session create that file under its write root is sandbox behaviour that is not visible either.
3. No independent verifier has re-checked the trace.

No code ran here, by task rule.

**Local plan for a verifier.** Sandboxed, network off:
1. Make a fixture `DSH_HOME` whose `profiles/thak` holds a `.pnpmfile.cjs` that writes a marker. Run the updater's exact command with `--offline` and check for the marker.
2. Run `hcom-seat dsh --home <fixture> -- <a write of that file>` and check whether srt allows the write.

**Smallest fix.** Either change closes the path:
- Narrow the `dsh` role's write roots to the runtime state DSH writes, or deny writes inside srt to `DSH_HOME/bin`, `DSH_HOME/dsh`, `DSH_HOME/profiles` and `DSH_HOME/plugins`. Under the judge, such denies need a tag of their own (`tag_row`) paired with `DSH_HOME`'s grant row, or every launch refuses.
- Run the profile install with `--ignore-pnpmfile --ignore-scripts`, and refuse unmanaged files in `profiles/thak` before it. This one touches only the updater and needs no lever change.

## 2. Security posture

**U306.**
- **The list grows by one name and still holds no credential.** The child's environment is still a named allow-list. `OMP_PROFILE` is its only addition (`config.mjs:10-13`). `pickEnv` copies only listed names the plugin's own environment holds (`gateway-client.mjs:26-33`; `index.mjs:73`). The use-case test still asserts that no KEY, TOKEN, SECRET, OAUTH or PASSWORD name is listed (`test/use-cases.test.mjs:622-626`). The new recorder test asserts the child carries `OMP_PROFILE` only when set (`test/gateway-client.test.mjs:251-283`).
- **The value moves the child into no new grant.** Under `hcom-seat dsh`, `OMP_PROFILE` is the lever's own `dsh`, set under `env -i` (`hcom-seat:2268`). It moves the child from the denied `~/.omp/agent` into `~/.omp/profiles/dsh`, which the role already grants and the judge pins to its own position (`:1494`, `:1795`, `:1801-1805`). srt still denies every other profile, so a different value would fail as the g6 run did, not widen.

**U272, merged.** The rows hold as run-18 recorded them at the byte-identical lever: the judge over every rendered grant and deny with position-keyed exemptions, the deny row by physical path, the options and argv, `env -i`, and the per-launch slots with checked presence reads.

**U227b on `main`.** The link step is unchanged and 47 lines later (`dsh_link_plugin` `:1851`). The profile gains U227f's two disabled rows, which remove API-key routes and add none.

## 3. Confirmed findings

None. The one candidate is unvalidated (section 1a) and is not a finding.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None as a final record. The candidate in section 1a would be a `needs_validation` record once an independent verifier re-checks it; it is now open on `origin/main`.

## 6. Hardening notes and positive patterns

### Hardening

1. **The gateway child's login state now lives in a dsh write root** (new; U306 unit). With `OMP_PROFILE=dsh` the child keeps its omp state, `agent.db` and whatever login state omp stores there, in `~/.omp/profiles/dsh`. The contained session can read and rewrite that profile (`hcom-seat:1494`, `:1795`). The child's environment carries no token name, so its Claude login comes from that profile or from a source this run may not inspect. If it is a stored refresh credential, it is a second copy of the operator's login inside the sandbox, beside the exported `CLAUDE_CODE_OAUTH_TOKEN` (pattern 7), and it outlives the launch. Not verified: the profile's contents are a credential store.
2. **The slot presence read depends on the message language** (carried from run-18). `path_presence` (`hcom-seat:2365-2376`) matches the English "No such file or directory" with no locale pinned, so a host with translated stat messages would end every dsh launch 2 after a good removal. A `local LC_ALL=C` there fixes it. Not verified on Linux.
3. **The dsh session keeps the worker's GitHub reach** (carried): `~/.config/gh` is in no deny, and the GitHub domains and push URL stay.
4. **`~/.omp/run` is shared with every other omp session** (carried): it is a dsh write root holding the session-owner locks and daemon records the operator's omp reads.
5. **Cleanup while a sandboxed process may still run** (carried).
6. **Slots after a refusal** (carried).
7. **The sandbox holds the operator's login token** (carried pattern, `hcom-seat:2207-2215`).

### Positive patterns

- A child environment kept as a named allow-list, with a test that no credential name is on it and a recorder that pins what the child receives.
- A fix that moves the child into the profile the containment already grants, instead of granting the default profile.

## 7. Coverage summary

From `coverage-ledger.json` (58 units):

| Status | Units |
|---|---|
| covered | 15 |
| candidate | 1 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 42 |

- **Covered:** the new U306 unit, the seven merged-U272 lever units (same-source), and the seven U227b units re-checked against `main`.
- **Candidate:** the write-root unit, now on `origin/main`.
- **Out of scope:** run-18's out-of-scope units.

**Critic results.** Neither the post-wave critic nor the final-clean critic accepted further work. Neither was an independent agent, so this is a single-reviewer coverage statement with one unvalidated candidate.
