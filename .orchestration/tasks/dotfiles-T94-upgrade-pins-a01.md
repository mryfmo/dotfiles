# AGMSG-TASK dotfiles-T94-upgrade-pins-a01

Drafted 2026-10-04 by the orchestrator seat. The operator's `make upgrade` left its pin diff uncommitted in the canonical clone (`~/.local/share/chezmoi`, then at c6de5156); per the regime rule that whole diff travels as one class-pure PR. The diff is saved verbatim as `.orchestration/tasks/dotfiles-T94-pending-pins.patch` (132 lines, 6 files, 18 insertions / 18 deletions, taken against c6de5156 before the clone was fast-forwarded to f32f33a0).

## Objective

1. Apply the patch on a branch from `origin/main` (`git apply --3way .orchestration/tasks/dotfiles-T94-pending-pins.patch`; if a hunk no longer applies because a later task moved the line, reproduce the same value change by hand and say so). The value changes, and nothing else, are:
   - mise `v2026.9.13` → `v2026.9.14` (`agent-config.yaml` pin, rendered `install/common/mise.sh`);
   - aws-cli `2.37.3` → `2.37.4` (`agent-config.yaml`, rendered `install/ubuntu/common/aws_cli.sh`);
   - crit `v0.21.0` → `v0.21.1` with its four platform sha256 values (`agent-config.yaml`, rendered `scripts/lib/installer-pins.sh`);
   - `home/dot_mise/config.toml` and `mise.lock`: `npm:@anthropic-ai/claude-code` `2.1.287` → `2.1.288`, `npm:pnpm` `12.6.0` → `12.7.0`.
2. `make render-check` must pass (the rendered files must equal what the generator produces from the manifest).
3. Sync every expected-version assertion in `tests/**` that pins one of the old values (grep output above the task text; T73 moved most of them to read the config, so expect few or none) and the CI statusline/version checks if they pin a literal.
4. No other change. Do not run `make upgrade` or `make update`.

Forbidden: any file outside the six patched files and the test files that pin the old values; any other pin.

[memory:decision] dotfiles-T94 (operator 2026-10-04): pins advance to mise v2026.9.14, aws-cli 2.37.4, crit v0.21.1, claude-code 2.1.288 and pnpm 12.7.0 through one class-pure PR carrying the whole `make upgrade` diff; the canonical clone no longer holds an uncommitted pin diff.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c chore/upgrade-pins-2026-10-04 origin/main` (f32f33a0 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml`, `home/dot_mise/config.toml`, `home/dot_mise/mise.lock`, `install/common/mise.sh`, `install/ubuntu/common/aws_cli.sh`, `scripts/lib/installer-pins.sh`, and any `tests/**` or `.github/workflows/**` file that pins one of the five old values
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T94-upgrade-pins-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
make validate-agent-assets
grep -rn "2\.1\.287\|12\.6\.0\|v0\.21\.0\|2\.37\.3\|v2026\.9\.13" home install scripts tests .github ; echo "rc=$?"
make unit-test
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if Plan Mode was used.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T94` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=25.

## Dispatch

- 2026-10-04 07:50Z to `claude-standard-dot-a005` (worker-c, wT:p2) right after its T71 RESULT (PR #249 pending acceptance; keep `feat/generator-multi-target` untouched). Branch from `origin/main` f32f33a0 or later. Disjoint from T71 (generator/validator code), T88 (SKILL/rule) and T92 (stop gate).
