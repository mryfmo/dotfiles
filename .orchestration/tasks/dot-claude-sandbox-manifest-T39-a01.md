# AGMSG-TASK dot-claude-sandbox-manifest-T39-a01

## Objective

Revive PR #179 (`feat/claude-sandbox-manifest`, head b729f54, merge-base
f2288d6e) minus what `main` already covers, and land it on today's `main`.
Main's T30 (#192, ad5f95d) ships the `bwrap-userns` AppArmor profile
(`install/ubuntu/common/apparmor_userns.sh`, `apparmor/bwrap-userns`,
`run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl`, `check_apparmor_userns`,
`tests/unit/test_apparmor_userns.py`). PR #179's own AppArmor part
(`install/ubuntu/common/bwrap_apparmor.sh`, `run_once_before_51-setup-bwrap-apparmor.sh.tmpl`,
`tests/install/ubuntu/common/bwrap_apparmor.bats`, the `/etc/apparmor.d/bwrap`
profile, `BWRAP_APPARMOR_*` env vars) is superseded and is DROPPED; a second
profile on `/usr/bin/bwrap` would cancel the first. Its bats failure on the PR
head (fake `sudo` logging to stdout that the script pipes to /dev/null) goes
away with it.

Keep and carry (operator 2026-09-29):

1. **Sandbox from the manifest.** `home/dot_agents/agent-config.yaml`
   `claude.sandbox` (PR L171-191), `render_claude_sandbox()` in
   `scripts/generate-agent-configs.py`, `validate_claude_sandbox()` in
   `scripts/validate-agent-assets.py`, the three tests in
   `tests/unit/test_validate_agent_assets.py`, parity item 9 in
   `home/dot_agents/README.md`. Resolve the header-comment conflict in
   agent-config.yaml by keeping main's lines and appending the PR's
   continuation ("the Claude sandbox allowWrite list is rendered from the same
   entries"). Regenerate `home/.chezmoitemplates/claude-settings-managed.json`
   with `python3 scripts/generate-agent-configs.py` (never hand-edit): after
   the merge `filesystem.allowWrite` must list all FOUR Codex writable roots
   (main added `agmsg/ext-tools`), and `--check` must pass.
2. **Operator-approved default values** (each is a permission-policy change;
   do not add or alter any other key):
   - `enabled: true`
   - `failIfUnavailable: false` (changed from the PR's `true`: two-stage
     rollout; a later task flips it after live E2E)
   - `autoAllowBashIfSandboxed: true`, `allowUnsandboxedCommands: true`,
     `excludedCommands: []` (as in the PR)
   - `filesystem.allowWrite`: rendered from `codex.sandbox_workspace_write.writable_roots`
   - `network.allowedDomains`: the PR's five GitHub hosts
   - NEW `network.allowUnixSockets`: the herdr socket
     (`~/.config/herdr/herdr.sock`) and the Claude messaging socket. Before
     adding it, read the current Claude Code sandbox settings reference
     (https://code.claude.com/docs/en/sandboxing and
     https://code.claude.com/docs/en/settings, read-only) and paste the
     exact key name, value type, and whether `~`/env expansion is supported
     into the validation file. If the documented schema cannot express the
     messaging socket (its path comes from `CLAUDE_CODE_MESSAGING_SOCKET` at
     runtime), add only the herdr socket and record the gap in the report.
     Extend `validate_claude_sandbox` to require every `allowUnixSockets`
     entry to be an absolute or `~/`-prefixed path with no globs, and add
     one test.
3. **Prerequisite packages.** `install/ubuntu/common/dependencies.sh` adds
   `bubblewrap` and `socat`; `tests/install/ubuntu/common/dependencies.bats`
   count becomes 18 (main is at 16 with mosh).
4. **Doctor.** In `scripts/check-tools.sh` keep only a `check_claude_sandbox`
   that reports `bwrap` and `socat` presence on PATH (WARN when missing, no
   sysctl or profile logic; `check_apparmor_userns` already covers that) under
   a "Claude Code sandbox" section placed after main's "AppArmor" section;
   `tests/unit/test_runtime_health.py` gets the matching presence test only,
   keeping main's `APPARMOR_USERNS_SYSCTL` fixture unchanged.
5. **README.** Carry the "### Claude Code sandbox" section; replace its
   `/etc/apparmor.d/bwrap` paragraph (PR L301-307) with a pointer to main's
   bwrap-userns paragraph (README.md:272-280). State the operator-visible
   effect in one paragraph: after the next `make update`, Claude Code Bash
   runs confined to the cwd, the session TMPDIR and `allowWrite`; hosts other
   than the listed GitHub domains prompt; commands that fail inside the
   sandbox may be retried unsandboxed after a normal prompt; missing
   bwrap/socat only warns while `failIfUnavailable` is false.

Build the branch as `git switch -c feat/claude-sandbox-manifest-r2 origin/main`
and `git merge --squash origin/pr/179` (fetch
`refs/pull/179/head:refs/remotes/origin/pr/179` first), then remove the
dropped files and apply the changes above; two commits: the carry, then the
reduction/defaults. Do NOT push to `feat/claude-sandbox-manifest` or close
#179; the orchestrator closes it at acceptance.

[memory:decision] T39: the Claude Code sandbox is rendered from
`claude.sandbox` in agent-config.yaml (enabled, failIfUnavailable=false for
the first stage, autoAllowBashIfSandboxed, allowUnsandboxedCommands,
allowWrite mirrored from the Codex writable roots, GitHub-only
allowedDomains, herdr/Claude unix sockets allowed) with bubblewrap+socat as
Ubuntu prerequisites and a presence-only doctor check; PR #179's own
`/etc/apparmor.d/bwrap` profile is dropped in favour of main's bwrap-userns
(T30). Flipping failIfUnavailable to true waits for live E2E (operator
2026-09-29).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- Base `origin/main`; verify the dispatched task_rev sha256 against this file
  on your base, else stop and PONG. If the worktree has uncommitted files or a
  branch other than the task branch is checked out with local commits, stop
  and PONG.

## Allowed files

- `home/dot_agents/agent-config.yaml`, `scripts/generate-agent-configs.py`, `home/.chezmoitemplates/claude-settings-managed.json` (generated only), `scripts/validate-agent-assets.py`, `tests/unit/test_validate_agent_assets.py`, `home/dot_agents/README.md`
- `install/ubuntu/common/dependencies.sh`, `tests/install/ubuntu/common/dependencies.bats`
- `scripts/check-tools.sh`, `tests/unit/test_runtime_health.py`
- `README.md` (the Claude Code sandbox section only)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-claude-sandbox-manifest-T39-a01.md` (main checkout), `.agents/worklog/**`

## Forbidden actions

- Creating or keeping `install/ubuntu/common/bwrap_apparmor.sh`, `home/.chezmoiscripts/ubuntu/run_once_before_51-setup-bwrap-apparmor.sh.tmpl`, `tests/install/ubuntu/common/bwrap_apparmor.bats`, any `/etc/apparmor.d/bwrap` profile, or `BWRAP_APPARMOR_*` variables.
- Touching main's AppArmor files (`apparmor_userns.sh`, `apparmor/bwrap-userns`, `run_onchange_after_07-*`, `test_apparmor_userns.py`, `check_apparmor_userns`).
- Any sandbox key or value not listed above; `home/dot_claude/settings*` outside the generated template; `.claude/hooks/**`; permgate; `.ua/**`; `.orchestration/tasks/**`.
- `sudo`, `make update`/`upgrade`, `chezmoi apply`, `mise install`; local bats; force push; pushing to `feat/claude-sandbox-manifest`; merging or closing PRs; posting bot review requests; writes outside the worktree except the listed paths.

## Validation commands (paste verbatim output)

```
git merge-base --is-ancestor origin/main HEAD && echo base-ok
git diff --stat origin/main
git ls-files install/ubuntu/common/bwrap_apparmor.sh home/.chezmoiscripts/ubuntu/run_once_before_51-setup-bwrap-apparmor.sh.tmpl tests/install/ubuntu/common/bwrap_apparmor.bats ; echo "dropped-files listed above must be empty"
python3 scripts/generate-agent-configs.py --check
python3 - <<'PY'
import json;s=json.load(open('home/.chezmoitemplates/claude-settings-managed.json'));print(json.dumps(s['sandbox'],indent=1,sort_keys=True))
PY
make validate-agent-assets
make unit-test
grep -n 'bubblewrap\|socat' install/ubuntu/common/dependencies.sh tests/install/ubuntu/common/dependencies.bats
gh pr checks <pr-number>
```

## Completion

1. PR to `main` titled `feat(agents): render the Claude Code sandbox from the shared manifest (supersedes #179)`, English description crediting #179, listing the dropped AppArmor part, every sandbox default with its value, and the operator-visible effect paragraph; ends with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green including the bats jobs.
2. Artifacts at the exact expected paths; validation with verbatim outputs, the PR number and head SHA, and the pasted `sandbox` JSON.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `send.sh --body-file` for replies (turn delivery reaches you).
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
