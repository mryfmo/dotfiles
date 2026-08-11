# T40 validation

```text
$ uv run --with pyyaml scripts/generate-agent-configs.py
generated agent configs updated

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok

$ python3 -m py_compile scripts/generate-agent-configs.py scripts/validate-agent-assets.py
exit 0
```

The new search-first guidance was found in all three targets:

```text
home/dot_config/claude/rules/understand-anything.md
home/dot_config/codex/AGENTS.md
home/dot_claude/agents/express-explorer.md
```

Before commit 2, `git status --short .ua/` showed exactly:

```text
A  .ua/.understandignore
A  .ua/config.json
A  .ua/fingerprints.json
A  .ua/knowledge-graph.json
A  .ua/meta.json
```

Commit stats:

```text
49b1cdd feat(agents): route agent search through the understand-anything graph
5 files changed, 6 insertions(+), 1 deletion(-)

074fb41 chore(ua): commit knowledge graph baseline with auto-update
6 files changed, 32161 insertions(+)
```

`make require-crit-review` in the feature worktree reported: `Review not required: no meaningful review trigger found.`
