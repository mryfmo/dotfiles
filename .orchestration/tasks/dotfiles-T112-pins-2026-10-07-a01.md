# AGMSG-TASK dotfiles-T112-pins-2026-10-07-a01

Drafted 2026-10-07 by the orchestrator seat (`claude-remediation-dot`, w1A:p1). The operator ran `make upgrade` in the canonical clone `~/.local/share/chezmoi`; its pending pin diff must travel to `main` as one class-pure PR (regime rule: never leave that diff dirty across sessions; precedent T37 #209, T104). The orchestrator extracted the pins-only part of that diff into `.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-pins.patch` (the clone also holds an unrelated, rejected project-map draft, excluded from the patch and handled by the orchestrator). Kind: version pins in the manifest, mise config and lock, two installer scripts; Claude seat allowed. Dispatched to `claude-standard-dot-a005` (worker-c, w1A:p2).

## Objective

1. `git fetch origin`; `git switch -c chore/pins-2026-10-07 --no-track origin/main` (main at 7d3a45ee or later).
2. `git apply --index ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-pins.patch`. Expected result, nothing else:
   - `home/dot_agents/agent-config.yaml`: `assets.mise.pin: v2026.9.17`, `assets.aws-cli.pin: 2.37.6`.
   - `home/dot_mise/config.toml`: uv 0.12.21, aqua:mikefarah/yq 4.54.1, npm:@anthropic-ai/claude-code 2.1.292, github:x-motemen/ghq 1.11.2, github:ogulcancelik/herdr 0.9.3.
   - `home/dot_mise/mise.lock`: the matching lock update.
   - `install/common/mise.sh`: `MISE_VERSION="v2026.9.17"`; `install/ubuntu/common/aws_cli.sh`: `AWS_CLI_VERSION="2.37.6"`.
3. Blob-identity proof: for each of the five files, `sha256sum <file>` in the branch must equal `sha256sum ~/.local/share/chezmoi/<file>` for the four non-manifest files (read-only access to the clone), and for `agent-config.yaml` paste `diff <(git show origin/main:home/dot_agents/agent-config.yaml) home/dot_agents/agent-config.yaml` showing only the two `pin:` lines changed.
4. Renderer consistency: `make render-check` rc=0 (the installer version lines are rendered from the manifest, so a mismatch fails here), `uv run --no-project --with pyyaml scripts/validate-agent-assets.py` rc=0, `make unit-test`. If any test pins an old version, update only that assertion and say so in the report (the orchestrator's grep found none).

Forbidden: anything else; `make update`; `make upgrade`; touching `~/.local/share/chezmoi` (read-only `sha256sum` excepted); thread resolution.

[memory:decision] dotfiles-T112 (orchestrator 2026-10-07): pending `make upgrade` pins from the canonical clone travel to `main` as one class-pure worker PR built from an orchestrator-extracted pins-only patch, with per-file blob identity proven against the clone; unrelated edits in the clone never ride along.

## Repo / branch

worker-c; branch `chore/pins-2026-10-07` from `origin/main`.

## Allowed files

`home/dot_agents/agent-config.yaml` (the two `pin:` lines only), `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`, `install/common/mise.sh`, `install/ubuntu/common/aws_cli.sh`; a version assertion in `tests/**` only if a test fails. Artifacts at the standard seven `dotfiles-T112-pins-2026-10-07-a01` paths in the main checkout (Claude seat, through the permission gate), masked.

## Validation commands (paste verbatim output, whole)

```
git apply --index ~/Workspace/dotfiles/.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-pins.patch; echo "rc=$?"
git diff --cached --stat
for f in home/dot_mise/config.toml home/dot_mise/mise.lock install/common/mise.sh install/ubuntu/common/aws_cli.sh; do sha256sum "$f" "~/.local/share/chezmoi/$f"; done
diff <(git show origin/main:home/dot_agents/agent-config.yaml) home/dot_agents/agent-config.yaml; echo "rc=$?"
make render-check; echo "rc=$?"
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
make unit-test 2>&1 | tail -3
shellcheck install/common/mise.sh install/ubuntu/common/aws_cli.sh; echo "rc=$?"
gh pr checks <pr>
```

## Completion

PR to `main` (English title `chore(pins): mise v2026.9.17, aws-cli 2.37.6, uv 0.12.21, yq 4.54.1, claude-code 2.1.292, ghq 1.11.2, herdr 0.9.3`, attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line, then `AGMSG-RESULT v1 task_id=dotfiles-T112` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot w1A:p1 "<single line>"`. max_turns=10.
