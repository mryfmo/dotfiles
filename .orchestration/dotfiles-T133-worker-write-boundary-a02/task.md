---
format: 2
task_id: dotfiles-T133-worker-write-boundary-a02
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - home/.chezmoitemplates/claude-worker-settings.json
  - home/.chezmoitemplates/claude-managed-settings.json
  - home/dot_claude/modify_private_settings.json
  - home/dot_claude-worker/modify_private_settings.json
  - home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
  - .claude/settings.json
  - scripts/generate-agent-configs.py
  - scripts/validate-agent-assets.py
  - Makefile
  - home/dot_local/bin/common/executable_herdr-agents
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - .gitignore
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_validate_agent_assets.py
  - tests/unit/test_claude_settings_merge.py
  - tests/unit/test_herdr_agents.py
  - tests/unit/test_agmsg_orchestration_docs.py
  - tests/unit/test_claude_worker_settings.py
  - tests/unit/test_claude_managed_settings.py
  - .orchestration/dotfiles-T133-worker-write-boundary-a02/**
after: []
reset_of: [dotfiles-T133-worker-write-boundary-a01]
threat_table:
  - control: home/dot_agents/agent-config.yaml
    disposition: "residual: the manifest separates worker policy and enumerates protected executable inputs statically; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy and tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest check both platforms without establishing same-UID isolation or executable binding."
  - control: home/.chezmoitemplates/claude-settings-managed.json
    disposition: "residual: the orchestrator baseline adds startup failure, hook failure policy and sanitized non-PermissionRequest commands while retaining the legacy PermissionRequest command; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the retained policy, and dotfiles-T133-trusted-entrypoint-binding-a01 owns the unbound PermissionRequest execution."
  - control: home/.chezmoitemplates/claude-worker-settings.json
    disposition: "residual: dedicated settings provide static trusted-path and worktree-configuration denies, restricted writes, minimal trusted delivery hooks, project-MCP auto-approval disables, explicit plugin disables and native merge denials; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the user baseline separately from shared managed capabilities and higher-scope overrides."
  - control: home/.chezmoitemplates/claude-managed-settings.json
    disposition: "residual: operator installation establishes the documented administrative sandbox scope; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox checks its content without claiming live enforcement or per-seat removal of shared exclusions and socket access."
  - control: home/dot_claude/modify_private_settings.json
    disposition: "residual: classification follows the managed non-PermissionRequest prefix and guard forms so upgrades replace stale managed hooks without consuming custom hooks; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_prefixed_guarded_managed_hooks_replace_legacy_hooks_idempotently checks migration and repeated merging while PermissionRequest retains its existing classification."
  - control: home/dot_claude-worker/modify_private_settings.json
    disposition: "residual: the separate renderer replaces stale worker-managed policy without importing orchestrator hooks or credentials; the common executable-field policy also covers legacy migration and preserved user fields, while tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks temporary-HOME deployment."
  - control: home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    disposition: "residual: the rendered guard checks canonical launch identity and fixed operation selection before project payload execution, with only fixed installed worker-delivery operations admitted for worker roots; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks project suppression and anchored fixture execution, while complete executable and formatter-tool binding belongs to dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: .claude/settings.json
    disposition: "residual: portable guarded commands and explicit clean-environment re-exports reduce worker-triggered project-hook execution; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure traverses every tracked entry without establishing complete descendant binding."
  - control: scripts/generate-agent-configs.py
    disposition: "residual: deterministic generation uses the static manifest inventory and emits separate user and administrative policies without consulting Git objects or discovering executable installations; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest checks correspondence and filesystem coverage."
  - control: scripts/validate-agent-assets.py
    disposition: "residual: the exclusion validator requires the same exact three-entry list on both platforms and preserves the existing legacy PermissionRequest check; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form covers exclusion failures while structural bound-PermissionRequest validation remains owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: Makefile
    disposition: "residual: the installation target stages administrative settings and prints the platform-specific sudo command without executing it; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo checks both destinations and the absence of privileged execution."
  - control: home/dot_local/bin/common/executable_herdr-agents
    disposition: "residual: one pre-start procedure screens every source class enumerated in premises, before workspace trust, migration or launch, and refuses noncanonical executable payloads with their source and key; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks complete fixture coverage without closing same-UID consumption races or later configuration changes."
  - control: home/dot_agents/skills/agmsg-orchestration/SKILL.md
    disposition: "residual: Worker Playbook step 4 gives one sandbox-only rule and blocked-PONG outcome with no worker exception anywhere in that playbook; evidence-sync writes, CompactionDB consolidation and agmsg-dispatch exemptions belong only to the orchestrator section, checked by tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_worker_playbook_has_no_sandbox_exceptions without claiming shared managed capabilities are unavailable."
  - control: .gitignore
    disposition: "residual: ignoring .uv-cache reduces accidental publication of worker cache contents; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
  - control: tests/unit/test_generate_agent_configs.py
    disposition: "residual: platform, static-inventory and guarded-command fixtures verify generated configuration and retain the existing literal PermissionRequest expectations without claiming live permission enforcement or bound executable identity."
  - control: tests/unit/test_validate_agent_assets.py
    disposition: "residual: exclusion cases and the corrected valid_claude_sandbox fixture exercise the retained policy checks while the existing PermissionRequest and hook-composition fixtures continue to use the legacy managed command."
  - control: tests/unit/test_claude_settings_merge.py
    disposition: "residual: migration fixtures cover prefixed and guarded managed SessionStart and PostToolUse commands, stale-ccgate removal, custom-hook preservation and idempotence without introducing bound PermissionRequest forms or native-binding expansion."
  - control: tests/unit/test_herdr_agents.py
    disposition: "residual: fake launchers and subprocess markers check every launch route and documented source class, old tracked settings, executable-field refusal, legacy migration, plugin disables, hook placement, sanitized delivery environments, caches and native denials without starting live seats or verifying the removed binding family."
  - control: tests/unit/test_agmsg_orchestration_docs.py
    disposition: "residual: assertions check the exact step 4 sentence, absence of worker escape instructions and placement of the retained exemptions in the orchestrator section; the complete module remains required."
  - control: tests/unit/test_claude_worker_settings.py
    disposition: "residual: fixtures check dedicated settings, project-MCP and plugin disables, protected policy bytes, narrow inventory, ordinary worktree writes and guard behavior without executing a bound PermissionRequest hook or claiming live Claude enforcement."
  - control: tests/unit/test_claude_managed_settings.py
    disposition: "residual: fixtures check administrative policy content, conflicting lower-scope settings and nonprivileged staging while real-uv hook execution and binary-identity deployment checks remain owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: .orchestration/dotfiles-T133-worker-write-boundary-a02/**
    disposition: "residual: branch artifacts distinguish inherited a01 observations, a02 final-head results, transferred binding work and pending operator deployment, and acceptance compares their claims with the final diff and CI."
  - control: <absolute-home>/.claude-worker/settings.json
    disposition: "residual: S01 is screened before regeneration, including preserved helpers and plugin selections; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_executable_settings_entrypoints_are_checked_before_launch checks refusal and unchanged bytes without preventing a later same-UID replacement."
  - control: <worktree>/.claude/settings.json
    disposition: "residual: S02 is screened even in an older reused worktree and is never silently rewritten; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_existing_worktree_with_unguarded_tracked_hook_is_refused_before_launch checks refusal before trust, spawn or payload execution."
  - control: <worktree>/.claude/settings.local.json
    disposition: "residual: S03 is screened before recognized legacy-hook migration can conceal an alternate executable field; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_executable_settings_entrypoints_are_checked_before_launch checks the legacy apiKeyHelper case and absent payload markers."
  - control: <anchored-checkout>/.claude/settings.local.json
    disposition: "residual: S04 is screened independently of worker-local settings because linked worktrees consume it; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_executable_settings_entrypoints_are_checked_before_launch checks refusal without treating dedicated user settings as an exclusion."
  - control: /Library/Application Support/ClaudeCode/managed-settings.json
    disposition: "residual: S05's Darwin file receives the same pre-start executable policy without administrative mutation; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch uses a temporary managed-root fixture rather than claiming live administrative enforcement."
  - control: /etc/claude-code/managed-settings.json
    disposition: "residual: S05's Linux file receives the same pre-start executable policy without administrative mutation; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks the Linux source fixture without starting a live seat."
  - control: <managed-root>/managed-settings.d/<name>.json
    disposition: "residual: every S06 drop-in is screened separately before settings precedence can hide its payload; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch plants a hook in one drop-in and checks named refusal."
  - control: <absolute-home>/.claude-worker/remote-settings.json
    disposition: "residual: S07's existing server-managed cache receives the common executable policy, and an additional managed delivery that cannot be enumerated before launch blocks startup; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks the cached-payload fixture without claiming control of later server updates."
  - control: <worktree>/.mcp.json
    disposition: "residual: S08 server definitions are screened independently of approval state and file tracking; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_existing_project_mcp_server_is_refused_before_launch checks refusal before trust or server execution."
  - control: <anchored-checkout>/.mcp.json
    disposition: "residual: S09 is screened when inherited, including when the worktree file is absent or empty; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_existing_project_mcp_server_is_refused_before_launch checks the main-checkout payload without relying on nearer definitions."
  - control: <loaded-ancestor>/.mcp.json
    disposition: "residual: each S10 ancestor file is screened independently, including intermediate and above-checkout ancestors the installed loader reads; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_existing_project_mcp_server_is_refused_before_launch checks an additional inherited source without closing consumption races."
  - control: <absolute-home>/.claude-worker/.claude.json
    disposition: "residual: S11 screening covers top-level user servers, project-keyed local servers and executable helpers without logging credentials or rewriting trust/authentication state; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_configuration_global_state_payload_is_refused_before_launch checks both MCP scopes and helper variants."
  - control: <skills-root>/<name>/.claude-plugin/plugin.json
    disposition: "residual: S12 descriptors and their implicit or declared executable components are checked even when worker user settings disable the plugin; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_skills_directory_plugin_payload_is_refused_before_launch checks worktree, dedicated-user and applicable main-checkout or managed roots without relying on workspace trust."
  - control: <plugins-root>/installed_plugins.json
    disposition: "residual: S13 install records cannot introduce an unchecked plugin root, scope or executable source; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks a planted installed-plugin payload before any plugin process runs."
  - control: <plugins-root>/known_marketplaces.json
    disposition: "residual: S14 command sources and executable header helpers refuse before marketplace refresh or plugin loading; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks refusal with the command marker absent."
  - control: <plugin-root>/.claude-plugin/plugin.json
    disposition: "residual: S15 inline commands and component references receive the same policy as settings, including implicitly loaded components; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks a planted manifest payload while complete executable binding remains deferred."
  - control: <plugin-hook-file>
    disposition: "residual: S16 covers each default or manifest-selected hooks JSON file separately, even under a disabled plugin; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch plants a command in each hook-file form and checks its source/key refusal."
  - control: <marketplace-root>/.claude-plugin/marketplace.json
    disposition: "residual: S17 plugin command sources, header helpers and local plugin selections cannot bypass the common pre-start policy; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks a marketplace-owned payload without fetching or installing it."
  - control: <plugin-mcp-file>
    disposition: "residual: S18 covers each default or manifest-selected MCP configuration file independently of plugin enablement; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks command/args refusal without starting a server."
  - control: <managed-root>/managed-mcp.json
    disposition: "residual: S19 managed MCP definitions receive the same no-unowned-server policy and are not exempted by administrative scope; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks the file through a temporary managed root."
  - control: <skills-root>/<name>/SKILL.md
    disposition: "residual: S20 executable frontmatter and dynamic shell expansion cannot introduce an unchecked command through a plain skill; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks a planted command without invoking the skill."
  - control: <commands-root>/<name>.md
    disposition: "residual: S21 legacy command files receive the same executable-frontmatter and dynamic-command policy as skills; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks refusal without invoking the command."
  - control: <agents-root>/<name>.md
    disposition: "residual: S22 subagent-frontmatter hooks receive the common executable policy before a worker can load them; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks the planted hook without starting a subagent."
  - control: <plugin-lsp-file>
    disposition: "residual: S23 default or manifest-selected language-server commands and arguments have no worker canonical operation and refuse; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks the selected file with an absent server marker."
  - control: plugin activation and additional executable components
    disposition: "residual: enabledPlugins, command-sourced plugins, dependency installation, workflow or monitor activation and caller-selected plugin roots cannot authorize code this launcher did not write; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks activation refusals, while post-start changes and upstream plugin execution remain outside a pre-start guarantee."
  - control: non-file managed delivery and launch overrides
    disposition: "residual: MDM policy, fresh server-managed delivery, host-supplied settings and CLI/environment source selectors must be enumerated under the same policy or produce a named refusal before launch; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch checks an unenumerable-source refusal without running policy helpers."
  - control: ~/.agents/permgate-policy.yaml
    disposition: "residual: an explicit static Edit deny protects the policy input reread by permgate, and tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_protect_permgate_policy checks denied writes and unchanged protected bytes without claiming environment isolation of the legacy hook."
  - control: ~/.local/lib/python*/site-packages
    disposition: "residual: explicit directory-target denies protect known user-site locations, and tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest checks the rendered patterns on both platforms."
  - control: ~/.local/lib/python*/site-packages/**
    disposition: "residual: descendant denies include .pth, usercustomize.py and sitecustomize.py fixtures, while execution-time Python isolation remains owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: ~/Library/Python/*/lib/python/site-packages
    disposition: "residual: explicit directory-target denies cover the macOS framework user-site location where used, without treating directory protection as proof of isolated interpreter startup."
  - control: ~/Library/Python/*/lib/python/site-packages/**
    disposition: "residual: descendant patterns protect macOS framework user-site startup files, and the inventory fixture checks their coverage while dotfiles-T133-trusted-entrypoint-binding-a01 owns the planted-startup execution test."
  - control: ~/.claude/hooks/orchestrator-only.sh
    disposition: "residual: the static inventory explicitly protects the installed guard as a consumed input, and inventory and guard fixtures check configured protection without closing concurrent same-UID path swaps."
  - control: formatter and project-map configuration selection
    disposition: "residual: the guard skips worker-repository and outside-anchor tool inputs before invoking these operations, while formatter PATH repair and actual tool-chain availability remain owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md
    disposition: "residual: C3 authorizes deletion of this predecessor task copy on the first a02 push only; the a01 implementation and canonical history remain, and no other predecessor artifact is edited."
  - control: .orchestration/dotfiles-T133-worker-write-boundary-a02/task.md
    disposition: "residual: the first a02 push adds the complete byte-identical dispatched text while deleting the predecessor copy, and TASK and RESULT bind this a02 copy by SHA256."
  - control: evidence records
    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, statuses and tested identities without credentials or literal operator home paths."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10, C7b and C11, the re-plan history, reset lineage, dispatched bytes and final-head PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE without treating local proposals as approval authority."
  - control: metadata separators
    disposition: "residual: the opening separators delimit format-2 metadata, and the task-copy SHA256 binds the complete front matter and body."
  - control: in-process effects
    disposition: "residual: generation and tests operate on repository files and temporary fixtures, and the worker performs no live deployment, login, administrative installation, permission-policy mutation or operator-session restart."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: non-PermissionRequest hook commands receive the prescribed clean prefix and fixed dispatch, and startup checks configuration-selected executable fields, while the legacy PermissionRequest, complete interpreter binding and deployment-check execution remain owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: new or renamed scripts
    disposition: "residual: the worker settings modify script and rendered guard have named source and installed paths, and this task adds no state-helper replacement, private executable-link manager, write-boundary hook or gh wrapper."
  - control: "5.14 item 0: host threat model"
    disposition: "residual: host controls reduce accidental and injected damage without separating same-UID seats, and P1-11 owns next-records-PR detection while separate-user or separate-host prevention remains the operator's future P1-16 decision."
  - control: "5.14 item 1: worker write controls"
    disposition: "residual: dedicated settings, static input-derived denies, restricted writes, one documented loading inventory, pre-trust executable-payload refusal, legacy migration and administrative sandbox policy reduce damage without establishing atomic protection against path-consumption races."
  - control: "5.14 item 2: sanitized environment and executable selection"
    disposition: "residual: canonical startup screening requires the clean prefix and fixed guarded operation for covered executable entries; the unchanged orchestrator managed PermissionRequest, exact interpreter selection and complete trusted-entrypoint binding remain owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: "5.14 item 3: trusted-path checks"
    disposition: "residual: guard fixtures check canonical launch and input identities including symlink and case aliases, while executable realpath binding belongs to dotfiles-T133-trusted-entrypoint-binding-a01 and other consuming helpers retain their own hardening owners."
  - control: "5.14 item 4: verified executable and consumed-byte identity"
    disposition: "residual: fixed guard operations avoid worker-selected project payloads, while executable identity belongs to dotfiles-T133-trusted-entrypoint-binding-a01 and snapshots and last-use digests remain with the consuming hardening tasks."
  - control: "5.14 item 5: output and reservation identity"
    disposition: "residual: this task introduces no reservation protocol, and full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator mechanisms that create them."
  - control: "5.14 item 6: honest residuals"
    disposition: "residual: the text retains same-UID, shared credential, managed exception, Herdr socket, agmsg sourcing, path-race and hook-event limitations and assigns executable-binding gaps to dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: "5.14 item 7: verification"
    disposition: "residual: retained render, merge, policy, guard, launch and cache tests plus one refusal fixture per documented source class provide final-head evidence, while real-uv hook execution belongs to dotfiles-T133-trusted-entrypoint-binding-a01 and the common trusted_exec_contract helper belongs to P1-6."
  - control: "5.14 item 8: committed approval ledger"
    disposition: "residual: P1-14 a05 obtains canonical main through the fixed-host, fixed-repository main-ref API and reads approval content at that full SHA; this task provides no authority from local files, remote configuration, refs or objects and no prevention of shared-credential API merges."
  - control: "5.14 item 9: private caches and isolated interpreters"
    disposition: "residual: private worker caches and explicit orchestrator-cache denies remain here, while exact uv/Python declarations, interpreter isolation, trusted resolver consumption and bound deployment checks belong to dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: "5.14 item 10: commands inside the sandbox"
    disposition: "residual: the worker execution rule has no exception and the retained exemptions are orchestrator-only; shared managed capabilities remain available and Codex network configuration and deterministic permgate deployment retain their separate owners."
  - control: hook handler type validation
    disposition: "residual: K01 inspects every handler's type before command lookup across S01-S07 and all other hook-bearing sources; only canonical command handlers pass, while HTTP, MCP-tool, prompt, agent, unknown and missing types refuse with source/event/index; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch plants command-free HTTP handlers per settings source class and checks absent markers without closing later reloads or same-UID replacement."
  - control: canonical GitHub API host binding
    disposition: "residual: both deferred-ledger API templates fix --hostname github.com and repos/mryfmo/dotfiles endpoints; tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host records both argv vectors under hostile GH_HOST and checks refusal without a host-bindable gh, while P1-14 a05 and P1-6 own consuming-path enforcement and credentials remain shared."
  - control: hook failure policy
    disposition: "residual: generated, tracked and launcher-managed entries carry onFailure block where supported, but template tests do not establish runtime timeout enforcement and background or excluded events carry no enforcement responsibility."
  - control: agmsg store driver and plugin selection
    disposition: "residual: plugin and trusted-plugins denies reduce one route, but writable team configuration still influences installed storage.sh sourcing and dotfiles-T133-agmsg-hardening-a01 owns driver-name validation, plugin authorization hardening and adversarial execution tests."
  - control: orchestrator effect merge
    disposition: "residual: the worker is forbidden to merge and the orchestrator uses final-head integration evidence and a pinned merge, while shared credentials still permit worker-initiated API merges that the regime detects rather than prevents."
  - control: orchestrator effect update-branch
    disposition: "residual: the orchestrator owns branch updates and obtains fresh required CI, feedback, audit and security evidence for the resulting head."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned, existing dirty-worktree protections remain, and acceptance identifies any operator-authorized discarded state."
premises:
  - claim: >-
      D-024-26 narrowed P1-15 to the worker write boundary and transferred
      executable binding. The a01 implementation remains at ea3c4fb84bbcf2419a17946fdd1ea68b2355102e
      on main 51ba5801, branch tools/worker-write-boundary-a01, PR 431.
      This is its INV-6 reset after the two a01 worker fix rounds.
    sources:
      - .orchestration/decisions.tsv
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      Final-head security review found tracked worktree settings were not
      screened before startup; its legacy-mode probe also retained
      apiKeyHelper. The superseded-head review found contradictory worker
      sandbox exceptions. Both are implementation requirements here.
    sources:
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-security-ea3c4fb.md.last.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-security-a286915.md.last.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      Reviews 2ae9e2c and ebbb71b found three input-inventory omissions
      (.mcp.json, skills-directory plugins, .claude.json) and repository binding,
      triggering S1 and the round-3 re-plan. Its first review b2a186e found
      non-command hook handlers omitted (P1, fourth lineage input-inventory
      finding) and inherited GH_HOST selecting ledger API hosts (P2).
      This is amendment 1 after that re-plan, not a new reset: one of three
      post-re-plan C-80 reviews is consumed. Preserve every finding/class row.
    sources:
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-2ae9e2c.md.last.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-ebbb71b.md.last.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-text-security-b2a186e.md.last.md
  - claim: >-
      Design section 5.14 is uncommitted main-checkout context. Items 1, 2,
      8 and 9 were re-read for amendment 1 after the re-plan. The worker reads the
      HOME-relative source named below, and the verbatim quotations bind
      the relied-on sentences without a literal operator home path.
    sources:
      - $HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
  - claim: >-
      The managed template renders PermissionRequest as
      ~/.local/bin/common/permgate claude, and the existing validator
      recognizes that legacy form; D-024-26 preserves it for this task.
    sources:
      - home/.chezmoitemplates/claude-settings-managed.json
      - home/dot_claude/modify_private_settings.json
      - scripts/validate-agent-assets.py
      - .orchestration/decisions.tsv
  - claim: >-
      The read-only installed-version probe returned "2.1.300 (Claude Code)".
      The quoted enumerations below replace paraphrased loading lists; S01-S23
      instantiate them for that version, retaining the earlier installed
      loader/schema observations for the worker to recheck. Paths with root parameters denote each
      actual matching file, never a merged document that hides its sources.
      The worker rechecks the version and records loader observations before
      implementation; an unsupported or unenumerable source refuses startup.
    sources:
      - "command: claude --version"
      - https://code.claude.com/docs/en/settings
      - https://code.claude.com/docs/en/hooks
      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
      - https://code.claude.com/docs/en/plugins/loading
      - https://code.claude.com/docs/en/skills
  - claim: >-
      Verbatim handler type enumeration: '"command", "http", "mcp_tool", "prompt", or "agent"'.
      A handler is an executable input whether it selects a command, URL, tool, prompt or agent.
      [Hooks reference, Common fields](https://code.claude.com/docs/en/hooks#common-fields).
    fetched_at: "2026-10-19T20:41:53Z"
    sources: [https://code.claude.com/docs/en/hooks]
  - claim: >-
      Verbatim settings scope labels: "User"; "Shared project"; "Project local"; "Managed".
      Verbatim precedence labels, highest first: "Managed settings"; "Command line";
      "Project local settings"; "Shared project settings"; "User settings".
      [Settings scopes and precedence](https://code.claude.com/docs/en/settings).
    fetched_at: "2026-10-19T20:41:53Z"
    sources: [https://code.claude.com/docs/en/settings]
  - claim: >-
      Verbatim MCP installation scope labels: "Local"; "Project"; "User".
      Local and user servers reside in global state; project servers reside in .mcp.json.
      [MCP installation scopes](https://code.claude.com/docs/en/mcp#mcp-installation-scopes).
    fetched_at: "2026-10-19T20:41:53Z"
    sources: ["https://code.claude.com/docs/en/mcp#mcp-installation-scopes"]
  - claim: >-
      Verbatim plugin origins: "@<marketplace>"; "@inline"; "@skills-dir"; "@synced".
      Verbatim enablement sources, lowest first: "--add-dir"; "user"; "project"; "local"; "flag"; "managed".
      [Plugin loading sources](https://code.claude.com/docs/en/plugins/loading).
      Initial fetches failed; the retry succeeded, so these values are verified, not cached assumptions.
    fetched_at: "2026-10-19T20:41:53Z"
    sources: [https://code.claude.com/docs/en/plugins/loading]
  - claim: >-
      Verbatim skills discovery labels: "Enterprise"; "Personal"; "Project"; "Nested";
      "Additional directory"; "Plugin"; "claude.ai account". Verbatim path values:
      ".claude/skills/<skill-name>/SKILL.md"; "~/.claude/skills/<skill-name>/SKILL.md";
      "<subdir>/.claude/skills/<skill-name>/SKILL.md"; "<plugin>/skills/<skill-name>/SKILL.md".
      [Skills discovery roots](https://code.claude.com/docs/en/skills#choose-where-skills-load).
      Enterprise uses the managed settings directory; Additional directory uses each admitted --add-dir root.
      Account inputs are disabled in the worker baseline; unenumerable reintroduction refuses.
    fetched_at: "2026-10-19T20:41:53Z"
    sources: [https://code.claude.com/docs/en/skills]
  - claim: >-
      S01 is the worker user settings file <absolute-home>/.claude-worker/settings.json under the launcher's enforced CLAUDE_CONFIG_DIR. It can select hooks, helpers, environment selectors, MCP approvals and enabled plugins.
    sources:
      - https://code.claude.com/docs/en/settings
      - https://code.claude.com/docs/en/hooks
  - claim: >-
      S02 is <worktree>/.claude/settings.json, including tracked settings checked out at an older commit. Dedicated user settings do not exclude this project source.
    sources:
      - https://code.claude.com/docs/en/settings
  - claim: >-
      S03 is the retained legacy <worktree>/.claude/settings.local.json. Existing executable content is inspected before any migration.
    sources:
      - https://code.claude.com/docs/en/settings
      - home/dot_local/bin/common/executable_herdr-agents
  - claim: >-
      S04 is <anchored-checkout>/.claude/settings.local.json, which linked worktree sessions load. S03 and S04 are checked independently.
    sources:
      - https://code.claude.com/docs/en/settings#where-claude-code-keeps-the-local-file-in-a-git-repository
  - claim: >-
      S05 is the platform's managed-settings.json: on Darwin /Library/Application Support/ClaudeCode/managed-settings.json; on Linux /etc/claude-code/managed-settings.json. Administrative scope does not exempt executable fields from screening.
    sources:
      - https://code.claude.com/docs/en/settings
      - https://code.claude.com/docs/en/managed-settings
  - claim: >-
      S06 is each <managed-root>/managed-settings.d/<name>.json drop-in the installed loader reads. managed-root is the system directory containing S05; inspect each file before precedence or merging.
    sources:
      - https://code.claude.com/docs/en/managed-settings#split-a-file-based-policy-across-teams
  - claim: >-
      S07 is the dedicated configuration directory's remote-settings.json server-managed cache. MDM's com.anthropic.claudecode policy and fresh server-managed delivery are additional non-file managed sources. Their executable entries must be enumerated before launch; when the launcher cannot establish that read set without executing a helper or starting Claude, it refuses with the managed source's name.
    sources:
      - https://code.claude.com/docs/en/server-managed-settings
      - https://code.claude.com/docs/en/managed-settings
  - claim: >-
      S08 is <worktree>/.mcp.json, tracked or untracked. It supplies project servers after workspace trust and can contain command, args, env and executable helpers.
    sources:
      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
  - claim: >-
      S09 is <anchored-checkout>/.mcp.json when inherited by the installed loader. Version 2.1.300 merges ancestor definitions before nearer definitions; a present worktree file does not exclude the main file.
    sources:
      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
      - .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md
  - claim: >-
      S10 is each other <loaded-ancestor>/.mcp.json read while walking the launch/project-configuration directory's ancestors, excluding the filesystem root in the observed 2.1.300 loader. Include intermediate and above-checkout files and check them independently of overrides.
    sources:
      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
      - home/dot_local/bin/common/executable_herdr-agents
  - claim: >-
      S11 is <absolute-home>/.claude-worker/.claude.json, the global state file selected by the dedicated CLAUDE_CONFIG_DIR. Top-level mcpServers supplies user-scoped servers; projects.<project>.mcpServers supplies project-local servers. Check every project record that can apply to the worker, including linked-main identities, and executable helpers without exposing authentication or environment values.
    sources:
      - https://code.claude.com/docs/en/settings
      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
  - claim: >-
      S12 is each <skills-root>/<name>/.claude-plugin/plugin.json. skills-root includes the worktree's .claude/skills, the dedicated configuration directory's skills, applicable managed skills, and main-checkout skills when the installed worktree loader falls back to them. Include applicable nested and additional-directory roots; the launcher must not admit an unenumerated root. A skills-directory plugin can load bundled hooks after workspace trust.
    sources:
      - https://code.claude.com/docs/en/plugins/loading#plugins-shared-through-a-repository
      - https://code.claude.com/docs/en/skills#choose-where-skills-load
  - claim: >-
      S13 is <plugins-root>/installed_plugins.json. The default plugins-root is under the dedicated configuration directory; installPath and scope can select a plugin outside the cache. Caller-selected cache, seed or inline roots are launch inputs and cannot escape the inventory.
    sources:
      - https://code.claude.com/docs/en/plugins/loading#find-plugins-on-disk
      - https://code.claude.com/docs/en/env-vars
  - claim: >-
      S14 is <plugins-root>/known_marketplaces.json. Marketplace source definitions and executable header helpers are inputs even when a plugin is already cached.
    sources:
      - https://code.claude.com/docs/en/plugins/loading
  - claim: >-
      S15 is each loaded or loadable <plugin-root>/.claude-plugin/plugin.json, reached through S12, S13, a marketplace, synced plugins or an admitted session source. Check inline executable fields and implicit/default components as well as manifest-selected component paths.
    sources:
      - https://code.claude.com/docs/en/plugins/loading
      - https://code.claude.com/docs/en/plugins/manifest-reference
  - claim: >-
      S16 is each plugin hook file: the default <plugin-root>/hooks/hooks.json and each hooks JSON path selected by a manifest, one file at a time. Inline manifest hooks remain in S15.
    sources:
      - https://code.claude.com/docs/en/hooks#hook-locations
      - https://code.claude.com/docs/en/plugins/manifest-reference
  - claim: >-
      S17 is <marketplace-root>/.claude-plugin/marketplace.json. Command-sourced plugins, command-sourced marketplaces, executable header helpers and relative plugin roots are executable selections, not harmless descriptive metadata.
    sources:
      - https://code.claude.com/docs/en/plugins/loading
      - https://code.claude.com/docs/en/plugins/marketplace-reference
  - claim: >-
      S18 is each plugin MCP configuration file: the default <plugin-root>/.mcp.json and each manifest-selected MCP JSON file. Inline definitions remain in S15; bundle paths or URLs are executable loading selections and have no canonical worker form in this task.
    sources:
      - https://code.claude.com/docs/en/mcp
      - https://code.claude.com/docs/en/plugins/manifest-reference
  - claim: >-
      S19 is <managed-root>/managed-mcp.json. This source is separate from the managed settings tier; managedMcpServers entries inside settings remain covered by S05-S07 and the common no-unowned-server policy.
    sources:
      - https://code.claude.com/docs/en/mcp
      - https://code.claude.com/docs/en/server-managed-settings
  - claim: >-
      S20 is each applicable <skills-root>/<name>/SKILL.md. Executable frontmatter hooks and dynamic shell expansion are checked without invoking a skill. Ordinary descriptive text is not executed to determine whether it is acceptable.
    sources:
      - https://code.claude.com/docs/en/skills
      - https://code.claude.com/docs/en/hooks#hook-locations
  - claim: >-
      S21 is each applicable <commands-root>/<name>.md legacy command file; its executable frontmatter and dynamic shell expansion follow S20's policy. commands-root uses the corresponding user, project, inherited, managed or plugin command location the installed loader can read.
    sources:
      - https://code.claude.com/docs/en/skills
  - claim: >-
      S22 is each applicable <agents-root>/<name>.md subagent definition. Its frontmatter can define hook handlers. Include user, project, managed and plugin roots selected by the worker launch; reject caller-supplied agent definitions that were not inventoried.
    sources:
      - https://code.claude.com/docs/en/hooks#hook-locations
  - claim: >-
      S23 is each default or manifest-selected plugin LSP configuration file. Language-server command and args fields are executable entries. Other plugin components that would run code, including dependency installation, workflows and monitors, have no canonical worker activation in this task and are refused at their selecting entry.
    sources:
      - https://code.claude.com/docs/en/plugins/manifest-reference
      - https://code.claude.com/docs/en/plugins/loading
  - claim: >-
      K01 is the executable-entry inventory applied to S01-S23, not a second
      source list. It begins with every hooks.<event>[*].hooks[*] handler:
      validate .type before reading .command. Only type command with the exact
      canonical guarded command, args, shell and interpreter form passes;
      every other type (including http, mcp_tool, prompt, agent, unknown,
      missing or non-string types) refuses even without a command field.
      It also includes apiKeyHelper; statusLine.command;
      subagentStatusLine.command; fileSuggestion.command; awsAuthRefresh;
      awsCredentialExport; gcpAuthRefresh; otelHeadersHelper; proxyAuthHelper;
      processWrapper; policyHelper and per-platform policyHelpers; sandbox
      bwrapPath, socatPath and ripgrep executable overrides; MCP server
      command/args/env and executable helpers such as headersHelper;
      plugin hook handlers of every type, plugin/marketplace command sources and header
      helpers; language-server command/args; and executable skill/agent
      frontmatter or dynamic command expansion. A misplaced or unsupported
      executable form refuses instead of being preserved.
    sources:
      - https://code.claude.com/docs/en/settings
      - https://code.claude.com/docs/en/hooks
      - https://code.claude.com/docs/en/mcp
      - https://code.claude.com/docs/en/plugins/manifest-reference
      - https://code.claude.com/docs/en/skills
      - https://code.claude.com/docs/en/server-managed-settings#security-approval-dialogs
  - claim: >-
      K02 covers executable/source selectors inside settings env or the
      launch environment, including CLAUDE_CODE_SHELL_PREFIX,
      CLAUDE_CODE_PROCESS_WRAPPER, CLAUDE_CODE_PLUGIN_DIRS, plugin cache/seed
      roots and conflicting configuration-directory selection. enabledPlugins,
      extraKnownMarketplaces and plugin sync settings select additional
      inputs. User false entries do not defeat higher-scope true entries;
      empty maps are not a universal plugin disable.
    sources:
      - https://code.claude.com/docs/en/env-vars
      - https://code.claude.com/docs/en/plugins/loading#find-where-a-plugin-is-enabled
  - claim: >-
      Same-macOS-user gh Keychain access is not separated by a configuration
      directory, and administrative settings and shared capabilities do not
      establish adversarial isolation between seats sharing one OS user.
    sources:
      - .orchestration/decisions.tsv
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-a02 — plan 024 P1-15; seat a010

## Goal

Finish the worker write boundary through the INV-6 reset of a01. Worker a010 is Codex in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`.

Continue `tools/worker-write-boundary-a01` from `ea3c4fb84bbcf2419a17946fdd1ea68b2355102e` on main `51ba5801`, using the existing PR #431. Keep the a01 implementation and its D-024-26 narrowing. Add only:

1. Before every Claude worker start, run one screening procedure over the installed version's documented loading inventory in `premises:`. Inspect every source independently before workspace trust, migration, regeneration or worker execution. An absent executable entry or its exact canonical guarded command form passes; every non-command handler and every other executable payload refuses with a named source/event/index or source/key message. Disable project MCP auto-approval and worktree plugin loading in worker user settings as additional controls, while still refusing pre-existing payloads.
2. Make the SKILL's sandbox-only worker rule consistent throughout the Worker Playbook and place the retained exemptions in the orchestrator section.

The a01 pre-push correction and single Bot correction exhausted its two worker fix rounds. Its final-head P1 stops integration; this declared reset supplies the a02 budget without erasing a01 history.

The a02 pre-dispatch text failed reviews `2ae9e2c` and `ebbb71b`, with three `input-inventory` findings triggering S1. The acceptance record declares the round-3 re-plan: enumerate the documented loading list once. Its first review `b2a186e` failed on omitted non-command hook handlers (P1) and unbound API host selection (P2). This is amendment 1 after that re-plan; one of three post-re-plan C-80 reviews is consumed, with no further reset. Preserve all three reports and every class row. No a02 implementation result is claimed.

Retain the dedicated `CLAUDE_CONFIG_DIR`, static trusted-path deny inventory enumerated from executable inputs, private caches, managed sandbox policy, legacy worktree-local hook migration, native merge denials, platform-symmetric exclusions and validator fixtures, guarded project hooks, and managed-hook classification.

Every command hook this task renders starts with the prescribed `/usr/bin/env -i …` prefix except the orchestrator managed PermissionRequest hook. Its command remains exactly `~/.local/bin/common/permgate claude`, behind managed deny rules until `dotfiles-T133-trusted-entrypoint-binding-a01` lands. Do not put that legacy command behind the system-only PATH prefix: its unchanged shebang requires uv discovery.

Bound PermissionRequest, its structural validator, exact uv/Python declarations and mise pins, binary-identity deployment checks, real-uv hook execution tests and formatter PATH repair remain transferred under D-024-26. Do not reintroduce them.

The host is not a security boundary between seats sharing one OS user. Host-local controls reduce accidental and injected damage; they do not prevent malicious same-UID processes from exploiting shared credentials, filesystem races, host processes or shared control-plane capabilities.

The GitHub boundary is detection, not prevention. P1-11 owns the next-records-PR check that every main merge since the previous boundary has acceptance and gate-passage evidence. Records do not reach main until that boundary PR; this task makes no main-push detection claim. Separate-user or separate-host prevention remains the operator's future P1-16 decision under D-024-23.

D-024-20 retains P1-15 as the write-boundary prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator owns their `after:` fields. This task has `after: []`. Satisfying this prerequisite does not establish the deferred executable-binding contract.

## Design contract and review history

Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10 as main-checkout context. This is the only form in which that design path appears in this task.

C-88: items 1, 2, 8 and 9 were re-read from the uncommitted design for amendment 1. The following relied-on sentences are quoted verbatim, including item 1's handler-type enumeration requirement (C-95) and item 8's canonical-main API and host-binding requirements. D-024-26 assigns the quoted executable-binding requirements to the binding task; quotation does not restore them to this task's implementation scope.

Item 0:

> ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。

Item 1:

> Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。

> managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。

> hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。

> `failIfUnavailable: true` を全席に置く。

> The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19).

> The inventory of executable configuration sources a worker start screens is the documented loading list of the installed Claude Code version, enumerated once from the documentation (settings: user, project, local and managed `settings.json`; project `.mcp.json`; the configuration directory's global state `.claude.json` with user-scoped and project-local MCP servers; plugins and skills directories (`.claude/skills/*/.claude-plugin/plugin.json`, enabled plugins); hook handlers of every documented type (`command`, `http` and any other `type` value the hooks reference lists: a handler is an executable input whether it names a command or a URL, and a worker start refuses every handler type but `command`), `apiKeyHelper`, `statusLine.command`, MCP server commands), and the launcher screens or disables every source before accepting workspace trust, refusing any executable payload it did not write; adding sources one review at a time is the anti-pattern (P1-15 a02 reviews 2ae9e2c and ebbb71b, 2026-10-19). The enumeration quotes the documentation's values (the page, its fetched_at and the listed values) in the text's premises so a reviewer can check them against the live page; naming a source by one of its fields ("hook commands" for hook handlers) is the same anti-pattern one level down (a02 review b2a186e, 2026-10-19T20:36Z; C-95).

Item 2:

> 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。

Item 3:

> 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。

Item 4:

> 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。

Item 5:

> 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。

Item 6:

> 境界だけが緩和するリスクを `closed` と書かない。各文は残余を 1 行で明記する。

Item 7:

> threat_table は本節の項目 1〜10 に 1 行ずつ対応させる（参照だけでは足りない）。

Item 8:

> permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。

> The sha of canonical `main` comes from the fixed repository's API (`gh api repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`), never from `git ls-remote origin`, whose destination the local remote and URL-rewrite configuration control (P1-12 a04 C-80, 2026-10-19T20:01Z); the content read at that sha comes from `repos/mryfmo/dotfiles/contents/<path>?ref=<sha40>`.

> Every `gh api` call that decides also binds the host with `--hostname github.com` (`GH_HOST` and the hosts configuration select the API host otherwise), a subcommand binds it through the `github.com/mryfmo/dotfiles` form of `--repo`, and a test that exports a hostile `GH_HOST` shows the call still names github.com or refuses (a02 review b2a186e, 2026-10-19T20:36Z).

Item 9:

> orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。

> `UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。

