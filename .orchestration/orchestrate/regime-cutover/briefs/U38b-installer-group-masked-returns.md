# U38b The installer group under SC2312: setup.sh, install/**, scripts/*.sh, scripts/lib — brief

GOAL
The second lint group of U38 (ADDENDUM 2) comes under the same two checks as the regime's own scripts: ShellCheck with `check-extra-masked-returns` and the masked-dirname check. Every finding in `setup.sh`, `install/**/*.sh`, `scripts/*.sh` and `scripts/lib/*` is fixed at root cause (the producer's status read and acted on), the CI step and `make shellcheck` drop the `--norc` exception for this group, and a bootstrap on a fresh host still works.

SCOPE
One branch `ci/installer-group-masked-returns` from `origin/main` (after U38 lands; it carries the mechanism). May write: the shell files of the group (`setup.sh`, `install/**/*.sh`, `scripts/*.sh`, `scripts/lib/*`) with the minimal fixes the checks demand, `Makefile` and `.github/workflows/test.yaml` (the group's `--norc` removed, nothing else), the tests that pin the installers' behaviour (`tests/install/**/*.bats`, `tests/unit/test_supply_chain_policy.py`, `tests/unit/test_update_agent_assets*.py` and the like) with one failure-injection case per fixed decision where a test file for that script exists, `home/.chezmoiscripts/**` only where a template is generated from a group script (run `make render-check`). No new `# shellcheck disable` line, no `|| true` to silence a check.

CONTEXT (U38 ADDENDUM 2, measured 2026-10-24T11:2xZ on 43e647f2)
- 150 findings in 31 files across the whole widened list; this group holds 96 of them under the rc: `scripts/update-agent-assets.sh` 36, `scripts/generate-docs.sh` 17, `scripts/check-tools.sh` 6, `setup.sh` 6, the rest 1 to 6 per file across `install/**` and `scripts/lib`, plus 6 default-rule findings in files never linted before.
- The fix patterns are U38's (its PR body): capture then test (`local x; x=$(cmd) || return 1`, never `local x=$(cmd)`); a pipeline inside `$()` runs its producer alone and post-processes the capture; `done < <(producer)` becomes a checked capture with the empty-output guard (`<<< ""` feeds one empty line); `eval "$(cmd shellenv)"` captures first; an intentional fallback stays inside the capture; nested substitutions split outermost last.
- Compatibility: `setup.sh` and `install/**` run under macOS `/bin/bash` 3.2 (no `${var,,}`, associative arrays, `mapfile`, `&>>`); keep `shfmt -i 4 -sr` formatting.
- Blast radius: these are the installers; a fix that turns a silent producer failure into a refusal changes bootstrap behaviour on a host where that producer fails. Each such refusal names the producer in its message. The CI public-bootstrap and chezmoi-apply jobs are the live check.

ACCEPTANCE
1. `make shellcheck` exits 0 with the group under the rc (the `--norc` gone from the Makefile and the workflow); the per-file count table before and after in the PR body (from `shellcheck -f gcc` or the make target's output, pasted).
2. Every fixed decision that can refuse at bootstrap has a failure-injection test where a test file for that script exists; the list of scripts without a test file is in the PR body with the reason each is left untested.
3. CI green on the head including the three public-bootstrap and three chezmoi-apply jobs (the installers ran); `make validate-agent-assets` and `make render-check` unchanged or regenerated, pasted.
4. PR body `Program-Unit: regime-cutover/U38` (the parent id, standing order 24), the threat table (one row per script group: what now refuses that was silent, and why that is right), the footer; pre-RESULT five-point self-check; audit seat (blast radius: the installers).

TIMEBOX
3 hours. If the count exceeds the timebox, stop at a file boundary, land the files done with the group still under `--norc` for the rest, and name the remainder as U38c with the counts; never a half-fixed file.

FORBIDDEN
No `# shellcheck disable`, no `|| true` to silence, no `set +e` tricks; no behaviour change beyond refusing on a producer failure that was silent; no omp subagent; no merge, rebase, force-push, PR close.

REPORT
Per STANDING 12 plus the RESULT line (standing order 23).

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (lines 20 to 24).

ADDENDUM (orchestrator-sari, 2026-10-24T12:5xZ): U38's threat table (PR #499 issuecomment-6384408600, after Codex P1 4367158102) names two residuals that this unit closes under standing order 22: (a) a pin test for the step-to-target wiring (the required ShellCheck CI step runs `make shellcheck`, a PR-controlled target: the test pins that the step calls exactly that target with no other command, and that the target's two groups and both checks are the ones the test enumerates); (b) the masked-dirname checker's multi-line and heredoc false negative (a `$(dirname "$(...)")` split across lines or inside a heredoc is not seen): close it in `scripts/ci/masked-dirname-check.sh` with cases in `tests/unit/test_masked_dirname_check.py`, or record why it stays with the shape it misses. ACCEPTANCE 5: both rows closed or dispositioned in the PR body.
Also under (a): the default group's recipe line `git ls-files -z -- "$@" | xargs -0 shellcheck --norc -x` runs shellcheck with no files when the list is empty under GNU xargs (a failure) but runs nothing under BSD xargs (macOS, a silent pass); when this unit moves the group under the rc, give it the masked group's explicit empty-list and no-bash-script refusals instead of the xargs form, pinned by the same test.
