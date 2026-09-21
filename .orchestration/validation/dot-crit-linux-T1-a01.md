# dot-crit-linux-T1-a01 validation

## Latest release and downloaded SHA-256 values

Command:

```text
printf 'latest release: '; gh api repos/tomasz-tomczyk/crit/releases/latest --jq '.tag_name + " draft=" + (.draft|tostring) + " prerelease=" + (.prerelease|tostring)' && printf 'local sha256:\n' && shasum -a 256 /tmp/dot-crit-linux.D3se9E/crit-linux-amd64 /tmp/dot-crit-linux.D3se9E/crit-linux-arm64 && printf 'upstream checksums:\n' && grep 'crit-linux-\(amd64\|arm64\)$' /tmp/dot-crit-linux.D3se9E/checksums.txt
```

Verbatim output:

```text
latest release: v0.20.2 draft=false prerelease=false
local sha256:
d2907008164fada5bd5221ffd37ed125c181280cec3ed74465e526ea7d25d20a  /tmp/dot-crit-linux.D3se9E/crit-linux-amd64
833dd8145e5b47c06d88af80f8b6505159693742aadefcf400f923d7bc6c3b11  /tmp/dot-crit-linux.D3se9E/crit-linux-arm64
upstream checksums:
d2907008164fada5bd5221ffd37ed125c181280cec3ed74465e526ea7d25d20a  crit-linux-amd64
833dd8145e5b47c06d88af80f8b6505159693742aadefcf400f923d7bc6c3b11  crit-linux-arm64
```

The initial sandboxed download attempt failed before creating artifacts:

```text
curl: (6) Could not resolve host: github.com
```

The approved retry downloaded both binaries and `checksums.txt`; the clean final comparison above records the retained evidence.

## Test-first RED

Command:

```text
uv run python -m unittest tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_install_is_pinned_atomic_and_recorded tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_correct_version_is_download_free tests.unit.test_runtime_health.RuntimeHealthTest.test_linux_crit_checksum_failure_preserves_existing_binary tests.unit.test_runtime_health.RuntimeHealthTest.test_upgrade_bumps_terminal_and_crit_pins_from_fetched_artifacts
```

Verbatim result before implementation:

```text
F.FF
Ran 4 tests in 0.267s

FAILED (failures=3)
```

The already-correct-version no-op passed; install, failure preservation, and upgrade pin rewrite failed until implemented.

## Final shell/static validation

Command:

```text
bash -n scripts/lib/installer-pins.sh scripts/update-agent-assets.sh scripts/upgrade-tools.sh && shellcheck -x scripts/lib/installer-pins.sh scripts/update-agent-assets.sh scripts/upgrade-tools.sh && shellcheck -x -e SC2314,SC2016 tests/install/common/lifecycle.bats && shfmt --indent 4 --space-redirects --diff scripts/lib/installer-pins.sh scripts/update-agent-assets.sh scripts/upgrade-tools.sh tests/install/common/lifecycle.bats && git diff --check && printf 'shell-static-and-diff: OK\n'
```

Verbatim output:

```text
shell-static-and-diff: OK
```

SC2314 and SC2016 are pre-existing findings throughout `lifecycle.bats`; the new assertion was written without adding either finding.

## Final related unit and Python lint validation

Command:

```text
UV_CACHE_DIR=/tmp/dot-crit-linux-uv-cache uv run python -m unittest tests.unit.test_runtime_health tests.unit.test_asset_manifest && UV_CACHE_DIR=/tmp/dot-crit-linux-uv-cache uv run ruff check tests/unit/test_runtime_health.py tests/unit/test_asset_manifest.py
```

Verbatim output:

```text
....................................
----------------------------------------------------------------------
Ran 36 tests in 9.320s

OK
All checks passed!
```

One earlier parallel lint invocation failed only because the sandbox could not initialize the shared `~/.cache/uv`; the task-specific `/tmp` cache retry above passed.

## `make update` clean/dirty driving trace

