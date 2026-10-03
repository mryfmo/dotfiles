# Plan 001: Make Starship install tests incapable of deleting unrelated binaries

> **Executor instructions**: Execute every atomic task in order. Confirm each
> Verify result before continuing. Do not run Bats locally. If a STOP condition
> occurs, stop without improvising and report the exact command and output.
>
> **Drift check**: `git diff --stat e7c2808..HEAD -- install/ubuntu/server/starship.sh tests/install/ubuntu/server/starship.bats scripts/run_unit_test.sh`
> If the install/uninstall targets or test HOME setup differ from Current state,
> stop and request plan refresh.

## Status

- **Priority**: P0
- **Effort**: S
- **Risk**: LOW — the intended Starship binary remains the only removal target
- **Depends on**: none
- **Category**: correctness, data-loss prevention, tests
- **Planned at**: commit `e7c2808`, 2026-07-11

## Plan quality self-audit

- [x] Compared with the reference early-plan standard; S scope justifies a
      shorter plan while retaining every execution boundary.
- [x] Required sections are present, including Steps, Commands, Scope, Test
      plan, Maintenance notes, STOP conditions, and 安全回帰.
- [x] Current state uses measured `file:line` evidence from `e7c2808`.
- [x] Scope names every permitted implementation file.
- [x] Every logic change has a positive and adversarial verification.
- [x] Done criteria are command/checklist based.
- [x] STOP conditions are specific to HOME isolation and removal scope.
- [x] DONE requires review/CI evidence and a repeated plan-quality audit.

## Why this matters

`uninstall_starship` currently removes the entire shared user binary directory.
The Ubuntu Server Bats teardown invokes it without replacing HOME. Running that
suite can destroy unrelated executables, including Herdr helpers. The invariant
is strict: this repository may remove only the Starship file it installed.

## Current state

- `install/ubuntu/server/starship.sh:15` sets
  `BIN_DIR="${HOME}/.local/bin"`.
- `install/ubuntu/server/starship.sh:36-38` implements uninstall with
  `rm -rf "${BIN_DIR}"`.
- `tests/install/ubuntu/server/starship.bats:5-10` sources the production script
  and calls `uninstall_starship` in teardown without a temporary HOME.
- `scripts/run_unit_test.sh:30-36` includes the server suite in Ubuntu CI.

## Commands you will need

| Purpose | Command | Expected |
|---|---|---|
| Python regression suite | `make unit-test` | exit 0 |
| Shell syntax | `bash -n install/ubuntu/server/starship.sh tests/install/ubuntu/server/starship.bats` | exit 0 |
| Format check | `shfmt -i 4 -sr -d install/ubuntu/server/starship.sh tests/install/ubuntu/server/starship.bats` | exit 0, no diff |
| Removal scan | `rg -n 'rm -rf .*BIN_DIR|rm -rf .*\.local/bin' install tests` | no matches |
| CI-only Bats | `OS=ubuntu-latest SYSTEM=server ./scripts/run_unit_test.sh` | GitHub Actions only; exit 0 |

## Scope

**In scope**:

- `install/ubuntu/server/starship.sh`
- `tests/install/ubuntu/server/starship.bats`

**Out of scope**:

- Changing the Starship version or installer URL.
- Refactoring other installers or creating a generic uninstall framework.
- Running Bats on the developer workstation.

## Steps

### A001 — Add a failing removal-boundary test

- [ ] In `tests/install/ubuntu/server/starship.bats`, make `setup` save the
      original HOME and set HOME to a fresh `mktemp -d` directory.
- [ ] Create `${HOME}/.local/bin/starship` and
      `${HOME}/.local/bin/must-survive` in a new test.
- [ ] Call `uninstall_starship` and assert Starship is absent, the sentinel is
      present, and `${HOME}/.local/bin` still exists.
- [ ] In teardown, delete only the temporary HOME and restore the original HOME.

**Verify positive**: inspect the test and confirm all filesystem writes use the
temporary HOME.

**Verify adversarial**: temporarily leave production `rm -rf "${BIN_DIR}"`
unchanged in the branch; the new CI Bats test must fail because
`must-survive` disappears. Do not run this adversarial check locally.

### A002 — Narrow the production removal target

- [ ] Change `uninstall_starship` to remove only `${BIN_DIR}/starship`.
- [ ] Use `rm -f --` and a quoted path.
- [ ] Do not remove `${BIN_DIR}`, even when empty.

**Verify**: `rg -n 'rm -f -- "\$\{BIN_DIR\}/starship"' install/ubuntu/server/starship.sh` → exactly one match.

### A003 — Preserve installation behavior

- [ ] Confirm `install_starship` still creates `${BIN_DIR}`.
- [ ] Confirm the upstream installer still receives `--bin-dir "${BIN_DIR}"`.
- [ ] Do not change version selection in this plan.

**Verify**: `rg -n -- '--bin-dir|mkdir -p' install/ubuntu/server/starship.sh` → both existing behaviors remain.

### A004 — Run safe local gates

- [ ] Run `bash -n install/ubuntu/server/starship.sh tests/install/ubuntu/server/starship.bats`.
- [ ] Run `shfmt -i 4 -sr -d install/ubuntu/server/starship.sh tests/install/ubuntu/server/starship.bats`.
- [ ] Run `make unit-test`.
- [ ] Confirm Bats was not run locally.

### A005 — Obtain CI proof

- [ ] Push only after operator authorization.
- [ ] Confirm the Ubuntu Server matrix ran the Starship Bats file.
- [ ] Confirm the sentinel regression passed.
- [ ] Save the GitHub check URL in the PR/acceptance record.

## Test plan

- Regression: Starship is removed while a sibling sentinel survives.
- Isolation: teardown restores HOME and removes only its temporary directory.
- Existing install assertion: Starship is installed under temporary HOME.
- Existing Python suite remains green.

## Done criteria

- [ ] `uninstall_starship` contains no directory-recursive removal.
- [ ] A test proves an unrelated `${HOME}/.local/bin` file survives.
- [ ] The test cannot write to the executor's original HOME.
- [ ] Local syntax, format, and Python unit commands exit 0.
- [ ] Ubuntu Server GitHub Actions Bats exits 0.
- [ ] `git diff --name-only` lists only the two in-scope files and plan status/evidence files allowed by the operator.
- [ ] `plans/README.md` status is updated after merge.
- [ ] Before implementation and again before DONE, the executor repeats this
      self-audit and records the result with the PR/CI acceptance evidence.

## STOP conditions

- The Starship installer writes files outside `${BIN_DIR}/starship` that the
  uninstall contract must remove.
- Bats cannot provide a temporary HOME without modifying shared test bootstrap.
- Any verification command touches the real `~/.local/bin`.
- The fix requires recursive removal of a directory.

## Maintenance notes

- Review future uninstall functions for ownership boundaries: remove owned files,
  never a shared parent directory.
- Any Bats test sourcing an installer that uses HOME must set a temporary HOME
  before sourcing it.
- Reviewers must reject recursive deletion whose operand is a shared directory.

## 安全回帰

- Unrelated user files survive install, uninstall, teardown, and failed install.
- Tests never mutate the developer's actual HOME.
- No additional dependency or abstraction is introduced.
