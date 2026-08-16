# T48c: Render the notify command path at apply time (T48 live-deploy defect)

task_id: T48c
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-compactiondb-research-integration.md (Phase 3; defect found by T51 deployment)

[memory: failure — chezmoi modify_ scripts are executed, not templated: a literal '{{ .chezmoi.homeDir }}' emitted by the profile generator reached ~/.codex/deep.config.toml unrendered, so Codex notify pointed at a nonexistent path.]

## Defect (orchestrator-verified live)

`home/dot_codex/modify_<profile>.config.toml` are chezmoi modify SCRIPTS
(Python, executed at apply); their output is NOT template-rendered. The
T48-generated MANAGED content embeds the literal
`{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify`, which
was deployed verbatim into ~/.codex/deep.config.toml.

## Fix (exact)

Keep the generator/agent-config.yaml value as-is (machine-portable source).
In the generator's modify-script emission (scripts/generate-agent-configs.py
and thus the regenerated modify scripts), make the modify script expand the
placeholder at APPLY time: replace occurrences of the literal
`{{ .chezmoi.homeDir }}` in MANAGED with `str(Path.home())` before output
(single well-named helper; Path is already imported). Regenerate all
profile modify scripts with the existing generator so express/review remain
byte-identical (no notify) and standard/deep gain the runtime expansion.

## Allowed files

- scripts/generate-agent-configs.py
- home/dot*codex/modify*\*.config.toml (generator output only — never
  hand-edit)
- home/dot_agents/agent-config.yaml ONLY if the placeholder syntax itself
  must change (prefer not; report if so)
- Your artifact paths (T48c five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; hardcoding
an absolute user path in any source file; vendor changes.

## Validation

1. `uv run --with pyyaml scripts/generate-agent-configs.py --check` green
   after regeneration.
2. Pipe the current ~/.codex/deep.config.toml through the NEW modify
   script locally (python3 modify_deep.config.toml < ~/.codex/deep.config.toml)
   and show the notify line contains the expanded real home path and NO
   '{{' remains. Same for standard; express/review outputs show no notify.
3. `make validate-agent-assets` green; `make format` still exit 0.
4. `git status --porcelain` / full `git diff` of generator + regenerated
   scripts.

## Completion / RESULT contract

Five artifacts (T48c). Report uses [memory:...] markers.
Reply AGMSG-RESULT v1 task_id=T48c. max_turns=15.
