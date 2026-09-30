# AGMSG-TASK dot-sandbox-unix-sockets-T44-a01

## Objective

T39 live E2E leg 1 (2026-09-29, after `make update`) confirmed the Linux
socket gap: inside the Claude Code sandbox `herdr pane list` fails with
`PermissionDenied: Operation not permitted` because `allowUnixSockets` is
macOS-only, so every `herdr` / `agmsg-dispatch` / `herdr-agents` call needs an
unsandboxed retry. Operator decision 2026-09-29: set
`sandbox.network.allowAllUnixSockets: true` (keeps filesystem and network
isolation; opens only local Unix sockets), keep `allowUnixSockets` for macOS.

Deliver:

1. `home/dot_agents/agent-config.yaml` `claude.sandbox.network`: add
   `allowAllUnixSockets: true` with a comment: Linux/WSL2 ignore
   `allowUnixSockets` and the seccomp filter blocks every Unix socket
   otherwise; the herdr control-plane socket must be reachable from
   sandboxed Bash.
2. `scripts/generate-agent-configs.py` `render_claude_sandbox`: render
   `network.allowAllUnixSockets` when present (boolean passthrough); the
   generator must not fail when the key is absent.
3. `scripts/validate-agent-assets.py` `validate_claude_sandbox`: if present,
   `allowAllUnixSockets` must be a boolean; one test each for accept/reject.
4. Regenerate `home/.chezmoitemplates/claude-settings-managed.json` with
   `uv run --with pyyaml scripts/generate-agent-configs.py`; `--check` ok.
5. README "Claude Code sandbox" section: one sentence stating that on Linux
   all Unix sockets are allowed for the control plane while file and network
   isolation stay in force; add "Operator-visible effect" wording accordingly.
6. `make unit-test`, `make validate-agent-assets` green.

7. Second leg-1 finding, same root cause: inside the sandbox `gh` returns
   HTTP 401 (the keyring D-Bus socket is a Unix socket too), so
   `allowAllUnixSockets` is expected to fix both herdr and gh; state that in
   the manifest comment and README sentence.
8. Third leg-1 finding: every `uv run` target fails inside the sandbox with
   `Read-only file system` on `~/.cache/uv`. Add `~/.cache/uv` to the Claude
   sandbox `filesystem.allowWrite` via a NEW manifest list
   `claude.sandbox.filesystem.extra_allow_write` (rendered after the Codex
   roots, validated as absolute or `~/` paths without globs, one test), with a
   comment naming the uv cache. Orchestrator decision 2026-09-30, flagged to
   the operator as a filesystem relaxation limited to the uv cache directory.

Do not touch `allowedDomains` (a separate finding under investigation) or
`failIfUnavailable`.

[memory:decision] T44: the Claude Code sandbox sets
`network.allowAllUnixSockets: true` so the herdr control plane works from
sandboxed Bash on Linux; file and network isolation are unchanged
(operator 2026-09-29, from T39 live E2E leg 1).

## Repo / branch

- Work ONLY in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`;
  branch `fix/sandbox-unix-sockets` from `origin/main`. Verify the dispatched
  task_rev sha256 against this file on your base, else stop and PONG. If the
  worktree has uncommitted files, stop and PONG.
- Ignore the Understand-Anything auto-update hook during this task; graph
  refresh is a separate task.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the sandbox.network block only), `scripts/generate-agent-configs.py`, `scripts/validate-agent-assets.py`, `home/.chezmoitemplates/claude-settings-managed.json` (generated only), `tests/unit/test_validate_agent_assets.py`, `tests/unit/test_generate_agent_configs.py`, `README.md` (the Claude Code sandbox section only)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-sandbox-unix-sockets-T44-a01.md` (main checkout)
- Note: inside a sandboxed shell prefix uv make targets with `UV_CACHE_DIR=$TMPDIR/uv-cache`; `gh` may need the unsandboxed retry until this change is live.

## Forbidden actions

- Any other sandbox key; `allowedDomains`; `failIfUnavailable`; hooks, settings outside the generated template, permgate; `.ua/**`; merging; force push; local bats; `make update`/`chezmoi apply`; writes outside the worktree except the listed paths.