Command:

```text
uv run python -c 'from tests.unit.test_runtime_health import RuntimeHealthTest; t=RuntimeHealthTest(); t.setUp(); clean,clean_log=t.update_fixture(); dirty,dirty_log=t.update_fixture(dirty=True); print("clean calls:"); print(clean_log.read_text(), end=""); print("dirty pull count:", dirty_log.read_text().count("git pull --ff-only")); print(next(line for line in dirty.stdout.splitlines() if line.startswith("Notice:")))'
```

Verbatim output:

```text
clean calls:
git pull --ff-only
chezmoi apply --verbose --exclude=scripts
mise install --locked node
mise install --locked npm:ccstatusline npm:ccusage
assets
dirty pull count: 0
Notice: local source not pulled (tracked files have staged or unstaged changes); run 'git -C /private/var/folders/r2/_gkywj713g54lbxkc_hv7j400000gn/T/runtime-health-test-7cw69zrr/update-dirty pull' to fetch remote updates.
```

## `adh-test` actual installer E2E

The first nested-shell attempt failed before Crit execution, and its outer trap removed the scratch user:

```text
bash: line 1: binary: unbound variable
```

The simplified direct-user run then succeeded. After Linux output exposed its leading `v`, the matcher was repaired and the final actual-function E2E was rerun.

Command shape:

```text
limactl shell adh-test -- sudo bash -lc '<create dotcrit01; copy exact worktree updater and libraries; run ensure_crit_cli as dotcrit01; print version and manifest path; delete user; assert user and home absent>'
```

Verbatim final output:

```text

==> Crit CLI
crit v0.20.2 (2026-09-18, 10a7475)
Inline code review for AI agent workflows
/home/dotcrit01/.local/bin/crit
scratch cleanup: OK
```

## CompactionDB

Command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dot-crit-linux-T1-a01: Linux Crit installs pin stable v0.20.2 amd64/arm64 release binaries with verified SHA-256 and atomic replacement, while make update pulls only clean main tracking origin/main and otherwise continues with an actionable notice.'
```

Verbatim output:

```text
7520a322-d63d-403a-9837-70af16f3b871
```

## Deliberately not run

```text
bats: NOT RUN locally (task and repository policy require CI)
git commit: NOT RUN
git push: NOT RUN
```

## Agent Crit data review gate

Initial gate output:

```text
Native agent review required before completion.
- review-sensitive path changed: .orchestration/autoskill/runs/dot-crit-linux-T1-a01.md
- broad diff touches 14 files
- broad diff changes 715 lines
make: *** [require-crit-review] Error 1
```

`crit status --json` initially reported no review file. Per the project rule prohibiting browser review, Codex independently reviewed the diff, added review-scope approval `r_c83cb1`, and resolved it. Repo-local evidence is `.agents/worklog/codex/review/dot-crit-linux-T1-a01.json`:

```text
resolved: 1
unresolved: 0
review_outcome: approved
```

The first receipt attempt used the unsupported value `approved-no-findings`:

```text
AGENT_REVIEWED=1 requires review evidence before completion.
- REVIEW_EVIDENCE agent reviewer requires `review_outcome: approved` or `review_outcome: addressed`
make: *** [require-crit-review] Error 1
```

After normalizing the receipt value, command:

```text
AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/dot-crit-linux-T1-a01-receipt.md make require-crit-review
```

Verbatim output:

```text
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Revision: cleanup trap lifetime and README token

Requested runtime-health command:

```text
uv run python -m unittest tests.unit.test_runtime_health
```

Verbatim green output:

```text
..........................
----------------------------------------------------------------------
Ran 26 tests in 8.170s

OK
```

Requested validator command:

```text
uv run --with pyyaml scripts/validate-agent-assets.py
```

Verbatim green output:

```text
agent asset validation ok
```

Revision static command:

```text
bash -n scripts/update-agent-assets.sh && shellcheck -x scripts/update-agent-assets.sh && shfmt --indent 4 --space-redirects --diff scripts/update-agent-assets.sh && git diff --check && printf 'revise-shell-static: OK\n'
```

