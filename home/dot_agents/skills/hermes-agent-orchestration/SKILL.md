---
name: hermes-agent-orchestration
description: Run Hermes as the orchestrator for parallel Codex and Claude Code work, backed by shared Cognee MCP memory.
---

# Hermes agent orchestration

Use this skill when Hermes delegates coding or review work to Codex and Claude Code, especially when both agents should use the same Cognee memory backend.

## Architecture

- Hermes is the orchestrator.
- Codex and Claude Code are peer coding agents.
- Cognee MCP is the shared long-term memory access layer.
- Cognee should run as a long-lived HTTP MCP server, not as one stdio process per agent.

Recommended flow:

```text
Hermes
├── recall/search Cognee memory
├── start Codex task
├── start Claude Code task
├── compare results
└── remember only durable facts

Codex ───────┐
Claude Code ─┼── Cognee MCP HTTP server ── shared memory backend
Hermes ──────┘
```

## Memory policy

Before delegating:

1. Recall project and user facts from Cognee.
2. Add only the relevant memory summary to each agent prompt.
3. Tell both agents to use Cognee recall/search before repository-specific decisions.

After delegation:

1. Save durable findings only.
2. Do not save raw logs, transient CI state, temporary todo lists, secrets, keys, tokens, or email addresses.
3. Do not allow delegated agents to run destructive memory operations such as prune/delete unless the user explicitly requests it.

Recommended Cognee datasets:

- `user_profile`: stable user preferences. Hermes writes; delegated agents mostly read.
- `project_dotfiles`: repository-specific conventions and pitfalls.
- `agent_operations`: reusable Codex, Claude Code, Hermes, MCP, CI, and workflow lessons.
- `session_cache`: temporary context that may later be promoted with `improve`.

## Parallel execution policy

Use parallel Codex and Claude Code work when:

- The task is a review, design comparison, implementation proposal, or bug analysis.
- Implementation can be split into independent worktrees.
- You want two independent model/tooling perspectives before applying changes.

Do not run both agents as writers in the same worktree. For implementation tasks, create separate branches/worktrees first, or designate one agent as writer and the other as reviewer.

## Hermes → Codex prompt template

```text
You are Codex working under Hermes orchestration.
Use gpt-5.5 and the configured MCP servers.
Before repository-specific decisions, use Cognee recall/search for relevant project memory.
Do not store secrets, tokens, email addresses, raw logs, temporary PR state, or transient todos.
Do not delete, prune, or forget memory.
At the end, store only durable technical facts that will help future sessions.
Return: summary, files changed, tests run, risks, and durable facts worth saving.

Task:
{task}
```

## Hermes → Claude Code prompt template

```text
You are Claude Code working under Hermes orchestration.
Use the configured MCP servers.
Before repository-specific decisions, use Cognee recall/search for relevant project memory.
Do not store secrets, tokens, email addresses, raw logs, temporary PR state, or transient todos.
Do not delete, prune, or forget memory.
At the end, store only durable technical facts that will help future sessions.
Return: summary, files changed, tests run, risks, and durable facts worth saving.

Task:
{task}
```

## Command patterns

Read-only parallel comparison in the current worktree:

```bash
agent-fanout "Review the current diff and propose fixes. Do not edit files."
```

Implementation with isolation:

1. Create one branch/worktree for Codex.
2. Create one branch/worktree for Claude Code.
3. Start Codex in the Codex worktree.
4. Start Claude Code in the Claude worktree.
5. Compare diffs and tests.
6. Apply the selected changes to the final branch.

## Verification

After agent work finishes:

1. Inspect `git diff --stat` and `git diff`.
2. Run repository-specific validators.
3. Save only durable memory facts to Cognee.
4. Keep Hermes built-in memory for compact, high-confidence user preferences and environment facts.
