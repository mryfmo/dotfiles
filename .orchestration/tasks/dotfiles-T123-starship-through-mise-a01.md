# AGMSG-TASK dotfiles-T123-starship-through-mise-a01

Drafted 2026-10-10 by the orchestrator seat (`claude-deep-dot`, w4:p1), as the follow-up named in T119 Amendment 7. T119 re-pinned starship because its releases are mutable and carry no attestation or signature; a same-release `.sha256` verifies the download only. The operator's intended shape is a manager that applies the cooldown and the publisher's safety features, so the question is whether mise can own starship with a verification that does not come from the release page it downloads from. Kind: research first, then the mise config, one installer and template deletion, tests and README; Claude seat allowed. Dispatched after T120 merges (file overlap on `home/dot_mise/config.toml`, README). **Amended 2026-10-11 (T128 reset of T120):** T120 will not merge; this task is dispatchable after T127 (T120's redesign) is accepted, or earlier if its scope does not depend on T120's changes, and it is converted to format 2 before dispatch.

## Research (paste the evidence; the decision follows from it)

1. `mise registry` maps `starship` to `aqua:starship/starship`. Read the aqua registry entry (`aquaproj/aqua-registry`, `pkgs/starship/starship/registry.yaml`): does it declare `cosign`, `slsa_provenance`, `minisign` or `github_artifact_attestations` for starship, or only a `checksum` taken from the release's `.sha256` files? Check the starship release assets for signatures or attestations (`gh api repos/starship/starship/releases/latest --jq '.assets[].name'`, `gh api repos/starship/starship/attestations/sha256:<digest>` for one asset).
2. mise settings `aqua.cosign`, `aqua.slsa`, `aqua.minisign`, `aqua.github_artifact_attestations` (names as `mise settings ls --all` prints them, default values pasted): which verifications mise performs for an aqua package that declares them, and what it does when the registry declares none.
3. If starship's registry entry provides an independent verification (anything beyond the same-release checksum), starship moves to mise: `starship = "latest"` in `home/dot_mise/config.toml` (under the 72h cooldown), the aqua verification settings asserted on in the config if not default, `install/ubuntu/server/starship.sh`, its `run_after_10` template, `tests/install/ubuntu/server/*starship*` and the `assets.starship` manifest entry deleted, the unit tests that name them updated, README's exception list and the asset table corrected. If it does not, starship stays pinned as T119 left it, and this task ends with the evidence and one README sentence saying why (`mise` would verify no more than the installer does).
4. The same question for `crit` through mise's `github:` backend (`github:tomasz-tomczyk/crit`): without a lockfile the backend has no independent checksum, so unless mise offers one (`mise settings` for GitHub artifact attestations on the github backend), crit stays pinned; one sentence in the report.

Forbidden: anything else; `make update`; touching `~/.local/share/chezmoi`; thread resolution.

## Standing instruction on Bot and CI findings (operator, 2026-10-09)

Every Codex Bot finding and every CI failure on the PR is fixed at its root cause in the PR itself, not dispositioned. A `not-applicable` is reserved for a finding that is factually wrong, with the refuting command and output pasted in the reply. A finding on the task's own wording is still fixed in the PR. "Out of scope" is not a disposition for a finding on files the PR touches: report the scope gap and the orchestrator amends the allowed files. Recheck the reviews once more right before sending the RESULT.

[memory:decision] dotfiles-T123 (orchestrator 2026-10-10): a release asset rolls only with a publisher verification independent of the release page (attestation, pinned-key signature, immutable registry index); a manager such as mise owns the tool when its registry supplies that verification under the 72h cooldown; otherwise the reviewed pin stays with its reason.

## Repo / branch

`.claude/worktrees/worker-c` after T127 (T120's redesign) is accepted, or earlier if independent of T120: `git fetch origin`; `git switch -c feat/starship-through-mise --no-track origin/main`.

## Allowed files

`home/dot_mise/config.toml`, `install/ubuntu/server/starship.sh` (delete), `home/.chezmoiscripts/ubuntu/run_after_10-install-starship.sh.tmpl` (delete), `home/dot_agents/agent-config.yaml` (`assets.starship` only), `scripts/lib/installer-pins.sh` (the starship constants), `scripts/check-tools.sh` (the starship line), `README.md` (the asset paragraph and exception list), `tests/install/ubuntu/server/starship.bats` (or the file that tests the installer), `tests/unit/test_supply_chain_policy.py`, `tests/unit/test_asset_manifest.py`, `tests/unit/test_runtime_health.py` (starship cases only), `tests/install/common/check_tools.bats` (the starship case). Artifacts at the standard `dotfiles-T123-starship-through-mise-a01` paths in the main checkout, masked.

## Validation commands (paste verbatim output, whole)

```
<the registry entry, the release asset listing, the attestation query, mise settings ls --all | grep -E 'aqua|attestation'>
<scratch MISE_CONFIG_DIR/MISE_DATA_DIR install of starship@latest with the cooldown, showing what mise verified (MISE_DEBUG=1 lines naming cosign/slsa/attestation or checksum)>
make render-check; echo "rc=$?"
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
make unit-test 2>&1 | tail -3
gh pr checks <pr>
```

## Completion

PR to `main` (English title `feat(tools): install starship through mise when its registry verifies the release`, or `docs(assets): why starship and crit stay pinned` if the research says no; attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line with the command and output pasted, then `AGMSG-RESULT v1 task_id=dotfiles-T123-starship-through-mise-a01` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=12.

## Addendum (orchestrator, 2026-10-10) — two mise bootstrap items join this task

- `install/common/mise.sh` runs `gpgv --keyring <scratch keyring>` without `--homedir`, so gpgv's default keyring (`~/.gnupg/trustedkeys.kbx`) is also consulted and a key the user once trusted could validate the checksums; pass `--homedir <scratch>` (or `--keyring` with `--ignore-time-conflict` is not the point: isolation is), as T120's `ensure_claude_code` does; test with a fake trustedkeys.kbx that must not validate.
- The mise release key is fetched from keys.openpgp.org at bootstrap (fingerprint pinned); commit the key under `home/` like the AWS key, with the keyserver as fallback only, so a keyserver outage cannot fail a Linux bootstrap.
`install/common/mise.sh` and its tests join `allowed_files`.
