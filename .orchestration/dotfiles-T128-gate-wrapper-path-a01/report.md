# Report: dotfiles-T128-gate-wrapper-path-a01

- **Seat and branch.** `claude-standard-dot-a003` in `.claude/worktrees/worker-c`, on the fresh branch `tools/gate-wrapper-path`. It was cut with `--no-track` from `origin/main` at `c15ba668`, after T704 (#352) merged (validation §1).
- **Task copy: masked, so not byte-identical.**
  - The task file's sha256 `3ccbc7bf…` matches the TASK's `task_sha256`.
  - Its lines 54 to 56 are premise output holding a home path. The repository validator refuses that under `.orchestration/`, and `validate` is a required check on main.
  - So the copy at `.orchestration/dotfiles-T128-gate-wrapper-path-a01/task.md` is the repository masker's output for the dispatched file, byte for byte: sha256 `f88f60865dfe0c1a8e4abccea4ac2aced9df7283bad8e9a40c141f8879a2ac42`. Only those three lines differ, where the home directory reads `~` (validation §1).
  - To check: mask a copy of the dispatched file with `scripts/validate-agent-assets.py --mask-secrets`, then compare.
- **Commits.**
  - `cb1f9cc4`: items 1 to 3.
  - `1483fef2`: two PATH assertions rewritten so a failure prints no environment value.
  - `8d3f6fca`: the task copy and evidence.
  - `eb959ac9`: the path test's temporary root renamed from `root` to `repo`. In pasted failure output, unittest shortens that path to a bare root segment after `[50 chars]`, which the evidence scan reads as root's home directory.
  - `3f0ead31` and `49549520`: the evidence refreshed, with the copy masked. PR #355 opened at `49549520`.
  - `a8a0ffed`: the Bot's P1 fixed. `mise which` runs under `env -i` ("PR #355 and the Bot's one round" below).
  - Then this evidence.
- cost: n/a (the runtime exposes no token or cost figures to the seat).

## Item 1 (`cb1f9cc4`): the gate's PATH is a private bin

The audit of `6847aa9f` rated one P1. The caller's PATH could resolve `gh` through a mise shim, and the gate starts `gh` with the review worktree (the PR head) as its cwd, where a PR-owned `mise.toml` picks the binary.

The steps in `scripts/orchestrator/orch-gate.sh`, after `uv python find` and the clean check of the review worktree:

1. **The EXIT trap is set first.** It removes `${bin}` when set, then cleans and restores the review worktree as before. It stays an inline string; a trap-only function would draw shellcheck SC2329. The string spans two lines, to keep the 120-column width.
2. **The private directory is created:** `bin="$(mktemp -d "${TMPDIR:-/tmp}/orch-gate.XXXXXX")"`.
3. **Each name in `gh git` is resolved in the trusted root** (the cwd is `${root}`) with `found="$(env -i PATH="${PATH}" HOME="${HOME}" mise which "${name}" 2> /dev/null || command -v "${name}")"`. The `env -i` came in `a8a0ffed`.
4. **The answer is checked.** orch-gate.sh refuses with exit 2 unless the answer is absolute and not under a `shims` directory. That covers an empty answer too.
5. **The answer is linked** as `${bin}/${name}`.
6. **Only then is the head checked out.**
7. **The `env -i` line passes `PATH="${bin}"`.** Everything else on that line is unchanged.

Other details:

- **Comments.** One comment names the audit finding, and one names the Bot's thread. The shdoc header now describes the private PATH and the trap's removal of it.
- **The list of names.** The pasted grep (validation §2) finds only `gh` and `git`. The collector starts as `sys.executable`, the pinned interpreter given by an absolute path. The list stays `gh git`.
- **The resolution expression matches the task's rule** in every case:
  - **mise is on PATH and knows the name.** Both use `mise which`.
  - **`command -v` lies under `shims` and mise cannot answer.** The rule's empty `mise which` result and this expression's shims path are both refused.
  - **Otherwise.** Both use `command -v`.
  - So the expression calls `mise which` once per name, with no separate test of `command -v`.
- **The absolute-path check** (`== /*`) refuses both an empty result and a relative one. A relative `command -v` answer would make a link that resolves relative to the private directory.

### Deviation: `mktemp` with an explicit template

The task wrote `bin="$(mktemp -d)"`. On this macOS, `mktemp -d` without a template ignores `TMPDIR` and writes under `/var/folders/…/T`. The Claude sandbox denies that path, so every orch-gate test failed there (validation §3). The explicit template `${TMPDIR:-/tmp}/orch-gate.XXXXXX` honours `TMPDIR` on BSD and GNU alike. It also lets an orchestrator run the wrapper sandboxed up to its `gh` step. `test_orch_gate_removes_the_private_bin_on_exit` asserts that the directory lies under the caller's `TMPDIR`.

### On this host (validation §3)

- **`gh`:** `~/.local/share/mise/installs/github-cli-cli/latest/bin/gh`, via `mise which`.
- **`git`:** `/opt/homebrew/bin/git`, via `command -v`, because `mise which git` fails.
- **`gh` authenticates** under `env -i PATH=<private> HOME`: `gh repo view` gives `mryfmo/dotfiles` with rc 0. `git` runs too.

## Item 2: `tests/unit/test_orch_gate_path.py` (new)

orch-gate.sh runs from its copy in a temporary root, with the stubs first on PATH.

- **The stubs.**
  - Every stub has the shebang `#!/bin/bash`.
  - Every stub appends one line `<name> <argv> <cwd>` to a shared log. It records with `printf` and `pwd -P` (builtins), `/usr/bin/env` and `/usr/bin/readlink`, and runs nothing else.
  - **`mise`** answers `<temp>/installs/<name>` for `mise which <name>`. It answers `<temp>/payload/<name>` if it sees a `MISE_CONFIG_FILE` or `MISE_TRUSTED_CONFIG_PATHS`, and every run exports both.
  - **`git`** answers `rev-parse --show-toplevel` with the root and `rev-parse HEAD` with a fixed head, and succeeds silently otherwise.
  - **`gh`** only logs.
  - **`uv`** answers the gate stub's path. The task's list omits `uv`, but orch-gate.sh runs `uv python find`, so the module stubs it too.
  - **The gate stub** records its environment and, while it runs, each PATH entry with its link target. The trap removes the directory before the test reads.
- **`test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries`** asserts:
  - the gate's `PATH` is one entry, and it is neither a caller PATH entry nor the stub directory. The test compares the intersection only, so a failure prints no caller PATH;
  - that entry holds exactly `gh` and `git`, each a symlink to the path that the stub `mise which` answered, not the stub `gh` on the caller's PATH;
  - the log's `mise which gh` and `mise which git` lines carry the trusted root as cwd;
  - both lines come before the stub git's `checkout -q --detach <head>`.
- **`test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory`** has two subtests: `mise which` answers `<temp>/mise/shims/gh`, and `mise which` answers nothing. Each asserts:
  - exit 2 and the refusal on stderr;
  - no log line carries the head, so there was no head checkout;
  - the review worktree directory is still empty;
  - the gate never ran.
- **`test_orch_gate_removes_the_private_bin_on_exit`** asserts two things. After a passing run, the gate's PATH was a directory under the caller's `TMPDIR`, and `TMPDIR` is empty again. After a shims refusal, `TMPDIR` is empty as well.

## Item 3: `tests/unit/test_orchestrator_tools.py`, three edits

1. **The shebangs.** The `uv` and `gate-python` stubs, the two stub interpreters built from `RUN`, become `#!/bin/bash`.
2. **The shared body `RUN`.** It records with `/usr/bin/env` and `/bin/cat`. The two lines are re-split to stay within 120 columns.
3. **`test_orch_gate_runs_the_gate_under_an_explicit_environment`.**
   - The test now expects the gate's `PATH` to be one entry that holds exactly `gh` and `git`.
   - `HOME`, `PYTHONSAFEPATH` and `AGENT_REVIEWED` keep their checks.
   - The private directory is gone when the test reads it. So inside this test the gate stub gets one more line, which lists `"$PATH"/*` while it runs.

Nothing else in the module changes. T704's `test_orch_audit_runs_the_ledger_check_by_default_and_refuses_a_gap` is untouched. The module does not stub `mise`:

- **On this host,** the real `mise which gh` answers from the temporary repository.
- **On a CI runner where mise does not know `gh`,** `command -v gh` finds the module's stub.

Either way the test sees two links.

## Proofs and size

- **Tests.** 43 tests across both modules are green on `a8a0ffed`, and shellcheck, shfmt and ruff are clean (validation §4).
- **Mutation proofs.** 8 mutants of `orch-gate.sh` at `a8a0ffed`, all killed (validation §5):
  - M1, the caller's PATH;
  - M2, the head checked out before the resolution;
  - M3, no shims check;
  - M4, no empty-or-relative check;
  - M5, a trap that keeps the directory;
  - M6, `command -v` only;
  - M7, `mise which` run from the review worktree;
  - M8, `mise which` run with this shell's environment.
- **Caps.** 27 changed lines outside `tests/` (of 200), 129 added under `tests/` (of 1000), and 3 files outside `.orchestration` (validation §6).

## Threat table

| Row | Where it is closed or bounded |
|---|---|
| behaviour one, the private PATH | `test_orch_gate_runs_the_gate_with_a_private_path_of_resolved_binaries`; M1, M2, M6, M7 and M8 die there |
| behaviour two, the shims or empty refusal | `test_orch_gate_refuses_a_binary_resolved_under_a_shims_directory`; M3 and M4 die there |
| behaviour three, the removal on every exit | `test_orch_gate_removes_the_private_bin_on_exit`; M5 dies there |
| item 3's three edits | the diff of `tests/unit/test_orchestrator_tools.py` against `origin/main`: 13 added and 6 deleted lines, all in the three places |
| the new module's stubs | they record names and paths and run nothing else (item 2 above) |
| the task copy | not byte-identical: the masker's output for the dispatched `3ccbc7bf…`, sha256 `f88f6086…`, differing on lines 54 to 56 only (validation §1) |
| evidence records | this directory; the sandbox record lists every permission-gated command |

## Notes for the orchestrator

- **The main-checkout task file.** `.orchestration/tasks/dotfiles-T128-gate-wrapper-path-a01.md` is untracked there. The same validator refuses it at the next boundary commit, for the same three lines. Masking it with the same masker yields this branch copy byte for byte.
- **The repository validator passes on this branch** (validation §7).
- **The wrapper's own commands.** orch-gate.sh itself still runs `git`, `uv`, `jq` and `mise` by name through the caller's PATH. The trap's `git` does too. They run with the trusted root as cwd (`git -C <review>` changes git's repository, not the process cwd). Item 1 covers the gate and the processes it starts, so these are unchanged.
- **HOME still passes.** gh reads its configuration and keyring entry under the orchestrator's HOME.
- **A mise-managed git** on another host would resolve through `mise which` the same way.
- **The Understand-Anything stale-graph hook** did not fire in this task.

