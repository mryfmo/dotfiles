# T38 validation

```text
$ git log --oneline -2 chore/orchestration-evidence-t35-t37
44b01cb chore(mise): commit managed toolchain bump
f67f36d chore(orchestration): sync T35/T36/T37 evidence
```

```text
$ git show --stat --oneline f67f36d
22 files changed, 425 insertions(+)
All paths are under .orchestration/.

$ git show --stat --oneline 44b01cb
2 files changed, 99 insertions(+), 98 deletions(-)
home/dot_mise/config.toml
home/dot_mise/mise.lock
```

The worktree is back on `main`; only the pre-existing T37 tracked edits and untracked `.ua/` remain outside these commits.

## T39

```text
$ grep -F '"github:ogulcancelik/herdr" = "0.8.0"' home/dot_mise/config.toml
"github:ogulcancelik/herdr" = "0.8.0"

$ grep -F '"github:ogulcancelik/herdr" = "0.8.0"' tests/install/common/mise.bats
run grep -F '"github:ogulcancelik/herdr" = "0.8.0"' home/dot_mise/config.toml

$ git show --stat --oneline a635ba1
a635ba1 test(mise): align herdr pin with 0.8.0 toolchain bump
tests/install/common/mise.bats | 2 +-
1 file changed, 1 insertion(+), 1 deletion(-)
```

No local bats test was run, per task policy.
