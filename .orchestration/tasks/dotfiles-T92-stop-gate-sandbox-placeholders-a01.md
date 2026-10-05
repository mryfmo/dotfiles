# AGMSG-TASK dotfiles-T92-stop-gate-sandbox-placeholders-a01

Drafted 2026-10-04 by the orchestrator seat; follow-up to T65 (PR #237, merged 06875e4e). Dispatched to `claude-standard-dot-a007` (worker-e), which wrote the gate.

## Objective

The merged Stop hook blocks the orchestrator seat on 19 "uncommitted changes" that do not exist: `.bash_profile`, `.bashrc`, `.claude/agents`, `.claude/commands`, `.claude/launch.json`, `.claude/loop.md`, `.claude/output-styles`, `.claude/routines`, `.claude/skills`, `.claude/workflows`, `.gitconfig`, `.gitmodules`, `.idea`, `.mcp.json`, `.profile`, `.ripgreprc`, `.vscode`, `.zprofile`, `.zshrc`. Evidence from the orchestrator (2026-10-04 05:40Z, main checkout):

- outside the sandbox: `ls -la .zshrc .claude/agents` → `No such file or directory`; `git status --porcelain --untracked-files=all` lists nothing outside `.orchestration/` and `.agents/`;
- inside the Claude Code sandbox (bubblewrap): the same paths are 0-byte, mode 0444 regular files owned by the user, created at the command's start (`stat` → 通常の空ファイル 444), `mount` shows 52 bind mounts under the repository root, and `git status` lists all 19 as `??`.

These are the sandbox's placeholders for its protected paths (`denyWithinAllow` for the project directory and the user's dotfiles). The Stop hook evidently runs inside that mount namespace, so `git status` reports them as untracked and the gate blocks every stop.

1. Skip an untracked entry that is a sandbox placeholder. Criterion: the path is a mount point in the hook's own mount namespace (`mountpoint -q -- "$path"`, util-linux; fall back to matching the path against `/proc/self/mountinfo` field 5 when `mountpoint` is absent, as on macOS where the sandbox differs and no placeholder appears). A real untracked file is never a mount point. Count the skipped entries and print one stderr note only when the gate blocks for another reason (`sandbox placeholders ignored: <n>`), so a clean stop stays silent.
2. Tests: a fake `mountpoint` on PATH that reports the placeholder paths as mount points → the orchestrator seat passes with those entries present and still blocks on a real untracked source file in the same tree; without the fake (no `mountpoint`), the `/proc/self/mountinfo` fallback is exercised with a fixture file through an env override such as `AGENT_STOP_GATE_MOUNTINFO` (test-only, documented in the header).
3. Keep every other behaviour; `shellcheck`/`shfmt` clean; header `@description` updated in one sentence.

Forbidden: `.claude/settings.json`; any other file.

[memory:decision] dotfiles-T92 (orchestrator 2026-10-04): the agent stop gate ignores untracked paths that are mount points in its own namespace, because the Claude Code sandbox bind-mounts 0-byte placeholders for protected paths into the repository root and the Stop hook runs inside that namespace.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c fix/stop-gate-sandbox-placeholders origin/main` (06875e4e or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `scripts/agent-stop-gate.sh`, `tests/unit/test_agent_stop_gate.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T92-stop-gate-sandbox-placeholders-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
bash -n scripts/agent-stop-gate.sh && shellcheck scripts/agent-stop-gate.sh && shfmt -d scripts/agent-stop-gate.sh
uv run python -m unittest tests.unit.test_agent_stop_gate 2>&1 | tail -3
make unit-test
make validate-agent-assets
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

Inside your sandboxed Bash, also paste: `ls -la .zshrc 2>&1; mountpoint .zshrc 2>&1; echo '{"stop_hook_active":false,"cwd":"'"$PWD"'"}' | scripts/agent-stop-gate.sh; echo rc=$?` from the worktree (the placeholders exist there too) before and after the change.

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if Plan Mode was used.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T92` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=25.

## Revise round 1 (orchestrator, 2026-10-04 08:40Z) — task-level audit of bbd3d3fb is `incorrect`

1. **P2, a user's empty read-only bind mount of another file is skipped.** mountinfo field 4 (root) separates the cases: a sandbox placeholder is a self-bind, so its root equals the mount point path within the same filesystem, while a bind of another file (an untracked `.env` mounted from elsewhere) has a different root. Require root == mount point (both in mountinfo's escaping; for a self-bind of a file under the home filesystem the root is the same absolute path) in addition to the existing predicate; test with a fixture whose root differs. This supersedes the not-applicable on Bot thread 4176428488; the orchestrator re-replies `fixed:<sha>`.
2. **P2, evidence: regression/mutation results, the predicate count and the benchmark are summaries.** Paste the executable commands and their raw output (unittest output for each "fails on the parent" claim, the live 19/19 predicate loop, the 600-file timing).
3. **P3, evidence: the `--jq '.mergeable_state'` entry shows an extra head sha the command cannot print.** Record the actual commands and outputs.

One commit for item 1 (code + test), artifact edits for items 2-3, `gh pr update-branch 248` if `main` moved, CI, Bot (paginated listing), RESULT naming every thread. Standing directive applies: do not stop to ask; permission prompts are approved by the operator.

## Revise round 2 (orchestrator, 2026-10-04 10:05Z) — task-level audit of 153a647d is `incorrect`

1. **P2, `$4 == $5` fails when `/home` is its own filesystem.** mountinfo's root (field 4) is relative to the source filesystem's root, so a self-bind of `~/.../.zshrc` shows `root=/moriya/.../.zshrc` with `mount point=~/.../.zshrc`, and the placeholder is reported again on that layout. Compare in one coordinate system: a self-bind is one whose mount point ends with its root (`substr($5, length($5) - length($4) + 1) == $4`, with `$4 == "/"` handled as a whole-filesystem bind, not a placeholder), or resolve the parent mount's mount point and join. Add a fixture with `/home` as a separate filesystem (root `/moriya/...`) and keep the existing same-filesystem fixture.

One commit; `gh pr update-branch 248` if `main` moved; CI; Bot (paginated listing); RESULT. Standing directive applies.
