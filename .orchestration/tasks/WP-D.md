# WP-D: Remove Hermes config, manifest entries, and generator/validator support

task_id: WP-D
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-tmux-hermes-removal
worker: codex-wpd

## Objective

Remove Hermes from the agent-config single-source-of-truth manifest and from the config generator/validators, and delete the deployed Hermes config sources. This is the most entangled package — the manifest and the validators MUST change consistently in this one task.

## Changes (exhaustive — do all, nothing else)

DELETE:

- home/private_dot_hermes/ (entire directory, contains private_config.yaml.tmpl)
- home/dot_agents/hermes-config-base.yaml

EDIT home/dot_agents/agent-config.yaml:

- remove `hermes` from the `targets:` list (~line 20)
- remove the top-level `hermes:` block (config_path/base_config_path/terminal/plugins, ~line 143+)
- remove every per-MCP-server `hermes: true|false` enablement flag (~lines 212-349)

EDIT scripts/generate-agent-configs.py:

- delete `render_hermes()` (~line 354-410) and its OUTPUTS entry (~line 484: `ROOT / manifest["hermes"]["config_path"]: render_hermes(manifest)`)
- remove any other hermes handling (grep the file)

EDIT scripts/validate-agent-assets.py:

- delete `validate_hermes_config_template()` (~line 278+) and its call (~line 636)
- change the targets check (~line 300-301) to require exactly `{"codex", "claude"}`
- remove the hermes parameter/logic from `validate_mcp_parity` (~lines 332-341, 637)
- remove hermes from the module docstring; grep for remaining hermes refs

EDIT scripts/check-agent-runtime.py:

- remove the Hermes config tuple (~line 120) and Hermes mention in the docstring (~line 5)

THEN REGENERATE AND VERIFY:

- Find how generation is invoked (see scripts/update-agent-assets.sh) and run the generator (likely `uv run --with pyyaml scripts/generate-agent-configs.py` or via that wrapper).
- The generated codex/claude outputs must be UNCHANGED by this removal (`git status` / `git diff --stat` shows no diffs beyond the files listed in this task). If they change, investigate and report — do not hand-tweak generated files.
- Run `uv run --with pyyaml scripts/validate-agent-assets.py` → must pass.

## Allowed files (edit boundary)

Only the files listed above, plus your artifact paths below. Generated outputs may be rewritten only by running the generator, and only if byte-identical results confirm no drift (otherwise report).

## Forbidden actions

git commit; git push; chezmoi apply; running bats; adding dependencies; editing skills directories, install/, .chezmoiscripts/, Makefile, README, .github/ (other tasks own those); hand-editing generated output files.

## Validation (run and capture output)

1. deleted paths gone
2. `grep -rn -i "hermes" home/dot_agents/agent-config.yaml scripts/generate-agent-configs.py scripts/validate-agent-assets.py scripts/check-agent-runtime.py || true` → zero hits
3. generator run output + `git status --porcelain` (only expected changes)
4. `uv run --with pyyaml scripts/validate-agent-assets.py` → PASS output captured
5. `make unit-test` if tests/unit covers these scripts (check first; capture output)

## Expected artifacts (write to these exact paths)

- report: .orchestration/reports/WP-D.md
- validation: .orchestration/validation/WP-D.txt
- sandbox: .orchestration/sandboxes/WP-D.md (record: codex exec --sandbox workspace-write fallback)
- learning: .orchestration/learning/WP-D.md ("none" if nothing)
- autoskill: .orchestration/autoskill/runs/WP-D.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-tmux-hermes-removal codex-wpd orchestrator-fable5 "AGMSG-RESULT v1 task_id=WP-D status=ready_for_review report=.orchestration/reports/WP-D.md validation=.orchestration/validation/WP-D.txt sandbox=.orchestration/sandboxes/WP-D.md learning=.orchestration/learning/WP-D.md autoskill=.orchestration/autoskill/runs/WP-D.md"
```

If blocked: same message with status=blocked, artifacts explaining why.

max_turns: 40
