# AGMSG-TASK dotfiles-T119-rolling-release-assets-a01

Drafted 2026-10-09 by the orchestrator seat (`claude-deep-dot`, w4:p1). Wave 2 of the operator's 2026-10-09 decision (T118 is wave 1): the release-asset installers stop carrying reviewed version pins and install the latest release that the publisher's own integrity mechanism can verify; where a publisher offers no verification, the pin stays and says why. Kind: installer scripts, the `assets:` section of the manifest, the renderer's asset constants, the installer-pins library, tests and prose; no permission, sandbox or hook block; Claude seat allowed. Dispatched after T118 merged (file overlap on `install/common/mise.sh`, `scripts/update-agent-assets.sh`, the manifest, README and the tests).

## Principle, stated once

For each entry of `assets:` in `home/dot_agents/agent-config.yaml`, the installer resolves the newest release at install time and verifies it with what the publisher provides, in this order of preference: a signed or attested artifact (GitHub artifact attestations via `gh attestation verify --repo <owner/repo>`, cosign/minisign signatures, a GPG signature with a key whose fingerprint the manifest keeps), then a publisher checksum file fetched from the same release. Only when a publisher offers nothing at all does the manifest keep a `pin` plus the committed `sha256`, with a one-line `reason`. The `verify` field names the mechanism actually used, and the manifest gains `release: latest` for rolling assets; `render:` constants and `scripts/lib/installer-pins.sh` go away for every rolling asset. Nothing is downloaded over plain HTTP; a verification failure leaves the installed tool untouched (the installers already stage and swap atomically; keep that).

## Per asset (research each with the real upstream before coding; paste the evidence)

- `mise` (`install/common/mise.sh`, bootstrap only): latest release from `https://api.github.com/repos/jdx/mise/releases/latest`, verified with that release's `SHASUMS256.txt` (as today) and, if the repository publishes them, GitHub attestations. After bootstrap, `mise self-update` (T118) keeps it current.
- `chezmoi-bootstrap` (`setup.sh#run_chezmoi`): latest release with its `chezmoi_<ver>_checksums.txt`, and the cosign signature of that checksums file if published (check the release assets).
- `starship` (`install/ubuntu/server/starship.sh`): latest release with its `.sha256` sidecar.
- `sheldon` (`install/common/sheldon.sh`): `cargo install sheldon --locked` without a version; cargo verifies the crate against the registry index; the constant goes.
- `aws-cli` (`install/ubuntu/common/aws_cli.sh`): the unversioned archive `awscli-exe-linux-<arch>.zip` is AWS's "latest" and ships a `.sig`; keep the GPG verification and the pinned key fingerprint (that is the publisher's mechanism), drop the version constant and the `aws-cli/<version>` equality check (report the installed version instead).
- `crit` (`scripts/update-agent-assets.sh#ensure_crit_cli`): check whether `tomasz-tomczyk/crit` releases carry GitHub attestations or a checksums file; if yes, latest with that; if no, the per-platform `sha256` pins stay with `reason: publisher ships no checksums or attestations`.
- `zed` (`install/ubuntu/client/zed.sh`): check whether `zed-industries/zed` releases publish `.sha256` files or attestations; same rule.
- `tode` and `terminal-browser` (`installer-script`, `payload-not-pinned-yet`): these are vendor install scripts fetched from `tode.sh` / `terminal-browser.sh`; check whether the projects publish GitHub releases with attestations or checksums that the installer could use instead of a script, or whether the script itself is signed. If neither, the script's `sha256` pin stays with a reason, and the report says so plainly: an unsigned `curl | bash` script is the one case where a committed hash is the only integrity check.
- `homebrew-installer` and `understand-anything-installer` (`git-commit` + `sha256` of a script): the publishers sign nothing; keep the pins with a reason (installer scripts, bootstrap-time only).
- `agmsg` (`AGMSG_PIN_VERSION` in `scripts/update-agent-assets.sh`): check the release assets of the agmsg repository for checksums or attestations; same rule.
- `compactiondb` (vendored) and `codex-plugins` are out of scope.

## Code and tests