> One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19).

> Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19).

> A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.

Item 10:

> worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。

Read the a01 task and acceptance record, including its last 30 lines, and both implementation security reviews:

- `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-security-ea3c4fb.md.last.md`
- `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-security-a286915.md.last.md`

The final-head review's `security:ea3c4fb:1` requires startup refusal for unguarded tracked hooks and screening of alternate executable settings. The superseded-head SKILL contradiction did not recur in the final-head report; settle it explicitly rather than treating that omission as closure.

The acceptance record retains the executable-binding class correction, D-024-26 re-plan and complete earlier text-review history. Its four binding findings remain transferred to `dotfiles-T133-trusted-entrypoint-binding-a01`, not fixed by this reset.

Read the a02 acceptance record's re-plan and all three pre-dispatch reports. Preserve the first two failed rounds and the first failed review after the re-plan; this amendment consumes no fresh reset. Preserve these findings and their dispositions:

- `text-security:2ae9e2c:1` — `input-inventory`, project `.mcp.json`.
- `text-security:ebbb71b:1` — `input-inventory`, skills-directory plugins.
- `text-security:ebbb71b:2` — `input-inventory`, configuration-directory global state.
- `text-security:ebbb71b:3` — `repository-binding`, canonical-main SHA selection.
- `text-security:b2a186e:1` — `input-inventory`, non-command hook handlers (P1, fourth lineage finding and first after the re-plan).
- `text-security:b2a186e:2` — `repository-binding`, inherited `GH_HOST` selecting the ledger API host (P2).

