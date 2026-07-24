# T13 validation evidence

## Required commands

### `git branch --show-current`

Exit: 0

```text
rule/agmsg-orchestration
```

### `git status --short -- home/dot_config/claude/rules/`

Exit: 0

```text
?? home/dot_config/claude/rules/agmsg-orchestration.md
```

### `wc -l home/dot_config/claude/rules/agmsg-orchestration.md`

Exit: 0

```text
      16 home/dot_config/claude/rules/agmsg-orchestration.md
```

## Additional checks

- `git diff --cached --name-only`: exit 0, no output; nothing is staged.
- `git rev-parse main HEAD`: both resolve to `8e25a4fad4cf76fc61113280a86091485ec9935f`; the branch was created from current `main`.
- Structure check after revision: `headings=1 bullets=14`.
- The 16-line file is below the 40-line target.
- `make require-crit-review` was not run because the task explicitly forbids it and reserves it for orchestrator integration.

## Revision validation

The three required commands were re-run after adding the delivery/liveness rules. All exited 0 with the outputs recorded above; the rule remains the only rules-directory change and remains untracked.

## Supplemental validation

### `cat home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl`

Exit: 0

```text
{{ .chezmoi.sourceDir }}/dot_config/claude/rules/agmsg-orchestration.md
```

### `cat home/dot_claude/rules/symlink_ponytail.md.tmpl`

Exit: 0

```text
{{ .chezmoi.sourceDir }}/dot_config/claude/rules/ponytail.md
```

### `git status --short -- home/dot_config/claude/rules/ home/dot_claude/rules/`

Exit: 0

```text
 M home/dot_claude/rules/symlink_ponytail.md.tmpl
?? home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl
?? home/dot_config/claude/rules/agmsg-orchestration.md
```

The original branch, rule status, and line-count validations were also re-run and remain unchanged. `git diff --cached --name-only` remains empty.

## Authorized commit

Commit hash:

```text
c4f80cf0f02d71c7414fe92230290068f4ae09da
```

### `git show --stat HEAD`

```text
commit c4f80cf0f02d71c7414fe92230290068f4ae09da
Author: mryfmo <mryfmo@gmail.com>
Date:   Fri Jul 17 08:09:08 2026 +0900

    feat(claude-rules): add agmsg orchestration rule and fix ponytail symlink
    
    Codify the Claude-orchestrator / Codex-worker agmsg regime as an always-on rule: delegation boundaries, delivery/liveness via both-mode + Monitor, and unique identity/registration convention. Fix the dead home/home ponytail rule symlink target.
    
    Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

 .../dot_claude/rules/symlink_agmsg-orchestration.md.tmpl |  1 +
 home/dot_claude/rules/symlink_ponytail.md.tmpl           |  2 +-
 home/dot_config/claude/rules/agmsg-orchestration.md      | 16 ++++++++++++++++
 3 files changed, 18 insertions(+), 1 deletion(-)
```

The scoped rules status is clean after commit. No push was performed.
