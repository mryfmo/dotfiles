# Security audit report: dotfiles at 88d53ce1e8bbda5cae2186803e3ddba4556ad465

## 1. Run, scope and limits

**This is a partial pass.** It is a scoped run, and it ran without independent agents.

**Profile and scope.** The profile is `standard`, scoped to the U227b change against the merged main, d2389a05..88d53ce1e8bbda5cae2186803e3ddba4556ad465 (branch `feat/dsh-profile-login-route`): the same nine files as round 3. Round 4 (U227e) merges main, which brings U226 (#674, the DSH build-commit input) and U224 (#673, which removes Understand-Anything), so the conflict resolution in `update_deepseek_harness` is hunted as its own unit.

The brief names `d1ecd495` as the base and `c4195463..HEAD` (29 paths) as the change, and calls run-6 the U227b head; run-6 swept U254. Every other top-level directory and the root files are carried as `out_of_scope` units, and no coverage claim is made for them.

**Output directory.** The brief names `run-8`, which already held the U264 sweep of 1a4d712f. This run writes to `run-9` and leaves `run-8` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Planned: four reconnaissance agents, one hunter wave, two critics, and one verifier per candidate. Spent: zero delegated agents.

**Execution.** Sandboxed source-and-local-only policy, and in practice source only. No target code ran.

**Independence gap.** The platform's delegation tool and eval kernel are denied by policy on this seat. Reconnaissance, the hunter wave and both critics ran in the parent, and no fresh independent agent reviewed this coverage. `run-metadata.json` therefore records `run_status: "incomplete"` with reason `independent_agents_unavailable`. No candidate survived the hunt, so there was nothing for a Phase 3 or Phase 5 verifier to verify.

**Prior runs.**
- **run-7** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-7`, source 1d23154b) is the U227b round-3 sweep. Its six units are re-checked here with lines re-mapped, because U224's removal shifts the updater.
- **run-8** (source 1a4d712f) is the newest ledger and carries every other unit. Its five U249 units are absent at this head and stay out of scope.

No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

No candidate survives. Each of the brief's questions, plus the merge:

**The rendered rows, as configuration an attacker who writes the profile could abuse.** Unchanged since round 3.
- `command` and `args` are the constant `omp auth-gateway stdio` (`generate-agent-configs.py:172`).
- Models must match `claude-` plus the launcher-safe form (`:167`, `:237-241`).
- The row carries no `env` and no `cwd` (`cordis.patch.yml:11-27`), so the plugin's allowlist and `homedir()` apply.
- Whoever writes `~/.dsh/profiles/thak` already decides which code DSH loads. The command row is that same operator authority.

**The updater's symlink step.**
- Plugin, profile and `node_modules` are each resolved physically and must lie under `DSH_HOME` (`update-agent-assets.sh:1905-1934`, `:1810-1820`).
- A plugin directory linked from outside `DSH_HOME` is refused with nothing installed.
- A directory or a file at the link name is refused and left alone (`:1935-1938`).
- A symlink there is replaced by a temporary link and `os.replace` (`:1826-1835`), which renames the link itself. A failure leaves the previous link.
- The step converges on the already-installed, fresh-install and repair paths (`:2020`, `:2106`, `:2109`).

**That no key or Ollama row survives.**
- Every dsh row is `{ model: claude-..., route: omp-gateway }` (`agent-config.yaml:544-590`).
- `DSH_ROUTES` is `omp-gateway` only (`generate-agent-configs.py:164`).
- The rendered profile has no providers block (`cordis.patch.yml:2-10`).
- A case-insensitive search of the DSH files for `ollama`, `apiKey`, `OLLAMA_` and `DEEPSEEK_API` finds nothing.

**The round-4 merge with U226.** The resolution keeps both units' controls:
- **U226's control still runs first.** The `DSH_COMMIT` refusal (`update-agent-assets.sh:1849-1852`) follows only the opt-in, and precedes U227b's link-row checks and the download.
- **The build line is intact.** It still exports the pinned commit (`:2093`) inside the sha256-verified archive.
- **The receipt records both units.** `dsh_record` (`:1796-1798`) lists the commit build command and the link commands. Its whole line equals the network-bounds exemption (`tests/unit/test_network_bounds.py:392`), which I compared over the committed blobs.
- **The pin is kept.** The manifest's `ref_commit` and its render constant are intact (`agent-config.yaml:1358`, `:1382`; `scripts/lib/installer-pins.sh:37`).

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

1. **Merge ordering (carried, still open).** The profile names a plugin this head does not deploy: `home/dot_dsh/plugins/omp-gateway` belongs to U240, which is not an ancestor. If U227b merges before U240:
   - `chezmoi apply` deploys a profile with `llm-deepseek` disabled and no gateway;
   - `make update`'s DSH step refuses with exit 1 on every opted-in host (`update-agent-assets.sh:1905-1908`).

   This fails closed, so it is availability only. U240 should merge first, or both together.
2. **Predictable temporary link name** (carried). It is `${link}.tmp.$$` (`update-agent-assets.sh:1826`), inside the operator's own `node_modules`, and is cleared first.

### Positive patterns

- A conflict resolution that keeps both units' controls, and keeps the receipt line and its exemption equal.
- Physical-path containment and atomic relinks.
- Constants and a strict model regex for the rendered rows.
- The withdrawn key routes removed outright.

## 7. Coverage summary

From `coverage-ledger.json` (44 units):

| Status | Units |
|---|---|
| covered | 7 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 37 |

The seven covered units, each owned by `parent-hunter` with source checks, are run-7's six U227b units re-checked at this head plus the new U226×U227b merge-resolution unit.

The 37 out-of-scope units are carried from run-8: its five U249 units (changed source) and its 32 other out-of-scope units. U226 and U254 are now in this head through main, but they are outside the U227b change, apart from the merge resolution; they were swept in run-1 and run-6.

**Critic results.** The post-wave critic accepted one unit (the merge resolution), which was covered in the same wave. The final-clean critic found no further work. Neither was an independent agent (see section 1), so this is a single-reviewer coverage statement, not a clean independent pass.
