# Acceptance: test (S6 fixture)

```text
4244128846	class-count-scope
4244175775	class-count-scope
audit:3a54d34:2	class-count-scope
4244248692	threat-row-outside-paths
```

search: class-count-scope: uv run --no-project .claude/hooks/contextdb_cli.py memory search class-count-scope; grep -rl class-count-scope .orchestration/acceptance .orchestration/learning
