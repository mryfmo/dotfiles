# WP-G: Residual hermes references (integration-grep findings)

task_id: WP-G
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpg

## Objective

Clean up two hermes remnants found by the orchestrator's integration grep after WP-A..WP-F were accepted. Hermes has been fully removed from this repo (install path, config deployment, manifest, generator/validator, skills). Only Codex and Claude Code remain as agent targets.

## Changes (exhaustive — do all, nothing else)

EDIT home/dot_agents/README.md:

- Rewrite so it documents the CURRENT two-agent reality (Codex + Claude Code only). Remove: all Hermes mentions, the reference to deleted `home/private_dot_hermes/private_config.yaml.tmpl`, the "all three agents" wording (now: both agents), the "Hermes orchestration" section, and Hermes lines in the architecture diagram. Keep everything that is still true (Cognee guidance for Codex/Claude Code, validator description, skill/MCP parity rules) — adjust wording, do not delete unrelated content.

EDIT scripts/require-crit-review.py:

- Remove the now-dead pattern entry `"home/dot_agents/hermes-config-base.yaml"` (~line 41). Touch nothing else in the guard logic.

KEEP: `home/dot_local/bin/common/executable_dev` tmux guard (deliberate), `home/dot_config/herdr/`, agmsg skills.

## Allowed files (edit boundary)

Only the two files above, plus your artifact paths.

## Forbidden actions

git commit; git push; chezmoi apply; running bats; dependency changes; editing any other file; running make require-crit-review (orchestrator's job).

## Validation (run and capture output)

1. `grep -n -i "hermes" home/dot_agents/README.md scripts/require-crit-review.py || true` → zero hits
2. `uv run --with pyyaml scripts/validate-agent-assets.py` → still passes
3. `make unit-test` → still passes (guard tests live in tests/unit)
4. `git status --porcelain` → only the two files changed

## Expected artifacts (write to these exact paths)

- report: .orchestration/reports/WP-G.md
- validation: .orchestration/validation/WP-G.txt
- sandbox: .orchestration/sandboxes/WP-G.md (record: codex workspace-write fallback)
- learning: .orchestration/learning/WP-G.md ("none" if nothing)
- autoskill: .orchestration/autoskill/runs/WP-G.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpg orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-G status=ready_for_review report=.orchestration/reports/WP-G.md validation=.orchestration/validation/WP-G.txt sandbox=.orchestration/sandboxes/WP-G.md learning=.orchestration/learning/WP-G.md autoskill=.orchestration/autoskill/runs/WP-G.md"
```

If blocked: same message with status=blocked, artifacts explaining why.

max_turns: 30
