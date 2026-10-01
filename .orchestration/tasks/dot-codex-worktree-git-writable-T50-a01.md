# AGMSG-TASK dot-codex-worktree-git-writable-T50-a01

Drafted 2026-10-02 from the T40 blocker (PONG 651); dispatched after T46 (PR
#220) merged as bb3370a. Worker-c, branch `fix/codex-worktree-git-writable`
from `origin/main` (bb3370a or later); the merged T46 branch
`fix/orchestrator-linkage-evidence` stays as a local branch, nothing to
clean. Verify the dispatched task_rev sha256 against this file; else stop and
PONG blocked.

## Objective

A Codex worker seated by `herdr-agents` in a nested worktree
(`.claude/worktrees/<name>`) runs with `sandbox_mode = workspace-write`, whose
writable root is the worktree. The worktree's git metadata lives outside it:
`git rev-parse --git-path index` → `<main>/.git/worktrees/<name>/index`,
objects and refs under `<main>/.git/`. Every `git add/commit/fetch/rebase/push`
therefore fails with `Unable to create <main>/.git/worktrees/<name>/index.lock:
Read-only file system` (T40, worker-sec, 2026-10-01T17:54Z) and the worker can
only escalate. Under the regime, agent-to-agent approval is forbidden and only
the human operator answers a permission prompt, so each Codex commit currently
needs the operator at the pane (operator decision 2026-10-02 for T40).

Make the sandbox grant exactly the git metadata a worktree needs, nothing more:

- writable: `<common>/objects`, `<common>/refs`, `<common>/logs`,
  `<common>/worktrees/<name>` (per-worktree `index`, `HEAD`, `ORIG_HEAD`,
  `FETCH_HEAD`, `logs/HEAD`, `rebase-merge`), where `<common>` is
  `git -C <worktree> rev-parse --git-common-dir`;
- still denied: `<common>/config`, `<common>/hooks`, `<common>/info`,
  `<common>/HEAD` (the main checkout's), `<common>/packed-refs` unless a probe
  shows a required operation needs it (then say which, and why it is safe);
- `approval_policy`, `sandbox_mode`, and `network_access` unchanged.

Verify empirically with Codex's own sandbox from a worktree cwd (`codex
sandbox -- sh -c '…'`): one probe per path above (touch + remove), then a real
`git commit --allow-empty`, `git fetch origin`, `git rebase origin/main`, and a
`git push --dry-run` on a scratch branch of a scratch worktree, all inside the
sandbox, before and after the change; paste every probe verbatim into the
validation file. Do not reason from memory about what Codex marks read-only.

## Deliverables

1. The grant mechanism. Two candidates; choose the one that passes the probes
   with the smaller surface and say why the other was rejected:
   - **Launcher:** `herdr-agents` computes the four paths from the worker's
     worktree when it seats a `codex` worker (`--add-worker` and the pair
     worker) and passes them as
     `-c sandbox_workspace_write.writable_roots=[…]` in the spawn options file
     (profile launch args) — the manifest's `writable_roots` (agmsg store
     directories) must remain included, since `-c` replaces the array.
   - **Project config:** a tracked `.codex/config.toml` (Codex loads
     project-scoped config for trusted projects; it cannot override profile
     selection or auth) with the same `[sandbox_workspace_write]` list, only
     if paths can be expressed without hard-coding this machine's `$HOME`
     and the worktree is a trusted project for Codex.
2. `tests/unit/test_herdr_agents.py`: the spawn options file for a codex
   worker contains the four computed paths plus the manifest roots (launcher
   path), or a validate-agent-assets check for the project config (config
   path). Negative check against the parent commit.
3. Docs: README `herdr-agents` section (one paragraph: what is granted and
   what stays denied, and that Codex escalation prompts are answered only by
   the operator); `home/dot_config/claude/rules/agmsg-orchestration.md` and
   the agmsg-orchestration SKILL identity/delivery section (one bullet each);
   mirror in `home/dot_config/codex/AGENTS.md` if that file carries the rule.
4. `[memory:decision]` T50: Codex workers in nested worktrees get
   `<common>/{objects,refs,logs,worktrees/<name>}` as writable roots from the
   launcher (or project config), never `.git` itself, `config`, `hooks`, or
   `info`; escalation prompts are answered only by the human operator
   (operator 2026-10-02).

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`, `tests/unit/test_herdr_agents.py`
- `README.md`, `home/dot_config/claude/rules/agmsg-orchestration.md`,
  `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/codex/AGENTS.md`
- Only for the project-config candidate: `.codex/config.toml`,
  `scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-codex-worktree-git-writable-T50-a01.md`
- `.agents/worklog/codex/**` waived.

## Forbidden actions

Changing `approval_policy`, `sandbox_mode`, `network_access`, or any model /
profile value; making `<common>` itself, `config`, `hooks`, or `info`
writable; `danger-full-access`; touching `.claude/worktrees/worker-sec` or
its branch; `.orchestration/acceptance/**`; merge; force-push;
`--delete-branch`; local `bats`; `make update`/`upgrade`.

## Validation (verbatim output)

`make render-check`, `make unit-test`, `make validate-agent-assets`, `shfmt -d`
and `shellcheck` on the launcher, the `codex sandbox` probes and git
operations above (before and after), `gh pr view <n> --json
url,headRefOid,mergeStateStatus`, `gh pr checks <n>`, and the CompactionDB
`memory add --kind decision --scope project` command with its output.

## Completion

English PR to `main`, CI green on Linux and macOS, artifacts at the expected
paths, `AGMSG-RESULT v1` with `cost:` in the report. max_turns=40.

## Orchestrator amendment r2 (2026-10-02; dispatched as AGMSG-ACCEPTANCE status=revise)

Pre-screen audit of 5952ab8 is **incorrect** with one P2 (high confidence),
reproduced by the auditor against the commit's parser:
`codex_worktree_writable_roots` reads `writable_roots` from
`~/.codex/config.toml` with an awk line matcher. An indented key, a
commented-out section header, or a multi-line array yields an empty
`configured`, and the `-c` override then **replaces** the configured roots
with the git paths alone — the worker loses write access to the agmsg store
(`db`, `teams`, `run`, `ext-tools`) and cannot send messages. The generator
renders the file single-line today, so the live behaviour is right, but the
grant must never be able to drop configured roots.

Fix in one commit on 5952ab8:

1. Parse the TOML properly: `python3 -c 'import tomllib, json, sys; …'`
   (stdlib, 3.11+) reading the file and emitting
   `sandbox_workspace_write.writable_roots` as JSON, or an explicit failure.
   Keep the `#`-free check for the spawn options dialect.
2. Fail closed on any doubt: if the file exists but cannot be parsed, or the
   key is present and not a list of strings, print the stderr line and emit
   **no** override (the worker keeps its configured roots and falls back to
   operator-approved escalation). Only a parseable file with a string list
   (or a missing key / missing file, which `-c` cannot regress) produces the
   override.
3. Tests: (a) indented key / multi-line array → the override still carries
   the configured roots first; (b) unparseable file → no `--config` entry
   and the stderr line; (c) keep the existing happy-path tests green.
   Negative check against 5952ab8 for (a) and (b).
4. Codex GitHub review of 5952ab8 (two P2s; the first is the same parser
   defect seen from the other side: a multi-line array makes `jq` reject
   the fragment and the grant is silently skipped — covered by items 1–3).
   The second: in a shallow clone, `git fetch --deepen/--unshallow` writes
   `<common>/shallow.lock` and `<common>/shallow`, which stay read-only
   because the common dir is not granted. Do not widen the grant. Detect it
   (`git -C <worktree> rev-parse --is-shallow-repository` = true) and print
   one stderr line saying shallow metadata is not granted and those fetches
   need an operator-approved escalation; state the same in the README
   paragraph and the launcher shdoc. One test: a fake `git` answering
   `true` → the stderr line, override otherwise unchanged.

Validation as before (render-check, unit-test, validate, shfmt, shellcheck,
the `codex sandbox` probes already recorded need no rerun unless the emitted
override text changes); push without `-u`; RESULT when CI is green on both
OSes.