## Validation commands (paste verbatim output)

```
git merge-base --is-ancestor origin/main HEAD && echo base-ok
git diff --stat origin/main
uv run --with pyyaml scripts/generate-agent-configs.py --check
python3 - <<'PY'
import json;s=json.load(open('home/.chezmoitemplates/claude-settings-managed.json'));print(json.dumps({k:s['sandbox'][k] for k in ('network','filesystem')},indent=1,sort_keys=True))
PY
make validate-agent-assets
make unit-test
gh pr checks <pr-number>
```

## Completion

1. PR to `main` titled `fix(agents): allow all Unix sockets in the Claude sandbox for the Linux control plane`, English description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green.
2. Artifacts at the exact expected paths with verbatim outputs, PR number and head SHA.
3. CompactionDB from the main checkout: `memory add --kind decision --scope project` with the `[memory:decision]` text above — paste command and output.
4. `send.sh --body-file` for replies. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.

## Orchestrator amendment (2026-09-30T04:30Z)

- Scope correction (audit of 1843dd1, P2): `allowed_files` reads
  "the sandbox.network block only" while addendum 8 requires the new
  `claude.sandbox.filesystem.extra_allow_write` list. The manifest allowance is
  the `sandbox.network` block **and** `sandbox.filesystem.extra_allow_write`;
  the forbidden "any other sandbox key" excludes those two. The worker's
  revision-1 resolution in favour of addendum 8 stands.

## Orchestrator amendment r2 (2026-10-01; dispatched as AGMSG-ACCEPTANCE status=revise; supersedes revision 1's socket relaxation)

Codex audit of c2c1f62 and the Codex GitHub P1 on PR #215
(`agent-config.yaml:232`) are confirmed on the operator's machine, outside the
sandbox: the user is in the `docker` group (`/var/run/docker.sock` root:docker
660), the user D-Bus session bus and `systemd --user` are reachable, and 110
Unix sockets are listening. With `allowAllUnixSockets: true` and
`autoAllowBashIfSandboxed: true`, an auto-approved sandboxed command can leave
the sandbox (`docker run -v /:/host …`, `systemd-run --user …`). Operator
decision 2026-10-01: **remove the socket relaxation; keep the uv cache
write.**

1. Remove `sandbox.network.allowAllUnixSockets` from
   `home/dot_agents/agent-config.yaml`, the generator passthrough
   (`scripts/generate-agent-configs.py`), the validator boolean check
   (`scripts/validate-agent-assets.py`), the rendered
   `home/.chezmoitemplates/claude-settings-managed.json`, and the two tests
   that assert it. Keep `allowUnixSockets: [~/.config/herdr/herdr.sock]` with its
   macOS-only comment. Keep `filesystem.extra_allow_write: [~/.cache/uv]` and
   everything built for it (generator, validator, tests, README sentence).
2. README sandbox section: state that Linux/WSL2 ignore `allowUnixSockets`
   (seccomp cannot inspect socket paths), so `herdr`, `agmsg-dispatch`,
   `herdr-agents` and `gh` (keyring over D-Bus) run through the normal
   unsandboxed retry prompt on Linux; `allowAllUnixSockets` is deliberately not
   used because on a workstation with a docker-group user or a reachable
   `systemd --user` bus it turns the auto-approved sandbox into an escape
   (upstream limitation: code.claude.com/docs/en/sandboxing#security-limitations).
3. Task-file note for the record: the round-1 orchestrator review accepted the
   relaxation with "docker.sock if present" in its impact line without weighing
   it as an escape; the security-profile review this trust-boundary change
   required under `model-selection.md` was not run. Removal narrows the
   boundary, so r2 needs no separate security review.

Validation: exit codes captured directly (never after a pipe); paste
`grep -n allowAllUnixSockets` over the four touched files returning nothing
(`exit=1`), `make render-check`, `make unit-test`, `make validate-agent-assets`.
allowed_files unchanged. Keep PR #215 (retitle to the uv cache change); push
without `-u`.