## CompactionDB

The main-checkout `memory add` runs after CI, with the masked main-checkout copy. The exact command and its output go into the main-checkout copy of this report.

- [memory:decision] orch-gate.sh gives the integration gate a PATH of one private directory holding links to `gh` and `git`. Each is resolved in the trusted root before the review worktree is entered: `mise which` under `env -i PATH HOME`, so no caller `MISE_*` override steers it, else `command -v`. A path under a `shims` directory, an empty answer or a relative one is refused with exit 2. The EXIT trap removes the directory. A mise shim run from the PR head can no longer choose the binary that runs with the orchestrator's credentials (the audit of 6847aa9f, P1).
- [memory:failure] On macOS, `mktemp -d` without a template ignores `TMPDIR`, and the Claude sandbox denies the default `/var/folders/…/T`. Use `mktemp -d "${TMPDIR:-/tmp}/<name>.XXXXXX"`.

## PR #355 and the Bot's one round

- **The PR.** PR #355 opened as a draft at `49549520`, and was marked ready at 07:20:03Z.
- **CI on `49549520`.** Every check passed, the required ones included (validation §8). `mergeStateStatus` is `BEHIND`, because main moved after `c15ba668`.
- **The Bot.** The Code Review and the Security Review both finished at 07:23Z. Review `5514396696` has one inline comment and no finding in its body. Issue comment `6163096917` is the Bot's status summary, not a finding.

