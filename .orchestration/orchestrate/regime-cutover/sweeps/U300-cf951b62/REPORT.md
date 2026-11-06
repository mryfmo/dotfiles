# Security audit report: dotfiles at cf951b6224803b062091e61ea121c8a02bc0c6ed

## 1. Run, scope and limits

**No finding, and no candidate.** The hunt over the head's change produced no candidate, and `findings.json` holds no record. The run is still marked incomplete, with reason `independent_agents_unavailable`: the platform's delegation tool and eval kernel are denied by policy on this seat. So reconnaissance, the hunter wave and both critic passes ran in the parent, and no independent critic re-checked the coverage.

**What the head is.** cf951b62 is one commit, U297 ("the public-bootstrap check skips the chromium snap on a GitHub Actions runner"), on `origin/main` 1878b569. The branch is `ci/public-bootstrap-chromium-snap`, and the brief's file name is `U300-…-u297-head`. The change touches four files:
- `install/ubuntu/client/misc.sh`: `install_chromium` returns 0 with one printed line when `is_ci_runner` holds, and a direct run sources `scripts/lib/ci-runner.sh`;
- `home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl`: includes `scripts/lib/ci-runner.sh` before the installer;
- `tests/install/ubuntu/client/misc.bats` and `tests/unit/test_ci_runner.py`: the runner cases.

**The brief contradicts itself again.** Its GOAL and CONTEXT are the U227b template the last five briefs carried, while its branch, file name and head name U297. This run reads both:
- **U297:** the head's own change, 1878b569..cf951b62, hunted as three new units;
- **U227b:** the hunt list (the rendered rows, the link step, no key or Ollama row), re-checked at this head, where U227b is merged (#686).

**U272 is not in this head's history.** `feat/hcom-seat-dsh-role` (1ddd42c9 to d1ffd919) is unmerged, and this head's `scripts/orchestrator/hcom-seat` has no `dsh` role. So run-15's U272 units are out of scope here, each with that reason in the ledger.

That includes the run-11 candidate `dsh-seat/DSH_HOME-write-root/host-pnpm-install-outside-srt`. It is not carried as a candidate at this head, because its premise is U272's srt containment of the dsh session. On `main` the operator runs dsh with their own authority, so a `.pnpmfile.cjs` the session writes under `DSH_HOME` gains it nothing it lacks. The updater leg is on `main` (`scripts/update-agent-assets.sh:2151`, still without `--ignore-pnpmfile` or `--ignore-scripts`), so **the candidate stands again at any U272 head.** It should be settled before U272 merges (run-15 `REPORT.md` 1a).

**Profile.** `standard`, scoped, source only. No target code ran.

**Output directory.** The brief names `run-8`, which holds the U264 sweep. This run writes to `run-16` and leaves `run-8` untouched.

**Source ref.** The checkout was clean at the head both before and after the run.

**Budget.** None was set. Spent: zero delegated agents.

**Prior runs.**
- **run-15** (`~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-15`, source d1ffd919) is the newest ledger of this seat. Its units are carried as follows:
  - the seven U227b units are re-checked here: three same-source, and four changed-source because they read `scripts/update-agent-assets.sh`;
  - its eight U272 units, the candidate included, are out of scope as not in this head's history;
  - its 42 out-of-scope units stay out of scope, with the reason restated for this head.
- The brief calls run-6 the set to carry. Run-6 swept U254, so the newest ledger is carried instead.

No prior run holds a finding.

**Deferred.** Nothing.

## 2. Security posture

**U297.**
- **The skip is narrow and loud.** `install_chromium` skips only where both `GITHUB_ACTIONS=true` and `RUNNER_TEMP` are set (`scripts/lib/ci-runner.sh:24-26`), never on the generic `CI` an agent shell exports. It prints one line and makes no snap or sudo call (`install/ubuntu/client/misc.sh:74-96`).
- **Spoofing the gate gains nothing.** The gate is environment-controlled, but whoever sets both variables only skips a desktop convenience snap. No check, verification or privilege rests on it. The apt packages, the retry, the timeout and the exit codes are unchanged.
- **The library comes from the repository on both paths.** `ci-runner.sh` is included verbatim by the chezmoi template (`run_once_50-client-install-misc.sh.tmpl:8-11`). On a direct run it is sourced from the script's own checkout, only when the function is missing (`misc.sh:14-18`). The library defines one function and runs nothing.
- **One expected re-run.** The `run_once` script's content changes, so every Ubuntu client runs it once more at the next apply: the same sudo `apt-get install` and snap install it already ran.
- **The tests use fakes only.** They use a recording snap, a pass-through `timeout` and a `sudo` function in temporary directories, and assert the skip on both sides: the runner, and an agent shell's `CI=true` off the runner.

**U227b at this head.**
- The renderer, the profile files and the manifest's DSH rows are byte-identical to run-15's head.
- In `scripts/update-agent-assets.sh` the link step is unchanged but 47 lines later (`dsh_record` `:1843`, `dsh_link_plugin` `:1851`).
- Other units changed only two command lines of `update_deepseek_harness`. U276b added `MISE_EXEC_AUTO_INSTALL=false` to the harness build (`:2142`) and the profile install (`:2151`), which only stops mise from installing a missing tool during the step. U283 changed the single-step mode elsewhere in the file.
- The hunt list holds as in run-9 to run-15.

## 3. Confirmed findings

None.

| Severity | Title | Affected boundary | Observed result |
|---|---|---|---|
| — | none | — | — |

## 4. Confirmed finding details

None.

## 5. Needs validation

None. No candidate survived the hunt at this head. The U272 candidate applies only at a U272 head (section 1).

## 6. Hardening notes and positive patterns

### Hardening

None new for U297. The U272 hardening notes (the `dsh` session's GitHub reach, the slot cleanup race, slots after a refusal) apply at U272 heads only; they are in run-15 `REPORT.md` section 6.

### Positive patterns

- One definition of "running in CI", kept equal across the library, `setup.sh` and the chezmoi config by `tests/unit/test_ci_runner.py`, and never keyed on the generic `CI`.
- A CI-only skip that prints what it skipped instead of passing silently.
- Tests that cannot reach the real snap store or `sudo`.

## 7. Coverage summary

From `coverage-ledger.json` (60 units):

| Status | Units |
|---|---|
| covered | 10 |
| candidate | 0 |
| blocked | 0 |
| deferred | 0 |
| out_of_scope | 50 |

- **Covered:** the three U297 units (the CI skip, the include and direct-run source, the tests) and the seven re-checked U227b units.
- **Out of scope:**
  - run-15's eight U272 units, as not in this head's history;
  - run-15's 42 out-of-scope units, outside the U297 change.

**Critic results.** Neither the post-wave critic nor the final-clean critic accepted further work. Neither was an independent agent, so this is a single-reviewer coverage statement. On the U272 branch the PR's own audits found six gaps this seat's sweeps missed (run-14 and run-15 `REPORT.md` section 1), so read this sweep as advisory.
