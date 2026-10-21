---
format: 2
task_id: dotfiles-T133-worker-write-boundary-a03
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
  - .orchestration/dotfiles-T133-worker-write-boundary-a03/**
after: []
reset_of: [dotfiles-T133-worker-write-boundary-a02]
threat_table:
  - control: home/dot_agents/agent-config.yaml
    disposition: "residual: the manifest declares the static protected inputs and closed worker-start schema; render tests check their correspondence without establishing same-UID isolation or complete executable binding."
  - control: home/.chezmoitemplates/claude-settings-managed.json
    disposition: "residual: the orchestrator baseline retains guarded non-PermissionRequest hooks and the unchanged legacy PermissionRequest command; its execution binding belongs to dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: home/.chezmoitemplates/claude-worker-settings.json
    disposition: "residual: dedicated policy retains narrow write grants, static denies, canonical delivery, MCP approval disables and explicit plugin disables; higher-scope inputs also undergo independent screening."
  - control: home/.chezmoitemplates/claude-managed-settings.json
    disposition: "residual: the administrative template declares sandbox requirements and the exact shared exceptions; content fixtures do not establish operator installation or live enforcement."
  - control: home/dot_claude/modify_private_settings.json
    disposition: "residual: exact managed-hook classification replaces owned legacy forms while preserving custom hooks and ordering; repeated merge fixtures check idempotence without proving descendant executable identity."
  - control: home/dot_claude-worker/modify_private_settings.json
    disposition: "residual: one source-aware closed-schema policy checks existing and prepared inputs before mutation; fixtures establish refusal at startup while later reloads and same-UID replacement remain possible."
  - control: home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    disposition: "residual: fixed operations and canonical launch identity suppress worker project payloads; complete interpreter, formatter and descendant binding remains with dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: .claude/settings.json
    disposition: "residual: every tracked command retains the clean prefix, installed guard, fixed operation and failure policy; portable render fixtures do not establish runtime timeout enforcement."
  - control: scripts/generate-agent-configs.py
    disposition: "residual: deterministic generation publishes manifest-owned policy without learning accepted keys or executable forms from candidate configuration; generation remains independent of deployment tool availability."
  - control: scripts/validate-agent-assets.py
    disposition: "residual: existing schema, exclusion, hook and asset checks remain, including legacy PermissionRequest recognition; no new bound-PermissionRequest or deployment checker is introduced."
  - control: Makefile
    disposition: "residual: staging prints privileged parent creation and file installation without executing either, and update-tree reconciles Claude settings after the Herdr installer; temporary fixtures check both sequences."
  - control: home/dot_local/bin/common/executable_herdr-agents
    disposition: "residual: all worker-start routes validate the repository anchor and all Claude routes run the same preflight before trust or mutation; no live seat or atomic consumption guarantee is claimed."
  - control: home/dot_agents/skills/agmsg-orchestration/SKILL.md
    disposition: "residual: the Worker Playbook has one sandbox-only command rule and no worker exemptions; documentation fixtures distinguish the retained orchestrator operations."
  - control: .gitignore
    disposition: "residual: .uv-cache remains ignored without removing either worklog/cache deny pattern; the temporary-checkout ignore fixture checks accidental-publication protection."
  - control: tests/unit/test_generate_agent_configs.py
    disposition: "residual: both-platform fixtures check separate policies, static inventory, closed-schema rendering and canonical commands without claiming live enforcement."
  - control: tests/unit/test_validate_agent_assets.py
    disposition: "residual: retained fixtures cover exact ordered exclusions, malformed variants and legacy permission-hook composition; formatting remains a CI concern."
  - control: tests/unit/test_claude_settings_merge.py
    disposition: "residual: migration and fake-update fixtures check custom-hook preservation, guarded replacement, installer ordering and idempotence without running a live update."
  - control: tests/unit/test_herdr_agents.py
    disposition: "residual: temporary roots and fake processes exercise source coverage, input refusals, launch routes and cache delivery without starting workers, plugins or authentication helpers."
  - control: tests/unit/test_agmsg_orchestration_docs.py
    disposition: "residual: fixtures read this task's dispatched copy and test the exact sandbox sentence and fixed-host ledger templates without introducing a ledger consumer."
  - control: tests/unit/test_claude_worker_settings.py
    disposition: "residual: render, merge, deny and guard fixtures verify configured policy and unchanged protected bytes without executing a bound PermissionRequest hook."
  - control: tests/unit/test_claude_managed_settings.py
    disposition: "residual: administrative-content and printed-command fixtures use temporary destinations and sudo markers; actual administrative installation remains an operator step."
  - control: .orchestration/dotfiles-T133-worker-write-boundary-a03/**
    disposition: "residual: evidence separates inherited observations, new regressions and final-head results, and records pending deployment without credentials or literal operator home paths."
  - control: <absolute-home>/.claude-worker/settings.json
    disposition: "residual: S01 is checked before regeneration under the closed settings schema, including every environment entry; a later same-UID replacement remains outside the startup guarantee."
  - control: <worktree>/.claude/settings.json
    disposition: "residual: S02 includes old tracked settings and is checked without rewriting it; a refusal requires an authorized guarded commit rather than launcher normalization."
  - control: <worktree>/.claude/settings.local.json
    disposition: "residual: S03 is inspected before exact legacy migration, so migration cannot conceal helpers, unknown keys or sandbox extensions."
  - control: <validated-anchor>/.claude/settings.local.json
    disposition: "residual: S04 is the validated repository's main-local source, independently screened because linked workers consume it; other repository roots refuse before preparation."
  - control: /Library/Application Support/ClaudeCode/managed-settings.json
    disposition: "residual: the Darwin S05 file is screened with the administrative schema through a temporary managed-root fixture; the worker never mutates the system file."
  - control: /etc/claude-code/managed-settings.json
    disposition: "residual: the Linux S05 file receives the same administrative schema and source-specific exceptions without claiming live installation."
  - control: <managed-root>/managed-settings.d/<name>.json
    disposition: "residual: S06 checks each drop-in independently before merging, admitting only canonical administrative fragments and refusing unknown keys or broadened lists."
  - control: <absolute-home>/.claude-worker/remote-settings.json
    disposition: "residual: S07 checks an existing cache independently; additional managed delivery that cannot be enumerated before launch produces a named refusal."
  - control: <worktree>/.mcp.json
    disposition: "residual: S08 admits only absent or empty server definitions regardless of trust or approval state, including ignored and untracked files."
  - control: <validated-anchor>/.mcp.json
    disposition: "residual: S09 is checked independently of nearer worktree definitions, so an absent or empty worktree file cannot conceal an inherited server."
  - control: <loaded-ancestor>/.mcp.json
    disposition: "residual: S10 checks each applicable ancestor file independently without using Git tracking or precedence as an exclusion."
  - control: <absolute-home>/.claude-worker/.claude.json
    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees"
  - control: S11 carried identity-field screening
    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member"
  - control: <skills-root>/<name>/.claude-plugin/plugin.json
    disposition: "residual: S12 includes enterprise skills at <managed-root>/.claude/skills and the other five admitted skills roots, even when the plugin is disabled."
  - control: <plugins-root>/installed_plugins.json
    disposition: "residual: S13 accepts only the declared registry shape and contained roots whose descriptors are read; an install record cannot add an unchecked root."
  - control: <plugins-root>/known_marketplaces.json
    disposition: "residual: S14 permits the declared empty registry only; refresh sources and executable header helpers have no canonical worker form."
  - control: <plugin-root>/.claude-plugin/plugin.json
    disposition: "residual: S15 admits declared descriptive metadata and scalar file references only; every selected file is inspected even for a disabled plugin."
  - control: <plugin-hook-file>
    disposition: "residual: S16 covers default and explicitly referenced hook files separately; plugin-owned executable handlers have no canonical worker operation."
  - control: <marketplace-root>/.claude-plugin/marketplace.json
    disposition: "residual: S17 admits descriptive metadata and an absent or empty plugin list only; command sources and additional plugin selections refuse."
  - control: <plugin-mcp-file>
    disposition: "residual: S18 checks default and referenced MCP files independently, admitting no nonempty worker server definitions."
  - control: <managed-root>/managed-mcp.json
    disposition: "residual: S19 applies the same empty-server rule independently of managed-settings precedence or administrative ownership."
  - control: <skills-root>/<name>/SKILL.md
    disposition: "residual: S20 inspects admitted Markdown files and frontmatter without invoking them; unknown frontmatter and inline or fenced dynamic commands refuse."
  - control: <commands-root>/<name>.md
    disposition: "residual: S21 reads every default or scalar-referenced command file; object mappings, inline content and directory references do not bypass Markdown inspection."
  - control: <agents-root>/<name>.md
    disposition: "residual: S22 inspects declared subagent metadata and refuses executable frontmatter without starting a subagent."
  - control: <plugin-lsp-file>
    disposition: "residual: S23 admits empty LSP configuration only; language-server commands and arguments have no canonical worker operation."
  - control: pre-start refusal of unknown settings keys
    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys"
  - control: pre-start refusal of undeclared provider selectors
    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors"
  - control: pre-start refusal of foreign repository roots
    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root"
  - control: pre-start refusal of object-form plugin components
    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components"
  - control: pre-start refusal of non-command hook handlers
    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch"
  - control: pre-start refusal of untrusted executable environment-file contents
    disposition: "closed: tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents"
  - control: plugin activation and additional executable components
    disposition: "residual: explicit false entries supplement screening; higher-scope enables, sync, dependencies, workflows, monitors and undeclared components refuse before launch."
  - control: non-file managed delivery and launch overrides
    disposition: "residual: unenumerable MDM, server delivery, host settings and caller-selected sources refuse without running a helper to discover their content."
  - control: lower-scope sandbox array merging
    disposition: "residual: source-specific canonical fragments reject extra exclusions, write roots and socket grants before Claude can merge arrays; live enforcement and later changes remain unverified."
  - control: actual enterprise skills root
    disposition: "residual: inventory starts at <managed-root>/.claude/skills, and temporary managed-root fixtures plant both Markdown and bundled plugin payloads there on both platforms."
  - control: ~/.agents/permgate-policy.yaml
    disposition: "residual: explicit static Edit denies protect the policy input and fixtures assert unchanged bytes; legacy hook environment and execution binding remain deferred."
  - control: ~/.local/lib/python*/site-packages
    disposition: "residual: directory-target and descendant denies retain protection for .pth, usercustomize.py and sitecustomize.py without claiming isolated interpreter startup."
  - control: ~/Library/Python/*/lib/python/site-packages
    disposition: "residual: macOS user-site directory and descendant patterns remain in the static inventory; planted-startup execution belongs to the binding task."
  - control: ~/.claude/hooks/orchestrator-only.sh
    disposition: "residual: the installed guard is an explicitly protected consumed input; routing fixtures do not close concurrent same-UID path swaps."
  - control: formatter and project-map configuration selection
    disposition: "residual: worker and outside-anchor input paths suppress tool execution; formatter availability and complete tool-chain binding remain deferred."
  - control: .orchestration/dotfiles-T133-worker-write-boundary-a02/task.md
    disposition: "residual: C3 authorizes deletion of this predecessor copy on the first a03 push only; all other predecessor artifacts and canonical history remain untouched."
  - control: .orchestration/dotfiles-T133-worker-write-boundary-a03/task.md
    disposition: "residual: the replacement copy is byte-identical to the dispatched a03 text and bound by SHA256 in TASK and RESULT."
  - control: evidence records
    disposition: "residual: report, validation, sandbox, learning, autoskill and review records preserve commands and identities while distinguishing proposals from acceptance authority."
  - control: task metadata
    disposition: "residual: the orchestrator checks reset lineage, scope, counters, finding classes, dispatched bytes and final-head evidence without treating worker proposals as approval."
  - control: metadata separators
    disposition: "residual: format-2 separators delimit the metadata, and the task-copy digest covers the entire front matter and body."
  - control: in-process effects
    disposition: "residual: generation and tests use repository files and temporary fixtures; the worker performs no deployment, login, administrative installation or restart."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: trusted parents supply clean environments before child execution and Python runs isolated; this task does not restore deferred version declarations or complete executable binding."
  - control: new or renamed scripts
    disposition: "residual: policy stays in the existing renderer, preparation script and guard; no new wrapper, state helper, interpreter resolver or executable-link manager is introduced."
  - control: "5.14 item 0: 脅威モデル"
    disposition: "residual: host controls reduce accidental and injected damage; shared credentials and same-UID processes prevent a seat-isolation claim."
  - control: "5.14 item 1: 書き込み境界"
    disposition: "residual: retained write policy and the closed startup schema implement this task's scope; later reloads and consumption races remain outside its guarantee."
  - control: "5.14 item 2: 無害化した環境を最初に"
    disposition: "residual: trusted-parent clean prefixes, fixed operations and declared environment inputs remain mandatory; the legacy orchestrator PermissionRequest and complete executable binding retain their separate owner."
  - control: "5.14 item 3: 信頼パスの境界検査"
    disposition: "residual: canonical root and component containment checks precede startup, including aliases; executable realpath binding remains with the binding task."
  - control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す"
    disposition: "residual: fixed dispatch avoids candidate-selected execution, while snapshots, last-use digests and complete executable identity remain with their consuming mechanisms."
  - control: "5.14 item 5: 出力と予約の同一性"
    disposition: "residual: this task introduces no reservation protocol; consuming orchestrator mechanisms retain ownership of full-head outputs and inode-bound locks."
  - control: "5.14 item 6: 正直な残余"
    disposition: "residual: the report retains shared credentials, administrative exceptions, socket access, agmsg sourcing, races, reloads and hook-event limitations."
  - control: "5.14 item 7: 検証"
    disposition: "residual: retained source-class fixtures and new allowlist regressions supply final-head evidence; shared trusted-execution helper adoption remains with P1-6."
  - control: "5.14 item 8: 承認はコミット済み台帳から読む"
    disposition: "residual: fixed-host ledger templates and hostile-host fixtures preserve the contract; P1-14 a05 and P1-6 own actual approval consumption."
  - control: "5.14 item 9: 私設キャッシュ"
    disposition: "residual: private worker caches and orchestrator-cache denies remain; exact interpreter declarations, resolver consumption and deployment binding remain separately owned."
  - control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない"
    disposition: "residual: the Worker Playbook permits no worker escape, while shared administrative capabilities and the operator's Codex permgate deployment remain explicit residuals."
  - control: canonical GitHub API host binding
    disposition: "residual: both ledger templates explicitly bind github.com and mryfmo/dotfiles; contract tests establish argv binding rather than enforcement by deferred consumers."
  - control: hook failure policy
    disposition: "residual: supported rendered entries retain onFailure block, but background hooks, excluded events and runtime timeout behavior establish no enforcement responsibility."
  - control: agmsg store driver and plugin selection
    disposition: "residual: plugin-code and trusted-plugin denies reduce one route; writable store-selected sourcing remains owned by dotfiles-T133-agmsg-hardening-a01."
  - control: orchestrator effect merge
    disposition: "residual: only the orchestrator integrates with final-head evidence and a pinned merge; shared credentials still permit API routes outside the native prefix denials."
  - control: orchestrator effect update-branch
    disposition: "residual: an update moves the head and requires fresh CI, feedback, local review, audit and security evidence before integration."
  - control: orchestrator effect forced worker removal
    disposition: "residual: none is planned; existing dirty-worktree protections remain and any operator-authorized discarded state must be recorded."
premises:
  - claim: >-
      This is the C-61 reset of a02 after both worker rounds were spent.
      Continue PR 431 on tools/worker-write-boundary-a01 from
      c0f50fa1383416240ad28959dbc4635afa777175, retaining its implementation.
      The preceding dispatched task and committed copy have SHA256
      ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50.
    sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md]
  - claim: >-
      The complete c0f50fa1 security review found AWS credential-chain
      selectors, a foreign-repository main-local inventory gap and
      object-form plugin command mappings. The local review found the
      incorrect enterprise skills root, lower-scope sandbox extensions,
      missing privileged parent creation and post-Herdr settings drift.
      The local chain stopped before a task-level audit; none exists for
      c0f50fa1. Repeated renderings in the local report are four findings,
      not additional independent findings.
    sources:
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-security-c0f50fa.md.last.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a02-local-review-c0f50fa.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a02.md
  - claim: >-
      D-024-26 retains the write boundary and transfers executable binding.
      D-024-29 freezes design 5.14; D-024-30 applies it by reference.
      The 2026-10-20 residual-list entry in this text records the allowlist
      generalisation without reopening the frozen items.
    sources:
      - .orchestration/decisions.tsv
      - $HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md
  - claim: >-
      The inherited read-only version observation is Claude Code 2.1.300.
      Documentation enumerations fetched at 2026-10-19T20:41:53Z were:
      settings scopes User, Shared project, Project local, Managed;
      precedence Managed settings, Command line, Project local settings,
      Shared project settings, User settings; MCP scopes Local, Project,
      User; hook types command, http, mcp_tool, prompt, agent; plugin
      origins @<marketplace>, @inline, @skills-dir, @synced; plugin
      enablement sources --add-dir, user, project, local, flag, managed;
      skills roots Enterprise, Personal, Project, Nested, Additional
      directory, Plugin; account-synced roots remain undeclared. Recheck the installed version
      and loader before changing implementation.
    fetched_at: "2026-10-19T20:41:53Z"
    sources:
      - https://code.claude.com/docs/en/settings
      - https://code.claude.com/docs/en/hooks
      - https://code.claude.com/docs/en/mcp#mcp-installation-scopes
      - https://code.claude.com/docs/en/plugins/loading
      - https://code.claude.com/docs/en/skills
  - claim: >-
      C-87: the orchestrator observed the documented ["Where skills live" table](https://code.claude.com/docs/en/skills) at 2026-10-20T04:47:57Z and the read-only loader probe at 2026-10-20T04:50Z. The Enterprise row says "`.claude/skills/<skill-name>/SKILL.md` in the managed settings directory", with Linux example `/etc/claude-code/.claude/skills/<skill-name>/`. The pinned 2.1.300 loader, SHA256 475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3, contains `/.claude/skills/` (11 occurrences), `.claude/skills/` (8), `/etc/claude-code` (6) and `/Library/Application Support/ClaudeCode` (3); the supplied probe excerpt is `LC_ALL=C /usr/bin/grep -a -o -E '…(\.claude/skills|/skills"|skills/)…' <loader> | sort | uniq -c`. These observations bind the enterprise inventory and fixture to `<managed-root>/.claude/skills`.
    sources: [https://code.claude.com/docs/en/skills, .orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md]
  - claim: "Worker a010 blocked before any edit (PONG 2694, 2026-10-20T04:00:43Z): the loader persists numStartups at start and hasCompletedOnboarding at onboarding; the orchestrator reproduced the installed-loader probe below, not a live worker start."
    sources: [.orchestration/acceptance/dotfiles-T133-worker-write-boundary-a03.md]
    probe: {executed_by: orchestrator, executed_at: "2026-10-20T04:10Z", loader: "$HOME/.local/share/mise/installs/npm-anthropic-ai-claude-code/2.1.300/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe", format_observed: Mach-O arm64}
    executed_commands:
      - {command: 'shasum -a 256 <loader>', output: '475517caa611e3318a2f298fa071287ec98955538df78c58f709ecc01e5ae2d3  <loader>'}
      - {command: '<loader> --version', output: '2.1.300 (Claude Code)'}
      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o numStartups <loader>', output: '12'}
      - {command: 'LC_ALL=C /usr/bin/grep -c -a -o hasCompletedOnboarding <loader>', output: '15'}
    quoted_string_probes: [{command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"numStartups"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasCompletedOnboarding"'' <loader>', output: '0'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"hasTrustDialogAccepted"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"oauthAccount"'' <loader>', output: '1'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"mcpServers"'' <loader>', output: '29'}, {command: 'LC_ALL=C /usr/bin/grep -c -a -o ''"enabledMcpjsonServers"'' <loader>', output: '5'}]
  - claim: >-
      The single source inventory is S01-S23 below plus executable
      environment-file contents admitted by the launch-input schema. Each parameter denotes
      every actual matching file, inspected independently before merging.
      User means the dedicated configuration directory; managed-root is
      the platform directory containing managed-settings.json.
      S01 user/settings.json; S02 worktree/.claude/settings.json;
      S03 worktree/.claude/settings.local.json; S04 validated-anchor/.claude/settings.local.json;
      S05 platform managed-settings.json; S06 each managed-root/managed-settings.d/*.json;
      S07 user/remote-settings.json plus independently enumerated non-file managed delivery;
      S08 worktree/.mcp.json; S09 validated-anchor/.mcp.json;
      S10 every other loaded ancestor .mcp.json;
      S11 user/.claude.json, screened declared structures and carried identity fields before launcher regeneration;
      S12 each skills-root/<name>/.claude-plugin/plugin.json;
      S13 user/plugins/installed_plugins.json; S14 user/plugins/known_marketplaces.json;
      S15 each admitted plugin-root/.claude-plugin/plugin.json;
      S16 every default hooks/hooks.json and explicitly referenced plugin hook file;
      S17 every admitted marketplace-root/.claude-plugin/marketplace.json;
      S18 every default or referenced plugin MCP file; S19 managed-root/managed-mcp.json;
      S20 every applicable SKILL.md; S21 every applicable legacy command Markdown file;
      S22 every applicable subagent Markdown file;
      S23 every default or referenced plugin LSP file.
      Non-file managed delivery and caller-selected inputs must fit the
      same closed schema and read set or cause a named refusal.
    sources:
      - https://code.claude.com/docs/en/settings
      - https://code.claude.com/docs/en/managed-settings
      - https://code.claude.com/docs/en/server-managed-settings
      - https://code.claude.com/docs/en/plugins/manifest-reference
      - https://code.claude.com/docs/en/skills
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-a03 — plan 024 P1-15; seat a010

## Goal and reset

[memory:decision] Reset a02 after C-61 exhausted its two worker rounds. Worker a010 is Codex in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`. Continue `tools/worker-write-boundary-a01` and PR #431 from `c0f50fa1383416240ad28959dbc4635afa777175`; keep the a02 implementation and open no second PR.

Replace executable-key denylisting with one manifest-declared, renderer-owned closed startup schema. A worker start accepts only declared settings keys, environment names, configuration sources, roots and value forms. Every other forwarded input causes a named refusal before trust, migration, regeneration or launch; discarded S11 state follows the launcher-generation rule below. Fix the four local-review findings within the same authorized files.

[memory:failure] a01 spent two rounds and a02 spent two rounds. Neither a new task name nor a clean historical test result closes their findings. This explicit reset supplies a03's fresh budget: at most two worker correction rounds in total, including pre-push corrections, and at most one independent pre-push review.

The current implementation is the starting point, not an approved result. The c0f50fa1 local chain stopped before its task-level audit. Obtain new final-head audit and security evidence; do not describe either as inherited.

Amendment 1 accepts `text-security:f7af699:1`, the sole P1 at line 374 in `.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-f7af699.md.last.md`, and adds only the executable environment-file contents control and its evidence/budget consequences. `previous_sha256: f7af699666211dd95cc3d3addfbbbecee9359b91c7916b1e2e54e47577e2d6d4`. This is task-text amendment 1, not a worker correction round.

Amendment 2 implements D-024-34, the second input-inventory re-plan after the allowlist, mapping accepted rows `worker:5067ed0:1 input-inventory` and `text-security:f7af699:1 input-inventory` to launcher-generated files. `previous_sha256: 5067ed07cf353371dd32091851cb286ad3011f190db5e6d4e7d670117ebbf669`. The worker blocked before any edit; this is task-text amendment 2, not a worker correction round. It changes S11, identity screening, three fixtures and their budget consequences; the `CLAUDE_ENV_FILE` control rows and fixture remain unchanged. Amendment 3 implements D-024-35, the third input-inventory re-plan, mapping accepted row `text-security:efa211d:1 input-inventory` from C-80 round 3's sole P2 at line 431 in `.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-efa211d.md.last.md`; `previous_sha256: efa211d1fa4e8fc90512fc88acf6e8cad1127d10a74defafe5adab2e2817faf5`. It removes S11's per-project inventory, regenerates `projects: {}` and relies on the existing spawn-readiness trust-dialog acceptance; an A-then-B shared-directory fixture replaces the same-worktree restart fixture. This is task-text amendment 3, not a worker correction round; identity screening, top-level MCP tamper refusal and the `CLAUDE_ENV_FILE` control remain. Amendment 4 accepts `text-security:be969e3:1 input-inventory`, C-80 round 4's sole P1 at line 425 in `.orchestration/validation/dotfiles-T133-worker-write-boundary-a03-text-security-be969e3.md.last.md`; `previous_sha256: be969e32246c9a1a55e61654d28be9111328fde0e7730a300465bb2e43b0c47e`. It corrects only the enterprise skills root to `<managed-root>/.claude/skills`, the corresponding S12 inventory and fixture, and their C-87 premise; the admitted skills roots are the documented six. This is task-text amendment 4, not a worker correction round; scope, implementation budgets and all other controls remain unchanged.

## Design and finding history

Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 by reference, including its residual list. D-024-29 keeps items 0-10 frozen; D-024-30 narrows C-88 to exact contract sentences asserted by tests.

Item 1 applies to dedicated worker settings, static input-derived write protection and refusal before startup.
Item 2 applies to trusted-parent execution, clean environments and fixed command selection.
Item 3 applies to canonical anchor, worktree and component identities before consumption.
Item 8 applies to committed approval authority through explicitly host-bound repository API calls.
Item 9 applies to private caches and the trusted parent's interpreter/cache inputs.

**2026-10-20 residual-list entry — owner: dotfiles-T133-worker-write-boundary-a03:** generalise item 1's refusal of executable payloads the launcher did not write to every startup input: accept only a manifest/renderer-declared closed schema of settings, environment names, sources, roots and value forms, and refuse everything else. D-024-34 treats global state and `CLAUDE_ENV_FILE` as one family of launcher-generated files: regenerate at every start from declared contents, carrying only screened identity fields where specified. D-024-35 removes all per-project inventory from generated global state: `projects` is always `{}` and workspace trust comes from the launcher's existing readiness-dialog acceptance. This changes the implementation approach without amending the frozen design. The orchestrator carries this entry into the design's residual list; the worker edits no design file.

Read the full a02 acceptance record and both c0f50fa1 reviews named in `premises:`. Retain the following history and finding classes in the a03 report and acceptance lineage:

| Finding | Class | Required treatment |
| --- | --- | --- |
| `text-security:2ae9e2c:1` | input-inventory | Project `.mcp.json` remains independently screened. |
| `text-security:ebbb71b:1` | input-inventory | Skills-directory plugins remain inventoried even when disabled. |
| `text-security:ebbb71b:2` | input-inventory | Dedicated global state regenerates `mcpServers: {}` and `projects: {}`; native project entries are discarded. |
| `text-security:ebbb71b:3` | repository-binding | Canonical main comes from the fixed repository API. |
| `text-security:b2a186e:1` | input-inventory | Inspect handler type before command; non-command types refuse. |
| `text-security:b2a186e:2` | repository-binding | Both ledger calls bind `--hostname github.com`. |
| `text-security:ac9ce14:0` | correct | Historical text approval only; it does not approve a03. |
| a02 independent pre-push review | input-inventory | Retain fixes for `env.HOME` guard selection and fenced dynamic commands. |
| `local:79ea98a:1` | tool-environment | Retain manifest-generated `--advisor fable` acceptance. |
| `local:79ea98a:2` | tool-environment | Retain absolute tool paths and attachment identity environment. |
| `local:79ea98a:3-4` | partial-fix | Retain custom-hook preservation and legacy PreToolUse migration. |
| `security:c0f50fa:1` | input-inventory | Refuse undeclared credential-chain/provider selectors. |
| `security:c0f50fa:2` | input-inventory | Refuse worker starts for repositories other than the validated anchor. |
| `security:c0f50fa:3` | input-inventory | Refuse object and inline plugin/command components. |
| `local:c0f50fa:1` | tool-environment | Inventory enterprise skills under the actual managed root. |
| `local:c0f50fa:2` | tool-environment | Reject lower-scope sandbox extensions before array merging. |
| `local:c0f50fa:3-4` | partial-fix | Fix printed parent creation and post-installer reconciliation here. |
| `text-security:f7af699:1` | input-inventory | Admit executable environment-file contents only when absent, empty or launcher-generated for this start. |
| `worker:5067ed0:1`, `text-security:efa211d:1` | input-inventory | Regenerate S11 at every start with `projects: {}` and screened identity; discard native persisted state, including every project's state, and use the launcher's existing spawn-readiness trust-dialog acceptance. |
| `text-security:be969e3:1` | input-inventory | Inventory enterprise skills and plant both Markdown and bundled plugin fixtures under `<managed-root>/.claude/skills`, following the C-87 documented table and pinned-loader probe. |

S1 first triggered on the three source omissions in 2ae9e2c/ebbb71b. The re-plan enumerated S01-S23, but subsequent findings still exploited open field/value acceptance; the c0f50fa1 security findings bring that post-re-plan family to its sixth finding. This reset changes the approach rather than adding three more denylist entries.

Preserve the advisory-owner history exactly as history. The two c0f50fa1 P2 fixes are explicitly brought into a03 by this text; the orchestrator reconciles their owner rows and updates dependent task references. The worker edits no canonical acceptance or owner task.

Retain D-024-26's transferred binding findings, including `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. Do not relabel them as fixed.

## Closed startup schema

Declare this schema in `home/dot_agents/agent-config.yaml` and expose it through the existing renderer/preparation code. Candidate files, Git objects and installed upstream schemas never define their own acceptance policy. Add no new helper, generated output file or dependency.

The schema below is exhaustive for data forwarded to the loader. Objects reject unknown keys at every level, including nested objects and records that would otherwise be preserved; S11 fields designated for discard are not screened or preserved. Reject duplicate JSON keys, wrong types, Boolean/integer substitutions, unreadable inputs and unsupported forms. Missing optional fields may pass; a present field must match its declared source-specific form.

### Settings and values

The only settings keys are `permissions`, `sandbox`, `hooks`, `env`, `enableAllProjectMcpServers`, `enabledMcpjsonServers`, `disabledMcpjsonServers`, `enabledPlugins`, `syncClaudeAiPlugins`, `syncClaudeAiSkills`, `extraKnownMarketplaces` and `disableSkillShellExecution`.

| Node | Accepted shape and values |
| --- | --- |
| `permissions` | Only `defaultMode`, `deny`, `additionalDirectories`; `defaultMode` is `auto` where applicable; `additionalDirectories` is `[]`; `deny` is a renderer-declared worker/native-denial fragment for that source. No caller-added allow/ask rule or alternate permission mode. |
| `sandbox` | Only the keys emitted by the worker or administrative renderer: `enabled`, `failIfUnavailable`, `autoAllowBashIfSandboxed`, `allowUnsandboxedCommands`, `excludedCommands`, `filesystem`, `network`, `enableWeakerNestedSandbox`, `enableWeakerNetworkIsolation`, `allowAppleEvents`. |
| `sandbox.filesystem` | Only `allowWrite`, `disabled`; exact source-specific canonical values. Worker write grants are the four declared agmsg stores; ordinary worktree/cache writes remain provided by the worktree boundary. |
| `sandbox.network` | Only `allowedDomains`, `allowUnixSockets`, `allowAllUnixSockets`, `allowLocalBinding`; exact source-specific canonical values. |
| Sandbox lists and Booleans | Every present leaf/list equals the canonical worker fragment in S01-S04 or administrative fragment in S05-S07. Worker exclusions are empty; additional write roots/sockets are refused. Only administrative sources may contain the exact shared three exclusions and single Herdr socket. |
| `hooks` | Only source/event/matcher/operation combinations generated by the trusted renderer or delivery constructor. Groups have only `matcher`, `hooks`; handlers have only renderer-declared `type`, `command`, `timeout`, `async`, `statusMessage`, `onFailure`, with exact canonical values. |
| Handler type | Only the string `command`; validate it before reading `command`. HTTP, MCP-tool, prompt, agent, unknown, missing, null and non-string types refuse. |
| MCP approval fields | `enableAllProjectMcpServers: false`; `enabledMcpjsonServers: []`; `disabledMcpjsonServers: []` when present. Approval state never exempts a server definition. |
| Plugin fields | `enabledPlugins` maps only manifest-known or inventoried plugin identities to `false`; both sync fields are `false`; `extraKnownMarketplaces` is `{}`. |
| Skill execution | `disableSkillShellExecution`, when present, is `true`. |
| `env` | Only the four exact name/value pairs in the next subsection; arbitrary strings, maps and provider credentials are not preserved. |

Absent or empty settings objects pass where the source permits them. Administrative drop-ins/cache may contain canonical partial objects; partial means omitted declared fields, never new fields or alternate values. Validate each list before merging so an empty generated worker list cannot conceal a broader lower-scope array.

There is no canonical worker setting for helpers, status-line commands, wrappers, alternate sandbox executables, policy helpers or authentication refresh/export commands. Their keys refuse as undeclared, including misplaced forms. The orchestrator managed PermissionRequest exception is not a worker-start exception.

The old instruction to preserve unrelated non-executable state now applies only to fields admitted by this schema. Unknown settings refuse without deletion or normalization; S11 alone discards pre-existing fields outside its declared structures and carried identity, without screening or forwarding them.

### Environment and launch arguments

Settings `env` admits exactly `GH_TELEMETRY="false"`, `DO_NOT_TRACK="1"`, `CHECKPOINT_DISABLE="1"` and `AWS_EC2_METADATA_DISABLED="true"`, as declared by the manifest. The last name is the sole declared `AWS_*` exception and cannot select credentials or a provider.

The launch-input schema admits only these names, with source-specific values supplied or checked by the trusted parent:

| Names | Value authority |
| --- | --- |
| `HOME`, `PATH`, `LANG`, `TERM` | Validated passwd home; prescribed system-only child PATH; `C.UTF-8`; declared terminal value. Hook children retain `TERM=dumb`. |
| `TMPDIR` | Canonical trusted temporary directory supplied by the parent, not a candidate configuration root. |
| `CLAUDE_CONFIG_DIR` | Exactly the dedicated worker directory under the validated home. |
| `CLAUDE_PROJECT_DIR`, `CLAUDE_ENV_FILE` | Parent-bound canonical project identity and runtime shell file; `CLAUDE_ENV_FILE` additionally requires the executable-content control below. |
| `UV_CACHE_DIR`, `UV_PYTHON_INSTALL_DIR` | Exactly `<canonical-worktree>/.uv-cache` and its `python` child. |
| `AGMSG_RESOLVE_PROJECT`, `AGMSG_STORAGE_PATH`, `AGMSG_CC_MONITOR_KEEP_ALIVE` | `0`, the validated launcher store selection, and the declared monitor value; unset default-store selection remains supported. |
| `HERDR_ENV`, `HERDR_PANE_ID`, `HERDR_WORKSPACE_ID`, `HERDR_AGENTS_LAYOUT`, `HERDR_SOCKET_PATH` | Validated control-plane identity, `managed` layout and canonical configured socket; these grant no worker sandbox exception. |
| `CLAUDE_CODE_SESSION_ID`, `CLAUDE_PID`, `AGMSG_AGENT_PID` | Parent/runtime session identifier and numeric process identifiers where required by canonical attachment/delivery. |
| `CLICOLOR_FORCE`, `FORCE_COLOR` | Launcher-written `1` only where the launch route uses them. |
| `GH_TELEMETRY`, `DO_NOT_TRACK`, `CHECKPOINT_DISABLE`, `AWS_EC2_METADATA_DISABLED` | The four fixed values above. |
| `CHEZMOI_SOURCE_DIR`, `CHEZMOI_HOME_DIR` | Preparation-only trusted source/home bindings; not caller-selected worker configuration or executable roots. |

The read-only amendment-1 probe of the [documented environment variables](https://code.claude.com/docs/en/env-vars) identifies `CLAUDE_ENV_FILE` as the only name admitted above that selects a file whose contents execute: Claude runs its shell contents before Bash commands. No other admitted name has that documented role; `CLAUDE_CODE_SHELL` and `CLAUDE_CODE_SHELL_PREFIX` remain undeclared. Include the named file's contents in the preflight read set alongside S01-S23.

For every admitted executable-content file variable, preflight accepts its named file only when absent, empty, or byte-identical to canonical contents generated by the launcher for this start. Inspect without sourcing or executing it; unreadable/nonregular files and any other contents refuse before trust, migration, regeneration, hooks or worker commands with `worker startup refused: <file>: <variable>: noncanonical executable environment file contents`. Preserve refused bytes; never overwrite a planted file to make it pass. After all preflight checks pass, the launcher itself writes the canonical runtime-file contents, records SHA256 bound to the variable, canonical file and this start in existing startup state/evidence, and verifies those bytes before forwarding. Candidate-supplied or prior-start digests cannot authorize contents. Reuse the existing runtime file and startup state; add no sidecar, helper or generated configuration output. Later replacement races and reloads retain their existing residual owners.

Validate proposed worker configuration inputs before forwarding them. A clean child environment contains only the names declared for that child role; do not inherit the caller environment wholesale. Unknown proposed environment names refuse rather than becoming an unchecked pass-through. Existing profile/control-plane variables used to select a worker are consumed through their existing manifest-owned interfaces, not forwarded as arbitrary worker settings.

Every `CLAUDE_CODE_USE_*`, `AWS_*`, `ANTHROPIC_*`, `*_API_KEY`, `*_TOKEN` and `*_PROFILE` name refuses unless explicitly declared above with its exact allowed value. In particular refuse `CLAUDE_CODE_USE_BEDROCK`, `AWS_CONFIG_FILE`, `AWS_SHARED_CREDENTIALS_FILE` and `AWS_PROFILE` in settings and launch inputs before any credential lookup or helper execution. Add no AWS configuration parser.

No shell/interpreter startup or loader override is declared: `BASH_ENV`, `ENV`, `NODE_OPTIONS`, `NODE_PATH`, `PYTHON*`, `LD_*`, `DYLD_*`, shell wrappers and alternate configuration/cache roots refuse as worker inputs. Do not print their values.

Preserve the manifest-generated Claude argument interface: only `--model`, `--effort`, `--advisor` with their declared profile values, including `--advisor fable`. Caller-added settings, MCP, plugin, agent and additional-directory arguments refuse. Keep existing Codex arguments and network/shared-Git policy unchanged.

If the installed loader or an existing launch route requires another name or preserved state field, send a blocked PONG with the exact boundary and evidence. Do not silently widen the schema, introduce wildcard name acceptance or treat a runtime default as authorization.

### Sources, roots and component forms

The sole repository anchor is the manifest declaration resolving to `$HOME/Workspace/dotfiles`. Bind its identity to the validated passwd home and actual main checkout, resolving symlinks and filesystem case aliases. Worker roots must be registered linked worktrees beneath that anchor's declared `.claude/worktrees/` root with the same Git common directory.

Every worker launch route, for either worker kind, refuses another repository before worktree creation, identity registration, hook writes, workspace trust or spawn. The refusal names this task: `worker startup refused: dotfiles-T133-worker-write-boundary-a03: unsupported repository root`. Do not fix the foreign-root finding by inspecting the fixed anchor while launching elsewhere.

Admitted configuration roots are the dedicated worker directory, the validated anchor/worktree `.claude` directories, applicable nested worktree and additional-directory `.claude` directories, the platform managed root and contained plugin roots discovered through the declared registry. Inherited MCP files are the independently enumerated ancestor read set. No account-synced, inline, seed, alternate cache or caller-selected root is admitted; caller-added additional-directory arguments remain refused.

The admitted skills roots are exactly Enterprise `<managed-root>/.claude/skills` (macOS `/Library/Application Support/ClaudeCode/.claude/skills`, Linux `/etc/claude-code/.claude/skills`), Personal `<absolute-home>/.claude-worker/skills` under the dedicated configuration directory, Project `<project>/.claude/skills`, Nested `<subdir>/.claude/skills`, Additional directory `<add-dir>/.claude/skills` under an applicable `--add-dir` directory, and Plugin `<plugin>/skills`. Inspect both `<skills-root>/<name>/SKILL.md` and bundled `<skills-root>/<name>/.claude-plugin/plugin.json`. Managed command/agent locations likewise start at the actual managed root. Resolve every selected path and refuse containment escapes, unsupported aliases, missing references or unreadable files.

| Source form | Closed acceptance |
| --- | --- |
| S08-S10, S18-S19 | Objects containing only absent or empty `mcpServers`/`managedMcpServers` maps. No server, including remote-only definitions, is canonical here. |
| S11 global state | At every start, after all preflight checks pass and before any loader/worker command, write the existing `CLAUDE_CONFIG_DIR/.claude.json` from scratch: `mcpServers: {}`, `projects: {}` and `hasCompletedOnboarding: true`, plus screened identity fields below. The generated file carries no per-project inventory or pre-generated workspace trust. Never merge the previous file into this output. |
| S11 pre-existing structures and identity | The existing file must be a JSON object. Missing optional retained fields pass and generated fields are written anew. Present top-level `mcpServers` must be `{}`. Carry optional `oauthAccount` only as an object with string-only members from this documented fixed set: `accountUuid`, `emailAddress`, `organizationUuid`, `displayName`, `fullName`, `organizationRole`, `workspaceRole`; declare the same set in the manifest and fixtures. Carry optional `userID` only as a string matching `^[0-9a-f]{64}$`, the installed loader's hex form. Undeclared identity members, non-string `oauthAccount` members, invalid identity values and a nonempty or malformed top-level MCP map refuse with `worker startup refused: <state-file>: <offending-key>: <named reason>` before any command or mutation, preserving refused bytes. Nonempty top-level servers use the exact reason `noncanonical global state` as tamper evidence. |
| S12/S15 plugin descriptor | Only `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and the component keys `hooks`, `mcpServers`, `lspServers`, `commands`, `agents`, `skills`. Descriptive fields are strings, keywords are strings, and author has only string `name`, `email`, `url`. |
| Component references | Each present component is one scalar string referencing a regular file within its admitted root. The screening reads that file under its source schema before accepting it. Arrays, objects, inline content, URLs and explicit directory references refuse. Default component directories are independently expanded into inspected files. |
| S13 installed registry | Only `version: 2` and `plugins`; plugin IDs map to record lists with only `scope`, `installPath`, `version`, `installedAt`, `lastUpdated`, `gitCommitSha`, `projectPath`. Scope is user/project/local; paths are contained and project-bound; descriptive fields are strings and a present commit is 40 hex. Every referenced descriptor is read and every discovered ID is disabled. |
| S14 marketplace registry | Only `{}`; no refresh source or executable header helper is canonical. |
| S16 hook file | Only an absent/empty `hooks` object; plugin-owned handlers have no canonical worker operation. |
| S17 marketplace descriptor | Only descriptive `name`, `owner`, `metadata`, `plugins`; owner has string name/email, metadata has string description/version, and plugins is absent or `[]`. Additional plugin selections refuse. |
| S20-S22 Markdown | Plain text with the existing restricted frontmatter grammar: name, description, argument-hint, disable-model-invocation, user-invocable, allowed-tools, model. Booleans are Boolean, model/tool selections are manifest-declared values, and unknown/nested executable forms refuse. Dynamic shell expansion, including fenced forms, refuses everywhere. |
| S23 LSP | Only `{}`; command/args definitions are not canonical. |
| Non-file managed inputs | Enumerated canonical administrative data only; otherwise refuse with the managed source name before executing any helper or starting Claude. |

For S11, every other pre-existing top-level field, including the entire `projects` value and all its contents, `numStartups`, prior onboarding state, tips/changelog caches, project `history`, `allowedTools` and cost counters, is neither screened nor preserved; only syntax/duplicate-key/readability checks apply to the whole input. Discarded objects and arrays are never recursively screened or forwarded. Generate onboarding anew and `projects: {}`, preserve only screened identity values, and reuse the existing atomic writer after the complete preflight; the loader regenerates native state. The anchor's workspace trust is established by the launcher's existing acceptance of the workspace-trust dialog during spawn's readiness wait (`herdr-agents --add-worker` for a Claude worker, documented in the SKILL's 'Regime activation and progress' section). All Claude workers share `CLAUDE_CONFIG_DIR` at `$HOME/.claude-worker`; discarding the prior `projects` value lets sequential sibling starts succeed. A loader requiring another preserved field blocks and retasks rather than widening silently.

These restrictions also apply to disabled plugins and shadowed sources. Do not recursively ignore an unknown object because it lacks a familiar executable key. A plugin `commands` mapping containing `{"source": ...}` or inline `content` refuses at the selecting file/key.

## Implementation and retained controls

1. Keep one preflight over S01-S23, admitted executable environment-file contents and the closed schema. Every Claude route calls it before workspace trust, migration, normalization, regeneration or execution. Enumerate through the filesystem, including ignored/untracked inputs; neither Git tracking nor a nearer definition removes a source. Inspect implicit and selected components separately without executing helpers, installing packages, fetching plugins or starting servers.

2. Refusals identify the actual source and key/class without printing payloads, environment values, URLs with credentials or authentication material. Preserve the handler message `worker startup refused: <source-file>: hooks.<event>[<group-index>].hooks[<handler-index>]: noncanonical hook handler`, with zero-based indices. Other refusals use `worker startup refused: <source>: <key>: <named reason>`. Unknown settings, selectors, roots, components and source forms each receive a named reason.

3. Retain exact recognized legacy-delivery classification, including canonical project binding. First screen every source; only after complete success migrate recognized owned entries, validate the prepared result under the same schema, then write. Unknown content outside S11's discard partition refuses without changing any pre-existing bytes; successful S11 regeneration intentionally replaces discarded state only after every source passes. Never rewrite tracked settings or create a local file merely for migration. Keep repeated preparation and delivery-tool-unavailable behavior.

4. Retain dedicated `CLAUDE_CONFIG_DIR`, both private cache variables on every actual worker route, `AGMSG_RESOLVE_PROJECT=0`, validated `AGMSG_STORAGE_PATH`, canonical attachment identity and `onFailure: "block"` where supported. A writable `run/proj.<pid>.project` cannot replace the explicit project identity. Preserve the a02 absolute Herdr/jq/Node/npm/Codex calls and attachment environment; fixed PATH must not regress attachment or default seating.

5. Keep static `trusted_paths` derived from trusted executable inputs, not Git trees/indexes. Preserve anchored source/control paths, tracked/main-local settings, `.orchestration`, both `.agents/worklog/**` and `.agents/worklog/uv-cache/**`, worktree `.claude` directory/descendant targets and `.mcp.json`. Ordinary worktree source and private cache writes remain available.

6. Retain explicit protection of `~/.agents/agent-config.yaml`, model profiles, permgate policy, skill scripts/SKILL files, agmsg plugin code and `db/trusted-plugins`, `~/.claude/**`, `~/.claude-worker/**`, installed guard, local wrappers/application code, configuration/state/tool installations and shared uv caches. Keep directory and descendant user-site protection for `.pth`, `usercustomize.py` and `sitecustomize.py` on both platforms. Add no blanket `~/.agents/**` or `~/.local/**` deny: agmsg `db`, `teams`, `run`, `ext-tools` stay writable except `db/trusted-plugins`.

7. Retain separate orchestrator, worker and administrative renders. Worker policy keeps `defaultMode: auto`, sandbox startup failure, disabled unsandboxed requests, empty user exclusions, restricted writes, no user Herdr socket, explicit MCP auto-approval disables, account sync off and false plugin entries including discovered `@skills-dir` identities. Empty maps alone do not disable plugins or replace screening.

8. Administrative settings retain enabled sandboxing, `failIfUnavailable: true`, disabled unsandboxed requests, filesystem enforcement, disabled weaker isolation/Apple Events/all-socket/local-binding switches, exactly the Herdr socket, and exactly these ordered exclusions: `agmsg-dispatch *`, `herdr-agents *`, `<absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *`. These shared capabilities remain available to every Claude seat and authorize no worker escape. Lower-scope canonical validation rejects extra exclusions, writes or sockets before array merging.

9. Keep the orchestrator managed PermissionRequest command exactly `~/.local/bin/common/permgate claude`, including existing legacy/stale-ccgate recognition. Add no clean prefix, new guard selector, interpreter declaration or structural bound-command validator for it. Every other rendered command retains the existing `/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"` prefix and fixed installed guard operation, with delivery/attachment re-exports only as declared.

10. Trusted parents supply the clean environment before child execution; do not replace this with an in-script self-reexec or caller sentinel. Preserve isolated Python and the existing absolute interpreter conventions. Add no version pins, private executable directory or PATH fallback. Git inspection follows design 5.14's sanitized environment, explicit checkout identity, disabled lazy fetch/hooks/fsmonitor/submodule recursion and disabled external diff/textconv. Do not execute arbitrary task-body shell strings as probes.

11. Preserve guard routing, fixed payload paths, argument boundaries, stdin and child status. Canonical worker/sibling/unrelated/missing launch identities execute no orchestrator project payload. Only fixed installed worker-delivery operations run for workers. Formatter/map operations also reject worker/outside-anchor tool inputs. Keep tracked settings portable and all existing event/validator markers.

12. Preserve managed SessionStart/PostToolUse/PreToolUse migration, custom-hook ordering, mixed entries, escaped-tilde distinctions, stale replacement and idempotence. For `make update`, reconcile the managed Claude settings after `scripts/update-agent-assets.sh` runs Herdr's installer, using the allowed Makefile/merge/renderer surfaces. Do not edit the updater script or import its unguarded hook as canonical. Verify one effective guarded hook and no managed-settings drift after repeated fake updates.

13. `install-managed-settings` still stages `~/.claude/managed-settings.rendered.json` nonprivileged. Print a quoted privileged `mkdir -p` for the detected administrative parent before the existing quoted `sudo install -m 0644` command. Cover both platform destinations and homes containing spaces. Execute neither privileged command; do not install, log in or restart.

14. Keep all existing validator checks, exact three-entry exclusion fixtures on both platforms, legacy PermissionRequest validity, duplicate-hook checks, ordering/timeouts, freshness, portability and secret/home-path scanning. Add no bound-PermissionRequest mode. `.gitignore` retains `.uv-cache/` as this task's only addition.

15. Worker Playbook step 4 retains this exact test-asserted sentence:

> Complete every worker command, including gh, git push and authenticated git fetch, inside the sandbox and allowlist without forbidden actions or escalation; anything that cannot complete there is `AGMSG-PONG v1 status=blocked` naming the exact command and boundary.

The entire Worker Playbook, including steps 2, 5 and 11, authorizes no exception. Evidence-sync writes/masking, CompactionDB consolidation and agmsg-dispatch control-plane exemptions remain orchestrator-only. Workers write required relative evidence in their own worktree; the orchestrator copies it before acceptance. Preserve merged documentation changes and run the complete documentation module.

## Regression fixtures

Write the new tests before implementation. Use the existing temporary-HOME, managed-root, linked-worktree and fake-launcher builders. Tests execute no payload, credential helper, HTTP endpoint, server, plugin, subagent or live worker.

Each refusal fixture asserts the source/key or named root message, unchanged existing bytes, no migration/regeneration, no trust acceptance, no spawn and absent execution/request markers. Positive absent/canonical controls and repeated starts remain covered.

| Selector | Required coverage |
| --- | --- |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_shared_global_state_across_worktrees` | Red on c0f50fa1, green after: sequentially start registered linked-worktree workers A then B on one shared `CLAUDE_CONFIG_DIR`. A's start leaves the regenerated file; simulated loader writes then add A's project entry with a `history` list. B's start succeeds and, before its first command, leaves exactly the regenerated file with `projects: {}` and screened identity. Replace any planted-project-key refusal and same-worktree restart fixture with this cross-worktree sequence. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_regenerates_global_state_with_screened_identity` | Red on c0f50fa1, green after: pre-existing S11 has `numStartups: 5`, `hasCompletedOnboarding: true`, `projects[anchor].history` as a list and synthetic valid `oauthAccount`/hex `userID`. A fake worker start succeeds; before its first command the file equals exactly `mcpServers: {}`, `projects: {}`, `hasCompletedOnboarding: true` plus unchanged screened identity. Cover absent state/identity; all discarded fields and project contents disappear without semantic screening. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonempty_global_mcp_servers` | Red on c0f50fa1, green after: pre-existing S11 has nonempty top-level `mcpServers`; assert exactly `worker startup refused: <state-file>: mcpServers: noncanonical global state` before any command, preserving all bytes and absent mutation/trust/spawn/execution markers. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_nonstring_oauth_account_member` | Red on c0f50fa1, green after: a documented `oauthAccount` member contains an object; refuse with the file and exact member key named before any command and preserve all bytes. Also cover arrays, other non-string values, undeclared identity members, invalid `userID` and malformed retained structures; canonical string-only identities pass. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_planted_claude_env_file_contents` | Red on c0f50fa1, green after: a pre-existing forwarded `CLAUDE_ENV_FILE` contains a planted command marker and exports restoring refused environment variables. Refuse with the variable and file named before any hook/worker command runs, without sourcing the file; assert unchanged bytes, no migration/regeneration/trust/spawn and absent command markers. In this one fixture retain absent, empty and same-start launcher-generated positive controls with recorded SHA256, and show that a prior-start digest cannot authorize foreign contents. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_aws_credential_chain_selectors` | Red on c0f50fa1: the four reported selectors select a synthetic worker-owned AWS configuration containing `credential_process`; preparation refuses without running or trusting it. Test settings and launch inputs. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_foreign_repository_root` | Red on c0f50fa1: another repository with main-local payload refuses with this task's name before any side effect, for both kinds and all worker routes; the validated anchor/control passes. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_object_plugin_command_components` | Red on c0f50fa1: object `source` mappings and inline `content`, including dynamic Markdown, refuse even with the plugin disabled. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_unknown_settings_keys` | One fixture per settings source, unknown top-level and nested keys, including a harmless-looking future key; candidate data cannot extend the allowlist. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_refuses_undeclared_provider_selectors` | Every prohibited name family, settings/launch placement, exact fixed-value AWS exception, unknown ordinary environment names and noncanonical declared values. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_start_requires_string_component_references` | Scalar file control; object, list, directory, missing file, outside-root reference and unreadable component negatives. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_noncommand_hook_handlers_are_refused_before_launch` | Command-free HTTP separately in S01-S07 on both platforms; other documented/unknown/missing/malformed types; other hook-bearing sources; exact indexed refusal. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_managed_skills_use_actual_managed_root` | Red on c0f50fa1: using the same temporary managed-root fixture as S05/S06 for both Darwin and Linux, plant a Markdown skill at `<managed-root>/.claude/skills/<name>/SKILL.md` and a bundled plugin payload at `<managed-root>/.claude/skills/<name>/.claude-plugin/plugin.json` with hooks; metadata-only control produces explicit disable. |
| `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_project_sandbox_extensions_are_refused_before_launch` | Red on c0f50fa1: `excludedCommands: ["*"]`, `filesystem.allowWrite: ["/"]`, extra sockets and nested unknowns in project/local scopes; canonical administrative controls remain accepted. |
| `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_creates_managed_parent_in_printed_commands` | Red on c0f50fa1: missing parent, both platforms, quoting, mkdir-before-install, staged JSON and absent executed-sudo marker. |
| `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_update_reconciles_settings_after_herdr_install` | Red on c0f50fa1: fake Herdr installer re-appends its literal hook, then update reconciliation restores one guarded entry; repeated update preserves custom hooks and produces no managed drift. |

The five allowlist classes each have an explicit fixture: unknown key, undeclared provider selector, foreign root, object-form component and non-command handler. Parameterization may share builders but must name every subcase in validation. Do not replace the three required c0f50fa1-red regressions with tests of a new validator alone.

Retain all a02 regressions: old tracked settings, alternate executable fields, inherited project MCP, dedicated global state, skills-directory plugins, per-source S01-S23 coverage, sandbox-only documentation, hostile-GH_HOST templates, private caches, native denials, migration and guarded delivery. The fixture-case source inventory equals the production source inventory; each case plants its payload in the source it claims to exercise.

Retain a02's red/green evidence for `env.HOME`, fenced dynamic commands and the four 79ea98a3 fixes as historical evidence. Do not claim those tests newly fail on c0f50fa1. Update the documentation template test to read the a03 task copy. Update inherited S11 sentinel-preservation/unknown-field-refusal expectations to the discard-and-regenerate contract with `projects: {}`; retain the top-level MCP tamper refusal, and do not keep the old blanket `oauthAccount` refusal or project-entry refusals.

C11: every `closed` row names one exact `tests/<path>::<Class>::<test>` selector present at acceptance. Its fixture establishes that row's stated closure. Same-UID races, later reloads, live enforcement and transferred binding remain residuals.

## Change budget

Changed lines mean additions plus deletions. The starting measurement is `git diff --numstat 51ba5801 c0f50fa1`, not the obsolete a01 estimate. Preserve its complete output and account separately for base-branch changes already merged into c0f50fa1.

For this task's allowed paths, excluding `.orchestration/`, tests and the three regenerated Claude settings templates, that command measures:

| Source | Changed lines |
| --- | ---: |
| `.claude/settings.json` | 96 |
| `.gitignore` | 1 |
| `Makefile` | 6 |
| `home/dot_agents/agent-config.yaml` | 60 |
| `home/dot_agents/skills/agmsg-orchestration/SKILL.md` | 10 |
| `home/dot_claude-worker/modify_private_settings.json` | 437 |
| `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` | 65 |
| `home/dot_claude/modify_private_settings.json` | 120 |
| `home/dot_local/bin/common/executable_herdr-agents` | 126 |
| `scripts/generate-agent-configs.py` | 181 |
| `scripts/validate-agent-assets.py` | 9 |
| **Measured starting source total** | **1111** |

The seven allowed test modules measure respectively 103, 15, 206, 935, 104, 310 and 95 changed lines in `allowed_files` order: **1768**. The full historical-base output additionally contains already-merged unrelated source/test rows; list them rather than charging them as new a03 work or editing them.

Amendment 1's read-only sizing counts 24 lines in c0f50fa1's `present`/`read_json`/`write` analogues plus 16 estimated declaration/digest/route lines, and the 42-line non-command-handler fixture plus 18 estimated content/control lines: **40 source / 60 test**. This measured analogue-based estimate is not a measured implementation result.

Amendment 2's read-only AST sizing of c0f50fa1 measures `present` 8 + `read_json` 10 + `write` 6 = 24 source analogue lines, plus 56 estimated declaration/project/identity/regeneration lines: **80 source**; the global-state fixture 20 + refusal helper 36 = 56 test analogue lines, plus 64 estimated generation/identity/restart subcases: **120 test**. These are sizing analogues reused without duplication, not measured implementation results. Amendment 3 retains the **80 source** ceiling, removes project-inventory work and replaces the restart subcases with the A-then-B shared-directory sequence: the same 56 test analogue lines plus 104 estimated generation/identity/sequential-start subcase lines give **160 test**, an additional **40 test** over amendment 2. This revised estimate is not a measured implementation result.

Authorize these incremental ceilings, attributed to accepted findings. These increments are estimates pending implementation measurement, not claimed measured results:

| Control/finding | Additional source | Additional tests |
| --- | ---: | ---: |
| Closed settings/nested-value schema and sandbox extensions; S1, `local:c0f50fa:2` | 180 | 140 |
| Environment/provider allowlist and credential-chain refusal; `security:c0f50fa:1` | 70 | 100 |
| Validated repository root; `security:c0f50fa:2` | 25 | 60 |
| Scalar inspected-file components; `security:c0f50fa:3` | 35 | 70 |
| Actual enterprise skills root; `local:c0f50fa:1`, `text-security:be969e3:1` | 10 | 40 |
| Handler-class/schema consistency; `text-security:b2a186e:1` | 10 | 30 |
| Printed privileged parent creation; `local:c0f50fa:3` | 10 | 25 |
| Post-Herdr reconciliation; `local:c0f50fa:4` | 10 | 45 |
| Existing render/docs fixture alignment with the accepted re-plan | 10 | 30 |
| Executable environment-file contents and launcher-written SHA256; `text-security:f7af699:1` | 40 | 60 |
| Launcher-generated S11, screened identity and empty shared project state; D-024-34/D-024-35, `worker:5067ed0:1` and `text-security:efa211d:1` with `text-security:f7af699:1` as the shared family | 80 | 160 |
| **Increment ceiling** | **480** | **760** |

The source cap is **1591 = 1111 + 480**; the test cap is **2528 = 1768 + 760**, including amendment 3's revised S11 ceiling of **80 source / 160 test** (amendment 2's **80 / 120** plus **0 / 40**). Count shared controls once. Retained code is not a new increment, and generated-template exclusions do not exempt preparation or merge scripts.

RESULT records final per-file numstat, historical-base and final PR merge-base identities, actual source/test totals and per-control attribution. Preserve both the complete historical comparison and the current PR comparison so merged base changes are visible.

Every later amendment maps to accepted review findings and carries `previous_sha256`; the worker raises no cap. Amend Change budget, both operative Check cap sentences and the Checks block together. A measured overrun produces a blocked PONG rather than suppression or an unreviewed text edit.

## Out of scope

D-024-26 still assigns exact host-probed uv/Python/Node declarations, mise pins, bound isolated PermissionRequest, structural validation/migrations, binary-identity deployment checks, real-uv/planted-startup execution, complete descendant binding, formatter PATH repair and any replacement state helper to `dotfiles-T133-trusted-entrypoint-binding-a01`. Its prerequisite becomes this reset successor by orchestrator amendment; this worker edits no owner task.

Keep `home/dot_mise/config.toml`, the installed state-helper source, Codex boundary sources and updater scripts outside scope. No binding-only code returns through shared files. Add no write-boundary Python hook, gh wrapper, credential-directory substitute, installation discovery or PATH fallback.

P1-14 a05 and P1-6 own approval/evidence consumption. The exact operative ledger templates tested from this task copy are `gh api --hostname github.com repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha` and `gh api --hostname github.com 'repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref=<sha40>'`. Validate the returned full 40-hex SHA and use the identical SHA in the content request. Every deciding API call binds `--hostname github.com`; every deciding subcommand binds `--repo github.com/mryfmo/dotfiles`. Refuse if the host cannot be bound, without an unbound retry or local fallback.

Retain `tests/unit/test_agmsg_orchestration_docs.py::AgmsgOrchestrationSkillTest::test_deferred_ledger_calls_bind_github_host_under_hostile_gh_host`: extract those two templates, substitute only the validated SHA, exercise argv without shell evaluation, export hostile `GH_HOST`, check exact hostname/repository/SHA binding and test an isolated no-gh refusal. This is a contract test, not a ledger consumer or authentication test. Local remotes, URL rewrites, refs, objects and working-copy rows establish no approval authority.

The host is not a security boundary between same-UID seats. `GH_CONFIG_DIR` does not separate macOS Keychain credentials. Native merge denials remain `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)`, `Bash(gh api graphql:*)`; shared credentials permit other API routes. P1-11 owns next-records-PR detection, not main-push detection or prevention. Separate-user/host prevention remains the operator's future P1-16 decision.

`dotfiles-T133-agmsg-hardening-a01` owns store driver-name validation and plugin authorization. Shared administrative exceptions/socket access, external host processes, same-UID races, later configuration reloads and hook-event limitations remain residuals. Dedicated login state is not imported from the orchestrator or used to discover executable acceptance rules.

Perform no live settings application, authentication/keyring/ruleset mutation, global/administrative installation, permission-policy deployment, restart or merge. Edit no canonical task, acceptance record, decision ledger, design or another task's evidence.

## Check

`make render-check` and `make validate-agent-assets` pass. Run repository formatting/lint on changed files, including shellcheck/shfmt on the launcher and rendered guard; shell comments use English shdoc-compatible annotations.

Run `uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` and `uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs -v` inside the worker sandbox with its private cache. Preserve complete outputs, statuses and tested identities.

The final diff has at most 1591 changed lines outside `tests/` and `.orchestration/`, excluding regenerated `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`.

The final diff has at most 2528 changed lines under `tests/`.

Measure the current PR diff against its authenticated merge-base; preserve the historical-base measurement and reconciliation described in Change budget. No unrelated base change becomes an authorized edit.

Validation includes amendment 3's four c0f50fa1-red/after-green S11 fixtures, including sequential A-then-B starts on the shared configuration directory, the three c0f50fa1-red security regressions, all four local-review regressions, every allowlist class, complete S01-S23 case coverage and final green module output. Malformed/unknown retained nested inputs, disabled plugin payloads and shadowed files refuse before mutation; S11 discarded fields are never forwarded. Positive controls retain default seating, canonical delivery, attachment, repeated preparation and ordinary worktree writes.

Both platform renders retain the exact static deny inventory, directory/descendant coverage, narrow writable stores, private caches, MCP/plugin disables and administrative policy. Sandbox-extension fixtures prove startup refusal, rather than merely showing unchanged administrative JSON.

Printed-installation evidence includes parent creation before file installation on both platforms with no privileged execution. Fake-update evidence covers Herdr's literal append followed by reconciliation and a second idempotent update.

Retain existing guard, descendant system-PATH/BASH_ENV, migration, custom-hook, native-denial and cache tests. Record the installed Claude version, actual source read sets, documentation observations and any unsupported-version/source refusal without logging credentials. A version mismatch is a blocked PONG requiring re-tasking.

Retain the inherited formatting reproduction at historical base `205fe85c` for the 12 out-of-scope shell files; do not repair them here. Run no local Bats tests. Required Bats results and all required checks come from GitHub Actions before RESULT.

The orchestrator runs the task-consistency checker before dispatch and acceptance against this complete a03 file, using the trusted parent/interpreter/cache contract. C1-C10 and C7b pass, including both C3 task-copy rows; check C11 selectors individually. A separate C-80 security-profile context reviews this reset text before dispatch. These are prerequisites, not results claimed by this draft.

## Artifacts, completion and deployment

On the first a03 push, delete `.orchestration/dotfiles-T133-worker-write-boundary-a02/task.md` and add `.orchestration/dotfiles-T133-worker-write-boundary-a03/task.md` byte-identical to the dispatched text. This C3 deletion is the sole authorized predecessor-path exception. Keep all other a01/a02 artifacts and implementation history.

Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, operator steps, budget attribution and worker review evidence under the a03 artifact directory. Evidence lives in the worker's own worktree; RESULT says so. Use the `-worker-` review-evidence infix. Record durable decisions/failures with CompactionDB markers; the orchestrator owns main-checkout consolidation.

Continue PR #431 on the existing branch from the specified head. Discard no unrelated work. The orchestrator owns base updates and dependent `after:` changes; this task retains `after: []`. Every moved final head receives fresh required evidence.

Every worker command completes inside its sandbox and allowlist. Each gh/git write is an individual command without shell chaining. A boundary failure produces the exact blocked PONG; no permission-gate, tool or shell alternative bypasses it. Do not clear shared Git metadata outside the worker boundary.

Allow at most one independent pre-push review and two total correction rounds, including that review's corrections. Preserve a01/a02 counters separately. Surviving P0/P1 findings are `open:<id>` or `open:review-<review id>` in RESULT and stop integration for the operator's decision; do not start a private third round.

Post no `@codex review` comment. Observe automatic final-head reviews within the bounded 15-minute window and record absence as `bot: none`. Required GitHub Actions pass before RESULT. Propose a disposition for every feedback item; the worker resolves no review thread and grants no acceptance.

Follow repository agent-side Crit-data/receipt rules without a browser or human review request. Record resolved evidence, including a justified review-scope approval when finding-free; never use `AGENT_REVIEWED=1` without reading the evidence. Report any Plan Mode server for orchestrator cleanup.

RESULT names final full head/base/branch, PR, changed files, task-copy SHA256, exact selectors, red/green identities, final numstat/attribution, schema/source/handler/root inventories, installed-version observations, inherited binding-removal inventory, scripts/installed paths, settings destinations, printed installation commands, feedback/dispositions, open findings, counters and all evidence paths. Distinguish historical claims from new final-head results.

Report user-visible changes: this repository's workers alone are supported; unknown settings or environment inputs refuse; every start regenerates global state with `projects: {}`, preserves only screened identity and resets native counters/caches/project history/allowedTools; workspace trust uses the launcher's existing spawn-readiness dialog acceptance; alternate providers/authentication selectors refuse; object/inline components refuse; lower-scope sandbox extensions refuse; actual enterprise skills are inspected. Refusal preserves original bytes and names the source without exposing values.

Retain user-visible effects of dedicated worker login, static denies also affecting Bash writes, writable agmsg stores except trusted-plugin authorization, private caches, no worker sandbox escape, shared administrative exceptions/socket access, guarded project hooks and unchanged legacy orchestrator PermissionRequest. Formatter availability and complete executable binding remain deferred.

The orchestrator obtains separate local review, task-level audit and security-profile review of the final implementation head. Final feedback collection, dispositions, acceptance and integration follow Orchestrator Playbook step 10 in order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the review receipt; merge is pinned to the reviewed final head. The worker writes no approval row.

Operator deployment remains post-merge and coupled to the approved P1-14 a05 change under D-024-31: `make update`, then `make install-managed-settings`, inspect staged content, then execute the printed privileged parent-creation and platform-specific file-installation commands. Record administrative installation separately from chezmoi application.

The operator logs in with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`, applies the separately prepared deterministic Codex permgate escape-denial change and restarts affected sessions. Inspect installed administrative content, dedicated directory, static denies, stores/caches, all startup sources, closed-schema refusals, MCP/plugin disables, PermissionRequest exception and sandbox startup. Check lower-scope conflicting arrays and report shared capabilities without exposing credentials.

Merge alone establishes no deployment readiness. Record application, administrative installation, login, startup checks and the Codex permgate change before releasing live dependents; mechanisms requiring executable binding also wait for that owner.

## Checks (pasted by the orchestrator before each send)

Amendment-3 operative caps are **1591 source / 2528 tests**, increments **480 / 760** including this control's **80 / 160**; amendment 3 adds **0 source / 40 tests** to amendment 2. C-99 cap statements updated: Change budget, both Check limits and this Checks statement. The fenced send-1 paste below is reproduced verbatim as historical evidence, including its superseded caps/counts; the orchestrator re-pastes current checker/C11/security/counter results and these limits before send 2. C-80 round 3 found the accepted P2 `text-security:efa211d:1`; round 4, the first after D-024-35's new re-plan line under C-92, found the accepted P1 `text-security:be969e3:1`, addressed by amendment 4's enterprise-root correction with no cap change. Amendment-4 validation is pending; no passing result is claimed here.

```
a03 reset text for a010 (Codex, worker-e); plan 024 P1-15; PR #431; branch tools/worker-write-boundary-a01; start c0f50fa1383416240ad28959dbc4635afa777175; reset_of a02; security true; after []
a02 dispatched/task-copy SHA256 ae1088a7fdef88152f6829c18440f9a4616b07dd4bde6381ed0f120d1b06be50; a01 worker rounds 2 spent; a02 worker rounds 2 spent; C-61 prohibits another a02 round
history: 2ae9e2c incorrect; ebbb71b incorrect -> S1 documented-source re-plan; b2a186e incorrect; ac9ce14 correct; pre-push HOME/fenced-command fixes retained; 79ea98a3 four local fixes retained; c0f50fa1 security 2 P1 + 1 P2; local review four unique findings; no c0f50fa1 task-level audit
approach: closed settings/environment/source/root/value schema; 2026-10-20 residual-list entry; D-024-29 design freeze; D-024-30 design by reference; D-024-26 binding transfer retained; D-024-31 deployment coupling retained
measured starting task-owned source 1111 / tests 1768 from git diff --numstat 51ba5801 c0f50fa1; incremental ceilings 400 / 600 (amendment 1 adds 40 / 60 for executable environment-file contents); operative caps 1511 / 2368; final RESULT must contain measured per-file and per-control totals
pasted 2026-10-20T03:55Z before send 1: task-consistency-check.py: `dotfiles-T133-worker-write-boundary-a03.md: OK`; C11: 6 closed rows, 0 without a `tests/<path>.py::<Class>::<test>` selector; validate-agent-assets.py SECRET_PATTERN: 0 matches; literal home paths: 0; complete text 622 lines before this paste
C-80: f7af699 incorrect (1 P1: CLAUDE_ENV_FILE contents unbound -> amendment 1, text-security:f7af699:1 input-inventory); 9bd6198 correct (`Verdict: correct`, 86 threat rows and 22 allowed-file entries checked); budget 2 of 3 used
acceptance counters (scripts/regime-counters.sh, 03:54Z): tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none; worker_fix_rounds 0; independent pre-push reviews 0
task SHA256: in the AGMSG-TASK line, computed over these final bytes; delivery read marker: this message's messages.db read_at, recorded in the acceptance record; later amendments require an accepted finding mapping and previous_sha256
```

Not performed by the worker: local Bats, live enforcement, administrative installation, login, permission-policy deployment or session restarts.