The first three require the complete inventory and per-source fixtures. `b2a186e:1` changes its field-level unit from command strings to every handler and adds per-settings-source command-free HTTP fixtures. Both repository-binding findings refresh the deferred ledger contract to fixed-host, fixed-repository API calls and hostile-host tests; they add no ledger consumer.

## Files

1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.

   Retain the separate worker settings output `home/.chezmoitemplates/claude-worker-settings.json`, administrative output `home/.chezmoitemplates/claude-managed-settings.json`, worker directory `~/.claude-worker` and anchored primary checkout declaration. Keep existing model selections and Codex profile, sandbox, approval, network and shared-Git settings unchanged.

   Keep the static `trusted_paths:` inventory. It protects anchored-checkout source and control paths outside `.claude/worktrees/`, including tracked `.claude` contents, main-local settings, `.orchestration`, scripts, tests, configuration and current top-level source paths. Explicitly include both `<anchored-checkout>/.agents/worklog/**` and `<anchored-checkout>/.agents/worklog/uv-cache/**`, with directory targets where needed.

   Do not deny the checkout parent or all of `.claude/worktrees/`. Separately protect the directory target and descendants of `//<anchored-checkout>/.claude/worktrees/*/.claude/**` and the file `//<anchored-checkout>/.claude/worktrees/*/.mcp.json`. Ordinary worktree source writes and per-seat caches remain available.

   Retain these protected inputs and their directory targets where applicable:

   - `~/.agents/agent-config.yaml`
   - `~/.agents/permgate-policy.yaml`
   - `~/.agents/model-profiles.env`
   - `~/.agents/skills/**/scripts/**`
   - `~/.agents/skills/**/SKILL.md`
   - `~/.agents/skills/agmsg/plugins/**`
   - `~/.agents/skills/agmsg/db/trusted-plugins`
   - `~/.claude/**`
   - `~/.claude/hooks/orchestrator-only.sh`
   - `~/.claude-worker/**`
   - `~/.local/bin/**`
   - `~/.local/lib/python*/site-packages`
   - `~/.local/lib/python*/site-packages/**`
   - `~/Library/Python/*/lib/python/site-packages`
   - `~/Library/Python/*/lib/python/site-packages/**`
   - `~/.local/share/**`
   - `~/.local/state/**`
   - `~/.local/share/mise/**`
   - `~/.config/**`
   - `~/.cache/uv/**`
   - `~/.local/share/uv/**`

   The user-site entries cover `.pth`, `usercustomize.py` and `sitecustomize.py`. Account for other startup locations of interpreters used by retained hooks through explicit entries or existing protected installation/configuration paths, without claiming isolated interpreter startup.

   Protect application code consumed by installed wrappers, including `~/.local/share/**`; protecting only wrappers is insufficient. Explicitly name the permgate policy and rendered guard even where patterns overlap.

   Do not replace the inventory with blanket `~/.agents/**` or `~/.local/**` denies. Agmsg stores `db`, `teams`, `run` and `ext-tools` remain writable, including ordinary descendants, except `db/trusted-plugins`; plugin code remains denied. Read/Edit denies also affect Bash sandbox writes.

   Worker user policy enables sandboxing, sets `failIfUnavailable: true` and `allowUnsandboxedCommands: false`, supplies no excluded commands or Herdr socket allowance, and restricts additional writes to agmsg stores and private seat caches. The project root provides ordinary worktree writes; shared uv and mise allowances are not copied.

   Orchestrator user policy retains its permissions and cache allowances, adds `failIfUnavailable: true`, and uses the same three control-plane exclusions on both platforms. The former Linux `gh *` exclusion remains removed.

   Add no exact interpreter versions, installation-layout assumptions, private executable links or discovery fallbacks.

