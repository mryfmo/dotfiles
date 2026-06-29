{
  // Generated from home/dot_agents/agent-config.yaml by scripts/generate-agent-configs.py.
  ['$schema']: "https://raw.githubusercontent.com/tak848/ccgate/main/schemas/claude.schema.json",
  provider: {
    name: 'anthropic',
    model: 'claude-haiku-4-5',
  },
  fallthrough_strategy: 'ask',
  append_environment: [
    'ccgate claude is an LLM-backed PermissionRequest gate. Its purpose is to automate clear permission prompts while preserving safety, human review, and useful feedback to the agent.',
    'The provider model is the ccgate classifier model, not the active Claude Code task model. Keep permission classification on a small structured-output model and do not spend premium task models on gating.',
    'Claude Code PermissionRequest input does not expose the active task model. Model governance for Claude Code must come from settings and agent rules; ccgate can only judge the requested tool action and return allow, deny, or fallthrough.',
    'Prefer fallthrough for ambiguous model-proportionality decisions in interactive TUI sessions. Use metrics later to tune repeated fallthrough or deny patterns.',
  ],
  append_allow: [
    'Allow focused read-only inspection, search, status, diff, and version checks when they support the current task and do not expose secrets, escalate privilege, modify files, or access the network.',
  ],
  append_deny: [
    'Deny only when the requested action is clearly unsafe, overbroad, destructive, privileged, network-executing without explicit need, or too broad to be a permission-safe unit. deny_message: Narrow the operation and choose the smallest Claude Code model adequate for the task before retrying.',
  ],
}
