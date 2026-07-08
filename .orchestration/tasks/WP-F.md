# WP-F: Shared tooling, CI, and docs cleanup (tmux + hermes)

task_id: WP-F
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpf

## Objective

Remove tmux/hermes references from shared maintenance tooling, CI workflows, and documentation. This task owns Makefile, scripts/ (except the three python scripts owned by WP-D), .github/, and README.

## Changes (exhaustive — do all, nothing else)

EDIT Makefile:

- remove line ~45: `chezmoi apply --verbose --force --exclude=scripts ~/.hermes` (the plain `chezmoi apply` on the next line stays)
- remove line ~55: `./scripts/update-codex-statusline-tools.sh` call in the `update` target

DELETE:

- scripts/update-codex-statusline-tools.sh (exists only for the tmux Codex status segment)

EDIT scripts/check-tools.sh:

- remove `check_command tmux -V` (~line 115) and `check_command hermes --version` (~line 116)

EDIT scripts/upgrade-tools.sh:

- remove `upgrade_tmux_plugins()` (~lines 331-356) and its call site (~line 412)
- remove the "Codex tmux status segment helpers" section (~line 358+) and its call site, IF it exists solely for the tmux status segment (read it; if it also installs non-tmux tooling, keep the non-tmux parts and report)
- keep shdoc comment conventions and shfmt formatting (`shfmt --indent 4 --space-redirects --diff scripts/upgrade-tools.sh scripts/check-tools.sh` must pass)

EDIT .github/workflows/macos.yaml and .github/workflows/ubuntu.yaml:

- remove the `home/dot_tmux.conf.d/...` path-trigger entries (lines ~13 and ~26 in each)
- also grep both workflows for tmux/tpm/hermes job steps or test enumerations and remove those (report what you find)

EDIT .github/workflows/agent-assets.yml:

- remove the three hermes-agent.nousresearch.com doc URLs (~lines 49-51) and any surrounding hermes-only logic

EDIT README.md:

- remove tmux badge (~line 13), hermes badge (~line 20), `hermes.install` docs (~lines 34-35), hermes mention (~line 149), tmux server.conf instructions (~lines 336, 339), and any other tmux/hermes prose you find in the file (grep it); keep surrounding structure/markdown valid

EDIT home/dot_local/bin/common/executable_start-cognee-mcp:

- remove the Hermes mention from its shdoc comment (~line 6); functionality unchanged

## Allowed files (edit boundary)

Only the files listed above, plus your artifact paths below.

## Forbidden actions

git commit; git push; chezmoi apply; running bats; adding dependencies; editing install/, home/.chezmoiscripts/, home/dot_agents/, home/dot_tmux\*, tests/, scripts/{generate-agent-configs.py,validate-agent-assets.py,check-agent-runtime.py} (other tasks own those).

## Validation (run and capture output)

1. `grep -n -i "tmux\|hermes\|tpm" Makefile scripts/check-tools.sh scripts/upgrade-tools.sh .github/workflows/*.yaml .github/workflows/*.yml README.md home/dot_local/bin/common/executable_start-cognee-mcp || true` → zero hits (justify any remainder)
2. `shfmt --indent 4 --space-redirects --diff scripts/ home/dot_local/bin/common/executable_start-cognee-mcp || true` → no diff for the files you touched
3. `git status --porcelain` → only expected changes

## Expected artifacts (write to these exact paths)

- report: .orchestration/reports/WP-F.md
- validation: .orchestration/validation/WP-F.txt
- sandbox: .orchestration/sandboxes/WP-F.md (record: codex exec --sandbox workspace-write fallback)
- learning: .orchestration/learning/WP-F.md ("none" if nothing)
- autoskill: .orchestration/autoskill/runs/WP-F.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpf orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-F status=ready_for_review report=.orchestration/reports/WP-F.md validation=.orchestration/validation/WP-F.txt sandbox=.orchestration/sandboxes/WP-F.md learning=.orchestration/learning/WP-F.md autoskill=.orchestration/autoskill/runs/WP-F.md"
```

If blocked: same message with status=blocked, artifacts explaining why.

max_turns: 40