2. `scripts/generate-agent-configs.py` renders distinct orchestrator user, worker user and administrative settings from the manifest.

   Render denies from the static inventory, using absolute `//` anchored-checkout patterns and listed home forms. Perform no Git tree, index, ref or object traversal to choose protected paths; `git ls-tree` and `git ls-files` are not inventory authority.

   Generation remains independent of deployment executable availability. Binding-only native `{{ output ... }}` expressions and installation probes stay removed. Ordinary home, source, platform and anchor substitutions suffice.

   Retain:

   - `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy`
   - `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest`
   - `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_leave_agmsg_stores_writable`
   - `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_protect_permgate_policy`

   Inventory fixtures check exact manifest-to-render correspondence on Darwin and Linux, directory targets and descendants, source coverage by filesystem enumeration under fixed roots, worklog/cache protection, explicit policy and guard entries, user-site startup-file coverage and ordinary worktree writes. Planted Git environment or replacement refs do not affect output.

   Include homes and anchors with spaces, tracked `.claude` children, main-local settings, worktree configuration, symlink components and filesystem case aliases. These check configured coverage and identity, not live Claude enforcement.

   The permgate-policy fixture refuses matched Edit and Write requests in a temporary HOME and asserts unchanged policy bytes; it executes no bound PermissionRequest hook and claims no policy-selection environment isolation.

3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator user baseline.

   Its managed PermissionRequest command stays exactly:

   ```text
   ~/.local/bin/common/permgate claude
   ```

   Add no env prefix, guard selector, absolute uv/Python invocation or new command-form validator for this hook. Keep its timeout and common `onFailure: "block"` entry policy. Its shebang, interpreter discovery and inherited environment remain the binding task's residuals.

   Every other command hook generated by this task starts with:

   ```text
   /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"
   ```

   Re-export HOME before paths use it and preserve launch identity explicitly. Agmsg delivery additionally sets `AGMSG_RESOLVE_PROJECT=0` and preserves launcher-supplied `AGMSG_STORAGE_PATH`.

   Project-sensitive commands use the installed guard and fixed operation identifiers. Reuse existing payload scripts; add no replacement Herdr state helper or formatter tool directories.

   Retain `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy`, accounting for startup/failure policy, prefixes, guarding and exclusions without claiming formatter availability or PermissionRequest binding.

