# Report: dot-codex-worktree-git-writable-T50-a01

- worker: claude-standard-dot-a005 (claude-code, standard profile), seated in worker-c
- task_rev: c33c0d8cf644ae3180f6df92d2b0e8c327c22e7c7a9c3507b098b457a873da49 (verified with sha256sum of the task file)
- branch: `fix/codex-worktree-git-writable` from `origin/main` bb3370a; one commit, **5952ab8**, pushed without `-u`
- PR: https://github.com/mryfmo/dotfiles/pull/222, head `5952ab8517b3be5f7b97b290cfaf789e3312d572`. CI is in the validation file.
- cost: n/a (no per-task token counter in this session)

## Outcome

`herdr-agents` gives a codex worker in a linked worktree that worktree's git metadata as writable roots:

- **How it is passed:**
  - pair worker: `-c sandbox_workspace_write.writable_roots=[...]` on `herdr agent start`, in every path that uses `start_worker_agent` (full mode, attach repair, `--restart-worker`);
  - `--add-worker`: a `--config` entry in the spawn options file. Upstream `spawn.sh` `%q`-quotes each option token, so the value reaches Codex as one argv word.
- **The list:**
  - the roots configured in `${CODEX_HOME:-~/.codex}/config.toml` first (the four agmsg store directories), because `-c` replaces the array;
  - then `<common>/objects`, `<common>/refs`, `<common>/logs` and the worktree's git dir `<common>/worktrees/<name>`.
- **Where `<common>` comes from:** `git -C <worktree> rev-parse --path-format=absolute --git-common-dir`, and the worktree's own dir from `--git-dir`.
- **Still read-only:** the common dir itself, `config`, `hooks`, `info`, the main checkout's `HEAD`, and `packed-refs`.
- **No override in two cases:**
  - a main checkout or legacy main-path seat, whose git dir is the common dir; a grant there would open `config` and `hooks`;
  - a config whose `writable_roots` cannot be read as a JSON-compatible string array. That case also prints a stderr warning naming the file.

  A root containing `#` is also refused, because the spawn options dialect strips ` #…` as a comment.
- `approval_policy`, `sandbox_mode`, `network_access` and every model or profile value are unchanged.

**Mechanism choice:** the launcher. A tracked `.codex/config.toml` was rejected for two reasons:
- `writable_roots` takes absolute paths (schema `AbsolutePathBuf`), so the file would hard-code this machine's `$HOME`.
- `<common>/worktrees/<name>` differs per worktree, while one tracked file is the same in every worktree.

## Empirical evidence (all verbatim in the validation file)

**Probe setup:** a scratch nested worktree `.claude/worktrees/t50-probe` on the scratch branch `scratch/t50-probe`, one commit behind `origin/main`. The probe script does:
- touch and remove a file in each directory;
- open each file for append without writing, which changes neither content nor mtime;
- `git commit --allow-empty`, `git fetch origin`, a local-path `git fetch <main> main`, `git rebase origin/main`, `git push --dry-run origin`, and a local-path `git push --dry-run`.

**Finding about the prescribed probe:** `codex sandbox -- sh -c '…'` (codex-cli 0.158.0) does not run in the worker's mode.
- Without `-P` it is read-only: even the worktree itself is denied.
- `-C <dir>` requires `--permission-profile`.
- `-P workspace-write` errors: ``default_permissions requires a `[permissions]` table``.
- `-P :workspace` makes the cwd writable but ignores the legacy `sandbox_workspace_write.writable_roots`: the agmsg roots stay denied even with `-c`.

So I used three layers of evidence:
1. **`codex sandbox -P :workspace`** (before): the four git paths, `hooks`, `info`, `.git`, `config`, `HEAD` and `packed-refs` are all read-only. `commit` fails on `index.lock`, both `fetch`es on `FETCH_HEAD`, and `rebase` on `rebase-merge`, all with Read-only file system, which is the T40 failure.
2. **`codex sandbox -P t50`** with an explicit `[permissions.t50]` profile (extends `:workspace`, four `write` entries) in a scratch `CODEX_HOME` copy of the config:
   - the four paths are writable and the other six stay denied;
   - `commit`, local `fetch` and `rebase` succeed. `rebase` prints `Unable to create …/packed-refs.lock` twice and then `Successfully rebased` (exit 0).
