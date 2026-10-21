---
format: 2
task_id: dotfiles-T133-regime-ci-token-a01
kind: code
security: true
allowed_files:
  - .github/workflows/regime.yml
  - scripts/orchestrator/regime-ci.py
  - tests/unit/test_regime_ci.py
  - .orchestration/dotfiles-T133-regime-ci-token-a01/**
after: []
threat_table:
  - {control: ".github/workflows/regime.yml", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_the_regime_workflow_runs_base_code_only"}
  - {control: "scripts/orchestrator/regime-ci.py", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_child_sees_parent_tokens"}
  - {control: "tests/unit/test_regime_ci.py", disposition: "residual: Final-head CI and the independent task audit compare fixture assertions with production behavior; tests supply no approval authority."}
  - {control: ".orchestration/dotfiles-T133-regime-ci-token-a01/**", disposition: "residual: These untrusted artifacts contain only this task's copy and evidence; no executable helper or credential is stored here."}
  - {control: "the task copy .orchestration/dotfiles-T133-regime-ci-token-a01/task.md", disposition: "residual: The orchestrator compares every byte and SHA256 with the dispatched text before acceptance."}
  - {control: "the evidence records under .orchestration/dotfiles-T133-regime-ci-token-a01/**", disposition: "residual: The audit compares reported commands, red/green outcomes, cap totals and CI with the final head; token values are excluded from evidence."}
  - {control: "task metadata (kind, security, allowed_files, after, threat_table, premises)", disposition: "residual: The consistency checker validates the front matter before dispatch and acceptance; whole-file comparison detects changed metadata."}
  - {control: "metadata separators", disposition: "residual: YAML parsing and the dispatched whole-file digest cover separators in the task copy; evidence remains untrusted data."}
  - {control: "in-process effects", disposition: "closed: tests/unit/test_regime_ci.py::RegimeCiTest::test_regime_ci_keeps_tokens_out_of_argv_and_output"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: the workflow sets GH_TOKEN for its own step; regime-ci.py inherits that environment unchanged (no allowlist, as at f7f38067) and the interpreter and uv come from PATH as before; the token-presence and no-token-in-argv-or-output tests close only those two facts; the rest is owned by dotfiles-T133-regime-ci-token-followup-a01."}
  - {control: "regime-ci CHECKER_RUN executable selection of uv and python", disposition: "residual: Executable selection, including PATH and virtual-environment discovery, is outside this task and owned by dotfiles-T133-regime-ci-token-followup-a01."}
  - {control: "GH_TOKEN and GITHUB_TOKEN authority", disposition: "residual: The workflow's GITHUB_TOKEN under permissions: contents: read can read public repository contents only. A token supplied by any other caller carries that caller's authority; this task neither widens nor narrows it. The checker forwards, never mints, tokens."}
  - {control: "new or renamed scripts", disposition: "residual: No script is added or renamed; retain the existing verifier, checker command and isolated interpreter setup."}
  - {control: "orchestrator effect merge", disposition: "residual: Only the orchestrator integrates under Playbook step 10, binding the merge to the audited full head after the gate; the worker never merges."}
  - {control: "orchestrator effect update-branch", disposition: "residual: A changed head requires fresh applicable CI, feedback and audit evidence under Playbook step 10 before integration."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: None planned; removal refuses dirty state without force, and the orchestrator records any discarded state in acceptance."}
  - {control: "5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: This token handoff establishes neither same-UID isolation nor separation of worker and orchestrator GitHub credentials."}
  - {control: "5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: This Claude seat uses its deployed sandbox; this slice changes no host boundary or managed settings and proves no deployment isolation."}
  - {control: "5.14 item 2: 無害化した環境を最初に", disposition: "residual: this task adds no environment allowlist; the checker child inherits regime-ci's environment as at f7f38067, and existing parent execution and PATH selection remain unchanged and are not claimed sanitized (owner dotfiles-T133-regime-ci-token-followup-a01)."}
  - {control: "5.14 item 3: 信頼パスの境界検査", disposition: "residual: Existing base-checkout and trusted-path checks remain unchanged; this task adds no protection against concurrent same-UID replacement."}
  - {control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: regime-ci's git reads inherit GIT_DIR; dotfiles-T133-regime-ci-token-followup-a01 owns binding those reads to the checker execution tree."}
  - {control: "5.14 item 5: 出力と予約の同一性", disposition: "residual: Evidence and RESULT identify the full head; this change adds no lock, reservation or physical execution slot."}
  - {control: "5.14 item 6: 正直な残余", disposition: "residual: Report fixture observations separately from hosted-runner evidence; parent startup, shared caches and same-UID access remain residual risks."}
  - {control: "5.14 item 7: 検証", disposition: "residual: Named red/green tests cover this handoff; retain existing security regressions and disclose unexecuted checks without claiming full contract closure."}
  - {control: "5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: The unchanged checker owns canonical-main API reads; token availability supplies authentication, never approval authority from local records."}
  - {control: "5.14 item 9: 私設キャッシュ", disposition: "residual: Preserve existing UV_CACHE_DIR handling and no-config isolated execution; this task neither provisions nor authenticates a private cache."}
  - {control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Claude worker seats run inside their sandbox except the manifest's remaining excludedCommands: agmsg-dispatch *; on Linux also gh *, herdr-agents * and actas-claim.sh *. dotfiles-T133-worker-sandbox-exclusions-a02 owns their removal under design 5.14 item 10. This task's git, uv, python and ruff commands are not excluded and run inside the sandbox; the deployed settings keep `failIfUnavailable: false`, so a missing sandbox dependency would run them unsandboxed, a residual of the Claude settings owned by design 5.14 item 10's lineage; a refusal is reported as AGMSG-PONG v1 status=blocked."}
premises:
  - claim: The reviewed checker head resolves locally; this identifies the review input, not canonical GitHub authority.
    command: |-
      git rev-parse 2cb58482
    output: |-
      2cb584823ccf5f22069ea925b252d8cefb020844
  - claim: The current workflow already declares read-only contents permission.
    command: |-
      grep -c 'contents: read' .github/workflows/regime.yml
    output: |-
      1
  - claim: The existing uv-configuration regression test is present.
    command: |-
      grep -c test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config tests/unit/test_regime_ci.py
    output: |-
      1
---

# AGMSG-TASK dotfiles-T133-regime-ci-token-a01 — authenticate the regime checker's read-only API requests

Amendment 1 addresses C-80 round 1 (`text-security:c32513e:1-5`); previous_sha256: c32513e5cbf65661a7a5d2f385dd814f6735d9ddaa1495b03da47db2f9c71335.

Operator premise: PR #440, head 2cb58482, lineage dotfiles-T133-task-generator-plan-check-a06-checker, is merging next; its checker forwards parent GH_TOKEN/GITHUB_TOKEN only to gh api, including canonical-main SHA, C6/C15 design bytes and C8/C9 lookups. A fresh hosted runner has no gh login: missing authentication exits 4 and regime-ci reports no verdict. The local review found this P1 caller defect outside #440's allowed_files; fix it before regime becomes a required check.

Design 5.14 (.orchestration/plans/024-design-quality.md), frozen by D-024-29, applies by reference under D-024-30; rely on items 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 and 10.

## Item 1

Add `GH_TOKEN: ${{ github.token }}` to the regime-ci step's env in .github/workflows/regime.yml; retain `permissions: {contents: read}` and base-only execution. This workflow edit is authorized because the workflow is this task's subject; do not activate a ruleset or widen permissions.

In `.github/workflows/regime.yml` the regime-ci step sets `GH_TOKEN: ${{ github.token }}` (the job's `permissions` block declares `contents: read`; the token reads public repository contents only). `scripts/orchestrator/regime-ci.py` keeps the checker's inherited environment as it is at f7f38067 (`checker()` calls `subprocess.run` with no `env=`, so the child already sees every variable of regime-ci's environment, GH_TOKEN included once the workflow sets it); this task introduces no environment allowlist. It adds tests in `tests/unit/test_regime_ci.py`: the checker child's environment holds `GH_TOKEN` exactly when regime-ci's own environment holds it and lacks it otherwise, and no token value appears in the child's argv or in regime-ci's stdout or stderr (the fake checker records its argv and environment to a file the test reads). Amendment 1 (`previous_sha256: 61a9942b4e74bc53129a733761bb192eec875fddbd91be458243c530f448405b`): the first text assumed a minimal environment that regime-ci.py never had, measured by the worker at f7f38067 (`git log --all -S UV_CACHE_DIR -- scripts/orchestrator/regime-ci.py` empty); the sentence above replaces that premise, and the module command passes the sandbox proxy variables through.

In tests/unit/test_regime_ci.py add RegimeCiTest.test_regime_ci_child_sees_parent_tokens: with both ambient token keys cleared, exercise neither, each alone and both with synthetic values, and assert that the checker child's environment holds exactly the tokens regime-ci's environment holds and still holds regime-ci's other variables (inheritance, no exclusion: the child environment is the parent's). Add RegimeCiTest.test_regime_ci_keeps_tokens_out_of_argv_and_output: the fake checker records its argv and the test asserts no token value appears in argv, stdout or stderr. Add RegimeCiTest.test_regime_yml_sets_the_token: the workflow's regime-ci step carries `GH_TOKEN: ${{ github.token }}` and the job's permissions block declares `contents: read`.

Update test_the_regime_workflow_runs_base_code_only's exact env assertion for the new token entry while retaining its permissions and base-only checks. Keep test_regime_ci_runs_the_checker_without_the_checkout_s_uv_config green and unittest.main() at the module end. Write and run tests before implementation: every new behavior must be red before its production change and green after; name each outcome in report.md and distinguish existing passing regressions.

## Check

Measured deployment for Worker Playbook step 4: Claude worker seats run inside their sandbox except the commands the manifest's excludedCommands still lists: `agmsg-dispatch *`, and on Linux `gh *`, `herdr-agents *`, `actas-claim.sh *`. Design 5.14 item 10's own task, dotfiles-T133-worker-sandbox-exclusions-a02, removes these exclusions. This task's git, uv, python and ruff commands are not excluded and run inside the sandbox. Record a refusal in sandbox.md and send `AGMSG-PONG v1 status=blocked` with the command and boundary; never retry outside.

Resolve uv once with `UV_DIR="$(dirname "$(env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv)")"` and paste the command and its output into report.md. The result is the absolute, non-shim directory that holds the uv binary mise installed (on this host `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/`); do not assume a `bin` subdirectory and read no pin file: the version is whatever mise resolves for this checkout, and the pasted path is the evidence.

Run before implementation and after: `/usr/bin/env -i PATH="$UV_DIR:/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_regime_ci.py`, substituting the pinned version and using that same resolved absolute uv directory for both runs.

Run `ruff check --config ruff.toml scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py` and `ruff format --config ruff.toml --check scripts/orchestrator/regime-ci.py tests/unit/test_regime_ci.py`. Paste commands, exit statuses and verbatim output without credential values into validation.md. Caps: at most 25 changed lines outside `tests/` and `.orchestration/`, and at most 60 under `tests/`.

Measure summed additions plus deletions with `git diff --numstat <base40>...<head40>`; base40 is pasted at dispatch and head40 comes from RESULT. This whole task text, including the orchestrator's Checks block, stays at or under 125 lines.

Do not run Bats locally. After the final push verify GitHub Actions for the exact final head with `gh pr checks <pr> --repo mryfmo/dotfiles --watch`, fix in-scope failures and repeat before RESULT; follow Worker Playbook step 15 for the bounded Bot wait and findings. Before completion run `make require-crit-review`; if required, follow AGENTS.md's crit-data evidence and receipt procedure with worker evidence under this task's allowed directory, without a browser review.

## Completion

Fetch current origin/main inside the sandbox and create a fresh branch with `git switch -c ci/regime-ci-token-a01 --no-track origin/main`. Save .orchestration/dotfiles-T133-regime-ci-token-a01/task.md byte-identical to the dispatched text. Under that directory commit report.md (implementation, named red/green outcomes, residuals, cost), validation.md (commands/output and both cap totals), sandbox.md, learning.md and autoskill.md (used or not-used); do not commit plan/todo/learn worklogs. Add no runtime helpers or changes outside allowed_files.

Push with `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u https://github.com/mryfmo/dotfiles.git <branch>` and open with `gh pr create --repo mryfmo/dotfiles` using an English title and body.

After final-head checks pass, send `AGMSG-RESULT v1 task_id=dotfiles-T133-regime-ci-token-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with artifact paths; no worker merge. Report skipped checks and remaining risks, including unchanged parent startup and cache behavior.

## Checks (pasted by the orchestrator before each send)

```
pre-send (author lines; C-80 rounds 1-3 incorrect -> amendments; round 4 correct at 2c8c05a5):
dotfiles-T133-regime-ci-token-a01.md: OK
secret-pattern: 0 match(es)
lines: 102 (self cap: 125)
sha256: 2c8c05a5d60867ccb9351b3359d64544f66785866e779a0199721158bdc0b4f2
```

Author verification: Implementation, tests and live sandbox behavior were not checked for this text-only amendment; executable selection, GIT_DIR inheritance and sandbox exclusions remain with their named follow-ups.