4. `home/dot_claude/modify_private_settings.json` retains its managed-hook classification and appended attachment hook.

   Keep `is_managed_permission_hook`'s legacy `permgate claude` recognition and stale `ccgate claude` migration. Add no bound PermissionRequest recognition.

   Managed SessionStart and PostToolUse classification recognizes exact owned prefixed/guarded forms, fixed operations and expected arguments alongside owned legacy forms. A foreign guard, malformed prefix, extra operation or custom hook does not become managed through a familiar basename.

   Preserve the quoted/escaped-tilde distinction, unrelated hooks, mixed entries, ordering, stale replacement without duplication and byte-identical repeated merges.

   The attachment hook appended by `main()` also has the clean prefix, installed guard route and `onFailure: "block"`; effective merged-settings fixtures cover it.

   Retain `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_prefixed_guarded_managed_hooks_replace_legacy_hooks_idempotently` and existing stale-ccgate, ordering, PostToolUse, tilde and custom-hook cases. Add no executable subprocess to template rendering.

5. `home/.chezmoitemplates/claude-worker-settings.json` is the dedicated worker baseline.

   Retain static trusted-path and worktree-configuration denies, native merge denials, `permissions.defaultMode: auto`, empty user exclusions, disabled unsandboxed requests, restricted writes, no user Herdr socket allowance and `failIfUnavailable: true` on both platforms.

   Set `enableAllProjectMcpServers: false` and `enabledMcpjsonServers: []` explicitly in the worker user settings on both platforms so that this baseline auto-approves no project server. Assert both fields in the existing worker-render and idempotent-merge fixtures; they do not replace item 11's screening.

   Disable worktree plugin loading with the installed version's explicit `enabledPlugins` false entries for applicable plugin IDs, including `<name>@skills-dir`; also set `syncClaudeAiPlugins: false` and `syncClaudeAiSkills: false` so this dedicated baseline does not add account-synced inputs. Keep the manifest-known false entries in the rendered baseline and let trusted preparation add false entries for identities found during read-only source enumeration. Do not treat `enabledPlugins: {}` as disabling default-enabled skills-directory plugins, invent wildcard semantics, or import the orchestrator's plugin state.

   Assert the disable fields and explicit skills-directory false entries in render/merge/preparation fixtures. A higher-scope enable, a new plugin identity or an already-present executable payload still faces the common screening policy and refuses; user settings are an additional control, not an override of all scopes.

   Worker user hooks remain limited to agmsg delivery. Import no orchestrator formatter, project-map, PermissionRequest, attachment, Herdr state, plugins or credential files.

   Delivery keeps the clean prefix, `AGMSG_RESOLVE_PROJECT=0`, launcher-supplied `AGMSG_STORAGE_PATH` and `onFailure: "block"`. To satisfy the common startup check in item 11, express each delivery entry through a fixed installed-guard operation while preserving its trusted agmsg delivery behavior and system-only descendant PATH.

   Store-selected sourced code remains the agmsg residual. Empty worker arrays do not subtract shared administrative exclusions or socket access.

6. `home/.chezmoitemplates/claude-managed-settings.json` supplies the separate administrative sandbox policy.

   Retain `sandbox.enabled: true`, `sandbox.failIfUnavailable: true` and `sandbox.allowUnsandboxedCommands: false`.

   Retain `sandbox.filesystem.disabled: false`, `sandbox.enableWeakerNestedSandbox: false`, `sandbox.enableWeakerNetworkIsolation: false`, `sandbox.network.allowAllUnixSockets: false`, `sandbox.network.allowLocalBinding: false` and `sandbox.allowAppleEvents: false`.

   Its ordered `sandbox.excludedCommands` list remains exactly:

   ```text
   agmsg-dispatch *
   herdr-agents *
   <absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *
   ```

   Its `sandbox.network.allowUnixSockets` contains exactly the trusted expansion of `~/.config/herdr/herdr.sock`.

   These administrative capabilities remain available to every Claude seat; worker user lists cannot revoke them. They grant no worker authorization to leave the sandbox.

   Retain:

   - `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox`
   - `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings`

   Lower-scope attempts to disable sandbox/startup failure, enable unsandboxed retries, add exclusions/sockets or weaken isolation leave trusted administrative content unchanged. The fixture is not proof of live enforcement.

