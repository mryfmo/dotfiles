# dot-crit-linux-T1-a01 learning triage

## Validated reusable learning

- Crit Linux release binaries report `crit v<version>`, while the Homebrew build reports `crit <version>`. Cross-acquisition checks must normalize one optional leading `v` on token two.
- A `RETURN` trap created inside a function can outlive that function's local cleanup variables and later fail under `set -u`. Use a subshell helper with an `EXIT` trap for download/staging cleanup.
- The learning was recorded in `.agents/worklog/codex/learn/20260921_150957_learn.md` and indexed.

## Follow-up candidate

- If full `remove-agent-asset ensure_crit_cli` support is desired, separately expand scope to allow the guarded remover to accept exactly `~/.local/bin/crit`. This task uses the approved documented reverse operation `rm ~/.local/bin/crit`.

## Skill decision

- No new or promoted skill is warranted. The finding is a project-specific installer/test rule, not a cross-project workflow package.
