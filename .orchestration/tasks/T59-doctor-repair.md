# T59: doctor REPAIR=1 — least-disruptive reconciliation (H5)

task_id: T59
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-harness-composability-integration.md (Phase 5)
analysis: .orchestration/analysis/harness-composability-research.md (H5)
depends: T57, T58 (accepted)

[memory: decision — make doctor REPAIR=1 repairs only detected drift with the least-disruptive action per category (single-target chezmoi apply, chmod, step-scoped reinstall), verifies convergence with a re-scan, and never auto-removes STALE/ORPHAN assets.]

## Goal

Replace "when anything drifts, rerun all of make update" with per-finding
minimal repair plus a convergence check (the operational analog of cordis
loader reconciliation: least-disruptive op per field, order-independent,
terminating).

## Allowed files (edit boundary)

- scripts/check-agent-runtime.py (repair mode)
- Makefile (doctor target: plumb REPAIR=1 variable, minimal diff)
- scripts/update-agent-assets.sh ONLY IF step-scoped invocation requires
  an entry point (e.g. accepting a function name argument). If needed,
  ask via agmsg BEFORE editing (per the plan risk clause) with the exact
  proposed diff shape.
- tests/unit/ (matching modules)
- Your artifact paths (T59 five artifacts)

## Forbidden actions

git commit; git push; bats; dependency changes; real-HOME repairs during
development (fake HOME only — chezmoi calls in tests must target fake
destinations or be stubbed); auto-removal of STALE/ORPHAN (suggestions
only, unchanged from T58); repairing anything not first detected by the
scan; guard weakening.

## Repair action table (fixed by the plan)

| Finding category                                          | REPAIR=1 action                        |
| --------------------------------------------------------- | -------------------------------------- |
| missing file (source-derived)                             | `chezmoi apply <single target>`        |
| content differs                                           | `chezmoi apply <single target>`        |
| executable bit missing                                    | `chmod +x <target>`                    |
| plugin/asset step missing or stale per manifest vs source | run ONLY that update-agent-assets step |
| STALE / ORPHAN                                            | suggestion only (never auto-remove)    |

## Work order (exact; ambiguity -> ask via agmsg)

1. Default behavior (no REPAIR): byte-identical to today — pin with a
   test that captures current output on a fixture and compares.
2. With REPAIR=1 (env var read by check-agent-runtime.py; Makefile passes
   it through): after the normal scan, execute the mapped action for each
   finding, printing one `repaired: <category> <target> (<action>)` line
   per action.
3. Convergence: re-run the scan after repairs. Zero remaining repairable
   findings -> exit as today. Any remaining repairable finding -> print
   `non-convergent after repair` and EXIT NONZERO (one repair round only;
   no loops).
4. Step-scoped reinstall: prefer invoking update-agent-assets.sh with a
   step-function argument if you add one (ask first, see Allowed files);
   otherwise use `bash -c 'source ...; <fn>'` ONLY if the script's
   structure makes that safe (verify set -e/-u interactions and document;
   if unsafe, the argument entry point is the answer).
5. Tests (fake HOME): each category repaired by exactly its mapped action
   (stub chezmoi/chmod/step calls and assert invocations); convergence
   success; forced non-convergence -> nonzero; REPAIR unset -> zero
   mutations (spy on all action functions); STALE/ORPHAN untouched with
   REPAIR=1.
6. Style gates per repo conventions.

## Validation (record in validation artifact)

1. `make format` exit 0; `bash -n` on touched shell.
2. `make unit-test` all green (totals + new count).
3. `make validate-agent-assets` green.
4. Fake-HOME transcripts: one full REPAIR=1 run showing repaired lines +
   convergence, one non-convergent run, one REPAIR-unset no-op proof.
5. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

- Five artifacts (T59 set); T45-contract memory add executed and quoted.
- Live repair verification is T61 E2E-3' (intentional single-file
  deletion -> REPAIR=1 -> converged).
- Reply `AGMSG-RESULT v1 task_id=T59 status=ready_for_review ...`.
  max_turns=25.