7. `Makefile` retains only `install-managed-settings` and its `.PHONY` addition.

   Stage the rendered administrative template at `~/.claude/managed-settings.rendered.json` and print:

   ```text
   sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"
   ```

   The destination is `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS or `/etc/claude-code/managed-settings.json` on Linux. Preserve quoting for spaces. Execute no sudo, live installation, authentication or restart.

   Retain `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo`, including both destinations, staged JSON, exact printed command and absent sudo marker.

8. `home/dot_claude-worker/modify_private_settings.json` renders `~/.claude-worker/settings.json`.

   Keep the stdin/stdout chezmoi interface and standard-library baseline. Replace stale worker-managed permissions, sandbox settings and hook arrays without accumulating old exclusions, sockets, shared caches or hooks.

   Read or copy no orchestrator user settings or credentials. Retain empty/malformed-input baseline behavior and idempotence; startup must reject malformed existing settings before that fallback can conceal executable configuration.

   Share the item 11 executable-field policy with legacy handling rather than leaving `--legacy` able to retain an `apiKeyHelper`. Preserve unrelated non-executable state only after screening. Rendering or migration never substitutes for the launcher's whole-inventory preflight.

   Retain:

   - `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently`
   - `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks`

   Binding-only native rendering stays removed.

9. `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` installs `~/.claude/hooks/orchestrator-only.sh`.

   Keep `.tmpl` and render trusted home and anchor constants. Fixtures exercise the source and installed form.

   The guard compares canonical `CLAUDE_PROJECT_DIR` with the anchored checkout. Worker, sibling, unrelated and missing/unresolvable launch identities execute no orchestrator project payload and exit 0; event cwd cannot change that decision. Launch identity never supplies an executable path.

   Fixed installed agmsg-delivery operations needed by item 11 are the only worker-root dispatches added here; they accept no worker-selected script or executable. Other operations retain anchored-only dispatch.

   Preserve fixed payload paths, argument boundaries, stdin and child status. Reject unknown operations; use no eval or worker-relative script selection.

   Keep existing absolute system-interpreter conventions. Add no version declarations, private executable directory, installation discovery or formatter PATH repair. Complete executable identity remains deferred.

   Formatter/map operations also check resolved tool-input paths: outside-anchor inputs and worker-repository inputs execute no formatter/map payload and consume no worker configuration.

   Retain `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads`, covering complete prefixes, positive anchored execution, worker/unrelated roots, mutable cwd, aliases, arguments/stdin/status and an absent inherited `BASH_ENV` marker.

   Formatter/map fixtures distinguish positive anchored inputs from outside-anchor and worker inputs; they establish routing, not Ruff, Prettier, Node or terminal-browser availability.

10. `.claude/settings.json` keeps its tracked project events and routes every command through the installed guard.

    Keep the non-template file portable. Commands use item 3's clean prefix followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation. Put no host-specific home, installation, anchor or tool-directory path in it.

    Every entry carries `onFailure: "block"`. Worker sessions execute no guarded project payload. Keep operation markers required by the existing validator, including `format-edited-files.py`.

    Retain `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure`, traversing every event, matcher and command and checking failure policy, explicit re-exports and absence of worker-selected payload paths.

    Temporary homes and anchors leave tracked commands identical. This file contains no bound PermissionRequest.

11. `home/dot_local/bin/common/executable_herdr-agents` prepares the worker launch boundary.

    Every Claude worker process receives `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`, including managed-workspace, standalone and repeated starts. Override conflicting caller values at the actual worker process.

    Every worker kind receives `UV_CACHE_DIR=<canonical-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<canonical-worktree>/.uv-cache/python`; caller values cannot replace them.

    Use S01-S23 and K01-K02 in `premises:` as the single inventory. Do not maintain a second shorter source list in a renderer, legacy path or launch route. Read the cited [settings](https://code.claude.com/docs/en/settings), [hooks](https://code.claude.com/docs/en/hooks), [MCP scopes](https://code.claude.com/docs/en/mcp#mcp-installation-scopes), [plugin loading](https://code.claude.com/docs/en/plugins/loading) and [skills](https://code.claude.com/docs/en/skills) documentation before implementing the procedure.

    Re-run `claude --version` read-only. The observed version for this text is `2.1.300`. Record the version, schema/loader inspection, each source class's actual read set, documented scope and acceptance policy in `validation.md`. Resolve an installed-version discrepancy as a blocked PONG requiring re-tasking; do not silently keep an older partial inventory.

    One pre-start screening procedure runs before any Claude worker process, workspace-trust acceptance, migration, normalization, regeneration, plugin resolution that executes code, or candidate command. Every launch route calls it. It enumerates files through the filesystem under the fixed launch, configuration and managed roots, including ignored/untracked files and applicable inherited sources; Git's index is not an exclusion authority.

    Expand each source class to individual files and inspect each file independently. A nearer or higher-precedence definition cannot conceal a payload in another loaded source. Deduplicate aliases only after resolving identity and retaining the source names needed for refusal messages. Include implicit plugin component locations as well as paths named by a manifest. Follow only readable configuration references; never run a helper, source a shell file, install a package, fetch a plugin or start a server to learn what it would load.

    An absent executable entry passes. An executable entry passes only when it exactly matches a form written by this launcher or the retained generated policy for that source, event, matcher, operation and arguments. Every other executable payload refuses startup with a named message identifying its actual source path and JSON/frontmatter key or executable selection. Keep payload values, environment values and credentials out of the message.

    Malformed, unreadable, ambiguous or unsupported executable configuration refuses; it is not treated as an absent entry. A non-file managed source or host-supplied configuration that cannot be enumerated before launch also causes a named refusal. No policy helper runs to make an unenumerable source acceptable, and the launcher does not mutate administrative settings or authentication state.

    K01 validates every handler at `hooks.<event>[<group-index>].hooks[<handler-index>].type` in each screened settings source and every other hook-bearing inventory source before looking for `command`. Only the string `command` proceeds to canonical-form validation. Refuse `http`, `mcp_tool`, `prompt`, `agent`, any other value, a missing type or a malformed handler even if `command` is absent or the event/matcher would not currently fire; type defaults and unsupported-event skipping are forbidden.

    Use the named refusal `worker startup refused: <source-file>: hooks.<event>[<group-index>].hooks[<handler-index>]: noncanonical hook handler` for both rejected types and noncanonical command handlers. Indices are zero-based; retain the actual file, event and both indices without printing payload, URL, headers or credentials. Apply it before migration/regeneration and any command, HTTP request, model/tool call or trust acceptance.

    Every surviving command hook has the prescribed `/usr/bin/env -i …` prefix, installed guard and fixed allowed operation with its exact arguments. Familiar substrings, extra shell syntax, substitutions, foreign guard paths, unknown operations and alternate exec-form arguments or shell selection do not pass. Dedicated user delivery uses the fixed trusted delivery operations described above; it is not an unguarded exception.

    Apply the same absent-or-canonical rule to every K01 executable field and K02 source selector in each applicable source. If this task defines no canonical guarded operation for a field, that field must be absent. Misplaced executable fields refuse rather than surviving because their scope is invalid. The legacy orchestrator PermissionRequest exception is not an allowed worker-start field.

    All MCP definitions receive that same rule, including global-state user servers and project-local records, inherited project files, plugin servers and managed definitions. No canonical worker MCP server or MCP guard operation is introduced here, so every nonempty applicable `mcpServers` or `managedMcpServers` definition refuses, including a remote server without a canonical command. Empty server maps and absent files pass. Inspect complete `command`, `args`, `env` and helper selections rather than only a command string.

    Apply MCP screening regardless of `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers` or saved trust/approval state. False user Booleans, empty user approval lists and rejection entries do not remove other sources or validate their definitions. Preserve original bytes on refusal, including global-state authentication and trust records.

    Plugin screening includes default-enabled skills-directory plugins, the enabled-plugin map in every settings scope, install and marketplace records, manifests, default hooks and manifest-selected hook files. Worker user settings explicitly disable applicable plugin IDs as item 5 requires, but screening still refuses pre-existing noncanonical payloads even when a plugin is disabled or workspace trust has not yet been accepted.

    No worker plugin activation is expected or introduced by this task. A higher-scope `enabledPlugins` true entry, command source, executable helper, unenumerated plugin root or executable component without a canonical worker form refuses. Empty `enabledPlugins` maps are not a disable mechanism. Account sync is off in the worker baseline; a managed requirement or other source that reintroduces plugin execution is screened or refuses.

    Plain skill, legacy command and subagent files are inspected for executable frontmatter and dynamic command expansion without invoking them. Plugin LSP commands and any other code-loading component have no canonical worker operation. Refuse unsupported loading forms at the selecting source/key rather than executing a parser supplied by the candidate or silently ignoring them. This task introduces no plugin installation, MCP startup, credential import or complete executable-binding claim.

    Reject caller-added `--settings`, `--mcp-config`, plugin, agent or additional-directory inputs unless they are fixed launcher-owned inputs already covered by the inventory. Settings `env` selectors cannot redirect the dedicated configuration directory or introduce an unenumerated executable/source root. Inspect the effective launch inputs before spawning the worker; do not rely on a later trust or approval prompt.

    Retain migration of exact recognized launcher-owned legacy delivery hooks. The preflight first classifies those exact owned legacy entries without executing them and screens all other fields across the whole inventory. Only after that complete pass may migration remove the recognized entries, preserve unrelated non-executable settings and install canonical delivery. Validate the retained/generated result with the same policy before launch. Unknown executable content refuses before any migration writes anything. Do not create a local file merely for migration.

    Never silently rewrite tracked `.claude/settings.json`. A refusal directs the operator or orchestrator to update the worktree to a commit whose tracked settings are guarded; the launcher does not refresh that tracked file itself.

    Regenerate trusted worker delivery on every preparation, avoiding duplicates. Retain guarded launcher-managed main-local agmsg/attachment hooks, permissions and unrelated non-executable settings. Update stale-hook fixtures to distinguish recognized managed migration from unknown executable content, which now refuses.

    Every launcher-rendered command has the clean prefix and `onFailure: "block"`; delivery preserves `AGMSG_RESOLVE_PROJECT=0` and launcher-supplied `AGMSG_STORAGE_PATH`. A writable `run/proj.<pid>.project` cannot override the explicit worker project.

    Retain native merge denials:

    ```text
    Bash(gh pr merge:*)
    Bash(gh api -X PUT:*)
    Bash(gh api --method PUT:*)
    Bash(gh api graphql:*)
    ```

    These do not prevent all API merge routes with shared credentials. Codex retains `--sandbox workspace-write`, `--ask-for-approval never` and existing shared Git grants; add no Codex network-policy change or test.

    Retain:

    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_repeated_worker_start_replaces_stale_managed_hooks`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_launch_adds_no_unsandboxed_route`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_settings_hook_has_system_path_prefix`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_claude_preparation_keeps_boundary_when_delivery_tool_is_unavailable`

    Add `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_existing_worktree_with_unguarded_tracked_hook_is_refused_before_launch`. Check out an older tracked settings file containing an unguarded hook in a fixture worktree; assert named refusal, unchanged tracked bytes, no worker spawn/trust acceptance and no command marker. Guarded and absent-entry controls pass, including repeated starts.

    Add `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_executable_settings_entrypoints_are_checked_before_launch`. Plant `apiKeyHelper` separately in each settings source, including the legacy path accepted by a01's `--legacy` handling, and assert refusal before normalization, launch or command execution. Parameterize the same fixture for K01-K02's applicable alternate entrypoints, with absent/canonical controls and malformed/foreign/extra-command negatives.

    Add `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch`. Reuse the source fixture builder to plant a command-free `{"type":"http","url":"https://example.invalid/hook"}` under `PreToolUse` separately in every settings source class S01-S07, including both S05 platform roots, each applicable managed drop-in/cache and the legacy path. Derive coverage from the production settings-source inventory. Assert the named refusal includes the planted file, event and zero-based group/handler indices; no migration, regeneration, trust acceptance, worker spawn, command or request occurs, bytes remain unchanged and execution/request markers are absent. Exercise other hook-bearing S15-S16/S20-S22 sources and misplaced S11 handlers under the same policy. Parameterize `mcp_tool`, `prompt`, `agent`, unknown/missing/null/non-string types and a `command` handler with noncanonical payload; retain absent and canonical-command controls, disabled-plugin and repeated-start variants. Use only temporary fixtures and synthetic values, never a live HTTP endpoint.

    Add `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_existing_project_mcp_server_is_refused_before_launch`. Before preparation, plant a server whose command would write a marker and existing settings with `enableAllProjectMcpServers: true`. Parameterize approval settings across all applicable settings scopes and the server across S08-S10, explicitly including the main checkout with the worktree file absent and with an empty worktree server map. Include named `enabledMcpjsonServers` approval and `disabledMcpjsonServers` rejection variants. Assert named source/key refusal before spawn, trust acceptance, normalization or regeneration, unchanged bytes and an absent marker. Reuse absent/empty controls and malformed/noncanonical negatives.

    Add `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_configuration_global_state_payload_is_refused_before_launch`. Use a synthetic dedicated configuration global-state file with nonsecret authentication/trust sentinels. Plant a top-level user server, a project-local server under the worker project key, a linked-main project-key variant and an executable helper separately. Assert source/key refusal, unchanged global-state bytes and sentinels, no spawn/trust acceptance and an absent command marker. Include absent/empty state controls; no real credentials are read.

    Add `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_skills_directory_plugin_payload_is_refused_before_launch`. Plant a metadata-only skill-folder plugin with a bundled marker-writing hook, testing both inline and default hook-file forms. Parameterize applicable worktree, dedicated-user, managed and main-checkout fallback roots, including a main fallback when the worktree skills directory is absent. Repeat with the plugin explicitly false in worker user settings to show that disabling does not conceal a pre-existing payload. Assert refusal before trust acceptance, plugin or worker execution, unchanged files and an absent marker. Metadata/absent-executable controls check the explicit disable entry without starting a plugin.

    Add `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch`. Reuse one fixture builder and the preceding focused tests, with one isolated planted-payload case for every S01-S23 class. Each case plants the payload in that class's own file, keeps other sources absent or canonical and asserts the refusal names that file and key. S05 covers both platform roots; S06 covers an individual drop-in; S07 covers the cache and an unenumerable non-file source; S12 and S16 cover inline/default/declared hook forms; S13-S19 and S23 cover their own registry, manifest or server files. S20-S22 plant executable frontmatter or dynamic command expansion without invoking the skill, command or subagent.

    The fixture-case inventory must equal the production source-class inventory, so omitting a source case fails the test. Include activation and launch-selector negatives for K02, higher-scope plugin enablement, an unexpected component/root and a managed source that cannot be screened without executing a helper. Every case asserts no worker spawn, no trust acceptance, no candidate/helper/plugin/server command execution, an absent marker and unchanged pre-existing bytes. Use temporary HOME and managed-root fixtures; never write system configuration.

    Preserve a01-red/final-head-green evidence for the new regressions. Start no live Claude worker, MCP server, plugin or subagent. A single parameterized selector may cover several source-class fixtures, but validation names every subcase and its actual source/key.

    Linked-worktree evidence covers tracked, dedicated user, main-local and legacy settings together, plus inherited MCP and applicable plugin/skill sources. Main-local project payload markers remain absent under worker roots; repeated preparation retains native denials. Prefix tests preserve explicit re-exports, suppress `BASH_ENV` and reject conflicting writable project-marker selection.

    These tests establish pre-start refusal for the enumerated files and launch inputs. They do not establish atomic protection against a same-UID replacement or complete mediation of configuration created or reloaded after startup; retain those residuals.

12. Retain the delivery-environment portion of `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters`.

    Exercise installed-style delivery with directly executed `/usr/bin/env bash` descendants. A leading outer Bash shim remains unexecuted because descendants receive `/usr/bin:/bin`.

    The replacement Herdr state helper and binding-only fixture stay removed; its installed state hook remains behind the orchestrator guard.

    Inventory reached delivery scripts, including `session-start.sh`, `session-end.sh`, `check-inbox.sh`, `identities.sh` and reached descendants. Distinguish clean environment and fixed PATH from complete executable binding.

    Fixed PATH does not mitigate `storage.sh` sourcing drivers selected by writable team configuration. Retain traversal/plugin authorization as `dotfiles-T133-agmsg-hardening-a01` residuals.

13. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` makes the worker rule consistent.

    Worker Playbook step 4 states this single sentence:

    > Complete every worker command, including gh, git push and authenticated git fetch, inside the sandbox and allowlist without forbidden actions or escalation; anything that cannot complete there is `AGMSG-PONG v1 status=blocked` naming the exact command and boundary.

    The Worker Playbook lists no worker exception. Remove contradictory instructions in steps 2, 5 and 11 as well as step 4: no unsandboxed push, main-checkout artifact write/masking, CompactionDB update or dispatch is authorized for a worker.

    In the orchestrator section, name the retained orchestrator-only exemptions: main-checkout artifact writes and masking under evidence-sync, CompactionDB consolidation, and agmsg-dispatch control-plane delivery. They do not transfer to workers. A worker writes evidence at required relative paths in its worktree; the orchestrator copies it before review. Dispatch that cannot complete inside the worker sandbox is a blocked PONG.

    Retain and strengthen `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox`.

    Add `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_worker_playbook_has_no_sandbox_exceptions`. Assert the exact step 4 sentence, absence of worker escape instructions throughout the Worker Playbook, and presence of the three exemptions only as orchestrator operations. Remove assertions requiring the superseded worker exceptions.

    Add `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host`. Read the two exact deferred-ledger command templates from the dispatched task copy's Out of scope paragraph (the operative host-bound forms, not the verbatim historical design example) and exercise them as argument vectors with only the validated SHA placeholder substituted, not through shell evaluation or a new ledger consumer. Export `GH_HOST=example.invalid`; a temporary stub `gh` records argv and returns only a synthetic 40-hex SHA and nonsecret ledger fixture. Assert both recorded API calls carry exactly `--hostname github.com`, the fixed `repos/mryfmo/dotfiles/` endpoint, and the content request's identical validated full SHA; reject an omitted/duplicate/conflicting hostname. Check that every deciding subcommand contract uses `--repo github.com/mryfmo/dotfiles`. In a second case remove the stub and provide an isolated PATH with no `gh`, so no host-bound invocation is possible: assert nonzero refusal identifying inability to bind github.com, no accepted SHA/ledger, and no retry using inherited host, local refs or files. No installed CLI, live API, credentials or network is used in that case. Record this contract-only limitation; P1-14 a05 and P1-6 must apply the same tests to their real consumers.

    Retain PR #427's merged changes and run the complete documentation-test module.

14. `.gitignore` retains only `.uv-cache/` as this task's addition.

    Retain `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored`.

    Existing `.agents/worklog/` ignoring covers the orchestrator cache; it removes neither worklog/cache pattern from the deny inventory. Consuming hardening tasks own use of that protected cache.

