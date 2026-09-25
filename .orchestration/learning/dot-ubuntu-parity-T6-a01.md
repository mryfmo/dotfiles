# dot-ubuntu-parity-T6-a01 — learning triage

## Reusable rule candidate

In chezmoi, `.chezmoiignore` always wins over `.chezmoiremove` for the same
target path — an ignored path is excluded from target-state computation
entirely, so it can never be declaratively removed via `.chezmoiremove`
while it stays ignored. Any future "remove this stale path" work must first
check whether the path is also matched by a `chezmoiignore.d/**` entry for
the relevant `os`/`system` combination; if so, `.chezmoiremove` is the wrong
tool and either manual cleanup or lifting the ignore is required instead.
This is the second time this session touched the ignore/remove pair for the
same path (T3/B7 added the now-removed entry without checking this), so it's
worth promoting from a one-off decision to something checked by default
whenever a future task edits `.chezmoiremove`. Recorded as CompactionDB
`[memory:decision]` id `e9d5e7c0-93f7-47c2-8899-25df46df03b9`.

Not promoting to `skills/candidates/` — this is a project-specific chezmoi
semantics fact, not a Claude/Codex workflow skill.
