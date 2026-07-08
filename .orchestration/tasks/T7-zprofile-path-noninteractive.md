# T7: Make PATH available to non-interactive login shells (fix ghostty initial-command chain)

task_id: T7
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-gpt55-high

## Background (why)

T5 wired `initial-command = /bin/zsh -lc 'exec herdr-session'` in the Ghostty
config. Rigorous re-verification with a CLEAN environment
(`env -i HOME=... /bin/zsh -lc ...`, reproducing Ghostty's launch context)
shows: `herdr`, `claude`, `codex`, `jq` resolve (`~/.zprofile` runs brew
shellenv + `mise activate zsh`, which does eager PATH setup), but
**`herdr-session` is NOT FOUND** — the `path=(... ~/.local/bin/common ...)`
block lives only in `home/dot_zshrc`, which non-interactive shells never
read. So the auto-start chain would die with exit 127 on Ghostty restart.
Root fix: user-level PATH construction belongs in `.zprofile` (read by ALL
login shells, interactive or not), per zsh convention.

## Goal

1. **Move** the `path=(...)` construction block (currently `home/dot_zshrc`
   lines ~6-12: `typeset -gU path`, `/usr/local/{,s}bin`, `${HOME}/.local/bin`,
   `${HOME}/.local/bin/common`) from `home/dot_zshrc` into `home/dot_zprofile`.
   Placement: after the existing brew shellenv + mise activate lines (mise
   tools must keep highest priority; `typeset -gU path` dedups). Keep the
   `(N-/)` glob qualifiers. Keep shdoc-style comments consistent with the
   file's existing header.
2. **Keep** the `fpath=(...)` block (completion functions) in `home/dot_zshrc`
   — fpath is interactive-only concern. Keep `typeset -gU path fpath` where
   needed so both files are correct standalone (e.g. `typeset -gU path` in
   zprofile, `typeset -gU fpath` in zshrc — adjust so neither file references
   an array it no longer sets up).
3. **Unit test**: extend tests/unit/test_herdr_agents.py (or the suitable
   existing test module) with a static check that `home/dot_zprofile` puts
   `${HOME}/.local/bin/common` on `path`, and that the E2E zsh-function test
   still passes. If the E2E test currently relies on dot_zshrc building PATH,
   adapt its setup minimally (it stubs commands via an injected PATH, so it
   likely needs no change — verify).
4. README: update only if it describes where PATH is set (grep first;
   minimal diff).

## Allowed files (edit boundary)

- home/dot_zprofile
- home/dot_zshrc
- tests/unit/ (minimal additions/adjustments)
- README.md (only if it references the moved block)
- plus your artifact paths under .orchestration/

## Forbidden actions

git commit; git push; chezmoi apply; make update/upgrade; make require-crit-review; editing ~/.zprofile / ~/.zshrc directly (repo sources only); local bats; herdr pane/workspace/agent operations; restarting Ghostty.

## Validation (record outputs in the validation artifact)

1. `zsh -n home/dot_zprofile` and `zsh -n home/dot_zshrc` → ok
2. Simulated clean-login check WITHOUT touching deployed files: run
   `env -i HOME=$(mktemp -d) ... zsh -lc` style simulation is not possible
   against repo sources directly, so instead assert content statically AND
   run: `zsh -fc 'HOME=/Users/mryfmo; source home/dot_zprofile 2>/dev/null; print -l $path | grep -c "/Users/mryfmo/.local/bin/common"'` → >= 1
   (stub `brew`/`mise` on a fake PATH first if sourcing errors otherwise; show what you did)
3. `uv run python -m unittest discover -s tests/unit -v` → green including new/updated tests
4. `git status --porcelain` → only expected changes

## Expected artifacts

- report: .orchestration/reports/T7.md
- validation: .orchestration/validation/T7.txt
- sandbox: .orchestration/sandboxes/T7.md
- learning: .orchestration/learning/T7.md
- autoskill: .orchestration/autoskill/runs/T7.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT v1 task_id=T7 status=ready_for_review report=.orchestration/reports/T7.md validation=.orchestration/validation/T7.txt sandbox=.orchestration/sandboxes/T7.md learning=.orchestration/learning/T7.md autoskill=.orchestration/autoskill/runs/T7.md"
```

max_turns: 25