15. `scripts/validate-agent-assets.py` retains the platform-symmetric exclusion checks.

    Both Darwin and Linux require exactly this ordered list:

    ```text
    agmsg-dispatch *
    herdr-agents *
    {{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *
    ```

    Compare the home-expanded equivalent for rendered settings. Keep non-empty-string validation and reject `gh *`, extra, missing, reordered or substituted entries on either platform.

    Preserve existing managed PermissionRequest wiring and ccgate refusal. The literal `permgate claude` remains valid. Add no bound-PermissionRequest parser, native-binding expansion or `--check-effective-settings` mode; Codex wiring stays unchanged.

    Preserve schema, model/effort, formatter markers, permission-list, sandbox, plugin and Crit checks, duplicate-hook rejection, permgate-first ordering, synchronous timeout budgets and SessionStart state-hook marker/order checks.

    Retain generated-output freshness, home-path/secret scanning, tracked settings portability and deterministic permgate-policy validation.

    Retain `tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form`, including macOS gh and Linux extra-exclusion cases, and the exact three-entry `valid_claude_sandbox` fixture with its callers:

    - `test_claude_sandbox_accepts_manifest_symmetric_settings`
    - `test_claude_sandbox_rejects_each_broken_rule`
    - `test_claude_sandbox_requires_extra_codex_writable_roots`
    - `test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs`
    - `test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs`

    PermissionRequest fixtures in `test_hook_composition_requires_permgate_first`, generator and merge tests retain the legacy command. Adjust surrounding forms only where the authorized prefix/guard change requires it.

16. The seven allowed test modules reuse render, merge, fake-launcher and temporary-HOME fixtures.

    Write the a02 regressions before implementation and preserve failure on `ea3c4fb8` followed by final-head success. Retain a01 red/green evidence as historical, not a substitute for a02 results.

    Do not restore real-uv PermissionRequest execution, interpreter discovery, planted-user-site execution, exact-version equality, installation-existence rendering or binary-identity deployment fixtures. Static user-site inventory assertions remain.

    Record the supported Claude version for `onFailure: "block"`; background hooks and excluded events have no enforcement effect from it. Configuration inspection establishes no runtime timeout/crash handling.

    Tests create no identities, initiate no login and access no real credential store. They do not establish credential separation, live administrative enforcement or upstream agmsg hardening.

    C11: every `closed` threat-table disposition must name one exact `tests/<path>::<Class>::<test>` selector whose fixture establishes that row's stated closure. A module name, prose assertion or command without that selector is insufficient. Keep same-UID races, future reloads and deferred binding as residuals; passing the pre-start fixtures does not close them.

17. `.orchestration/dotfiles-T133-worker-write-boundary-a02/` contains byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, operator instructions and worker review evidence.

    On the first a02 push, delete `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md` and add the byte-identical a02 task copy. This C3 predecessor-copy deletion is the sole authorized action outside the replacement artifact directory; edit no other a01 artifact or canonical task/acceptance record.

    Map historical findings to retained controls, residuals or owners. Binding findings remain transferred under D-024-26. Retain the a01 report of removed binding files/portions; do not repeat their removal or describe them as new a02 fixes.

    Preserve the a02 input-inventory re-plan, all four input-inventory class rows and both repository-binding findings, including amendment 1 and the post-re-plan review count. Record S01-S23 and handler-type fixture coverage, five fetched documentation enumerations and the refreshed item 8 quotation without claiming text itself closes implementation findings.

## Change budget

`git diff --numstat 51ba5801 ea3c4fb8` measures `96 + 1 + 6 + 55 + 2 + 63 + 56 + 99 + 116 + 158 + 9 = 661` changed source lines outside `tests/` and `.orchestration/`, excluding the three regenerated Claude settings templates. Add an estimated 240 lines for Goal item 1's common screening procedure, complete source enumeration, explicit plugin disables, guarded delivery and launcher calls, and 30 for Goal item 2's SKILL consistency, plus 30 for amendment 1's handler-type validation and named refusals, giving the source cap `661 + 240 + 30 + 30 = 961`. Amendment 1 (2026-10-19T23:40:53Z, measured, the one cap amendment this text takes): `git diff --numstat 51ba5801 80869efc` at the pushed head measures `96 + 1 + 6 + 60 + 10 + 424 + 65 + 99 + 90 + 181 + 9 = 1041` changed source lines (the same exclusion of the three regenerated Claude settings templates); the 240-line estimate for the common screening procedure measured 361 in `home/dot_claude-worker/modify_private_settings.json` alone (the S01-S23/K01-K02 screening of the documented loading list, 424 lines) while the launcher shrank by 26 (budget-attribution.json in the task directory carries the per-file and per-control attribution); the source cap is therefore `1041`, measured, and is not raised again.

The same command measures `3 + 95 + 131 + 260 + 103 + 342 + 15 = 949` changed lines under `tests/`. Add an estimated 160 for the old-checkout and alternate executable-entrypoint fixtures, 50 for documentation assertions, 60 for the pre-existing project-MCP fixture, and 240 for global-state, skills-plugin and complete source-class fixtures with shared builders and platform/root subcases, plus 90 for command-free HTTP and other handler-type subcases and 60 for the hostile-GH_HOST argv/refusal contract test, giving the test cap `949 + 160 + 50 + 60 + 240 + 90 + 60 = 1609`.

The additions are estimates, not measured a02 results; record final per-file numstat and actual totals; the test cap is not raised, and the source cap was amended once to its measured value above and is not raised again. The 240-line fixture estimate includes the common fixture-coverage assertion and worker-render/merge assertions for plugin disables; count them once. The new 90 and 60 estimates reuse those builders and add no production ledger consumer.

## Out of scope

`dotfiles-T133-trusted-entrypoint-binding-a01` remains the executable-binding owner, with the reset successor replacing the withdrawn prerequisite:

```yaml
after:
  - dotfiles-T133-worker-write-boundary-a02
  - dotfiles-T133-ci-efficiency-followup-a04
```

It consumes the latter task's trusted interpreter resolver and owns exact host-probed uv/Python/Node layouts and declarations, mise pins, bound isolated PermissionRequest, structural validation and binding migrations, trusted binary-identity deployment checks, real-uv and planted-startup tests, complete descendant binding, formatter PATH changes and any binding-driven replacement state helper.

This task writes no owner task file and claims none of those mechanisms have landed.

`home/dot_mise/config.toml` and `home/dot_local/bin/common/executable_herdr-agent-state.sh` remain outside `allowed_files` and have no final PR diff. Binding-only portions removed from shared files stay removed; leave no dormant binding machinery.

The orchestrator managed PermissionRequest keeps its direct command behind managed denies. Its discovery, startup environment and execution remain unverified; no sanitized-prefix claim includes it. This exception does not authorize executable fields in the worker-start sources screened by item 11.

Formatter/project-map PATH repair is deferred. The clean PATH may leave current formatter or reload dependencies unavailable; report that limitation. Guard fixtures do not establish actual Ruff, Prettier, Node or terminal-browser behavior.

Codex network changes remain owned by `dotfiles-T133-codex-worker-network-a01` on a Claude seat. This Codex worker edits no Codex-boundary source; shared Git grants stay unchanged.

The worker-write-boundary Python hook and gh-trusted wrapper stay dropped. Add no gh configuration directory or credential-separation substitute.

`GH_CONFIG_DIR` does not separate same-macOS-user Keychain access. Shared credentials permit worker-initiated API merges despite native denials; separate-user/host prevention remains the operator's P1-16 decision.

P1-14 a05 and P1-6 own approval/evidence-of-record consumption. The regime obtains canonical main's full SHA through `gh api --hostname github.com repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha`, validates the returned 40-hex commit identity, and reads the committed ledger through `gh api --hostname github.com 'repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref=<sha40>'` inside the sandbox. Both calls bind github.com and the repository explicitly; every deciding `gh api` call carries `--hostname github.com`, and a deciding subcommand carries `--repo github.com/mryfmo/dotfiles`. Inherited `GH_HOST`, hosts configuration, `origin`, URL rewrites, local remotes/refs and the shared object database select no approval authority. If github.com cannot be bound, refuse without an unbound retry or local fallback. Item 13 tests these command templates under hostile `GH_HOST`; their owners enforce the same contract in the consuming implementations. This task implements no consuming mechanism, gh wrapper or approval row. [CLI host selection](https://cli.github.com/manual/gh_help_environment), [explicit API hostname](https://cli.github.com/manual/gh_api).

P1-11 owns next-records-PR detection of missing acceptance/gate evidence. `dotfiles-T133-agmsg-hardening-a01` owns driver-name validation and plugin authorization; recorded `drivers.partition` traversal and trusted-plugin sourcing remain residuals. Add no new store-derived sourcing.

Snapshots, reservation locks, full-head output identities, the common trusted-execution helper and review-worktree relocation remain with their owners.

Codex templates, modify script and merge tests retain `permgate codex`. `tests/unit/test_permgate.py` keeps direct testing of unchanged permgate; `tests/unit/test_statusline_tools.py` keeps existing rendering assertions. No binding render expression makes these depend on deployment installations.

Perform no authentication/keyring/ruleset mutation, administrative or global installation, live settings application, session restart or merge. Edit no canonical acceptance record, decision ledger or another task's text.

The screening procedure introduces no plugin installation or MCP service. It does not claim to mediate later configuration reloads atomically or prevent a same-UID process from replacing a file after inspection. An unenumerable startup source produces refusal; it is not an invitation to bypass the sandbox, invoke its helper or weaken the policy.

## Check

`make render-check` and `make validate-agent-assets` pass. Task files pass the `make format` flags: `shfmt -i 4 -sr --diff`, `ruff format --config ruff.toml --check` and `prettier --check`.

The clean historical base `205fe85c` has an inherited formatting failure on 12 out-of-scope files: ten archived task shell sources, `project-map-reload.sh` and `brew.bats`. Retain its reproduction, exact output and per-file exit statuses in `validation.md`; authorize no out-of-scope repair.

Shellcheck and shfmt cover changed shell sources, including the launcher and rendered guard. Changed shell comments use English shdoc-compatible annotations. Changed Python receives repository formatting and lint checks.

`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` is green.

`uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs -v` is green.

The validation record contains retained red/green selectors and complete final module outputs, with historical a01 results distinguished from new a02 results.

`tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_existing_worktree_with_unguarded_tracked_hook_is_refused_before_launch` fails on the a01 head and passes on the final head: older tracked settings cause a named refusal before spawn, trust acceptance or command execution, with tracked bytes unchanged.

`tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_executable_settings_entrypoints_are_checked_before_launch` fails on the a01 head and passes on the final head: an `apiKeyHelper` in each covered settings source refuses before migration/regeneration or execution, and the inventoried alternate executable entries receive the same absent/canonical/refuse policy.

`tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch` fails on the a01 head and passes on the final head: every settings source class's command-free HTTP fixture refuses before any execution/request, names the source/event/indices, preserves bytes and leaves markers absent. Other documented, unknown, missing and malformed types refuse; only canonical command controls pass.

`tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_existing_project_mcp_server_is_refused_before_launch` fails on the a01 head and passes on the final head: each worktree, main-checkout and other inherited project-MCP payload refuses before trust or command execution, regardless of approval state.

`tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_configuration_global_state_payload_is_refused_before_launch` fails on the a01 head and passes on the final head: user-scoped and project-local MCP servers and executable helpers in the dedicated global state cause source/key refusal with unchanged synthetic authentication/trust sentinels and an absent marker.

`tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_skills_directory_plugin_payload_is_refused_before_launch` fails on the a01 head and passes on the final head: each applicable skills-directory plugin payload refuses before trust or plugin execution, including when worker user settings already disable that plugin.

`tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_each_documented_loading_source_refuses_payload_before_launch` checks one planted-payload fixture per S01-S23 source class and the non-file/activation selectors. Its fixture-case inventory equals the production inventory. Every case shows named source/key refusal, unchanged existing bytes, no worker spawn, no trust acceptance, no candidate/helper/plugin/server command execution and an absent marker. Each file-based fixture plants its payload in the source class it claims to test.

`tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_worker_playbook_has_no_sandbox_exceptions` checks the exact step 4 sentence, no worker exceptions and the three exemptions in the orchestrator section; the retained launcher documentation assertion and complete docs module pass.

`tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host` passes: hostile `GH_HOST` does not change either recorded call's explicit hostname, repository or SHA binding; the no-stub/no-gh case refuses with no approval output or fallback. Retain both subcase outputs and the contract-only limitation.

