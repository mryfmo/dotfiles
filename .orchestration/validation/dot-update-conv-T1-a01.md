# dot-update-conv-T1-a01 validation

review_surface: crit-data
reviewer: codex
review_source: .agents/worklog/codex/review/dot-update-conv-T1-a01-crit.json
review_outcome: approved

## Test-first RED

Command:

    uv run python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing -v

Verbatim pre-implementation output (exit 1):

    test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... FAIL

    ======================================================================
    FAIL: test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/mryfmo/Workspace/dotfiles/.claude/worktrees/update-converge/tests/unit/test_runtime_health.py", line 273, in test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing
        self.assertNotIn("Error:", result.stdout + result.stderr)
        ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    AssertionError: 'Error:' unexpectedly found in '\n==> Codex plugins\nCodex Superpowers was not installed: the OpenAI-curated catalog is unavailable.\nRun `codex login`, then `codex plugin add superpowers@openai-curated`.\nError: plugin superpowers@openai-curated was not found\n'

    ----------------------------------------------------------------------
    Ran 1 test in 0.014s

    FAILED (failures=1)

## Focused GREEN

Same command after implementation, verbatim output (exit 0):

    test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok

    ----------------------------------------------------------------------
    Ran 1 test in 0.013s

    OK

## Final adh-test convergence E2E

Command:

    set -o pipefail; limactl shell adh-test -- bash .orchestration/validation/dot-update-conv-T1-a01.md <repo> | grep -E <acceptance-markers>

The temporary validation file was the shell harness before this evidence replaced it. It downloaded checksum-verified chezmoi 2.70.4, initialized an actual old-main source from commit b884aec, seeded all 23 rendered old-main run_once SHA-256 records, copied the changed worktree into VM-local storage, and ran literal make update twice. Only unrelated already-bootstrapped asset/mise/Herdr operations were stubbed; chezmoi, Makefile, and the 51 default-shell installer were real. Verbatim filtered output (exit 0):

    chezmoi_2.70.4_linux_arm64.tar.gz: OK
    === old-main apply without scripts ===
    === seed old-main run_once state ===
    old-run-once-records=23
    === literal make update: first ===
    Login shell changed to /usr/bin/zsh; sign in again or run `exec zsh`.
    first-update-exit=0
    Login shell changed to /usr/bin/zsh; sign in again or run `exec zsh`.
    === literal make update: second ===
    second-update-exit=0
    run-once-repeated=no
    === final chezmoi drift gate ===
    final-status=clean
    drift-warning-count=0
    === unauthenticated Codex Superpowers output ===
    Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.
    Run `codex login`, then `codex plugin add superpowers@openai-curated`.
    superpowers-status=0
    Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.
    Run `codex login`, then `codex plugin add superpowers@openai-curated`.
    raw-error-count=0
    scratch-user-removed=yes

The duplicated first-run and guidance lines are the harness's explicit grep assertions echoing the matched lines after their original command output.

## Harness corrections and cleanup

- The first init attempt used prompt variable names instead of chezmoi's displayed prompt keys and exited before apply; its EXIT trap removed the scratch user.
- The next attempts established the run_once proof but exposed missing scratch PATH and source-root setup in unrelated fixture steps. Each attempt's EXIT trap removed the user/home/sudoers state.
- Cleanup after each correction was separately checked and printed:

      scratch-user-removed=yes

- One final filtered rerun initially hit the host filesystem sandbox before VM access; the approved retry was scoped to limactl shell adh-test and produced the successful output above.

## Static checks

Commands, each exit 0 with empty stdout/stderr:

    bash -n scripts/update-agent-assets.sh
    shellcheck -x scripts/update-agent-assets.sh
    shfmt --indent 4 --space-redirects --diff scripts/update-agent-assets.sh tests/install/common/lifecycle.bats
    git diff --check

The initial shellcheck invocation without -x exited 1 only because the existing dynamic source paths raised SC1091. Verbatim output:

    In scripts/update-agent-assets.sh line 43:
        source "${AGENT_ASSET_SCRIPT_DIR}/lib/asset-manifest.sh"
               ^-- SC1091 (info): Not following: scripts/lib/asset-manifest.sh was not specified as input (see shellcheck -x).

    In scripts/update-agent-assets.sh line 46:
    source "${AGENT_ASSET_SCRIPT_DIR}/lib/installer-pins.sh"
           ^-- SC1091 (info): Not following: scripts/lib/installer-pins.sh was not specified as input (see shellcheck -x).

The static update-contract command:

    if rg -n -- '--exclude=scripts' Makefile; then exit 1; else printf 'make-update-script-exclusion=absent\n'; fi

Verbatim output:

    make-update-script-exclusion=absent

## Agent asset validation

Command and verbatim output:

    make validate-agent-assets

    uv run --with pyyaml scripts/validate-agent-assets.py
    agent asset validation ok

## Full Python unit suite

Command and verbatim output:

    set -o pipefail; make unit-test 2>&1 | tail -5

    ----------------------------------------------------------------------
    Ran 363 tests in 42.169s

    OK

## Crit-data review gate

Initial make require-crit-review output (exit 2):

    Native agent review required before completion.
    - agent lifecycle path changed: scripts/update-agent-assets.sh
    - broad diff touches 7 files
    - broad diff changes 227 lines

The complete diff and evidence were reviewed. Finding-free approval records r_57d210 and r_a8a6ea (the latter after the final debug-path adjustment) were resolved and saved to the declared JSON evidence path. Final command:

    AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-update-conv-T1-a01-receipt.md make require-crit-review

Verbatim output:

    Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.

## CompactionDB decision

Command:

    python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-update-conv-T1-a01: make update applies public and private chezmoi scripts so newly committed run_once content hashes execute exactly once while unchanged hashes remain skipped; make upgrade remains the only tool-pin advancement path. Codex Superpowers add output is captured and raw CLI errors are shown only when DOTFILES_DEBUG is set.'

Verbatim output:

    e24e8cbb-92a4-4643-b4c8-440ebe111a46

## Deliberately not run

    bats: NOT RUN locally (task and repository policy require CI)
    git commit: NOT RUN
    git push: NOT RUN
    codex login: NOT RUN
