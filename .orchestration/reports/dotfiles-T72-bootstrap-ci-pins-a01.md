# Report: dotfiles-T72-bootstrap-ci-pins-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/bootstrap-ci-pins` from `origin/main` 2e2e1e09. Earlier branches are untouched.
- **task_rev:** `sha256:6c432d04…688c`, matched. The main checkout no longer holds the task file (the boundary commit #255 moved it), so I read and hashed it from `origin/orchestration/boundary-2026-10-04` (48a83e6c).
- **PR:** #256, https://github.com/mryfmo/dotfiles/pull/256.
- **Commits:**
  - `25c7a637`: the change.
  - `52ec8f88`: CI fix; see section 3.
  - `339ce6e7`: `gh pr update-branch`, merging main 680b29b1 (#255).
  - `d5856e26`: Codex P2 4177599468; `make docker` rebuilds on a pin change.
- **Final head:** `d5856e26`. CI, branch and bot state are in the validation file.
- **Status:** ready_for_review.

## 1. What changed

1. **Assets** (`home/dot_agents/agent-config.yaml`):
   - New `chezmoi-bootstrap`:
     - `github-release`, `twpayne/chezmoi`, `pin: 2.70.4`, `verify: release-shasums`, `install_path: ~/.local/bin/chezmoi`, `installer: setup.sh#run_chezmoi`;
     - its render list writes `setup.sh` `CHEZMOI_VERSION` (`declare -r`) and `scripts/lib/installer-pins.sh` `CHEZMOI_BOOTSTRAP_PIN_VERSION`, a new line.
   - `homebrew-installer`'s render is now a list: `install/macos/common/brew.sh` plus `setup.sh` (`HOMEBREW_INSTALL_COMMIT` and `HOMEBREW_INSTALL_SHA256`, `declare -r`).
   - No pin value changed; the manifest values equal the `setup.sh` values, and `make render-check` is clean.
2. **`scripts/upgrade-tools.sh` `bump_release_asset_pins`:** also resolves `chezmoi-bootstrap` from `github_release_versions twpayne/chezmoi | sed 's/^v//'` under the same 7-day window. It writes `--set-asset chezmoi-bootstrap.pin=…`, and the summary line names chezmoi.
3. **CI:**
   - **chezmoi:**
     - `test.yaml` installs chezmoi from the pinned release tarball on both macOS and Ubuntu. The version comes from sourcing `installer-pins.sh` (`CHEZMOI_BOOTSTRAP_PIN_VERSION`), the platform from `uname`, and the release checksums are verified (`sha256sum`, or `shasum -a 256` where `sha256sum` is missing).
     - macOS no longer takes chezmoi from `brew install`. The literal `2.70.5` that had drifted from `setup.sh`'s 2.70.4 is gone.
     - A new assertion checks that the resolved `chezmoi --version` reports the pinned version, so a runner-provided binary earlier on PATH cannot shadow it.
   - **mise:** every `jdx/mise-action` (`test.yaml`, `docs.yml`, `ubuntu.yaml`, `macos.yaml`) takes `version: ${{ env.DOTFILES_MISE_VERSION }}`. A preceding step writes that variable from `install/common/mise.sh`'s rendered `MISE_VERSION`, using the task's `sed` expression and `test -n`.
     - Before, `test.yaml` pinned `2026.9.12` against the manifest's `v2026.9.14`, and docs, ubuntu and macos installed the latest mise. CI now runs mise 2026.9.14, the single manifest pin; that follows from the task, not from a pin change.
4. **`Dockerfile`:** `ARG CHEZMOI_VERSION` with no default, and a guard that fails the build without it. The image installs that checksum-verified release tarball (`dpkg --print-architecture`) instead of piping the unpinned `get.chezmoi.io` script to `sh`. The `Makefile` `docker` target passes `--build-arg CHEZMOI_VERSION="$(sed -n 's/^declare -r CHEZMOI_VERSION="\(.*\)"$/\1/p' setup.sh)"`; `make -n docker` expands it to 2.70.4. After the Codex P2 on `339ce6e7`, the image carries `LABEL chezmoi.version=$CHEZMOI_VERSION`, and `make docker` rebuilds whenever that label differs from `setup.sh`'s pin, where before it skipped any existing image. CI builds no Docker image, so the Dockerfile is unexercised; `make -n docker | bash -n` passes.
5. **Validator:** `validate_assets` also scans `setup.sh`. `scripts/lib` was already scanned, since `rglob` over `scripts/` covers it, so T71's "left out" applied only to `setup.sh`. The `is_file()` guard keeps the fixture-rooted unit tests, which have no `setup.sh`, working.
6. **Tests:**
   - `test_bootstrap_pins_render_into_setup_and_their_installers` (generator; a fixture of the T72 shapes);
   - `test_assets_scan_setup_sh_for_unrendered_versions` (validator);
   - `test_bump_writes_only_the_five_pins_through_set_asset` (`tests/unit/test_release_asset_pins.py`; see section 2).
   - The validator and bump tests fail against the `origin/main` scripts. The generator test documents the shape; the mechanism already exists since T71.
   - `make unit-test` passes with 785 tests.

## 2. Deviations

- **A file outside allowed_files.** `tests/unit/test_release_asset_pins.py` pins `bump_release_asset_pins`'s exact `--set-asset` call sequence, so item 2 cannot land without editing it. I added the chezmoi fixture asset, the fake `gh` releases, the expected `--set-asset` and the window skip, and renamed the test from "four pins" to "five pins". I decided, recorded and continued under the standing directive.
- **The variable name `MISE_PIN`** (task item 3) breaks mise. mise reads every `MISE_*` environment variable as a setting, and `MISE_PIN` is its boolean `pin` setting. The first CI run on `25c7a637` failed with "failed to deserialize value `Settings::pin` from environment variable `MISE_PIN`: invalid value for bool: '2026.9.14'". `52ec8f88` renames it to `DOTFILES_MISE_VERSION` in all four workflows.
- **`homebrew-installer` source line numbers:** the task's `setup.sh:32-33` matches exactly.

## 3. CI coverage limits

- **`docs.yml`** runs only on pushes to `main` and `workflow_dispatch`. I did not dispatch it on the branch, because its `deploy` job publishes the docs site. Its pin step is identical to the one `test.yaml` runs and passed.
- **`ubuntu.yaml` and `macos.yaml` `build`** ran on the PR, but every step after the explanation is gated on the private deploy key and email secrets, so the pin and mise-action steps were skipped. The job step listing is in the validation file. Those paths run first on a push to `main` with secrets.
- **Exercised on this PR:**
  - `test.yaml`'s chezmoi install on both platforms: the first run's log shows `chezmoi_2.70.4_linux_amd64.tar.gz: OK` and `chezmoi version v2.70.4`, and the final head's 4 test jobs pass, macos-14 included.
  - `test.yaml`'s mise pin.

## 4. Codex bot

| Head | Result |
|---|---|
| `25c7a637` | 👍 at 12:12:25Z. That bot review missed the mise failure; CI caught it. |
| `52ec8f88` | 👍 at 12:22:11Z. |
| `339ce6e7` | P2 4177599468, "Rebuild the Docker image when the pinned version changes": `fixed:d5856e26`. |
| `d5856e26` (final) | No review or reaction within the 15-minute window (pushed 12:39:31Z, polled until 12:55:43Z). The reaction listing shows no 👍 for this head; the earlier 👍 was removed when the head moved. |

I did not reply to or resolve any thread.

## CompactionDB

```
$ cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T72 (operator 2026-10-03): the chezmoi bootstrap version, the Homebrew installer commit/sha, and the mise version used by setup.sh, the Dockerfile and every CI workflow render from `agent-config.yaml` assets; no workflow or bootstrap script holds a version literal of its own.'
a9e30717-83d1-4b7b-8af2-efef3b533be1
[exit 0]
```

[memory:decision] dotfiles-T72 (operator 2026-10-03): the chezmoi bootstrap version, the Homebrew installer commit/sha, and the mise version used by setup.sh, the Dockerfile and every CI workflow render from `agent-config.yaml` assets; no workflow or bootstrap script holds a version literal of its own.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T72-bootstrap-ci-pins-a01.md`
- learning: `.orchestration/learning/dotfiles-T72-bootstrap-ci-pins-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T72-bootstrap-ci-pins-a01.md`

cost: n/a (no subagents, no model-driven runs; the runtime does not expose session totals).