3. **`codex doctor --json`** (effective filesystem policy): the legacy `writable_roots` appear as `write` entries. With the launcher-computed `-c` value, the same four agmsg entries plus the four git paths appear. The value the launcher function prints for the scratch worktree is byte-identical to the hand-built override.
4. **Live worker mode**, closing the gap: two disposable `codex exec --profile express --sandbox workspace-write --ephemeral --json` test-subject runs. `--profile express` comes from `MODEL_PROFILE_EXPRESS_CODEX_ARGS`, which the model-selection rule sanctions for throwaway sessions. The command output comes from the harness's `command_execution` events, not from model prose.
   - **before** (no `-c`): exactly layer 1's result.
   - **after** (`-c` = the launcher value): the four paths are writable and `hooks`, `info`, `.git`, `config`, `HEAD` and `packed-refs` stay DENIED. `commit` exit 0, local `fetch` exit 0, `rebase` exit 0 (same `packed-refs.lock` notice); local `push --dry-run` exit 0.
   - **both runs:** `git fetch origin` and `git push --dry-run origin` fail on `Could not resolve host: github.com` (network_access=false, unchanged).

**packed-refs:** not granted. No required operation needs it: `rebase` succeeds and only logs the lock failure. It stays read-only as the task asks.

## Tests

- `test_add_worker_passes_codex_profile_and_sandbox_through_spawn_options` (updated): with a generated-style `~/.codex/config.toml` holding the four agmsg roots, the spawn options file is exactly the profile pairs plus `--config: sandbox_workspace_write.writable_roots=[<agmsg roots>, <common>/objects, <common>/refs, <common>/logs, <common>/worktrees/b2]`, and it names no `/config`, `/hooks`, `/info`, `/HEAD`, `/packed-refs` or bare `.git`.
- `test_full_mode_gives_a_codex_worker_its_worktree_git_metadata_roots` (new): a codex pair worker in the manifest worktree is started with `-- --sandbox workspace-write --profile standard -c sandbox_workspace_write.writable_roots=[…]`.
- `run_helper` now drops `CODEX_HOME`.
- **Negative check against bb3370a:** with the parent `herdr-agents` swapped in and then restored (`cmp` exit 0), both tests **fail**.
- **Other codex start tests:** the exact-match tests (`… --profile standard`) run with no linked worktree, so they are unchanged and green.

**Checks:**
- `make render-check`: exit 0.
- `make unit-test`: 682 tests OK, 1 skipped; exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck` and `shfmt -d` (3.14.1) on the launcher: exit 0.

## Docs

- `README.md` herdr-agents seat section: one paragraph on what is granted, what stays read-only, that network stays off, and that escalation prompts are answered only by the human operator.
- `home/dot_config/claude/rules/agmsg-orchestration.md` and the agmsg-orchestration SKILL "Identity, delivery, and storage" section: one bullet each, after the worktree-seat bullet.
- `home/dot_config/codex/AGENTS.md` does not carry the sandbox or escalation rule (no `sandbox`, `escalat` or operator-approval wording), so nothing is mirrored there.

## CompactionDB

`python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T50: …'` was run in the main checkout. The memory id is **97c86c4c-8646-413a-aa34-bba5c9f0b1f3**; the full command and output are in the validation file.

[memory:decision] T50: Codex workers in nested worktrees get `<common>/{objects,refs,logs,worktrees/<name>}` as writable roots from the launcher, never `.git` itself, `config`, `hooks` or `info`; escalation prompts are answered only by the human operator (operator 2026-10-02).

## Observations for the orchestrator

- **`.git/config.lock`:** the main checkout holds a 0-byte, mode `r--r--r--` `.git/config.lock` dated 2026-10-02 06:26 local (21:26Z), before T50 started. It matches the sandbox phantom-stub pattern. It made `git worktree add -b` fail at the upstream write (the branch was created; the worktree was then added on the existing branch), and `git branch -D` warn `could not lock config file` (no config section existed, so nothing was lost). I did not touch it (standing rule: never remove `.git/*.lock`). Any `git config` write in this repository fails until it is cleared.
- **T45 record:** the kept untracked `.orchestration/sandboxes/dot-plain-start-visibility-T45-a01.md` in worker-c blocked the branch switch, because origin/main now tracks that path. Its bytes are an exact prefix of the committed copy (a5f33ee, `head -c` + `cmp` exit 0), so I moved it, not deleted it, to this session's scratchpad (`…/scratchpad/t50/`).
- **Live confirmation:** the pair worker and `--add-worker` paths are covered by unit tests and the live `codex exec` probe. A real reseat (`herdr-agents --restart-worker` or `--add-worker`) was not run; that is the operator's or orchestrator's call, for example when T40 resumes.

