# dot-upgrade-regen-T1-a01 report

Status: ready_for_review

## Result

- Plain `make upgrade` completed on macOS with `Upgrade summary: required failures: 0; optional warnings: 0` after one retry.
- The first run completed most upgrades but exited 2 after a transient connection reset during mise self-update; the retry updated mise from 2026.9.10 to 2026.9.12 and exited 0.
- Regenerated changes are limited to `home/dot_mise/config.toml` and `home/dot_mise/mise.lock`.
- `scripts/lib/installer-pins.sh` was regenerated with identical content (`cmp` exit 0).
- No out-of-scope tracked worktree diff was produced.

## Repository pin changes

| Tool | Old | New |
| --- | --- | --- |
| node | 26.7.0 | 26.8.2 |
| rust | 1.98.0 | 1.98.1 |
| age | 1.3.1 | 1.3.2 |
| bun | 1.4.0 | 1.4.2 |
| chezmoi | 2.72.0 | 2.72.2 |
| cmake | 4.4.2 | 4.4.3 |
| dotenvx | 2.21.0 | 2.24.1 |
| hugo-extended | 0.165.0 | 0.166.0 |
| uv | 0.12.5 | 0.12.13 |
| yazi | 26.8.15 | 26.9.1 |
| shfmt | 3.13.1 | 3.14.1 |
| npm:@anthropic-ai/claude-code | 2.1.251 | 2.1.278 |
| npm:@openai/codex | 0.150.1 | 0.155.1 |
| npm:ccstatusline | 2.2.27 | 2.2.29 |
| npm:ccusage | 20.0.19 | 20.0.20 |
| npm:pyright | 1.1.413 | 1.1.414 |
| github:cli/cli | 2.98.0 | 2.100.0 |
| github:ogulcancelik/herdr | 0.8.2 | 0.9.0 |

The paired lockfile was regenerated for all configured platforms. The fast-moving Codex and Claude CLI phase intentionally advanced those two npm pins to current releases after the general 7-day-window phase.

## Releases ignored by `minimum_release_age = 7d`

These lines are from the successful run:

- dotenvx 2.28.2 (eligible 2026-09-27 09:19 JST); latest eligible 2.24.1.
- github:cli/cli 2.101.0 (eligible 2026-09-22 23:24 JST); latest eligible 2.100.0.
- github:ogulcancelik/herdr 0.9.1 (eligible 2026-09-24 03:40 JST); latest eligible 0.9.0.
- node 26.9.0 (eligible 2026-09-23 09:00 JST); latest eligible 26.8.2.
- npm:bash-language-server 5.8.1 (eligible 2026-09-27 05:44 JST); latest eligible 5.6.0.
- npm:ccstatusline 2.2.30 (eligible 2026-09-25 02:42 JST); latest eligible 2.2.29.
- npm:ccusage 20.0.24 (eligible 2026-09-28 20:28 JST); latest eligible 20.0.20.
- uv 0.12.17 (eligible 2026-09-26 03:59 JST); latest eligible 0.12.13.

## Skips and warnings

- Homebrew `node` was skipped because it is a forbidden formula.
- mise `fd` was skipped because newer releases lack a macOS x64 asset.
- Pinned HTTP tools `http:bats` and `http:gcloud` were skipped by the generic mise bump.
- The successful run emitted the informational `mise WARN  No untrusted config files found.` plus the eight minimum-release-age warnings listed above.
- The initial run also emitted transient GitHub HTTP timeout/retry warnings and failed only the mise self-update connection; the successful retry resolved that required failure.
- No herdr reload failure occurred; this upgrade path refreshed integrations but did not report a server reload error.

## Machine effects and reversal

Effect `make-upgrade-user-tools` includes Homebrew formula/cask updates, mise self-update and tool updates, agent CLI/plugin/assets refreshes, and other user-level lifecycle updates performed by plain `make upgrade`. Notable Homebrew changes were uv 0.12.15→0.12.17, crit 0.20.1→0.20.2, ffmpeg 9.0.1_1→9.0.2, mole 1.54.0→1.55.0, protobuf 36.1→36.2, mosh 1.4.0_42→1.4.0_43, terraform 1.16.1→1.16.3, awscli 2.36.47→2.36.50, codexbar 0.60.4→0.63.0, aws-c-common 1.0.0→1.0.1, and aws-c-s3 1.1.2→1.1.3.

