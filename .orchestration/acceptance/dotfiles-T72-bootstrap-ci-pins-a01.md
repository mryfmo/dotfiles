# Acceptance: dotfiles-T72-bootstrap-ci-pins-a01

- **Decision:** ACCEPTED. PR #256 squash-merged to `main` as `2ad504e3`; final head `d5856e26fe3b2ae05dd86047550cae048cc634a9`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, six dispositions below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 13:45Z).
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `sha256:6c432d04…688c` matched (the worker hashed it from the boundary branch 48a83e6c; the same bytes are on `main` since #255).
- **Exemption declared:** acceptance and final integration (sweep, evidence, gate, merge, ACCEPTANCE).
- **Plan reference:** Phase 3, dotfiles-T72 (principle 3: one pin location). Depends on T71 (merged 65915b93).

## What was accepted (PR #256, head `d5856e26fe3b2ae05dd86047550cae048cc634a9`; commits 25c7a637, 52ec8f88, 339ce6e7 update-branch onto 680b29b1, d5856e26)

- `assets.chezmoi-bootstrap` (github-release, twpayne/chezmoi, pin 2.70.4 unchanged, release-shasums) renders `setup.sh` `CHEZMOI_VERSION` and `scripts/lib/installer-pins.sh` `CHEZMOI_BOOTSTRAP_PIN_VERSION`; `homebrew-installer` also renders `setup.sh` lines 32-33. `make render-check` clean, so no rendered value moved.
- `bump_release_asset_pins` resolves the chezmoi pin (tags stripped of `v`) under the same 7-day window and writes `--set-asset chezmoi-bootstrap.pin=…`.
- CI: `test.yaml` installs chezmoi from the pinned release tarball on both platforms (checksums verified, `shasum` fallback on macOS) and asserts `chezmoi --version` reports the pin; the drifted literal 2.70.5 and the brew-installed chezmoi are gone. Every `jdx/mise-action` (`test.yaml`, `docs.yml`, `ubuntu.yaml`, `macos.yaml`) takes `version: ${{ env.DOTFILES_MISE_VERSION }}` from a preceding step that reads `install/common/mise.sh`; the `2026.9.12` literal is gone.
- `Dockerfile`: `ARG CHEZMOI_VERSION` (no default, build fails without it), checksum-verified release tarball instead of the unpinned `get.chezmoi.io` pipe, `LABEL chezmoi.version`; `make docker` rebuilds when the label differs from the `setup.sh` pin (Codex P2 4177599468, fixed d5856e26).
- Validator: `validate_assets` scans `setup.sh` too (`scripts/lib` was already covered by the `scripts/` rglob).
- Tests: generator render fixture, validator setup.sh scan, and the release-pin bump sequence (five pins).

## Deviations (accepted)

- `tests/unit/test_release_asset_pins.py` edited outside `allowed_files`: it pins the exact `--set-asset` call sequence, so the fifth pin cannot land without it; class-pure test sync of the changed script.
- Env var named `DOTFILES_MISE_VERSION`, not the task's `MISE_PIN`: mise reads every `MISE_*` variable as a setting and `MISE_PIN` is its boolean `pin` setting; the first CI run on 25c7a637 failed on it (log excerpt in the validation file). The rename is the correct fix.
- The task's grep criterion hits `setup.sh:32,34`: those are the rendered constants (`setup.sh` is now a render target), which is the intended end state; the criterion as written was imprecise.

## Orchestrator re-derivation

- Read the full diff against origin/main (13 files, +188/−34, no `.orchestration` files in the PR). Checked `setup.sh` lines 32-34 match the manifest values; the Makefile sed pattern matches `declare -r CHEZMOI_VERSION="…"`; the Dockerfile artifact name follows chezmoi's `linux_<dpkg arch>` naming; the `||` chain in `bump_release_asset_pins` with the interleaved comment is exercised by the bump unit test.
- Coverage limit acknowledged: `docs.yml` (push-to-main only) and the secret-gated `ubuntu.yaml`/`macos.yaml` build steps did not run the new pin step on the PR; the identical step passed in `test.yaml` on ubuntu and macos-14. Residual risk is a workflow-syntax slip in those three files, caught on the next main push or gated run.
- Residual (not blocking): `grep -F "v2.70.4"` on `chezmoi --version` would also accept `v2.70.40`; a future pin bump keeps the check meaningful in practice.
- CI 16/16 green on d5856e26; branch up to date (behind_by 0); PR `clean` after the thread resolution.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head d5856e26 | incorrect (6) → dispositions below |

audit-finding: 1 the sandbox file records pushes, `gh` calls and the main-checkout CompactionDB write run outside the worker sandbox → not-applicable:the standing Claude-seat GitHub exception (GitHub calls and the main-checkout memory add go through the permission gate, answered by the auto-mode classifier since T62), written into the Worker Playbook by T69 (PR 253) and rooted out by T97; no other out-of-sandbox action is recorded
audit-finding: 2 `tests/unit/test_release_asset_pins.py` is outside the task's `allowed_files` → not-applicable:accepted deviation; the test pins the exact `--set-asset` sequence of `bump_release_asset_pins`, so the fifth pin cannot land without it, and the edit is a class-pure test sync of the changed script (recorded above)
audit-finding: 3 `test.yaml:187` matches the pinned version as a substring, so `v2.70.40` would satisfy a `2.70.4` pin → not-applicable:the assertion guards against a runner-provided chezmoi shadowing the just-installed pin, and a shadow binary differs in minor or patch; the only false pass is a same-minor release whose patch extends the pinned patch by a digit (2.70.4 vs 2.70.40), and the 2.70 line has only single-digit patches (checked against the twpayne/chezmoi release tags on 2026-10-04; two-digit patches exist only in the 2.0 line), so the check is exact for the pinned line
audit-finding: 4 `docs.yml` never ran on the final head although the task lists it among the green workflows → not-applicable:`docs.yml` triggers only on pushes to `main` and manual dispatch, and its `deploy` job publishes the site, so the worker was right not to dispatch it from a branch; its pin step is byte-identical to the one that passed on both `test.yaml` platforms, and the orchestrator watches the docs run on the merge commit as part of this acceptance
audit-finding: 5 the report's Bot thumbs-up timestamps for the first two heads have no pasted reaction snapshot → not-applicable:evidence-only finding about superseded heads; the final head has no Bot review, and the orchestrator's sweep of d5856e26 is the acceptance evidence
audit-finding: 6 the report's `make -n docker | bash -n` line reads as if the recipe expanded the pin → not-applicable:the claim is syntax validity of the recipe, not value expansion; the orchestrator re-derived the value separately (`sed -n 's/^declare -r CHEZMOI_VERSION="\(.*\)"$/\1/p' setup.sh` prints `2.70.4` on this checkout)

- Codex Bot: one P2 thread (4177599468, Makefile) fixed in d5856e26; the orchestrator replied `fixed:d5856e26` (4177830465) and resolved it after confirming the fix commit is the head. No Bot review on the final head within the worker's 15-minute window.
- Sweep (head d5856e26): 10 items, 1 `fixed:d5856e26`, 9 `not-applicable` (CodeRabbit summary/status, two Codex/own review containers, the orchestrator's reply, four macOS capacity notices). Masked copy: `.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-pr-feedback.json`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## CompactionDB

- Worker decision `a9e30717-83d1-4b7b-8af2-efef3b533be1`; orchestrator consolidation `def52896-d2c5-4f35-bc64-e4401503ff48`.

## Post-merge (2026-10-04 13:58Z)

- All six main-branch workflows on `2ad504e3` succeeded: Docs 37206650166 (its `Pin mise` and `Setup mise` steps ran and passed, closing audit finding 4), Ubuntu 37206650062, MacOS 37206650090, Agent assets 37206650061, Unit test 37206650088, Snippet install 37206650155.
- The `ubuntu.yaml`/`macos.yaml` pin and mise-action steps were `skipped` on `main` as well (the private deploy-key and email secrets gate them and are absent here), so those two files' new steps remain unexercised in this repository; the step text is byte-identical to the passing `test.yaml`/`docs.yml` steps.
