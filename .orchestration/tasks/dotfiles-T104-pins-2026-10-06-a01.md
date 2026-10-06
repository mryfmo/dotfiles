# AGMSG-TASK dotfiles-T104-pins-2026-10-06-a01

Drafted 2026-10-06 00:40Z by the orchestrator seat. The canonical clone `~/.local/share/chezmoi` holds a pending `make upgrade` pin diff (7 files, +57/−57; surfaced as "Applied autostash" during the T103 deploy). Per the regime rule it travels as one class-pure pin PR with the test assertions synced; it is never left dirty across sessions. Kind: pins only (manifest `assets.*.pin`, mise config and lock, rendered installer pin lines); no boundary source. Dispatched to `claude-standard-dot-a005` (worker-c, wT:p2).

## Objective

1. Apply `.orchestration/validation/pins-2026-10-06.diff` (exported verbatim from the canonical clone with `git diff`; read it from the main checkout) onto a fresh branch from `origin/main` in worker-c: `git apply --index <main checkout>/.orchestration/validation/pins-2026-10-06.diff`. Pins: mise v2026.9.14 → v2026.9.16; aws-cli 2.37.4 → 2.37.5; chezmoi 2.70.4/2.72.2 → 2.73.0 (bootstrap pin, `setup.sh`, `installer-pins.sh`, mise); dotenvx 2.30.0 → 2.31.1; hugo-extended 0.166.0 → 0.167.0; claude-code 2.1.288 → 2.1.289; codex 0.160.0 → 0.160.1; ccusage 20.0.24 → 20.0.26; pnpm 12.7.0 → 12.8.1; `mise.lock` entries accordingly.
2. `make render-check` must be clean on the result (the installer lines are rendered from the manifest; if the diff and the renderer disagree, the renderer wins and you say so).
3. Sync `tests/**` expected-version assertions that pin the *live* values (T37 #209, T53 #224 pattern). Fixture values inside fake release listings stay as fixtures unless a test asserts them against the manifest; list each test you changed and each you left, with the reason.
4. No other change. In particular no hook-trust edit: Codex 0.160.1 is a pin bump only; the hash algorithm check belongs to the orchestrator's post-deploy verification (`hooks/list`).

Forbidden: any file outside the diff's seven plus `tests/**`; `make update`/`upgrade`/`apply`; thread resolution; local bats.

[memory:decision] dotfiles-T104 (orchestrator 2026-10-06): the pending `make upgrade` pin diff of the canonical clone travels as one pin PR with synced test assertions; the orchestrator verifies the Codex hook hashes after deploy.

## Repo / branch

- Work ONLY in worker-c. `git fetch origin`; `git switch -c pins/upgrade-2026-10-06 --no-track origin/main` (main at ca5d28ec or later). Verify the dispatched task_rev against the main checkout's task file; otherwise stop and PONG blocked.

## Allowed files

`home/dot_agents/agent-config.yaml` (pins only), `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`, `install/common/mise.sh`, `install/ubuntu/common/aws_cli.sh`, `scripts/lib/installer-pins.sh`, `setup.sh` (the `CHEZMOI_VERSION` line), `tests/**`. Artifacts at the standard seven `dotfiles-T104-pins-2026-10-06-a01` paths in the main checkout through the permission gate (Claude seat), masked.

## Validation commands (paste verbatim output, whole)

```
git apply --index ~/Workspace/dotfiles/.orchestration/validation/pins-2026-10-06.diff; echo "rc=$?"
git diff --cached --stat
make render-check
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
git diff origin/main --stat
gh pr checks <pr>
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`; CI green on the final head.
2. After the final push: Bot wait per the SKILL (end on a quota notice and record it); fix P0/P1; do not resolve threads.
3. Artifacts, validation with verbatim outputs, PR number, head SHA; `cost: n/a`.
4. CompactionDB: record the `[memory:decision]` line with `uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project` in the main checkout.
5. `AGMSG-RESULT v1 task_id=dotfiles-T104` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"`. max_turns=12.

### PONG decision 1 (orchestrator, 2026-10-06 01:10Z) — audit of bd0327a0: two artifact corrections, no push

The audit found no code defect. Two artifact findings: (1) the sandbox record lists "the inbox read" under the Worker Playbook step-4 exceptions, which do not include inbox reads: state the exact command that was run and where (an `inbox.sh` read works inside the sandbox since the agmsg store is a writable root; if it did run through the permission gate, record it as a disclosed deviation with the reason, not as a step-4 exception); (2) the validation file has no pasted PR metadata: append the verbatim output of `gh pr view 290 --json number,title,body,headRefOid` so the English title/description and the attribution footer are on record. Re-mask both files in the main checkout and answer `AGMSG-PONG v1 task_id=dotfiles-T104 status=corrected …` (no push, no new RESULT; the head stays bd0327a0).
