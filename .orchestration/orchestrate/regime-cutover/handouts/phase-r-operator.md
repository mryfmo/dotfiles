# Phase R operator handout (2026-10-26)

These are the steps the coordinator cannot take. Each one names the rule that stops the agent. The full inventory is `phase-r-issues.md`. Every dry-run below was measured read-only on 2026-10-26. Run the dry-run again before the command; if the output differs, stop and tell the coordinator.

## 1. Bot threads (C1): no action needed

The coordinator now answers bot findings with PR comments (standing order 32). #568, #569 and #572 were answered and merged that way.

## 2. macOS: worktrees inside the checkout (C4)

After U95 lands, a seat launch refuses while any linked worktree sits inside the checkout. Agents never write under `~/Workspace`.

Dry-run: `git -C ~/Workspace/dotfiles worktree list --porcelain` lists 10 under `.claude/worktrees/`, all clean (`git status --porcelain=v1` prints nothing in each).

- The 8 under `.claude/worktrees/.gc-quarantine/` were quarantined by worktree-gc on 2026-10-25 (gate G8). Delete them with `~/.local/bin/common/worktree-gc.sh --purge` from `~/Workspace/dotfiles`.
- Two are locked Claude Code agent worktrees. `agent-a3b422ab1792c0c06` holds `feat/coordinator-levers-preauthorized` (PR #481, closed). `agent-aef8f310d7f4c14e2` holds `ci/public-bootstrap-apt-mirror` (PR #480, merged). Removing a worktree keeps its branch:

```
cd ~/Workspace/dotfiles
for w in .claude/worktrees/agent-a3b422ab1792c0c06 .claude/worktrees/agent-aef8f310d7f4c14e2; do
  git worktree unlock "$w" && git worktree remove "$w"
done
```

## 3. macOS: doctor warnings (C6, C7)

- `make gh-auth` stores the GitHub login in gh's file, which the Claude sandbox can read. It is an interactive login.
- `ai-coe-daily-ops@ai-coe` is enabled with no pin. It comes from a local directory marketplace under `~/Workspace`. Choose one: disable it (`claude plugin disable ai-coe-daily-ops@ai-coe --scope user`), keep it with the warning (the default), or ask the coordinator for a unit that pins it from the private source.

## 4. Ubuntu host: after the coordinator reports the last unit landed (C3, C4, C5)

Standing orders 27 and 30 keep the agent's ssh read-only.

Dry-run: the chezmoi source is at `81c74922`, and `srt` and `rg` are not on PATH, so every seat launch refuses after U85 (`f1374ba7`).

```
cd ~/.local/share/chezmoi && sudo make update && make doctor
for w in orchestrator-review worker-c worker-d worker-e worker-sec; do
  git -C ~/Workspace/dotfiles worktree remove ".claude/worktrees/$w"
done
```

The second loop is G16 row 12. All five trees are clean and unlocked.

## 5. G16 host cleanup rows still open (C5)

Run them from `docs/operator-handout-g16.md`. Measured state on 2026-10-26:

| row | host | state |
| --- | --- | --- |
| 1 | mac | `~/.omp/profiles/pilot-bridge` present |
| 2 | mac | `default.rules.pre-apply-20261015` present |
| 3 | mac | no `~/.ssh/*.pub` |
| 4 | Ubuntu | done (all four directories 700) |
| 5 | Ubuntu | node 26.9.0 still installed |
| 6 | Ubuntu | `mise prune --dry-run` still lists claude-code versions |
| 7 | mac | `mise prune --dry-run` still lists claude-code versions |
| 8 | Ubuntu | `~/.local/bin/starship` present |
| 9 | both | cmake 4.4.4 still in mise; prune after the deploy |
| 11 | Ubuntu | done (`docker.sources`) |
| 12 | Ubuntu | five worktrees present (section 4) |
| 13 | mac | both retired audit seat worktrees present |

## 6. Whenever convenient

- F027 (C9). Run `.orchestration/validation/025-pilot-s0-siwc-probe.py` once and consent in the browser. Paste the model count it prints. Without it, the static model rows stay.
- U88 (C8). Create the GitHub machine account and a fine-grained PAT (design in `units.tsv` row U88). Without it, seats keep the G17 conditions.
