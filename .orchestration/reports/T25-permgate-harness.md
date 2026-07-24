# T25 permgate harness report

## Outcome

`permgate` is a repository-owned PermissionRequest gate for Claude Code and
Codex. It evaluates a versioned deterministic policy first, then invokes the
originating agent's official authenticated CLI (`claude -p` or `codex exec`)
for bounded classification. Unknown or failed classifications return no hook
decision so the native permission prompt remains authoritative.

Both provider layers ship in shadow mode (`llm_enabled: false`). They can
record a would-be allow but cannot approve a request in this change.

Pull request: [mryfmo/dotfiles#92](https://github.com/mryfmo/dotfiles/pull/92)
at head `bdfd6b2`.

## Official hook contracts

Sources:

- [Claude Code PermissionRequest hooks](https://code.claude.com/docs/en/hooks#permissionrequest)
- [Claude Code CLI flags](https://code.claude.com/docs/en/cli-usage)
- [Codex PermissionRequest hooks](https://learn.chatgpt.com/docs/hooks#permissionrequest)

Claude Code sends this event shape:

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "PermissionRequest",
  "tool_name": "string",
  "tool_input": {},
  "permission_suggestions": []
}
```

`permission_suggestions` is optional. Codex sends:

```json
{
  "session_id": "string",
  "turn_id": "string",
  "transcript_path": "string|null",
  "cwd": "string",
  "permission_mode": "string",
  "hook_event_name": "PermissionRequest",
  "model": "string",
  "tool_name": "string",
  "tool_input": {}
}
```

Both harnesses accept the same explicit allow/deny output:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow"
    }
  }
}
```

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "deny",
      "message": "reason"
    }
  }
}
```

Exit 0 with no stdout means permgate has made no decision and the native
permission flow continues. Permgate does not emit `updatedInput`,
`updatedPermissions`, or `interrupt`.

## Design

- The executable is stdlib-only Python launched by
  `uv run --no-cache --script`.
- `home/dot_agents/permgate-policy.yaml` is JSON-compatible YAML and is the
  single source for categories, prompt, model, timeout, enablement, and
  deterministic patterns. Keeping it standalone avoids adding a runtime YAML
  dependency; the agent manifest remains the source only for hook wiring.
- Layer 1 checks deny rules before allow rules. Shell composition and
  write-capable read-command options are excluded from automatic allow.
- Layer 2 routes Claude events to a dated Haiku model through `claude -p` with
  customizations and tools disabled. Codex events route to the repository's
  low-cost Codex model through ephemeral, read-only `codex exec` with user
  config, rules, and hooks disabled. `PERMGATE_INNER=1` remains a backstop.
- Classifiers receive only a policy-listed normalized action and argument/
  option counts. Raw commands, values, patches, and structured inputs never
  cross the classifier boundary.
- A schema-valid category/confidence is accepted only when the deterministic
  policy assigns that normalized action to the returned category. The LLM
  never denies and cannot make write actions eligible.
- Missing CLI, non-zero exit, malformed JSON, timeout, invalid policy, unsafe
  options, sensitive structured input, or a log-write failure cannot allow.
- Audit JSONL stores a SHA-256 input hash, bounded operation summary, provider,
  normalized action, status, category, confidence, and shadow decision, not
  arguments, full commands, outputs, or structured values.

## Metrics-derived deterministic policy

Corrected state source: the installed ccgate state under the normal user HOME
with `XDG_STATE_HOME` unset. The 2026-07-18 through 2026-07-24 aggregates were:

- Codex: 370 fallthroughs — `apply_patch` 268, `Bash` 102.
- Claude: 9 fallthroughs — `Bash` 7, `Monitor` 2.

The aggregate store does not retain command rows. Prefix counts were therefore
derived separately from local Codex approval records and Claude Bash tool-use
records without copying request bodies:

| Pattern | Codex count | Claude count |
| --- | ---: | ---: |
| `gh pr view/checks/diff` | 112 | 20 |
| `gh run list/view` | 17 | 6 |
| `gh repo view` | 11 | 0 |
| `git status` | 3 | 0 |
| `git diff` | 1 | 7 |
| `git branch --show-current/--list` | 5 | 0 |
| `git remote get-url` | 1 | 0 |
| process inspection (`ps`/`pgrep`/`sysctl`) | 6 | 0 |

The policy records these counts on each pattern. Version checks are a
conservative zero-count seed. Recursive root deletion is the single
deterministic deny safety invariant.

## Wiring and merge behavior

`home/dot_agents/agent-config.yaml` generates:

- Claude: `~/.local/bin/common/permgate claude`
- Codex: `{{ .chezmoi.homeDir }}/.local/bin/common/permgate codex`

Explicit installed paths are required because the managed Codex hook
environment does not guarantee `~/.local/bin/common` on PATH. The obsolete
removed-prefix rule was deleted: the managed PermissionRequest table now wins
normal merge precedence, and a regression test proves that a stale private
`ccgate codex` table cannot survive.

The Claude settings merge now treats `PermissionRequest` as managed rather
than additive, so a stale current `ccgate claude` hook cannot survive beside
permgate.

Existing Claude deny/ask rules and Codex permission configuration were not
changed. The ccgate mise package also remains installed, but no hook invokes
it.

## Review outcome

Native review found eight security/correctness issues: write-capable
`git diff` options, structured secrets reaching the classifier, structured
secrets reaching log summaries, a hook PATH mismatch, Authorization/Bearer
secrets reaching the classifier, and interpreter execution of a script named
`version` being mistaken for a version check. CodeRabbit additionally identified
Cookie/basic-auth URL credential forms and incomplete classifier-policy
validation. All eight received regression tests and fixes. The findings were
recorded and resolved in local review data, and the guarded
`make require-crit-review` passed.

All GitHub Actions and the CodeRabbit status passed on the final head. All four
GitHub review threads are resolved. The PR remains open and unmerged pending
AGMSG acceptance.

## Adversarial repair

A later adversarial review rejected the Claude-only classifier architecture.
The repair added origin-specific official CLI adapters, removed raw classifier
payloads, bounded every eligible action to exactly one safe category, made
provider enablement independent, recorded reviewable shadow metadata, added
success and p50/p95 readiness gates, pinned the Claude model to a dated ID, and
closed the stale Claude hook migration gap.

The corrected live five-run bench reached neither provider's enablement gate:

- Claude: 2/5 successful, p50 6071 ms, p95 7032 ms.
- Codex: 3/5 successful, p50 4911 ms, p95 6859 ms.

Both remain shadow-only. These failures are an enforced operational gate, not
a reason to bypass existing auth or weaken the classifier boundary.