## Effects

Outside the working tree:
- a scratch worktree and local branch `scratch/t50-probe`, both removed (cleanup output pasted);
- no remote branch: both pushes were `--dry-run`;
- two disposable `codex exec --ephemeral` sessions (express profile);
- one CompactionDB decision.

worker-sec and its branch were not touched.

Understand-Anything auto-update hook: hook fired; not acted on (`.ua/**` is not in allowed_files).

## Revision 2 (orchestrator status=revise 22:33:27Z; amendment r2; task_rev 52c0b98f…f55a1 verified)

One commit, **e334af5**, on 5952ab8, pushed without `-u`. There was no force push. PR #222 head: `e334af51ca3c8bb8b742151f73faaa1b2b1439ac`. CI results are in the validation file.

**Fixes:**

1. **Parser** (audit P2, and the first Codex GitHub P2): `codex_worktree_writable_roots` reads the file with python3's `tomllib`. It emits `sandbox_workspace_write.writable_roots` as JSON, or exits non-zero when the value is not a list of strings or the table is malformed. The awk line match is gone. The `#`-free check for the spawn options dialect stays, with its own stderr line.
2. **Fail closed:** when the file exists but cannot be parsed, `tomllib` is missing (python3 older than 3.11), or `writable_roots` is not a list of strings, the launcher prints `cannot read sandbox_workspace_write.writable_roots in <file> as a list of strings (python3 3.11+ tomllib); the codex worker in <worktree> gets no git metadata roots.` and emits **no** override. The worker keeps its configured roots. Only a missing file or a missing key (configured roots empty, which `-c` cannot narrow) or a parseable string list produces the override.
3. **Shallow clones** (second Codex GitHub P2): when `git -C <worktree> rev-parse --is-shallow-repository` prints `true`, the launcher prints `<worktree> is a shallow clone; its shallow metadata (<common>/shallow) is not granted, so git fetch --deepen or --unshallow in the codex worker needs an operator-approved escalation.` The override is otherwise unchanged, and the grant is not widened. The README paragraph and the function's shdoc say the same.

**Tests** (new):
- `test_add_worker_keeps_the_configured_roots_from_an_indented_multi_line_array`: a commented-out `# [sandbox_workspace_write]` line, then the real header, an indented key, and a multi-line array with a trailing comma. The override still carries the four configured roots first.
- `test_add_worker_emits_no_override_for_an_unparseable_codex_config`: the options file has no `--config` entry, and the stderr line appears.
- `test_add_worker_reports_shallow_metadata_as_not_granted`: a fake `git` on PATH answers `true` to `--is-shallow-repository` and delegates everything else to the real git. The stderr line appears and the override is unchanged.
- **Fixture change:** `write_codex_config_roots` gives the restricted test PATH this interpreter as `python3`, because a runner's `/usr/bin/python3` may predate `tomllib`. The existing happy-path tests stay green.

**Negative check against 5952ab8:** with its `herdr-agents` swapped in and then restored (`cmp` exit 0), all three new tests **fail**.

**Override text unchanged:** for the generated single-line config, the new parser emits exactly the bytes the 5952ab8 parser did (`cmp` exit 0, pasted). So the recorded `codex sandbox`, `codex doctor` and live `codex exec` probes still apply and were not rerun.

**Checks at e334af5:**
- `make render-check`: exit 0.
- `make unit-test`: 685 tests OK, 1 skipped; exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck` and `shfmt -d` (3.14.1) on the launcher: exit 0.

**Behaviour change to note:** on a machine whose `python3` is older than 3.11, an existing `~/.codex/config.toml` now means no git metadata roots, with a stderr line. This is fail-closed by design. The worker then falls back to operator-approved escalation, as before T50.

**CompactionDB:** the T50 memory (97c86c4c-8646-413a-aa34-bba5c9f0b1f3) stands. The parser and fail-closed rule are in the learning file (item 5).

cost: n/a
