# T32 validation

Worktree: `/Users/mryfmo/Workspace/dotfiles-t32`

```text
$ git log --oneline origin/main..HEAD
7bc4a5b docs(rules): codify evidence sync and tool bump timing
cae7228 chore(orchestration): sync T30/T31 evidence
4082e29 chore(mise): bump managed claude-code to 2.1.219

$ git show --stat --oneline 4082e29
4082e29 chore(mise): bump managed claude-code to 2.1.219
 home/dot_mise/config.toml | 2 +-
 home/dot_mise/mise.lock   | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)

$ git show --stat --oneline cae7228
cae7228 chore(orchestration): sync T30/T31 evidence
12 files changed, 319 insertions(+)

$ git show --stat --oneline 7bc4a5b
7bc4a5b docs(rules): codify evidence sync and tool bump timing
 home/dot_config/claude/rules/agmsg-orchestration.md | 1 +
 1 file changed, 1 insertion(+)

$ cmp <main source> <t32 copy>  # repeated for 2 mise + 12 evidence files
(no output; all 14 copied files are byte-identical)

$ git status --short
(no output; clean)

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
```