Verbatim output:

```text
revise-shell-static: OK
```

CompactionDB failure command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dot-crit-linux-T1-a01 revise: a RETURN trap created inside ensure_crit_cli can outlive its local cleanup variables and fail later function returns under set -u; isolate download staging in a subshell helper and use an EXIT trap, following _install_mise_binary.'
```

Verbatim output:

```text
1639ae38-a92b-4f5a-a0c4-b7659a9b257e
```

Revision Crit data evidence added resolved approval `r_ac5c99`. Final Crit status and gate output:

```text
resolved: 2
unresolved: 0
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```

## Revision: Bats logical versus physical fixture path

GitHub was inspected first. Run: https://github.com/mryfmo/dotfiles/actions/runs/35569113472

Failed macOS job: https://github.com/mryfmo/dotfiles/actions/runs/35569113472/job/106236824349

Relevant verbatim log output:

```text
not ok 12 [common] update skips pull for tracked changes and prints the manual command
# (in test file tests/install/common/lifecycle.bats, line 94)
#   `[[ "$output" == *"Notice: local source not pulled (tracked files have staged or unstaged changes); run 'git -C ${UPDATE_FIXTURE} pull' to fetch remote updates."* ]]' failed
```

Ubuntu client job: https://github.com/mryfmo/dotfiles/actions/runs/35569113472/job/106236824366

Ubuntu server job: https://github.com/mryfmo/dotfiles/actions/runs/35569113472/job/106236824343

Relevant verbatim log output:

```text
test (ubuntu-latest, client) Run unit test 2026-09-21T06:36:24.6339350Z ok 12 [common] update skips pull for tracked changes and prints the manual command
test (ubuntu-latest, client) Run unit test 2026-09-21T06:37:11.1629750Z ##[error]The operation was canceled.
test (ubuntu-latest, server) Run unit test 2026-09-21T06:36:31.1527502Z ok 12 [common] update skips pull for tracked changes and prints the manual command
test (ubuntu-latest, server) Upload coverage to Codecov 2026-09-21T06:37:03.7209397Z ##[error]The operation was canceled.
```

The Ubuntu logs do not print the two compared paths. Because the original logical-path assertion passed in both Ubuntu jobs, it is reasonable to infer that those jobs had no observable logical/physical divergence; cancellation occurred later, not in test 12. macOS local physical-resolution proof:

```text
logical parent: /var/folders/r2/_gkywj713g54lbxkc_hv7j400000gn/T
physical parent: /private/var/folders/r2/_gkywj713g54lbxkc_hv7j400000gn/T
```

The test now records `UPDATE_FIXTURE_PHYSICAL="$(cd "${fixture}" && pwd -P)"` and uses that value only for the Notice path assertion.

Allowed local checks (Bats remained CI-only):

```text
$ uv run python -m unittest tests.unit.test_runtime_health
..........................
----------------------------------------------------------------------
Ran 26 tests in 8.100s

OK

$ shellcheck -x -e SC2314,SC2016 tests/install/common/lifecycle.bats && shfmt --indent 4 --space-redirects --diff tests/install/common/lifecycle.bats && git diff --check && printf 'lifecycle-bats-static: OK\n'
lifecycle-bats-static: OK

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
```

CompactionDB command:

```text
python3 .claude/hooks/contextdb_cli.py memory add --kind failure --scope project --content 'dot-crit-linux-T1-a01 revise: Bats temp paths can be logical while make -C reports physical CURDIR (macOS /var versus /private/var); assertions for printed repository paths must derive expected values with pwd -P. In CI run 35569113472 the old assertion failed on macOS but passed on both Ubuntu jobs.'
```

Verbatim output:

```text
b62160c1-001b-444f-afac-f3c18347527f
```

Path-resolution revision Crit evidence and final gate:

```text
resolved: 3
unresolved: 0
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
```
