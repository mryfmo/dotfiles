# pstack model configuration. One line per role; a role without a line falls back to the skill default.

# Generated from home/dot_agents/agent-config.yaml by scripts/generate-agent-configs.py. Change standing_rules.pstack_models there; chezmoi apply replaces any other write.

# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit the Agent tool's `model`). Alias entries in a panel list still count toward its fan-out.

# budget: standard (medium; the deep preset for the hardest tenth)

feature, refactoring: inherit-parent
bug-fix: inherit-parent
perf-issue: inherit-parent
hillclimb: inherit-parent
judgment and prose: opus medium
hardest tasks: fable high
how explorer: inherit-parent
how explainer: opus medium
why investigators: inherit-parent
why synthesizer: opus medium
reflect tooling: inherit-parent
reflect judgment, divergent, synthesizer: opus medium
arena runners: opus medium, inherit-parent
arena cross-judge pool: opus medium, inherit-parent
swarm workers: inherit-parent
architect runners: opus medium, inherit-parent
interrogate reviewers: opus medium, inherit-parent
