---
task_id: dotfiles-T133-regime-ci-token-a01
seat: claude-standard-dot-a009
amendment: 1
branch: ci/regime-ci-token-a01
pr: 446
base: f7f3806749815ba9dfd90e7ff9ee390ca6079014
task_sha256: d4798ebf298a380ab939d55c94f753019891e2c42a39626a1e5be3940dfc626b
cost: n/a (the seat's token and time usage is not visible to the worker)
---

# Report: dotfiles-T133-regime-ci-token-a01 (P1-17: authenticate the regime checker's read-only API requests)

- **Task:** AGMSG-TASK of 14:27:05Z (sha `61a9942b…`), then amendment 1 of 14:53:26Z (sha `d4798ebf…`). The branch copy is byte-identical to amendment 1 (validation §1).
- **The question round, before any edit:**
  - **Message 2873:** the first text extended "the checker's minimal environment (HOME, PATH, LANG, UV_CACHE_DIR)". But `scripts/orchestrator/regime-ci.py` at `f7f38067` has none: `checker()` calls `subprocess.run(cmd, cwd=root, capture_output=True, text=True, check=False)` with no `env=`, and `git log --all -S UV_CACHE_DIR` and `-S '"LANG"'` on the file are empty.
  - **Message 2876:** the Check's module command failed on the unmodified module without the proxy variables (§3).
  - **The answer:** option (b), keep the inherited environment, which amendment 1 states.
- **uv:** resolved once to `$HOME/.local/share/mise/installs/uv/latest/uv-aarch64-apple-darwin`, the command and output in §2. That is the directory mise resolves for this checkout, holding the real `uv` binary, not a shim.

## Item 1

- **`.github/workflows/regime.yml`** (+3 lines): the regime-ci step's env gains `GH_TOKEN: ${{ github.token }}` and a two-line comment saying the job's `contents: read` token can only read this repository's contents. `permissions: contents: read`, `persist-credentials: false`, the pinned actions and base-only execution are unchanged.
- **`scripts/orchestrator/regime-ci.py`:** unchanged. The checker inherits regime-ci's environment, so GH_TOKEN reaches it once the workflow sets it. No allowlist is introduced.
- **`tests/unit/test_regime_ci.py`** (+44/−1):
  - a `record_checker(rc)` fixture: a fake base checker that writes its argv and environment to the fixture repository's `.git/checker.json`, then prints the verdict line (rc 0) or a no-verdict line (rc 3);
  - **`test_regime_ci_child_sees_parent_tokens`:** with both ambient token keys cleared and an unrelated `PROBE_KEPT`, it runs neither token, each alone, and both. The child holds exactly the given tokens, plus `PROBE_KEPT` (inheritance);
  - **`test_regime_ci_keeps_tokens_out_of_argv_and_output`:** for the verdict and the no-verdict checker, both synthetic tokens are first asserted present in the child, then absent from the child's argv and from regime-ci's stdout and stderr. The no-verdict case also asserts regime-ci's `no verdict (exit 3)` diagnostic;
  - **`test_regime_yml_sets_the_token`:** the regime-ci step's env has `GH_TOKEN: ${{ github.token }}`, and permissions are `{contents: read}`;
  - **`test_the_regime_workflow_runs_base_code_only`:** its exact env assertion now includes the token.

## Red and green

| Test | Before the workflow change | After |
|---|---|---|
| `test_regime_yml_sets_the_token` | red: `['${{ github.token }}'] != [None]` (§4) | green |
| `test_the_regime_workflow_runs_base_code_only` (updated) | red: the env lacks `GH_TOKEN` (§4) | green |
| `test_regime_ci_child_sees_parent_tokens` | green: characterization, since regime-ci.py has no production change and already inherits | green |
| `test_regime_ci_keeps_tokens_out_of_argv_and_output` | green: characterization, same reason | green |
| `test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config` and the other existing tests | green (existing regressions) | green |

## The module runs

- **Before, on unmodified `f7f38067` (§3):**
  - With the first text's command, without the proxy variables: `Ran 16 tests`, `FAILED (failures=21, errors=1)`. These are 11 `dns error` lines: uv's pyyaml fetch, because `env -i` strips the sandbox proxy variables.
  - With amendment 1's command: `Ran 16 tests`, `OK`.
- **After (§5):** amendment 1's command gives `Ran 19 tests`, `OK`.
- **ruff (§6):** check and format clean on both files.
- **The crit-review gate (§7):** satisfied with the worker review evidence.
- **Caps** (`git diff --numstat f7f38067…<head>`, validation): 3 of 25 outside `tests/` and `.orchestration/`, and 45 of 60 under `tests/`.

## Residuals and unperformed checks

- **Not changed here:**
  - CHECKER_RUN executable selection (PATH, virtual-environment discovery) and GIT_DIR inheritance stay with `dotfiles-T133-regime-ci-token-followup-a01`.
  - Parent startup and shared caches are unchanged.
- **Not shown in this sandbox:** a live hosted-runner `gh api` call with the token. CI on the PR runs the module; the regime job itself runs the base's workflow, so the new env takes effect after merge.
- **Local tools:** Bats was not run locally. `npx --no-install prettier` was refused network access (registry.npmjs.org) and was not retried; formatting is CI's.

## Review

- **The one pre-push round:** a fresh, read-only general-purpose subagent, working inside its sandbox, returned `Verdict: correct` with no P0, P1 or P2 (the worker-crit JSON and receipt).
  - **Security:** it confirmed the token is set in the verifier step's env only, never interpolated into `run:`; permissions stay `contents: read` with `persist-credentials: false`; no step runs head code, and the base's checker reads base-dispatched bytes.
  - **Tests:** it confirmed they are non-vacuous.
- **Two P3, fixed in the one correction round:** the comment's wording ("public repository contents only" became "can only read this repository's contents"), and the rc=3 no-verdict assertion.
- **One P3, unchanged:** a real checker that echoed a token would leak through regime-ci's 300-character no-verdict tail (regime-ci.py:161). That is existing behaviour of the unchanged script.

## Completion

- **PR:** https://github.com/mryfmo/dotfiles/pull/446, opened ready for review, not as a draft, at 2026-10-20T21:26:54Z on `085142f0`, inside the sandbox (validation §8).
- **CI on `085142f0`:** `gh pr checks 446 --repo mryfmo/dotfiles --watch` exited 0. All 11 checks pass, and the 10 check runs all succeeded (§9).
- **The Bot:** Codex's code review (completed 21:38:17Z) and security review (21:29:43Z) of `085142f0` were triggered when the PR opened. Both report `has_any_findings: false`, with no review threads and no comments (§10). No `@codex review` was posted.
- **The final head** adds only this directory's records on top of `085142f0`. The RESULT carries its CI.
- **The push:** the task's `push -u` landed; only its upstream write was refused (sandbox record).
- **Open items:** none. Any advisory P2 goes to the owner the orchestrator names.

## Revise round 2 (ACCEPTANCE status=revise of 2026-10-21T01:30:11Z, previous_head a8c03fae)

- **The finding:** the security-profile review of `a8c03fae` (`.orchestration/validation/dotfiles-T133-regime-ci-token-a01-security-a8c03fa.md`) raised a P2. The output-secrecy row claimed closed, but `regime-ci.py:161` forwarded the checker's diagnostics unredacted: the no-verdict tail `(run.stdout + run.stderr)[-300:]` and the checker lines. A checker that echoed a token would leak it.
- **The fix, code only:** `redact(text)` masks the values of `GH_TOKEN` and `GITHUB_TOKEN` from regime-ci's environment, and any token-like literal (`gh[pousr]_[A-Za-z0-9]{20,}`, `github_pat_[A-Za-z0-9_]{20,}`), as `[redacted]`. It applies to both paths: the no-verdict diagnostic, redacted before the 300-character truncation so a split token cannot survive as a fragment, and every forwarded checker line. The verdict detection still reads the raw stdout.
- **The test:** `test_regime_ci_redacts_tokens_in_checker_diagnostics` uses a fake checker that prints the env token and a token-like literal to stdout and the env token to stderr. In its no-verdict case (exit 3), the diagnostic still reports `no verdict (exit 3)`. In its FAIL case (exit 1), the forwarded line reads `C9 leak [redacted] [redacted]`. Neither value appears in stdout or stderr.
  - It is red at `a8c03fae`, both subtests, with the values in the output (validation R2.1), and green after.
  - `test_regime_ci_keeps_tokens_out_of_argv_and_output` stays green.
- **The run:** the module gives `Ran 20 tests`, `OK`, and ruff is clean (R2.3).
- **Caps from `f7f38067`:** 15 of 25 outside `tests/` and `.orchestration/`, and 58 of 60 under `tests/`.
- **Unchanged:** the task copy stays at `d4798ebf…` (no amendment). The P3 on the "public repository contents" wording in task.md is advisory and owned by `dotfiles-T133-regime-ci-token-followup-a01`.

### The lint dispositions after CI on 26b4a28c (the orchestrator's decision b-prime)

- **Why:** round 2 made `regime-ci.py` a changed file, so the changed-file comparison lint failed in CI on five hits that pre-date this task. Main has no baseline rows for the file. They were reported as blocked PONG 2922, and the decision was to mark each line with the documented inline marker and its reason, with no baseline edit and no behaviour change. Commit `8a1b16f3`:
  - `regime-ci.py:66` (R6): `# lint-comparisons: allow name is the literal precheck or task_copy`. `token()`'s only callers pass those two literals (lines 138–198).
  - `:72` (R4): `# lint-comparisons: allow glob-syntax test on an allowed_files entry, not a path`.
  - `:73` (R4): `# lint-comparisons: allow git-listed relative path vs the entry dir prefix`. The paths come from `git diff --name-only`.
  - `:91` (R4): `# lint-comparisons: allow git numstat repository-relative paths against the task text's literal cap prefixes  # fmt: skip`.
  - `:254` (R4): `# lint-comparisons: allow git-listed repository-relative paths against the literal .orchestration/ prefix  # fmt: skip`.
- **The two `# fmt: skip`:** lines 91 and 254 are 92 and 75 columns before the marker, so no concrete reason fits within ruff's 120 columns. Without the skip, ruff would split the statement and move the marker off the flagged line, where the lint does not read it. The skip keeps the layout; the code is unchanged.
- **The checks:** the lint on the file exits 0, the changed-file lint test is OK, the module passes, and ruff is clean (validation R2.4).
- **Caps:** 25 of 25 outside `tests/` and `.orchestration/`, exactly at the cap, and 58 of 60 under `tests/`.