- `scripts/generate-agent-configs.py` `render_asset_constants`: rolling assets have no `render:`; the function keeps working for the remaining pinned ones. `scripts/validate-agent-assets.py` asset rules (~580–700): `release: latest` is valid for `github-release`, `https-download`, `crates`; a rolling asset has no `pin`, `ref`, `ref_commit` or `sha256`; a pinned asset needs `reason`; `verify` values gain `github-attestation` (and whatever else is used) with their required fields. `scripts/lib/installer-pins.sh` shrinks to the remaining pinned constants or is deleted if none remain; every consumer (`install/ubuntu/client/zed.sh`, the zed chezmoi script, `scripts/update-agent-assets.sh`, `scripts/check-tools.sh`, `.github/workflows/test.yaml:155`) follows. Tests: `tests/unit/test_release_asset_pins.py`, `tests/unit/test_aws_cli_acquisition.py`, `tests/unit/test_asset_manifest.py` rewritten to the new rules (resolution of `latest` is faked with a local HTTP fixture or a fake `gh`/`curl` on PATH, as the existing tests already fake downloads); `tests/unit/test_validate_agent_assets.py` and `tests/unit/test_generate_agent_configs.py` where the rules move. README ~1285–1305 (the asset table paragraph: `pin: unknown`, `installer-pins.sh`) becomes the principle above in one paragraph, with the exceptions listed by name and reason.

Forbidden: anything else; `make update`; running the installers against the host (scratch `HOME`/prefix only); touching `~/.local/share/chezmoi`; thread resolution; T118's files beyond the lines this task names.

User-visible change for the PR body: fresh machines and `make update` install the latest release of each asset that its publisher can verify; the manifest lists the assets that stay pinned and why.

[memory:decision] dotfiles-T119 (orchestrator 2026-10-09): release-asset installers install the latest release verified by the publisher's own mechanism (attestation or signature first, checksum file second); only assets whose publisher offers nothing keep a pinned version and checksum with a stated reason; `render:` constants and `installer-pins.sh` exist only for those.

## Standing instruction on Bot and CI findings (operator, 2026-10-09)

Every Codex Bot finding and every CI failure on the PR is fixed at its root cause in the PR itself, not dispositioned. A `not-applicable` is reserved for a finding that is factually wrong, with the refuting command and output pasted in the reply. A finding on the task's own wording is still fixed in the PR. "Out of scope" is not a disposition for a finding on files the PR touches: report the scope gap and the orchestrator amends the allowed files. Recheck the reviews once more right before sending the RESULT.

## Repo / branch

`.claude/worktrees/worker-c`; after T118 merged: `git fetch origin`; `git switch -c feat/rolling-release-assets --no-track origin/main`.

## Allowed files

`home/dot_agents/agent-config.yaml` (`assets:` only), `scripts/generate-agent-configs.py` (asset rendering), `scripts/validate-agent-assets.py` (asset rules), `scripts/lib/installer-pins.sh`, `install/common/mise.sh` (download/verify part), `install/common/sheldon.sh`, `install/ubuntu/server/starship.sh`, `install/ubuntu/common/aws_cli.sh`, `install/ubuntu/client/zed.sh`, `home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl`, `setup.sh` (chezmoi bootstrap and the rendered constants), `install/macos/common/brew.sh` (only if its constants move), `scripts/update-agent-assets.sh` (crit, tode, terminal-browser, agmsg sections), `scripts/check-tools.sh`, `.github/workflows/test.yaml` (the `installer-pins` line), `README.md` (the asset paragraph), `tests/unit/test_release_asset_pins.py`, `tests/unit/test_aws_cli_acquisition.py`, `tests/unit/test_asset_manifest.py`, `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_generate_agent_configs.py`. Artifacts at the standard `dotfiles-T119-rolling-release-assets-a01` paths in the main checkout, masked.

## Validation commands (paste verbatim output, whole)

```
<per-asset evidence: the release asset listing or attestation check for each upstream (gh api …/releases/latest --jq '.assets[].name'; gh attestation verify … where claimed)>
shellcheck install/common/mise.sh install/common/sheldon.sh install/ubuntu/server/starship.sh install/ubuntu/common/aws_cli.sh install/ubuntu/client/zed.sh scripts/update-agent-assets.sh; echo "rc=$?"
<scratch-HOME run of one rolling installer end to end, e.g. starship or mise, showing resolution, verification and the installed version>
make render-check; echo "rc=$?"
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
uv run python -m unittest tests.unit.test_release_asset_pins tests.unit.test_aws_cli_acquisition tests.unit.test_asset_manifest tests.unit.test_validate_agent_assets tests.unit.test_generate_agent_configs 2>&1 | tail -3
make unit-test 2>&1 | tail -3
gh pr checks <pr>
```

## Completion

PR to `main` (English title `feat(assets): install the latest publisher-verified release, pin only what cannot be verified`, English body with the per-asset table: mechanism used or reason for the remaining pin; attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line, then `AGMSG-RESULT v1 task_id=dotfiles-T119-rolling-release-assets-a01` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=24.
