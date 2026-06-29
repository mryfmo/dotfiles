{
  // Generated from home/dot_agents/agent-config.yaml by scripts/generate-agent-configs.py.
  ['$schema']: "https://raw.githubusercontent.com/tak848/ccgate/main/schemas/codex.schema.json",
  provider: {
    name: 'anthropic',
    model: 'claude-haiku-4-5',
  },
  fallthrough_strategy: 'ask',
  append_environment: [
    'ccgate codex is an LLM-backed PermissionRequest gate. Its purpose is to automate clear permission prompts while preserving safety, human review, and useful feedback to the agent.',
    'The provider model is the ccgate classifier model, not the active Codex task model. Keep permission classification on a small structured-output model and do not spend premium task models on gating.',
    'Codex HookInput.model is available. Use it as proportionality context, not as a deterministic block. Premium models such as gpt-5.5, gpt-5, and reasoning-tier models are appropriate for architecture, ambiguous debugging, multi-file design, security-sensitive review, and high-stakes decisions.',
    'Do not deny necessary read-only inspection, search, or small setup commands solely because a premium model is active. Those operations are often part of a larger task that legitimately needs the active model.',
    'Prefer fallthrough for ambiguous model-proportionality decisions in interactive TUI sessions. Use metrics later to tune repeated fallthrough or deny patterns.',
  ],
  append_allow: [
    'Allow focused read-only inspection, search, status, diff, and version checks when they support the current task and do not expose secrets, escalate privilege, modify files, or access the network.',
  ],
  append_deny: [
    'Deny only when the requested action is clearly unsafe, overbroad, destructive, privileged, network-executing without explicit need, or a repeated trivial operation under a premium active model that is unrelated to any complex user task. deny_message: Narrow the operation or switch to a smaller model before retrying; ccgate should guide model proportionality without blocking necessary task inspection.',
  ],
}