| Thread | Priority | Finding | Disposition |
|---|---|---|---|
| 4267889542 (`orch-gate.sh:68`) | P1 | `mise which` inherits the caller's `MISE_CONFIG_FILE` and `MISE_TRUSTED_CONFIG_PATHS`, which can make it answer an arbitrary absolute path outside `shims` | `fixed:a8a0ffed` |

- **Reproduced first.** A caller's `MISE_CONFIG_FILE` named a trusted configuration with `"github:cli/cli" = "path:<D>/payload"`, and `mise which gh` answered `<D>/payload/bin/gh`. Under `env -i PATH HOME`, it answered the installed gh (validation §8).
- **The fix.** The resolution runs `env -i PATH="${PATH}" HOME="${HOME}" mise which`. Every run of the path test exports both overrides, and the stub mise answers a payload path when it sees either one. The test still requires links to the installed binaries. M8, without the `env -i`, is killed.
- **Fallback.** A host whose mise needs a `MISE_*` or `XDG_*` variable to find its installs gets no `mise which` answer. Then `command -v` decides, and a shim is refused (fail closed).
- **No further round.** This is the task's one fix round. The Bot reviews only at PR open, so `a8a0ffed` gets no Bot review. CI on it is in the main-checkout copy and the RESULT.
- **Left to the orchestrator.** I resolved no thread.
