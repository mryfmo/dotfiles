---
task: dotfiles-T133-task-generator-plan-check-a01
head: 9da0ed3fe67fd1f9267c56fcdcb7e5aaaaa9ffab
pr: 417
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T21:17:15Z
finished: 2026-10-18T21:25:52Z
findings: 7
engine: codex review --base main (profile review, read-only)
---

- [P2] Classify glob matches before deciding whether C12 applies — scripts/orchestrator/task-consistency-check.py:182-186
- [P2] Detect intersections between two glob allowlists — scripts/orchestrator/plan-check.py:94-99
- [P2] Match complete todo IDs when selecting a wave — scripts/orchestrator/task-from-plan.py:157-159
- [P2] Preserve glob paths in generated allowed_files — scripts/orchestrator/task-from-plan.py:123-124
- [P2] Read each program item through its next numbered heading — scripts/orchestrator/task-from-plan.py:72-75
- [P2] Read the current acceptance status instead of the last textual match — scripts/orchestrator/plan-check.py:155-158
- [P2] Retain premise commands whose executables are unavailable — scripts/orchestrator/task-from-plan.py:67-69

```text
Read-only probes reproduced missed glob conflicts, incomplete generated tasks, incorrect wave selection, and false acceptance drift. All changed Python files parsed successfully; the filesystem-writing unit suite was not run.

Full review comments:

- [P2] Classify glob matches before deciding whether C12 applies — scripts/orchestrator/task-consistency-check.py:182-186
  An allowlist such as `install/**` matches executable shell scripts, but this condition skips C12 because the pattern itself has no applied-file suffix and starts outside the four listed directories. A task with only one aggregate installer row therefore passes without per-file threat rows. Classify the matched files instead, preserving the wildcard row-unit requirement invoked by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Detect intersections between two glob allowlists — scripts/orchestrator/plan-check.py:94-99
  Matching each pattern against the other pattern's text does not establish disjointness. For example, `scripts/orchestrator/task-*.py` and `scripts/orchestrator/*check.py` both permit the existing `task-consistency-check.py`, but neither matches the other's literal spelling, so F2 reports no conflict. Resolve concrete matches or otherwise calculate pattern intersections before allowing these tasks in the same wave.

- [P2] Preserve glob paths in generated allowed_files — scripts/orchestrator/task-from-plan.py:123-124
  Explicit paths such as `config/*.toml` and `.githooks/*` are rejected by this character whitelist and silently disappear from the generated scope. The subsequent script-name grep does not recover these configuration or hook patterns; a fixture naming only `config/*.toml` produces an allowlist containing only the evidence directory. Preserve valid glob paths or expand them into concrete entries before drafting the threat rows.

- [P2] Match complete todo IDs when selecting a wave — scripts/orchestrator/task-from-plan.py:157-159
  This substring test treats `P1-1` as present in a cell naming `P1-10`, `P1-11`, or `P1-12`. If such a row precedes the actual `P1-1` row, the generator selects the wrong wave and copies Check commands from unrelated sibling tasks. Match complete todo-ID tokens rather than searching for the raw substring.

- [P2] Read each program item through its next numbered heading — scripts/orchestrator/task-from-plan.py:72-75
  A blank line ends the item here, even when subsequent paragraphs or fenced examples still belong to it. For an item containing a heading, a blank line, and `Run `printf known-output``, the generated Files section omits the command paragraph and `premises` is empty. Read until the next numbered item so ordinary Markdown paragraph breaks do not silently discard specifications and premise commands.

- [P2] Retain premise commands whose executables are unavailable — scripts/orchestrator/task-from-plan.py:67-69
  When an item quotes a command whose tool is unavailable, such as `no-such-tool-a01 --help`, this predicate rejects it before the generator reaches its failed-command handling. The generated task consequently contains neither the premise nor the promised `verify:` claim and exit code. Identify command candidates independently of executable availability, then record execution failures instead of silently omitting them.

- [P2] Read the current acceptance status instead of the last textual match — scripts/orchestrator/plan-check.py:155-158
  Existing acceptance records place their final dispatch in front matter and older bus messages in a later appendix, so the last textual match is not necessarily the latest status. For example, `dotfiles-T128-settings-hook-dedupe-followup-a01.md` records final acceptance above an older `pending-integration` message; an accurate `accepted` progress row is therefore reported as drift. Read the authoritative dispatch data for the matching task rather than relying on document order.
Read-only probes reproduced missed glob conflicts, incomplete generated tasks, incorrect wave selection, and false acceptance drift. All changed Python files parsed successfully; the filesystem-writing unit suite was not run.

Full review comments:

- [P2] Classify glob matches before deciding whether C12 applies — scripts/orchestrator/task-consistency-check.py:182-186
  An allowlist such as `install/**` matches executable shell scripts, but this condition skips C12 because the pattern itself has no applied-file suffix and starts outside the four listed directories. A task with only one aggregate installer row therefore passes without per-file threat rows. Classify the matched files instead, preserving the wildcard row-unit requirement invoked by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Detect intersections between two glob allowlists — scripts/orchestrator/plan-check.py:94-99
  Matching each pattern against the other pattern's text does not establish disjointness. For example, `scripts/orchestrator/task-*.py` and `scripts/orchestrator/*check.py` both permit the existing `task-consistency-check.py`, but neither matches the other's literal spelling, so F2 reports no conflict. Resolve concrete matches or otherwise calculate pattern intersections before allowing these tasks in the same wave.

- [P2] Preserve glob paths in generated allowed_files — scripts/orchestrator/task-from-plan.py:123-124
  Explicit paths such as `config/*.toml` and `.githooks/*` are rejected by this character whitelist and silently disappear from the generated scope. The subsequent script-name grep does not recover these configuration or hook patterns; a fixture naming only `config/*.toml` produces an allowlist containing only the evidence directory. Preserve valid glob paths or expand them into concrete entries before drafting the threat rows.

- [P2] Match complete todo IDs when selecting a wave — scripts/orchestrator/task-from-plan.py:157-159
  This substring test treats `P1-1` as present in a cell naming `P1-10`, `P1-11`, or `P1-12`. If such a row precedes the actual `P1-1` row, the generator selects the wrong wave and copies Check commands from unrelated sibling tasks. Match complete todo-ID tokens rather than searching for the raw substring.

- [P2] Read each program item through its next numbered heading — scripts/orchestrator/task-from-plan.py:72-75
  A blank line ends the item here, even when subsequent paragraphs or fenced examples still belong to it. For an item containing a heading, a blank line, and `Run `printf known-output``, the generated Files section omits the command paragraph and `premises` is empty. Read until the next numbered item so ordinary Markdown paragraph breaks do not silently discard specifications and premise commands.

- [P2] Retain premise commands whose executables are unavailable — scripts/orchestrator/task-from-plan.py:67-69
  When an item quotes a command whose tool is unavailable, such as `no-such-tool-a01 --help`, this predicate rejects it before the generator reaches its failed-command handling. The generated task consequently contains neither the premise nor the promised `verify:` claim and exit code. Identify command candidates independently of executable availability, then record execution failures instead of silently omitting them.

- [P2] Read the current acceptance status instead of the last textual match — scripts/orchestrator/plan-check.py:155-158
  Existing acceptance records place their final dispatch in front matter and older bus messages in a later appendix, so the last textual match is not necessarily the latest status. For example, `dotfiles-T128-settings-hook-dedupe-followup-a01.md` records final acceptance above an older `pending-integration` message; an accurate `accepted` progress row is therefore reported as drift. Read the authoritative dispatch data for the matching task rather than relying on document order.
```
