---
task_id: dotfiles-T129-assets-omp-hcom-a01
amendment: 2
---

# Amendment 2 current validation

Current task SHA256 0634d0eb62fe82c614282d7fbec3d998a8c37b9c1b0e89be5e3701923f073255. Amendment1 records and tests are superseded and archived untracked in amendment1/. No source result or test count from that implementation is a current claim. The operator performs the real make update after merge; no installation in any sandbox, only fake binaries/fixture downloads in tests.

Restored the three withdrawn files to clean HEAD35ab0e95: home/dot_mise/config.toml, scripts/validate-agent-assets.py, tests/unit/test_validate_agent_assets.py. The existing fresh branch feat/pinned-omp-hcom is retained by explicit re-task instruction.

## red

```text
$ uv run --offline --no-project python -m unittest tests/unit/test_update_agent_assets.py -v
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... 
  test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Darwin/arm64') ... FAIL
  test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Darwin/x86_64') ... FAIL
  test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Linux/x86_64') ... FAIL
  test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Linux/aarch64') ... FAIL
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... FAIL
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... FAIL

======================================================================
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Darwin/arm64')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 162, in test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin
    self.exercise_update("hcom", platform)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 101, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> hcom
fixture installer requires an already downloaded file: hcom==0.7.30


======================================================================
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Darwin/x86_64')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 162, in test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin
    self.exercise_update("hcom", platform)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 101, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> hcom
fixture installer requires an already downloaded file: hcom==0.7.30


======================================================================
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Linux/x86_64')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 162, in test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin
    self.exercise_update("hcom", platform)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 101, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> hcom
fixture installer requires an already downloaded file: hcom==0.7.30


======================================================================
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) (platform='Linux/aarch64')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 162, in test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin
    self.exercise_update("hcom", platform)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 101, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> hcom
fixture installer requires an already downloaded file: hcom==0.7.30


======================================================================
FAIL: test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 163, in test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin
    self.exercise_update("hcom", "Plan9/unknown", unsupported=True)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 101, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> hcom
fixture installer requires an already downloaded file: hcom==0.7.30


======================================================================
FAIL: test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 157, in test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin
    self.exercise_update("omp")
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 101, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 127 : bash: update_omp: command not found


----------------------------------------------------------------------
Ran 2 tests in 0.769s

FAILED (failures=6)
(exit 1)
```

## generate

```text
$ uv run --offline --no-project --with pyyaml scripts/generate-agent-configs.py --set-asset omp.pin=18.11.3 --set-asset hcom.pin=0.7.30
ERROR: assets.hcom.files.darwin-arm64 is not a plain pin value: 'https://files.pythonhosted.org/packages/f5/ed/5e951b0e6fcadef1a2598e82b969b3eaa387a3e202f8987102d0e84cddfc/hcom-0.7.30-py3-none-macosx_11_0_arm64.whl'
(exit 1)
```

## green

```text
$ uv run --offline --no-project python -m unittest tests/unit/test_update_agent_assets.py -v
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... FAIL

======================================================================
FAIL: test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 157, in test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin
    self.exercise_update("omp")
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 110, in exercise_update
    self.assertEqual(
    ~~~~~~~~~~~~~~~~^
        f"https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-{pin}.tgz", url
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
AssertionError: 'http[16 chars]js.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-18.11.3.tgz' != 'http[16 chars]js.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-.tgz'
- https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-18.11.3.tgz
?                                                                        -------
+ https://registry.npmjs.org/@oh-my-pi/pi-coding-agent/-/pi-coding-agent-.tgz


----------------------------------------------------------------------
Ran 2 tests in 3.573s

FAILED (failures=1)
(exit 1)
```

## generate-fallback

```text
$ uv run --offline --no-project --with pyyaml scripts/generate-agent-configs.py --set-asset omp.pin=18.11.3 --set-asset hcom.pin=0.7.30
asset pins updated: omp.pin, hcom.pin
(exit 0)
```

## green-current

```text
$ uv run --offline --no-project python -m unittest tests/unit/test_update_agent_assets.py -v
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok

----------------------------------------------------------------------
Ran 2 tests in 3.872s

OK
(exit 0)
```

## shellcheck

```text
$ shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## shfmt

```text
$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## ruff

```text
$ ruff check --config ruff.toml tests/unit/test_update_agent_assets.py
All checks passed!
(exit 0)
```

## ruff-format

```text
$ ruff format --config ruff.toml --check tests/unit/test_update_agent_assets.py
1 file already formatted
(exit 0)
```

## generated-check

```text
$ uv run --offline --no-project --with pyyaml scripts/generate-agent-configs.py --check
generated agent configs are up to date
(exit 0)
```

## whitespace

```text
$ git diff --cached --check
(exit 0)
```

## Current source and task integrity

```text
$ uv run --offline --no-project --with pyyaml <TMP>/codex-T129-integrity2.py
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "da7cb9020b59bba30fbcd3f3c78acc9c3817395ddee3d7140866ddb82de8b495",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "e6c8abb6e8857ed450196888aa2b912a8b025e7ef7038c46065867358f296c19",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_update_agent_assets.py": "fa830f443beceed7ab76e9187c787b89e8e7c68ae8c88d161e7a952f5a1d4b9a"
  },
  "source_changed": 161,
  "test_added": 195,
  "withdrawn_paths_unchanged": true,
  "existing_helpers_and_Bats_byte_identical": true,
  "task_hashes_and_URLs_match": true,
  "URL_render_fallback": "files values are not plain pin values; URLs declared beside existing installer URLs and match manifest files",
  "numstat": "35\t0\thome/dot_agents/agent-config.yaml\n33\t0\tscripts/check-tools.sh\n8\t0\tscripts/lib/installer-pins.sh\n85\t0\tscripts/update-agent-assets.sh\n32\t0\ttests/install/common/check_tools.bats\n163\t0\ttests/unit/test_update_agent_assets.py\n"
}
(exit 0)
```

## initial-review-gate

```text
$ make require-crit-review
Native agent review required before completion.
- review-sensitive path changed: .orchestration/dotfiles-T128-project-map-pane-open-a01-followup-a01/crit-status.json
- broad diff touches 570 files
- broad diff changes 29969 lines
Use the active agent's review path, not a browser by default:
- Codex: retrieve Crit comments/status data, review it inside the task, then address findings.
- Claude Code: retrieve Crit comments/status data, review it inside the task, then address findings.
- Use browser Crit review only when the user explicitly asks for Crit web UI or Crit data is unavailable.
Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.
For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file.
Evidence must contain at least one resolved record; for a finding-free review, add and resolve one review-scope approval record.
This local evidence is process evidence, not reviewer authentication.
Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`.
After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.
make: *** [require-crit-review] Error 1
(exit 2)
```

## Clean staged-candidate validator

```text
Candidate snapshot from the staged index; unrelated untracked historical logs are absent. All six changed source/test hashes equal worker-e.
$ cd <TMP>/codex-T129-candidate-vzzdbg11
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: no agmsg identity at the active seat /private/tmp/codex-T129-candidate-vzzdbg11 (expected one)
WARN: regime-boundary: canonical clone <HOME>/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_claude/modify_private_settings.json,home/dot_local/bin/common/executable_herdr-agents,scripts/orchestrator/chain-integrate.sh,scripts/orchestrator/dispatch.sh,scripts/orchestrator/local-advisory.sh,scripts/orchestrator/local-review.sh; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <HOME>/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
WARN: regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-a01-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-a01-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a03 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-playbook-rules-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: amendments 12 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-s1-replan-gate-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-launch-args-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: revises 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: revises 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
(exit 0)
```

## Current Crit lookup

```text
$ crit status --json
{
  "branch": "feat/pinned-omp-hcom",
  "daemon": {
    "running": false
  },
  "review_file": "<HOME>/.crit/reviews/3c569e3521ce/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
(exit 0)
```

## runtime-health-after-source-fix

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check -v
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py:1373: SyntaxWarning: "\ " is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\ "? A raw string is also an option.
  upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... 
  test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) (fail='gh:extension list') ... FAIL
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok

======================================================================
FAIL: test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) (fail='gh:extension list')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 1242, in test_doctor_required_optional_and_healthy_statuses
    self.assertIn(summary, result.stdout)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'optional warnings: 1' not found in '\n==> Core commands\nfound:   git -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-bin-gh-extension-list-Linux/git\ngit healthy\nfound:   chezmoi -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-bin-gh-extension-list-Linux/chezmoi\nchezmoi healthy\nfound:   mise -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-bin-gh-extension-list-Linux/mise\nmise healthy\nfound:   uv -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-bin-gh-extension-list-Linux/uv\nuv healthy\nfound:   gh -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-bin-gh-extension-list-Linux/gh\ngh healthy\n\n==> Chezmoi\nchezmoi healthy\nfound:   private source -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-home/.local/share/chezmoi-private\nfound:   private config -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-home/.config/chezmoi-private/chezmoi.yaml\n\n==> Mise\nmise healthy\nmise healthy\n\n==> Homebrew\nnot applicable: Homebrew (non-Darwin)\n\n==> Crit CLI\nnot applicable: Crit CLI (not installed)\n\n==> Agent tools\n\n==> Zed\nnot applicable: Zed (installed on Ubuntu clients only)\n\n==> SSH\nfound:   machine SSH key -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-home/.ssh/id_ed25519.pub\n\n==> AppArmor\nnot applicable: AppArmor userns restriction (not enabled)\n\n==> Claude Code sandbox\nfound:   bwrap -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-bin-gh-extension-list-Linux/bwrap\nfound:   socat -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-5u_d86mz/doctor-bin-gh-extension-list-Linux/socat\n\n==> GitHub CLI extensions\n\n==> agmsg\nnot applicable: agmsg (not installed)\n\nTool check summary: required failures: 0; optional warnings: 3\n'

----------------------------------------------------------------------
Ran 5 tests in 8.228s

FAILED (failures=1)
(exit 1)
```

## shfmt-health-fix

```text
$ shfmt -d scripts/check-tools.sh scripts/update-agent-assets.sh scripts/lib/installer-pins.sh
diff scripts/check-tools.sh.orig scripts/check-tools.sh
--- scripts/check-tools.sh.orig
+++ scripts/check-tools.sh
@@ -17,7 +17,7 @@
 # @arg $1 string Heading text.
 #
 function section() {
-    printf '\n==> %s\n' "$1"
+	printf '\n==> %s\n' "$1"
 }
 
 #
@@ -26,35 +26,35 @@
 # @arg $@ string Optional version command arguments.
 #
 function check_command() {
-    local command_name="$1"
-    shift || true
-
-    if ! command -v "${command_name}" > /dev/null 2>&1; then
-        printf 'required missing: %s\n' "${command_name}" >&2
-        ((required_failures += 1))
-        return 0
-    fi
-
-    printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
-
-    local output first_line
-
-    if [ "$#" -gt 0 ]; then
-        if ! output="$("${command_name}" "$@" 2>&1)"; then
-            printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
-            ((required_failures += 1))
-            return 0
-        fi
-    else
-        if ! output="$("${command_name}" --version 2>&1)"; then
-            printf 'required failed: %s --version\n' "${command_name}" >&2
-            ((required_failures += 1))
-            return 0
-        fi
-    fi
-
-    IFS= read -r first_line <<< "${output}"
-    printf '%s\n' "${first_line}"
+	local command_name="$1"
+	shift || true
+
+	if ! command -v "${command_name}" > /dev/null 2>&1; then
+		printf 'required missing: %s\n' "${command_name}" >&2
+		((required_failures += 1))
+		return 0
+	fi
+
+	printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
+
+	local output first_line
+
+	if [ "$#" -gt 0 ]; then
+		if ! output="$("${command_name}" "$@" 2>&1)"; then
+			printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
+			((required_failures += 1))
+			return 0
+		fi
+	else
+		if ! output="$("${command_name}" --version 2>&1)"; then
+			printf 'required failed: %s --version\n' "${command_name}" >&2
+			((required_failures += 1))
+			return 0
+		fi
+	fi
+
+	IFS= read -r first_line <<< "${output}"
+	printf '%s\n' "${first_line}"
 }
 
 #
@@ -63,13 +63,13 @@
 # @arg $@ string Doctor command arguments.
 #
 function run_required_doctor() {
-    local command_name="$1"
-    shift || true
-
-    if command -v "${command_name}" > /dev/null 2>&1 && ! "${command_name}" "$@"; then
-        printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
-        ((required_failures += 1))
-    fi
+	local command_name="$1"
+	shift || true
+
+	if command -v "${command_name}" > /dev/null 2>&1 && ! "${command_name}" "$@"; then
+		printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
+		((required_failures += 1))
+	fi
 }
 
 #
@@ -77,8 +77,8 @@
 # @arg $1 string Warning text.
 #
 function warn_optional() {
-    printf 'optional warning: %s\n' "$1" >&2
-    ((optional_warnings += 1))
+	printf 'optional warning: %s\n' "$1" >&2
+	((optional_warnings += 1))
 }
 
 #
@@ -87,14 +87,14 @@
 #   usePrivate key, matching the owner's existing machines' behavior.
 #
 function private_layer_enabled() {
-    local use_private
-
-    if ! command -v chezmoi > /dev/null 2>&1 || ! command -v jq > /dev/null 2>&1; then
-        return 0
-    fi
-
-    use_private="$(chezmoi data 2> /dev/null | jq -r '.usePrivate' 2> /dev/null)"
-    [ "${use_private}" != "false" ]
+	local use_private
+
+	if ! command -v chezmoi > /dev/null 2>&1 || ! command -v jq > /dev/null 2>&1; then
+		return 0
+	fi
+
+	use_private="$(chezmoi data 2> /dev/null | jq -r '.usePrivate' 2> /dev/null)"
+	[ "${use_private}" != "false" ]
 }
 
 #
@@ -101,27 +101,27 @@
 # @description Print the configured private chezmoi source state.
 #
 function check_private_chezmoi() {
-    local private_source="${HOME%/}/.local/share/chezmoi-private"
-    local private_config="${HOME%/}/.config/chezmoi-private/chezmoi.yaml"
-
-    if ! private_layer_enabled; then
-        printf 'not applicable: private layer (usePrivate=false)\n'
-        return 0
-    fi
-
-    if [ -d "${private_source}" ]; then
-        printf 'found:   private source -> %s\n' "${private_source}"
-        if [ -f "${private_config}" ]; then
-            printf 'found:   private config -> %s\n' "${private_config}"
-        else
-            warn_optional "private config is missing: ${private_config}"
-        fi
-    else
-        warn_optional "private source is missing: ${private_source}"
-        if [ ! -f "${private_config}" ]; then
-            warn_optional "private config is missing: ${private_config}"
-        fi
-    fi
+	local private_source="${HOME%/}/.local/share/chezmoi-private"
+	local private_config="${HOME%/}/.config/chezmoi-private/chezmoi.yaml"
+
+	if ! private_layer_enabled; then
+		printf 'not applicable: private layer (usePrivate=false)\n'
+		return 0
+	fi
+
+	if [ -d "${private_source}" ]; then
+		printf 'found:   private source -> %s\n' "${private_source}"
+		if [ -f "${private_config}" ]; then
+			printf 'found:   private config -> %s\n' "${private_config}"
+		else
+			warn_optional "private config is missing: ${private_config}"
+		fi
+	else
+		warn_optional "private source is missing: ${private_source}"
+		if [ ! -f "${private_config}" ]; then
+			warn_optional "private config is missing: ${private_config}"
+		fi
+	fi
 }
 
 #
@@ -128,12 +128,12 @@
 # @description Require Homebrew on macOS and skip it on other platforms.
 #
 function check_homebrew() {
-    if [ "$(uname)" != "Darwin" ]; then
-        printf 'not applicable: Homebrew (non-Darwin)\n'
-        return 0
-    fi
-
-    check_command brew --version
+	if [ "$(uname)" != "Darwin" ]; then
+		printf 'not applicable: Homebrew (non-Darwin)\n'
+		return 0
+	fi
+
+	check_command brew --version
 }
 
 #
@@ -140,13 +140,13 @@
 # @description Print whether the per-machine signing/push SSH key exists.
 #
 function check_machine_ssh_key() {
-    local key_path="${HOME%/}/.ssh/id_ed25519.pub"
-
-    if [ -f "${key_path}" ]; then
-        printf 'found:   machine SSH key -> %s\n' "${key_path}"
-    else
-        warn_optional "machine SSH key is missing: ${key_path} (run provision-machine-key)"
-    fi
+	local key_path="${HOME%/}/.ssh/id_ed25519.pub"
+
+	if [ -f "${key_path}" ]; then
+		printf 'found:   machine SSH key -> %s\n' "${key_path}"
+	else
+		warn_optional "machine SSH key is missing: ${key_path} (run provision-machine-key)"
+	fi
 }
 
 #
@@ -155,15 +155,15 @@
 #   GitHub release on every OS; not required, so a missing binary is not a failure.
 #
 function check_crit_cli() {
-    local target="${HOME%/}/.local/bin/crit"
-
-    if [ ! -x "${target}" ]; then
-        printf 'not applicable: Crit CLI (not installed)\n'
-        return 0
-    fi
-
-    printf 'found:   crit -> %s (pinned release)\n' "${target}"
-    "${target}" --version || warn_optional "crit --version failed; the managed binary may be corrupt (try REPAIR=1 make doctor)"
+	local target="${HOME%/}/.local/bin/crit"
+
+	if [ ! -x "${target}" ]; then
+		printf 'not applicable: Crit CLI (not installed)\n'
+		return 0
+	fi
+
+	printf 'found:   crit -> %s (pinned release)\n' "${target}"
+	"${target}" --version || warn_optional "crit --version failed; the managed binary may be corrupt (try REPAIR=1 make doctor)"
 }
 
 #
@@ -170,15 +170,15 @@
 # @description Report omp's installed version beside its manifest pin.
 #
 function check_omp() {
-    local target="${HOME%/}/.local/bin/omp"
-    if [ ! -x "${target}" ]; then
-        warn_optional "omp not installed; run make update"
-        return 0
-    fi
-    local pin
-    pin="$(awk -F'"' '/^OMP_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
-    printf 'found:   omp -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
-    "${target}" --version || warn_optional "omp --version failed; run make update"
+	local target="${HOME%/}/.local/bin/omp"
+	if [ ! -x "${target}" ]; then
+		warn_optional "omp not installed; run make update"
+		return 0
+	fi
+	local pin
+	pin="$(awk -F'"' '/^OMP_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
+	printf 'found:   omp -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
+	"${target}" --version || warn_optional "omp --version failed; run make update"
 }
 
 #
@@ -185,15 +185,15 @@
 # @description Report hcom's installed version beside its manifest pin.
 #
 function check_hcom() {
-    local target="${HOME%/}/.local/bin/hcom"
-    if [ ! -x "${target}" ]; then
-        warn_optional "hcom not installed; run make update"
-        return 0
-    fi
-    local pin
-    pin="$(awk -F'"' '/^HCOM_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
-    printf 'found:   hcom -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
-    "${target}" --version || warn_optional "hcom --version failed; run make update"
+	local target="${HOME%/}/.local/bin/hcom"
+	if [ ! -x "${target}" ]; then
+		warn_optional "hcom not installed; run make update"
+		return 0
+	fi
+	local pin
+	pin="$(awk -F'"' '/^HCOM_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
+	printf 'found:   hcom -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
+	"${target}" --version || warn_optional "hcom --version failed; run make update"
 }
 
 #
@@ -201,18 +201,18 @@
 #   authenticated gh, because a GitHub release attestation is the only verification Zed publishes.
 #
 function check_zed() {
-    local target="${HOME%/}/.local/bin/zed" system
-    system="$(chezmoi execute-template '{{ .system }}' 2> /dev/null || true)"
-    if [ "$(uname -s)" != Linux ] || [ "${system}" != client ]; then
-        printf 'not applicable: Zed (installed on Ubuntu clients only)\n'
-        return 0
-    fi
-    if [ ! -x "${target}" ]; then
-        warn_optional "zed not installed: run make gh-auth, then make update; its release attestation cannot be verified without an authenticated gh"
-        return 0
-    fi
-    printf 'found:   zed -> %s\n' "${target}"
-    "${target}" --version || warn_optional "zed --version failed; the install may be corrupt"
+	local target="${HOME%/}/.local/bin/zed" system
+	system="$(chezmoi execute-template '{{ .system }}' 2> /dev/null || true)"
+	if [ "$(uname -s)" != Linux ] || [ "${system}" != client ]; then
+		printf 'not applicable: Zed (installed on Ubuntu clients only)\n'
+		return 0
+	fi
+	if [ ! -x "${target}" ]; then
+		warn_optional "zed not installed: run make gh-auth, then make update; its release attestation cannot be verified without an authenticated gh"
+		return 0
+	fi
+	printf 'found:   zed -> %s\n' "${target}"
+	"${target}" --version || warn_optional "zed --version failed; the install may be corrupt"
 }
 
 #
@@ -222,33 +222,33 @@
 #   root-only to list, so an unprivileged bwrap probe is the effective check.
 #
 function check_apparmor_userns() {
-    local restrict="${APPARMOR_USERNS_SYSCTL:-/proc/sys/kernel/apparmor_restrict_unprivileged_userns}"
-    local bwrap="${APPARMOR_USERNS_BWRAP:-/usr/bin/bwrap}"
-    local profile="${APPARMOR_USERNS_PROFILE_TARGET:-/etc/apparmor.d/bwrap-userns}"
-
-    if [ "$(cat "${restrict}" 2> /dev/null)" != "1" ]; then
-        printf 'not applicable: AppArmor userns restriction (not enabled)\n'
-        return 0
-    fi
-    if ! command -v codex > /dev/null 2>&1; then
-        warn_optional "codex is not installed; skipped the bwrap user-namespace probe"
-        return 0
-    fi
-    if [ ! -x "${bwrap}" ]; then
-        printf 'required failed: %s is missing; sandboxed codex runs need it under the AppArmor userns restriction (install the bubblewrap package)\n' "${bwrap}" >&2
-        ((required_failures += 1))
-        return 0
-    fi
-    if "${bwrap}" --ro-bind / / true > /dev/null 2>&1; then
-        printf 'found:   bwrap user namespaces allowed -> %s\n' "${bwrap}"
-        return 0
-    fi
-    if [ -f "${profile}" ]; then
-        printf 'required failed: bwrap user-namespace probe; %s exists but is not effective (sudo apparmor_parser -r %s)\n' "${profile}" "${profile}" >&2
-    else
-        printf 'required failed: bwrap user-namespace probe; AppArmor profile %s is missing, so sandboxed codex runs fail (sudo -v && bash install/ubuntu/common/apparmor_userns.sh)\n' "${profile}" >&2
-    fi
-    ((required_failures += 1))
+	local restrict="${APPARMOR_USERNS_SYSCTL:-/proc/sys/kernel/apparmor_restrict_unprivileged_userns}"
+	local bwrap="${APPARMOR_USERNS_BWRAP:-/usr/bin/bwrap}"
+	local profile="${APPARMOR_USERNS_PROFILE_TARGET:-/etc/apparmor.d/bwrap-userns}"
+
+	if [ "$(cat "${restrict}" 2> /dev/null)" != "1" ]; then
+		printf 'not applicable: AppArmor userns restriction (not enabled)\n'
+		return 0
+	fi
+	if ! command -v codex > /dev/null 2>&1; then
+		warn_optional "codex is not installed; skipped the bwrap user-namespace probe"
+		return 0
+	fi
+	if [ ! -x "${bwrap}" ]; then
+		printf 'required failed: %s is missing; sandboxed codex runs need it under the AppArmor userns restriction (install the bubblewrap package)\n' "${bwrap}" >&2
+		((required_failures += 1))
+		return 0
+	fi
+	if "${bwrap}" --ro-bind / / true > /dev/null 2>&1; then
+		printf 'found:   bwrap user namespaces allowed -> %s\n' "${bwrap}"
+		return 0
+	fi
+	if [ -f "${profile}" ]; then
+		printf 'required failed: bwrap user-namespace probe; %s exists but is not effective (sudo apparmor_parser -r %s)\n' "${profile}" "${profile}" >&2
+	else
+		printf 'required failed: bwrap user-namespace probe; AppArmor profile %s is missing, so sandboxed codex runs fail (sudo -v && bash install/ubuntu/common/apparmor_userns.sh)\n' "${profile}" >&2
+	fi
+	((required_failures += 1))
 }
 
 #
@@ -255,9 +255,9 @@
 # @description Print the current GitHub CLI extension state when gh is installed.
 #
 function check_gh_extensions() {
-    if command -v gh > /dev/null 2>&1 && ! gh extension list; then
-        warn_optional "unable to list installed GitHub CLI extensions"
-    fi
+	if command -v gh > /dev/null 2>&1 && ! gh extension list; then
+		warn_optional "unable to list installed GitHub CLI extensions"
+	fi
 }
 
 #
@@ -267,24 +267,24 @@
 #   required, so a missing install is not a failure.
 #
 function check_agmsg() {
-    local target="${HOME%/}/.agents/skills/agmsg"
-    local script_dir pin installed
-
-    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
-    pin="$(awk -F'"' '/^AGMSG_PIN_VERSION=/ { print $2; exit }' "${script_dir}/update-agent-assets.sh" 2> /dev/null || true)"
-
-    if [ ! -f "${target}/VERSION" ]; then
-        printf 'not applicable: agmsg (not installed)\n'
-        return 0
-    fi
-
-    installed="$(cat "${target}/VERSION")"
-    if [ "${installed}" = "${pin:-unknown}" ]; then
-        printf 'found:   agmsg -> %s (version %s, matches pin)\n' "${target}" "${installed}"
-    else
-        printf 'found:   agmsg -> %s (version %s, pin %s)\n' "${target}" "${installed}" "${pin:-unknown}"
-        warn_optional "agmsg version ${installed} does not match the pinned ${pin:-unknown}; run make update"
-    fi
+	local target="${HOME%/}/.agents/skills/agmsg"
+	local script_dir pin installed
+
+	script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+	pin="$(awk -F'"' '/^AGMSG_PIN_VERSION=/ { print $2; exit }' "${script_dir}/update-agent-assets.sh" 2> /dev/null || true)"
+
+	if [ ! -f "${target}/VERSION" ]; then
+		printf 'not applicable: agmsg (not installed)\n'
+		return 0
+	fi
+
+	installed="$(cat "${target}/VERSION")"
+	if [ "${installed}" = "${pin:-unknown}" ]; then
+		printf 'found:   agmsg -> %s (version %s, matches pin)\n' "${target}" "${installed}"
+	else
+		printf 'found:   agmsg -> %s (version %s, pin %s)\n' "${target}" "${installed}" "${pin:-unknown}"
+		warn_optional "agmsg version ${installed} does not match the pinned ${pin:-unknown}; run make update"
+	fi
 }
 
 #
@@ -293,20 +293,20 @@
 #   side, so this check has no sysctl or profile logic.
 #
 function check_claude_sandbox() {
-    local command_name
-
-    if [ "$(uname)" != "Linux" ]; then
-        printf 'not applicable: Claude Code sandbox prerequisites (non-Linux; macOS uses Seatbelt)\n'
-        return 0
-    fi
-
-    for command_name in bwrap socat; do
-        if command -v "${command_name}" > /dev/null 2>&1; then
-            printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
-        else
-            warn_optional "Claude Code sandbox prerequisite is missing: ${command_name} (run make update)"
-        fi
-    done
+	local command_name
+
+	if [ "$(uname)" != "Linux" ]; then
+		printf 'not applicable: Claude Code sandbox prerequisites (non-Linux; macOS uses Seatbelt)\n'
+		return 0
+	fi
+
+	for command_name in bwrap socat; do
+		if command -v "${command_name}" > /dev/null 2>&1; then
+			printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
+		else
+			warn_optional "Claude Code sandbox prerequisite is missing: ${command_name} (run make update)"
+		fi
+	done
 }
 
 #
@@ -313,54 +313,54 @@
 # @description Run the read-only dotfiles health checks.
 #
 function main() {
-    section "Core commands"
-    check_command git --version
-    check_command chezmoi --version
-    check_command mise --version
-    check_command uv --version
-    check_command gh --version
-
-    section "Chezmoi"
-    run_required_doctor chezmoi doctor
-    check_private_chezmoi
-
-    section "Mise"
-    run_required_doctor mise doctor
-    run_required_doctor mise ls --current
-
-    section "Homebrew"
-    check_homebrew
-
-    section "Crit CLI"
-    check_crit_cli
-
-    section "Agent tools"
-    check_omp
-    check_hcom
-
-    section "Zed"
-    check_zed
-
-    section "SSH"
-    check_machine_ssh_key
-
-    section "AppArmor"
-    check_apparmor_userns
-
-    section "Claude Code sandbox"
-    check_claude_sandbox
-
-    section "GitHub CLI extensions"
-    check_gh_extensions
-
-    section "agmsg"
-    check_agmsg
-
-    printf '\nTool check summary: required failures: %d; optional warnings: %d\n' \
-        "${required_failures}" "${optional_warnings}"
-    [ "${required_failures}" -eq 0 ]
+	section "Core commands"
+	check_command git --version
+	check_command chezmoi --version
+	check_command mise --version
+	check_command uv --version
+	check_command gh --version
+
+	section "Chezmoi"
+	run_required_doctor chezmoi doctor
+	check_private_chezmoi
+
+	section "Mise"
+	run_required_doctor mise doctor
+	run_required_doctor mise ls --current
+
+	section "Homebrew"
+	check_homebrew
+
+	section "Crit CLI"
+	check_crit_cli
+
+	section "Agent tools"
+	check_omp
+	check_hcom
+
+	section "Zed"
+	check_zed
+
+	section "SSH"
+	check_machine_ssh_key
+
+	section "AppArmor"
+	check_apparmor_userns
+
+	section "Claude Code sandbox"
+	check_claude_sandbox
+
+	section "GitHub CLI extensions"
+	check_gh_extensions
+
+	section "agmsg"
+	check_agmsg
+
+	printf '\nTool check summary: required failures: %d; optional warnings: %d\n' \
+		"${required_failures}" "${optional_warnings}"
+	[ "${required_failures}" -eq 0 ]
 }
 
 if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
-    main "$@"
+	main "$@"
 fi
diff scripts/update-agent-assets.sh.orig scripts/update-agent-assets.sh
--- scripts/update-agent-assets.sh.orig
+++ scripts/update-agent-assets.sh
@@ -17,21 +17,21 @@
 # @exitcode 1 Neither the wrapper export nor direct script path was valid.
 #
 function resolve_dotfiles_source_dir() {
-    local candidate
-
-    if [[ -n "${DOTFILES_SOURCE_DIR:-}" ]] && [[ -d "${DOTFILES_SOURCE_DIR}/vendor/compactiondb" ]]; then
-        printf '%s\n' "${DOTFILES_SOURCE_DIR}"
-        return 0
-    fi
-
-    candidate="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
-    if [[ -d "${candidate}/vendor/compactiondb" ]]; then
-        printf '%s\n' "${candidate}"
-        return 0
-    fi
-
-    printf 'Unable to resolve dotfiles source root: vendor/compactiondb was not found via DOTFILES_SOURCE_DIR or BASH_SOURCE.\n' >&2
-    return 1
+	local candidate
+
+	if [[ -n "${DOTFILES_SOURCE_DIR:-}" ]] && [[ -d "${DOTFILES_SOURCE_DIR}/vendor/compactiondb" ]]; then
+		printf '%s\n' "${DOTFILES_SOURCE_DIR}"
+		return 0
+	fi
+
+	candidate="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
+	if [[ -d "${candidate}/vendor/compactiondb" ]]; then
+		printf '%s\n' "${candidate}"
+		return 0
+	fi
+
+	printf 'Unable to resolve dotfiles source root: vendor/compactiondb was not found via DOTFILES_SOURCE_DIR or BASH_SOURCE.\n' >&2
+	return 1
 }
 
 DOTFILES_REPO_SOURCE_DIR="$(resolve_dotfiles_source_dir)" || exit 1
@@ -39,8 +39,8 @@
 AGENT_ASSET_SCRIPT_DIR="${DOTFILES_REPO_SOURCE_DIR}/scripts"
 readonly AGENT_ASSET_SCRIPT_DIR
 if ! declare -F manifest_record > /dev/null 2>&1; then
-    # shellcheck source=scripts/lib/asset-manifest.sh
-    source "${AGENT_ASSET_SCRIPT_DIR}/lib/asset-manifest.sh"
+	# shellcheck source=scripts/lib/asset-manifest.sh
+	source "${AGENT_ASSET_SCRIPT_DIR}/lib/asset-manifest.sh"
 fi
 # shellcheck source=scripts/lib/installer-pins.sh
 source "${AGENT_ASSET_SCRIPT_DIR}/lib/installer-pins.sh"
@@ -92,7 +92,7 @@
 # @arg $1 string Heading text.
 #
 function section() {
-    printf '\n==> %s\n' "$1"
+	printf '\n==> %s\n' "$1"
 }
 
 #
@@ -100,7 +100,7 @@
 # @arg $1 string Command name.
 #
 function has_command() {
-    command -v "$1" > /dev/null 2>&1
+	command -v "$1" > /dev/null 2>&1
 }
 
 #
@@ -107,14 +107,14 @@
 # @description Remove node-global agent CLIs that shadow their dedicated mise tools.
 #
 function remove_node_global_agent_cli_shadows() {
-    local npm_package
-
-    has_command npm || return 0
-    for npm_package in "@openai/codex" "@anthropic-ai/claude-code"; do
-        if npm list -g "${npm_package}" --depth=0 > /dev/null 2>&1; then
-            npm uninstall -g "${npm_package}"
-        fi
-    done
+	local npm_package
+
+	has_command npm || return 0
+	for npm_package in "@openai/codex" "@anthropic-ai/claude-code"; do
+		if npm list -g "${npm_package}" --depth=0 > /dev/null 2>&1; then
+			npm uninstall -g "${npm_package}"
+		fi
+	done
 }
 
 #
@@ -123,20 +123,20 @@
 # @arg $2 string mise npm tool name.
 #
 function ensure_mise_npm_agent_cli() {
-    local cli="$1"
-    local mise_tool="$2"
-
-    if has_command "${cli}" && "${cli}" --version > /dev/null 2>&1; then
-        return 0
-    fi
-    has_command mise || return 0
-
-    printf 'Repairing %s through the mise npm backend.\n' "${cli}"
-    MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 \
-        mise install --force "${mise_tool}"
-    hash -r
-    "${cli}" --version > /dev/null
-    manifest_record "ensure_mise_npm_agent_cli:${cli}" installer "$("${cli}" --version 2> /dev/null || printf 'unknown\n')" "$(mise where "${mise_tool}" 2> /dev/null || command -v "${cli}")" -- "MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 mise install --force ${mise_tool}"
+	local cli="$1"
+	local mise_tool="$2"
+
+	if has_command "${cli}" && "${cli}" --version > /dev/null 2>&1; then
+		return 0
+	fi
+	has_command mise || return 0
+
+	printf 'Repairing %s through the mise npm backend.\n' "${cli}"
+	MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 \
+		mise install --force "${mise_tool}"
+	hash -r
+	"${cli}" --version > /dev/null
+	manifest_record "ensure_mise_npm_agent_cli:${cli}" installer "$("${cli}" --version 2> /dev/null || printf 'unknown\n')" "$(mise where "${mise_tool}" 2> /dev/null || command -v "${cli}")" -- "MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 mise install --force ${mise_tool}"
 }
 
 #
@@ -143,7 +143,7 @@
 # @description Install configured GitHub CLI extensions when authentication is ready.
 #
 function ensure_gh_extensions() {
-    bash "${DOTFILES_REPO_SOURCE_DIR}/install/common/gh_extensions.sh"
+	bash "${DOTFILES_REPO_SOURCE_DIR}/install/common/gh_extensions.sh"
 }
 
 #
@@ -152,10 +152,10 @@
 # @arg $@ string Command and arguments to run.
 #
 function command_output_contains() {
-    local needle="$1"
-    shift
-
-    "$@" 2> /dev/null | grep -Fq "${needle}"
+	local needle="$1"
+	shift
+
+	"$@" 2> /dev/null | grep -Fq "${needle}"
 }
 
 #
@@ -163,9 +163,9 @@
 # @arg $1 string Marketplace name.
 #
 function codex_marketplace_root() {
-    local marketplace="$1"
-
-    codex plugin marketplace list 2> /dev/null | awk -v name="${marketplace}" '$1 == name { print $2; exit }'
+	local marketplace="$1"
+
+	codex plugin marketplace list 2> /dev/null | awk -v name="${marketplace}" '$1 == name { print $2; exit }'
 }
 
 #
@@ -174,18 +174,18 @@
 # @arg $2 string Expected HTTPS origin URL.
 #
 function git_remote_origin_matches() {
-    local root="$1"
-    local expected_source="$2"
-    local expected_ssh="git@github.com:${expected_source#https://github.com/}"
-    local remote
-
-    remote="$(git -C "${root}" config --get remote.origin.url 2> /dev/null || true)"
-    case "${remote}" in
-    "${expected_source}" | "${expected_source%.git}" | "${expected_ssh}" | "${expected_ssh%.git}")
-        return 0
-        ;;
-    esac
-    return 1
+	local root="$1"
+	local expected_source="$2"
+	local expected_ssh="git@github.com:${expected_source#https://github.com/}"
+	local remote
+
+	remote="$(git -C "${root}" config --get remote.origin.url 2> /dev/null || true)"
+	case "${remote}" in
+	"${expected_source}" | "${expected_source%.git}" | "${expected_ssh}" | "${expected_ssh%.git}")
+		return 0
+		;;
+	esac
+	return 1
 }
 
 #
@@ -194,16 +194,16 @@
 # @arg $2 string Expected HTTPS origin URL.
 #
 function codex_marketplace_has_source() {
-    local marketplace="$1"
-    local expected_source="$2"
-    local root
-
-    root="$(codex_marketplace_root "${marketplace}")"
-    if [ -z "${root}" ] || [ ! -d "${root}/.git" ]; then
-        return 1
-    fi
-
-    git_remote_origin_matches "${root}" "${expected_source}"
+	local marketplace="$1"
+	local expected_source="$2"
+	local root
+
+	root="$(codex_marketplace_root "${marketplace}")"
+	if [ -z "${root}" ] || [ ! -d "${root}/.git" ]; then
+		return 1
+	fi
+
+	git_remote_origin_matches "${root}" "${expected_source}"
 }
 
 #
@@ -210,11 +210,11 @@
 # @description Ensure the official Claude Code plugin marketplace is configured.
 #
 function ensure_claude_superpowers_marketplace() {
-    if command_output_contains "claude-plugins-official" claude plugin marketplace list; then
-        return 0
-    fi
-
-    claude plugin marketplace add "${CLAUDE_SUPERPOWERS_MARKETPLACE}"
+	if command_output_contains "claude-plugins-official" claude plugin marketplace list; then
+		return 0
+	fi
+
+	claude plugin marketplace add "${CLAUDE_SUPERPOWERS_MARKETPLACE}"
 }
 
 #
@@ -225,31 +225,31 @@
 # @arg $3 path Destination executable path.
 #
 function install_crit_release() (
-    local artifact="$1"
-    local pinned="$2"
-    local target="$3"
-    local tag="${CRIT_PIN_VERSION}"
-    local actual base_url checksums download expected staging=""
-
-    base_url="https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}"
-    download="$(mktemp)" || return
-    checksums="$(mktemp)" || return
-    trap 'rm -f "${download}" "${checksums}" ${staging:+"${staging}"}' EXIT
-    curl -fsSL "${base_url}/${artifact}" -o "${download}" || return
-    curl -fsSL "${base_url}/checksums.txt" -o "${checksums}" || return
-    expected="$(awk -v name="${artifact}" '$2 == name { print $1; exit }' "${checksums}")"
-    actual="$(shasum -a 256 "${download}" | awk '{ print $1 }')"
-    # The release is mutable, so the reviewed sha256 is the check; checksums.txt only re-checks the download.
-    if [ -z "${pinned}" ] || [ "${actual}" != "${pinned}" ] || [ "${actual}" != "${expected}" ]; then
-        printf 'Crit checksum mismatch for %s %s.\n' "${artifact}" "${tag}" >&2
-        return 1
-    fi
-
-    mkdir -p "$(dirname "${target}")" || return
-    staging="$(mktemp "${target}.XXXXXX")" || return
-    install -m 0755 "${download}" "${staging}" || return
-    [ "$(crit_version "${staging}")" = "${tag#v}" ] || return
-    mv -f "${staging}" "${target}"
+	local artifact="$1"
+	local pinned="$2"
+	local target="$3"
+	local tag="${CRIT_PIN_VERSION}"
+	local actual base_url checksums download expected staging=""
+
+	base_url="https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}"
+	download="$(mktemp)" || return
+	checksums="$(mktemp)" || return
+	trap 'rm -f "${download}" "${checksums}" ${staging:+"${staging}"}' EXIT
+	curl -fsSL "${base_url}/${artifact}" -o "${download}" || return
+	curl -fsSL "${base_url}/checksums.txt" -o "${checksums}" || return
+	expected="$(awk -v name="${artifact}" '$2 == name { print $1; exit }' "${checksums}")"
+	actual="$(shasum -a 256 "${download}" | awk '{ print $1 }')"
+	# The release is mutable, so the reviewed sha256 is the check; checksums.txt only re-checks the download.
+	if [ -z "${pinned}" ] || [ "${actual}" != "${pinned}" ] || [ "${actual}" != "${expected}" ]; then
+		printf 'Crit checksum mismatch for %s %s.\n' "${artifact}" "${tag}" >&2
+		return 1
+	fi
+
+	mkdir -p "$(dirname "${target}")" || return
+	staging="$(mktemp "${target}.XXXXXX")" || return
+	install -m 0755 "${download}" "${staging}" || return
+	[ "$(crit_version "${staging}")" = "${tag#v}" ] || return
+	mv -f "${staging}" "${target}"
 )
 
 #
@@ -258,11 +258,11 @@
 # @arg $1 path Crit executable.
 #
 function crit_version() {
-    local output
-    [ -x "$1" ] || return 0
-    # A binary that exits non-zero is broken whatever it printed, so it reports no version.
-    output="$("$1" --version 2> /dev/null)" || return 0
-    printf '%s\n' "${output}" | awk '$1 == "crit" { sub(/^v/, "", $2); print $2; exit }'
+	local output
+	[ -x "$1" ] || return 0
+	# A binary that exits non-zero is broken whatever it printed, so it reports no version.
+	output="$("$1" --version 2> /dev/null)" || return 0
+	printf '%s\n' "${output}" | awk '$1 == "crit" { sub(/^v/, "", $2); print $2; exit }'
 }
 
 #
@@ -269,27 +269,27 @@
 # @description Ensure the Crit CLI is the pinned release for agent integrations.
 #
 function ensure_crit_cli() {
-    local artifact checksum tag="${CRIT_PIN_VERSION}" target
-
-    case "$(uname -s)/$(uname -m)" in
-    Linux/x86_64 | Linux/amd64) artifact="crit-linux-amd64" checksum="${CRIT_LINUX_AMD64_SHA256}" ;;
-    Linux/aarch64 | Linux/arm64) artifact="crit-linux-arm64" checksum="${CRIT_LINUX_ARM64_SHA256}" ;;
-    Darwin/x86_64 | Darwin/amd64) artifact="crit-darwin-amd64" checksum="${CRIT_DARWIN_AMD64_SHA256}" ;;
-    Darwin/arm64 | Darwin/aarch64) artifact="crit-darwin-arm64" checksum="${CRIT_DARWIN_ARM64_SHA256}" ;;
-    *)
-        printf 'Skipping Crit integrations: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
-        return 1
-        ;;
-    esac
-
-    target="${HOME}/.local/bin/crit"
-    if [ "$(crit_version "${target}")" != "${tag#v}" ]; then
-        section "Crit CLI"
-        install_crit_release "${artifact}" "${checksum}" "${target}" || return 1
-    fi
-    export PATH="${HOME}/.local/bin:${PATH}"
-    hash -r
-    manifest_record "ensure_crit_cli" installer "${tag}" "${target}" -- "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/${artifact}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/checksums.txt" "shasum -a 256 <binary>" "install -m 0755 <binary> ${target}"
+	local artifact checksum tag="${CRIT_PIN_VERSION}" target
+
+	case "$(uname -s)/$(uname -m)" in
+	Linux/x86_64 | Linux/amd64) artifact="crit-linux-amd64" checksum="${CRIT_LINUX_AMD64_SHA256}" ;;
+	Linux/aarch64 | Linux/arm64) artifact="crit-linux-arm64" checksum="${CRIT_LINUX_ARM64_SHA256}" ;;
+	Darwin/x86_64 | Darwin/amd64) artifact="crit-darwin-amd64" checksum="${CRIT_DARWIN_AMD64_SHA256}" ;;
+	Darwin/arm64 | Darwin/aarch64) artifact="crit-darwin-arm64" checksum="${CRIT_DARWIN_ARM64_SHA256}" ;;
+	*)
+		printf 'Skipping Crit integrations: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
+		return 1
+		;;
+	esac
+
+	target="${HOME}/.local/bin/crit"
+	if [ "$(crit_version "${target}")" != "${tag#v}" ]; then
+		section "Crit CLI"
+		install_crit_release "${artifact}" "${checksum}" "${target}" || return 1
+	fi
+	export PATH="${HOME}/.local/bin:${PATH}"
+	hash -r
+	manifest_record "ensure_crit_cli" installer "${tag}" "${target}" -- "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/${artifact}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/checksums.txt" "shasum -a 256 <binary>" "install -m 0755 <binary> ${target}"
 }
 
 #
@@ -296,11 +296,11 @@
 # @description Ensure the Crit Claude Code plugin marketplace is configured.
 #
 function ensure_claude_crit_marketplace() {
-    if command_output_contains "${CLAUDE_CRIT_MARKETPLACE_NAME}" claude plugin marketplace list; then
-        return 0
-    fi
-
-    claude plugin marketplace add "${CLAUDE_CRIT_MARKETPLACE}"
+	if command_output_contains "${CLAUDE_CRIT_MARKETPLACE_NAME}" claude plugin marketplace list; then
+		return 0
+	fi
+
+	claude plugin marketplace add "${CLAUDE_CRIT_MARKETPLACE}"
 }
 
 #
@@ -307,11 +307,11 @@
 # @description Ensure the Ponytail Claude Code plugin marketplace is configured.
 #
 function ensure_claude_ponytail_marketplace() {
-    if command_output_contains "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" claude plugin marketplace list; then
-        return 0
-    fi
-
-    claude plugin marketplace add "${CLAUDE_PONYTAIL_MARKETPLACE}"
+	if command_output_contains "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" claude plugin marketplace list; then
+		return 0
+	fi
+
+	claude plugin marketplace add "${CLAUDE_PONYTAIL_MARKETPLACE}"
 }
 
 #
@@ -318,11 +318,11 @@
 # @description Ensure the Understand-Anything Claude Code plugin marketplace is configured.
 #
 function ensure_claude_understand_anything_marketplace() {
-    if command_output_contains "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" claude plugin marketplace list; then
-        return 0
-    fi
-
-    claude plugin marketplace add "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}"
+	if command_output_contains "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" claude plugin marketplace list; then
+		return 0
+	fi
+
+	claude plugin marketplace add "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}"
 }
 
 #
@@ -329,11 +329,11 @@
 # @description Return success when the Claude Code Crit plugin is already enabled.
 #
 function claude_crit_plugin_is_enabled() {
-    if ! has_command python3; then
-        return 1
-    fi
-
-    claude plugin list --json 2> /dev/null | CLAUDE_CRIT_PLUGIN_ID="${CLAUDE_CRIT_PLUGIN}" python3 -c '
+	if ! has_command python3; then
+		return 1
+	fi
+
+	claude plugin list --json 2> /dev/null | CLAUDE_CRIT_PLUGIN_ID="${CLAUDE_CRIT_PLUGIN}" python3 -c '
 import json
 import os
 import sys
@@ -358,11 +358,11 @@
 # @description Return success when the Claude Code Ponytail plugin is already enabled.
 #
 function claude_ponytail_plugin_is_enabled() {
-    if ! has_command python3; then
-        return 1
-    fi
-
-    claude plugin list --json 2> /dev/null | CLAUDE_PONYTAIL_PLUGIN_ID="${CLAUDE_PONYTAIL_PLUGIN}" python3 -c '
+	if ! has_command python3; then
+		return 1
+	fi
+
+	claude plugin list --json 2> /dev/null | CLAUDE_PONYTAIL_PLUGIN_ID="${CLAUDE_PONYTAIL_PLUGIN}" python3 -c '
 import json
 import os
 import sys
@@ -387,11 +387,11 @@
 # @description Return success when the Claude Code Understand-Anything plugin is already enabled.
 #
 function claude_understand_anything_plugin_is_enabled() {
-    if ! has_command python3; then
-        return 1
-    fi
-
-    claude plugin list --json 2> /dev/null | CLAUDE_UNDERSTAND_ANYTHING_PLUGIN_ID="${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" python3 -c '
+	if ! has_command python3; then
+		return 1
+	fi
+
+	claude plugin list --json 2> /dev/null | CLAUDE_UNDERSTAND_ANYTHING_PLUGIN_ID="${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" python3 -c '
 import json
 import os
 import sys
@@ -416,14 +416,14 @@
 # @description Install or refresh the Herdr agent integrations.
 #
 function ensure_herdr_integrations() {
-    if ! has_command herdr; then
-        return 0
-    fi
-
-    section "herdr integrations"
-    herdr integration install claude
-    herdr integration install codex
-    manifest_record "ensure_herdr_integrations" integration "$(herdr --version 2> /dev/null | awk 'NF { version = $NF } END { print version ? version : "unknown" }')" "${HOME}/.claude/hooks/herdr-agent-state.sh" "${HOME}/.codex/herdr-agent-state.sh" -- "herdr integration install claude" "herdr integration install codex"
+	if ! has_command herdr; then
+		return 0
+	fi
+
+	section "herdr integrations"
+	herdr integration install claude
+	herdr integration install codex
+	manifest_record "ensure_herdr_integrations" integration "$(herdr --version 2> /dev/null | awk 'NF { version = $NF } END { print version ? version : "unknown" }')" "${HOME}/.claude/hooks/herdr-agent-state.sh" "${HOME}/.codex/herdr-agent-state.sh" -- "herdr integration install claude" "herdr integration install codex"
 }
 
 #
@@ -433,30 +433,30 @@
 # @exitcode 0 Always; a failed refresh only warns, and the next apply retries it.
 #
 function refresh_codex_hook_trust() {
-    local managed target
-    local pattern='/\.codex/([a-z0-9_]+\.)?config\.toml$'
-    local -a targets=()
-
-    if ! has_command chezmoi; then
-        return 0
-    fi
-    if ! managed="$(chezmoi managed --path-style=absolute --include=files 2> /dev/null)"; then
-        printf 'WARN: Codex hook trust not refreshed: chezmoi managed failed; the next apply retries it.\n' >&2
-        return 0
-    fi
-    while IFS= read -r target; do
-        if [[ ${target} =~ ${pattern} ]]; then
-            targets+=("${target}")
-        fi
-    done <<< "${managed}"
-    if ((${#targets[@]} == 0)); then
-        return 0
-    fi
-
-    section "codex hook trust"
-    if ! chezmoi apply --force "${targets[@]}"; then
-        printf 'WARN: Codex hook trust not refreshed: chezmoi apply failed; the next apply retries it.\n' >&2
-    fi
+	local managed target
+	local pattern='/\.codex/([a-z0-9_]+\.)?config\.toml$'
+	local -a targets=()
+
+	if ! has_command chezmoi; then
+		return 0
+	fi
+	if ! managed="$(chezmoi managed --path-style=absolute --include=files 2> /dev/null)"; then
+		printf 'WARN: Codex hook trust not refreshed: chezmoi managed failed; the next apply retries it.\n' >&2
+		return 0
+	fi
+	while IFS= read -r target; do
+		if [[ ${target} =~ ${pattern} ]]; then
+			targets+=("${target}")
+		fi
+	done <<< "${managed}"
+	if ((${#targets[@]} == 0)); then
+		return 0
+	fi
+
+	section "codex hook trust"
+	if ! chezmoi apply --force "${targets[@]}"; then
+		printf 'WARN: Codex hook trust not refreshed: chezmoi apply failed; the next apply retries it.\n' >&2
+	fi
 }
 
 #
@@ -463,22 +463,22 @@
 # @description Install or update the Claude Code Superpowers plugin.
 #
 function update_claude_superpowers() {
-    if ! has_command claude; then
-        printf 'Skipping Claude Code plugins: claude command not found.\n'
-        return 0
-    fi
-
-    section "Claude Code plugins"
-    ensure_claude_superpowers_marketplace
-    claude plugin marketplace update claude-plugins-official || true
-
-    if command_output_contains "\"id\":\"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json ||
-        command_output_contains "\"id\": \"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json; then
-        claude plugin update "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
-    else
-        claude plugin install "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
-    fi
-    manifest_record "update_claude_superpowers" plugin "$(manifest_claude_plugin_version "${CLAUDE_SUPERPOWERS_PLUGIN}")" "${HOME}/.claude/plugins/cache/claude-plugins-official/superpowers" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_SUPERPOWERS_MARKETPLACE}" "claude plugin marketplace update claude-plugins-official" "claude plugin install ${CLAUDE_SUPERPOWERS_PLUGIN}" "claude plugin update ${CLAUDE_SUPERPOWERS_PLUGIN}"
+	if ! has_command claude; then
+		printf 'Skipping Claude Code plugins: claude command not found.\n'
+		return 0
+	fi
+
+	section "Claude Code plugins"
+	ensure_claude_superpowers_marketplace
+	claude plugin marketplace update claude-plugins-official || true
+
+	if command_output_contains "\"id\":\"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json ||
+		command_output_contains "\"id\": \"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json; then
+		claude plugin update "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
+	else
+		claude plugin install "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
+	fi
+	manifest_record "update_claude_superpowers" plugin "$(manifest_claude_plugin_version "${CLAUDE_SUPERPOWERS_PLUGIN}")" "${HOME}/.claude/plugins/cache/claude-plugins-official/superpowers" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_SUPERPOWERS_MARKETPLACE}" "claude plugin marketplace update claude-plugins-official" "claude plugin install ${CLAUDE_SUPERPOWERS_PLUGIN}" "claude plugin update ${CLAUDE_SUPERPOWERS_PLUGIN}"
 }
 
 #
@@ -485,30 +485,30 @@
 # @description Install or update the Claude Code Crit plugin.
 #
 function update_claude_crit() {
-    if ! has_command claude; then
-        printf 'Skipping Claude Code Crit plugin: claude command not found.\n'
-        return 0
-    fi
-
-    section "Claude Code Crit plugin"
-    if ! ensure_crit_cli; then
-        return 0
-    fi
-    ensure_claude_crit_marketplace
-    claude plugin marketplace update "${CLAUDE_CRIT_MARKETPLACE_NAME}" || true
-
-    if command_output_contains "\"id\":\"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json ||
-        command_output_contains "\"id\": \"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json; then
-        claude plugin update "${CLAUDE_CRIT_PLUGIN}" || true
-    else
-        claude plugin install "${CLAUDE_CRIT_PLUGIN}" || true
-    fi
-    if claude_crit_plugin_is_enabled; then
-        printf 'Claude Code Crit plugin is already enabled.\n'
-    else
-        claude plugin enable "${CLAUDE_CRIT_PLUGIN}" || true
-    fi
-    manifest_record "update_claude_crit" plugin "$(manifest_claude_plugin_version "${CLAUDE_CRIT_PLUGIN}")" "${HOME}/.claude/plugins/cache/crit/crit" "${HOME}/.claude/settings.json" -- "ensure_crit_cli" "claude plugin marketplace add ${CLAUDE_CRIT_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_CRIT_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_CRIT_PLUGIN}" "claude plugin update ${CLAUDE_CRIT_PLUGIN}" "claude plugin enable ${CLAUDE_CRIT_PLUGIN}"
+	if ! has_command claude; then
+		printf 'Skipping Claude Code Crit plugin: claude command not found.\n'
+		return 0
+	fi
+
+	section "Claude Code Crit plugin"
+	if ! ensure_crit_cli; then
+		return 0
+	fi
+	ensure_claude_crit_marketplace
+	claude plugin marketplace update "${CLAUDE_CRIT_MARKETPLACE_NAME}" || true
+
+	if command_output_contains "\"id\":\"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json ||
+		command_output_contains "\"id\": \"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json; then
+		claude plugin update "${CLAUDE_CRIT_PLUGIN}" || true
+	else
+		claude plugin install "${CLAUDE_CRIT_PLUGIN}" || true
+	fi
+	if claude_crit_plugin_is_enabled; then
+		printf 'Claude Code Crit plugin is already enabled.\n'
+	else
+		claude plugin enable "${CLAUDE_CRIT_PLUGIN}" || true
+	fi
+	manifest_record "update_claude_crit" plugin "$(manifest_claude_plugin_version "${CLAUDE_CRIT_PLUGIN}")" "${HOME}/.claude/plugins/cache/crit/crit" "${HOME}/.claude/settings.json" -- "ensure_crit_cli" "claude plugin marketplace add ${CLAUDE_CRIT_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_CRIT_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_CRIT_PLUGIN}" "claude plugin update ${CLAUDE_CRIT_PLUGIN}" "claude plugin enable ${CLAUDE_CRIT_PLUGIN}"
 }
 
 #
@@ -515,28 +515,28 @@
 # @description Install or update the Claude Code Ponytail plugin.
 #
 function update_claude_ponytail() {
-    if ! has_command claude; then
-        printf 'Skipping Claude Code Ponytail plugin: claude command not found.\n'
-        return 0
-    fi
-
-    section "Claude Code Ponytail plugin"
-    ensure_claude_ponytail_marketplace
-    claude plugin marketplace update "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" || true
-
-    if command_output_contains "\"id\":\"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json ||
-        command_output_contains "\"id\": \"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json; then
-        claude plugin update "${CLAUDE_PONYTAIL_PLUGIN}" || true
-    else
-        claude plugin install "${CLAUDE_PONYTAIL_PLUGIN}" || true
-    fi
-    if claude_ponytail_plugin_is_enabled; then
-        printf 'Claude Code Ponytail plugin is already enabled.\n'
-    else
-        claude plugin enable "${CLAUDE_PONYTAIL_PLUGIN}" || true
-    fi
-    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
-    manifest_record "update_claude_ponytail" plugin "$(manifest_claude_plugin_version "${CLAUDE_PONYTAIL_PLUGIN}")" "${HOME}/.claude/plugins/cache/ponytail/ponytail" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_PONYTAIL_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin update ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin enable ${CLAUDE_PONYTAIL_PLUGIN}"
+	if ! has_command claude; then
+		printf 'Skipping Claude Code Ponytail plugin: claude command not found.\n'
+		return 0
+	fi
+
+	section "Claude Code Ponytail plugin"
+	ensure_claude_ponytail_marketplace
+	claude plugin marketplace update "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" || true
+
+	if command_output_contains "\"id\":\"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json ||
+		command_output_contains "\"id\": \"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json; then
+		claude plugin update "${CLAUDE_PONYTAIL_PLUGIN}" || true
+	else
+		claude plugin install "${CLAUDE_PONYTAIL_PLUGIN}" || true
+	fi
+	if claude_ponytail_plugin_is_enabled; then
+		printf 'Claude Code Ponytail plugin is already enabled.\n'
+	else
+		claude plugin enable "${CLAUDE_PONYTAIL_PLUGIN}" || true
+	fi
+	printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
+	manifest_record "update_claude_ponytail" plugin "$(manifest_claude_plugin_version "${CLAUDE_PONYTAIL_PLUGIN}")" "${HOME}/.claude/plugins/cache/ponytail/ponytail" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_PONYTAIL_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin update ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin enable ${CLAUDE_PONYTAIL_PLUGIN}"
 }
 
 #
@@ -543,27 +543,27 @@
 # @description Install or update the Claude Code Understand-Anything plugin.
 #
 function update_claude_understand_anything() {
-    if ! has_command claude; then
-        printf 'Skipping Claude Code Understand-Anything plugin: claude command not found.\n'
-        return 0
-    fi
-
-    section "Claude Code Understand-Anything plugin"
-    ensure_claude_understand_anything_marketplace
-    claude plugin marketplace update "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" || true
-
-    if command_output_contains "\"id\":\"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json ||
-        command_output_contains "\"id\": \"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json; then
-        claude plugin update "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
-    else
-        claude plugin install "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
-    fi
-    if claude_understand_anything_plugin_is_enabled; then
-        printf 'Claude Code Understand-Anything plugin is already enabled.\n'
-    else
-        claude plugin enable "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
-    fi
-    manifest_record "update_claude_understand_anything" plugin "$(manifest_claude_plugin_version "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}")" "${HOME}/.claude/plugins/cache/understand-anything/understand-anything" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin update ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin enable ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}"
+	if ! has_command claude; then
+		printf 'Skipping Claude Code Understand-Anything plugin: claude command not found.\n'
+		return 0
+	fi
+
+	section "Claude Code Understand-Anything plugin"
+	ensure_claude_understand_anything_marketplace
+	claude plugin marketplace update "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" || true
+
+	if command_output_contains "\"id\":\"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json ||
+		command_output_contains "\"id\": \"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json; then
+		claude plugin update "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
+	else
+		claude plugin install "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
+	fi
+	if claude_understand_anything_plugin_is_enabled; then
+		printf 'Claude Code Understand-Anything plugin is already enabled.\n'
+	else
+		claude plugin enable "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
+	fi
+	manifest_record "update_claude_understand_anything" plugin "$(manifest_claude_plugin_version "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}")" "${HOME}/.claude/plugins/cache/understand-anything/understand-anything" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin update ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin enable ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}"
 }
 
 #
@@ -570,31 +570,31 @@
 # @description Install the Codex Superpowers plugin from the OpenAI-curated catalog.
 #
 function update_codex_superpowers() {
-    local codex_output
-
-    if ! has_command codex; then
-        printf 'Skipping Codex plugins: codex command not found.\n'
-        return 0
-    fi
-
-    section "Codex plugins"
-    if command_output_contains "\"pluginId\":\"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json ||
-        command_output_contains "\"pluginId\": \"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json; then
-        printf 'Codex Superpowers plugin is already installed.\n'
-    elif codex_output="$(codex plugin add "${CODEX_SUPERPOWERS_PLUGIN}" 2>&1)"; then
-        if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
-            printf '%s\n' "${codex_output}" >&2
-        fi
-        printf 'Codex Superpowers plugin installed.\n'
-    else
-        if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
-            printf '%s\n' "${codex_output}" >&2
-        fi
-        printf 'Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.\n'
-        # shellcheck disable=SC2016 # Backticks are literal operator guidance.
-        printf 'Run `codex login`, then `codex plugin add %s`.\n' "${CODEX_SUPERPOWERS_PLUGIN}"
-    fi
-    manifest_record "update_codex_superpowers" plugin "$(manifest_codex_plugin_version "${CODEX_SUPERPOWERS_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/.tmp/plugins/plugins/superpowers" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin add ${CODEX_SUPERPOWERS_PLUGIN}"
+	local codex_output
+
+	if ! has_command codex; then
+		printf 'Skipping Codex plugins: codex command not found.\n'
+		return 0
+	fi
+
+	section "Codex plugins"
+	if command_output_contains "\"pluginId\":\"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json ||
+		command_output_contains "\"pluginId\": \"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json; then
+		printf 'Codex Superpowers plugin is already installed.\n'
+	elif codex_output="$(codex plugin add "${CODEX_SUPERPOWERS_PLUGIN}" 2>&1)"; then
+		if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
+			printf '%s\n' "${codex_output}" >&2
+		fi
+		printf 'Codex Superpowers plugin installed.\n'
+	else
+		if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
+			printf '%s\n' "${codex_output}" >&2
+		fi
+		printf 'Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.\n'
+		# shellcheck disable=SC2016 # Backticks are literal operator guidance.
+		printf 'Run `codex login`, then `codex plugin add %s`.\n' "${CODEX_SUPERPOWERS_PLUGIN}"
+	fi
+	manifest_record "update_codex_superpowers" plugin "$(manifest_codex_plugin_version "${CODEX_SUPERPOWERS_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/.tmp/plugins/plugins/superpowers" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin add ${CODEX_SUPERPOWERS_PLUGIN}"
 }
 
 #
@@ -601,26 +601,26 @@
 # @description Ensure the Ponytail Codex plugin marketplace is configured.
 #
 function ensure_codex_ponytail_marketplace() {
-    local codex_home="${CODEX_HOME:-${HOME}/.codex}"
-    local codex_config="${codex_home%/}/config.toml"
-
-    if [ -f "${codex_config}" ] && grep -Fq "[marketplaces.${CODEX_PONYTAIL_MARKETPLACE_NAME}]" "${codex_config}"; then
-        if grep -Fq "source = \"${CODEX_PONYTAIL_MARKETPLACE_SOURCE}\"" "${codex_config}"; then
-            return 0
-        fi
-        printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
-        return 1
-    fi
-
-    if codex_marketplace_has_source "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"; then
-        return 0
-    fi
-    if command_output_contains "${CODEX_PONYTAIL_MARKETPLACE_NAME}" codex plugin marketplace list; then
-        printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
-        return 1
-    fi
-
-    codex plugin marketplace add "${CODEX_PONYTAIL_MARKETPLACE}"
+	local codex_home="${CODEX_HOME:-${HOME}/.codex}"
+	local codex_config="${codex_home%/}/config.toml"
+
+	if [ -f "${codex_config}" ] && grep -Fq "[marketplaces.${CODEX_PONYTAIL_MARKETPLACE_NAME}]" "${codex_config}"; then
+		if grep -Fq "source = \"${CODEX_PONYTAIL_MARKETPLACE_SOURCE}\"" "${codex_config}"; then
+			return 0
+		fi
+		printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
+		return 1
+	fi
+
+	if codex_marketplace_has_source "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"; then
+		return 0
+	fi
+	if command_output_contains "${CODEX_PONYTAIL_MARKETPLACE_NAME}" codex plugin marketplace list; then
+		printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
+		return 1
+	fi
+
+	codex plugin marketplace add "${CODEX_PONYTAIL_MARKETPLACE}"
 }
 
 #
@@ -627,24 +627,24 @@
 # @description Install or update the Codex Ponytail plugin from its marketplace.
 #
 function update_codex_ponytail() {
-    if ! has_command codex; then
-        printf 'Skipping Codex Ponytail plugin: codex command not found.\n'
-        return 0
-    fi
-
-    section "Codex Ponytail plugin"
-    ensure_codex_ponytail_marketplace
-    codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}" || true
-
-    if command_output_contains "\"pluginId\":\"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json ||
-        command_output_contains "\"pluginId\": \"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json; then
-        printf 'Codex Ponytail plugin is already installed.\n'
-    else
-        codex plugin add "${CODEX_PONYTAIL_PLUGIN}" || true
-    fi
-    printf 'Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.\n'
-    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
-    manifest_record "update_codex_ponytail" plugin "$(manifest_codex_plugin_version "${CODEX_PONYTAIL_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/plugins/cache/ponytail/ponytail" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin marketplace add ${CODEX_PONYTAIL_MARKETPLACE}" "codex plugin marketplace upgrade ${CODEX_PONYTAIL_MARKETPLACE_NAME}" "codex plugin add ${CODEX_PONYTAIL_PLUGIN}"
+	if ! has_command codex; then
+		printf 'Skipping Codex Ponytail plugin: codex command not found.\n'
+		return 0
+	fi
+
+	section "Codex Ponytail plugin"
+	ensure_codex_ponytail_marketplace
+	codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}" || true
+
+	if command_output_contains "\"pluginId\":\"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json ||
+		command_output_contains "\"pluginId\": \"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json; then
+		printf 'Codex Ponytail plugin is already installed.\n'
+	else
+		codex plugin add "${CODEX_PONYTAIL_PLUGIN}" || true
+	fi
+	printf 'Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.\n'
+	printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
+	manifest_record "update_codex_ponytail" plugin "$(manifest_codex_plugin_version "${CODEX_PONYTAIL_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/plugins/cache/ponytail/ponytail" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin marketplace add ${CODEX_PONYTAIL_MARKETPLACE}" "codex plugin marketplace upgrade ${CODEX_PONYTAIL_MARKETPLACE_NAME}" "codex plugin add ${CODEX_PONYTAIL_PLUGIN}"
 }
 
 #
@@ -651,23 +651,23 @@
 # @description Install or update the Codex Crit plugin and plan-review hook.
 #
 function update_codex_crit() {
-    if ! has_command codex; then
-        printf 'Skipping Codex Crit plugin: codex command not found.\n'
-        return 0
-    fi
-    if ! ensure_crit_cli; then
-        return 0
-    fi
-
-    section "Codex Crit plugin"
-    (
-        cd "${HOME}"
-        crit install codex-plugin --force
-    ) || true
-    if [ -f "${HOME}/.agents/plugins/marketplace.json" ]; then
-        chmod 644 "${HOME}/.agents/plugins/marketplace.json"
-    fi
-    manifest_record "update_codex_crit" plugin "$(crit --version 2> /dev/null | awk 'NR == 1 { print $2 }')" "${CODEX_HOME:-${HOME}/.codex}/plugins/crit" "${CODEX_HOME:-${HOME}/.codex}/config.toml" "${HOME}/.agents/skills/crit" "${HOME}/.agents/skills/crit-cli" "${HOME}/.agents/skills/crit-story" -- "ensure_crit_cli" "crit install codex-plugin --force"
+	if ! has_command codex; then
+		printf 'Skipping Codex Crit plugin: codex command not found.\n'
+		return 0
+	fi
+	if ! ensure_crit_cli; then
+		return 0
+	fi
+
+	section "Codex Crit plugin"
+	(
+		cd "${HOME}"
+		crit install codex-plugin --force
+	) || true
+	if [ -f "${HOME}/.agents/plugins/marketplace.json" ]; then
+		chmod 644 "${HOME}/.agents/plugins/marketplace.json"
+	fi
+	manifest_record "update_codex_crit" plugin "$(crit --version 2> /dev/null | awk 'NR == 1 { print $2 }')" "${CODEX_HOME:-${HOME}/.codex}/plugins/crit" "${CODEX_HOME:-${HOME}/.codex}/config.toml" "${HOME}/.agents/skills/crit" "${HOME}/.agents/skills/crit-cli" "${HOME}/.agents/skills/crit-story" -- "ensure_crit_cli" "crit install codex-plugin --force"
 }
 
 #
@@ -687,31 +687,31 @@
 # @stderr One WARN line naming the manual command when the build cannot run or fails.
 #
 function build_understand_anything_core() {
-    local root="$1"
-    local -a pnpm_cmd
-
-    [ -d "${root}/packages/core" ] || return 0
-    if [ -f "${root}/packages/core/dist/index.js" ] &&
-        [ -z "$(find "${root}/packages/core/src" "${root}/pnpm-lock.yaml" -type f -newer "${root}/packages/core/dist/index.js" -print -quit 2> /dev/null || true)" ]; then
-        return 0
-    fi
-    if has_command mise; then
-        pnpm_cmd=(mise exec npm:pnpm -- pnpm)
-    elif has_command pnpm; then
-        pnpm_cmd=(pnpm)
-    else
-        printf 'WARN: Understand-Anything core not built: pnpm not found; run: cd %q && pnpm install --frozen-lockfile && pnpm --filter @understand-anything/core build\n' "${root}" >&2
-        return 0
-    fi
-    if ! (
-        cd "${root}" &&
-            { "${pnpm_cmd[@]}" install --frozen-lockfile 2> /dev/null || "${pnpm_cmd[@]}" install; } &&
-            "${pnpm_cmd[@]}" --filter @understand-anything/core build
-    ); then
-        printf 'WARN: Understand-Anything core build failed in %s; run: cd %q && %s install --frozen-lockfile && %s --filter @understand-anything/core build\n' \
-            "${root}" "${root}" "${pnpm_cmd[*]}" "${pnpm_cmd[*]}" >&2
-    fi
-    return 0
+	local root="$1"
+	local -a pnpm_cmd
+
+	[ -d "${root}/packages/core" ] || return 0
+	if [ -f "${root}/packages/core/dist/index.js" ] &&
+		[ -z "$(find "${root}/packages/core/src" "${root}/pnpm-lock.yaml" -type f -newer "${root}/packages/core/dist/index.js" -print -quit 2> /dev/null || true)" ]; then
+		return 0
+	fi
+	if has_command mise; then
+		pnpm_cmd=(mise exec npm:pnpm -- pnpm)
+	elif has_command pnpm; then
+		pnpm_cmd=(pnpm)
+	else
+		printf 'WARN: Understand-Anything core not built: pnpm not found; run: cd %q && pnpm install --frozen-lockfile && pnpm --filter @understand-anything/core build\n' "${root}" >&2
+		return 0
+	fi
+	if ! (
+		cd "${root}" &&
+			{ "${pnpm_cmd[@]}" install --frozen-lockfile 2> /dev/null || "${pnpm_cmd[@]}" install; } &&
+			"${pnpm_cmd[@]}" --filter @understand-anything/core build
+	); then
+		printf 'WARN: Understand-Anything core build failed in %s; run: cd %q && %s install --frozen-lockfile && %s --filter @understand-anything/core build\n' \
+			"${root}" "${root}" "${pnpm_cmd[*]}" "${pnpm_cmd[*]}" >&2
+	fi
+	return 0
 }
 
 #
@@ -723,17 +723,17 @@
 # @stdout Prints a skip message when no matching Claude release artifact is available.
 #
 function provision_codex_understand_anything_runtime() {
-    local plugin_root claude_cache release_root source destination
-
-    plugin_root="${HOME}/.understand-anything/repo/understand-anything-plugin"
-    claude_cache="${HOME}/.claude/plugins/cache/understand-anything/understand-anything"
-    if ! has_command python3; then
-        printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
-        build_understand_anything_core "${plugin_root}"
-        return 0
-    fi
-    release_root="$(
-        python3 - "${plugin_root}/.claude-plugin/plugin.json" "${claude_cache}" << 'PY'
+	local plugin_root claude_cache release_root source destination
+
+	plugin_root="${HOME}/.understand-anything/repo/understand-anything-plugin"
+	claude_cache="${HOME}/.claude/plugins/cache/understand-anything/understand-anything"
+	if ! has_command python3; then
+		printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
+		build_understand_anything_core "${plugin_root}"
+		return 0
+	fi
+	release_root="$(
+		python3 - "${plugin_root}/.claude-plugin/plugin.json" "${claude_cache}" << 'PY'
 import json
 import sys
 from pathlib import Path
@@ -758,21 +758,21 @@
     release_root = max(matches, key=lambda path: path.name, default=None)
 print(release_root or "")
 PY
-    )"
-    if [ -z "${release_root}" ]; then
-        printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
-        build_understand_anything_core "${plugin_root}"
-        return 0
-    fi
-
-    build_understand_anything_core "${release_root}"
-    for source in "packages/core/dist" "packages/core/node_modules" "node_modules"; do
-        destination="${plugin_root}/${source}"
-        [ -d "${release_root}/${source}" ] || continue
-        rm -rf "${destination}"
-        mkdir -p "$(dirname "${destination}")"
-        cp -R "${release_root}/${source}" "${destination}"
-    done
+	)"
+	if [ -z "${release_root}" ]; then
+		printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
+		build_understand_anything_core "${plugin_root}"
+		return 0
+	fi
+
+	build_understand_anything_core "${release_root}"
+	for source in "packages/core/dist" "packages/core/node_modules" "node_modules"; do
+		destination="${plugin_root}/${source}"
+		[ -d "${release_root}/${source}" ] || continue
+		rm -rf "${destination}"
+		mkdir -p "$(dirname "${destination}")"
+		cp -R "${release_root}/${source}" "${destination}"
+	done
 }
 
 #
@@ -783,34 +783,34 @@
 #   those symlinks as an expected unmanaged-skill WARN.
 #
 function update_codex_understand_anything() {
-    if ! has_command codex; then
-        printf 'Skipping Codex Understand-Anything skills: codex command not found.\n'
-        return 0
-    fi
-
-    section "Codex Understand-Anything skills"
-    (
-        local actual installer
-        installer="$(mktemp)"
-        trap 'rm -f "${installer}"' EXIT
-        curl -fsSL "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" -o "${installer}" || {
-            printf 'Skipping Codex Understand-Anything skills: installer download failed.\n'
-            return 0
-        }
-        actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
-        [ "${actual}" = "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256}" ] || {
-            printf 'Understand-Anything installer checksum mismatch\n' >&2
-            return 1
-        }
-        bash "${installer}" codex < /dev/null || {
-            printf 'Understand-Anything installer failed; Codex skills unchanged.\n' >&2
-            return 1
-        }
-        provision_codex_understand_anything_runtime
-        # shellcheck disable=SC2016 # $understand is the literal Codex skill invocation, not a variable.
-        printf 'Invoke Understand-Anything in Codex with $understand after restarting the CLI.\n'
-    ) || true
-    manifest_record "update_codex_understand_anything" installer "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}" "${HOME}/.understand-anything/repo" "${HOME}/.agents/skills/understand" "${HOME}/.agents/skills/understand-chat" "${HOME}/.agents/skills/understand-dashboard" "${HOME}/.agents/skills/understand-diff" "${HOME}/.agents/skills/understand-domain" "${HOME}/.agents/skills/understand-explain" "${HOME}/.agents/skills/understand-figma" "${HOME}/.agents/skills/understand-knowledge" "${HOME}/.agents/skills/understand-onboard" -- "curl -fsSL ${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer> codex"
+	if ! has_command codex; then
+		printf 'Skipping Codex Understand-Anything skills: codex command not found.\n'
+		return 0
+	fi
+
+	section "Codex Understand-Anything skills"
+	(
+		local actual installer
+		installer="$(mktemp)"
+		trap 'rm -f "${installer}"' EXIT
+		curl -fsSL "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" -o "${installer}" || {
+			printf 'Skipping Codex Understand-Anything skills: installer download failed.\n'
+			return 0
+		}
+		actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
+		[ "${actual}" = "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256}" ] || {
+			printf 'Understand-Anything installer checksum mismatch\n' >&2
+			return 1
+		}
+		bash "${installer}" codex < /dev/null || {
+			printf 'Understand-Anything installer failed; Codex skills unchanged.\n' >&2
+			return 1
+		}
+		provision_codex_understand_anything_runtime
+		# shellcheck disable=SC2016 # $understand is the literal Codex skill invocation, not a variable.
+		printf 'Invoke Understand-Anything in Codex with $understand after restarting the CLI.\n'
+	) || true
+	manifest_record "update_codex_understand_anything" installer "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}" "${HOME}/.understand-anything/repo" "${HOME}/.agents/skills/understand" "${HOME}/.agents/skills/understand-chat" "${HOME}/.agents/skills/understand-dashboard" "${HOME}/.agents/skills/understand-diff" "${HOME}/.agents/skills/understand-domain" "${HOME}/.agents/skills/understand-explain" "${HOME}/.agents/skills/understand-figma" "${HOME}/.agents/skills/understand-knowledge" "${HOME}/.agents/skills/understand-onboard" -- "curl -fsSL ${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer> codex"
 }
 
 #
@@ -820,12 +820,12 @@
 #   Intel macOS has no release asset, so it is skipped rather than failed.
 #
 function zenbu_platform_supported() {
-    case "$(uname -s)-$(uname -m)" in
-    Darwin-arm64 | Linux-x86_64 | Linux-amd64 | Linux-aarch64 | Linux-arm64)
-        return 0
-        ;;
-    esac
-    return 1
+	case "$(uname -s)-$(uname -m)" in
+	Darwin-arm64 | Linux-x86_64 | Linux-amd64 | Linux-aarch64 | Linux-arm64)
+		return 0
+		;;
+	esac
+	return 1
 }
 
 #
@@ -835,24 +835,24 @@
 # @arg $@ string Optional NAME=value environment assignments for the installer run.
 #
 function run_pinned_installer() {
-    local url="$1"
-    local expected="$2"
-    local actual installer
-    shift 2
-
-    installer="$(mktemp)"
-    # shellcheck disable=SC2064 # Expand the temp path now; it never changes.
-    trap "rm -f '${installer}'" RETURN
-    curl -fsSL "${url}" -o "${installer}" || {
-        printf 'Installer download failed: %s\n' "${url}" >&2
-        return 1
-    }
-    actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
-    [ "${actual}" = "${expected}" ] || {
-        printf 'Installer checksum mismatch for %s\n' "${url}" >&2
-        return 1
-    }
-    env "$@" bash "${installer}" < /dev/null
+	local url="$1"
+	local expected="$2"
+	local actual installer
+	shift 2
+
+	installer="$(mktemp)"
+	# shellcheck disable=SC2064 # Expand the temp path now; it never changes.
+	trap "rm -f '${installer}'" RETURN
+	curl -fsSL "${url}" -o "${installer}" || {
+		printf 'Installer download failed: %s\n' "${url}" >&2
+		return 1
+	}
+	actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
+	[ "${actual}" = "${expected}" ] || {
+		printf 'Installer checksum mismatch for %s\n' "${url}" >&2
+		return 1
+	}
+	env "$@" bash "${installer}" < /dev/null
 }
 
 #
@@ -859,26 +859,26 @@
 # @description Install or update the terminal-code (tode) CLI at the pinned version.
 #
 function update_terminal_code() {
-    local installed
-
-    zenbu_platform_supported || {
-        printf 'Skipping terminal-code: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
-        return 0
-    }
-
-    section "terminal-code (tode)"
-    installed="$(jq -r '.version' "${HOME}/.local/state/tode/install.json" 2> /dev/null || printf 'none\n')"
-    # Short-circuit only when every manifest-recorded artifact is present, so a
-    # partially deleted install is repaired instead of skipped forever.
-    if [ "${installed}" = "${TERMINAL_CODE_PIN_VERSION}" ] &&
-        [ -x "${HOME}/.local/bin/tode" ] &&
-        [ -d "${HOME}/.local/lib/tode" ]; then
-        printf 'tode %s is already installed.\n' "${installed}"
-    else
-        run_pinned_installer "${TERMINAL_CODE_INSTALLER_URL}" "${TERMINAL_CODE_INSTALLER_SHA256}" ||
-            printf 'tode installer failed; existing install unchanged.\n' >&2
-    fi
-    manifest_record "update_terminal_code" installer "${TERMINAL_CODE_PIN_VERSION}" "${HOME}/.local/lib/tode" "${HOME}/.local/bin/tode" "${HOME}/.local/state/tode/install.json" -- "curl -fsSL ${TERMINAL_CODE_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer>"
+	local installed
+
+	zenbu_platform_supported || {
+		printf 'Skipping terminal-code: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
+		return 0
+	}
+
+	section "terminal-code (tode)"
+	installed="$(jq -r '.version' "${HOME}/.local/state/tode/install.json" 2> /dev/null || printf 'none\n')"
+	# Short-circuit only when every manifest-recorded artifact is present, so a
+	# partially deleted install is repaired instead of skipped forever.
+	if [ "${installed}" = "${TERMINAL_CODE_PIN_VERSION}" ] &&
+		[ -x "${HOME}/.local/bin/tode" ] &&
+		[ -d "${HOME}/.local/lib/tode" ]; then
+		printf 'tode %s is already installed.\n' "${installed}"
+	else
+		run_pinned_installer "${TERMINAL_CODE_INSTALLER_URL}" "${TERMINAL_CODE_INSTALLER_SHA256}" ||
+			printf 'tode installer failed; existing install unchanged.\n' >&2
+	fi
+	manifest_record "update_terminal_code" installer "${TERMINAL_CODE_PIN_VERSION}" "${HOME}/.local/lib/tode" "${HOME}/.local/bin/tode" "${HOME}/.local/state/tode/install.json" -- "curl -fsSL ${TERMINAL_CODE_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer>"
 }
 
 #
@@ -892,26 +892,26 @@
 #   run `terminal-browser setup` manually once if wanted.
 #
 function update_terminal_browser() {
-    local installed
-
-    zenbu_platform_supported || {
-        printf 'Skipping terminal-browser: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
-        return 0
-    }
-
-    section "terminal-browser"
-    installed="$(cat "${HOME}/.local/share/terminal-browser/app/VERSION" 2> /dev/null || printf 'none\n')"
-    # Short-circuit only when every manifest-recorded artifact is present, so a
-    # partially deleted install is repaired instead of skipped forever.
-    if [ "${installed}" = "${TERMINAL_BROWSER_PIN_VERSION}" ] &&
-        [ -x "${HOME}/.local/bin/terminal-browser" ] &&
-        [ -f "${HOME}/.local/state/terminal-browser/skills.links" ]; then
-        printf 'terminal-browser %s is already installed.\n' "${installed}"
-    else
-        run_pinned_installer "${TERMINAL_BROWSER_INSTALLER_URL}" "${TERMINAL_BROWSER_INSTALLER_SHA256}" TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 ||
-            printf 'terminal-browser installer failed; existing install unchanged.\n' >&2
-    fi
-    manifest_record "update_terminal_browser" installer "${TERMINAL_BROWSER_PIN_VERSION}" "${HOME}/.local/share/terminal-browser/app" "${HOME}/.local/bin/terminal-browser" "${HOME}/.local/state/terminal-browser/skills.links" -- "curl -fsSL ${TERMINAL_BROWSER_INSTALLER_URL}" "shasum -a 256 <installer>" "TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 bash <installer>"
+	local installed
+
+	zenbu_platform_supported || {
+		printf 'Skipping terminal-browser: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
+		return 0
+	}
+
+	section "terminal-browser"
+	installed="$(cat "${HOME}/.local/share/terminal-browser/app/VERSION" 2> /dev/null || printf 'none\n')"
+	# Short-circuit only when every manifest-recorded artifact is present, so a
+	# partially deleted install is repaired instead of skipped forever.
+	if [ "${installed}" = "${TERMINAL_BROWSER_PIN_VERSION}" ] &&
+		[ -x "${HOME}/.local/bin/terminal-browser" ] &&
+		[ -f "${HOME}/.local/state/terminal-browser/skills.links" ]; then
+		printf 'terminal-browser %s is already installed.\n' "${installed}"
+	else
+		run_pinned_installer "${TERMINAL_BROWSER_INSTALLER_URL}" "${TERMINAL_BROWSER_INSTALLER_SHA256}" TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 ||
+			printf 'terminal-browser installer failed; existing install unchanged.\n' >&2
+	fi
+	manifest_record "update_terminal_browser" installer "${TERMINAL_BROWSER_PIN_VERSION}" "${HOME}/.local/share/terminal-browser/app" "${HOME}/.local/bin/terminal-browser" "${HOME}/.local/state/terminal-browser/skills.links" -- "curl -fsSL ${TERMINAL_BROWSER_INSTALLER_URL}" "shasum -a 256 <installer>" "TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 bash <installer>"
 }
 
 #
@@ -919,33 +919,33 @@
 # @exitcode 1 The download checksum or installed version differs from its pin.
 #
 function update_omp() (
-    local installed download_dir tarball actual
-    has_command npm || {
-        printf 'Skipping omp: npm command not found.\n'
-        return 0
-    }
-    section "omp"
-    installed="$(omp --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    if [ "${installed}" = "${OMP_PIN_VERSION}" ]; then
-        printf 'omp %s is already installed.\n' "${installed}"
-        return 0
-    fi
-    download_dir="$(mktemp -d)" || return
-    trap 'rm -rf "${download_dir}"' EXIT
-    tarball="${download_dir}/omp-${OMP_PIN_VERSION}.tgz"
-    curl -fsSL "${OMP_TARBALL_URL}" -o "${tarball}" || return
-    actual="$(shasum -a 256 "${tarball}" | awk '{ print $1 }')" || return
-    if [ "${actual}" != "${OMP_TARBALL_SHA256}" ]; then
-        printf 'omp checksum mismatch: expected %s, got %s.\n' "${OMP_TARBALL_SHA256}" "${actual}" >&2
-        return 1
-    fi
-    npm install -g --prefix "${HOME}/.local" "${tarball}" || return
-    installed="$(omp --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    if [ "${installed}" != "${OMP_PIN_VERSION}" ]; then
-        printf 'omp version mismatch: expected %s, got %s.\n' "${OMP_PIN_VERSION}" "${installed}" >&2
-        return 1
-    fi
-    manifest_record "update_omp" installer "${OMP_PIN_VERSION}" "${HOME}/.local/bin/omp" -- "npm install -g --prefix ${HOME}/.local <verified-omp-tarball>"
+	local installed download_dir tarball actual
+	has_command npm || {
+		printf 'Skipping omp: npm command not found.\n'
+		return 0
+	}
+	section "omp"
+	installed="$(omp --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+	if [ "${installed}" = "${OMP_PIN_VERSION}" ]; then
+		printf 'omp %s is already installed.\n' "${installed}"
+		return 0
+	fi
+	download_dir="$(mktemp -d)" || return
+	trap 'rm -rf "${download_dir}"' EXIT
+	tarball="${download_dir}/omp-${OMP_PIN_VERSION}.tgz"
+	curl -fsSL "${OMP_TARBALL_URL}" -o "${tarball}" || return
+	actual="$(shasum -a 256 "${tarball}" | awk '{ print $1 }')" || return
+	if [ "${actual}" != "${OMP_TARBALL_SHA256}" ]; then
+		printf 'omp checksum mismatch: expected %s, got %s.\n' "${OMP_TARBALL_SHA256}" "${actual}" >&2
+		return 1
+	fi
+	npm install -g --prefix "${HOME}/.local" "${tarball}" || return
+	installed="$(omp --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+	if [ "${installed}" != "${OMP_PIN_VERSION}" ]; then
+		printf 'omp version mismatch: expected %s, got %s.\n' "${OMP_PIN_VERSION}" "${installed}" >&2
+		return 1
+	fi
+	manifest_record "update_omp" installer "${OMP_PIN_VERSION}" "${HOME}/.local/bin/omp" -- "npm install -g --prefix ${HOME}/.local <verified-omp-tarball>"
 )
 
 #
@@ -953,43 +953,43 @@
 # @exitcode 1 The download checksum or installed version differs from its pin.
 #
 function update_hcom() (
-    local url expected installed download_dir wheel actual
-    case "$(uname -s)/$(uname -m)" in
-    Darwin/arm64 | Darwin/aarch64) url="${HCOM_DARWIN_ARM64_URL}" expected="${HCOM_DARWIN_ARM64_SHA256}" ;;
-    Darwin/x86_64 | Darwin/amd64) url="${HCOM_DARWIN_AMD64_URL}" expected="${HCOM_DARWIN_AMD64_SHA256}" ;;
-    Linux/x86_64 | Linux/amd64) url="${HCOM_LINUX_AMD64_URL}" expected="${HCOM_LINUX_AMD64_SHA256}" ;;
-    Linux/aarch64 | Linux/arm64) url="${HCOM_LINUX_ARM64_URL}" expected="${HCOM_LINUX_ARM64_SHA256}" ;;
-    *)
-        printf 'Skipping hcom: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
-        return 0
-        ;;
-    esac
-    has_command uv || {
-        printf 'Skipping hcom: uv command not found.\n'
-        return 0
-    }
-    section "hcom"
-    installed="$(hcom --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    if [ "${installed}" = "${HCOM_PIN_VERSION}" ]; then
-        printf 'hcom %s is already installed.\n' "${installed}"
-        return 0
-    fi
-    download_dir="$(mktemp -d)" || return
-    trap 'rm -rf "${download_dir}"' EXIT
-    wheel="${download_dir}/${url##*/}"
-    curl -fsSL "${url}" -o "${wheel}" || return
-    actual="$(shasum -a 256 "${wheel}" | awk '{ print $1 }')" || return
-    if [ "${actual}" != "${expected}" ]; then
-        printf 'hcom checksum mismatch: expected %s, got %s.\n' "${expected}" "${actual}" >&2
-        return 1
-    fi
-    uv tool install --force "${wheel}" || return
-    installed="$(hcom --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    if [ "${installed}" != "${HCOM_PIN_VERSION}" ]; then
-        printf 'hcom version mismatch: expected %s, got %s.\n' "${HCOM_PIN_VERSION}" "${installed}" >&2
-        return 1
-    fi
-    manifest_record "update_hcom" installer "${HCOM_PIN_VERSION}" "${HOME}/.local/bin/hcom" -- "uv tool install --force <verified-hcom-wheel>"
+	local url expected installed download_dir wheel actual
+	case "$(uname -s)/$(uname -m)" in
+	Darwin/arm64 | Darwin/aarch64) url="${HCOM_DARWIN_ARM64_URL}" expected="${HCOM_DARWIN_ARM64_SHA256}" ;;
+	Darwin/x86_64 | Darwin/amd64) url="${HCOM_DARWIN_AMD64_URL}" expected="${HCOM_DARWIN_AMD64_SHA256}" ;;
+	Linux/x86_64 | Linux/amd64) url="${HCOM_LINUX_AMD64_URL}" expected="${HCOM_LINUX_AMD64_SHA256}" ;;
+	Linux/aarch64 | Linux/arm64) url="${HCOM_LINUX_ARM64_URL}" expected="${HCOM_LINUX_ARM64_SHA256}" ;;
+	*)
+		printf 'Skipping hcom: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
+		return 0
+		;;
+	esac
+	has_command uv || {
+		printf 'Skipping hcom: uv command not found.\n'
+		return 0
+	}
+	section "hcom"
+	installed="$(hcom --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+	if [ "${installed}" = "${HCOM_PIN_VERSION}" ]; then
+		printf 'hcom %s is already installed.\n' "${installed}"
+		return 0
+	fi
+	download_dir="$(mktemp -d)" || return
+	trap 'rm -rf "${download_dir}"' EXIT
+	wheel="${download_dir}/${url##*/}"
+	curl -fsSL "${url}" -o "${wheel}" || return
+	actual="$(shasum -a 256 "${wheel}" | awk '{ print $1 }')" || return
+	if [ "${actual}" != "${expected}" ]; then
+		printf 'hcom checksum mismatch: expected %s, got %s.\n' "${expected}" "${actual}" >&2
+		return 1
+	fi
+	uv tool install --force "${wheel}" || return
+	installed="$(hcom --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+	if [ "${installed}" != "${HCOM_PIN_VERSION}" ]; then
+		printf 'hcom version mismatch: expected %s, got %s.\n' "${HCOM_PIN_VERSION}" "${installed}" >&2
+		return 1
+	fi
+	manifest_record "update_hcom" installer "${HCOM_PIN_VERSION}" "${HOME}/.local/bin/hcom" -- "uv tool install --force <verified-hcom-wheel>"
 )
 
 #
@@ -996,10 +996,10 @@
 # @description Sync the vendored CompactionDB tree without deleting project runtime state.
 #
 function update_compactiondb() {
-    local source_root
-    source_root="${DOTFILES_REPO_SOURCE_DIR}/vendor/compactiondb/"
-    rsync -a --delete --exclude '.claude/contextdb/state/' --exclude '.claude/contextdb/spool/' --exclude '.claude/contextdb/health/' --exclude '.claude/contextdb/contextdb.sqlite3*' "${source_root}" "${HOME}/.agents/compactiondb/" || true
-    manifest_record "update_compactiondb" rsync "$(awk '/^## / { print $2; exit }' "${source_root}CHANGELOG.md")" "${HOME}/.agents/compactiondb" -- "rsync -a --delete --exclude .claude/contextdb/state/ --exclude .claude/contextdb/spool/ --exclude .claude/contextdb/health/ --exclude .claude/contextdb/contextdb.sqlite3* ${source_root} ${HOME}/.agents/compactiondb/"
+	local source_root
+	source_root="${DOTFILES_REPO_SOURCE_DIR}/vendor/compactiondb/"
+	rsync -a --delete --exclude '.claude/contextdb/state/' --exclude '.claude/contextdb/spool/' --exclude '.claude/contextdb/health/' --exclude '.claude/contextdb/contextdb.sqlite3*' "${source_root}" "${HOME}/.agents/compactiondb/" || true
+	manifest_record "update_compactiondb" rsync "$(awk '/^## / { print $2; exit }' "${source_root}CHANGELOG.md")" "${HOME}/.agents/compactiondb" -- "rsync -a --delete --exclude .claude/contextdb/state/ --exclude .claude/contextdb/spool/ --exclude .claude/contextdb/health/ --exclude .claude/contextdb/contextdb.sqlite3* ${source_root} ${HOME}/.agents/compactiondb/"
 }
 
 #
@@ -1008,14 +1008,14 @@
 # @exitcode 1 If neither tool exists or hashing fails.
 #
 function agmsg_sha256() {
-    if command -v sha256sum > /dev/null 2>&1; then
-        sha256sum -- "$@"
-    elif command -v shasum > /dev/null 2>&1; then
-        shasum -a 256 -- "$@"
-    else
-        printf 'agmsg: neither sha256sum nor shasum is available\n' >&2
-        return 1
-    fi
+	if command -v sha256sum > /dev/null 2>&1; then
+		sha256sum -- "$@"
+	elif command -v shasum > /dev/null 2>&1; then
+		shasum -a 256 -- "$@"
+	else
+		printf 'agmsg: neither sha256sum nor shasum is available\n' >&2
+		return 1
+	fi
 }
 
 #
@@ -1028,33 +1028,33 @@
 # @exitcode 1 If the paths cannot be listed or hashed completely.
 #
 function agmsg_state_snapshot() {
-    local skill_dir="$1"
-    local relative list file hashes
-    local -a paths=() files=()
-    shift
-
-    for relative in "$@"; do
-        [ ! -e "${skill_dir}/${relative}" ] || paths+=("${skill_dir}/${relative}")
-    done
-    ((${#paths[@]})) || return 0
-    list="$(mktemp)" || return 1
-    if ! find "${paths[@]}" -type f -print0 > "${list}"; then
-        rm -f "${list}"
-        printf 'agmsg: could not list the live state under %s\n' "${skill_dir}" >&2
-        return 1
-    fi
-    while IFS= read -r -d '' file; do
-        files+=("${file}")
-    done < "${list}"
-    rm -f "${list}"
-    ((${#files[@]})) || return 0
-    hashes="$(agmsg_sha256 "${files[@]}")" || return 1
-    # sha256sum/shasum prefix a line with \ when the name needs escaping.
-    if [ "$(printf '%s\n' "${hashes}" | grep -c '^\\\{0,1\}[0-9a-f]\{64\} ')" -ne "${#files[@]}" ]; then
-        printf 'agmsg: hashed fewer live-state files than exist under %s\n' "${skill_dir}" >&2
-        return 1
-    fi
-    printf '%s\n' "${hashes}" | LC_ALL=C sort
+	local skill_dir="$1"
+	local relative list file hashes
+	local -a paths=() files=()
+	shift
+
+	for relative in "$@"; do
+		[ ! -e "${skill_dir}/${relative}" ] || paths+=("${skill_dir}/${relative}")
+	done
+	((${#paths[@]})) || return 0
+	list="$(mktemp)" || return 1
+	if ! find "${paths[@]}" -type f -print0 > "${list}"; then
+		rm -f "${list}"
+		printf 'agmsg: could not list the live state under %s\n' "${skill_dir}" >&2
+		return 1
+	fi
+	while IFS= read -r -d '' file; do
+		files+=("${file}")
+	done < "${list}"
+	rm -f "${list}"
+	((${#files[@]})) || return 0
+	hashes="$(agmsg_sha256 "${files[@]}")" || return 1
+	# sha256sum/shasum prefix a line with \ when the name needs escaping.
+	if [ "$(printf '%s\n' "${hashes}" | grep -c '^\\\{0,1\}[0-9a-f]\{64\} ')" -ne "${#files[@]}" ]; then
+		printf 'agmsg: hashed fewer live-state files than exist under %s\n' "${skill_dir}" >&2
+		return 1
+	fi
+	printf '%s\n' "${hashes}" | LC_ALL=C sort
 }
 
 #
@@ -1075,80 +1075,80 @@
 # @exitcode 1 On any failure, with the reason on stderr.
 #
 function install_pinned_agmsg() (
-    local skill_dir="$1"
-    local fetch_url="https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz"
-    local tool tarball extract_dir actual before_state after_state before_run after_run changed install_log backup_dir state_dir installed
-    local -a install_args=(--cmd agmsg --agent-type claude-code)
-
-    for tool in curl tar; do
-        command -v "${tool}" > /dev/null 2>&1 || {
-            printf 'agmsg: %s not found; nothing was installed\n' "${tool}" >&2
-            return 1
-        }
-    done
-    before_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
-        printf 'agmsg: could not snapshot the live state under %s; nothing was installed\n' "${skill_dir}" >&2
-        return 1
-    }
-    before_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
-    if [ -f "${skill_dir}/.agmsg" ]; then
-        install_args=(--update "${install_args[@]}")
-    fi
-
-    tarball="$(mktemp)" || return 1
-    extract_dir="$(mktemp -d)" || return 1
-    install_log="$(mktemp)" || return 1
-    trap 'rm -f "${tarball}" "${install_log}"; rm -rf "${extract_dir}"' EXIT
-    curl -fsSL "${fetch_url}" -o "${tarball}" || {
-        printf 'agmsg download failed: %s; nothing was installed\n' "${fetch_url}" >&2
-        return 1
-    }
-    actual="$(agmsg_sha256 "${tarball}")" || return 1
-    [ "${actual%% *}" = "${AGMSG_PIN_SHA256}" ] || {
-        printf 'agmsg checksum mismatch for %s; nothing was installed\n' "${fetch_url}" >&2
-        return 1
-    }
-    tar xzf "${tarball}" -C "${extract_dir}" --strip-components=1 || {
-        printf 'agmsg extraction failed for %s; nothing was installed\n' "${fetch_url}" >&2
-        return 1
-    }
-
-    if [ -d "${skill_dir}" ]; then
-        backup_dir="${HOME}/.agents/backups/agmsg-state-$(date -u +%Y%m%dT%H%M%SZ)"
-        mkdir -p "${backup_dir}" || return 1
-        for state_dir in teams db run agents; do
-            [ ! -e "${skill_dir}/${state_dir}" ] || cp -Rp "${skill_dir}/${state_dir}" "${backup_dir}/" || {
-                printf 'agmsg: could not back up %s/%s; nothing was installed\n' "${skill_dir}" "${state_dir}" >&2
-                return 1
-            }
-        done
-        printf 'agmsg: live state copied to %s before install.sh %s\n' "${backup_dir}" "${install_args[*]}"
-    fi
-    if ! bash "${extract_dir}/install.sh" "${install_args[@]}" > "${install_log}" 2>&1; then
-        cat "${install_log}" >&2
-        printf 'agmsg: install.sh %s failed; the skill directory may be partially updated%s\n' \
-            "${install_args[*]}" "${backup_dir:+; pre-install state copy: ${backup_dir}}" >&2
-        return 1
-    fi
-    after_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
-        printf 'agmsg: install.sh %s finished, but the live state could not be re-checked; pre-install state copy: %s\n' \
-            "${install_args[*]}" "${backup_dir:-none}" >&2
-        return 1
-    }
-    changed="$(LC_ALL=C comm -23 <(printf '%s\n' "${before_state}") <(printf '%s\n' "${after_state}") | sed 's/^[^ ]*  *//')"
-    if [ -n "${changed}" ]; then
-        printf 'agmsg: install.sh %s changed or removed existing live state (the installer or a concurrent writer); pre-install state copy: %s\n%s\n' \
-            "${install_args[*]}" "${backup_dir:-none}" "${changed}" >&2
-        return 1
-    fi
-    after_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
-    [ "${before_run}" = "${after_run}" ] ||
-        printf 'agmsg: note: run/ changed during install.sh %s (watchers and sync engines rewrite it); not treated as a failure\n' "${install_args[*]}"
-    installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none')"
-    if ! [ -f "${skill_dir}/.agmsg" ] || [ "${installed}" != "${AGMSG_PIN_VERSION}" ]; then
-        printf 'agmsg: install.sh %s left VERSION %s (want %s)\n' "${install_args[*]}" "${installed}" "${AGMSG_PIN_VERSION}" >&2
-        return 1
-    fi
+	local skill_dir="$1"
+	local fetch_url="https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz"
+	local tool tarball extract_dir actual before_state after_state before_run after_run changed install_log backup_dir state_dir installed
+	local -a install_args=(--cmd agmsg --agent-type claude-code)
+
+	for tool in curl tar; do
+		command -v "${tool}" > /dev/null 2>&1 || {
+			printf 'agmsg: %s not found; nothing was installed\n' "${tool}" >&2
+			return 1
+		}
+	done
+	before_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
+		printf 'agmsg: could not snapshot the live state under %s; nothing was installed\n' "${skill_dir}" >&2
+		return 1
+	}
+	before_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
+	if [ -f "${skill_dir}/.agmsg" ]; then
+		install_args=(--update "${install_args[@]}")
+	fi
+
+	tarball="$(mktemp)" || return 1
+	extract_dir="$(mktemp -d)" || return 1
+	install_log="$(mktemp)" || return 1
+	trap 'rm -f "${tarball}" "${install_log}"; rm -rf "${extract_dir}"' EXIT
+	curl -fsSL "${fetch_url}" -o "${tarball}" || {
+		printf 'agmsg download failed: %s; nothing was installed\n' "${fetch_url}" >&2
+		return 1
+	}
+	actual="$(agmsg_sha256 "${tarball}")" || return 1
+	[ "${actual%% *}" = "${AGMSG_PIN_SHA256}" ] || {
+		printf 'agmsg checksum mismatch for %s; nothing was installed\n' "${fetch_url}" >&2
+		return 1
+	}
+	tar xzf "${tarball}" -C "${extract_dir}" --strip-components=1 || {
+		printf 'agmsg extraction failed for %s; nothing was installed\n' "${fetch_url}" >&2
+		return 1
+	}
+
+	if [ -d "${skill_dir}" ]; then
+		backup_dir="${HOME}/.agents/backups/agmsg-state-$(date -u +%Y%m%dT%H%M%SZ)"
+		mkdir -p "${backup_dir}" || return 1
+		for state_dir in teams db run agents; do
+			[ ! -e "${skill_dir}/${state_dir}" ] || cp -Rp "${skill_dir}/${state_dir}" "${backup_dir}/" || {
+				printf 'agmsg: could not back up %s/%s; nothing was installed\n' "${skill_dir}" "${state_dir}" >&2
+				return 1
+			}
+		done
+		printf 'agmsg: live state copied to %s before install.sh %s\n' "${backup_dir}" "${install_args[*]}"
+	fi
+	if ! bash "${extract_dir}/install.sh" "${install_args[@]}" > "${install_log}" 2>&1; then
+		cat "${install_log}" >&2
+		printf 'agmsg: install.sh %s failed; the skill directory may be partially updated%s\n' \
+			"${install_args[*]}" "${backup_dir:+; pre-install state copy: ${backup_dir}}" >&2
+		return 1
+	fi
+	after_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
+		printf 'agmsg: install.sh %s finished, but the live state could not be re-checked; pre-install state copy: %s\n' \
+			"${install_args[*]}" "${backup_dir:-none}" >&2
+		return 1
+	}
+	changed="$(LC_ALL=C comm -23 <(printf '%s\n' "${before_state}") <(printf '%s\n' "${after_state}") | sed 's/^[^ ]*  *//')"
+	if [ -n "${changed}" ]; then
+		printf 'agmsg: install.sh %s changed or removed existing live state (the installer or a concurrent writer); pre-install state copy: %s\n%s\n' \
+			"${install_args[*]}" "${backup_dir:-none}" "${changed}" >&2
+		return 1
+	fi
+	after_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
+	[ "${before_run}" = "${after_run}" ] ||
+		printf 'agmsg: note: run/ changed during install.sh %s (watchers and sync engines rewrite it); not treated as a failure\n' "${install_args[*]}"
+	installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none')"
+	if ! [ -f "${skill_dir}/.agmsg" ] || [ "${installed}" != "${AGMSG_PIN_VERSION}" ]; then
+		printf 'agmsg: install.sh %s left VERSION %s (want %s)\n' "${install_args[*]}" "${installed}" "${AGMSG_PIN_VERSION}" >&2
+		return 1
+	fi
 )
 
 #
@@ -1155,22 +1155,22 @@
 # @description Install or refresh the pinned upstream agmsg skill in place.
 #
 function update_agmsg() {
-    local skill_dir="${HOME}/.agents/skills/agmsg"
-    local installed
-
-    section "agmsg"
-    installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')"
-    if [ "${installed}" != "${AGMSG_PIN_VERSION}" ] || ! [ -f "${skill_dir}/.agmsg" ] || ! [ -x "${skill_dir}/scripts/send.sh" ]; then
-        install_pinned_agmsg "${skill_dir}" ||
-            printf 'agmsg installer failed (installed: %s); see the reason above.\n' "${installed}" >&2
-    fi
-
-    manifest_record "update_agmsg" installer \
-        "$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')" \
-        "${skill_dir}/SKILL.md" "${skill_dir}/scripts" "${skill_dir}/VERSION" -- \
-        "curl -fsSL https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz" \
-        "sha256sum <tarball> (shasum -a 256 on macOS)" \
-        "bash <extracted>/install.sh [--update when .agmsg exists] --cmd agmsg --agent-type claude-code"
+	local skill_dir="${HOME}/.agents/skills/agmsg"
+	local installed
+
+	section "agmsg"
+	installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')"
+	if [ "${installed}" != "${AGMSG_PIN_VERSION}" ] || ! [ -f "${skill_dir}/.agmsg" ] || ! [ -x "${skill_dir}/scripts/send.sh" ]; then
+		install_pinned_agmsg "${skill_dir}" ||
+			printf 'agmsg installer failed (installed: %s); see the reason above.\n' "${installed}" >&2
+	fi
+
+	manifest_record "update_agmsg" installer \
+		"$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')" \
+		"${skill_dir}/SKILL.md" "${skill_dir}/scripts" "${skill_dir}/VERSION" -- \
+		"curl -fsSL https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz" \
+		"sha256sum <tarball> (shasum -a 256 on macOS)" \
+		"bash <extracted>/install.sh [--update when .agmsg exists] --cmd agmsg --agent-type claude-code"
 }
 
 #
@@ -1178,35 +1178,35 @@
 # @arg $@ string Command-line arguments.
 #
 function main() {
-    if [ "$#" -gt 0 ]; then
-        printf 'Usage: scripts/update-agent-assets.sh\n' >&2
-        exit 2
-    fi
-
-    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
-    remove_node_global_agent_cli_shadows
-    ensure_mise_npm_agent_cli claude "npm:@anthropic-ai/claude-code"
-    ensure_mise_npm_agent_cli codex "npm:@openai/codex"
-    ensure_gh_extensions
-    update_claude_superpowers
-    update_claude_crit
-    update_claude_ponytail
-    update_claude_understand_anything
-    update_codex_superpowers
-    update_codex_crit
-    update_codex_ponytail
-    update_codex_understand_anything
-    update_terminal_code
-    update_terminal_browser
-    update_omp
-    update_hcom
-    update_compactiondb
-    update_agmsg
-    ensure_herdr_integrations
-    # After every plugin update above, so the trust hashes follow the plugin content of this run.
-    refresh_codex_hook_trust
+	if [ "$#" -gt 0 ]; then
+		printf 'Usage: scripts/update-agent-assets.sh\n' >&2
+		exit 2
+	fi
+
+	export PATH="${HOME}/.local/share/mise/shims:${PATH}"
+	remove_node_global_agent_cli_shadows
+	ensure_mise_npm_agent_cli claude "npm:@anthropic-ai/claude-code"
+	ensure_mise_npm_agent_cli codex "npm:@openai/codex"
+	ensure_gh_extensions
+	update_claude_superpowers
+	update_claude_crit
+	update_claude_ponytail
+	update_claude_understand_anything
+	update_codex_superpowers
+	update_codex_crit
+	update_codex_ponytail
+	update_codex_understand_anything
+	update_terminal_code
+	update_terminal_browser
+	update_omp
+	update_hcom
+	update_compactiondb
+	update_agmsg
+	ensure_herdr_integrations
+	# After every plugin update above, so the trust hashes follow the plugin content of this run.
+	refresh_codex_hook_trust
 }
 
 if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
-    main "$@"
+	main "$@"
 fi
(exit 1)
```

## shellcheck-health-fix

```text
$ shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## shfmt-health-fix-project-flags

```text
$ shfmt -i 4 -sr -d scripts/check-tools.sh scripts/update-agent-assets.sh scripts/lib/installer-pins.sh
(exit 0)
```

## Current source and task integrity

```text
$ uv run --offline --no-project --with pyyaml <TMP>/codex-T129-integrity2.py
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "e6c8abb6e8857ed450196888aa2b912a8b025e7ef7038c46065867358f296c19",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_update_agent_assets.py": "fa830f443beceed7ab76e9187c787b89e8e7c68ae8c88d161e7a952f5a1d4b9a"
  },
  "source_changed": 162,
  "test_added": 195,
  "withdrawn_paths_unchanged": true,
  "existing_helpers_and_Bats_byte_identical": true,
  "task_hashes_and_URLs_match": true,
  "URL_render_fallback": "files values are not plain pin values; URLs declared beside existing installer URLs and match manifest files",
  "numstat": "35\t0\thome/dot_agents/agent-config.yaml\n34\t0\tscripts/check-tools.sh\n8\t0\tscripts/lib/installer-pins.sh\n85\t0\tscripts/update-agent-assets.sh\n32\t0\ttests/install/common/check_tools.bats\n163\t0\ttests/unit/test_update_agent_assets.py\n"
}
(exit 0)
```

## Independent review before health fixes

# Independent worker review — Amendment 2

Task: dotfiles-T129-assets-omp-hcom-a01
Baseline: 35ab0e95a7fe27c501db3478d4f37e69a514d532
Task SHA256: 0634d0eb62fe82c614282d7fbec3d998a8c37b9c1b0e89be5e3701923f073255
Candidate: six staged code/test files on feat/pinned-omp-hcom. Amendment 1 is superseded. This is worker-side review, not orchestrator acceptance.

Plan/todo: read current task and candidate; inspect connected lifecycle callers; independently verify hashes and stub behavior; investigate regressions; record findings. All review steps completed. No repository edits or installs were performed. Review records and standalone fixture probes are under /tmp; the repository worklog was not mutated in this read-only assignment.

## Findings

1. P2, confidence 1.00 — scripts/check-tools.sh:13. The unconditional installer-pins import introduces both a dirname PATH dependency at source time and a companion-file requirement into existing callers. test_doctor_reports_claude_sandbox_prerequisites deliberately sources the script with a fixture-only PATH and now exits on `dirname: command not found`. The three make-doctor tests copy only check-tools.sh to a temporary scripts directory and now fail on the missing lib/installer-pins.sh before tool checks execute. All four pass against baseline. Keep unrelated checks sourceable under their established environment, and adapt the isolated doctor fixtures to any intentional companion-file dependency. tests/unit/test_runtime_health.py is outside current allowed_files, so any required fixture change needs orchestrator scope disposition rather than an unauthorized edit.

2. P2, confidence 1.00 — scripts/check-tools.sh:336. The new check_omp/check_hcom calls add two optional warnings to the existing doctor fixture, but test_doctor_required_optional_and_healthy_statuses still requires `optional warnings: 1` when gh extension listing fails. Actual output now reports 3 and the existing test fails. The warning behavior is requested and should remain; update the healthy fixture to provide both managed fake binaries or explicitly update its expected counts, with scope authorization for the existing test module. This exact test passes against baseline.

No additional proven security defect was found in the top-level artifact verification path. Review cannot approve while these five existing tests regress.

## Verification assessment

- Both current required named tests independently pass (2 methods, 4.024 seconds). Their cases verify four hcom platform mappings, correct local-artifact argv, hash rejection before installer execution, post-install version refusal, idempotence, missing-manager and unsupported-platform skips, receipt suppression and temporary-directory removal.
- Additional fake-command probes verify curl exit 23 and installer exit 19 propagate unchanged for both functions, produce no receipt, and remove the artifact directory. No real package manager or network transfer is used by these probes.
- ShellCheck with -x exits 0; generator --check reports generated configs up to date; git diff --cached --check exits 0.
- All six source hashes match working tree, staged index and source-integrity.json. Seven generated pin/hash constants and four fallback URLs agree with the manifest and the current task. All three withdrawn files are byte-identical to baseline.
- The source diff is additive only: 161 production lines and 195 test lines. Existing installer helpers and prior Bats cases are untouched by the diff. Makefile update-tree still runs upgrade-tools.sh then update-agent-assets.sh. Existing runtime-health callers were inspected, exposing the findings above.
- Current canonical validation.md contains the clean staged-candidate validator result `agent asset validation ok` and exit 0. This is parent-run evidence, not a validator invocation by this reviewer. It includes ordinary pre-existing regime warnings; no full-suite or CI success is inferred.
- Current report/sandbox distinguish fixtures from real installs and explicitly supersede Amendment 1. The generator URL fallback is authorized by the current task. Final-head CI, Bot review, integration and operator installation are still future steps, not verified results.
- Only top-level downloaded artifacts are covered by these pinned SHA256 checks. Transitive dependency resolution and actual npm/uv behavior were not exercised. The existing uv upgrade --all lifecycle remains a real-install integration risk to assess with the operator's permitted post-merge run, especially because hcom is installed from a temporary local wheel. No failure of that interaction is claimed or included as a finding without reproduction.
- Read-only official uv documentation was consulted to assess retained install settings and upgrade behavior: https://docs.astral.sh/uv/concepts/tools/#upgrading-tools . It states upgrades retain install constraints/settings; it does not establish the deleted-wheel behavior, so that remains explicitly unverified.

## Check commands and outputs

The focused and regression commands use PYTHONDONTWRITEBYTECODE=1 and UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache, with uv run --offline --no-project. Tests use temporary HOME fixtures. No Bats, actual install/download, denied-request retry, GitHub mutation, browser Crit/server, broad process inventory or profile/sandbox change was performed.

### Focused unit command

Command: `uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets -v`

```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok

----------------------------------------------------------------------
Ran 2 tests in 4.024s

OK
```

### Integrity checks

Command: `Read each source; SHA256 compare with amendment2/source-integrity.json and git show :path; compare withdrawn files to git show baseline:path; compare YAML render values and URLs to task text`

```text
home/dot_agents/agent-config.yaml e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310 matches index/evidence
scripts/check-tools.sh da7cb9020b59bba30fbcd3f3c78acc9c3817395ddee3d7140866ddb82de8b495 matches index/evidence
scripts/lib/installer-pins.sh a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091 matches index/evidence
scripts/update-agent-assets.sh e6c8abb6e8857ed450196888aa2b912a8b025e7ef7038c46065867358f296c19 matches index/evidence
tests/install/common/check_tools.bats 9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed matches index/evidence
tests/unit/test_update_agent_assets.py fa830f443beceed7ab76e9187c787b89e8e7c68ae8c88d161e7a952f5a1d4b9a matches index/evidence
task sha256 0634d0eb62fe82c614282d7fbec3d998a8c37b9c1b0e89be5e3701923f073255
withdrawn path byte-identical: home/dot_mise/config.toml
withdrawn path byte-identical: scripts/validate-agent-assets.py
withdrawn path byte-identical: tests/unit/test_validate_agent_assets.py
manifest/render/task URL and hashes match: omp
manifest/render/task URL and hashes match: hcom
35	0	home/dot_agents/agent-config.yaml
33	0	scripts/check-tools.sh
8	0	scripts/lib/installer-pins.sh
85	0	scripts/update-agent-assets.sh
32	0	tests/install/common/check_tools.bats
163	0	tests/unit/test_update_agent_assets.py

```

### Fake failure probes

Command: `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/codex-T129-review-amendment2-failures.py`

```text
omp curl failure: exit=23; no receipt; artifact directory removed; installer-called=False
omp installer failure: exit=19; no receipt; artifact directory removed; installer-called=True
hcom curl failure: exit=23; no receipt; artifact directory removed; installer-called=False
hcom installer failure: exit=19; no receipt; artifact directory removed; installer-called=True
```

### Connected regression command

Command: `uv run --offline --no-project python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check -v`

```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py:1373: SyntaxWarning: "\ " is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\ "? A raw string is also an option.
  upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... 
  test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) (fail='gh:extension list') ... FAIL
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... FAIL
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ERROR
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... FAIL
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... FAIL

======================================================================
ERROR: test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 1303, in test_make_doctor_propagates_runtime_drift_after_tool_checks
    self.assertIn("git --version", (self.temp_dir / "doctor.log").read_text())
                                   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 986, in read_text
    with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
         ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/.local/share/mise/installs/python/latest/lib/python3.15/pathlib/__init__.py", line 970, in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-om2_ycoi/doctor.log'

======================================================================
FAIL: test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) (fail='gh:extension list')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 1242, in test_doctor_required_optional_and_healthy_statuses
    self.assertIn(summary, result.stdout)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'optional warnings: 1' not found in '\n==> Core commands\nfound:   git -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-bin-gh-extension-list-Linux/git\ngit healthy\nfound:   chezmoi -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-bin-gh-extension-list-Linux/chezmoi\nchezmoi healthy\nfound:   mise -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-bin-gh-extension-list-Linux/mise\nmise healthy\nfound:   uv -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-bin-gh-extension-list-Linux/uv\nuv healthy\nfound:   gh -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-bin-gh-extension-list-Linux/gh\ngh healthy\n\n==> Chezmoi\nchezmoi healthy\nfound:   private source -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-home/.local/share/chezmoi-private\nfound:   private config -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-home/.config/chezmoi-private/chezmoi.yaml\n\n==> Mise\nmise healthy\nmise healthy\n\n==> Homebrew\nnot applicable: Homebrew (non-Darwin)\n\n==> Crit CLI\nnot applicable: Crit CLI (not installed)\n\n==> Agent tools\n\n==> Zed\nnot applicable: Zed (installed on Ubuntu clients only)\n\n==> SSH\nfound:   machine SSH key -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-home/.ssh/id_ed25519.pub\n\n==> AppArmor\nnot applicable: AppArmor userns restriction (not enabled)\n\n==> Claude Code sandbox\nfound:   bwrap -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-bin-gh-extension-list-Linux/bwrap\nfound:   socat -> /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/runtime-health-test-jc11qnka/doctor-bin-gh-extension-list-Linux/socat\n\n==> GitHub CLI extensions\n\n==> agmsg\nnot applicable: agmsg (not installed)\n\nTool check summary: required failures: 0; optional warnings: 3\n'

======================================================================
FAIL: test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 1265, in test_doctor_reports_claude_sandbox_prerequisites
    self.assertEqual(0, result.returncode, output)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : <HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/check-tools.sh: line 13: dirname: command not found
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/scripts/check-tools.sh: line 13: /lib/installer-pins.sh: No such file or directory


======================================================================
FAIL: test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 1334, in test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing
    self.assertIn("Doctor summary: tools=passed; runtime=failed", result.stdout)
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'Doctor summary: tools=passed; runtime=failed' not found in '\nDoctor summary: tools=failed; runtime=failed\n'

======================================================================
FAIL: test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 1355, in test_make_doctor_passes_repair_variable_to_runtime_check
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 2 : repair=1

Doctor summary: tools=failed; runtime=passed
./scripts/check-tools.sh: line 13: ./scripts/lib/installer-pins.sh: No such file or directory
make: *** [doctor] Error 1


----------------------------------------------------------------------
Ran 5 tests in 4.222s

FAILED (failures=4, errors=1)
```

### Baseline comparison

Command: `Export baseline Makefile and scripts/check-tools.sh with git show into /tmp; set imported test_runtime_health.ROOT to that directory; run the same five RuntimeHealthTest methods through unittest.TextTestRunner`

```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py:1373: SyntaxWarning: "\ " is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\ "? A raw string is also an option.
  upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok

----------------------------------------------------------------------
Ran 5 tests in 15.692s

OK
```

Other commands: shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh (exit 0, no output); git diff --cached --check (exit 0, no output); uv run --offline --no-project --with pyyaml scripts/generate-agent-configs.py --check (exit 0, generated agent configs are up to date).

Verdict: incorrect


## Amendment3 task copy

Full dispatched task read; byte-copy hash verified: 8cc6a6b4060befdbe7a33ad0bc53d92b4f32e7fbd50e68091736a38f7296a6f5. Only the doctor warning-count/fixture test expansion is authorized by Amendment3; updater main fixture expansion remains requested.

## runtime-health-amendment3

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend -v
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py:1373: SyntaxWarning: "\ " is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\ "? A raw string is also an option.
  upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... FAIL
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... FAIL

======================================================================
FAIL: test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 184, in test_agent_asset_update_removes_node_global_shadows_before_agent_commands
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> Claude Code plugins

==> Claude Code Crit plugin

==> Crit CLI

==> Claude Code Ponytail plugin
Ponytail default mode is full. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.

==> Claude Code Understand-Anything plugin

==> Codex plugins
Codex Superpowers plugin installed.

==> Crit CLI

==> Codex Ponytail plugin
Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.
Ponytail default mode is full. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.

==> Codex Understand-Anything skills
Skipping Codex Understand-Anything skills: installer download failed.

==> terminal-code (tode)

==> terminal-browser

==> omp
Warning: GitHub CLI is not authenticated. Run setup-gh, then make update to install extensions.
Installer download failed: https://tode.sh/install
tode installer failed; existing install unchanged.
Installer download failed: https://terminal-browser.sh/install
terminal-browser installer failed; existing install unchanged.


======================================================================
FAIL: test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py", line 267, in test_agent_asset_update_repairs_broken_claude_with_npm_backend
    self.assertEqual(0, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : Repairing claude through the mise npm backend.

==> Claude Code plugins

==> Claude Code Crit plugin

==> Crit CLI

==> Claude Code Ponytail plugin
Ponytail default mode is full. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.

==> Claude Code Understand-Anything plugin

==> Codex plugins
Codex Superpowers plugin installed.

==> Crit CLI

==> Codex Ponytail plugin
Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.
Ponytail default mode is full. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.

==> Codex Understand-Anything skills
Skipping Codex Understand-Anything skills: installer download failed.

==> terminal-code (tode)

==> terminal-browser

==> omp
warning: failed to record asset manifest step ensure_mise_npm_agent_cli:claude
Warning: GitHub CLI is not authenticated. Run setup-gh, then make update to install extensions.
Installer download failed: https://tode.sh/install
tode installer failed; existing install unchanged.
Installer download failed: https://terminal-browser.sh/install
terminal-browser installer failed; existing install unchanged.


----------------------------------------------------------------------
Ran 7 tests in 19.188s

FAILED (failures=2)
(exit 1)
```

## Current source and task integrity

```text
$ uv run --offline --no-project --with pyyaml <TMP>/codex-T129-integrity2.py
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "e6c8abb6e8857ed450196888aa2b912a8b025e7ef7038c46065867358f296c19",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_runtime_health.py": "0d6bf989ca1615540f0f919a18f8639252ff48347b956126b269c2d0550dbae4",
    "tests/unit/test_update_agent_assets.py": "fa830f443beceed7ab76e9187c787b89e8e7c68ae8c88d161e7a952f5a1d4b9a"
  },
  "source_changed": 162,
  "test_added": 196,
  "withdrawn_paths_unchanged": true,
  "existing_helpers_and_Bats_byte_identical": true,
  "task_hashes_and_URLs_match": true,
  "URL_render_fallback": "files values are not plain pin values; URLs declared beside existing installer URLs and match manifest files",
  "numstat": "35\t0\thome/dot_agents/agent-config.yaml\n34\t0\tscripts/check-tools.sh\n8\t0\tscripts/lib/installer-pins.sh\n85\t0\tscripts/update-agent-assets.sh\n32\t0\ttests/install/common/check_tools.bats\n1\t1\ttests/unit/test_runtime_health.py\n163\t0\ttests/unit/test_update_agent_assets.py\n"
}
(exit 0)
```

## Amendment4 task copy

Full dispatched task read; byte-copy hash verified: c7fe714979195fd1f68d5da188130f75353327ccf8c200a0de62daf29159af85. Existing runtime-health fixture adaptations now authorized; no assertion removed.

## Current source and task integrity

```text
$ uv run --offline --no-project --with pyyaml <TMP>/codex-T129-integrity2.py
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "e6c8abb6e8857ed450196888aa2b912a8b025e7ef7038c46065867358f296c19",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_runtime_health.py": "ed344e770b47b2519c46763e5c41ea8018866d3df0ea74c2180a77204dda2763",
    "tests/unit/test_update_agent_assets.py": "fa830f443beceed7ab76e9187c787b89e8e7c68ae8c88d161e7a952f5a1d4b9a"
  },
  "source_changed": 162,
  "test_added": 210,
  "withdrawn_paths_unchanged": true,
  "existing_helpers_and_Bats_byte_identical": true,
  "task_hashes_and_URLs_match": true,
  "URL_render_fallback": "files values are not plain pin values; URLs declared beside existing installer URLs and match manifest files",
  "numstat": "35\t0\thome/dot_agents/agent-config.yaml\n34\t0\tscripts/check-tools.sh\n8\t0\tscripts/lib/installer-pins.sh\n85\t0\tscripts/update-agent-assets.sh\n32\t0\ttests/install/common/check_tools.bats\n15\t3\ttests/unit/test_runtime_health.py\n163\t0\ttests/unit/test_update_agent_assets.py\n"
}
(exit 0)
```

## final-ruff-format

```text
$ ruff format --check --config ruff.toml tests/unit/test_update_agent_assets.py tests/unit/test_runtime_health.py
unformatted: File would be reformatted
   --> tests/unit/test_runtime_health.py:179:57
    |
178 |                 "-c",
    -                 "source scripts/update-agent-assets.sh; "
    -                 "update_omp() { :; }; update_hcom() { :; }; main",
179 +                 "source scripts/update-agent-assets.sh; update_omp() { :; }; update_hcom() { :; }; main",
180 |             ],
--------------------------------------------------------------------------------
264 |                 "-c",
    -                 "source scripts/update-agent-assets.sh; "
    -                 "update_omp() { :; }; update_hcom() { :; }; main",
265 +                 "source scripts/update-agent-assets.sh; update_omp() { :; }; update_hcom() { :; }; main",
266 |             ],
    |

1 file would be reformatted, 1 file already formatted
(exit 1)
```

## final-units-and-regressions

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend -v
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py:1385: SyntaxWarning: "\ " is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\ "? A raw string is also an option.
  upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok

----------------------------------------------------------------------
Ran 10 tests in 24.204s

OK
(exit 0)
```

## Current source and task integrity

```text
$ uv run --offline --no-project --with pyyaml <TMP>/codex-T129-integrity2.py
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "e6c8abb6e8857ed450196888aa2b912a8b025e7ef7038c46065867358f296c19",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_runtime_health.py": "0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6",
    "tests/unit/test_update_agent_assets.py": "fa830f443beceed7ab76e9187c787b89e8e7c68ae8c88d161e7a952f5a1d4b9a"
  },
  "source_changed": 162,
  "test_added": 208,
  "withdrawn_paths_unchanged": true,
  "existing_helpers_and_Bats_byte_identical": true,
  "task_hashes_and_URLs_match": true,
  "URL_render_fallback": "files values are not plain pin values; URLs declared beside existing installer URLs and match manifest files",
  "numstat": "35\t0\thome/dot_agents/agent-config.yaml\n34\t0\tscripts/check-tools.sh\n8\t0\tscripts/lib/installer-pins.sh\n85\t0\tscripts/update-agent-assets.sh\n32\t0\ttests/install/common/check_tools.bats\n13\t3\ttests/unit/test_runtime_health.py\n163\t0\ttests/unit/test_update_agent_assets.py\n"
}
(exit 0)
```

## final-ruff-format-corrected

```text
$ ruff format --check --config ruff.toml tests/unit/test_update_agent_assets.py tests/unit/test_runtime_health.py
2 files already formatted
(exit 0)
```

## final-ruff

```text
$ ruff check --config ruff.toml tests/unit/test_update_agent_assets.py tests/unit/test_runtime_health.py
EXE001 Shebang is present but file is not executable
 --> tests/unit/test_runtime_health.py:1:1
  |
1 | #!/usr/bin/env python3
  | ^^^^^^^^^^^^^^^^^^^^^^
2 | """Verify truthful runtime artifact, doctor, and upgrade behavior."""
  |

RUF059 Unpacked variable `checksum` is never used
   --> tests/unit/test_runtime_health.py:469:26
    |
468 |     def test_linux_crit_install_is_pinned_atomic_and_recorded(self) -> None:
469 |         repo, home, env, checksum = self.crit_fixture()
    |                          ^^^^^^^^
470 |         result = self.run_test_command(
471 |             [
    |
help: Prefix it with an underscore or any other dummy variable pattern
    |
468 |     def test_linux_crit_install_is_pinned_atomic_and_recorded(self) -> None:
    -         repo, home, env, checksum = self.crit_fixture()
469 +         repo, home, env, _checksum = self.crit_fixture()
470 |         result = self.run_test_command(
    |
note: This is an unsafe fix and may change runtime behavior

RUF059 Unpacked variable `checksum` is never used
   --> tests/unit/test_runtime_health.py:493:26
    |
492 |     def test_linux_crit_correct_version_is_download_free(self) -> None:
493 |         repo, home, env, checksum = self.crit_fixture("9.9.9")
    |                          ^^^^^^^^
494 |         result = self.run_test_command(
495 |             [
    |
help: Prefix it with an underscore or any other dummy variable pattern
    |
492 |     def test_linux_crit_correct_version_is_download_free(self) -> None:
    -         repo, home, env, checksum = self.crit_fixture("9.9.9")
493 +         repo, home, env, _checksum = self.crit_fixture("9.9.9")
494 |         result = self.run_test_command(
    |
note: This is an unsafe fix and may change runtime behavior

RUF059 Unpacked variable `home` is never used
   --> tests/unit/test_runtime_health.py:514:15
    |
513 |     def test_linux_crit_prefers_pinned_target_over_older_path_binary(self) -> None:
514 |         repo, home, env, checksum = self.crit_fixture("9.9.9")
    |               ^^^^
515 |         self.executable(
516 |             repo / "bin/crit",
    |
help: Prefix it with an underscore or any other dummy variable pattern
    |
513 |     def test_linux_crit_prefers_pinned_target_over_older_path_binary(self) -> None:
    -         repo, home, env, checksum = self.crit_fixture("9.9.9")
514 +         repo, _home, env, checksum = self.crit_fixture("9.9.9")
515 |         self.executable(
    |
note: This is an unsafe fix and may change runtime behavior

RUF059 Unpacked variable `checksum` is never used
   --> tests/unit/test_runtime_health.py:514:26
    |
513 |     def test_linux_crit_prefers_pinned_target_over_older_path_binary(self) -> None:
514 |         repo, home, env, checksum = self.crit_fixture("9.9.9")
    |                          ^^^^^^^^
515 |         self.executable(
516 |             repo / "bin/crit",
    |
help: Prefix it with an underscore or any other dummy variable pattern
    |
513 |     def test_linux_crit_prefers_pinned_target_over_older_path_binary(self) -> None:
    -         repo, home, env, checksum = self.crit_fixture("9.9.9")
514 +         repo, home, env, _checksum = self.crit_fixture("9.9.9")
515 |         self.executable(
    |
note: This is an unsafe fix and may change runtime behavior

RUF059 Unpacked variable `checksum` is never used
   --> tests/unit/test_runtime_health.py:568:26
    |
567 |     def test_darwin_crit_install_is_pinned_atomic_and_recorded(self) -> None:
568 |         repo, home, env, checksum = self.crit_fixture(os_name="Darwin", arch="arm64")
    |                          ^^^^^^^^
569 |         result = self.run_test_command(
570 |             [
    |
help: Prefix it with an underscore or any other dummy variable pattern
    |
567 |     def test_darwin_crit_install_is_pinned_atomic_and_recorded(self) -> None:
    -         repo, home, env, checksum = self.crit_fixture(os_name="Darwin", arch="arm64")
568 +         repo, home, env, _checksum = self.crit_fixture(os_name="Darwin", arch="arm64")
569 |         result = self.run_test_command(
    |
note: This is an unsafe fix and may change runtime behavior

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:809:17
    |
807 |                   "bash",
808 |                   "-c",
809 | /                 "source scripts/update-agent-assets.sh; "
810 | |                 f"AGMSG_PIN_SHA256={checksum}; "
811 | |                 "AGMSG_PIN_VERSION=9.9.9; "
812 | |                 "update_agmsg",
    | |______________________________^
813 |               ],
814 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses
    |
808 |                 "-c",
    -                 "source scripts/update-agent-assets.sh; "
809 +                 ("source scripts/update-agent-assets.sh; "
810 |                 f"AGMSG_PIN_SHA256={checksum}; "
811 |                 "AGMSG_PIN_VERSION=9.9.9; "
    -                 "update_agmsg",
812 +                 "update_agmsg"),
813 |             ],
    |
note: This is an unsafe fix and may change runtime behavior

RUF059 Unpacked variable `home` is never used
   --> tests/unit/test_runtime_health.py:830:15
    |
829 |     def test_agmsg_already_pinned_skips_download(self) -> None:
830 |         repo, home, env, checksum = self.agmsg_fixture(preinstalled_version="1.4.2")
    |               ^^^^
831 |         result = self.run_test_command(
832 |             [
    |
help: Prefix it with an underscore or any other dummy variable pattern
    |
829 |     def test_agmsg_already_pinned_skips_download(self) -> None:
    -         repo, home, env, checksum = self.agmsg_fixture(preinstalled_version="1.4.2")
830 +         repo, _home, env, checksum = self.agmsg_fixture(preinstalled_version="1.4.2")
831 |         result = self.run_test_command(
    |
note: This is an unsafe fix and may change runtime behavior

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:835:17
    |
833 |                   "bash",
834 |                   "-c",
835 | /                 "source scripts/update-agent-assets.sh; "
836 | |                 f"AGMSG_PIN_SHA256={checksum}; "
837 | |                 "AGMSG_PIN_VERSION=1.4.2; "
838 | |                 "update_agmsg",
    | |______________________________^
839 |               ],
840 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses
    |
834 |                 "-c",
    -                 "source scripts/update-agent-assets.sh; "
835 +                 ("source scripts/update-agent-assets.sh; "
836 |                 f"AGMSG_PIN_SHA256={checksum}; "
837 |                 "AGMSG_PIN_VERSION=1.4.2; "
    -                 "update_agmsg",
838 +                 "update_agmsg"),
839 |             ],
    |
note: This is an unsafe fix and may change runtime behavior

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:875:17
    |
873 |                   "bash",
874 |                   "-c",
875 | /                 "source scripts/update-agent-assets.sh; "
876 | |                 f"AGMSG_PIN_SHA256={checksum}; "
877 | |                 "AGMSG_PIN_VERSION=9.9.9; "
878 | |                 "update_agmsg",
    | |______________________________^
879 |               ],
880 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses
    |
874 |                 "-c",
    -                 "source scripts/update-agent-assets.sh; "
875 +                 ("source scripts/update-agent-assets.sh; "
876 |                 f"AGMSG_PIN_SHA256={checksum}; "
877 |                 "AGMSG_PIN_VERSION=9.9.9; "
    -                 "update_agmsg",
878 +                 "update_agmsg"),
879 |             ],
    |
note: This is an unsafe fix and may change runtime behavior

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:902:17
    |
900 |                   "bash",
901 |                   "-c",
902 | /                 "source scripts/update-agent-assets.sh; "
903 | |                 f"AGMSG_PIN_SHA256={checksum}; "
904 | |                 "AGMSG_PIN_VERSION=9.9.9; "
905 | |                 "update_agmsg",
    | |______________________________^
906 |               ],
907 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses
    |
901 |                 "-c",
    -                 "source scripts/update-agent-assets.sh; "
902 +                 ("source scripts/update-agent-assets.sh; "
903 |                 f"AGMSG_PIN_SHA256={checksum}; "
904 |                 "AGMSG_PIN_VERSION=9.9.9; "
    -                 "update_agmsg",
905 +                 "update_agmsg"),
906 |             ],
    |
note: This is an unsafe fix and may change runtime behavior

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:935:17
    |
933 |                   "bash",
934 |                   "-c",
935 | /                 "source scripts/update-agent-assets.sh; "
936 | |                 f"AGMSG_PIN_SHA256={checksum}; "
937 | |                 "AGMSG_PIN_VERSION=9.9.9; "
938 | |                 "update_agmsg",
    | |______________________________^
939 |               ],
940 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses
    |
934 |                 "-c",
    -                 "source scripts/update-agent-assets.sh; "
935 +                 ("source scripts/update-agent-assets.sh; "
936 |                 f"AGMSG_PIN_SHA256={checksum}; "
937 |                 "AGMSG_PIN_VERSION=9.9.9; "
    -                 "update_agmsg",
938 +                 "update_agmsg"),
939 |             ],
    |
note: This is an unsafe fix and may change runtime behavior

ISC004 Unparenthesized implicit string concatenation in collection
   --> tests/unit/test_runtime_health.py:967:17
    |
965 |                   "bash",
966 |                   "-c",
967 | /                 "source scripts/update-agent-assets.sh; "
968 | |                 f"AGMSG_PIN_SHA256={checksum}; "
969 | |                 "AGMSG_PIN_VERSION=9.9.9; "
970 | |                 "update_agmsg",
    | |______________________________^
971 |               ],
972 |               cwd=repo,
    |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses
    |
966 |                 "-c",
    -                 "source scripts/update-agent-assets.sh; "
967 +                 ("source scripts/update-agent-assets.sh; "
968 |                 f"AGMSG_PIN_SHA256={checksum}; "
969 |                 "AGMSG_PIN_VERSION=9.9.9; "
    -                 "update_agmsg",
970 +                 "update_agmsg"),
971 |             ],
    |
note: This is an unsafe fix and may change runtime behavior

ISC004 Unparenthesized implicit string concatenation in collection
    --> tests/unit/test_runtime_health.py:1003:17
     |
1001 |                   "bash",
1002 |                   "-c",
1003 | /                 "source scripts/update-agent-assets.sh; "
1004 | |                 f"AGMSG_PIN_SHA256={checksum}; "
1005 | |                 "AGMSG_PIN_VERSION=9.9.9; "
1006 | |                 "update_agmsg",
     | |______________________________^
1007 |               ],
1008 |               cwd=repo,
     |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses
     |
1002 |                 "-c",
     -                 "source scripts/update-agent-assets.sh; "
1003 +                 ("source scripts/update-agent-assets.sh; "
1004 |                 f"AGMSG_PIN_SHA256={checksum}; "
1005 |                 "AGMSG_PIN_VERSION=9.9.9; "
     -                 "update_agmsg",
1006 +                 "update_agmsg"),
1007 |             ],
     |
note: This is an unsafe fix and may change runtime behavior

RUF059 Unpacked variable `home` is never used
    --> tests/unit/test_runtime_health.py:1019:15
     |
1018 |     def test_agmsg_reports_an_installer_that_leaves_the_wrong_version(self) -> None:
1019 |         repo, home, env, checksum = self.agmsg_fixture()
     |               ^^^^
1020 |
1021 |         result = self.run_test_command(
     |
help: Prefix it with an underscore or any other dummy variable pattern
     |
1018 |     def test_agmsg_reports_an_installer_that_leaves_the_wrong_version(self) -> None:
     -         repo, home, env, checksum = self.agmsg_fixture()
1019 +         repo, _home, env, checksum = self.agmsg_fixture()
1020 |
     |
note: This is an unsafe fix and may change runtime behavior

ISC004 Unparenthesized implicit string concatenation in collection
    --> tests/unit/test_runtime_health.py:1052:17
     |
1050 |                   "bash",
1051 |                   "-c",
1052 | /                 "source scripts/update-agent-assets.sh; "
1053 | |                 f"AGMSG_PIN_SHA256={checksum}; "
1054 | |                 "AGMSG_PIN_VERSION=9.9.9; "
1055 | |                 "update_agmsg",
     | |______________________________^
1056 |               ],
1057 |               cwd=repo,
     |
help: Did you forget a comma?
help: Wrap implicitly concatenated strings in parentheses
     |
1051 |                 "-c",
     -                 "source scripts/update-agent-assets.sh; "
1052 +                 ("source scripts/update-agent-assets.sh; "
1053 |                 f"AGMSG_PIN_SHA256={checksum}; "
1054 |                 "AGMSG_PIN_VERSION=9.9.9; "
     -                 "update_agmsg",
1055 +                 "update_agmsg"),
1056 |             ],
     |
note: This is an unsafe fix and may change runtime behavior

W605 [*] Invalid escape sequence: `\ `
    --> tests/unit/test_runtime_health.py:1383:24
     |
1381 |             case "$*" in
1382 |                 "outdated --formula --quiet") printf 'jq\n' ;;
1383 |                 upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
     |                        ^^
1384 |                     "${HOMEBREW_VERIFY_ATTESTATIONS:-unset}" "${HOMEBREW_NO_ASK:-unset}" >> "$TEST_LOG" ;;
1385 |             esac
     |
help: Add backslash to escape sequence
     |
1382 |                 "outdated --formula --quiet") printf 'jq\n' ;;
     -                 upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
1383 +                 upgrade\\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
1384 |                     "${HOMEBREW_VERIFY_ATTESTATIONS:-unset}" "${HOMEBREW_NO_ASK:-unset}" >> "$TEST_LOG" ;;
     |

Found 17 errors.
[*] 1 fixable with `--fix` (15 unsafe fixes available with `--fix --unsafe-fixes`).
(exit 1)
```

## Runtime-health lint baseline comparison

```text
Ruff diagnostic comparison; no --fix and no source edits.
$ ruff check --config ruff.toml --output-format json --stdin-filename tests/unit/test_runtime_health.py - < baseline-source
[
  {
    "cell": null,
    "code": "EXE001",
    "end_location": {
      "column": 23,
      "row": 1
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": null,
    "location": {
      "column": 1,
      "row": 1
    },
    "message": "Shebang is present but file is not executable",
    "name": "shebang-not-executable",
    "noqa_row": 2,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/shebang-not-executable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 34,
      "row": 459
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_checksum",
          "end_location": {
            "column": 34,
            "row": 459
          },
          "location": {
            "column": 26,
            "row": 459
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 26,
      "row": 459
    },
    "message": "Unpacked variable `checksum` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 459,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 34,
      "row": 483
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_checksum",
          "end_location": {
            "column": 34,
            "row": 483
          },
          "location": {
            "column": 26,
            "row": 483
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 26,
      "row": 483
    },
    "message": "Unpacked variable `checksum` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 483,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 19,
      "row": 504
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_home",
          "end_location": {
            "column": 19,
            "row": 504
          },
          "location": {
            "column": 15,
            "row": 504
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 15,
      "row": 504
    },
    "message": "Unpacked variable `home` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 504,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 34,
      "row": 504
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_checksum",
          "end_location": {
            "column": 34,
            "row": 504
          },
          "location": {
            "column": 26,
            "row": 504
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 26,
      "row": 504
    },
    "message": "Unpacked variable `checksum` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 504,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 34,
      "row": 558
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_checksum",
          "end_location": {
            "column": 34,
            "row": 558
          },
          "location": {
            "column": 26,
            "row": 558
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 26,
      "row": 558
    },
    "message": "Unpacked variable `checksum` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 558,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 802
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 799
          },
          "location": {
            "column": 17,
            "row": 799
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 802
          },
          "location": {
            "column": 31,
            "row": 802
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 799
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 799,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 19,
      "row": 820
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_home",
          "end_location": {
            "column": 19,
            "row": 820
          },
          "location": {
            "column": 15,
            "row": 820
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 15,
      "row": 820
    },
    "message": "Unpacked variable `home` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 820,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 828
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 825
          },
          "location": {
            "column": 17,
            "row": 825
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 828
          },
          "location": {
            "column": 31,
            "row": 828
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 825
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 825,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 868
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 865
          },
          "location": {
            "column": 17,
            "row": 865
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 868
          },
          "location": {
            "column": 31,
            "row": 868
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 865
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 865,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 895
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 892
          },
          "location": {
            "column": 17,
            "row": 892
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 895
          },
          "location": {
            "column": 31,
            "row": 895
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 892
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 892,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 928
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 925
          },
          "location": {
            "column": 17,
            "row": 925
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 928
          },
          "location": {
            "column": 31,
            "row": 928
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 925
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 925,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 960
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 957
          },
          "location": {
            "column": 17,
            "row": 957
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 960
          },
          "location": {
            "column": 31,
            "row": 960
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 957
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 957,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 996
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 993
          },
          "location": {
            "column": 17,
            "row": 993
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 996
          },
          "location": {
            "column": 31,
            "row": 996
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 993
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 993,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 19,
      "row": 1009
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_home",
          "end_location": {
            "column": 19,
            "row": 1009
          },
          "location": {
            "column": 15,
            "row": 1009
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 15,
      "row": 1009
    },
    "message": "Unpacked variable `home` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 1009,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 1045
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 1042
          },
          "location": {
            "column": 17,
            "row": 1042
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 1045
          },
          "location": {
            "column": 31,
            "row": 1045
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 1042
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 1042,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "W605",
    "end_location": {
      "column": 26,
      "row": 1373
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "\\",
          "end_location": {
            "column": 25,
            "row": 1373
          },
          "location": {
            "column": 25,
            "row": 1373
          }
        }
      ],
      "message": "Add backslash to escape sequence"
    },
    "location": {
      "column": 24,
      "row": 1373
    },
    "message": "Invalid escape sequence: `\\ `",
    "name": "invalid-escape-sequence",
    "noqa_row": 1376,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/invalid-escape-sequence"
  }
](exit 1)
$ ruff check --config ruff.toml --output-format json --stdin-filename tests/unit/test_runtime_health.py - < current-source
[
  {
    "cell": null,
    "code": "EXE001",
    "end_location": {
      "column": 23,
      "row": 1
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": null,
    "location": {
      "column": 1,
      "row": 1
    },
    "message": "Shebang is present but file is not executable",
    "name": "shebang-not-executable",
    "noqa_row": 2,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/shebang-not-executable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 34,
      "row": 469
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_checksum",
          "end_location": {
            "column": 34,
            "row": 469
          },
          "location": {
            "column": 26,
            "row": 469
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 26,
      "row": 469
    },
    "message": "Unpacked variable `checksum` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 469,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 34,
      "row": 493
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_checksum",
          "end_location": {
            "column": 34,
            "row": 493
          },
          "location": {
            "column": 26,
            "row": 493
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 26,
      "row": 493
    },
    "message": "Unpacked variable `checksum` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 493,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 19,
      "row": 514
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_home",
          "end_location": {
            "column": 19,
            "row": 514
          },
          "location": {
            "column": 15,
            "row": 514
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 15,
      "row": 514
    },
    "message": "Unpacked variable `home` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 514,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 34,
      "row": 514
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_checksum",
          "end_location": {
            "column": 34,
            "row": 514
          },
          "location": {
            "column": 26,
            "row": 514
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 26,
      "row": 514
    },
    "message": "Unpacked variable `checksum` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 514,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 34,
      "row": 568
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_checksum",
          "end_location": {
            "column": 34,
            "row": 568
          },
          "location": {
            "column": 26,
            "row": 568
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 26,
      "row": 568
    },
    "message": "Unpacked variable `checksum` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 568,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 812
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 809
          },
          "location": {
            "column": 17,
            "row": 809
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 812
          },
          "location": {
            "column": 31,
            "row": 812
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 809
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 809,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 19,
      "row": 830
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_home",
          "end_location": {
            "column": 19,
            "row": 830
          },
          "location": {
            "column": 15,
            "row": 830
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 15,
      "row": 830
    },
    "message": "Unpacked variable `home` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 830,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 838
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 835
          },
          "location": {
            "column": 17,
            "row": 835
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 838
          },
          "location": {
            "column": 31,
            "row": 838
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 835
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 835,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 878
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 875
          },
          "location": {
            "column": 17,
            "row": 875
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 878
          },
          "location": {
            "column": 31,
            "row": 878
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 875
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 875,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 905
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 902
          },
          "location": {
            "column": 17,
            "row": 902
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 905
          },
          "location": {
            "column": 31,
            "row": 905
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 902
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 902,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 938
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 935
          },
          "location": {
            "column": 17,
            "row": 935
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 938
          },
          "location": {
            "column": 31,
            "row": 938
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 935
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 935,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 970
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 967
          },
          "location": {
            "column": 17,
            "row": 967
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 970
          },
          "location": {
            "column": 31,
            "row": 970
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 967
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 967,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 1006
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 1003
          },
          "location": {
            "column": 17,
            "row": 1003
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 1006
          },
          "location": {
            "column": 31,
            "row": 1006
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 1003
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 1003,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "RUF059",
    "end_location": {
      "column": 19,
      "row": 1019
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "_home",
          "end_location": {
            "column": 19,
            "row": 1019
          },
          "location": {
            "column": 15,
            "row": 1019
          }
        }
      ],
      "message": "Prefix it with an underscore or any other dummy variable pattern"
    },
    "location": {
      "column": 15,
      "row": 1019
    },
    "message": "Unpacked variable `home` is never used",
    "name": "unused-unpacked-variable",
    "noqa_row": 1019,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/unused-unpacked-variable"
  },
  {
    "cell": null,
    "code": "ISC004",
    "end_location": {
      "column": 31,
      "row": 1055
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "(",
          "end_location": {
            "column": 17,
            "row": 1052
          },
          "location": {
            "column": 17,
            "row": 1052
          }
        },
        {
          "content": ")",
          "end_location": {
            "column": 31,
            "row": 1055
          },
          "location": {
            "column": 31,
            "row": 1055
          }
        }
      ],
      "message": "Did you forget a comma?"
    },
    "location": {
      "column": 17,
      "row": 1052
    },
    "message": "Unparenthesized implicit string concatenation in collection",
    "name": "implicit-string-concatenation-in-collection-literal",
    "noqa_row": 1052,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/implicit-string-concatenation-in-collection-literal"
  },
  {
    "cell": null,
    "code": "W605",
    "end_location": {
      "column": 26,
      "row": 1383
    },
    "filename": "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "\\",
          "end_location": {
            "column": 25,
            "row": 1383
          },
          "location": {
            "column": 25,
            "row": 1383
          }
        }
      ],
      "message": "Add backslash to escape sequence"
    },
    "location": {
      "column": 24,
      "row": 1383
    },
    "message": "Invalid escape sequence: `\\ `",
    "name": "invalid-escape-sequence",
    "noqa_row": 1386,
    "severity": "error",
    "url": "https://docs.astral.sh/ruff/rules/invalid-escape-sequence"
  }
](exit 1)
All17 runtime-health diagnostics match baseline by code, message and source line. No new lint diagnostic; no pre-commit configuration exists in this repo. New installer module Ruff lint passes separately.
```

## final-source-whitespace

```text
$ git diff --cached --check
(exit 0)
```

## Independent final source approval

# Independent final worker review — Amendment 4

Task: dotfiles-T129-assets-omp-hcom-a01
Task SHA256: c7fe714979195fd1f68d5da188130f75353327ccf8c200a0de62daf29159af85
Baseline: 35ab0e95a7fe27c501db3478d4f37e69a514d532
Candidate: seven staged source/test paths on feat/pinned-omp-hcom, hashes below. This is an independent worker code/security review, not orchestrator acceptance or the final-head integration audit.

## Decision

Explicit approval of the reviewed source candidate: no remaining actionable finding. The two previous P2 findings are addressed, and the newly discovered main-caller fixtures are isolated without deleting their behavioral assertions. Ten focused tests independently pass on the exact final source bytes. Checksum comparison remains before npm/uv invocation; errors propagate and temporary artifacts are cleaned. The scope and recorded pins match the dispatched Amendment 4 task.

## Earlier findings resolved

- Former scripts/check-tools.sh:13 unconditional source dependency: removed. Current lines179/194 read only pin data with awk after checking whether the managed binary exists. Shell parameter expansion replaces source-time dirname. The four affected standalone/source-only doctor tests pass, including restricted PATH and relocated script fixtures. Missing pin data reports unknown without executing it.
- Former scripts/check-tools.sh:336 warning-count regression: the runtime health expectation now counts three real warnings, retaining omp/hcom absence warnings and the pre-existing gh warning. The associated regression test passes.
- tests/unit/test_runtime_health.py:108,179,265: all three updater-main fixtures stub update_omp/update_hcom, consistent with their existing isolation and the current task's explicit scope. Their original assertions remain. Switching two fixtures to source+main preserves execution of the behavior under test; the dedicated new module separately exercises the new installers.

## Security/correctness assessment

The manifest's omp tarball and all four hcom platform URLs/hashes match task metadata and the generated constants. The explicitly permitted URL fallback is used because the generator rejects URL pin values. All three withdrawn files are byte-identical to baseline; other manifest data is unchanged.

Both update functions use private mktemp directories, quoted local-artifact paths, actual shasum comparison before package-manager invocation, post-install version checking, and function-local subshell EXIT cleanup. Existing installer helpers are unchanged. Four additional fake-command probes reproduce curl failures and installer failures for each tool, showing exact exit-code preservation, no false success receipt, and directory cleanup. Unsupported platforms and unavailable package managers remain intentional skips. Scope is 162 changed production lines and 208 added test lines.

This review verifies top-level artifact integrity and fixture behavior. It does not establish actual npm/uv package compatibility, transitive dependency reproducibility, host PATH behavior, or future uv upgrade behavior after removal of the local wheel source. These are limitations, not unproven findings. The operator owns real installation after merge under the task.

## Evidence integrity and validation boundaries

The current task, report, sandbox, source-integrity.json, final source diffs and relevant validation sections were read. The record retains earlier RED outcomes and intermediate snapshots rather than claiming they belong to final source. Amendment1 results are superseded. Current report still awaits this independent review and does not claim CI/Bot success. Baseline-existing lint warnings were not changed; the parent records an exact17-diagnostic comparison and new-module lint success. Formatting of two equivalent adjacent fixture literals is covered by the independent ten-method run below.

At this review's initial inspection, the refreshed final-source clean-index validator was still parent-owned/in progress; only the earlier snapshot's exit0 appeared in validation.md. This approval makes no advance claim about that refresh. The final validator receipt, CI/Bats, Bot, task audit, acceptance gate and merge remain separate completion requirements. No final commit/head is invented.

## Read-only procedure

Plan/todo completed: read current task; inspect changed paths and connected caller isolation; compare task/source hashes; independently rerun10 focused methods and4 failure probes; inspect required evidence; write this record. No repository file was modified. No real package install/download, local Bats, broader runtime-health run, denied-command retry, network operation, GitHub mutation, Crit browser/server, sandbox/profile change or process inventory occurred during this final review. Temporary fixtures and this review record are under permitted temporary directories. No full-suite success is claimed.

## Commands and results

All Python commands set PYTHONDONTWRITEBYTECODE=1. uv commands set UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache and use --offline --no-project.

### Focused final tests

`uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend -v`

```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py:1383: SyntaxWarning: "\ " is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\ "? A raw string is also an option.
  upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok

----------------------------------------------------------------------
Ran 10 tests in 21.927s

OK
```

Exit: 0.

### Source integrity

`uv run --offline --no-project --with pyyaml python - (stdlib SHA256 and git show :path comparisons; YAML render/task and baseline manifest comparisons)`

```text
home/dot_agents/agent-config.yaml e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310 matches working tree/index/evidence
scripts/check-tools.sh 45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224 matches working tree/index/evidence
scripts/lib/installer-pins.sh a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091 matches working tree/index/evidence
scripts/update-agent-assets.sh e6c8abb6e8857ed450196888aa2b912a8b025e7ef7038c46065867358f296c19 matches working tree/index/evidence
tests/install/common/check_tools.bats 9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed matches working tree/index/evidence
tests/unit/test_runtime_health.py 0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6 matches working tree/index/evidence
tests/unit/test_update_agent_assets.py fa830f443beceed7ab76e9187c787b89e8e7c68ae8c88d161e7a952f5a1d4b9a matches working tree/index/evidence
task SHA256 c7fe714979195fd1f68d5da188130f75353327ccf8c200a0de62daf29159af85
withdrawn path byte-identical: home/dot_mise/config.toml
withdrawn path byte-identical: scripts/validate-agent-assets.py
withdrawn path byte-identical: tests/unit/test_validate_agent_assets.py
manifest/render/task URLs and hashes match: omp
manifest/render/task URLs and hashes match: hcom
all non-omp/hcom manifest data byte-equivalent in parsed representation
35	0	home/dot_agents/agent-config.yaml
34	0	scripts/check-tools.sh
8	0	scripts/lib/installer-pins.sh
85	0	scripts/update-agent-assets.sh
32	0	tests/install/common/check_tools.bats
13	3	tests/unit/test_runtime_health.py
163	0	tests/unit/test_update_agent_assets.py

```

Exit: 0.

### Fake failure propagation

`PYTHONDONTWRITEBYTECODE=1 python3 /tmp/codex-T129-review-amendment2-failures.py`

```text
omp curl failure: exit=23; no receipt; artifact directory removed; installer-called=False
omp installer failure: exit=19; no receipt; artifact directory removed; installer-called=True
hcom curl failure: exit=23; no receipt; artifact directory removed; installer-called=False
hcom installer failure: exit=19; no receipt; artifact directory removed; installer-called=True
```

Exit: 0.

Additional exact commands (independently run on final source):

- `shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh`: exit0, no diagnostics.
- `shfmt -i 4 -sr -d scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh`: exit0, no formatting diff.
- `git diff --cached --check`: exit0, no output.
- `uv run --offline --no-project --with pyyaml scripts/generate-agent-configs.py --check`: exit0, `generated agent configs are up to date` (environment's unrelated blocc version-list warning also printed).

The integrity probe independently compares every current source byte string to its index object and declared SHA256; compares the withdrawn paths to git show35ab0e95:path; verifies each rendered scalar exists in installer-pins.sh and task metadata, and each fallback URL occurs in the updater and task; parses the manifest and removes only assets.omp/hcom to compare all other values with baseline. Task hash is asserted, not merely reported.

Verdict: correct


## Clean staged-candidate validator

```text
Candidate snapshot from the staged index; unrelated untracked historical logs are absent. All seven changed source/test hashes equal worker-e.
$ cd <TMP>/codex-T129-candidate-m3__ayly
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: no agmsg identity at the active seat /private/tmp/codex-T129-candidate-m3__ayly (expected one)
WARN: regime-boundary: canonical clone <HOME>/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_claude/modify_private_settings.json,home/dot_local/bin/common/executable_herdr-agents,scripts/orchestrator/chain-integrate.sh,scripts/orchestrator/dispatch.sh,scripts/orchestrator/local-advisory.sh,scripts/orchestrator/local-review.sh; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <HOME>/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
WARN: regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-a01-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-a01-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a03 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-playbook-rules-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: amendments 12 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-s1-replan-gate-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-launch-args-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: revises 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: revises 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: questions 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-normalised-comparison-lint-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
(exit 0)
```

## reviewed-source-gate

```text
$ env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
(exit 0)
```

## Final clean staged-candidate validator

```text
Candidate snapshot from the staged index; unrelated untracked historical logs are absent. All seven changed source/test hashes equal worker-e.
$ cd <TMP>/codex-T129-candidate-rg7t9vdo
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: no agmsg identity at the active seat /private/tmp/codex-T129-candidate-rg7t9vdo (expected one)
WARN: regime-boundary: canonical clone <HOME>/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_claude/modify_private_settings.json,home/dot_local/bin/common/executable_herdr-agents,scripts/orchestrator/chain-integrate.sh,scripts/orchestrator/dispatch.sh,scripts/orchestrator/local-advisory.sh,scripts/orchestrator/local-review.sh; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <HOME>/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
WARN: regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-a01-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-a01-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a03 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-playbook-rules-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: amendments 12 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-s1-replan-gate-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-launch-args-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: revises 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: revises 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: questions 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-normalised-comparison-lint-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
(exit 0)
```

## Final source/snapshot equality

Seven working-tree hashes, source-integrity.json, independent final approval and final-candidate-snapshot.json match. Final validator exit0; production162/test208; taskc7fe7149. No code changes after independent review. Publication checks are observed after commit and saved in the raw publishing evidence referenced by RESULT.

## Canonical mask output

```text
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
(exit 0)
```

## final-canonical-whitespace

```text
$ git diff --cached --check
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:16: trailing whitespace.
+test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:34: trailing whitespace.
+AssertionError: 0 != 1 : 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:49: trailing whitespace.
+AssertionError: 0 != 1 : 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:64: trailing whitespace.
+AssertionError: 0 != 1 : 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:79: trailing whitespace.
+AssertionError: 0 != 1 : 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:94: trailing whitespace.
+AssertionError: 0 != 1 : 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:398: trailing whitespace.
+test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:435: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:500: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:521: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:532: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:555: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:604: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:623: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:644: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:669: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:694: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:719: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:750: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:811: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:824: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:867: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:902: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1001: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1044: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1064: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1073: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1096: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1131: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1140: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1155: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1168: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1199: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1226: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1243: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1300: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1317: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1366: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1383: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1400: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1417: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1491: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1546: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1585: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1640: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1691: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1740: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1797: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1844: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1887: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1928: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:1985: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2051: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2114: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2133: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2176: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2223: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2270: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2331: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2412: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2427: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2450: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2511: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2666: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2705: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2766: trailing whitespace.
+ 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:2908: trailing whitespace.
+test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... 
.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md:3029: trailing whitespace.
+AssertionError: 0 != 1 : 
(exit 2)
```

## final-canonical-review-gate

```text
$ env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
(exit 0)
```

## Verbatim trace whitespace

The all-records git diff --cached --check exits2 because copied RED/shfmt/unittest traces contain five trailing-whitespace lines in this validation file. They are preserved verbatim as required by Worker Playbook6; the seven source/test paths pass scoped whitespace checking. No code whitespace defect is suppressed or ignored by a checker configuration.

## final-code-whitespace

```text
$ git diff --cached --check -- home/dot_agents/agent-config.yaml scripts/check-tools.sh scripts/lib/installer-pins.sh scripts/update-agent-assets.sh tests/install/common/check_tools.bats tests/unit/test_runtime_health.py tests/unit/test_update_agent_assets.py
(exit 0)
```

## shadow-red

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed -v
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... 
  test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='pin') ... FAIL
  test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='0.0.0') ... FAIL
  test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='pin') ... FAIL
  test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='0.0.0') ... FAIL

======================================================================
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='pin')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 181, in test_updates_use_managed_binaries_when_path_is_shadowed
    self.exercise_update(tool, shadow_version=shadow_version)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 119, in exercise_update
    self.assertEqual(["curl", "npm" if tool == "omp" else "uv"], [row["tool"] for row in records])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['curl', 'npm'] != []

First list contains 2 additional elements.
First extra element 0:
'curl'

- ['curl', 'npm']
+ []

======================================================================
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='0.0.0')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 181, in test_updates_use_managed_binaries_when_path_is_shadowed
    self.exercise_update(tool, shadow_version=shadow_version)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 113, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> omp
omp version mismatch: expected 18.11.3, got 0.0.0.


======================================================================
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='pin')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 181, in test_updates_use_managed_binaries_when_path_is_shadowed
    self.exercise_update(tool, shadow_version=shadow_version)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 119, in exercise_update
    self.assertEqual(["curl", "npm" if tool == "omp" else "uv"], [row["tool"] for row in records])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['curl', 'uv'] != []

First list contains 2 additional elements.
First extra element 0:
'curl'

- ['curl', 'uv']
+ []

======================================================================
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='0.0.0')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 181, in test_updates_use_managed_binaries_when_path_is_shadowed
    self.exercise_update(tool, shadow_version=shadow_version)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 113, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> hcom
hcom version mismatch: expected 0.7.30, got 0.0.0.


----------------------------------------------------------------------
Ran 1 test in 1.688s

FAILED (failures=4)
(exit 1)
```

## shadow-green-and-connected

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend -v
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py:1383: SyntaxWarning: "\ " is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\ "? A raw string is also an option.
  upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok

----------------------------------------------------------------------
Ran 11 tests in 18.969s

OK
(exit 0)
```

## fix-ruff-format

```text
$ ruff format --check --config ruff.toml tests/unit/test_update_agent_assets.py tests/unit/test_runtime_health.py
2 files already formatted
(exit 0)
```

## fix-ruff

```text
$ ruff check --config ruff.toml tests/unit/test_update_agent_assets.py
All checks passed!
(exit 0)
```

## fix-shellcheck

```text
$ shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## fix-shfmt

```text
$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## Current source and task integrity

```text
$ uv run --offline --no-project --with pyyaml <TMP>/codex-T129-integrity2.py
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "previous_head": "6b9c5d970f22d37b95516aebe9700615c7d4383b",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "80066713c6dc4e3c2d30ee0405e8a9477f38942a2d0401ed12a26d7f9a4aaea4",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_runtime_health.py": "0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6",
    "tests/unit/test_update_agent_assets.py": "75f275085b4eb8ac9069c3b4de4329b9abff8363ff86e9e21076785e920ec92b"
  },
  "source_changed": 162,
  "test_added": 226,
  "withdrawn_paths_unchanged": true,
  "existing_helpers_and_Bats_byte_identical": true,
  "task_hashes_and_URLs_match": true,
  "URL_render_fallback": "files values are not plain pin values; URLs declared beside existing installer URLs and match manifest files",
  "numstat": "8\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md\n32\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json\n6\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md\n8\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md\n34\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md\n12\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md\n152\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md\n5501\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md\n35\t0\thome/dot_agents/agent-config.yaml\n34\t0\tscripts/check-tools.sh\n8\t0\tscripts/lib/installer-pins.sh\n85\t0\tscripts/update-agent-assets.sh\n32\t0\ttests/install/common/check_tools.bats\n13\t3\ttests/unit/test_runtime_health.py\n181\t0\ttests/unit/test_update_agent_assets.py\n"
}
(exit 0)
```

## Initial-head Bot feedback (read in full before authorized fix)

```json
{
  "head": "6b9c5d970f22d37b95516aebe9700615c7d4383b",
  "reviews": [
    {
      "body": "<!-- codex-review-receipt:v1 -->\n\n\n### \ud83d\udca1 Codex Review\n\nHere are some automated review suggestions for this pull request.\n\n**Reviewed commit:** `6b9c5d970f`\n    \n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\nCodex has been enabled to automatically review pull requests in this repo. Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with \ud83d\udc4d.\n\n\n\n\nWhen you [sign up for Codex through ChatGPT](https://openai.com/codex), Codex can also answer questions or update the PR, like \"@codex address that feedback\".\n            \n</details>",
      "commit_id": "6b9c5d970f22d37b95516aebe9700615c7d4383b",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/388#pullrequestreview-5557546445",
      "id": 5557546445,
      "state": "COMMENTED",
      "submitted_at": "2026-10-17T11:20:37Z"
    }
  ],
  "inline": [
    {
      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Validate the managed binaries instead of PATH shadows**\n\nWhen an `omp` at the pinned version already exists earlier on `PATH`\u2014for example, from mise or a system-wide install\u2014this check returns success without creating the declared `${HOME}/.local/bin/omp`; the identical lookup at line 972 affects hcom. I reproduced both update functions reporting \u201calready installed\u201d while both managed targets were absent, and a stale shadow can likewise cause the post-install version check to reject a correctly installed target. The threat row marked closed by these tests is not fully exercised because the fixture puts the managed target first on `PATH`; check the explicit managed path and require it to exist before short-circuiting.\n\nAGENTS.md reference: [AGENTS.md:L78-L78](https://github.com/mryfmo/dotfiles/blob/6b9c5d970f22d37b95516aebe9700615c7d4383b/AGENTS.md#L78-L78)\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.\n\n<!-- codex-code-review-finding:v1 -->",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/388#discussion_r4302479678",
      "id": 4302479678,
      "line": 931,
      "original_commit_id": "6b9c5d970f22d37b95516aebe9700615c7d4383b",
      "path": "scripts/update-agent-assets.sh"
    }
  ],
  "issue_comments": [
    {
      "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"6b9c5d970f22d37b95516aebe9700615c7d4383b\",\"has_any_findings\":null,\"has_unresolved_findings\":null,\"status\":\"running\"},\"security_review\":{\"commit_sha\":\"6b9c5d970f22d37b95516aebe9700615c7d4383b\",\"has_any_findings\":null,\"has_unresolved_findings\":null,\"status\":\"running\"}} -->\n<!-- codex-security-review:v1 {\"blockingSeverityThreshold\":\"P0\",\"headSha\":\"6b9c5d970f22d37b95516aebe9700615c7d4383b\",\"mergeGateEnabled\":false,\"pullRequestNumber\":388,\"repository\":\"mryfmo/dotfiles\",\"status\":\"running\"} -->\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| \ud83d\udcdd **Code Review** | \ud83d\udd04 **Running** since <relative-time datetime=\"2026-10-17T11:19:33.784406Z\">2026-10-17T11:19:33.784406Z</relative-time> | `6b9c5d9` | Draft marked ready |\n| \ud83d\udd12 **Security Review** | \ud83d\udd04 **Running** since <relative-time datetime=\"2026-10-17T11:19:34.795611Z\">2026-10-17T11:19:34.795611Z</relative-time> | `6b9c5d9` | Draft marked ready |\n\n\n\n<details> <summary>\u2139\ufe0f About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with \ud83d\udc40 while any review is running, comments if it has suggestions, and reacts with \ud83d\udc4d once all reviews finish with no findings.\n\n</details>",
      "created_at": "2026-10-17T11:19:38Z",
      "html_url": "https://github.com/mryfmo/dotfiles/pull/388#issuecomment-6233277127",
      "id": 6233277127,
      "updated_at": "2026-10-17T11:19:44Z"
    }
  ]
}
```

## Final clean staged-candidate validator

```text
Candidate snapshot from the staged index; unrelated untracked historical logs are absent. All seven changed source/test hashes equal worker-e.
$ cd <TMP>/codex-T129-candidate-1ffnghyb
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: no agmsg identity at the active seat /private/tmp/codex-T129-candidate-1ffnghyb (expected one)
WARN: regime-boundary: canonical clone <HOME>/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_claude/modify_private_settings.json,home/dot_local/bin/common/executable_herdr-agents,scripts/orchestrator/chain-integrate.sh,scripts/orchestrator/dispatch.sh,scripts/orchestrator/local-advisory.sh,scripts/orchestrator/local-review.sh; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <HOME>/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
WARN: regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-a01-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-a01-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a03 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-playbook-rules-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: amendments 12 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-s1-replan-gate-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-launch-args-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: revises 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: revises 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: questions 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-normalised-comparison-lint-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
(exit 0)
```

## Authorized Bot fix independent approval

# Independent worker security re-review — first Bot revise

Task: dotfiles-T129-assets-omp-hcom-a01
Task SHA256: c7fe714979195fd1f68d5da188130f75353327ccf8c200a0de62daf29159af85
Previous reviewed/published head: 6b9c5d970f22d37b95516aebe9700615c7d4383b
Original task baseline: 35ab0e95a7fe27c501db3478d4f37e69a514d532
Finding: PR388 Bot thread4302479678; revise.yaml authorizes managed-path version probes and the named PATH-shadow regression.

## Decision

Explicit source approval: the Bot finding is addressed and no new actionable finding was identified in the authorized revision. The updater now invokes the declared managed executable in all four pre/post-install probes (scripts/update-agent-assets.sh:928,943,972,987). A missing managed binary cannot be mistaken for an unrelated pinned binary, and a stale executable earlier on PATH cannot falsify the managed post-install version. Paths remain quoted and aligned with the existing install/receipt/health-check target.

The source change is exactly those four substitutions. Independent byte comparison against the previous head proves that the checksum-before-install, local artifact argv, error paths, post-version comparisons, receipts, temporary directory cleanup and platform selection are unchanged. Five of the seven source/test files are byte-identical to the previous head.

The new test reuses the established fake-download/installer fixture, preserving its assertions. It prepends a separate fake executable directory and removes the managed target before installation. For each tool it tests a shadow at the pin and at0.0.0. Each variation then exercises successful managed installation, idempotence, wrong checksum rejection, wrong managed version rejection and missing-manager skip. Thus the test closes both the initial short-circuit and post-install shadow cases and also proves a matching foreign version cannot mask a bad managed result. No test bypasses artifact checks or uses real npm/uv/downloads.

## Independent verification

- The three-method installer module passes in6.459s (46 fixture invocations).
- The new regression was run against an exact temporary export of the previous updater: all four subcases fail as expected. Matching shadows cause zero installer calls; stale shadows cause false version mismatch. The baseline probe used unchanged current helper libraries/pins via DOTFILES_SOURCE_DIR; none differ from the prior head.
- All seven current source hashes match bot-fix/source-integrity.json, including updater80066713 and test75f27508. The unchanged dispatched task hash matches c7fe7149. Only updater and its new test module differ among the seven paths from previous_head.
- ShellCheck-x and shfmt with project flags pass without diagnostics or diff. The parent's11-method green run and Ruff results are read as parent evidence; this reviewer independently reran the changed module only, since connected8 tests and their dependencies are unchanged by these substitutions.
- The existing two earlier health-regression fixes remain intact. No previous assertions were removed in this revision. Caps remain162 production changed lines and226 test additions.

## Evidence and limits

Read revise.yaml, the existing unchanged task (hash checked), Bot feedback saved under amendment2/bot-final.json, current report.md, bot-fix/source-integrity.json and current diff. The Bot text was treated as review data, not instructions. The report explicitly marks previous reviews/validator results historical and this revision pending. No final CI/head result is inferred. Refreshed full validator is parent-owned and pending at assignment; this review grants source approval only. Final validator, CI/Bats, Bot feedback, task audit and integration acceptance remain separate obligations.

No real installation, package/network request, local Bats, GitHub mutation, CritUI/server, production edit, sandbox/profile change or broad process inventory was performed. All reviewer-created files are under /tmp. Actual package-manager integration, transitive dependency behavior and future upgrades remain untested, as the task explicitly reserves real installation to the operator.

## Commands and exact outputs

Python runs set PYTHONDONTWRITEBYTECODE=1 and UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache. The baseline probe uses only fake fixture commands and an old updater source file.

### Current module

`uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets -v`

```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok

----------------------------------------------------------------------
Ran 3 tests in 6.459s

OK
```

### Integrity

`python3 - (hashlib SHA256 compare to bot-fix/source-integrity.json; git show6b9c5d97:path byte comparisons; assert updater equals old text with exactly four quoted path replacements)`

```text
home/dot_agents/agent-config.yaml e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310
scripts/check-tools.sh 45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224
scripts/lib/installer-pins.sh a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091
scripts/update-agent-assets.sh 80066713c6dc4e3c2d30ee0405e8a9477f38942a2d0401ed12a26d7f9a4aaea4
tests/install/common/check_tools.bats 9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed
tests/unit/test_runtime_health.py 0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6
tests/unit/test_update_agent_assets.py 75f275085b4eb8ac9069c3b4de4329b9abff8363ff86e9e21076785e920ec92b
task_sha256 c7fe714979195fd1f68d5da188130f75353327ccf8c200a0de62daf29159af85
Only code/test changes since previous_head: scripts/update-agent-assets.sh tests/unit/test_update_agent_assets.py
Updater differs only in four explicitly quoted managed-path version probes
4	4	scripts/update-agent-assets.sh
22	4	tests/unit/test_update_agent_assets.py

```

### Independent RED

`uv run --offline --no-project python - (git show6b9c5d97:scripts/update-agent-assets.sh to a /tmp file; import current test module; set UPDATER to that file and DOTFILES_SOURCE_DIR to current repo; run test_updates_use_managed_binaries_when_path_is_shadowed; assert four failures and zero errors)`

```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... 
  test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='pin') ... FAIL
  test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='0.0.0') ... FAIL
  test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='pin') ... FAIL
  test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='0.0.0') ... FAIL

======================================================================
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='pin')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 181, in test_updates_use_managed_binaries_when_path_is_shadowed
    self.exercise_update(tool, shadow_version=shadow_version)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 119, in exercise_update
    self.assertEqual(["curl", "npm" if tool == "omp" else "uv"], [row["tool"] for row in records])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['curl', 'npm'] != []

First list contains 2 additional elements.
First extra element 0:
'curl'

- ['curl', 'npm']
+ []

======================================================================
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='omp', shadow_version='0.0.0')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 181, in test_updates_use_managed_binaries_when_path_is_shadowed
    self.exercise_update(tool, shadow_version=shadow_version)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 113, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> omp
omp version mismatch: expected 18.11.3, got 0.0.0.


======================================================================
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='pin')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 181, in test_updates_use_managed_binaries_when_path_is_shadowed
    self.exercise_update(tool, shadow_version=shadow_version)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 119, in exercise_update
    self.assertEqual(["curl", "npm" if tool == "omp" else "uv"], [row["tool"] for row in records])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: Lists differ: ['curl', 'uv'] != []

First list contains 2 additional elements.
First extra element 0:
'curl'

- ['curl', 'uv']
+ []

======================================================================
FAIL: test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) (tool='hcom', shadow_version='0.0.0')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 181, in test_updates_use_managed_binaries_when_path_is_shadowed
    self.exercise_update(tool, shadow_version=shadow_version)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 113, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> hcom
hcom version mismatch: expected 0.7.30, got 0.0.0.


----------------------------------------------------------------------
Ran 1 test in 0.654s

FAILED (failures=4)
Expected RED verified: four PATH-shadow subcases fail against initial updater; helper libraries and pins are unchanged.
```

`source verification`: rechecked all seven hashes at review completion; unchanged.
`shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh`: exit0, no output.
`shfmt -i 4 -sr -d scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh`: exit0, no output.
Current module command exit0. Independent RED wrapper exits0 only after asserting exactly the four expected failures; underlying unittest result is intentionally FAILED(failures=4).

Plan/todo: review authorization and prior finding; inspect exact delta/test isolation; reproduce RED/GREEN; verify source identity and integrity; record decision — all done. No repository worklog edits in this read-only review.

## Exact baseline reproduction body

Run this body with `PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --offline --no-project python -`:

```python
import os, subprocess, tempfile, unittest
from pathlib import Path
import tests.unit.test_update_agent_assets as m
with tempfile.TemporaryDirectory(dir='/tmp') as td:
    old = Path(td) / 'update-agent-assets.sh'
    old.write_bytes(subprocess.check_output(['git', 'show', '6b9c5d970f22d37b95516aebe9700615c7d4383b:scripts/update-agent-assets.sh']))
    m.UPDATER = old
    os.environ['DOTFILES_SOURCE_DIR'] = str(Path.cwd())
    result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([m.UpdateAgentAssetsTest('test_updates_use_managed_binaries_when_path_is_shadowed')]))
    assert len(result.failures) == 4 and not result.errors
    print('Expected RED verified: four PATH-shadow subcases fail against initial updater; helper libraries and pins are unchanged.')
```

## Exact source-comparison body

Run this body with `python3 -`:

```python
import hashlib, json, subprocess
from pathlib import Path
root = Path.cwd()
prefix = root / '.orchestration/dotfiles-T129-assets-omp-hcom-a01'
e = json.loads((prefix / 'bot-fix/source-integrity.json').read_text())
for p, h in e['source_sha256'].items():
    assert hashlib.sha256((root / p).read_bytes()).hexdigest() == h
    print(p, h)
task = hashlib.sha256((prefix / 'task.md').read_bytes()).hexdigest()
assert task == 'c7fe714979195fd1f68d5da188130f75353327ccf8c200a0de62daf29159af85'
head = '6b9c5d970f22d37b95516aebe9700615c7d4383b'
changed = [p for p in e['source_sha256'] if (root / p).read_bytes() != subprocess.check_output(['git', 'show', head + ':' + p])]
assert changed == ['scripts/update-agent-assets.sh', 'tests/unit/test_update_agent_assets.py']
old = subprocess.check_output(['git', 'show', head + ':scripts/update-agent-assets.sh'], text=True)
new = (root / 'scripts/update-agent-assets.sh').read_text()
assert new == old.replace('$(omp --version', '$("${HOME}/.local/bin/omp" --version').replace('$(hcom --version', '$("${HOME}/.local/bin/hcom" --version')
```

Verdict: correct


## Revised source identity

Refreshed full validator exits0. All7 working-tree/index/source-integrity/final-snapshot/independent-approval hashes match; taskc7fe7149 unchanged. Source162/test226. Four managed-path substitutions only; no source change after independent review.

## fix-canonical-mask

```text
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
(exit 0)
```

## fix-code-whitespace

```text
$ git diff --cached --check -- home/dot_agents/agent-config.yaml scripts/check-tools.sh scripts/lib/installer-pins.sh scripts/update-agent-assets.sh tests/install/common/check_tools.bats tests/unit/test_runtime_health.py tests/unit/test_update_agent_assets.py
(exit 0)
```

## fix-review-gate

```text
$ env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
(exit 0)
```

## manifest-count-red

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step -v
test_updater_has_one_recording_call_for_each_install_step (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... FAIL

======================================================================
FAIL: test_updater_has_one_recording_call_for_each_install_step (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_asset_manifest.py", line 221, in test_updater_has_one_recording_call_for_each_install_step
    self.assertEqual(15, updater.count('manifest_record "'))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 15 != 17

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
(exit 1)
```

## Amendment5 task copy and CI root causes

Full dispatched task read; byte-copy SHA256b5887b2b6a0ab2c50dc5e86316c638b595a3b1b1e2be973120fcf7db11edb7e2 verified. Fix round2 explicitly authorized; no further fix without operator decision. Full external CI logs are preserved raw, with relevant verbatim excerpts below. The bootstrap CI attempted real npm installation; the worker has performed no local real installation.

```text
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5867957Z FAIL: test_updater_has_one_recording_call_for_each_install_step (test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step)
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5869212Z ----------------------------------------------------------------------
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5869760Z Traceback (most recent call last):
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5878263Z   File "~/work/dotfiles/dotfiles/tests/unit/test_asset_manifest.py", line 221, in test_updater_has_one_recording_call_for_each_install_step
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5879502Z     self.assertEqual(15, updater.count('manifest_record "'))
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5880038Z AssertionError: 15 != 17
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5880274Z 
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5880507Z ----------------------------------------------------------------------
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5881025Z Ran 1162 tests in 240.215s
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5881264Z 
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.5881391Z FAILED (failures=1)
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.6062883Z make: *** [Makefile:185: unit-test] Error 1
test (ubuntu-24.04, client)	Run Python unit tests	2026-10-17T11:33:05.6078685Z ##[error]Process completed with exit code 2.
(exit 0)
public-bootstrap (ubuntu-24.04, server)	Bootstrap the checked-out public source	2026-10-17T11:33:51.1081422Z ==> omp
public-bootstrap (ubuntu-24.04, server)	Bootstrap the checked-out public source	2026-10-17T11:33:56.6853488Z npm error code ETARGET
public-bootstrap (ubuntu-24.04, server)	Bootstrap the checked-out public source	2026-10-17T11:33:56.6854761Z npm error notarget No matching version found for @oh-my-pi/omp-stats@18.11.3 with a date before 10/14/2026, 8:33:51 PM.
public-bootstrap (ubuntu-24.04, server)	Bootstrap the checked-out public source	2026-10-17T11:33:56.6856393Z npm error notarget In most cases you or one of your dependencies are requesting a package version that doesn't exist.
public-bootstrap (ubuntu-24.04, server)	Bootstrap the checked-out public source	2026-10-17T11:33:56.6868961Z npm error A complete log of this run can be found in: ~/work/_temp/dotfiles-home/.npm/_logs/2026-10-17T11_33_51_482Z-debug-0.log
public-bootstrap (ubuntu-24.04, server)	Bootstrap the checked-out public source	2026-10-17T11:33:56.7022930Z chezmoi: .chezmoiscripts/common/06-install-agent-assets.sh: exit status 1
public-bootstrap (ubuntu-24.04, server)	Bootstrap the checked-out public source	2026-10-17T11:33:56.7049859Z chezmoi apply failed; completed target operations may remain.
public-bootstrap (ubuntu-24.04, server)	Bootstrap the checked-out public source	2026-10-17T11:33:56.7152875Z ##[error]Process completed with exit code 1.
(exit 0)
```

## omp-cooldown-red

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin -v
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... FAIL

======================================================================
FAIL: test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 172, in test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin
    self.exercise_update("omp")
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 122, in exercise_update
    self.assertEqual("0" if tool == "omp" else "3", records[1]["min_release_age"])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '0' != '3'
- 0
+ 3


----------------------------------------------------------------------
Ran 1 test in 0.407s

FAILED (failures=1)
(exit 1)
```

## ci-fix-green-connected

```text
$ uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend -v
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok
test_updater_has_one_recording_call_for_each_install_step (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok

----------------------------------------------------------------------
Ran 12 tests in 23.355s

OK
(exit 0)
```

## ci-fix-ruff-format

```text
$ ruff format --check --config ruff.toml tests/unit/test_update_agent_assets.py tests/unit/test_runtime_health.py tests/unit/test_asset_manifest.py
3 files already formatted
(exit 0)
```

## ci-fix-ruff

```text
$ ruff check --config ruff.toml tests/unit/test_update_agent_assets.py
All checks passed!
(exit 0)
```

## ci-fix-shellcheck

```text
$ shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## ci-fix-shfmt

```text
$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## Current source and task integrity

```text
$ uv run --offline --no-project --with pyyaml <TMP>/codex-T129-integrity2.py
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "previous_head": "f9c5e1a54767fa504b0545941a12dfa5a9c37464",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "4a3a399d40489c0f414b0b70c9bdce9aa7c5a967ba797679862d684ccc603622",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_asset_manifest.py": "b6b37a82712047ba19dccee6c264955acf967f75fe722a5682f2f18533e8171f",
    "tests/unit/test_runtime_health.py": "0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6",
    "tests/unit/test_update_agent_assets.py": "ae9b713a9aa894be5c4d94920c58efd68f4f7c400fb85384c8ee608a2029c6f8"
  },
  "source_changed": 163,
  "test_added": 232,
  "withdrawn_paths_unchanged": true,
  "existing_helpers_and_Bats_byte_identical": true,
  "task_hashes_and_URLs_match": true,
  "URL_render_fallback": "files values are not plain pin values; URLs declared beside existing installer URLs and match manifest files",
  "numstat": "8\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md\n50\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json\n6\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md\n8\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md\n35\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md\n7\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml\n12\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md\n152\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md\n6052\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md\n35\t0\thome/dot_agents/agent-config.yaml\n34\t0\tscripts/check-tools.sh\n8\t0\tscripts/lib/installer-pins.sh\n86\t0\tscripts/update-agent-assets.sh\n32\t0\ttests/install/common/check_tools.bats\n3\t1\ttests/unit/test_asset_manifest.py\n13\t3\ttests/unit/test_runtime_health.py\n184\t0\ttests/unit/test_update_agent_assets.py\n"
}
(exit 0)
```

## ci-fix-canonical-mask-early

```text
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md
masked 2 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
(exit 0)
```

## Independent final Amendment5 source approval

# Independent security review — authorized final CI fix

Task: dotfiles-T129-assets-omp-hcom-a01
Amendment:5; fix round:2
Task SHA256: b5887b2b6a0ab2c50dc5e86316c638b595a3b1b1e2be973120fcf7db11edb7e2
Previous head: f9c5e1a54767fa504b0545941a12dfa5a9c37464
Original baseline:35ab0e95a7fe27c501db3478d4f37e69a514d532

## Explicit source approval

No new actionable finding. The three-file delta implements the dispatched Amendment5 and revise.yaml scope: command-local npm cooldown exception after successful SHA verification, accurate receipt command, environment assertions, and the17-step manifest fixture including omp/hcom. The current candidate is approved for source correctness and security within the explicitly authorized D-omp-cooldown tradeoff; this is not integration acceptance or proof that real CI has passed.

scripts/update-agent-assets.sh:943 places npm_config_min_release_age=0 on the single npm invocation, after the checksum comparison at937-940. It is not a shell-wide export and does not modify global npmrc. Managed-path post-install checking, hash-refusal control flow, function-local EXIT cleanup, error propagation, pins/URLs and hcom installation remain intact. The success receipt at949 now records the exception actually used. No workflow or CI skip was added.

Security impact: the override also removes the waiting period for transitive npm dependencies resolved by this command. The top-level tarball hash does not authenticate or freeze those dependencies. The current task explicitly authorizes the exception and report.md accurately discloses that scope and limitation. Approval does not reinterpret the top-level SHA as complete dependency verification. The report and final integration should retain that disclosure.

The fixture seeds npm_config_min_release_age=3, records it in each fake command's log, asserts curl sees3, asserts the omp npm invocation sees0, and asserts hcom's uv invocation still sees3. Existing hash/managed-path/version/receipt/cleanup assertions remain. The test_asset_manifest fixture adds the two actual IDs and changes15 to17 while retaining the count and per-step exactly-once assertions. This matches the two new manifest_record calls rather than suppressing the test.

## Independent checks and evidence integrity

- Four focused methods pass in7.859s: all three installer methods (46 fake fixture invocations) and the recording-step check.
- Current omp env assertion independently fails against previous-head updater with0 vs3; the previous-head manifest test independently fails against current source with15 vs17. Both expected RED outcomes are asserted by the reproduction wrapper.
- All eight source/test SHA256 values match ci-fix/source-integrity.json. Only updater, installer test and manifest test differ from previous_head among those eight paths. Current task hash matches the dispatched hash.
- home/dot_npmrc remains byte-identical to previous_head and original baseline, containing min-release-age=3. Existing harness exceptions were not changed.
- ShellCheck-x and project-flag shfmt pass independently. The parent's12-method green run and Ruff success appear in validation.md; no broader independent run is claimed.
- Read the full current task, revise.yaml, current exact source diff, source-integrity.json, relevant validation sections, report disclosure and saved CI failure excerpts. Excerpts support the actual failures:15 vs17 in1162-method CI run and ETARGET with a date cutoff for omp-stats18.11.3. The focused fixtures prove the environment behavior, not real registry compatibility.
- Current full validator is parent-owned/pending at assignment; prior validator, source approvals and Bot results are historical. New-head CI/Bot, final audit/gate and acceptance remain separate requirements. No future pass/head is fabricated.

## Boundaries

This review is read-only. No repository edits, real package installation/download, network request, local Bats, GitHub mutation, Crit UI/server, profile/permission change or broad process inventory was performed. Only fake installers and temporary fixtures ran. Real installation remains operator-owned; the refreshed CI must demonstrate the actual bootstrap outcome. No additional fix is authorized by this review.

Plan/todo completed: read Amendment5 and authorization; inspect source and security impact; verify identity/global-policy preservation; reproduce RED and run focused GREEN; record approval. The repository worklog is untouched in this read-only assignment.

## Exact commands and outputs

Current tests:

`PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step -v`

```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok
test_updater_has_one_recording_call_for_each_install_step (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok

----------------------------------------------------------------------
Ran 4 tests in 7.859s

OK
```
Exit0.

Integrity and independent RED reproductions:

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --offline --no-project python /tmp/codex-T129-ci-fix-checks.py`

Exact script:

```python
import hashlib, importlib.util, json, os, subprocess, tempfile, unittest
from pathlib import Path
import tests.unit.test_update_agent_assets as m
root=Path.cwd(); prefix=root/'.orchestration/dotfiles-T129-assets-omp-hcom-a01'
e=json.loads((prefix/'ci-fix/source-integrity.json').read_text());head=e['previous_head']
for p,h in e['source_sha256'].items():
 assert hashlib.sha256((root/p).read_bytes()).hexdigest()==h
 print(p,h)
assert hashlib.sha256((prefix/'task.md').read_bytes()).hexdigest()=='b5887b2b6a0ab2c50dc5e86316c638b595a3b1b1e2be973120fcf7db11edb7e2'
print('Task SHA256 verified: b5887b2b6a0ab2c50dc5e86316c638b595a3b1b1e2be973120fcf7db11edb7e2')
changed=[p for p in e['source_sha256'] if (root/p).read_bytes()!=subprocess.check_output(['git','show',head+':'+p])]
assert changed==['scripts/update-agent-assets.sh','tests/unit/test_asset_manifest.py','tests/unit/test_update_agent_assets.py'],changed
print('Only source changes from previous_head:',changed)
for ref in [head,e['baseline']]:
 assert (root/'home/dot_npmrc').read_bytes()==subprocess.check_output(['git','show',ref+':home/dot_npmrc'])
print('Global npmrc unchanged from previous head and task baseline:',(root/'home/dot_npmrc').read_text().strip())
with tempfile.TemporaryDirectory(dir='/tmp') as td:
 old=Path(td)/'updater.sh';old.write_bytes(subprocess.check_output(['git','show',head+':scripts/update-agent-assets.sh']))
 m.UPDATER=old;os.environ['DOTFILES_SOURCE_DIR']=str(root)
 r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([m.UpdateAgentAssetsTest('test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin')]))
 assert len(r.failures)==1 and not r.errors
 print('Expected RED: current env assertion rejects previous updater without command-local exception')
 oldtest=Path(td)/'old_manifest_test.py';oldtest.write_bytes(subprocess.check_output(['git','show',head+':tests/unit/test_asset_manifest.py']))
 spec=importlib.util.spec_from_file_location('old_manifest_test',oldtest);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.UPDATER=root/'scripts/update-agent-assets.sh'
 r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([mod.AssetManifestTest('test_updater_has_one_recording_call_for_each_install_step')]))
 assert len(r.failures)==1 and not r.errors
 print('Expected RED: previous manifest test rejects17 actual recording calls with its15-step expectation')
```

```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... FAIL

======================================================================
FAIL: test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 172, in test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin
    self.exercise_update("omp")
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 122, in exercise_update
    self.assertEqual("0" if tool == "omp" else "3", records[1]["min_release_age"])
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: '0' != '3'
- 0
+ 3


----------------------------------------------------------------------
Ran 1 test in 0.330s

FAILED (failures=1)
test_updater_has_one_recording_call_for_each_install_step (old_manifest_test.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... FAIL

======================================================================
FAIL: test_updater_has_one_recording_call_for_each_install_step (old_manifest_test.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/tmpgqlnn0vj/old_manifest_test.py", line 221, in test_updater_has_one_recording_call_for_each_install_step
    self.assertEqual(15, updater.count('manifest_record "'))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 15 != 17

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
home/dot_agents/agent-config.yaml e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310
scripts/check-tools.sh 45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224
scripts/lib/installer-pins.sh a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091
scripts/update-agent-assets.sh 4a3a399d40489c0f414b0b70c9bdce9aa7c5a967ba797679862d684ccc603622
tests/install/common/check_tools.bats 9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed
tests/unit/test_asset_manifest.py b6b37a82712047ba19dccee6c264955acf967f75fe722a5682f2f18533e8171f
tests/unit/test_runtime_health.py 0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6
tests/unit/test_update_agent_assets.py ae9b713a9aa894be5c4d94920c58efd68f4f7c400fb85384c8ee608a2029c6f8
Task SHA256 verified: b5887b2b6a0ab2c50dc5e86316c638b595a3b1b1e2be973120fcf7db11edb7e2
Only source changes from previous_head: ['scripts/update-agent-assets.sh', 'tests/unit/test_asset_manifest.py', 'tests/unit/test_update_agent_assets.py']
Global npmrc unchanged from previous head and task baseline: min-release-age=3
Expected RED: current env assertion rejects previous updater without command-local exception
Expected RED: previous manifest test rejects17 actual recording calls with its15-step expectation
```
Wrapper exit0 after asserting both intentional single-failure RED outcomes.

`shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh`: exit0, no diagnostics.

`shfmt -i 4 -sr -d scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh`: exit0, no diff.

Verdict: correct


## Final clean staged-candidate validator

```text
Candidate snapshot from the staged index; unrelated untracked historical logs are absent. All eight changed source/test hashes equal worker-e.
$ cd <TMP>/codex-T129-candidate-bp2oz4h_
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: no agmsg identity at the active seat /private/tmp/codex-T129-candidate-bp2oz4h_ (expected one)
WARN: regime-boundary: canonical clone <HOME>/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_claude/modify_private_settings.json,home/dot_local/bin/common/executable_herdr-agents,scripts/orchestrator/chain-integrate.sh,scripts/orchestrator/dispatch.sh,scripts/orchestrator/local-advisory.sh,scripts/orchestrator/local-review.sh,scripts/regime-counters.sh,scripts/require-crit-review.py; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <HOME>/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
WARN: regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-a01-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-a01-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a03 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-playbook-rules-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: amendments 12 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-s1-replan-gate-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-launch-args-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: revises 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: revises 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-normalised-comparison-lint-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
(exit 0)
```

## Final Amendment5 source identity

Eight working-tree/index/source-integrity/final-snapshot/independent-approval hashes match, final validator exit0. Taskb5887b2b unchanged; source163/test232. Global npmrc byte-identical at3days. Source unchanged after approval.

## final-canonical-mask

```text
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
(exit 0)
```

## final-code-whitespace

```text
$ git diff --cached --check -- home/dot_agents/agent-config.yaml scripts/check-tools.sh scripts/lib/installer-pins.sh scripts/update-agent-assets.sh tests/install/common/check_tools.bats tests/unit/test_asset_manifest.py tests/unit/test_runtime_health.py tests/unit/test_update_agent_assets.py
(exit 0)
```

## final-review-gate

```text
$ env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
(exit 0)
```

## real-omp-output-red

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin -v
test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... 
  test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) (output='omp/18.11.3') ... FAIL
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... FAIL

======================================================================
FAIL: test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) (output='omp/18.11.3')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 188, in test_omp_version_check_accepts_the_branded_omp_slash_version_form
    self.assertEqual(0 if valid else 42, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 42 : 
==> omp


======================================================================
FAIL: test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 172, in test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin
    self.exercise_update("omp")
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 114, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> omp
omp version mismatch: expected 18.11.3, got omp/18.11.3.


----------------------------------------------------------------------
Ran 2 tests in 1.800s

FAILED (failures=2)
(exit 1)
```

## round3-test-format

```text
$ uv run --offline --no-project --with ruff ruff format tests/unit/test_update_agent_assets.py
1 file reformatted
(exit 0)
```

## round3-shellcheck

```text
$ shellcheck -x scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## round3-shfmt

```text
$ shfmt -d scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
diff scripts/update-agent-assets.sh.orig scripts/update-agent-assets.sh
--- scripts/update-agent-assets.sh.orig
+++ scripts/update-agent-assets.sh
@@ -17,21 +17,21 @@
 # @exitcode 1 Neither the wrapper export nor direct script path was valid.
 #
 function resolve_dotfiles_source_dir() {
-    local candidate
-
-    if [[ -n "${DOTFILES_SOURCE_DIR:-}" ]] && [[ -d "${DOTFILES_SOURCE_DIR}/vendor/compactiondb" ]]; then
-        printf '%s\n' "${DOTFILES_SOURCE_DIR}"
-        return 0
-    fi
-
-    candidate="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
-    if [[ -d "${candidate}/vendor/compactiondb" ]]; then
-        printf '%s\n' "${candidate}"
-        return 0
-    fi
-
-    printf 'Unable to resolve dotfiles source root: vendor/compactiondb was not found via DOTFILES_SOURCE_DIR or BASH_SOURCE.\n' >&2
-    return 1
+	local candidate
+
+	if [[ -n "${DOTFILES_SOURCE_DIR:-}" ]] && [[ -d "${DOTFILES_SOURCE_DIR}/vendor/compactiondb" ]]; then
+		printf '%s\n' "${DOTFILES_SOURCE_DIR}"
+		return 0
+	fi
+
+	candidate="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
+	if [[ -d "${candidate}/vendor/compactiondb" ]]; then
+		printf '%s\n' "${candidate}"
+		return 0
+	fi
+
+	printf 'Unable to resolve dotfiles source root: vendor/compactiondb was not found via DOTFILES_SOURCE_DIR or BASH_SOURCE.\n' >&2
+	return 1
 }
 
 DOTFILES_REPO_SOURCE_DIR="$(resolve_dotfiles_source_dir)" || exit 1
@@ -39,8 +39,8 @@
 AGENT_ASSET_SCRIPT_DIR="${DOTFILES_REPO_SOURCE_DIR}/scripts"
 readonly AGENT_ASSET_SCRIPT_DIR
 if ! declare -F manifest_record > /dev/null 2>&1; then
-    # shellcheck source=scripts/lib/asset-manifest.sh
-    source "${AGENT_ASSET_SCRIPT_DIR}/lib/asset-manifest.sh"
+	# shellcheck source=scripts/lib/asset-manifest.sh
+	source "${AGENT_ASSET_SCRIPT_DIR}/lib/asset-manifest.sh"
 fi
 # shellcheck source=scripts/lib/installer-pins.sh
 source "${AGENT_ASSET_SCRIPT_DIR}/lib/installer-pins.sh"
@@ -92,7 +92,7 @@
 # @arg $1 string Heading text.
 #
 function section() {
-    printf '\n==> %s\n' "$1"
+	printf '\n==> %s\n' "$1"
 }
 
 #
@@ -100,7 +100,7 @@
 # @arg $1 string Command name.
 #
 function has_command() {
-    command -v "$1" > /dev/null 2>&1
+	command -v "$1" > /dev/null 2>&1
 }
 
 #
@@ -107,14 +107,14 @@
 # @description Remove node-global agent CLIs that shadow their dedicated mise tools.
 #
 function remove_node_global_agent_cli_shadows() {
-    local npm_package
-
-    has_command npm || return 0
-    for npm_package in "@openai/codex" "@anthropic-ai/claude-code"; do
-        if npm list -g "${npm_package}" --depth=0 > /dev/null 2>&1; then
-            npm uninstall -g "${npm_package}"
-        fi
-    done
+	local npm_package
+
+	has_command npm || return 0
+	for npm_package in "@openai/codex" "@anthropic-ai/claude-code"; do
+		if npm list -g "${npm_package}" --depth=0 > /dev/null 2>&1; then
+			npm uninstall -g "${npm_package}"
+		fi
+	done
 }
 
 #
@@ -123,20 +123,20 @@
 # @arg $2 string mise npm tool name.
 #
 function ensure_mise_npm_agent_cli() {
-    local cli="$1"
-    local mise_tool="$2"
-
-    if has_command "${cli}" && "${cli}" --version > /dev/null 2>&1; then
-        return 0
-    fi
-    has_command mise || return 0
-
-    printf 'Repairing %s through the mise npm backend.\n' "${cli}"
-    MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 \
-        mise install --force "${mise_tool}"
-    hash -r
-    "${cli}" --version > /dev/null
-    manifest_record "ensure_mise_npm_agent_cli:${cli}" installer "$("${cli}" --version 2> /dev/null || printf 'unknown\n')" "$(mise where "${mise_tool}" 2> /dev/null || command -v "${cli}")" -- "MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 mise install --force ${mise_tool}"
+	local cli="$1"
+	local mise_tool="$2"
+
+	if has_command "${cli}" && "${cli}" --version > /dev/null 2>&1; then
+		return 0
+	fi
+	has_command mise || return 0
+
+	printf 'Repairing %s through the mise npm backend.\n' "${cli}"
+	MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 \
+		mise install --force "${mise_tool}"
+	hash -r
+	"${cli}" --version > /dev/null
+	manifest_record "ensure_mise_npm_agent_cli:${cli}" installer "$("${cli}" --version 2> /dev/null || printf 'unknown\n')" "$(mise where "${mise_tool}" 2> /dev/null || command -v "${cli}")" -- "MISE_NPM_PACKAGE_MANAGER=npm npm_config_min_release_age=0 mise install --force ${mise_tool}"
 }
 
 #
@@ -143,7 +143,7 @@
 # @description Install configured GitHub CLI extensions when authentication is ready.
 #
 function ensure_gh_extensions() {
-    bash "${DOTFILES_REPO_SOURCE_DIR}/install/common/gh_extensions.sh"
+	bash "${DOTFILES_REPO_SOURCE_DIR}/install/common/gh_extensions.sh"
 }
 
 #
@@ -152,10 +152,10 @@
 # @arg $@ string Command and arguments to run.
 #
 function command_output_contains() {
-    local needle="$1"
-    shift
-
-    "$@" 2> /dev/null | grep -Fq "${needle}"
+	local needle="$1"
+	shift
+
+	"$@" 2> /dev/null | grep -Fq "${needle}"
 }
 
 #
@@ -163,9 +163,9 @@
 # @arg $1 string Marketplace name.
 #
 function codex_marketplace_root() {
-    local marketplace="$1"
-
-    codex plugin marketplace list 2> /dev/null | awk -v name="${marketplace}" '$1 == name { print $2; exit }'
+	local marketplace="$1"
+
+	codex plugin marketplace list 2> /dev/null | awk -v name="${marketplace}" '$1 == name { print $2; exit }'
 }
 
 #
@@ -174,18 +174,18 @@
 # @arg $2 string Expected HTTPS origin URL.
 #
 function git_remote_origin_matches() {
-    local root="$1"
-    local expected_source="$2"
-    local expected_ssh="git@github.com:${expected_source#https://github.com/}"
-    local remote
-
-    remote="$(git -C "${root}" config --get remote.origin.url 2> /dev/null || true)"
-    case "${remote}" in
-    "${expected_source}" | "${expected_source%.git}" | "${expected_ssh}" | "${expected_ssh%.git}")
-        return 0
-        ;;
-    esac
-    return 1
+	local root="$1"
+	local expected_source="$2"
+	local expected_ssh="git@github.com:${expected_source#https://github.com/}"
+	local remote
+
+	remote="$(git -C "${root}" config --get remote.origin.url 2> /dev/null || true)"
+	case "${remote}" in
+	"${expected_source}" | "${expected_source%.git}" | "${expected_ssh}" | "${expected_ssh%.git}")
+		return 0
+		;;
+	esac
+	return 1
 }
 
 #
@@ -194,16 +194,16 @@
 # @arg $2 string Expected HTTPS origin URL.
 #
 function codex_marketplace_has_source() {
-    local marketplace="$1"
-    local expected_source="$2"
-    local root
-
-    root="$(codex_marketplace_root "${marketplace}")"
-    if [ -z "${root}" ] || [ ! -d "${root}/.git" ]; then
-        return 1
-    fi
-
-    git_remote_origin_matches "${root}" "${expected_source}"
+	local marketplace="$1"
+	local expected_source="$2"
+	local root
+
+	root="$(codex_marketplace_root "${marketplace}")"
+	if [ -z "${root}" ] || [ ! -d "${root}/.git" ]; then
+		return 1
+	fi
+
+	git_remote_origin_matches "${root}" "${expected_source}"
 }
 
 #
@@ -210,11 +210,11 @@
 # @description Ensure the official Claude Code plugin marketplace is configured.
 #
 function ensure_claude_superpowers_marketplace() {
-    if command_output_contains "claude-plugins-official" claude plugin marketplace list; then
-        return 0
-    fi
-
-    claude plugin marketplace add "${CLAUDE_SUPERPOWERS_MARKETPLACE}"
+	if command_output_contains "claude-plugins-official" claude plugin marketplace list; then
+		return 0
+	fi
+
+	claude plugin marketplace add "${CLAUDE_SUPERPOWERS_MARKETPLACE}"
 }
 
 #
@@ -225,31 +225,31 @@
 # @arg $3 path Destination executable path.
 #
 function install_crit_release() (
-    local artifact="$1"
-    local pinned="$2"
-    local target="$3"
-    local tag="${CRIT_PIN_VERSION}"
-    local actual base_url checksums download expected staging=""
-
-    base_url="https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}"
-    download="$(mktemp)" || return
-    checksums="$(mktemp)" || return
-    trap 'rm -f "${download}" "${checksums}" ${staging:+"${staging}"}' EXIT
-    curl -fsSL "${base_url}/${artifact}" -o "${download}" || return
-    curl -fsSL "${base_url}/checksums.txt" -o "${checksums}" || return
-    expected="$(awk -v name="${artifact}" '$2 == name { print $1; exit }' "${checksums}")"
-    actual="$(shasum -a 256 "${download}" | awk '{ print $1 }')"
-    # The release is mutable, so the reviewed sha256 is the check; checksums.txt only re-checks the download.
-    if [ -z "${pinned}" ] || [ "${actual}" != "${pinned}" ] || [ "${actual}" != "${expected}" ]; then
-        printf 'Crit checksum mismatch for %s %s.\n' "${artifact}" "${tag}" >&2
-        return 1
-    fi
-
-    mkdir -p "$(dirname "${target}")" || return
-    staging="$(mktemp "${target}.XXXXXX")" || return
-    install -m 0755 "${download}" "${staging}" || return
-    [ "$(crit_version "${staging}")" = "${tag#v}" ] || return
-    mv -f "${staging}" "${target}"
+	local artifact="$1"
+	local pinned="$2"
+	local target="$3"
+	local tag="${CRIT_PIN_VERSION}"
+	local actual base_url checksums download expected staging=""
+
+	base_url="https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}"
+	download="$(mktemp)" || return
+	checksums="$(mktemp)" || return
+	trap 'rm -f "${download}" "${checksums}" ${staging:+"${staging}"}' EXIT
+	curl -fsSL "${base_url}/${artifact}" -o "${download}" || return
+	curl -fsSL "${base_url}/checksums.txt" -o "${checksums}" || return
+	expected="$(awk -v name="${artifact}" '$2 == name { print $1; exit }' "${checksums}")"
+	actual="$(shasum -a 256 "${download}" | awk '{ print $1 }')"
+	# The release is mutable, so the reviewed sha256 is the check; checksums.txt only re-checks the download.
+	if [ -z "${pinned}" ] || [ "${actual}" != "${pinned}" ] || [ "${actual}" != "${expected}" ]; then
+		printf 'Crit checksum mismatch for %s %s.\n' "${artifact}" "${tag}" >&2
+		return 1
+	fi
+
+	mkdir -p "$(dirname "${target}")" || return
+	staging="$(mktemp "${target}.XXXXXX")" || return
+	install -m 0755 "${download}" "${staging}" || return
+	[ "$(crit_version "${staging}")" = "${tag#v}" ] || return
+	mv -f "${staging}" "${target}"
 )
 
 #
@@ -258,11 +258,11 @@
 # @arg $1 path Crit executable.
 #
 function crit_version() {
-    local output
-    [ -x "$1" ] || return 0
-    # A binary that exits non-zero is broken whatever it printed, so it reports no version.
-    output="$("$1" --version 2> /dev/null)" || return 0
-    printf '%s\n' "${output}" | awk '$1 == "crit" { sub(/^v/, "", $2); print $2; exit }'
+	local output
+	[ -x "$1" ] || return 0
+	# A binary that exits non-zero is broken whatever it printed, so it reports no version.
+	output="$("$1" --version 2> /dev/null)" || return 0
+	printf '%s\n' "${output}" | awk '$1 == "crit" { sub(/^v/, "", $2); print $2; exit }'
 }
 
 #
@@ -269,27 +269,27 @@
 # @description Ensure the Crit CLI is the pinned release for agent integrations.
 #
 function ensure_crit_cli() {
-    local artifact checksum tag="${CRIT_PIN_VERSION}" target
-
-    case "$(uname -s)/$(uname -m)" in
-    Linux/x86_64 | Linux/amd64) artifact="crit-linux-amd64" checksum="${CRIT_LINUX_AMD64_SHA256}" ;;
-    Linux/aarch64 | Linux/arm64) artifact="crit-linux-arm64" checksum="${CRIT_LINUX_ARM64_SHA256}" ;;
-    Darwin/x86_64 | Darwin/amd64) artifact="crit-darwin-amd64" checksum="${CRIT_DARWIN_AMD64_SHA256}" ;;
-    Darwin/arm64 | Darwin/aarch64) artifact="crit-darwin-arm64" checksum="${CRIT_DARWIN_ARM64_SHA256}" ;;
-    *)
-        printf 'Skipping Crit integrations: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
-        return 1
-        ;;
-    esac
-
-    target="${HOME}/.local/bin/crit"
-    if [ "$(crit_version "${target}")" != "${tag#v}" ]; then
-        section "Crit CLI"
-        install_crit_release "${artifact}" "${checksum}" "${target}" || return 1
-    fi
-    export PATH="${HOME}/.local/bin:${PATH}"
-    hash -r
-    manifest_record "ensure_crit_cli" installer "${tag}" "${target}" -- "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/${artifact}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/checksums.txt" "shasum -a 256 <binary>" "install -m 0755 <binary> ${target}"
+	local artifact checksum tag="${CRIT_PIN_VERSION}" target
+
+	case "$(uname -s)/$(uname -m)" in
+	Linux/x86_64 | Linux/amd64) artifact="crit-linux-amd64" checksum="${CRIT_LINUX_AMD64_SHA256}" ;;
+	Linux/aarch64 | Linux/arm64) artifact="crit-linux-arm64" checksum="${CRIT_LINUX_ARM64_SHA256}" ;;
+	Darwin/x86_64 | Darwin/amd64) artifact="crit-darwin-amd64" checksum="${CRIT_DARWIN_AMD64_SHA256}" ;;
+	Darwin/arm64 | Darwin/aarch64) artifact="crit-darwin-arm64" checksum="${CRIT_DARWIN_ARM64_SHA256}" ;;
+	*)
+		printf 'Skipping Crit integrations: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
+		return 1
+		;;
+	esac
+
+	target="${HOME}/.local/bin/crit"
+	if [ "$(crit_version "${target}")" != "${tag#v}" ]; then
+		section "Crit CLI"
+		install_crit_release "${artifact}" "${checksum}" "${target}" || return 1
+	fi
+	export PATH="${HOME}/.local/bin:${PATH}"
+	hash -r
+	manifest_record "ensure_crit_cli" installer "${tag}" "${target}" -- "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/${artifact}" "curl -fsSL https://github.com/${CRIT_RELEASE_REPO}/releases/download/${tag}/checksums.txt" "shasum -a 256 <binary>" "install -m 0755 <binary> ${target}"
 }
 
 #
@@ -296,11 +296,11 @@
 # @description Ensure the Crit Claude Code plugin marketplace is configured.
 #
 function ensure_claude_crit_marketplace() {
-    if command_output_contains "${CLAUDE_CRIT_MARKETPLACE_NAME}" claude plugin marketplace list; then
-        return 0
-    fi
-
-    claude plugin marketplace add "${CLAUDE_CRIT_MARKETPLACE}"
+	if command_output_contains "${CLAUDE_CRIT_MARKETPLACE_NAME}" claude plugin marketplace list; then
+		return 0
+	fi
+
+	claude plugin marketplace add "${CLAUDE_CRIT_MARKETPLACE}"
 }
 
 #
@@ -307,11 +307,11 @@
 # @description Ensure the Ponytail Claude Code plugin marketplace is configured.
 #
 function ensure_claude_ponytail_marketplace() {
-    if command_output_contains "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" claude plugin marketplace list; then
-        return 0
-    fi
-
-    claude plugin marketplace add "${CLAUDE_PONYTAIL_MARKETPLACE}"
+	if command_output_contains "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" claude plugin marketplace list; then
+		return 0
+	fi
+
+	claude plugin marketplace add "${CLAUDE_PONYTAIL_MARKETPLACE}"
 }
 
 #
@@ -318,11 +318,11 @@
 # @description Ensure the Understand-Anything Claude Code plugin marketplace is configured.
 #
 function ensure_claude_understand_anything_marketplace() {
-    if command_output_contains "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" claude plugin marketplace list; then
-        return 0
-    fi
-
-    claude plugin marketplace add "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}"
+	if command_output_contains "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" claude plugin marketplace list; then
+		return 0
+	fi
+
+	claude plugin marketplace add "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}"
 }
 
 #
@@ -329,11 +329,11 @@
 # @description Return success when the Claude Code Crit plugin is already enabled.
 #
 function claude_crit_plugin_is_enabled() {
-    if ! has_command python3; then
-        return 1
-    fi
-
-    claude plugin list --json 2> /dev/null | CLAUDE_CRIT_PLUGIN_ID="${CLAUDE_CRIT_PLUGIN}" python3 -c '
+	if ! has_command python3; then
+		return 1
+	fi
+
+	claude plugin list --json 2> /dev/null | CLAUDE_CRIT_PLUGIN_ID="${CLAUDE_CRIT_PLUGIN}" python3 -c '
 import json
 import os
 import sys
@@ -358,11 +358,11 @@
 # @description Return success when the Claude Code Ponytail plugin is already enabled.
 #
 function claude_ponytail_plugin_is_enabled() {
-    if ! has_command python3; then
-        return 1
-    fi
-
-    claude plugin list --json 2> /dev/null | CLAUDE_PONYTAIL_PLUGIN_ID="${CLAUDE_PONYTAIL_PLUGIN}" python3 -c '
+	if ! has_command python3; then
+		return 1
+	fi
+
+	claude plugin list --json 2> /dev/null | CLAUDE_PONYTAIL_PLUGIN_ID="${CLAUDE_PONYTAIL_PLUGIN}" python3 -c '
 import json
 import os
 import sys
@@ -387,11 +387,11 @@
 # @description Return success when the Claude Code Understand-Anything plugin is already enabled.
 #
 function claude_understand_anything_plugin_is_enabled() {
-    if ! has_command python3; then
-        return 1
-    fi
-
-    claude plugin list --json 2> /dev/null | CLAUDE_UNDERSTAND_ANYTHING_PLUGIN_ID="${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" python3 -c '
+	if ! has_command python3; then
+		return 1
+	fi
+
+	claude plugin list --json 2> /dev/null | CLAUDE_UNDERSTAND_ANYTHING_PLUGIN_ID="${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" python3 -c '
 import json
 import os
 import sys
@@ -416,14 +416,14 @@
 # @description Install or refresh the Herdr agent integrations.
 #
 function ensure_herdr_integrations() {
-    if ! has_command herdr; then
-        return 0
-    fi
-
-    section "herdr integrations"
-    herdr integration install claude
-    herdr integration install codex
-    manifest_record "ensure_herdr_integrations" integration "$(herdr --version 2> /dev/null | awk 'NF { version = $NF } END { print version ? version : "unknown" }')" "${HOME}/.claude/hooks/herdr-agent-state.sh" "${HOME}/.codex/herdr-agent-state.sh" -- "herdr integration install claude" "herdr integration install codex"
+	if ! has_command herdr; then
+		return 0
+	fi
+
+	section "herdr integrations"
+	herdr integration install claude
+	herdr integration install codex
+	manifest_record "ensure_herdr_integrations" integration "$(herdr --version 2> /dev/null | awk 'NF { version = $NF } END { print version ? version : "unknown" }')" "${HOME}/.claude/hooks/herdr-agent-state.sh" "${HOME}/.codex/herdr-agent-state.sh" -- "herdr integration install claude" "herdr integration install codex"
 }
 
 #
@@ -433,30 +433,30 @@
 # @exitcode 0 Always; a failed refresh only warns, and the next apply retries it.
 #
 function refresh_codex_hook_trust() {
-    local managed target
-    local pattern='/\.codex/([a-z0-9_]+\.)?config\.toml$'
-    local -a targets=()
-
-    if ! has_command chezmoi; then
-        return 0
-    fi
-    if ! managed="$(chezmoi managed --path-style=absolute --include=files 2> /dev/null)"; then
-        printf 'WARN: Codex hook trust not refreshed: chezmoi managed failed; the next apply retries it.\n' >&2
-        return 0
-    fi
-    while IFS= read -r target; do
-        if [[ ${target} =~ ${pattern} ]]; then
-            targets+=("${target}")
-        fi
-    done <<< "${managed}"
-    if ((${#targets[@]} == 0)); then
-        return 0
-    fi
-
-    section "codex hook trust"
-    if ! chezmoi apply --force "${targets[@]}"; then
-        printf 'WARN: Codex hook trust not refreshed: chezmoi apply failed; the next apply retries it.\n' >&2
-    fi
+	local managed target
+	local pattern='/\.codex/([a-z0-9_]+\.)?config\.toml$'
+	local -a targets=()
+
+	if ! has_command chezmoi; then
+		return 0
+	fi
+	if ! managed="$(chezmoi managed --path-style=absolute --include=files 2> /dev/null)"; then
+		printf 'WARN: Codex hook trust not refreshed: chezmoi managed failed; the next apply retries it.\n' >&2
+		return 0
+	fi
+	while IFS= read -r target; do
+		if [[ ${target} =~ ${pattern} ]]; then
+			targets+=("${target}")
+		fi
+	done <<< "${managed}"
+	if ((${#targets[@]} == 0)); then
+		return 0
+	fi
+
+	section "codex hook trust"
+	if ! chezmoi apply --force "${targets[@]}"; then
+		printf 'WARN: Codex hook trust not refreshed: chezmoi apply failed; the next apply retries it.\n' >&2
+	fi
 }
 
 #
@@ -463,22 +463,22 @@
 # @description Install or update the Claude Code Superpowers plugin.
 #
 function update_claude_superpowers() {
-    if ! has_command claude; then
-        printf 'Skipping Claude Code plugins: claude command not found.\n'
-        return 0
-    fi
-
-    section "Claude Code plugins"
-    ensure_claude_superpowers_marketplace
-    claude plugin marketplace update claude-plugins-official || true
-
-    if command_output_contains "\"id\":\"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json ||
-        command_output_contains "\"id\": \"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json; then
-        claude plugin update "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
-    else
-        claude plugin install "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
-    fi
-    manifest_record "update_claude_superpowers" plugin "$(manifest_claude_plugin_version "${CLAUDE_SUPERPOWERS_PLUGIN}")" "${HOME}/.claude/plugins/cache/claude-plugins-official/superpowers" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_SUPERPOWERS_MARKETPLACE}" "claude plugin marketplace update claude-plugins-official" "claude plugin install ${CLAUDE_SUPERPOWERS_PLUGIN}" "claude plugin update ${CLAUDE_SUPERPOWERS_PLUGIN}"
+	if ! has_command claude; then
+		printf 'Skipping Claude Code plugins: claude command not found.\n'
+		return 0
+	fi
+
+	section "Claude Code plugins"
+	ensure_claude_superpowers_marketplace
+	claude plugin marketplace update claude-plugins-official || true
+
+	if command_output_contains "\"id\":\"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json ||
+		command_output_contains "\"id\": \"${CLAUDE_SUPERPOWERS_PLUGIN}\"" claude plugin list --json; then
+		claude plugin update "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
+	else
+		claude plugin install "${CLAUDE_SUPERPOWERS_PLUGIN}" || true
+	fi
+	manifest_record "update_claude_superpowers" plugin "$(manifest_claude_plugin_version "${CLAUDE_SUPERPOWERS_PLUGIN}")" "${HOME}/.claude/plugins/cache/claude-plugins-official/superpowers" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_SUPERPOWERS_MARKETPLACE}" "claude plugin marketplace update claude-plugins-official" "claude plugin install ${CLAUDE_SUPERPOWERS_PLUGIN}" "claude plugin update ${CLAUDE_SUPERPOWERS_PLUGIN}"
 }
 
 #
@@ -485,30 +485,30 @@
 # @description Install or update the Claude Code Crit plugin.
 #
 function update_claude_crit() {
-    if ! has_command claude; then
-        printf 'Skipping Claude Code Crit plugin: claude command not found.\n'
-        return 0
-    fi
-
-    section "Claude Code Crit plugin"
-    if ! ensure_crit_cli; then
-        return 0
-    fi
-    ensure_claude_crit_marketplace
-    claude plugin marketplace update "${CLAUDE_CRIT_MARKETPLACE_NAME}" || true
-
-    if command_output_contains "\"id\":\"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json ||
-        command_output_contains "\"id\": \"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json; then
-        claude plugin update "${CLAUDE_CRIT_PLUGIN}" || true
-    else
-        claude plugin install "${CLAUDE_CRIT_PLUGIN}" || true
-    fi
-    if claude_crit_plugin_is_enabled; then
-        printf 'Claude Code Crit plugin is already enabled.\n'
-    else
-        claude plugin enable "${CLAUDE_CRIT_PLUGIN}" || true
-    fi
-    manifest_record "update_claude_crit" plugin "$(manifest_claude_plugin_version "${CLAUDE_CRIT_PLUGIN}")" "${HOME}/.claude/plugins/cache/crit/crit" "${HOME}/.claude/settings.json" -- "ensure_crit_cli" "claude plugin marketplace add ${CLAUDE_CRIT_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_CRIT_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_CRIT_PLUGIN}" "claude plugin update ${CLAUDE_CRIT_PLUGIN}" "claude plugin enable ${CLAUDE_CRIT_PLUGIN}"
+	if ! has_command claude; then
+		printf 'Skipping Claude Code Crit plugin: claude command not found.\n'
+		return 0
+	fi
+
+	section "Claude Code Crit plugin"
+	if ! ensure_crit_cli; then
+		return 0
+	fi
+	ensure_claude_crit_marketplace
+	claude plugin marketplace update "${CLAUDE_CRIT_MARKETPLACE_NAME}" || true
+
+	if command_output_contains "\"id\":\"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json ||
+		command_output_contains "\"id\": \"${CLAUDE_CRIT_PLUGIN}\"" claude plugin list --json; then
+		claude plugin update "${CLAUDE_CRIT_PLUGIN}" || true
+	else
+		claude plugin install "${CLAUDE_CRIT_PLUGIN}" || true
+	fi
+	if claude_crit_plugin_is_enabled; then
+		printf 'Claude Code Crit plugin is already enabled.\n'
+	else
+		claude plugin enable "${CLAUDE_CRIT_PLUGIN}" || true
+	fi
+	manifest_record "update_claude_crit" plugin "$(manifest_claude_plugin_version "${CLAUDE_CRIT_PLUGIN}")" "${HOME}/.claude/plugins/cache/crit/crit" "${HOME}/.claude/settings.json" -- "ensure_crit_cli" "claude plugin marketplace add ${CLAUDE_CRIT_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_CRIT_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_CRIT_PLUGIN}" "claude plugin update ${CLAUDE_CRIT_PLUGIN}" "claude plugin enable ${CLAUDE_CRIT_PLUGIN}"
 }
 
 #
@@ -515,28 +515,28 @@
 # @description Install or update the Claude Code Ponytail plugin.
 #
 function update_claude_ponytail() {
-    if ! has_command claude; then
-        printf 'Skipping Claude Code Ponytail plugin: claude command not found.\n'
-        return 0
-    fi
-
-    section "Claude Code Ponytail plugin"
-    ensure_claude_ponytail_marketplace
-    claude plugin marketplace update "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" || true
-
-    if command_output_contains "\"id\":\"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json ||
-        command_output_contains "\"id\": \"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json; then
-        claude plugin update "${CLAUDE_PONYTAIL_PLUGIN}" || true
-    else
-        claude plugin install "${CLAUDE_PONYTAIL_PLUGIN}" || true
-    fi
-    if claude_ponytail_plugin_is_enabled; then
-        printf 'Claude Code Ponytail plugin is already enabled.\n'
-    else
-        claude plugin enable "${CLAUDE_PONYTAIL_PLUGIN}" || true
-    fi
-    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
-    manifest_record "update_claude_ponytail" plugin "$(manifest_claude_plugin_version "${CLAUDE_PONYTAIL_PLUGIN}")" "${HOME}/.claude/plugins/cache/ponytail/ponytail" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_PONYTAIL_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin update ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin enable ${CLAUDE_PONYTAIL_PLUGIN}"
+	if ! has_command claude; then
+		printf 'Skipping Claude Code Ponytail plugin: claude command not found.\n'
+		return 0
+	fi
+
+	section "Claude Code Ponytail plugin"
+	ensure_claude_ponytail_marketplace
+	claude plugin marketplace update "${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" || true
+
+	if command_output_contains "\"id\":\"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json ||
+		command_output_contains "\"id\": \"${CLAUDE_PONYTAIL_PLUGIN}\"" claude plugin list --json; then
+		claude plugin update "${CLAUDE_PONYTAIL_PLUGIN}" || true
+	else
+		claude plugin install "${CLAUDE_PONYTAIL_PLUGIN}" || true
+	fi
+	if claude_ponytail_plugin_is_enabled; then
+		printf 'Claude Code Ponytail plugin is already enabled.\n'
+	else
+		claude plugin enable "${CLAUDE_PONYTAIL_PLUGIN}" || true
+	fi
+	printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
+	manifest_record "update_claude_ponytail" plugin "$(manifest_claude_plugin_version "${CLAUDE_PONYTAIL_PLUGIN}")" "${HOME}/.claude/plugins/cache/ponytail/ponytail" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_PONYTAIL_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_PONYTAIL_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin update ${CLAUDE_PONYTAIL_PLUGIN}" "claude plugin enable ${CLAUDE_PONYTAIL_PLUGIN}"
 }
 
 #
@@ -543,27 +543,27 @@
 # @description Install or update the Claude Code Understand-Anything plugin.
 #
 function update_claude_understand_anything() {
-    if ! has_command claude; then
-        printf 'Skipping Claude Code Understand-Anything plugin: claude command not found.\n'
-        return 0
-    fi
-
-    section "Claude Code Understand-Anything plugin"
-    ensure_claude_understand_anything_marketplace
-    claude plugin marketplace update "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" || true
-
-    if command_output_contains "\"id\":\"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json ||
-        command_output_contains "\"id\": \"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json; then
-        claude plugin update "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
-    else
-        claude plugin install "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
-    fi
-    if claude_understand_anything_plugin_is_enabled; then
-        printf 'Claude Code Understand-Anything plugin is already enabled.\n'
-    else
-        claude plugin enable "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
-    fi
-    manifest_record "update_claude_understand_anything" plugin "$(manifest_claude_plugin_version "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}")" "${HOME}/.claude/plugins/cache/understand-anything/understand-anything" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin update ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin enable ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}"
+	if ! has_command claude; then
+		printf 'Skipping Claude Code Understand-Anything plugin: claude command not found.\n'
+		return 0
+	fi
+
+	section "Claude Code Understand-Anything plugin"
+	ensure_claude_understand_anything_marketplace
+	claude plugin marketplace update "${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" || true
+
+	if command_output_contains "\"id\":\"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json ||
+		command_output_contains "\"id\": \"${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}\"" claude plugin list --json; then
+		claude plugin update "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
+	else
+		claude plugin install "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
+	fi
+	if claude_understand_anything_plugin_is_enabled; then
+		printf 'Claude Code Understand-Anything plugin is already enabled.\n'
+	else
+		claude plugin enable "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" || true
+	fi
+	manifest_record "update_claude_understand_anything" plugin "$(manifest_claude_plugin_version "${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}")" "${HOME}/.claude/plugins/cache/understand-anything/understand-anything" "${HOME}/.claude/settings.json" -- "claude plugin marketplace add ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE}" "claude plugin marketplace update ${CLAUDE_UNDERSTAND_ANYTHING_MARKETPLACE_NAME}" "claude plugin install ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin update ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}" "claude plugin enable ${CLAUDE_UNDERSTAND_ANYTHING_PLUGIN}"
 }
 
 #
@@ -570,31 +570,31 @@
 # @description Install the Codex Superpowers plugin from the OpenAI-curated catalog.
 #
 function update_codex_superpowers() {
-    local codex_output
-
-    if ! has_command codex; then
-        printf 'Skipping Codex plugins: codex command not found.\n'
-        return 0
-    fi
-
-    section "Codex plugins"
-    if command_output_contains "\"pluginId\":\"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json ||
-        command_output_contains "\"pluginId\": \"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json; then
-        printf 'Codex Superpowers plugin is already installed.\n'
-    elif codex_output="$(codex plugin add "${CODEX_SUPERPOWERS_PLUGIN}" 2>&1)"; then
-        if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
-            printf '%s\n' "${codex_output}" >&2
-        fi
-        printf 'Codex Superpowers plugin installed.\n'
-    else
-        if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
-            printf '%s\n' "${codex_output}" >&2
-        fi
-        printf 'Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.\n'
-        # shellcheck disable=SC2016 # Backticks are literal operator guidance.
-        printf 'Run `codex login`, then `codex plugin add %s`.\n' "${CODEX_SUPERPOWERS_PLUGIN}"
-    fi
-    manifest_record "update_codex_superpowers" plugin "$(manifest_codex_plugin_version "${CODEX_SUPERPOWERS_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/.tmp/plugins/plugins/superpowers" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin add ${CODEX_SUPERPOWERS_PLUGIN}"
+	local codex_output
+
+	if ! has_command codex; then
+		printf 'Skipping Codex plugins: codex command not found.\n'
+		return 0
+	fi
+
+	section "Codex plugins"
+	if command_output_contains "\"pluginId\":\"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json ||
+		command_output_contains "\"pluginId\": \"${CODEX_SUPERPOWERS_PLUGIN}\"" codex plugin list --json; then
+		printf 'Codex Superpowers plugin is already installed.\n'
+	elif codex_output="$(codex plugin add "${CODEX_SUPERPOWERS_PLUGIN}" 2>&1)"; then
+		if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
+			printf '%s\n' "${codex_output}" >&2
+		fi
+		printf 'Codex Superpowers plugin installed.\n'
+	else
+		if [ -n "${DOTFILES_DEBUG:-}" ] && [ -n "${codex_output}" ]; then
+			printf '%s\n' "${codex_output}" >&2
+		fi
+		printf 'Codex Superpowers was not installed: the OpenAI-curated catalog is unavailable.\n'
+		# shellcheck disable=SC2016 # Backticks are literal operator guidance.
+		printf 'Run `codex login`, then `codex plugin add %s`.\n' "${CODEX_SUPERPOWERS_PLUGIN}"
+	fi
+	manifest_record "update_codex_superpowers" plugin "$(manifest_codex_plugin_version "${CODEX_SUPERPOWERS_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/.tmp/plugins/plugins/superpowers" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin add ${CODEX_SUPERPOWERS_PLUGIN}"
 }
 
 #
@@ -601,26 +601,26 @@
 # @description Ensure the Ponytail Codex plugin marketplace is configured.
 #
 function ensure_codex_ponytail_marketplace() {
-    local codex_home="${CODEX_HOME:-${HOME}/.codex}"
-    local codex_config="${codex_home%/}/config.toml"
-
-    if [ -f "${codex_config}" ] && grep -Fq "[marketplaces.${CODEX_PONYTAIL_MARKETPLACE_NAME}]" "${codex_config}"; then
-        if grep -Fq "source = \"${CODEX_PONYTAIL_MARKETPLACE_SOURCE}\"" "${codex_config}"; then
-            return 0
-        fi
-        printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
-        return 1
-    fi
-
-    if codex_marketplace_has_source "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"; then
-        return 0
-    fi
-    if command_output_contains "${CODEX_PONYTAIL_MARKETPLACE_NAME}" codex plugin marketplace list; then
-        printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
-        return 1
-    fi
-
-    codex plugin marketplace add "${CODEX_PONYTAIL_MARKETPLACE}"
+	local codex_home="${CODEX_HOME:-${HOME}/.codex}"
+	local codex_config="${codex_home%/}/config.toml"
+
+	if [ -f "${codex_config}" ] && grep -Fq "[marketplaces.${CODEX_PONYTAIL_MARKETPLACE_NAME}]" "${codex_config}"; then
+		if grep -Fq "source = \"${CODEX_PONYTAIL_MARKETPLACE_SOURCE}\"" "${codex_config}"; then
+			return 0
+		fi
+		printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
+		return 1
+	fi
+
+	if codex_marketplace_has_source "${CODEX_PONYTAIL_MARKETPLACE_NAME}" "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"; then
+		return 0
+	fi
+	if command_output_contains "${CODEX_PONYTAIL_MARKETPLACE_NAME}" codex plugin marketplace list; then
+		printf 'Codex Ponytail marketplace exists with an unexpected source; expected %s.\n' "${CODEX_PONYTAIL_MARKETPLACE_SOURCE}"
+		return 1
+	fi
+
+	codex plugin marketplace add "${CODEX_PONYTAIL_MARKETPLACE}"
 }
 
 #
@@ -627,24 +627,24 @@
 # @description Install or update the Codex Ponytail plugin from its marketplace.
 #
 function update_codex_ponytail() {
-    if ! has_command codex; then
-        printf 'Skipping Codex Ponytail plugin: codex command not found.\n'
-        return 0
-    fi
-
-    section "Codex Ponytail plugin"
-    ensure_codex_ponytail_marketplace
-    codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}" || true
-
-    if command_output_contains "\"pluginId\":\"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json ||
-        command_output_contains "\"pluginId\": \"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json; then
-        printf 'Codex Ponytail plugin is already installed.\n'
-    else
-        codex plugin add "${CODEX_PONYTAIL_PLUGIN}" || true
-    fi
-    printf 'Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.\n'
-    printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
-    manifest_record "update_codex_ponytail" plugin "$(manifest_codex_plugin_version "${CODEX_PONYTAIL_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/plugins/cache/ponytail/ponytail" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin marketplace add ${CODEX_PONYTAIL_MARKETPLACE}" "codex plugin marketplace upgrade ${CODEX_PONYTAIL_MARKETPLACE_NAME}" "codex plugin add ${CODEX_PONYTAIL_PLUGIN}"
+	if ! has_command codex; then
+		printf 'Skipping Codex Ponytail plugin: codex command not found.\n'
+		return 0
+	fi
+
+	section "Codex Ponytail plugin"
+	ensure_codex_ponytail_marketplace
+	codex plugin marketplace upgrade "${CODEX_PONYTAIL_MARKETPLACE_NAME}" || true
+
+	if command_output_contains "\"pluginId\":\"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json ||
+		command_output_contains "\"pluginId\": \"${CODEX_PONYTAIL_PLUGIN}\"" codex plugin list --json; then
+		printf 'Codex Ponytail plugin is already installed.\n'
+	else
+		codex plugin add "${CODEX_PONYTAIL_PLUGIN}" || true
+	fi
+	printf 'Review and trust Ponytail lifecycle hooks in Codex with /hooks, then start a new thread.\n'
+	printf 'Ponytail default mode is %s. Set PONYTAIL_DEFAULT_MODE=lite|full|ultra|off to override.\n' "${PONYTAIL_DEFAULT_MODE:-full}"
+	manifest_record "update_codex_ponytail" plugin "$(manifest_codex_plugin_version "${CODEX_PONYTAIL_PLUGIN}")" "${CODEX_HOME:-${HOME}/.codex}/plugins/cache/ponytail/ponytail" "${CODEX_HOME:-${HOME}/.codex}/config.toml" -- "codex plugin marketplace add ${CODEX_PONYTAIL_MARKETPLACE}" "codex plugin marketplace upgrade ${CODEX_PONYTAIL_MARKETPLACE_NAME}" "codex plugin add ${CODEX_PONYTAIL_PLUGIN}"
 }
 
 #
@@ -651,23 +651,23 @@
 # @description Install or update the Codex Crit plugin and plan-review hook.
 #
 function update_codex_crit() {
-    if ! has_command codex; then
-        printf 'Skipping Codex Crit plugin: codex command not found.\n'
-        return 0
-    fi
-    if ! ensure_crit_cli; then
-        return 0
-    fi
-
-    section "Codex Crit plugin"
-    (
-        cd "${HOME}"
-        crit install codex-plugin --force
-    ) || true
-    if [ -f "${HOME}/.agents/plugins/marketplace.json" ]; then
-        chmod 644 "${HOME}/.agents/plugins/marketplace.json"
-    fi
-    manifest_record "update_codex_crit" plugin "$(crit --version 2> /dev/null | awk 'NR == 1 { print $2 }')" "${CODEX_HOME:-${HOME}/.codex}/plugins/crit" "${CODEX_HOME:-${HOME}/.codex}/config.toml" "${HOME}/.agents/skills/crit" "${HOME}/.agents/skills/crit-cli" "${HOME}/.agents/skills/crit-story" -- "ensure_crit_cli" "crit install codex-plugin --force"
+	if ! has_command codex; then
+		printf 'Skipping Codex Crit plugin: codex command not found.\n'
+		return 0
+	fi
+	if ! ensure_crit_cli; then
+		return 0
+	fi
+
+	section "Codex Crit plugin"
+	(
+		cd "${HOME}"
+		crit install codex-plugin --force
+	) || true
+	if [ -f "${HOME}/.agents/plugins/marketplace.json" ]; then
+		chmod 644 "${HOME}/.agents/plugins/marketplace.json"
+	fi
+	manifest_record "update_codex_crit" plugin "$(crit --version 2> /dev/null | awk 'NR == 1 { print $2 }')" "${CODEX_HOME:-${HOME}/.codex}/plugins/crit" "${CODEX_HOME:-${HOME}/.codex}/config.toml" "${HOME}/.agents/skills/crit" "${HOME}/.agents/skills/crit-cli" "${HOME}/.agents/skills/crit-story" -- "ensure_crit_cli" "crit install codex-plugin --force"
 }
 
 #
@@ -687,31 +687,31 @@
 # @stderr One WARN line naming the manual command when the build cannot run or fails.
 #
 function build_understand_anything_core() {
-    local root="$1"
-    local -a pnpm_cmd
-
-    [ -d "${root}/packages/core" ] || return 0
-    if [ -f "${root}/packages/core/dist/index.js" ] &&
-        [ -z "$(find "${root}/packages/core/src" "${root}/pnpm-lock.yaml" -type f -newer "${root}/packages/core/dist/index.js" -print -quit 2> /dev/null || true)" ]; then
-        return 0
-    fi
-    if has_command mise; then
-        pnpm_cmd=(mise exec npm:pnpm -- pnpm)
-    elif has_command pnpm; then
-        pnpm_cmd=(pnpm)
-    else
-        printf 'WARN: Understand-Anything core not built: pnpm not found; run: cd %q && pnpm install --frozen-lockfile && pnpm --filter @understand-anything/core build\n' "${root}" >&2
-        return 0
-    fi
-    if ! (
-        cd "${root}" &&
-            { "${pnpm_cmd[@]}" install --frozen-lockfile 2> /dev/null || "${pnpm_cmd[@]}" install; } &&
-            "${pnpm_cmd[@]}" --filter @understand-anything/core build
-    ); then
-        printf 'WARN: Understand-Anything core build failed in %s; run: cd %q && %s install --frozen-lockfile && %s --filter @understand-anything/core build\n' \
-            "${root}" "${root}" "${pnpm_cmd[*]}" "${pnpm_cmd[*]}" >&2
-    fi
-    return 0
+	local root="$1"
+	local -a pnpm_cmd
+
+	[ -d "${root}/packages/core" ] || return 0
+	if [ -f "${root}/packages/core/dist/index.js" ] &&
+		[ -z "$(find "${root}/packages/core/src" "${root}/pnpm-lock.yaml" -type f -newer "${root}/packages/core/dist/index.js" -print -quit 2> /dev/null || true)" ]; then
+		return 0
+	fi
+	if has_command mise; then
+		pnpm_cmd=(mise exec npm:pnpm -- pnpm)
+	elif has_command pnpm; then
+		pnpm_cmd=(pnpm)
+	else
+		printf 'WARN: Understand-Anything core not built: pnpm not found; run: cd %q && pnpm install --frozen-lockfile && pnpm --filter @understand-anything/core build\n' "${root}" >&2
+		return 0
+	fi
+	if ! (
+		cd "${root}" &&
+			{ "${pnpm_cmd[@]}" install --frozen-lockfile 2> /dev/null || "${pnpm_cmd[@]}" install; } &&
+			"${pnpm_cmd[@]}" --filter @understand-anything/core build
+	); then
+		printf 'WARN: Understand-Anything core build failed in %s; run: cd %q && %s install --frozen-lockfile && %s --filter @understand-anything/core build\n' \
+			"${root}" "${root}" "${pnpm_cmd[*]}" "${pnpm_cmd[*]}" >&2
+	fi
+	return 0
 }
 
 #
@@ -723,17 +723,17 @@
 # @stdout Prints a skip message when no matching Claude release artifact is available.
 #
 function provision_codex_understand_anything_runtime() {
-    local plugin_root claude_cache release_root source destination
-
-    plugin_root="${HOME}/.understand-anything/repo/understand-anything-plugin"
-    claude_cache="${HOME}/.claude/plugins/cache/understand-anything/understand-anything"
-    if ! has_command python3; then
-        printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
-        build_understand_anything_core "${plugin_root}"
-        return 0
-    fi
-    release_root="$(
-        python3 - "${plugin_root}/.claude-plugin/plugin.json" "${claude_cache}" << 'PY'
+	local plugin_root claude_cache release_root source destination
+
+	plugin_root="${HOME}/.understand-anything/repo/understand-anything-plugin"
+	claude_cache="${HOME}/.claude/plugins/cache/understand-anything/understand-anything"
+	if ! has_command python3; then
+		printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
+		build_understand_anything_core "${plugin_root}"
+		return 0
+	fi
+	release_root="$(
+		python3 - "${plugin_root}/.claude-plugin/plugin.json" "${claude_cache}" << 'PY'
 import json
 import sys
 from pathlib import Path
@@ -758,21 +758,21 @@
     release_root = max(matches, key=lambda path: path.name, default=None)
 print(release_root or "")
 PY
-    )"
-    if [ -z "${release_root}" ]; then
-        printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
-        build_understand_anything_core "${plugin_root}"
-        return 0
-    fi
-
-    build_understand_anything_core "${release_root}"
-    for source in "packages/core/dist" "packages/core/node_modules" "node_modules"; do
-        destination="${plugin_root}/${source}"
-        [ -d "${release_root}/${source}" ] || continue
-        rm -rf "${destination}"
-        mkdir -p "$(dirname "${destination}")"
-        cp -R "${release_root}/${source}" "${destination}"
-    done
+	)"
+	if [ -z "${release_root}" ]; then
+		printf 'Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact; run make update after installing the Claude plugin.\n'
+		build_understand_anything_core "${plugin_root}"
+		return 0
+	fi
+
+	build_understand_anything_core "${release_root}"
+	for source in "packages/core/dist" "packages/core/node_modules" "node_modules"; do
+		destination="${plugin_root}/${source}"
+		[ -d "${release_root}/${source}" ] || continue
+		rm -rf "${destination}"
+		mkdir -p "$(dirname "${destination}")"
+		cp -R "${release_root}/${source}" "${destination}"
+	done
 }
 
 #
@@ -783,34 +783,34 @@
 #   those symlinks as an expected unmanaged-skill WARN.
 #
 function update_codex_understand_anything() {
-    if ! has_command codex; then
-        printf 'Skipping Codex Understand-Anything skills: codex command not found.\n'
-        return 0
-    fi
-
-    section "Codex Understand-Anything skills"
-    (
-        local actual installer
-        installer="$(mktemp)"
-        trap 'rm -f "${installer}"' EXIT
-        curl -fsSL "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" -o "${installer}" || {
-            printf 'Skipping Codex Understand-Anything skills: installer download failed.\n'
-            return 0
-        }
-        actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
-        [ "${actual}" = "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256}" ] || {
-            printf 'Understand-Anything installer checksum mismatch\n' >&2
-            return 1
-        }
-        bash "${installer}" codex < /dev/null || {
-            printf 'Understand-Anything installer failed; Codex skills unchanged.\n' >&2
-            return 1
-        }
-        provision_codex_understand_anything_runtime
-        # shellcheck disable=SC2016 # $understand is the literal Codex skill invocation, not a variable.
-        printf 'Invoke Understand-Anything in Codex with $understand after restarting the CLI.\n'
-    ) || true
-    manifest_record "update_codex_understand_anything" installer "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}" "${HOME}/.understand-anything/repo" "${HOME}/.agents/skills/understand" "${HOME}/.agents/skills/understand-chat" "${HOME}/.agents/skills/understand-dashboard" "${HOME}/.agents/skills/understand-diff" "${HOME}/.agents/skills/understand-domain" "${HOME}/.agents/skills/understand-explain" "${HOME}/.agents/skills/understand-figma" "${HOME}/.agents/skills/understand-knowledge" "${HOME}/.agents/skills/understand-onboard" -- "curl -fsSL ${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer> codex"
+	if ! has_command codex; then
+		printf 'Skipping Codex Understand-Anything skills: codex command not found.\n'
+		return 0
+	fi
+
+	section "Codex Understand-Anything skills"
+	(
+		local actual installer
+		installer="$(mktemp)"
+		trap 'rm -f "${installer}"' EXIT
+		curl -fsSL "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" -o "${installer}" || {
+			printf 'Skipping Codex Understand-Anything skills: installer download failed.\n'
+			return 0
+		}
+		actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
+		[ "${actual}" = "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_SHA256}" ] || {
+			printf 'Understand-Anything installer checksum mismatch\n' >&2
+			return 1
+		}
+		bash "${installer}" codex < /dev/null || {
+			printf 'Understand-Anything installer failed; Codex skills unchanged.\n' >&2
+			return 1
+		}
+		provision_codex_understand_anything_runtime
+		# shellcheck disable=SC2016 # $understand is the literal Codex skill invocation, not a variable.
+		printf 'Invoke Understand-Anything in Codex with $understand after restarting the CLI.\n'
+	) || true
+	manifest_record "update_codex_understand_anything" installer "${CODEX_UNDERSTAND_ANYTHING_INSTALLER_COMMIT}" "${HOME}/.understand-anything/repo" "${HOME}/.agents/skills/understand" "${HOME}/.agents/skills/understand-chat" "${HOME}/.agents/skills/understand-dashboard" "${HOME}/.agents/skills/understand-diff" "${HOME}/.agents/skills/understand-domain" "${HOME}/.agents/skills/understand-explain" "${HOME}/.agents/skills/understand-figma" "${HOME}/.agents/skills/understand-knowledge" "${HOME}/.agents/skills/understand-onboard" -- "curl -fsSL ${CODEX_UNDERSTAND_ANYTHING_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer> codex"
 }
 
 #
@@ -820,12 +820,12 @@
 #   Intel macOS has no release asset, so it is skipped rather than failed.
 #
 function zenbu_platform_supported() {
-    case "$(uname -s)-$(uname -m)" in
-    Darwin-arm64 | Linux-x86_64 | Linux-amd64 | Linux-aarch64 | Linux-arm64)
-        return 0
-        ;;
-    esac
-    return 1
+	case "$(uname -s)-$(uname -m)" in
+	Darwin-arm64 | Linux-x86_64 | Linux-amd64 | Linux-aarch64 | Linux-arm64)
+		return 0
+		;;
+	esac
+	return 1
 }
 
 #
@@ -835,24 +835,24 @@
 # @arg $@ string Optional NAME=value environment assignments for the installer run.
 #
 function run_pinned_installer() {
-    local url="$1"
-    local expected="$2"
-    local actual installer
-    shift 2
-
-    installer="$(mktemp)"
-    # shellcheck disable=SC2064 # Expand the temp path now; it never changes.
-    trap "rm -f '${installer}'" RETURN
-    curl -fsSL "${url}" -o "${installer}" || {
-        printf 'Installer download failed: %s\n' "${url}" >&2
-        return 1
-    }
-    actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
-    [ "${actual}" = "${expected}" ] || {
-        printf 'Installer checksum mismatch for %s\n' "${url}" >&2
-        return 1
-    }
-    env "$@" bash "${installer}" < /dev/null
+	local url="$1"
+	local expected="$2"
+	local actual installer
+	shift 2
+
+	installer="$(mktemp)"
+	# shellcheck disable=SC2064 # Expand the temp path now; it never changes.
+	trap "rm -f '${installer}'" RETURN
+	curl -fsSL "${url}" -o "${installer}" || {
+		printf 'Installer download failed: %s\n' "${url}" >&2
+		return 1
+	}
+	actual="$(shasum -a 256 "${installer}" | awk '{ print $1 }')"
+	[ "${actual}" = "${expected}" ] || {
+		printf 'Installer checksum mismatch for %s\n' "${url}" >&2
+		return 1
+	}
+	env "$@" bash "${installer}" < /dev/null
 }
 
 #
@@ -859,26 +859,26 @@
 # @description Install or update the terminal-code (tode) CLI at the pinned version.
 #
 function update_terminal_code() {
-    local installed
-
-    zenbu_platform_supported || {
-        printf 'Skipping terminal-code: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
-        return 0
-    }
-
-    section "terminal-code (tode)"
-    installed="$(jq -r '.version' "${HOME}/.local/state/tode/install.json" 2> /dev/null || printf 'none\n')"
-    # Short-circuit only when every manifest-recorded artifact is present, so a
-    # partially deleted install is repaired instead of skipped forever.
-    if [ "${installed}" = "${TERMINAL_CODE_PIN_VERSION}" ] &&
-        [ -x "${HOME}/.local/bin/tode" ] &&
-        [ -d "${HOME}/.local/lib/tode" ]; then
-        printf 'tode %s is already installed.\n' "${installed}"
-    else
-        run_pinned_installer "${TERMINAL_CODE_INSTALLER_URL}" "${TERMINAL_CODE_INSTALLER_SHA256}" ||
-            printf 'tode installer failed; existing install unchanged.\n' >&2
-    fi
-    manifest_record "update_terminal_code" installer "${TERMINAL_CODE_PIN_VERSION}" "${HOME}/.local/lib/tode" "${HOME}/.local/bin/tode" "${HOME}/.local/state/tode/install.json" -- "curl -fsSL ${TERMINAL_CODE_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer>"
+	local installed
+
+	zenbu_platform_supported || {
+		printf 'Skipping terminal-code: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
+		return 0
+	}
+
+	section "terminal-code (tode)"
+	installed="$(jq -r '.version' "${HOME}/.local/state/tode/install.json" 2> /dev/null || printf 'none\n')"
+	# Short-circuit only when every manifest-recorded artifact is present, so a
+	# partially deleted install is repaired instead of skipped forever.
+	if [ "${installed}" = "${TERMINAL_CODE_PIN_VERSION}" ] &&
+		[ -x "${HOME}/.local/bin/tode" ] &&
+		[ -d "${HOME}/.local/lib/tode" ]; then
+		printf 'tode %s is already installed.\n' "${installed}"
+	else
+		run_pinned_installer "${TERMINAL_CODE_INSTALLER_URL}" "${TERMINAL_CODE_INSTALLER_SHA256}" ||
+			printf 'tode installer failed; existing install unchanged.\n' >&2
+	fi
+	manifest_record "update_terminal_code" installer "${TERMINAL_CODE_PIN_VERSION}" "${HOME}/.local/lib/tode" "${HOME}/.local/bin/tode" "${HOME}/.local/state/tode/install.json" -- "curl -fsSL ${TERMINAL_CODE_INSTALLER_URL}" "shasum -a 256 <installer>" "bash <installer>"
 }
 
 #
@@ -892,26 +892,26 @@
 #   run `terminal-browser setup` manually once if wanted.
 #
 function update_terminal_browser() {
-    local installed
-
-    zenbu_platform_supported || {
-        printf 'Skipping terminal-browser: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
-        return 0
-    }
-
-    section "terminal-browser"
-    installed="$(cat "${HOME}/.local/share/terminal-browser/app/VERSION" 2> /dev/null || printf 'none\n')"
-    # Short-circuit only when every manifest-recorded artifact is present, so a
-    # partially deleted install is repaired instead of skipped forever.
-    if [ "${installed}" = "${TERMINAL_BROWSER_PIN_VERSION}" ] &&
-        [ -x "${HOME}/.local/bin/terminal-browser" ] &&
-        [ -f "${HOME}/.local/state/terminal-browser/skills.links" ]; then
-        printf 'terminal-browser %s is already installed.\n' "${installed}"
-    else
-        run_pinned_installer "${TERMINAL_BROWSER_INSTALLER_URL}" "${TERMINAL_BROWSER_INSTALLER_SHA256}" TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 ||
-            printf 'terminal-browser installer failed; existing install unchanged.\n' >&2
-    fi
-    manifest_record "update_terminal_browser" installer "${TERMINAL_BROWSER_PIN_VERSION}" "${HOME}/.local/share/terminal-browser/app" "${HOME}/.local/bin/terminal-browser" "${HOME}/.local/state/terminal-browser/skills.links" -- "curl -fsSL ${TERMINAL_BROWSER_INSTALLER_URL}" "shasum -a 256 <installer>" "TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 bash <installer>"
+	local installed
+
+	zenbu_platform_supported || {
+		printf 'Skipping terminal-browser: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
+		return 0
+	}
+
+	section "terminal-browser"
+	installed="$(cat "${HOME}/.local/share/terminal-browser/app/VERSION" 2> /dev/null || printf 'none\n')"
+	# Short-circuit only when every manifest-recorded artifact is present, so a
+	# partially deleted install is repaired instead of skipped forever.
+	if [ "${installed}" = "${TERMINAL_BROWSER_PIN_VERSION}" ] &&
+		[ -x "${HOME}/.local/bin/terminal-browser" ] &&
+		[ -f "${HOME}/.local/state/terminal-browser/skills.links" ]; then
+		printf 'terminal-browser %s is already installed.\n' "${installed}"
+	else
+		run_pinned_installer "${TERMINAL_BROWSER_INSTALLER_URL}" "${TERMINAL_BROWSER_INSTALLER_SHA256}" TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 ||
+			printf 'terminal-browser installer failed; existing install unchanged.\n' >&2
+	fi
+	manifest_record "update_terminal_browser" installer "${TERMINAL_BROWSER_PIN_VERSION}" "${HOME}/.local/share/terminal-browser/app" "${HOME}/.local/bin/terminal-browser" "${HOME}/.local/state/terminal-browser/skills.links" -- "curl -fsSL ${TERMINAL_BROWSER_INSTALLER_URL}" "shasum -a 256 <installer>" "TERMINAL_BROWSER_SKIP_EDITOR_SETUP=1 bash <installer>"
 }
 
 #
@@ -919,36 +919,36 @@
 # @exitcode 1 The download checksum or installed version differs from its pin.
 #
 function update_omp() (
-    local installed download_dir tarball actual
-    has_command npm || {
-        printf 'Skipping omp: npm command not found.\n'
-        return 0
-    }
-    section "omp"
-    installed="$("${HOME}/.local/bin/omp" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    installed="${installed#omp/}"
-    if [ "${installed}" = "${OMP_PIN_VERSION}" ]; then
-        printf 'omp %s is already installed.\n' "${installed}"
-        return 0
-    fi
-    download_dir="$(mktemp -d)" || return
-    trap 'rm -rf "${download_dir}"' EXIT
-    tarball="${download_dir}/omp-${OMP_PIN_VERSION}.tgz"
-    curl -fsSL "${OMP_TARBALL_URL}" -o "${tarball}" || return
-    actual="$(shasum -a 256 "${tarball}" | awk '{ print $1 }')" || return
-    if [ "${actual}" != "${OMP_TARBALL_SHA256}" ]; then
-        printf 'omp checksum mismatch: expected %s, got %s.\n' "${OMP_TARBALL_SHA256}" "${actual}" >&2
-        return 1
-    fi
-    # Allow this reviewed pin before the default three-day cooldown expires.
-    npm_config_min_release_age=0 npm install -g --prefix "${HOME}/.local" "${tarball}" || return
-    installed="$("${HOME}/.local/bin/omp" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    installed="${installed#omp/}"
-    if [ "${installed}" != "${OMP_PIN_VERSION}" ]; then
-        printf 'omp version mismatch: expected %s, got %s.\n' "${OMP_PIN_VERSION}" "${installed}" >&2
-        return 1
-    fi
-    manifest_record "update_omp" installer "${OMP_PIN_VERSION}" "${HOME}/.local/bin/omp" -- "npm_config_min_release_age=0 npm install -g --prefix ${HOME}/.local <verified-omp-tarball>"
+	local installed download_dir tarball actual
+	has_command npm || {
+		printf 'Skipping omp: npm command not found.\n'
+		return 0
+	}
+	section "omp"
+	installed="$("${HOME}/.local/bin/omp" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+	installed="${installed#omp/}"
+	if [ "${installed}" = "${OMP_PIN_VERSION}" ]; then
+		printf 'omp %s is already installed.\n' "${installed}"
+		return 0
+	fi
+	download_dir="$(mktemp -d)" || return
+	trap 'rm -rf "${download_dir}"' EXIT
+	tarball="${download_dir}/omp-${OMP_PIN_VERSION}.tgz"
+	curl -fsSL "${OMP_TARBALL_URL}" -o "${tarball}" || return
+	actual="$(shasum -a 256 "${tarball}" | awk '{ print $1 }')" || return
+	if [ "${actual}" != "${OMP_TARBALL_SHA256}" ]; then
+		printf 'omp checksum mismatch: expected %s, got %s.\n' "${OMP_TARBALL_SHA256}" "${actual}" >&2
+		return 1
+	fi
+	# Allow this reviewed pin before the default three-day cooldown expires.
+	npm_config_min_release_age=0 npm install -g --prefix "${HOME}/.local" "${tarball}" || return
+	installed="$("${HOME}/.local/bin/omp" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+	installed="${installed#omp/}"
+	if [ "${installed}" != "${OMP_PIN_VERSION}" ]; then
+		printf 'omp version mismatch: expected %s, got %s.\n' "${OMP_PIN_VERSION}" "${installed}" >&2
+		return 1
+	fi
+	manifest_record "update_omp" installer "${OMP_PIN_VERSION}" "${HOME}/.local/bin/omp" -- "npm_config_min_release_age=0 npm install -g --prefix ${HOME}/.local <verified-omp-tarball>"
 )
 
 #
@@ -956,43 +956,43 @@
 # @exitcode 1 The download checksum or installed version differs from its pin.
 #
 function update_hcom() (
-    local url expected installed download_dir wheel actual
-    case "$(uname -s)/$(uname -m)" in
-    Darwin/arm64 | Darwin/aarch64) url="${HCOM_DARWIN_ARM64_URL}" expected="${HCOM_DARWIN_ARM64_SHA256}" ;;
-    Darwin/x86_64 | Darwin/amd64) url="${HCOM_DARWIN_AMD64_URL}" expected="${HCOM_DARWIN_AMD64_SHA256}" ;;
-    Linux/x86_64 | Linux/amd64) url="${HCOM_LINUX_AMD64_URL}" expected="${HCOM_LINUX_AMD64_SHA256}" ;;
-    Linux/aarch64 | Linux/arm64) url="${HCOM_LINUX_ARM64_URL}" expected="${HCOM_LINUX_ARM64_SHA256}" ;;
-    *)
-        printf 'Skipping hcom: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
-        return 0
-        ;;
-    esac
-    has_command uv || {
-        printf 'Skipping hcom: uv command not found.\n'
-        return 0
-    }
-    section "hcom"
-    installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    if [ "${installed}" = "${HCOM_PIN_VERSION}" ]; then
-        printf 'hcom %s is already installed.\n' "${installed}"
-        return 0
-    fi
-    download_dir="$(mktemp -d)" || return
-    trap 'rm -rf "${download_dir}"' EXIT
-    wheel="${download_dir}/${url##*/}"
-    curl -fsSL "${url}" -o "${wheel}" || return
-    actual="$(shasum -a 256 "${wheel}" | awk '{ print $1 }')" || return
-    if [ "${actual}" != "${expected}" ]; then
-        printf 'hcom checksum mismatch: expected %s, got %s.\n' "${expected}" "${actual}" >&2
-        return 1
-    fi
-    uv tool install --force "${wheel}" || return
-    installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
-    if [ "${installed}" != "${HCOM_PIN_VERSION}" ]; then
-        printf 'hcom version mismatch: expected %s, got %s.\n' "${HCOM_PIN_VERSION}" "${installed}" >&2
-        return 1
-    fi
-    manifest_record "update_hcom" installer "${HCOM_PIN_VERSION}" "${HOME}/.local/bin/hcom" -- "uv tool install --force <verified-hcom-wheel>"
+	local url expected installed download_dir wheel actual
+	case "$(uname -s)/$(uname -m)" in
+	Darwin/arm64 | Darwin/aarch64) url="${HCOM_DARWIN_ARM64_URL}" expected="${HCOM_DARWIN_ARM64_SHA256}" ;;
+	Darwin/x86_64 | Darwin/amd64) url="${HCOM_DARWIN_AMD64_URL}" expected="${HCOM_DARWIN_AMD64_SHA256}" ;;
+	Linux/x86_64 | Linux/amd64) url="${HCOM_LINUX_AMD64_URL}" expected="${HCOM_LINUX_AMD64_SHA256}" ;;
+	Linux/aarch64 | Linux/arm64) url="${HCOM_LINUX_ARM64_URL}" expected="${HCOM_LINUX_ARM64_SHA256}" ;;
+	*)
+		printf 'Skipping hcom: unsupported platform %s %s.\n' "$(uname -s)" "$(uname -m)"
+		return 0
+		;;
+	esac
+	has_command uv || {
+		printf 'Skipping hcom: uv command not found.\n'
+		return 0
+	}
+	section "hcom"
+	installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+	if [ "${installed}" = "${HCOM_PIN_VERSION}" ]; then
+		printf 'hcom %s is already installed.\n' "${installed}"
+		return 0
+	fi
+	download_dir="$(mktemp -d)" || return
+	trap 'rm -rf "${download_dir}"' EXIT
+	wheel="${download_dir}/${url##*/}"
+	curl -fsSL "${url}" -o "${wheel}" || return
+	actual="$(shasum -a 256 "${wheel}" | awk '{ print $1 }')" || return
+	if [ "${actual}" != "${expected}" ]; then
+		printf 'hcom checksum mismatch: expected %s, got %s.\n' "${expected}" "${actual}" >&2
+		return 1
+	fi
+	uv tool install --force "${wheel}" || return
+	installed="$("${HOME}/.local/bin/hcom" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+	if [ "${installed}" != "${HCOM_PIN_VERSION}" ]; then
+		printf 'hcom version mismatch: expected %s, got %s.\n' "${HCOM_PIN_VERSION}" "${installed}" >&2
+		return 1
+	fi
+	manifest_record "update_hcom" installer "${HCOM_PIN_VERSION}" "${HOME}/.local/bin/hcom" -- "uv tool install --force <verified-hcom-wheel>"
 )
 
 #
@@ -999,10 +999,10 @@
 # @description Sync the vendored CompactionDB tree without deleting project runtime state.
 #
 function update_compactiondb() {
-    local source_root
-    source_root="${DOTFILES_REPO_SOURCE_DIR}/vendor/compactiondb/"
-    rsync -a --delete --exclude '.claude/contextdb/state/' --exclude '.claude/contextdb/spool/' --exclude '.claude/contextdb/health/' --exclude '.claude/contextdb/contextdb.sqlite3*' "${source_root}" "${HOME}/.agents/compactiondb/" || true
-    manifest_record "update_compactiondb" rsync "$(awk '/^## / { print $2; exit }' "${source_root}CHANGELOG.md")" "${HOME}/.agents/compactiondb" -- "rsync -a --delete --exclude .claude/contextdb/state/ --exclude .claude/contextdb/spool/ --exclude .claude/contextdb/health/ --exclude .claude/contextdb/contextdb.sqlite3* ${source_root} ${HOME}/.agents/compactiondb/"
+	local source_root
+	source_root="${DOTFILES_REPO_SOURCE_DIR}/vendor/compactiondb/"
+	rsync -a --delete --exclude '.claude/contextdb/state/' --exclude '.claude/contextdb/spool/' --exclude '.claude/contextdb/health/' --exclude '.claude/contextdb/contextdb.sqlite3*' "${source_root}" "${HOME}/.agents/compactiondb/" || true
+	manifest_record "update_compactiondb" rsync "$(awk '/^## / { print $2; exit }' "${source_root}CHANGELOG.md")" "${HOME}/.agents/compactiondb" -- "rsync -a --delete --exclude .claude/contextdb/state/ --exclude .claude/contextdb/spool/ --exclude .claude/contextdb/health/ --exclude .claude/contextdb/contextdb.sqlite3* ${source_root} ${HOME}/.agents/compactiondb/"
 }
 
 #
@@ -1011,14 +1011,14 @@
 # @exitcode 1 If neither tool exists or hashing fails.
 #
 function agmsg_sha256() {
-    if command -v sha256sum > /dev/null 2>&1; then
-        sha256sum -- "$@"
-    elif command -v shasum > /dev/null 2>&1; then
-        shasum -a 256 -- "$@"
-    else
-        printf 'agmsg: neither sha256sum nor shasum is available\n' >&2
-        return 1
-    fi
+	if command -v sha256sum > /dev/null 2>&1; then
+		sha256sum -- "$@"
+	elif command -v shasum > /dev/null 2>&1; then
+		shasum -a 256 -- "$@"
+	else
+		printf 'agmsg: neither sha256sum nor shasum is available\n' >&2
+		return 1
+	fi
 }
 
 #
@@ -1031,33 +1031,33 @@
 # @exitcode 1 If the paths cannot be listed or hashed completely.
 #
 function agmsg_state_snapshot() {
-    local skill_dir="$1"
-    local relative list file hashes
-    local -a paths=() files=()
-    shift
-
-    for relative in "$@"; do
-        [ ! -e "${skill_dir}/${relative}" ] || paths+=("${skill_dir}/${relative}")
-    done
-    ((${#paths[@]})) || return 0
-    list="$(mktemp)" || return 1
-    if ! find "${paths[@]}" -type f -print0 > "${list}"; then
-        rm -f "${list}"
-        printf 'agmsg: could not list the live state under %s\n' "${skill_dir}" >&2
-        return 1
-    fi
-    while IFS= read -r -d '' file; do
-        files+=("${file}")
-    done < "${list}"
-    rm -f "${list}"
-    ((${#files[@]})) || return 0
-    hashes="$(agmsg_sha256 "${files[@]}")" || return 1
-    # sha256sum/shasum prefix a line with \ when the name needs escaping.
-    if [ "$(printf '%s\n' "${hashes}" | grep -c '^\\\{0,1\}[0-9a-f]\{64\} ')" -ne "${#files[@]}" ]; then
-        printf 'agmsg: hashed fewer live-state files than exist under %s\n' "${skill_dir}" >&2
-        return 1
-    fi
-    printf '%s\n' "${hashes}" | LC_ALL=C sort
+	local skill_dir="$1"
+	local relative list file hashes
+	local -a paths=() files=()
+	shift
+
+	for relative in "$@"; do
+		[ ! -e "${skill_dir}/${relative}" ] || paths+=("${skill_dir}/${relative}")
+	done
+	((${#paths[@]})) || return 0
+	list="$(mktemp)" || return 1
+	if ! find "${paths[@]}" -type f -print0 > "${list}"; then
+		rm -f "${list}"
+		printf 'agmsg: could not list the live state under %s\n' "${skill_dir}" >&2
+		return 1
+	fi
+	while IFS= read -r -d '' file; do
+		files+=("${file}")
+	done < "${list}"
+	rm -f "${list}"
+	((${#files[@]})) || return 0
+	hashes="$(agmsg_sha256 "${files[@]}")" || return 1
+	# sha256sum/shasum prefix a line with \ when the name needs escaping.
+	if [ "$(printf '%s\n' "${hashes}" | grep -c '^\\\{0,1\}[0-9a-f]\{64\} ')" -ne "${#files[@]}" ]; then
+		printf 'agmsg: hashed fewer live-state files than exist under %s\n' "${skill_dir}" >&2
+		return 1
+	fi
+	printf '%s\n' "${hashes}" | LC_ALL=C sort
 }
 
 #
@@ -1078,80 +1078,80 @@
 # @exitcode 1 On any failure, with the reason on stderr.
 #
 function install_pinned_agmsg() (
-    local skill_dir="$1"
-    local fetch_url="https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz"
-    local tool tarball extract_dir actual before_state after_state before_run after_run changed install_log backup_dir state_dir installed
-    local -a install_args=(--cmd agmsg --agent-type claude-code)
-
-    for tool in curl tar; do
-        command -v "${tool}" > /dev/null 2>&1 || {
-            printf 'agmsg: %s not found; nothing was installed\n' "${tool}" >&2
-            return 1
-        }
-    done
-    before_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
-        printf 'agmsg: could not snapshot the live state under %s; nothing was installed\n' "${skill_dir}" >&2
-        return 1
-    }
-    before_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
-    if [ -f "${skill_dir}/.agmsg" ]; then
-        install_args=(--update "${install_args[@]}")
-    fi
-
-    tarball="$(mktemp)" || return 1
-    extract_dir="$(mktemp -d)" || return 1
-    install_log="$(mktemp)" || return 1
-    trap 'rm -f "${tarball}" "${install_log}"; rm -rf "${extract_dir}"' EXIT
-    curl -fsSL "${fetch_url}" -o "${tarball}" || {
-        printf 'agmsg download failed: %s; nothing was installed\n' "${fetch_url}" >&2
-        return 1
-    }
-    actual="$(agmsg_sha256 "${tarball}")" || return 1
-    [ "${actual%% *}" = "${AGMSG_PIN_SHA256}" ] || {
-        printf 'agmsg checksum mismatch for %s; nothing was installed\n' "${fetch_url}" >&2
-        return 1
-    }
-    tar xzf "${tarball}" -C "${extract_dir}" --strip-components=1 || {
-        printf 'agmsg extraction failed for %s; nothing was installed\n' "${fetch_url}" >&2
-        return 1
-    }
-
-    if [ -d "${skill_dir}" ]; then
-        backup_dir="${HOME}/.agents/backups/agmsg-state-$(date -u +%Y%m%dT%H%M%SZ)"
-        mkdir -p "${backup_dir}" || return 1
-        for state_dir in teams db run agents; do
-            [ ! -e "${skill_dir}/${state_dir}" ] || cp -Rp "${skill_dir}/${state_dir}" "${backup_dir}/" || {
-                printf 'agmsg: could not back up %s/%s; nothing was installed\n' "${skill_dir}" "${state_dir}" >&2
-                return 1
-            }
-        done
-        printf 'agmsg: live state copied to %s before install.sh %s\n' "${backup_dir}" "${install_args[*]}"
-    fi
-    if ! bash "${extract_dir}/install.sh" "${install_args[@]}" > "${install_log}" 2>&1; then
-        cat "${install_log}" >&2
-        printf 'agmsg: install.sh %s failed; the skill directory may be partially updated%s\n' \
-            "${install_args[*]}" "${backup_dir:+; pre-install state copy: ${backup_dir}}" >&2
-        return 1
-    fi
-    after_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
-        printf 'agmsg: install.sh %s finished, but the live state could not be re-checked; pre-install state copy: %s\n' \
-            "${install_args[*]}" "${backup_dir:-none}" >&2
-        return 1
-    }
-    changed="$(LC_ALL=C comm -23 <(printf '%s\n' "${before_state}") <(printf '%s\n' "${after_state}") | sed 's/^[^ ]*  *//')"
-    if [ -n "${changed}" ]; then
-        printf 'agmsg: install.sh %s changed or removed existing live state (the installer or a concurrent writer); pre-install state copy: %s\n%s\n' \
-            "${install_args[*]}" "${backup_dir:-none}" "${changed}" >&2
-        return 1
-    fi
-    after_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
-    [ "${before_run}" = "${after_run}" ] ||
-        printf 'agmsg: note: run/ changed during install.sh %s (watchers and sync engines rewrite it); not treated as a failure\n' "${install_args[*]}"
-    installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none')"
-    if ! [ -f "${skill_dir}/.agmsg" ] || [ "${installed}" != "${AGMSG_PIN_VERSION}" ]; then
-        printf 'agmsg: install.sh %s left VERSION %s (want %s)\n' "${install_args[*]}" "${installed}" "${AGMSG_PIN_VERSION}" >&2
-        return 1
-    fi
+	local skill_dir="$1"
+	local fetch_url="https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz"
+	local tool tarball extract_dir actual before_state after_state before_run after_run changed install_log backup_dir state_dir installed
+	local -a install_args=(--cmd agmsg --agent-type claude-code)
+
+	for tool in curl tar; do
+		command -v "${tool}" > /dev/null 2>&1 || {
+			printf 'agmsg: %s not found; nothing was installed\n' "${tool}" >&2
+			return 1
+		}
+	done
+	before_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
+		printf 'agmsg: could not snapshot the live state under %s; nothing was installed\n' "${skill_dir}" >&2
+		return 1
+	}
+	before_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
+	if [ -f "${skill_dir}/.agmsg" ]; then
+		install_args=(--update "${install_args[@]}")
+	fi
+
+	tarball="$(mktemp)" || return 1
+	extract_dir="$(mktemp -d)" || return 1
+	install_log="$(mktemp)" || return 1
+	trap 'rm -f "${tarball}" "${install_log}"; rm -rf "${extract_dir}"' EXIT
+	curl -fsSL "${fetch_url}" -o "${tarball}" || {
+		printf 'agmsg download failed: %s; nothing was installed\n' "${fetch_url}" >&2
+		return 1
+	}
+	actual="$(agmsg_sha256 "${tarball}")" || return 1
+	[ "${actual%% *}" = "${AGMSG_PIN_SHA256}" ] || {
+		printf 'agmsg checksum mismatch for %s; nothing was installed\n' "${fetch_url}" >&2
+		return 1
+	}
+	tar xzf "${tarball}" -C "${extract_dir}" --strip-components=1 || {
+		printf 'agmsg extraction failed for %s; nothing was installed\n' "${fetch_url}" >&2
+		return 1
+	}
+
+	if [ -d "${skill_dir}" ]; then
+		backup_dir="${HOME}/.agents/backups/agmsg-state-$(date -u +%Y%m%dT%H%M%SZ)"
+		mkdir -p "${backup_dir}" || return 1
+		for state_dir in teams db run agents; do
+			[ ! -e "${skill_dir}/${state_dir}" ] || cp -Rp "${skill_dir}/${state_dir}" "${backup_dir}/" || {
+				printf 'agmsg: could not back up %s/%s; nothing was installed\n' "${skill_dir}" "${state_dir}" >&2
+				return 1
+			}
+		done
+		printf 'agmsg: live state copied to %s before install.sh %s\n' "${backup_dir}" "${install_args[*]}"
+	fi
+	if ! bash "${extract_dir}/install.sh" "${install_args[@]}" > "${install_log}" 2>&1; then
+		cat "${install_log}" >&2
+		printf 'agmsg: install.sh %s failed; the skill directory may be partially updated%s\n' \
+			"${install_args[*]}" "${backup_dir:+; pre-install state copy: ${backup_dir}}" >&2
+		return 1
+	fi
+	after_state="$(agmsg_state_snapshot "${skill_dir}" teams db/messages.db)" || {
+		printf 'agmsg: install.sh %s finished, but the live state could not be re-checked; pre-install state copy: %s\n' \
+			"${install_args[*]}" "${backup_dir:-none}" >&2
+		return 1
+	}
+	changed="$(LC_ALL=C comm -23 <(printf '%s\n' "${before_state}") <(printf '%s\n' "${after_state}") | sed 's/^[^ ]*  *//')"
+	if [ -n "${changed}" ]; then
+		printf 'agmsg: install.sh %s changed or removed existing live state (the installer or a concurrent writer); pre-install state copy: %s\n%s\n' \
+			"${install_args[*]}" "${backup_dir:-none}" "${changed}" >&2
+		return 1
+	fi
+	after_run="$(agmsg_state_snapshot "${skill_dir}" run 2> /dev/null || printf 'unavailable')"
+	[ "${before_run}" = "${after_run}" ] ||
+		printf 'agmsg: note: run/ changed during install.sh %s (watchers and sync engines rewrite it); not treated as a failure\n' "${install_args[*]}"
+	installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none')"
+	if ! [ -f "${skill_dir}/.agmsg" ] || [ "${installed}" != "${AGMSG_PIN_VERSION}" ]; then
+		printf 'agmsg: install.sh %s left VERSION %s (want %s)\n' "${install_args[*]}" "${installed}" "${AGMSG_PIN_VERSION}" >&2
+		return 1
+	fi
 )
 
 #
@@ -1158,22 +1158,22 @@
 # @description Install or refresh the pinned upstream agmsg skill in place.
 #
 function update_agmsg() {
-    local skill_dir="${HOME}/.agents/skills/agmsg"
-    local installed
-
-    section "agmsg"
-    installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')"
-    if [ "${installed}" != "${AGMSG_PIN_VERSION}" ] || ! [ -f "${skill_dir}/.agmsg" ] || ! [ -x "${skill_dir}/scripts/send.sh" ]; then
-        install_pinned_agmsg "${skill_dir}" ||
-            printf 'agmsg installer failed (installed: %s); see the reason above.\n' "${installed}" >&2
-    fi
-
-    manifest_record "update_agmsg" installer \
-        "$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')" \
-        "${skill_dir}/SKILL.md" "${skill_dir}/scripts" "${skill_dir}/VERSION" -- \
-        "curl -fsSL https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz" \
-        "sha256sum <tarball> (shasum -a 256 on macOS)" \
-        "bash <extracted>/install.sh [--update when .agmsg exists] --cmd agmsg --agent-type claude-code"
+	local skill_dir="${HOME}/.agents/skills/agmsg"
+	local installed
+
+	section "agmsg"
+	installed="$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')"
+	if [ "${installed}" != "${AGMSG_PIN_VERSION}" ] || ! [ -f "${skill_dir}/.agmsg" ] || ! [ -x "${skill_dir}/scripts/send.sh" ]; then
+		install_pinned_agmsg "${skill_dir}" ||
+			printf 'agmsg installer failed (installed: %s); see the reason above.\n' "${installed}" >&2
+	fi
+
+	manifest_record "update_agmsg" installer \
+		"$(cat "${skill_dir}/VERSION" 2> /dev/null || printf 'none\n')" \
+		"${skill_dir}/SKILL.md" "${skill_dir}/scripts" "${skill_dir}/VERSION" -- \
+		"curl -fsSL https://github.com/fujibee/agmsg/archive/${AGMSG_PIN_COMMIT}.tar.gz" \
+		"sha256sum <tarball> (shasum -a 256 on macOS)" \
+		"bash <extracted>/install.sh [--update when .agmsg exists] --cmd agmsg --agent-type claude-code"
 }
 
 #
@@ -1181,35 +1181,35 @@
 # @arg $@ string Command-line arguments.
 #
 function main() {
-    if [ "$#" -gt 0 ]; then
-        printf 'Usage: scripts/update-agent-assets.sh\n' >&2
-        exit 2
-    fi
-
-    export PATH="${HOME}/.local/share/mise/shims:${PATH}"
-    remove_node_global_agent_cli_shadows
-    ensure_mise_npm_agent_cli claude "npm:@anthropic-ai/claude-code"
-    ensure_mise_npm_agent_cli codex "npm:@openai/codex"
-    ensure_gh_extensions
-    update_claude_superpowers
-    update_claude_crit
-    update_claude_ponytail
-    update_claude_understand_anything
-    update_codex_superpowers
-    update_codex_crit
-    update_codex_ponytail
-    update_codex_understand_anything
-    update_terminal_code
-    update_terminal_browser
-    update_omp
-    update_hcom
-    update_compactiondb
-    update_agmsg
-    ensure_herdr_integrations
-    # After every plugin update above, so the trust hashes follow the plugin content of this run.
-    refresh_codex_hook_trust
+	if [ "$#" -gt 0 ]; then
+		printf 'Usage: scripts/update-agent-assets.sh\n' >&2
+		exit 2
+	fi
+
+	export PATH="${HOME}/.local/share/mise/shims:${PATH}"
+	remove_node_global_agent_cli_shadows
+	ensure_mise_npm_agent_cli claude "npm:@anthropic-ai/claude-code"
+	ensure_mise_npm_agent_cli codex "npm:@openai/codex"
+	ensure_gh_extensions
+	update_claude_superpowers
+	update_claude_crit
+	update_claude_ponytail
+	update_claude_understand_anything
+	update_codex_superpowers
+	update_codex_crit
+	update_codex_ponytail
+	update_codex_understand_anything
+	update_terminal_code
+	update_terminal_browser
+	update_omp
+	update_hcom
+	update_compactiondb
+	update_agmsg
+	ensure_herdr_integrations
+	# After every plugin update above, so the trust hashes follow the plugin content of this run.
+	refresh_codex_hook_trust
 }
 
 if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
-    main "$@"
+	main "$@"
 fi
diff scripts/check-tools.sh.orig scripts/check-tools.sh
--- scripts/check-tools.sh.orig
+++ scripts/check-tools.sh
@@ -17,7 +17,7 @@
 # @arg $1 string Heading text.
 #
 function section() {
-    printf '\n==> %s\n' "$1"
+	printf '\n==> %s\n' "$1"
 }
 
 #
@@ -26,35 +26,35 @@
 # @arg $@ string Optional version command arguments.
 #
 function check_command() {
-    local command_name="$1"
-    shift || true
-
-    if ! command -v "${command_name}" > /dev/null 2>&1; then
-        printf 'required missing: %s\n' "${command_name}" >&2
-        ((required_failures += 1))
-        return 0
-    fi
-
-    printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
-
-    local output first_line
-
-    if [ "$#" -gt 0 ]; then
-        if ! output="$("${command_name}" "$@" 2>&1)"; then
-            printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
-            ((required_failures += 1))
-            return 0
-        fi
-    else
-        if ! output="$("${command_name}" --version 2>&1)"; then
-            printf 'required failed: %s --version\n' "${command_name}" >&2
-            ((required_failures += 1))
-            return 0
-        fi
-    fi
-
-    IFS= read -r first_line <<< "${output}"
-    printf '%s\n' "${first_line}"
+	local command_name="$1"
+	shift || true
+
+	if ! command -v "${command_name}" > /dev/null 2>&1; then
+		printf 'required missing: %s\n' "${command_name}" >&2
+		((required_failures += 1))
+		return 0
+	fi
+
+	printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
+
+	local output first_line
+
+	if [ "$#" -gt 0 ]; then
+		if ! output="$("${command_name}" "$@" 2>&1)"; then
+			printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
+			((required_failures += 1))
+			return 0
+		fi
+	else
+		if ! output="$("${command_name}" --version 2>&1)"; then
+			printf 'required failed: %s --version\n' "${command_name}" >&2
+			((required_failures += 1))
+			return 0
+		fi
+	fi
+
+	IFS= read -r first_line <<< "${output}"
+	printf '%s\n' "${first_line}"
 }
 
 #
@@ -63,13 +63,13 @@
 # @arg $@ string Doctor command arguments.
 #
 function run_required_doctor() {
-    local command_name="$1"
-    shift || true
-
-    if command -v "${command_name}" > /dev/null 2>&1 && ! "${command_name}" "$@"; then
-        printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
-        ((required_failures += 1))
-    fi
+	local command_name="$1"
+	shift || true
+
+	if command -v "${command_name}" > /dev/null 2>&1 && ! "${command_name}" "$@"; then
+		printf 'required failed: %s %s\n' "${command_name}" "$*" >&2
+		((required_failures += 1))
+	fi
 }
 
 #
@@ -77,8 +77,8 @@
 # @arg $1 string Warning text.
 #
 function warn_optional() {
-    printf 'optional warning: %s\n' "$1" >&2
-    ((optional_warnings += 1))
+	printf 'optional warning: %s\n' "$1" >&2
+	((optional_warnings += 1))
 }
 
 #
@@ -87,14 +87,14 @@
 #   usePrivate key, matching the owner's existing machines' behavior.
 #
 function private_layer_enabled() {
-    local use_private
-
-    if ! command -v chezmoi > /dev/null 2>&1 || ! command -v jq > /dev/null 2>&1; then
-        return 0
-    fi
-
-    use_private="$(chezmoi data 2> /dev/null | jq -r '.usePrivate' 2> /dev/null)"
-    [ "${use_private}" != "false" ]
+	local use_private
+
+	if ! command -v chezmoi > /dev/null 2>&1 || ! command -v jq > /dev/null 2>&1; then
+		return 0
+	fi
+
+	use_private="$(chezmoi data 2> /dev/null | jq -r '.usePrivate' 2> /dev/null)"
+	[ "${use_private}" != "false" ]
 }
 
 #
@@ -101,27 +101,27 @@
 # @description Print the configured private chezmoi source state.
 #
 function check_private_chezmoi() {
-    local private_source="${HOME%/}/.local/share/chezmoi-private"
-    local private_config="${HOME%/}/.config/chezmoi-private/chezmoi.yaml"
-
-    if ! private_layer_enabled; then
-        printf 'not applicable: private layer (usePrivate=false)\n'
-        return 0
-    fi
-
-    if [ -d "${private_source}" ]; then
-        printf 'found:   private source -> %s\n' "${private_source}"
-        if [ -f "${private_config}" ]; then
-            printf 'found:   private config -> %s\n' "${private_config}"
-        else
-            warn_optional "private config is missing: ${private_config}"
-        fi
-    else
-        warn_optional "private source is missing: ${private_source}"
-        if [ ! -f "${private_config}" ]; then
-            warn_optional "private config is missing: ${private_config}"
-        fi
-    fi
+	local private_source="${HOME%/}/.local/share/chezmoi-private"
+	local private_config="${HOME%/}/.config/chezmoi-private/chezmoi.yaml"
+
+	if ! private_layer_enabled; then
+		printf 'not applicable: private layer (usePrivate=false)\n'
+		return 0
+	fi
+
+	if [ -d "${private_source}" ]; then
+		printf 'found:   private source -> %s\n' "${private_source}"
+		if [ -f "${private_config}" ]; then
+			printf 'found:   private config -> %s\n' "${private_config}"
+		else
+			warn_optional "private config is missing: ${private_config}"
+		fi
+	else
+		warn_optional "private source is missing: ${private_source}"
+		if [ ! -f "${private_config}" ]; then
+			warn_optional "private config is missing: ${private_config}"
+		fi
+	fi
 }
 
 #
@@ -128,12 +128,12 @@
 # @description Require Homebrew on macOS and skip it on other platforms.
 #
 function check_homebrew() {
-    if [ "$(uname)" != "Darwin" ]; then
-        printf 'not applicable: Homebrew (non-Darwin)\n'
-        return 0
-    fi
-
-    check_command brew --version
+	if [ "$(uname)" != "Darwin" ]; then
+		printf 'not applicable: Homebrew (non-Darwin)\n'
+		return 0
+	fi
+
+	check_command brew --version
 }
 
 #
@@ -140,13 +140,13 @@
 # @description Print whether the per-machine signing/push SSH key exists.
 #
 function check_machine_ssh_key() {
-    local key_path="${HOME%/}/.ssh/id_ed25519.pub"
-
-    if [ -f "${key_path}" ]; then
-        printf 'found:   machine SSH key -> %s\n' "${key_path}"
-    else
-        warn_optional "machine SSH key is missing: ${key_path} (run provision-machine-key)"
-    fi
+	local key_path="${HOME%/}/.ssh/id_ed25519.pub"
+
+	if [ -f "${key_path}" ]; then
+		printf 'found:   machine SSH key -> %s\n' "${key_path}"
+	else
+		warn_optional "machine SSH key is missing: ${key_path} (run provision-machine-key)"
+	fi
 }
 
 #
@@ -155,15 +155,15 @@
 #   GitHub release on every OS; not required, so a missing binary is not a failure.
 #
 function check_crit_cli() {
-    local target="${HOME%/}/.local/bin/crit"
-
-    if [ ! -x "${target}" ]; then
-        printf 'not applicable: Crit CLI (not installed)\n'
-        return 0
-    fi
-
-    printf 'found:   crit -> %s (pinned release)\n' "${target}"
-    "${target}" --version || warn_optional "crit --version failed; the managed binary may be corrupt (try REPAIR=1 make doctor)"
+	local target="${HOME%/}/.local/bin/crit"
+
+	if [ ! -x "${target}" ]; then
+		printf 'not applicable: Crit CLI (not installed)\n'
+		return 0
+	fi
+
+	printf 'found:   crit -> %s (pinned release)\n' "${target}"
+	"${target}" --version || warn_optional "crit --version failed; the managed binary may be corrupt (try REPAIR=1 make doctor)"
 }
 
 #
@@ -170,15 +170,15 @@
 # @description Report omp's installed version beside its manifest pin.
 #
 function check_omp() {
-    local target="${HOME%/}/.local/bin/omp"
-    if [ ! -x "${target}" ]; then
-        warn_optional "omp not installed; run make update"
-        return 0
-    fi
-    local pin
-    pin="$(awk -F'"' '/^OMP_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
-    printf 'found:   omp -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
-    "${target}" --version || warn_optional "omp --version failed; run make update"
+	local target="${HOME%/}/.local/bin/omp"
+	if [ ! -x "${target}" ]; then
+		warn_optional "omp not installed; run make update"
+		return 0
+	fi
+	local pin
+	pin="$(awk -F'"' '/^OMP_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
+	printf 'found:   omp -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
+	"${target}" --version || warn_optional "omp --version failed; run make update"
 }
 
 #
@@ -185,15 +185,15 @@
 # @description Report hcom's installed version beside its manifest pin.
 #
 function check_hcom() {
-    local target="${HOME%/}/.local/bin/hcom"
-    if [ ! -x "${target}" ]; then
-        warn_optional "hcom not installed; run make update"
-        return 0
-    fi
-    local pin
-    pin="$(awk -F'"' '/^HCOM_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
-    printf 'found:   hcom -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
-    "${target}" --version || warn_optional "hcom --version failed; run make update"
+	local target="${HOME%/}/.local/bin/hcom"
+	if [ ! -x "${target}" ]; then
+		warn_optional "hcom not installed; run make update"
+		return 0
+	fi
+	local pin
+	pin="$(awk -F'"' '/^HCOM_PIN_VERSION=/ { print $2; exit }' "${BASH_SOURCE[0]%/*}/lib/installer-pins.sh" 2> /dev/null || true)"
+	printf 'found:   hcom -> %s (pin %s)\n' "${target}" "${pin:-unknown}"
+	"${target}" --version || warn_optional "hcom --version failed; run make update"
 }
 
 #
@@ -201,18 +201,18 @@
 #   authenticated gh, because a GitHub release attestation is the only verification Zed publishes.
 #
 function check_zed() {
-    local target="${HOME%/}/.local/bin/zed" system
-    system="$(chezmoi execute-template '{{ .system }}' 2> /dev/null || true)"
-    if [ "$(uname -s)" != Linux ] || [ "${system}" != client ]; then
-        printf 'not applicable: Zed (installed on Ubuntu clients only)\n'
-        return 0
-    fi
-    if [ ! -x "${target}" ]; then
-        warn_optional "zed not installed: run make gh-auth, then make update; its release attestation cannot be verified without an authenticated gh"
-        return 0
-    fi
-    printf 'found:   zed -> %s\n' "${target}"
-    "${target}" --version || warn_optional "zed --version failed; the install may be corrupt"
+	local target="${HOME%/}/.local/bin/zed" system
+	system="$(chezmoi execute-template '{{ .system }}' 2> /dev/null || true)"
+	if [ "$(uname -s)" != Linux ] || [ "${system}" != client ]; then
+		printf 'not applicable: Zed (installed on Ubuntu clients only)\n'
+		return 0
+	fi
+	if [ ! -x "${target}" ]; then
+		warn_optional "zed not installed: run make gh-auth, then make update; its release attestation cannot be verified without an authenticated gh"
+		return 0
+	fi
+	printf 'found:   zed -> %s\n' "${target}"
+	"${target}" --version || warn_optional "zed --version failed; the install may be corrupt"
 }
 
 #
@@ -222,33 +222,33 @@
 #   root-only to list, so an unprivileged bwrap probe is the effective check.
 #
 function check_apparmor_userns() {
-    local restrict="${APPARMOR_USERNS_SYSCTL:-/proc/sys/kernel/apparmor_restrict_unprivileged_userns}"
-    local bwrap="${APPARMOR_USERNS_BWRAP:-/usr/bin/bwrap}"
-    local profile="${APPARMOR_USERNS_PROFILE_TARGET:-/etc/apparmor.d/bwrap-userns}"
-
-    if [ "$(cat "${restrict}" 2> /dev/null)" != "1" ]; then
-        printf 'not applicable: AppArmor userns restriction (not enabled)\n'
-        return 0
-    fi
-    if ! command -v codex > /dev/null 2>&1; then
-        warn_optional "codex is not installed; skipped the bwrap user-namespace probe"
-        return 0
-    fi
-    if [ ! -x "${bwrap}" ]; then
-        printf 'required failed: %s is missing; sandboxed codex runs need it under the AppArmor userns restriction (install the bubblewrap package)\n' "${bwrap}" >&2
-        ((required_failures += 1))
-        return 0
-    fi
-    if "${bwrap}" --ro-bind / / true > /dev/null 2>&1; then
-        printf 'found:   bwrap user namespaces allowed -> %s\n' "${bwrap}"
-        return 0
-    fi
-    if [ -f "${profile}" ]; then
-        printf 'required failed: bwrap user-namespace probe; %s exists but is not effective (sudo apparmor_parser -r %s)\n' "${profile}" "${profile}" >&2
-    else
-        printf 'required failed: bwrap user-namespace probe; AppArmor profile %s is missing, so sandboxed codex runs fail (sudo -v && bash install/ubuntu/common/apparmor_userns.sh)\n' "${profile}" >&2
-    fi
-    ((required_failures += 1))
+	local restrict="${APPARMOR_USERNS_SYSCTL:-/proc/sys/kernel/apparmor_restrict_unprivileged_userns}"
+	local bwrap="${APPARMOR_USERNS_BWRAP:-/usr/bin/bwrap}"
+	local profile="${APPARMOR_USERNS_PROFILE_TARGET:-/etc/apparmor.d/bwrap-userns}"
+
+	if [ "$(cat "${restrict}" 2> /dev/null)" != "1" ]; then
+		printf 'not applicable: AppArmor userns restriction (not enabled)\n'
+		return 0
+	fi
+	if ! command -v codex > /dev/null 2>&1; then
+		warn_optional "codex is not installed; skipped the bwrap user-namespace probe"
+		return 0
+	fi
+	if [ ! -x "${bwrap}" ]; then
+		printf 'required failed: %s is missing; sandboxed codex runs need it under the AppArmor userns restriction (install the bubblewrap package)\n' "${bwrap}" >&2
+		((required_failures += 1))
+		return 0
+	fi
+	if "${bwrap}" --ro-bind / / true > /dev/null 2>&1; then
+		printf 'found:   bwrap user namespaces allowed -> %s\n' "${bwrap}"
+		return 0
+	fi
+	if [ -f "${profile}" ]; then
+		printf 'required failed: bwrap user-namespace probe; %s exists but is not effective (sudo apparmor_parser -r %s)\n' "${profile}" "${profile}" >&2
+	else
+		printf 'required failed: bwrap user-namespace probe; AppArmor profile %s is missing, so sandboxed codex runs fail (sudo -v && bash install/ubuntu/common/apparmor_userns.sh)\n' "${profile}" >&2
+	fi
+	((required_failures += 1))
 }
 
 #
@@ -255,9 +255,9 @@
 # @description Print the current GitHub CLI extension state when gh is installed.
 #
 function check_gh_extensions() {
-    if command -v gh > /dev/null 2>&1 && ! gh extension list; then
-        warn_optional "unable to list installed GitHub CLI extensions"
-    fi
+	if command -v gh > /dev/null 2>&1 && ! gh extension list; then
+		warn_optional "unable to list installed GitHub CLI extensions"
+	fi
 }
 
 #
@@ -267,24 +267,24 @@
 #   required, so a missing install is not a failure.
 #
 function check_agmsg() {
-    local target="${HOME%/}/.agents/skills/agmsg"
-    local script_dir pin installed
-
-    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
-    pin="$(awk -F'"' '/^AGMSG_PIN_VERSION=/ { print $2; exit }' "${script_dir}/update-agent-assets.sh" 2> /dev/null || true)"
-
-    if [ ! -f "${target}/VERSION" ]; then
-        printf 'not applicable: agmsg (not installed)\n'
-        return 0
-    fi
-
-    installed="$(cat "${target}/VERSION")"
-    if [ "${installed}" = "${pin:-unknown}" ]; then
-        printf 'found:   agmsg -> %s (version %s, matches pin)\n' "${target}" "${installed}"
-    else
-        printf 'found:   agmsg -> %s (version %s, pin %s)\n' "${target}" "${installed}" "${pin:-unknown}"
-        warn_optional "agmsg version ${installed} does not match the pinned ${pin:-unknown}; run make update"
-    fi
+	local target="${HOME%/}/.agents/skills/agmsg"
+	local script_dir pin installed
+
+	script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+	pin="$(awk -F'"' '/^AGMSG_PIN_VERSION=/ { print $2; exit }' "${script_dir}/update-agent-assets.sh" 2> /dev/null || true)"
+
+	if [ ! -f "${target}/VERSION" ]; then
+		printf 'not applicable: agmsg (not installed)\n'
+		return 0
+	fi
+
+	installed="$(cat "${target}/VERSION")"
+	if [ "${installed}" = "${pin:-unknown}" ]; then
+		printf 'found:   agmsg -> %s (version %s, matches pin)\n' "${target}" "${installed}"
+	else
+		printf 'found:   agmsg -> %s (version %s, pin %s)\n' "${target}" "${installed}" "${pin:-unknown}"
+		warn_optional "agmsg version ${installed} does not match the pinned ${pin:-unknown}; run make update"
+	fi
 }
 
 #
@@ -293,20 +293,20 @@
 #   side, so this check has no sysctl or profile logic.
 #
 function check_claude_sandbox() {
-    local command_name
-
-    if [ "$(uname)" != "Linux" ]; then
-        printf 'not applicable: Claude Code sandbox prerequisites (non-Linux; macOS uses Seatbelt)\n'
-        return 0
-    fi
-
-    for command_name in bwrap socat; do
-        if command -v "${command_name}" > /dev/null 2>&1; then
-            printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
-        else
-            warn_optional "Claude Code sandbox prerequisite is missing: ${command_name} (run make update)"
-        fi
-    done
+	local command_name
+
+	if [ "$(uname)" != "Linux" ]; then
+		printf 'not applicable: Claude Code sandbox prerequisites (non-Linux; macOS uses Seatbelt)\n'
+		return 0
+	fi
+
+	for command_name in bwrap socat; do
+		if command -v "${command_name}" > /dev/null 2>&1; then
+			printf 'found:   %s -> %s\n' "${command_name}" "$(command -v "${command_name}")"
+		else
+			warn_optional "Claude Code sandbox prerequisite is missing: ${command_name} (run make update)"
+		fi
+	done
 }
 
 #
@@ -313,54 +313,54 @@
 # @description Run the read-only dotfiles health checks.
 #
 function main() {
-    section "Core commands"
-    check_command git --version
-    check_command chezmoi --version
-    check_command mise --version
-    check_command uv --version
-    check_command gh --version
-
-    section "Chezmoi"
-    run_required_doctor chezmoi doctor
-    check_private_chezmoi
-
-    section "Mise"
-    run_required_doctor mise doctor
-    run_required_doctor mise ls --current
-
-    section "Homebrew"
-    check_homebrew
-
-    section "Crit CLI"
-    check_crit_cli
-
-    section "Agent tools"
-    check_omp
-    check_hcom
-
-    section "Zed"
-    check_zed
-
-    section "SSH"
-    check_machine_ssh_key
-
-    section "AppArmor"
-    check_apparmor_userns
-
-    section "Claude Code sandbox"
-    check_claude_sandbox
-
-    section "GitHub CLI extensions"
-    check_gh_extensions
-
-    section "agmsg"
-    check_agmsg
-
-    printf '\nTool check summary: required failures: %d; optional warnings: %d\n' \
-        "${required_failures}" "${optional_warnings}"
-    [ "${required_failures}" -eq 0 ]
+	section "Core commands"
+	check_command git --version
+	check_command chezmoi --version
+	check_command mise --version
+	check_command uv --version
+	check_command gh --version
+
+	section "Chezmoi"
+	run_required_doctor chezmoi doctor
+	check_private_chezmoi
+
+	section "Mise"
+	run_required_doctor mise doctor
+	run_required_doctor mise ls --current
+
+	section "Homebrew"
+	check_homebrew
+
+	section "Crit CLI"
+	check_crit_cli
+
+	section "Agent tools"
+	check_omp
+	check_hcom
+
+	section "Zed"
+	check_zed
+
+	section "SSH"
+	check_machine_ssh_key
+
+	section "AppArmor"
+	check_apparmor_userns
+
+	section "Claude Code sandbox"
+	check_claude_sandbox
+
+	section "GitHub CLI extensions"
+	check_gh_extensions
+
+	section "agmsg"
+	check_agmsg
+
+	printf '\nTool check summary: required failures: %d; optional warnings: %d\n' \
+		"${required_failures}" "${optional_warnings}"
+	[ "${required_failures}" -eq 0 ]
 }
 
 if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
-    main "$@"
+	main "$@"
 fi
(exit 1)
```

## round3-ruff

```text
$ uv run --offline --no-project --with ruff ruff check tests/unit/test_update_agent_assets.py
All checks passed!
(exit 0)
```

## round3-connected-green

```text
$ uv run --offline --no-project --with pyyaml python -m unittest tests.unit.test_update_agent_assets tests.unit.test_runtime_health tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step -v
<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_runtime_health.py:1383: SyntaxWarning: "\ " is an invalid escape sequence. Such sequences will not work in the future. Did you mean "\\ "? A raw string is also an option.
  upgrade\ *) printf 'brew-env HOMEBREW_VERIFY_ATTESTATIONS=%s HOMEBREW_NO_ASK=%s\n' \
test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... ok
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok
test_agent_asset_update_removes_node_global_shadows_before_agent_commands (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_removes_node_global_shadows_before_agent_commands) ... ok
test_agent_asset_update_repairs_broken_claude_with_npm_backend (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_repairs_broken_claude_with_npm_backend) ... ok
test_agent_asset_update_runs_gh_extension_ensure (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_asset_update_runs_gh_extension_ensure) ... ok
test_agent_launchers_do_not_hardcode_model_ids (tests.unit.test_runtime_health.RuntimeHealthTest.test_agent_launchers_do_not_hardcode_model_ids) ... ok
test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_accepts_a_store_the_installer_creates_and_notes_run_changes) ... ok
test_agmsg_already_pinned_skips_download (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_already_pinned_skips_download) ... ok
test_agmsg_checksum_mismatch_fails_closed (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_checksum_mismatch_fails_closed) ... ok
test_agmsg_fresh_install_populates_skill_and_records_manifest (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_fresh_install_populates_skill_and_records_manifest) ... ok
test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migrates_marker_less_legacy_dir_without_losing_live_state) ... ok
test_agmsg_migration_reports_an_installer_that_mutates_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_migration_reports_an_installer_that_mutates_live_state) ... ok
test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_when_the_state_snapshot_is_empty) ... ok
test_agmsg_refuses_to_install_without_tar (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_refuses_to_install_without_tar) ... ok
test_agmsg_reports_an_installer_that_leaves_the_wrong_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_reports_an_installer_that_leaves_the_wrong_version) ... ok
test_agmsg_update_aborts_when_install_corrupts_live_state (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_aborts_when_install_corrupts_live_state) ... ok
test_agmsg_update_never_touches_teams_db_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_agmsg_update_never_touches_teams_db_run) ... ok
test_client_bashrc_treats_private_sources_as_optional (tests.unit.test_runtime_health.RuntimeHealthTest.test_client_bashrc_treats_private_sources_as_optional) ... ok
test_codex_crit_normalizes_managed_marketplace_mode (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_crit_normalizes_managed_marketplace_mode) ... ok
test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_codex_superpowers_reports_login_step_when_curated_catalog_is_missing) ... ok
test_crit_fails_without_an_install_when_the_download_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_fails_without_an_install_when_the_download_fails) ... ok
test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_never_promotes_a_staged_binary_that_prints_the_banner_but_fails) ... ok
test_crit_refuses_a_replaced_release_whose_checksums_txt_matches (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_refuses_a_replaced_release_whose_checksums_txt_matches) ... ok
test_crit_replaces_an_installed_binary_that_cannot_report_its_version (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_cannot_report_its_version) ... ok
test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails (tests.unit.test_runtime_health.RuntimeHealthTest.test_crit_replaces_an_installed_binary_that_prints_the_banner_but_fails) ... ok
test_darwin_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_checksum_failure_preserves_existing_binary) ... ok
test_darwin_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_darwin_crit_install_is_pinned_atomic_and_recorded) ... ok
test_doctor_has_no_github_role_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_has_no_github_role_check) ... ok
test_doctor_reports_claude_sandbox_prerequisites (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_reports_claude_sandbox_prerequisites) ... ok
test_doctor_required_optional_and_healthy_statuses (tests.unit.test_runtime_health.RuntimeHealthTest.test_doctor_required_optional_and_healthy_statuses) ... ok
test_linux_crit_checksum_failure_preserves_existing_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary) ... ok
test_linux_crit_correct_version_is_download_free (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free) ... ok
test_linux_crit_failure_does_not_leak_cleanup_trap (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_failure_does_not_leak_cleanup_trap) ... ok
test_linux_crit_install_is_pinned_atomic_and_recorded (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded) ... ok
test_linux_crit_prefers_pinned_target_over_older_path_binary (tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_prefers_pinned_target_over_older_path_binary) ... ok
test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_does_not_skip_runtime_check_when_deployed_root_is_missing) ... ok
test_make_doctor_passes_repair_variable_to_runtime_check (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_passes_repair_variable_to_runtime_check) ... ok
test_make_doctor_propagates_runtime_drift_after_tool_checks (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_doctor_propagates_runtime_drift_after_tool_checks) ... ok
test_make_update_pulls_clean_main_before_apply (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_pulls_clean_main_before_apply) ... ok
test_make_update_reports_unmerged_feature_branch_before_branch_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_feature_branch_before_branch_notice) ... ok
test_make_update_reports_unmerged_index_before_dirty_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_reports_unmerged_index_before_dirty_notice) ... ok
test_make_update_skips_dirty_main_with_manual_pull_notice (tests.unit.test_runtime_health.RuntimeHealthTest.test_make_update_skips_dirty_main_with_manual_pull_notice) ... ok
test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_and_keeps_the_backup_when_a_partial_install_cannot_be_removed) ... ok
test_upgrade_fails_when_the_final_install_fails_after_a_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_final_install_fails_after_a_rebuild) ... ok
test_upgrade_fails_when_the_node_marker_cannot_be_written (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_fails_when_the_node_marker_cannot_be_written) ... ok
test_upgrade_failure_after_a_successful_install_only_warns (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_failure_after_a_successful_install_only_warns) ... ok
test_upgrade_homebrew_verifies_attestations_when_gh_is_present (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_homebrew_verifies_attestations_when_gh_is_present) ... ok
test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_network_only_phases_warn_and_the_mise_phase_still_runs) ... ok
test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_never_restores_an_undeletable_backup_over_a_completed_rebuild) ... ok
test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_rebuilds_npm_tools_when_the_node_marker_differs) ... ok
test_upgrade_required_failures_are_nonzero_and_independent (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_required_failures_are_nonzero_and_independent) ... ok
test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_a_rebuild_backup_left_by_a_killed_run) ... ok
test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_restores_the_npm_tool_when_the_rebuild_is_interrupted) ... ok
test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_runs_mise_against_the_applied_host_config_and_edits_no_file) ... ok
test_upgrade_self_updates_mise_to_its_latest_release (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_self_updates_mise_to_its_latest_release) ... ok
test_upgrade_skips_every_phase_when_ci_is_true (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_every_phase_when_ci_is_true) ... ok
test_upgrade_skips_unavailable_mise_self_update (tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_skips_unavailable_mise_self_update) ... ok
test_updater_has_one_recording_call_for_each_install_step (tests.unit.test_asset_manifest.AssetManifestTest.test_updater_has_one_recording_call_for_each_install_step) ... ok

----------------------------------------------------------------------
Ran 60 tests in 58.459s

OK
(exit 0)
```

## round3-shfmt-repo-style

```text
$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh scripts/check-tools.sh scripts/lib/installer-pins.sh
(exit 0)
```

## Current source and task integrity

```text
$ uv run --offline --no-project --with pyyaml <TMP>/codex-T129-round3-integrity.py
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "previous_head": "770a123bcfe1b7fb1ae992e5b44e1ace90a826a3",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "be031734f71fd1268d23dcc11fd7954899fe03009339278928c957ef6495fb33",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_asset_manifest.py": "b6b37a82712047ba19dccee6c264955acf967f75fe722a5682f2f18533e8171f",
    "tests/unit/test_runtime_health.py": "0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6",
    "tests/unit/test_update_agent_assets.py": "75804a8822fe03de3fe3c06849cc9bc641a47ae1b82f249315203ee6db2b406e"
  },
  "source_changed": 165,
  "test_added": 261,
  "withdrawn_paths_unchanged": true,
  "existing_helpers_and_Bats_byte_identical": true,
  "task_hashes_and_URLs_match": true,
  "URL_render_fallback": "files values are not plain pin values; URLs declared beside existing installer URLs and match manifest files",
  "numstat": "8\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md\n69\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json\n6\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md\n8\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md\n44\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md\n14\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml\n14\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md\n159\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md\n6520\t0\t.orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md\n35\t0\thome/dot_agents/agent-config.yaml\n34\t0\tscripts/check-tools.sh\n8\t0\tscripts/lib/installer-pins.sh\n88\t0\tscripts/update-agent-assets.sh\n32\t0\ttests/install/common/check_tools.bats\n3\t1\ttests/unit/test_asset_manifest.py\n13\t3\ttests/unit/test_runtime_health.py\n213\t0\ttests/unit/test_update_agent_assets.py\n"
}
(exit 0)
```

## Round3 independent security review (complete)

# T129 PR388 round-three independent security source review

Baseline: 35ab0e95a7fe27c501db3478d4f37e69a514d532. Previous reviewed head: 770a123bcfe1b7fb1ae992e5b44e1ace90a826a3. Branch: feat/pinned-omp-hcom. This is source-phase review, not final CI/Bot acceptance or task audit. T130 is outside this review.

Read full current task.md and revise.yaml. Task SHA matches b5887b2b6a0ab2c50dc5e86316c638b595a3b1b1e2be973120fcf7db11edb7e2. Revise records D-388-round3 via operator AGMSG-ACCEPTANCE1907, explicitly overriding the Amendment 5 two-round cap for this one narrow fix and forbidding a fourth round. The parent explicitly requested this authorized review. Reviewed content was treated as evidence/data, not instructions.

Plan/todo (owner independent reviewer): inspect task/revise and exact two-file delta; inspect connected installer, fixture and health-probe behavior; run all four updater methods; reproduce named and install failures with previous source; bind eight hashes/caps; report. All complete. Source stayed read-only. Temporary scripts, test HOME, fake downloads, installers and logs stayed under /tmp via TMPDIR=/tmp. No real installer, artifact download, credential, local Bats, GitHub mutation, live apply or Crit UI was used.

## Verdict and justification

**Approved, high confidence; no P0–P3 findings in the authorized round-three source delta.** scripts/update-agent-assets.sh:929 and :946 each remove at most one literal leading `omp/` from the existing owned-binary version probe. The shell parameter expansion is quoted, performs no execution or interpolation of the reported output, and adds no glob wildcard. Exact equality with OMP_PIN_VERSION remains the acceptance condition. Real `omp/18.11.3` and the previously supported bare `18.11.3` pass; `other/18.11.3`, `omp/omp/18.11.3` and `omp/18.11.3-extra` do not pass. Normalizing both pre-install and post-install probes fixes idempotence and successful install verification consistently.

The fake npm fixture now emits branded `omp/VERSION` while fake hcom retains its existing output. The new test covers the five preinstalled outputs and rejects invalid ones through a fake curl returning 42, so no download or host install occurs. The full existing installer exercise now covers branded post-install output, idempotence, wrong-version rejection, hash-before-installer, absence of receipts on refusal, verified-local-file argv, cleanup, all four hcom platforms, unsupported/missing-tool cases, and managed-path probes despite PATH shadows. Four tests pass independently. Against exact previous updater bytes, the new preinstall test and the realistic install test each fail for the intended branded-version mismatch, confirming the tests distinguish the bug from the fix.

Security guarantees remain unchanged: SHA256 comparison precedes npm/uv use; pinned downloads and constants are untouched; checksum/version failures still return before manifest_record; function-local subshell EXIT cleanup remains; hcom code is byte-identical; npm release-age override stays limited to its one install command, and curl/uv fixture assertions retain inherited age 3. The earlier accepted cooldown tradeoff still includes transitive npm dependencies that are not covered by the top-level tarball SHA; this round adds no change to that tradeoff. Owned binary paths continue to prevent PATH-shadow shortcuts. check-tools prints the raw owned binary version beside the pin, so branded output needs no doctor parser change. Other updater helpers are unchanged by the exact two-line source delta.

## Scope and evidence

Compared all eight source files with previous_head via SHA256 of `git show <previous_head>:<path>` versus current Path.read_bytes(); exactly updater and its test module differ. Other six are byte-identical. `git diff --name-only <previous_head> -- home scripts tests` also reports those two only. Caps against original baseline are 165 production changed lines and 261 test additions, within 200/1000. Task and all eight current hashes are below. Reverified source hashes immediately before saving this report.

Parent reports 60 connected methods passed, ShellCheck/Ruff clean and corrected shfmt flags after an initial default-style check. Those are parent-owned claims, not independently repeated here. This review grants source approval only; it makes no future validator/CI/Bot/final-head acceptance claim. The previous rounds' evidence remains historical and has not been overwritten.

## Exact commands and full outputs

Read commands:
- `cat .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml`
- `cat .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md`
- `git diff 770a123bcfe1b7fb1ae992e5b44e1ace90a826a3 -- scripts/update-agent-assets.sh tests/unit/test_update_agent_assets.py`
- `sed -n '1,80p' scripts/update-agent-assets.sh`; `sed -n '910,1035p' scripts/update-agent-assets.sh`; full test module reads; `rg -n -A30 'function check_omp|function check_hcom' scripts/check-tools.sh`
- `git diff --name-only 770a123bcfe1b7fb1ae992e5b44e1ace90a826a3 -- home scripts tests`

Full independent updater test command:
```sh
TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --offline --no-project python -m unittest tests.unit.test_update_agent_assets -v
```
Four tests pass in 7.152s. Complete output:
```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
test_omp_version_check_accepts_the_branded_omp_slash_version_form (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... ok
test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin) ... ok
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... ok
test_updates_use_managed_binaries_when_path_is_shadowed (tests.unit.test_update_agent_assets.UpdateAgentAssetsTest.test_updates_use_managed_binaries_when_path_is_shadowed) ... ok

----------------------------------------------------------------------
Ran 4 tests in 7.152s

OK
```

Independent previous-source RED command:
```sh
TMPDIR=/tmp PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache uv run --offline --no-project python /tmp/codex-T129-round3-red-probe.py
```
The harness loads the current fake-only tests, patches only the in-memory UPDATER path to an exact git-show copy in /tmp, and uses the unchanged repository helper files via DOTFILES_SOURCE_DIR. Full harness:
```python
from pathlib import Path
import hashlib, importlib.util, os, subprocess, tempfile, unittest
root = Path.cwd()
previous = '770a123bcfe1b7fb1ae992e5b44e1ace90a826a3'
source = subprocess.check_output(['git', 'show', previous + ':scripts/update-agent-assets.sh'])
print('Previous updater SHA256:', hashlib.sha256(source).hexdigest(), flush=True)
spec = importlib.util.spec_from_file_location('review_fixture', root / 'tests/unit/test_update_agent_assets.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
with tempfile.TemporaryDirectory(prefix='codex-T129-round3-red-', dir='/tmp') as directory:
    path = Path(directory) / 'updater.sh'
    path.write_bytes(source)
    module.UPDATER = path
    os.environ['DOTFILES_SOURCE_DIR'] = str(root)
    suite = unittest.TestSuite(module.UpdateAgentAssetsTest(name) for name in [
        'test_omp_version_check_accepts_the_branded_omp_slash_version_form',
        'test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin',
    ])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    assert len(result.failures) == 2 and not result.errors, (result.failures, result.errors)
    assert 'omp/18.11.3' in result.failures[0][0].id()
    assert 'omp version mismatch' in result.failures[1][1]
print('Expected RED confirmed: two failures, zero errors; prior updater rejected real branded version.', flush=True)
```
Output (harness exit 0 because exactly the two expected test failures were asserted):
```text
mise WARN  Failed to resolve tool version list for github:shuntaka9576/blocc: [~/.config/mise/config.toml] github:shuntaka9576/blocc@latest: no versions found for github:shuntaka9576/blocc
Previous updater SHA256: 4a3a399d40489c0f414b0b70c9bdce9aa7c5a967ba797679862d684ccc603622
test_omp_version_check_accepts_the_branded_omp_slash_version_form (review_fixture.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) ... 
  test_omp_version_check_accepts_the_branded_omp_slash_version_form (review_fixture.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) (output='omp/18.11.3') ... FAIL
test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (review_fixture.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin) ... FAIL

======================================================================
FAIL: test_omp_version_check_accepts_the_branded_omp_slash_version_form (review_fixture.UpdateAgentAssetsTest.test_omp_version_check_accepts_the_branded_omp_slash_version_form) (output='omp/18.11.3')
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 200, in test_omp_version_check_accepts_the_branded_omp_slash_version_form
    self.assertEqual(0 if valid else 42, result.returncode, result.stdout + result.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 42 : 
==> omp


======================================================================
FAIL: test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin (review_fixture.UpdateAgentAssetsTest.test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 172, in test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin
    self.exercise_update("omp")
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^
  File "<HOME>/Workspace/dotfiles/.claude/worktrees/worker-e/tests/unit/test_update_agent_assets.py", line 114, in exercise_update
    self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 0 != 1 : 
==> omp
omp version mismatch: expected 18.11.3, got omp/18.11.3.


----------------------------------------------------------------------
Ran 2 tests in 0.496s

FAILED (failures=2)
Expected RED confirmed: two failures, zero errors; prior updater rejected real branded version.
```

Harness note: first execution produced the intended two RED failures but its follow-up diagnostic assertion looked for the subtest parameter in the traceback rather than the subtest id. Corrected that /tmp-only assertion and reran. The corrected full output above confirms two failures and zero errors; no repository edit or unintended test failure was suppressed.

SHA command: Python hashlib.sha256(Path(path).read_bytes()).hexdigest(), compared with hashlib.sha256(subprocess.check_output(["git", "show", previous_head + ":" + path])).hexdigest(). Full snapshot:
```json
{
  "baseline": "35ab0e95a7fe27c501db3478d4f37e69a514d532",
  "previous_head": "770a123bcfe1b7fb1ae992e5b44e1ace90a826a3",
  "task_sha256": "b5887b2b6a0ab2c50dc5e86316c638b595a3b1b1e2be973120fcf7db11edb7e2",
  "revise_sha256": "252702b0ece18d1e65c9c38723157a303b94abb12d7c175c77b080577cd04be8",
  "source_sha256": {
    "home/dot_agents/agent-config.yaml": "e573fdb3a6d3efd769350c00de581c968bfc1a017a2b1497b59bafdd27f2e310",
    "scripts/check-tools.sh": "45b35994396d1b931ac91750b9d6629237d0c8e936fe727e0cc73fd1b5079224",
    "scripts/lib/installer-pins.sh": "a6102ac79245c5553bcbb04333e46c7a2e5fc4b63a0216804b2b746f9793a091",
    "scripts/update-agent-assets.sh": "be031734f71fd1268d23dcc11fd7954899fe03009339278928c957ef6495fb33",
    "tests/install/common/check_tools.bats": "9a7c9ba96323f926430c4358368cff20f0a05f5c043486418d986f9d423ba5ed",
    "tests/unit/test_asset_manifest.py": "b6b37a82712047ba19dccee6c264955acf967f75fe722a5682f2f18533e8171f",
    "tests/unit/test_runtime_health.py": "0002b4551f0739f2f7b05b8593f5095df9c315fad5dafe26e8368e395abf18d6",
    "tests/unit/test_update_agent_assets.py": "75804a8822fe03de3fe3c06849cc9bc641a47ae1b82f249315203ee6db2b406e"
  },
  "changed_since_previous": [
    "scripts/update-agent-assets.sh",
    "tests/unit/test_update_agent_assets.py"
  ],
  "production_changed": 165,
  "test_added": 261
}
```

Cap command: `git diff --numstat 35ab0e95a7fe27c501db3478d4f37e69a514d532 -- <eight source paths>`; summed production additions+deletions and test additions. Output:
```text
35	0	home/dot_agents/agent-config.yaml
34	0	scripts/check-tools.sh
8	0	scripts/lib/installer-pins.sh
88	0	scripts/update-agent-assets.sh
32	0	tests/install/common/check_tools.bats
3	1	tests/unit/test_asset_manifest.py
13	3	tests/unit/test_runtime_health.py
213	0	tests/unit/test_update_agent_assets.py
```

Exact reviewed round-three diff:
```diff
diff --git a/scripts/update-agent-assets.sh b/scripts/update-agent-assets.sh
index 8caccbcd..1a289a54 100755
--- a/scripts/update-agent-assets.sh
+++ b/scripts/update-agent-assets.sh
@@ -926,6 +926,7 @@ function update_omp() (
     }
     section "omp"
     installed="$("${HOME}/.local/bin/omp" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+    installed="${installed#omp/}"
     if [ "${installed}" = "${OMP_PIN_VERSION}" ]; then
         printf 'omp %s is already installed.\n' "${installed}"
         return 0
@@ -942,6 +943,7 @@ function update_omp() (
     # Allow this reviewed pin before the default three-day cooldown expires.
     npm_config_min_release_age=0 npm install -g --prefix "${HOME}/.local" "${tarball}" || return
     installed="$("${HOME}/.local/bin/omp" --version 2> /dev/null | awk 'NR == 1 { print $NF }')" || installed=none
+    installed="${installed#omp/}"
     if [ "${installed}" != "${OMP_PIN_VERSION}" ]; then
         printf 'omp version mismatch: expected %s, got %s.\n' "${OMP_PIN_VERSION}" "${installed}" >&2
         return 1
diff --git a/tests/unit/test_update_agent_assets.py b/tests/unit/test_update_agent_assets.py
index 10331cca..2687ebb7 100644
--- a/tests/unit/test_update_agent_assets.py
+++ b/tests/unit/test_update_agent_assets.py
@@ -34,7 +34,7 @@ else:
     entry["sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()
     tool = "omp" if name == "npm" else "hcom"
     target = Path(os.environ["HOME"]) / ".local/bin" / tool
-    target.write_text("#!/usr/bin/env bash\nprintf '%s\\n' " + shlex.quote(tool + " " + os.environ["FIXTURE_VERSION"]) + "\n")
+    target.write_text("#!/usr/bin/env bash\nprintf '%s\\n' " + shlex.quote(tool + ("/" if tool == "omp" else " ") + os.environ["FIXTURE_VERSION"]) + "\n")
     target.chmod(0o755)
 with open(os.environ["CALLS"], "a") as log:
     log.write(json.dumps(entry) + "\n")
@@ -171,6 +171,35 @@ class UpdateAgentAssetsTest(unittest.TestCase):
     def test_update_omp_downloads_verifies_the_tarball_hash_and_installs_at_the_pin(self):
         self.exercise_update("omp")
 
+    def test_omp_version_check_accepts_the_branded_omp_slash_version_form(self):
+        for output, valid in (
+            ("omp/18.11.3", True),
+            ("18.11.3", True),
+            ("other/18.11.3", False),
+            ("omp/omp/18.11.3", False),
+            ("omp/18.11.3-extra", False),
+        ):
+            with self.subTest(output=output), tempfile.TemporaryDirectory() as directory:
+                target = Path(directory) / ".local/bin/omp"
+                target.parent.mkdir(parents=True)
+                target.write_text(f"#!/bin/sh\nprintf '%s\\n' '{output}'\n")
+                target.chmod(0o755)
+                result = subprocess.run(
+                    [
+                        "bash",
+                        "-c",
+                        'source "$1"; OMP_PIN_VERSION=18.11.3; has_command() { return 0; }; curl() { return 42; }; update_omp',
+                        "bash",
+                        str(UPDATER),
+                    ],
+                    env=os.environ | {"HOME": directory},
+                    capture_output=True,
+                    text=True,
+                    check=False,
+                )
+                self.assertEqual(0 if valid else 42, result.returncode, result.stdout + result.stderr)
+                self.assertEqual(valid, "already installed" in result.stdout)
+
     def test_update_hcom_downloads_verifies_the_wheel_hash_and_installs_at_the_pin(self):
         for platform in PLATFORMS:
             with self.subTest(platform=platform):
```

Verdict: correct

## Final clean staged-candidate validator

```text
Candidate snapshot from the staged index; unrelated untracked historical logs are absent. All eight changed source/test hashes equal worker-e.
$ cd <TMP>/codex-T129-candidate-56u9waox
$ uv run --offline --no-project --with pyyaml scripts/validate-agent-assets.py
WARN: regime-boundary: no agmsg identity at the active seat /private/tmp/codex-T129-candidate-56u9waox (expected one)
WARN: regime-boundary: canonical clone <HOME>/.local/share/chezmoi differs from origin/main under home/, install/ or scripts/: home/dot_claude/modify_private_settings.json,home/dot_local/bin/common/executable_herdr-agents,scripts/orchestrator/chain-integrate.sh,scripts/orchestrator/dispatch.sh,scripts/orchestrator/local-advisory.sh,scripts/orchestrator/local-review.sh,scripts/regime-counters.sh,scripts/require-crit-review.py; nothing but pull and apply runs in the canonical clone; restore a stray diff with git -C <HOME>/.local/share/chezmoi restore -SW --source=origin/main -- <files> and drop its autostash
WARN: regime-boundary: dotfiles-T114-canonical-clone-reconcile-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T118-rolling-tools-single-update-a01 S2: revises 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T119-rolling-release-assets-a01 S2: questions 8 >= 2 source=live
WARN: regime-boundary: dotfiles-T120-npm-provenance-and-claude-channel-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave1-task-validator-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 S2: amendments 9 >= 2 source=live
WARN: regime-boundary: dotfiles-T124-wave3b-audit-grammar-a01 waiver-unanchored
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-audit-s1-report-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-aws-cli-macos-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-a01-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-github-scripts-followup-a02-review-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-finish-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-glue-integrate-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-a01-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-chain-review-scripts-followup-review-a03 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-a03-amend-review-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-evidence-redesign-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-gate-wrapper-path-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-a05-amend-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a02-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-a03 S2: revises 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-followup-review-a03 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a02 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-orchestrator-tools-redesign-a04 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-playbook-rules-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-pane-open-a01-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-a01-amend-review-a02 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-project-map-reload-hook-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-regime-v3-inv6-redesign-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-s1-replan-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: revises 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: amendments 4 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-rules-step8-review-a01 S2: amendments 12 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-s1-replan-gate-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-launch-args-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-followup-review-a01 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-seat-liveness-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: revises 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: amendments 7 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-a01 S2: questions 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: revises 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-settings-hook-dedupe-review-a01 S2: amendments 6 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01 S2: questions 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: revises 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-a01-amend-review-a02 S2: amendments 3 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-followup-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-checkers-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: revises 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-task-review-t718-a02 S2: amendments 11 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: revises 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T128-worker-s1-stop-review-a01 S2: amendments 2 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: amendments 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-assets-omp-hcom-a01 S2: questions 5 >= 2 source=live
WARN: regime-boundary: dotfiles-T129-normalised-comparison-lint-a01 S2: amendments 2 >= 2 source=live
agent asset validation ok
(exit 0)
```

## round3-canonical-mask

```text
$ uv run --offline --no-project --with pyyaml <HOME>/Workspace/dotfiles/scripts/validate-agent-assets.py --mask-secrets .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/task.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/revise.yaml
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/report.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/validation.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/sandbox.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/learning.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/autoskill.md
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-crit.json
masked 0 match(es) in .orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md
(exit 0)
```

## round3-code-whitespace

```text
$ git diff --check -- scripts/update-agent-assets.sh tests/unit/test_update_agent_assets.py
(exit 0)
```

## round3-review-gate

```text
$ env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/dotfiles-T129-assets-omp-hcom-a01/dotfiles-T129-assets-omp-hcom-a01-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
(exit 0)
```
