# U38 ShellCheck catches a masked producer status before the audit does — brief

GOAL
The class of defect the audit seat found in U31 (`dir=$(cd "$(dirname …)" && pwd -P)`: an inner command substitution whose status is masked, preferences.md line 21) is refused by a lint in CI and in the worker's pre-RESULT self-check, for every shell file the regime ships, so it costs a lint line instead of a fix round (U31b: about 35 minutes of worker, CI and audit time, measured 07:26Z to 08:01Z).

SCOPE
One branch `ci/shellcheck-masked-returns` from `origin/main`. May write: a new `.shellcheckrc` at the repository root, `.github/workflows/test.yaml` (the "Run `ShellCheck`" step's file list, lines 340-343 today), `scripts/run_unit_test.sh` or the Makefile only if the local `make unit-test` or a new `make shellcheck` target should run the same list, the shell files the widened list and the new check flag (`scripts/orchestrator/*` without an extension, `home/dot_local/bin/common/executable_*` shell scripts, `install/**/*.sh`, `scripts/*.sh`) with the minimal fixes the check demands (capture and test the producer, or split the path in the shell as U31b did), and `home/dot_agents/skills/hcom-worker/SKILL.md` "Reply" item (e) only if U36 has landed (else the sentence goes into the brief of the next skill unit): "the ShellCheck run is part of the local checks". Nothing else.

CONTEXT (measured 2026-10-24T08:2xZ on `origin/main` ad3206af)
- `.github/workflows/test.yaml:340-343` runs `git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -`; `scripts/orchestrator/hcom-seat` and `hcom-dispatch` (no extension) and every file under `scripts/orchestrator/` and `home/dot_local/bin/common/` are outside that list; there is no `.shellcheckrc`, and SC2312 (`check-extra-masked-returns`, an optional check: "Consider invoking this command separately to avoid masking its return value") is not enabled anywhere.
- The U31 defect would have been reported by SC2312 at `scripts/orchestrator/hcom-seat:58` and the three sibling levers (inferred from the check's definition; measure it in ACCEPTANCE 1 against `git show 89427c81:scripts/orchestrator/hcom-seat`).
- Levers are bash with shdoc headers (standing order 8); the `executable_` copies are byte-identical to the checkout scripts (U31 pins), so linting the checkout copies suffices and the copies are regenerated.

ACCEPTANCE
1. `.shellcheckrc` enables `check-extra-masked-returns` (and nothing that disables an existing default); `shellcheck` on `git show 89427c81:scripts/orchestrator/hcom-seat` (written to a temp file) reports SC2312 at the `dirname` line (paste); on `origin/main` the same file is clean.
2. The CI step lints the widened list (`setup.sh`, `install/**/*.sh`, `scripts/*.sh`, `scripts/orchestrator/*`, `home/dot_local/bin/common/executable_*` that start with a bash shebang; select by shebang, paste the selection command); every reported SC2312 and any other new finding fixed at root cause (capture then test, or shell splitting), never with a `# shellcheck disable` line; the fixes change behaviour only by refusing on a producer failure that was silent before, each with a failure-injection test where a test file for that script exists.
3. A `make shellcheck` target runs the same list locally; `make unit-test` unchanged; `make render-check` refreshes the lever pins after the fixes.
4. CI green; PR body `Program-Unit: regime-cutover/U38`, no threat table needed (a lint and refusals; say so), the footer; pre-RESULT five-point self-check; orchestrator's own verdict with the ACCEPTANCE 1 reproduction.

TIMEBOX
90 minutes.

FORBIDDEN
No `# shellcheck disable` added; no edits outside SCOPE; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 23).

ADDENDUM (orchestrator-sari, 2026-10-24T11:2xZ, worker question bus row 5730, answer row 5754)
1. ACCEPTANCE 1 premise corrected as measured (shellcheck 0.11.0, `enable=check-extra-masked-returns`): on `git show 89427c81:scripts/orchestrator/hcom-seat` SC2312 fires once at `:192` (a `[[ $(git rev-parse ...) -ef ... ]]` test), not at `:58`; ShellCheck exempts `dirname` and `basename` from SC2312, so the lint catches the class but not the U31 instance. Record the probe output in the PR body; never describe SC2312 alone as detecting the exempt shape.
2. SCOPE granted: a new `scripts/ci/masked-dirname-check.sh` that refuses a `$(dirname` or `$(basename` whose argument is itself a `$( )` substitution, across the same widened file list, called from `make shellcheck` and the CI ShellCheck step; a new `tests/unit/test_masked_dirname_check.py` (not `tests/unit/test_ci_workflows.py`, which U39 edits on its branch) with a positive case (the 89427c81 `:58` shape), a negative case (`dirname` of a plain variable) and a failure-injection case (an unreadable file list refuses, preferences line 21).
3. ACCEPTANCE 1 amended: SC2312 fires on the class and the supplemental check fires on the exempt shape at `89427c81:58`; `origin/main` is clean under both.

ADDENDUM 2 (orchestrator-sari, 2026-10-24T11:2xZ, worker note bus row 5764, answer row 5787)
Measured size: 72 bash files by shebang, 150 findings in 31 files (144 SC2312, 6 defaults in files never linted before). Split: this unit lints two groups, `scripts/orchestrator/*` and the `home/dot_local/bin/common/executable_*` bash scripts, and fixes every finding there at root cause; the CI step and `make shellcheck` name the groups so the widening is visible. `setup.sh`, `install/**/*.sh`, `scripts/*.sh` and `scripts/lib` (36 in `update-agent-assets.sh`, 17 in `generate-docs.sh`, 6 in `check-tools.sh`, the rest) are U38b, its own brief after this unit lands; this unit does not lint them. The timebox is the reason: a 31-file installer diff is not one audit. No omp subagents on a seat.