The final diff has at most 1041 changed lines outside `tests/` and `.orchestration/`, excluding regenerated `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`.

The final diff has at most 1609 changed lines under `tests/`.

Changed lines mean additions plus deletions. Record per-file numstat, base/head identities and actual totals; measurement and estimate arithmetic stay in Change budget.

Record exact commands, verbatim outputs, exit statuses and tested identities. Git verification introduced or changed here follows sanitized Git requirements: explicit checkout selection, disabled system/global configuration, hooks/fsmonitor restrictions and disabled external diff/textconv where applicable.

Both platform renders show separate worker/orchestrator settings, exact static inventory correspondence, filesystem source coverage, both worklog/cache patterns, explicit policy/guard protection, user-site coverage, ordinary worktree writes, worktree `.claude`/`.mcp.json` denies, narrow home denies, writable stores, empty worker exclusions, restricted writes and `failIfUnavailable: true`.

Both worker renders and idempotent merge/preparation fixtures show project-MCP auto-approval off, account plugin/skill sync off and explicit false entries for applicable plugin IDs. An empty enable map alone does not satisfy this check. Higher-scope enables and disabled-but-present executable payloads still refuse in startup fixtures.

Managed evidence asserts sandbox enablement, startup failure, disabled retries, required anti-weakening Booleans, exactly three ordered exclusions and exactly the Herdr socket. Conflicting lower-scope fixtures leave trusted content unchanged; this is configuration evidence, not live enforcement.

Staging evidence shows temporary-HOME output and the exact quoted `sudo install -m 0644` command for both destinations, with no executed sudo marker.

Hook evidence inventories generated, tracked, appended and launcher-managed handlers by type, with command-free cases included; every surviving worker handler is a canonical command. It separately confirms unchanged orchestrator managed PermissionRequest. Every other rendered command has the clean prefix and explicit re-exports.

Startup evidence records the installed-version probe, every S01-S23 source class and its actual files, applicable K01-K02 entries, every handler type, source URLs/fetched_at/verbatim enumeration values, documented scopes and canonical acceptance/refusal policy. It shows one whole-inventory procedure precedes worker startup and workspace trust and cannot be bypassed by precedence, disabled plugin state, regeneration, legacy handling, a missing delivery tool or a repeated start.

Record inherited MCP read sets explicitly. Main-checkout and other ancestor definitions are checked even when nearer files exist. Record applicable skills/plugin roots, implicit and declared hook files, the dedicated global state's user and project-local maps, managed files/drop-ins/cache and any named unenumerable-source refusal. Do not log configuration secrets or raw credential values.

Delivery evidence checks `AGMSG_RESOLVE_PROJECT=0`, preserved `AGMSG_STORAGE_PATH`, conflicting writable marker rejection, suppressed `BASH_ENV` and system PATH in env-bash descendants, without claiming complete executable binding.

Merged-settings evidence shows managed non-PermissionRequest replacement, preserved custom hooks, attachment handling, idempotence and unchanged legacy PermissionRequest migration.

Launch evidence shows both cache variables reach every actual worker route and Claude receives its dedicated directory. Repeated preparation retains native denials and Codex sandbox/approval arguments.

Linked-worktree evidence checks all four settings sources together. Recognized old delivery hooks are removed only after the whole preflight passes, unrelated non-executable settings survive, unknown executable entries refuse, and absent local files are not created.

Guard evidence uses complete prefixes. Worker project roots, unrelated/missing identities and outside-anchor/worker formatter inputs leave project payload/configuration markers absent; positive anchored cases preserve arguments, stdin and status. Fixed trusted worker-delivery operations still deliver. Report formatter availability as deferred.

The report retains a01's removed binding-file/portion inventory and confirms no final PR diff outside the authorized files, apart from the explicit C3 predecessor task-copy deletion.

Retain named residuals: agmsg sourcing and owner, shared managed exclusions/socket access, same-UID credentials, consumption races, later configuration changes, external-process trust, hook-event limitations, legacy PermissionRequest and Codex shared Git grants.

Run no local Bats tests; required Bats results come from GitHub Actions. Required checks pass before RESULT; retain actual failure output and fix only within the authorized scope and round budget.

The orchestrator runs `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-worker-write-boundary-a02.md` before dispatch and at acceptance. C1 to C10 and C7b pass, including both C3 task-copy rows. Check C11's exact-selector requirement for every `closed` row; do not infer closure from a module-wide pass.

A C-80 security-profile context reviews this complete re-planned text before dispatch. Its review and checker output are prerequisites, not results claimed by this draft. Preserve the re-plan declaration and prior failed reviews; do not reset their history by renaming the family.

## Completion

Continue PR #431 on `tools/worker-write-boundary-a01` from `ea3c4fb84bbcf2419a17946fdd1ea68b2355102e`, retaining main base `51ba5801` and historical bases in the record. Open no second implementation PR and discard no unrelated work.

Keep a01's narrowed implementation and tests. The first a02 push deletes `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md` and adds `.orchestration/dotfiles-T133-worker-write-boundary-a02/task.md` byte-identical to the dispatched text; report its SHA256.

The Completion clauses of `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` apply with this branch, files and evidence paths, `dotfiles-T133-worker-write-boundary-followup-a01` unchanged as advisory P2 owner, and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-write-boundary-a02/task.md>` in RESULT. The a05-specific PR, copy-deletion, deadline and implementation requirements do not transfer. The orchestrator writes the owner task before assigning its first advisory P2.

Every worker-side fix round, including pre-push corrections, counts toward INV-6. Allow at most one independent pre-push review and no private correction/review loop beyond the declared round budget. Preserve a01's two spent rounds as history; only this explicit reset supplies a02's fresh budget.

Send each surviving P0/P1 in RESULT as `open:<id>` and stop integration for the operator's decision. Use `open:review-<review id>` for a review-body finding; do not hide surviving findings behind proposed dispositions or start another correction cycle.

Post no `@codex review` comment. Observe automatic final-head reviews within the bounded 15-minute window and record absence as `bot: none`. Required GitHub Actions checks pass before RESULT. Propose a disposition for every feedback item while preserving surviving P0/P1 findings as open.

Every gh write and git write is an individual command inside the sandbox, without shell chaining. Every other worker command also completes inside that sandbox and allowlist; anything that cannot complete there produces `AGMSG-PONG v1 status=blocked` naming the exact command and boundary.

Write evidence at required relative paths in the worker's own worktree and say so in RESULT. Use the `-worker-` infix for worker review evidence. Follow repository Crit-data and receipt rules without a browser review or human review request; the orchestrator copies evidence before acceptance.

`AGMSG-RESULT v1` names final head, base, branch, changed files, retained binding-removal inventory, scripts/installed paths, trusted anchor, hook and executable-source/key inventories, S01-S23 and handler-type fixture coverage, hostile-host contract cases, installed-version observations, PermissionRequest exception, settings destinations, staging/printed installation command, Bot findings/dispositions, open P0/P1 findings, exact selectors, measured totals, task-copy SHA256 and evidence paths. Separate historical observations from final-head results and name pending operator steps.

Report user-visible effects:

- Claude workers use `~/.claude-worker` and require separate Claude login.
- Trusted-path/worktree-configuration denies also affect Bash sandbox writes.
- Agmsg stores remain writable except `db/trusted-plugins`; plugin code is denied.
- Worker user policy adds no exclusions or Herdr socket, while shared administrative policy retains both.
- Existing worktrees or dedicated configuration state with noncanonical executable payloads refuse startup before workspace trust; the operator or orchestrator updates tracked settings through a guarded commit.
- Project MCP auto-approval and worktree plugin loading are disabled in the worker baseline; pre-existing MCP, plugin or helper payloads still refuse rather than being concealed by those disables.
- Tracked/main-local project hooks execute no project payload in workers; trusted worker delivery remains functional.
- Worker caches are private and every Claude seat fails when sandboxing is unavailable.
- Administrative policy requires sandboxing and disables unsandboxed retries for the orchestrator too.
- The former Linux gh exemption remains removed and the Worker Playbook authorizes no sandbox escape.
- Non-PermissionRequest commands receive the clean prefix; legacy orchestrator PermissionRequest is unchanged.
- Formatter/map availability and complete executable binding remain deferred.

Report that gh credential separation is not established. Shared credentials permit worker API merges despite native denials; P1-11 supplies next-records-PR detection, not prevention.

This task remains `security: true`. The orchestrator obtains a task-level audit and separate security-profile review of the final implementation head. Preserve D-024-26, the executable-binding class history, `decision-not-bound-to-execution`, `unbound-evidence`, `fail-open-on-error`, the tracked-hook startup finding, and the a02 input-inventory re-plan. Do not erase inherited history or relabel transferred findings as fixed.

Final-head feedback collection, audit, dispositions, acceptance and integration follow Orchestrator Playbook step 10 in order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the review receipt. Changed heads receive fresh required evidence; final-head security review precedes the gate.

The permission-surface change receives operator-backed approval through the existing process. The worker writes no approval row and treats no candidate-tree decision as authority.

Live deployment is the operator's post-merge `make update`, followed by `make install-managed-settings`, staging inspection and the printed platform-specific `sudo install -m 0644`. Record administrative installation separately from chezmoi application.

The operator logs in with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`, applies the prepared deterministic Codex permgate rule denying sandbox escapes, and restarts affected sessions.

Retain effective-policy inspection after deployment: installed administrative content, worker directory, static denies, configuration protection, writable stores, every covered startup source, explicit MCP/plugin disables and payload refusal, PermissionRequest exception, failure-policy coverage and sandbox startup. Check conflicting lower-scope relaxations and record shared capabilities without exposing credentials.

This inspection adds no removed binary-identity checker, trusted checker launch, executable version deployment probe or real-uv hook execution. Those remain with the binding task.

Merge alone establishes no deployment readiness. Record application, administrative installation, login, startup checks and the Codex permgate change before releasing dependent mechanisms for live operation; mechanisms requiring executable binding also wait for that prerequisite.

Local Bats, live enforcement, administrative installation, login, permgate policy changes and deployment are not performed by the worker.
Legacy PermissionRequest execution, formatter availability, same-UID access, shared capabilities, consumption races, later configuration changes and agmsg sourcing remain residuals.

## Checks (pasted by the orchestrator before each send)

```
dispatch to a010 (worker-e), 2026-10-19T20:55:28Z; task-consistency-check.py: OK; C-80 text-security-review.sh rounds: 2ae9e2c incorrect (1 P1), ebbb71b incorrect (3 findings; S1 input-inventory -> re-plan, design 5.14 item 1), b2a186e incorrect (1 P1 + 1 P2; amendment 1 by the review profile, items 1 and 8 amended), ac9ce14 correct; C-92 budget after the re-plan: 2 of 3 consumed; security: true (task-level audit and security review at acceptance); D-024-25 (a Codex seat takes this orchestrator-side security task), D-024-26 (write boundary alone; executable binding -> dotfiles-T133-trusted-entrypoint-binding-a01); reset_of a01 (PR #431 withdrawn at ea3c4fb8 after the final-head security P1); measured text: 1112 lines, 22 allowed files, 81 threat rows
amendment 1 to a010, 2026-10-19T23:40:53Z: the source cap amended once to the measured 1041 (previous_sha256 6d36b24e7601d49f34672f755ec15df375bb7a89cc1b78d51e69f79c8c51881c); task-consistency-check.py re-run below; C-80 verdict ac9ce14 covers the body (the amendment changes two sentences of the Change budget and this block); S2 counter: amendments 1, questions 0, worker_fix_rounds 1 (the pre-push review fix)
amendment 1b (clerical alignment, 2026-10-19T23:57:25Z): the `## Check` cap sentence (the one regime-ci.py reads) now says 1041 like the Change budget; no new authorisation (previous_sha256 e96dcac923bf2ba8d926e4618895f959be9c4f01ca29424a7f9251fd8eb5491d); C-89 miss: the consumer sentence was not enumerated at amendment 1
```

This re-planned text claims no implementation-test, CI or live-deployment results. Same-UID access, shared capabilities, consumption races and the transferred executable-binding work remain risks.