Reverse mapping for `make-upgrade-user-tools`: **irreversible as one atomic operation** because package managers removed prior installed versions and refreshed external caches/assets. Repository pin changes can be reversed with the reviewed Git diff; individual machine tools require reinstalling the recorded prior version with their owning package manager, then rerunning the corresponding asset installer if applicable.

## Validation

- `uv run python -m unittest tests.unit.test_supply_chain_policy`: 17 tests, OK.
- Revision: `uv run python -m unittest tests.unit.test_statusline_tools`: 5 tests, OK after the expected pre-fix failure.
- Revision: all six workflow YAML files parsed with `yaml.safe_load`.
- Node-first revision: the focused test failed before the workflow change, then passed all 5 tests; supply-chain remained 17 tests OK and all six workflows parsed.
- `git diff --check`: exit 0.
- Revision's consumer implementation diff is limited to the four approved files: `.github/workflows/test.yaml`, `tests/unit/test_statusline_tools.py`, `scripts/check-statusline-tools.py`, and `tests/install/common/mise.bats`; task evidence files were also updated.
- Full command evidence: `.orchestration/validation/dot-upgrade-regen-T1-a01.md`.

## CI revision

The superseding revision aligns all exact-version consumers with the regenerated pins:

- `.github/workflows/test.yaml`: mise-action 2026.7.5→2026.9.12, ccstatusline 2.2.27→2.2.29, ccusage 20.0.19→20.0.20.
- `tests/unit/test_statusline_tools.py`: exact config/lock and workflow token expectations updated to ccstatusline 2.2.29 and ccusage 20.0.20.
- `scripts/check-statusline-tools.py`: smoke-test version expectations updated to ccstatusline 2.2.29 and ccusage 20.0.20.
- `tests/install/common/mise.bats`: herdr config assertion updated from 0.8.2 to 0.9.0. The Bats suite was not run locally, per repository policy.

Repository scan found one remaining `0.8.2` occurrence outside lock/history: `home/dot_local/bin/common/executable_herdr-agents:70`, in the comment `Derive and validate a herdr 0.8.2 agent registration name.` It is outside the explicitly approved four-file revision scope and is not an exact-version runtime consumer, so it was reported rather than changed. No remaining `2.2.27`, `20.0.19`, or `2026.7.5` runtime/test consumer was found outside historical evidence.

## Node-first CI revision

mise 2026.9.12 requires the configured dependency `node@26.8.2` to be installed before the locked npm statusline tools in the isolated workflow directory. `.github/workflows/test.yaml` now runs the locked node install first, mirroring `install/common/mise.sh::run_mise_install`. `tests/unit/test_statusline_tools.py` asserts both presence and ordering. The subsequent smoke step already runs after installation and resolves both binaries from their exact mise roots, so it required no change.

## CompactionDB

[memory:decision] The Mac-generated config/lock pair is the authoritative chore diff for this task; installer pins were unchanged. Dedicated worktrees must copy the regenerated pair from the active mise symlink target.

Memory ID: `da6cdf40-7e32-4480-9b50-7d394ad7d838`

Exact command:

```sh
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-upgrade-regen-T1-a01: Mac make upgrade regenerated home/dot_mise/config.toml and mise.lock for the chore change; installer-pins.sh remained unchanged. Because ~/.config/mise config and lock symlink to the normal checkout, a dedicated worktree must copy the regenerated pair from those symlink targets before review.'
```

[memory:decision] Exact-version CI and smoke-test consumers must advance with regenerated mise pins.

Revision memory ID: `0578538c-58fa-4da5-a467-a4e6aae4dd3d`

Exact command:

```sh
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-upgrade-regen-T1-a01 revision: CI exact-version consumers must advance with regenerated mise pins. test.yaml now uses mise-action 2026.9.12, ccstatusline 2.2.29, and ccusage 20.0.20; Python smoke expectations match; the mise.bats herdr assertion matches 0.9.0.'
```

[memory:decision] mise 2026.9.12 requires node to be installed before configured npm tools in the isolated CI directory.

Node-first revision memory ID: `f2e8be05-427a-4c7d-894c-98d2ec4a4f24`

Exact command:

```sh
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-upgrade-regen-T1-a01 node-first revision: mise 2026.9.12 requires configured install dependency node@26.8.2 to be installed before locked npm statusline tools in the isolated CI mise directory; test.yaml now mirrors run_mise_install ordering and the unit test asserts it.'
```

cost: n/a
