# Report: dotfiles-T112-pins-2026-10-07-a01

- **PR:** https://github.com/mryfmo/dotfiles/pull/301, branch `chore/pins-2026-10-07` from `origin/main` `7d3a45ee`, head `f678999551cc40733ad96cb32f0292849de7d932` (one commit).
- **Status:** ready_for_review.
- **CI:** all 16 checks pass on `f6789995`, and every check run carries that head_sha.
- **Bot:** `bot: none`. The 15-minute wait after green CI found no Bot review or inline comment (31 iterations, all `rc=0`, empty). The Codex code review reported "usage limits have been reached". The Codex security review completed on `f6789995` (summary comment `6030181536`: `headSha` f6789995, `status: completed`) and left no comment or thread. CodeRabbit skipped because auto reviews are disabled.
- **Unresolved threads:** none.

## What changed

- `git apply --index` of the orchestrator's `dotfiles-T112-pins-2026-10-07-a01-pins.patch` returned rc=0. The commit holds exactly the five allowed files:
  - `home/dot_agents/agent-config.yaml`: `assets.mise.pin` v2026.9.16 → v2026.9.17, `assets.aws-cli.pin` 2.37.5 → 2.37.6. The diff against `origin/main` is only those two lines (lines 351 and 381).
  - `install/common/mise.sh`: `MISE_VERSION="v2026.9.17"`. `install/ubuntu/common/aws_cli.sh`: `AWS_CLI_VERSION="2.37.6"`.
  - `home/dot_mise/config.toml`: uv 0.12.21, yq 4.54.1, claude-code 2.1.292 (`allow_builds` kept), ghq 1.11.2, herdr 0.9.3. `home/dot_mise/mise.lock` carries the matching update.
- **Blob identity:** the four non-manifest files have the same sha256 as their copies in the canonical clone. The clone was only read.
- **No test or workflow edit was needed.** `git grep` finds no old version string outside `mise.lock` and `.orchestration` (rc=1). CI derives `DOTFILES_MISE_VERSION` from the pin. render-check, the validator, shellcheck, shfmt and `make unit-test` (921, skipped=1) pass.

## User-visible impact (AGENTS.md "Dotfiles safety")

- After `chezmoi apply` and `mise install`, the listed tools move to the new versions. Fresh bootstraps install mise v2026.9.17 and aws-cli 2.37.6. No shell startup, PATH, auth, hook or permission default changes.

## Worker review (Worker Playbook step 5; `crit status --json` had no review file)

- An independent read-only subagent reviewed `7d3a45ee..f6789995` and approved it with 4 informational P3s. Evidence: `.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-worker-crit.json` and `-worker-review-receipt.md`.
- **Note for the orchestrator (P3, not applicable here):** the herdr lock URLs moved from `github.com/herdrdev/herdr` to `github.com/ogulcancelik/herdr`. The validation file pastes `gh api` output showing that `repos/ogulcancelik/herdr` resolves to the canonical `herdrdev/herdr`. mise wrote the URLs from the `github:ogulcancelik/herdr` backend that `config.toml` already declared on `main`, and `provenance = "github-attestations"` is kept. Renaming the backend to `github:herdrdev/herdr` would need its own task, because this PR must stay byte-identical to the clone.
- **Pre-existing, outside the changeset:** an orphan `aqua:tak848/ccgate` 0.9.5 lock entry, already present at `7d3a45ee` (ccgate was removed in T28).

## CompactionDB (main checkout, through the permission gate)

```
cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T112 (orchestrator 2026-10-07): pending `make upgrade` pins from the canonical clone travel to `main` as one class-pure worker PR built from an orchestrator-extracted pins-only patch, with per-file blob identity proven against the clone; unrelated edits in the clone never ride along.'
```

ID `0e4d1b15-e1cf-400e-9868-5597258886ba` (output in the validation file).

[memory:decision] dotfiles-T112 (orchestrator 2026-10-07): pending `make upgrade` pins travel to `main` as one class-pure worker PR built from an orchestrator-extracted pins-only patch, with per-file blob identity proven against the clone.

## Other

- Understand-Anything hook: did not fire. Plan Mode not used; no Crit server started.
- cost: n/a
- **Main-checkout validator, for the orchestrator:** `validate-agent-assets.py` run in the main checkout exits rc=1. Its only error is `.orchestration/tasks/dotfiles-T112-pins-2026-10-07-a01.md names a home directory`, which is the orchestrator's task file and not one of this task's artifacts, so I did not edit it. The seven T112 artifacts are masked and raise no error. The run inside worker-c passes (rc=0, in the validation file).
