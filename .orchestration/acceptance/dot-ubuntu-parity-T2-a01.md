# dot-ubuntu-parity-T2-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot (adversarial re-derivation)
evidence:
  - branch commits 720a3fd f9223d9 fce3fc3 aaef350 352833b 70c5967 (+ dac183f artifacts) — all reviewed by full diff
  - independent re-run: make validate-agent-assets ok; make unit-test Ran 376 OK (skipped=1) — matches worker claim
  - rendered codex-config-managed.toml:126 keys trust with {{ .chezmoi.workingTree }}; zero /Users/mryfmo hits
  - branch touched only allowed_files; main worktree untouched (status clean); MISE_CONFIG_DIR scoping verified
  - validation file contains verbatim outputs incl. CompactionDB memory id 6c8f2285-58bb-444e-a028-dd0c09a9141f
judgment_calls_endorsed:
  - stale github:mikefarah/yq lock entry kept (out-of-scope test hardcodes it) → follow-up B2b in T3
  - sheldon ubuntu.toml kept as empty include target (plugins.toml.tmpl unconditional include) → endorsed
  - B6 unquoted absolute path (test_herdr_agents literal assertion) → endorsed
follow_ups_routed_to_T3:
  - B0b: pre-existing shfmt drift breaks make format (executable_contextdb-codex-notify, executable_herdr-agents)
  - B2b: move test_supply_chain_policy.py:229 to aqua:mikefarah/yq and prune stale lock entry
cost: n/a (worker runtime exposes no figures)
