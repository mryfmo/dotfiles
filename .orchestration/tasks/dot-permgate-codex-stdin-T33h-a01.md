# AGMSG-TASK dot-permgate-codex-stdin-T33h-a01

## Objective

Product hardening carried over from T33d (`.orchestration/acceptance/dot-permgate-bench-flake-T33d-a01.md`):
`home/dot_local/bin/common/executable_permgate` `classify()` runs the codex
classifier with the prompt as the last argv element and NO `stdin` argument
(second `subprocess.run`, around line 393), so the child inherits the hook's
stdin. The claude branch passes `input=prompt` (stdin reaches EOF). If the
codex CLI ever reads an inherited open stdin, a PermissionRequest hook would
hang until `timeout_seconds` and fail closed as `timeout`. Make the classifier
independent of the caller's stdin.

Deliver:

1. `executable_permgate`: add `stdin=subprocess.DEVNULL` to the codex
   `subprocess.run` in `classify()` (the branch that writes `--output-last-message`).
   Do not change the claude branch (`input=prompt` already closes stdin) and do
   not change timeouts, prompts, or the policy.
2. Tests (`tests/unit/test_permgate.py`, mutation baseline against the unmodified
   script): a fake codex that ALSO reads stdin (like the pre-T33d fixture) must
   classify successfully while the test runner's stdin is an open pipe — reuse
   the T33d reproduction (`sleep 20 | python3 -m unittest … -k <case>`) as the
   proof in the validation file: FAIL on the old script, OK on the new one. Keep
   the T33d argv-prompt fixture as the default fake.
3. `bench` uses the same `classify()`; no separate change unless the code path
   differs — say so in the report.

[memory:decision] T33h: permgate runs the codex classifier with
`stdin=subprocess.DEVNULL` so hook classification never depends on the caller's
stdin (operator 2026-09-28, from the T33d diagnosis).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`; `git switch -c fix/permgate-codex-stdin origin/main`.
  Verify the dispatched task_rev sha256 against this file on your base, else
  stop and PONG. If the worktree has uncommitted files, stop and PONG. After
  switching, you may delete your previous local branch `fix/ua-core-build-shim`
  (merged as 2b30a21).

## Allowed files

- `home/dot_local/bin/common/executable_permgate`
- `tests/unit/test_permgate.py`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-permgate-codex-stdin-T33h-a01.md` (main checkout)

## Forbidden actions

- Any change to the permgate policy, hooks configs, model_profiles, or other
  scripts; running real `codex`/`claude`; merging; force push; local bats;
  `make apply`/`chezmoi apply`; writes outside the worktree except the listed
  `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
sleep 20 | python3 -m unittest tests.unit.test_permgate -k <new case>   (before and after)
git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the mutation baseline) and the PR number/head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `inbox.sh dotfiles claude-standard-dot-a005` at each milestone.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
