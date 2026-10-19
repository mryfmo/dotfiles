---
format: 2
task_id: dotfiles-T133-worker-write-boundary-a01
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
  - .orchestration/dotfiles-T133-worker-write-boundary-a01/**
after: []
threat_table:
  - control: home/dot_agents/agent-config.yaml
    disposition: "residual: the manifest separates worker policy and enumerates protected executable inputs statically; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy and tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest check both platforms without establishing same-UID isolation or executable binding."
  - control: home/.chezmoitemplates/claude-settings-managed.json
    disposition: "residual: the orchestrator baseline adds startup failure, hook failure policy and sanitized non-PermissionRequest commands while retaining the legacy PermissionRequest command; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy checks the retained policy, and dotfiles-T133-trusted-entrypoint-binding-a01 owns the unbound PermissionRequest execution."
  - control: home/.chezmoitemplates/claude-worker-settings.json
    disposition: "residual: dedicated settings provide static trusted-path and worktree-configuration denies, restricted writes, minimal delivery hooks and native merge denials; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_policy_renders_for_both_platforms checks the user baseline separately from shared managed capabilities."
  - control: home/.chezmoitemplates/claude-managed-settings.json
    disposition: "residual: operator installation establishes the documented administrative sandbox scope; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox checks its content without claiming live enforcement or per-seat removal of shared exclusions and socket access."
  - control: home/dot_claude/modify_private_settings.json
    disposition: "residual: classification follows the managed non-PermissionRequest prefix and guard forms so upgrades replace stale managed hooks without consuming custom hooks; tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_prefixed_guarded_managed_hooks_replace_legacy_hooks_idempotently checks migration and repeated merging while PermissionRequest retains its existing classification."
  - control: home/dot_claude-worker/modify_private_settings.json
    disposition: "residual: the separate renderer replaces stale worker-managed policy without importing orchestrator hooks or credentials; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently checks temporary-HOME deployment."
  - control: home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl
    disposition: "residual: the rendered guard checks canonical launch identity and fixed operation selection before project payload execution; tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads checks worker suppression and anchored fixture execution, while complete executable and formatter-tool binding belongs to dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: .claude/settings.json
    disposition: "residual: portable guarded commands and explicit clean-environment re-exports reduce worker-triggered project-hook execution; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure traverses every tracked entry without establishing complete descendant binding."
  - control: scripts/generate-agent-configs.py
    disposition: "residual: deterministic generation uses the static manifest inventory and emits separate user and administrative policies without consulting Git objects or discovering executable installations; tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest checks correspondence and filesystem coverage."
  - control: scripts/validate-agent-assets.py
    disposition: "residual: the exclusion validator requires the same exact three-entry list on both platforms and preserves the existing legacy PermissionRequest check; tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form covers exclusion failures while structural bound-hook validation remains owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: Makefile
    disposition: "residual: the installation target stages administrative settings and prints the platform-specific sudo command without executing it; tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo checks both destinations and the absence of privileged execution."
  - control: home/dot_local/bin/common/executable_herdr-agents
    disposition: "residual: preparation supplies dedicated settings and private caches on every launch route and migrates legacy local delivery hooks; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches and tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks check actual launch construction and stale-hook removal."
  - control: home/dot_agents/skills/agmsg-orchestration/SKILL.md
    disposition: "residual: the governing sentence removes procedural authorization for worker sandbox escapes; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox checks the replacement without representing shared managed capabilities as per-seat isolation."
  - control: .gitignore
    disposition: "residual: ignoring .uv-cache reduces accidental publication of worker cache contents; tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored checks the pattern in a temporary checkout."
  - control: tests/unit/test_generate_agent_configs.py
    disposition: "residual: platform, static-inventory and guarded-command fixtures verify generated configuration and retain the existing literal PermissionRequest expectations without claiming live permission enforcement or bound executable identity."
  - control: tests/unit/test_validate_agent_assets.py
    disposition: "residual: exclusion cases and the corrected valid_claude_sandbox fixture exercise the retained policy checks while the existing PermissionRequest and hook-composition fixtures continue to use the legacy managed command."
  - control: tests/unit/test_claude_settings_merge.py
    disposition: "residual: migration fixtures cover prefixed and guarded managed SessionStart and PostToolUse commands, stale-ccgate removal, custom-hook preservation and idempotence without introducing bound PermissionRequest forms or native-binding expansion."
  - control: tests/unit/test_herdr_agents.py
    disposition: "residual: fake launchers and subprocess markers check every launch route, legacy migration, hook placement, sanitized delivery environments, caches and native denials without starting live seats or verifying the removed binding family."
  - control: tests/unit/test_agmsg_orchestration_docs.py
    disposition: "residual: only the assertion of the Worker Playbook step 4 sentence follows its replacement, and the complete module remains green on the rebased final head."
  - control: tests/unit/test_claude_worker_settings.py
    disposition: "residual: fixtures check dedicated settings, protected policy bytes, narrow inventory, ordinary worktree writes and guard behavior without executing a bound PermissionRequest hook or claiming live Claude enforcement."
  - control: tests/unit/test_claude_managed_settings.py
    disposition: "residual: fixtures check administrative policy content, conflicting lower-scope settings and nonprivileged staging while real-uv hook execution and binary-identity deployment checks remain owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: .orchestration/dotfiles-T133-worker-write-boundary-a01/**
    disposition: "residual: branch artifacts distinguish historical observations, retained final-head results, removed binding work and pending operator deployment, and acceptance compares their claims with the final diff and CI."
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
    disposition: "residual: the next push replaces the previous task copy with the complete byte-identical dispatched narrowing text, and TASK and RESULT identify that copy by SHA256."
  - control: evidence records
    disposition: "residual: report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence retain commands, statuses and tested identities without credentials or literal operator home paths."
  - control: task metadata
    disposition: "residual: the orchestrator checks C1 to C10 and C7b, dispatched bytes and final-head PR_FEEDBACK_EVIDENCE, AUDIT_EVIDENCE, ACCEPTANCE_EVIDENCE and REVIEW_EVIDENCE without treating local proposals as approval authority."
  - control: metadata separators
    disposition: "residual: the opening separators delimit format-2 metadata, and the task-copy SHA256 binds the complete front matter and body."
  - control: in-process effects
    disposition: "residual: generation and tests operate on repository files and temporary fixtures, and the worker performs no live deployment, login, administrative installation, permission-policy mutation or operator-session restart."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: non-PermissionRequest hook commands receive the prescribed clean prefix and delivery PATH, while the legacy PermissionRequest, complete interpreter binding and deployment-check execution remain owned by dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: new or renamed scripts
    disposition: "residual: the worker settings modify script and rendered orchestrator guard have named source and installed paths, and this task adds no state-helper replacement, private executable-link manager, write-boundary hook or gh wrapper."
  - control: "5.14 item 0: host threat model"
    disposition: "residual: host controls reduce accidental and injected damage without separating same-UID seats, and P1-11 owns next-records-PR detection while separate-user or separate-host prevention remains the operator's future P1-16 decision."
  - control: "5.14 item 1: worker write controls"
    disposition: "residual: dedicated settings, static input-derived denies, restricted writes, legacy-hook migration and administrative sandbox policy reduce damage without establishing atomic protection against path-consumption races."
  - control: "5.14 item 2: sanitized environment and executable selection"
    disposition: "residual: the clean prefix applies to every command hook rendered by this task except the unchanged managed PermissionRequest, and dotfiles-T133-trusted-entrypoint-binding-a01 owns that exception, exact interpreter selection and complete trusted-entrypoint binding."
  - control: "5.14 item 3: trusted-path checks"
    disposition: "residual: guard fixtures check canonical launch and input identities including symlink and case aliases, while executable realpath binding belongs to dotfiles-T133-trusted-entrypoint-binding-a01 and other consuming helpers retain their own hardening owners."
  - control: "5.14 item 4: verified executable and consumed-byte identity"
    disposition: "residual: fixed guard operations avoid worker-selected project payloads, while executable identity belongs to dotfiles-T133-trusted-entrypoint-binding-a01 and snapshots and last-use digests remain with the consuming hardening tasks."
  - control: "5.14 item 5: output and reservation identity"
    disposition: "residual: this task introduces no reservation protocol, and full-head output names, fixed-inode locks and physical-slot identity remain with the orchestrator mechanisms that create them."
  - control: "5.14 item 6: honest residuals"
    disposition: "residual: the text retains same-UID, shared credential, managed exception, Herdr socket, agmsg sourcing, path-race and hook-event limitations and assigns executable-binding gaps to dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: "5.14 item 7: verification"
    disposition: "residual: retained render, merge, policy, guard, launch and cache tests provide final-head evidence, while real-uv hook execution belongs to dotfiles-T133-trusted-entrypoint-binding-a01 and the common trusted_exec_contract helper belongs to P1-6."
  - control: "5.14 item 8: committed approval ledger"
    disposition: "residual: P1-14 a05 implements SHA-bound GitHub API approval reads, and this task provides no authority from local files, refs or objects and no prevention of shared-credential API merges."
  - control: "5.14 item 9: private caches and isolated interpreters"
    disposition: "residual: private worker caches and explicit orchestrator-cache denies remain here, while exact uv/Python declarations, interpreter isolation, trusted resolver consumption and bound deployment checks belong to dotfiles-T133-trusted-entrypoint-binding-a01."
  - control: "5.14 item 10: commands inside the sandbox"
    disposition: "residual: empty worker user exclusions and the governing execution rule remove worker authorization to escape, while shared managed capabilities remain available and Codex network configuration and deterministic permgate deployment retain their separate owners."
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
      D-024-26 narrows P1-15 after the fourth executable-binding finding;
      amendment 8 is not the implementation contract for this dispatch.
      The acceptance record retains the class correction, re-plan line and
      complete review history.
    sources:
      - .orchestration/decisions.tsv
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-5204254.md.last.md
  - claim: >-
      Design section 5.14 is uncommitted main-checkout context. The worker
      reads the HOME-relative source named below, and the verbatim quotations
      in this task bind the relied-on sentences without a literal operator
      home path in tracked text.
    sources:
      - $HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      The worker's latest measured local snapshot is 7c3a6394 on main
      69dccca9, with 876 source and 1299 test changed lines under the former
      888 and 1335 caps; no implementation push has occurred.
    sources:
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
  - claim: >-
      The managed template currently renders the PermissionRequest command
      as ~/.local/bin/common/permgate claude, and the existing validator
      recognizes that legacy form; D-024-26 preserves it for this task.
    sources:
      - home/.chezmoitemplates/claude-settings-managed.json
      - home/dot_claude/modify_private_settings.json
      - scripts/validate-agent-assets.py
      - .orchestration/decisions.tsv
  - claim: >-
      Linked-worktree sessions load main-checkout local settings and can
      retain legacy worktree-local delivery hooks; worker user settings,
      main-local guarding and legacy migration must therefore be checked
      together.
    sources:
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
      - .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-f589c7c.md.last.md
      - home/dot_local/bin/common/executable_herdr-agents
  - claim: >-
      Same-macOS-user gh Keychain access is not separated by a configuration
      directory, and administrative settings and shared capabilities do not
      establish adversarial isolation between seats sharing one OS user.
    sources:
      - .orchestration/decisions.tsv
      - .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md
---

# AGMSG-TASK dotfiles-T133-worker-write-boundary-a01 — D-024-26 re-plan; plan 024 P1-15; seat a010

## Goal

Ship the worker write boundary alone. This complete text replaces amendment 8; it is a re-plan under D-024-26, not a ninth incremental amendment.

Continue the existing implementation branch `tools/worker-write-boundary-a01` in `$HOME/Workspace/dotfiles/.claude/worktrees/worker-e`, retaining the work that belongs to the narrowed scope. The latest local snapshot is `7c3a6394` on main `69dccca9`, with no push. The worker replaces its task copy with the byte-identical text dispatched after this re-plan passes its checks.

Retain the dedicated `CLAUDE_CONFIG_DIR`, static trusted-path deny inventory enumerated from executable inputs, private caches, managed sandbox policy, legacy worktree-local hook migration, native merge denials, platform-symmetric exclusions and their validator fixtures, guarded project hooks, and the orchestrator modify script's classification of its managed hooks.

Every command hook this task renders starts with the prescribed `/usr/bin/env -i …` prefix except the managed PermissionRequest hook. Its command remains exactly `~/.local/bin/common/permgate claude`, as the current managed template renders it, behind the managed deny rules until `dotfiles-T133-trusted-entrypoint-binding-a01` lands. Do not put that legacy command behind the system-only PATH prefix: its unchanged shebang requires uv discovery.

The bound PermissionRequest form, its structural validator, exact uv/Python declarations and mise pins, binary-identity deployment checker, real-uv hook execution test and formatter PATH changes leave this task. The worker reverts or leaves unmerged its amendment-6/amendment-7 implementation belonging to that family and names the removed files and portions in RESULT.

The host is not a security boundary between seats sharing one OS user. Host-local controls reduce accidental and injected damage. They do not prevent a malicious same-UID process from exploiting shared credentials, filesystem races, host processes or shared control-plane capabilities.

The GitHub boundary is detection, not prevention. P1-11 owns the next-records-PR check that every main merge since the previous boundary has acceptance and gate-passage evidence. Records do not reach main until that boundary PR, so this text makes no main-push detection claim. Separate-user or separate-host prevention remains the operator's future P1-16 decision under D-024-23.

D-024-20 retains P1-15 as the write-boundary prerequisite of P1-14 a05, P1-10 a02, audit-pool-a02 and P1-6. The orchestrator owns their `after:` fields. This task has `after: []`. Satisfying this write-boundary prerequisite does not establish the executable-binding contract deferred by D-024-26.

## Design contract and review history

Read `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 items 0 through 10 as main-checkout context. This is the only form in which that design path appears in this task.

C-88: the following relied-on sentences are quoted verbatim. D-024-26 assigns the quoted executable-binding requirements to the binding task; quotation does not restore them to this task's implementation scope.

Item 0:

> ホスト内の制御（本節 1〜10）は事故と prompt injection による損害の抑制であり、文はそう書く。

Item 1:

> Claude worker 席は専用の設定ディレクトリ `CLAUDE_CONFIG_DIR=~/.claude-worker`（chezmoi が描画、operator が一度 login）で起動し、orchestrator の `~/.claude` と設定を共有しない。

> managed settings の配置先は OS で異なる（macOS `/Library/Application Support/ClaudeCode/managed-settings.json`、Linux `/etc/claude-code/managed-settings.json`）。

> hook は agmsg 配送だけを、hook コマンドを `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<home> …` で始めて（`BASH_ENV` などの継承環境を bash 起動前に消す；PATH 固定だけでは BASH_ENV が先に走る）絶対パスのインタプリタで呼び（上流の agmsg スクリプトは `/usr/bin/env bash` の shebang を持つので、hook 実行環境の PATH が shim を含まないことで束縛する）、各 hook に `onFailure: "block"`。

> `failIfUnavailable: true` を全席に置く。

> The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19).

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

Item 9:

> orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。

> `UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。

> One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19).

> Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19).

Item 10:

> worker 席の除外コマンドは空にし、gh も git push も sandbox 内の proxy 経由で実行する。

The acceptance record retains the entire findings history. Read every `.orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-*.md.last.md`, including the final amendment-8 review `5204254`; do not use an earlier `Verdict: correct` as approval of this text.

The executable-binding class combines `text-security:f810c30:1`, `text-security:772cde0:2`, `text-security:e5c055e:1` and the fourth binding finding `text-security:5204254:1`. The acceptance record's class correction and re-plan line remain authoritative history. The nonexistent uv layout and missing Node interpreter are assigned to the binding task, not described as fixed by this narrowing.

Retained responses to the earlier findings are the static input inventory, narrow denies around writable agmsg stores, worklog/cache protection, dedicated worker settings, administrative sandbox scope, explicit hook-variable re-exports, guarded main-local hooks, legacy worktree-local migration and honest same-UID and agmsg-sourcing residuals.

## Files

1. `home/dot_agents/agent-config.yaml` remains the source of agent policy and model profiles.

   Add the separate worker settings output `home/.chezmoitemplates/claude-worker-settings.json`, administrative output `home/.chezmoitemplates/claude-managed-settings.json`, worker directory `~/.claude-worker` and anchored primary checkout declaration. Keep existing model selections and Codex profile, sandbox, approval, network and shared-Git settings unchanged.

   Keep the static `trusted_paths:` inventory. It protects anchored-checkout source and control paths outside `.claude/worktrees/`, including tracked `.claude` contents, the main checkout's `.claude/settings.local.json`, `.orchestration`, scripts, tests, configuration and other current top-level source paths. Explicitly include both `<anchored-checkout>/.agents/worklog/**` and `<anchored-checkout>/.agents/worklog/uv-cache/**`, with directory targets where needed.

   Do not deny the checkout parent or all of `.claude/worktrees/`. Separately protect the directory target and descendants of `//<anchored-checkout>/.claude/worktrees/*/.claude/**` and the file `//<anchored-checkout>/.claude/worktrees/*/.mcp.json`. Ordinary worktree source writes and per-seat caches remain available.

   Enumerate protected inputs of trusted executables, including these home paths and their directory targets where applicable:

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

   The user-site entries cover `.pth`, `usercustomize.py` and `sitecustomize.py`. Account for other user-site or startup-hook locations of interpreters currently used by the retained hooks through an explicit inventory entry or an existing protected installation/configuration path. This inventory work does not introduce exact interpreter declarations or claim isolated startup.

   Protect application code consumed by installed wrappers, including code beneath `~/.local/share/**`; protecting only the wrapper executable is insufficient. Explicitly name the permgate policy and rendered guard even where another pattern overlaps them.

   Do not replace the inventory with a blanket `~/.agents/**` or `~/.local/**` deny. The agmsg stores `~/.agents/skills/agmsg/db`, `teams`, `run` and `ext-tools` remain writable, including ordinary descendants, except `db/trusted-plugins`. Plugin code remains denied. Read/Edit denies also affect Bash sandbox writes.

   Worker user policy enables sandboxing, sets `failIfUnavailable: true` and `allowUnsandboxedCommands: false`, supplies no excluded commands or Herdr socket allowance, and limits additional write allowances to the agmsg stores and private seat caches. The project root provides ordinary worktree writes. Do not copy shared uv or mise write allowances into worker settings.

   The orchestrator user policy retains its existing permissions and cache allowances, receives `failIfUnavailable: true`, and uses the same three control-plane exclusions on both platforms. Remove the former Linux `gh *` exclusion.

   Remove the amendment-6/amendment-7 uv/Python binding declarations and formatter-tool declarations from this PR. Do not add exact versions, installation-layout assumptions, private executable links or tool-discovery fallbacks.

2. `scripts/generate-agent-configs.py` renders distinct orchestrator user, worker user and administrative settings from the manifest.

   Render deny rules from the static inventory, using absolute `//` anchored-checkout patterns and the listed home forms. Perform no Git tree, index, ref or object traversal to choose protected paths. Do not use `git ls-tree` or `git ls-files` as inventory authority.

   Generation is independent of deployment executable availability. Remove binding-only native `{{ output ... }}` expressions, executable discovery and installation probes from the narrowed outputs. Ordinary trusted home, source, platform and anchor substitutions remain sufficient for this task's templates.

   Add or retain `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_policy_is_separate_from_orchestrator_policy`.

   Add or retain `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_worker_deny_inventory_is_static_and_matches_manifest`. It checks exact manifest-to-render correspondence on Darwin and Linux, directory targets and descendants, current source-path coverage by filesystem enumeration under fixed roots, worklog/cache protection, the explicit policy and guard entries, user-site startup-file fixtures and ordinary worktree writes. Git-controlled enumeration and planted Git environment or replacement refs must not change the output.

   Include anchors and homes containing spaces. Cover tracked `.claude` children, main-local settings, worktree configuration, symlink components and filesystem case aliases. These fixtures check configured coverage and identity; they do not simulate proof of Claude's live permission enforcement.

   Retain `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_leave_agmsg_stores_writable`, including the plugin and `trusted-plugins` exceptions.

   Add `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_denies_protect_permgate_policy`. In a temporary HOME, match worker Edit and Write requests against the rendered protected policy rule, refuse the fixture write and assert unchanged policy bytes. Do not execute a bound PermissionRequest command or claim resistance to inherited policy-selection environment inputs.

3. `home/.chezmoitemplates/claude-settings-managed.json` remains the orchestrator user baseline.

   Its managed PermissionRequest command remains exactly:

   ```text
   ~/.local/bin/common/permgate claude
   ```

   Do not add an env prefix, guard selector, absolute uv/Python invocation or new command-form validator for this hook. Keep its existing timeout and add the task's common `onFailure: "block"` entry policy. The unchanged command's shebang, interpreter discovery and inherited environment are explicit residuals owned by the binding task.

   Every other command hook generated by this task starts with:

   ```text
   /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR="${CLAUDE_PROJECT_DIR}" CLAUDE_ENV_FILE="${CLAUDE_ENV_FILE}"
   ```

   Re-export HOME before an entrypoint path uses it, and preserve launch identity explicitly. Agmsg delivery commands additionally set `AGMSG_RESOLVE_PROJECT=0` and preserve `AGMSG_STORAGE_PATH` when supplied by the launcher.

   Project-sensitive orchestrator commands use the installed guard and fixed operation identifiers. Use existing payload scripts; do not introduce the repository-owned Herdr state-helper replacement. Do not add formatter-specific tool directories or private executable links.

   Retain `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_orchestrator_settings_keep_existing_policy`, accounting for the changed startup/failure policy, prefixes, guarding and exclusions. Do not claim that this test verifies formatter tools or PermissionRequest executable binding.

4. `home/dot_claude/modify_private_settings.json` stays in scope because its managed-hook classifiers and appended attachment hook consume the retained command changes.

   Keep `is_managed_permission_hook`'s existing legacy `permgate claude` recognition and stale `ccgate claude` migration. Add no bound PermissionRequest recognition or binding-upgrade migration.

   Update classification of managed SessionStart and PostToolUse hooks for the exact prefixed and guarded forms this task emits. Recognize owned guard paths, fixed operation identifiers and expected arguments, alongside the existing owned legacy forms. A foreign guard path, unrelated command, malformed prefix, extra operation or custom hook must not become managed merely because a token has a familiar basename.

   Preserve the existing quoted/escaped-tilde distinction for legacy PostToolUse commands. Preserve unrelated hooks, including custom hooks sharing an entry with a managed hook. Replace stale managed forms in place without duplication, retaining ordering and byte-identical repeated merge behavior.

   The attachment hook appended by `main()` also receives the clean prefix, installed guard route and `onFailure: "block"`. Account for it in effective merged-settings fixtures; it is not covered merely by inspecting the generated baseline.

   Add `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_prefixed_guarded_managed_hooks_replace_legacy_hooks_idempotently`, covering legacy-to-prefixed/guarded SessionStart and PostToolUse replacement, attachment handling, repeated merging, mixed custom entries and foreign-form rejection.

   Retain the existing stale-ccgate, SessionStart ordering, PostToolUse migration, quoted/escaped-tilde, unrelated-hook and mixed-entry preservation tests. No native-binding renderer or executable subprocess is added to template rendering.

5. `home/.chezmoitemplates/claude-worker-settings.json` is the dedicated worker baseline.

   Render the static trusted-path and worktree-configuration denies, native merge denials, empty user exclusions, disabled unsandboxed requests, restricted additional writes, no user Herdr socket allowance and `failIfUnavailable: true` on both platforms.

   Worker user hooks are limited to agmsg delivery. Do not import orchestrator formatter, project-map, PermissionRequest, attachment, Herdr state, plugins or credential files.

   Every worker command hook uses the clean prefix from item 3, followed by the absolute system shell and installed agmsg script path. Add `AGMSG_RESOLVE_PROJECT=0` and preserve launcher-supplied `AGMSG_STORAGE_PATH`. Every entry carries `onFailure: "block"`.

   Use the existing `/bin/bash` delivery invocation and fixed system PATH; do not introduce versioned interpreter declarations. Upstream env-bash descendants inherit the system-only PATH. Their store-selected sourced code remains the separately owned agmsg residual.

   Worker empty arrays do not subtract shared administrative exclusions or socket access.

6. `home/.chezmoitemplates/claude-managed-settings.json` supplies the separate administrative sandbox policy.

   Set `sandbox.enabled: true`, `sandbox.failIfUnavailable: true` and `sandbox.allowUnsandboxedCommands: false`.

   Set `sandbox.filesystem.disabled: false`, `sandbox.enableWeakerNestedSandbox: false`, `sandbox.enableWeakerNetworkIsolation: false`, `sandbox.network.allowAllUnixSockets: false`, `sandbox.network.allowLocalBinding: false` and `sandbox.allowAppleEvents: false`.

   Its ordered `sandbox.excludedCommands` list is exactly:

   ```text
   agmsg-dispatch *
   herdr-agents *
   <absolute-home>/.agents/skills/agmsg/scripts/actas-claim.sh *
   ```

   Its `sandbox.network.allowUnixSockets` list contains exactly the trusted home expansion of `~/.config/herdr/herdr.sock`.

   These administrative exceptions remain available to every Claude seat. Empty worker user lists cannot revoke them. The worker execution rule provides no authorization to use them outside the sandbox.

   Retain `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_rendered_policy_requires_admin_sandbox`.

   Retain `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_managed_render_is_independent_of_conflicting_project_and_local_settings`. Supply lower-scope attempts to disable sandboxing and startup failure, enable unsandboxed retries, add exclusions/sockets and weaken isolation or filesystem policy. Assert unchanged trusted administrative content without representing a fixture merger as live runtime enforcement.

7. `Makefile` adds only `install-managed-settings` and its `.PHONY` declaration.

   Render `home/.chezmoitemplates/claude-managed-settings.json` into the absolute home staging path `~/.claude/managed-settings.rendered.json`.

   Detect `/Library/Application Support/ClaudeCode/managed-settings.json` on macOS and `/etc/claude-code/managed-settings.json` on Linux, then print the exact ready-to-run operator command:

   ```text
   sudo install -m 0644 "<absolute-home>/.claude/managed-settings.rendered.json" "<detected-managed-settings-path>"
   ```

   Preserve shell quoting, including homes and destinations containing spaces. Execute no sudo command, live installation, authentication or restart.

   Retain `tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_install_target_stages_and_prints_without_running_sudo`, covering both platform destinations, staged JSON, exact printed command and an absent planted-sudo marker.

8. `home/dot_claude-worker/modify_private_settings.json` renders `~/.claude-worker/settings.json`.

   Follow the existing stdin/stdout chezmoi modify-script interface and standard-library baseline conventions. Replace stale worker-managed permissions, sandbox settings and hook arrays. Old exclusions, socket allowances, shared cache allowances and stale hooks must not accumulate.

   Do not read or copy the orchestrator's `~/.claude/settings.json`. Keep empty/malformed-input baseline behavior and idempotence. Perform no authentication or credential access.

   Retain `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_replace_stale_policy_idempotently` and `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_worker_settings_do_not_import_orchestrator_hooks`.

   Remove binding-only native rendering code from the worker renderer.

9. `home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl` installs `~/.claude/hooks/orchestrator-only.sh`.

   Keep the `.tmpl` suffix: chezmoi must render trusted home and anchored-checkout constants into the installed guard. Render fixtures exercise that source and its installed form; a plain executable source copied without expansion is insufficient.

   The guard compares canonical `CLAUDE_PROJECT_DIR` with the anchored primary checkout. Worker roots, sibling worktrees, unrelated checkouts and missing/unresolvable launch identity execute no payload and exit 0. Event cwd cannot change the launch-root decision. `CLAUDE_PROJECT_DIR` supplies identity, never an executable path.

   An anchored invocation selects a fixed owned operation and its anchored or installed payload path. Preserve argument boundaries, stdin and child status. Reject unknown operations; perform no eval or worker-relative script selection.

   Retain existing absolute system-interpreter conventions for the guard and fixed payload dispatch. Do not add exact uv/Python version declarations, a private executable-link directory, binary installation discovery or formatter PATH repair. Complete runtime executable identity remains the binding task's residual.

   For formatter and project-map operations, also check resolved tool-input paths. Inputs outside the canonical launch root or within a worker repository under `.claude/worktrees/` execute no formatter/map payload and consume no worker configuration. An anchored launch alone is insufficient.

   Retain `tests/unit/test_claude_worker_settings.py::ClaudeWorkerSettingsTest::test_project_guard_uses_launch_root_and_never_runs_worker_payloads`. Exercise complete prefixed invocations, positive anchored fixture execution, worker/unrelated roots, mutable event cwd, symlink and case aliases, preserved arguments/stdin/status, and an inherited `BASH_ENV` marker that remains absent.

   Formatter/map fixture cases keep the launch identity anchored while supplying outside-anchor and worker-repository inputs; payload and configuration markers remain absent. Anchored-file fixture inputs reach their selected fixture operations. This verifies guard routing, not actual Ruff, Prettier, Node or terminal-browser availability.

10. `.claude/settings.json` keeps its tracked project events and routes every command through the installed guard.

    Keep this non-template file portable. Commands use the exact clean prefix from item 3, followed by `"$HOME/.claude/hooks/orchestrator-only.sh"` and a fixed operation identifier. Put no host-specific home, interpreter-installation, anchor or tool-directory path in the tracked file.

    Every hook entry carries `onFailure: "block"`. Worker sessions execute no guarded project payload. Keep operation markers required by the existing validator, including `format-edited-files.py`.

    Retain `tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_every_tracked_project_hook_is_guarded_and_blocks_on_failure`. Traverse all events, matchers and command entries; reject unguarded commands, missing failure policy, missing HOME/launch-variable re-exports and worker-selected payload paths.

    Render distinct temporary homes and anchors while keeping tracked commands identical. No bound PermissionRequest appears in this tracked file.

11. `home/dot_local/bin/common/executable_herdr-agents` prepares the actual worker launch boundary.

    Every Claude worker process receives `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`, including managed-workspace and standalone routes and repeated starts. A variable present only in the parent spawn process is insufficient. Do not inherit a conflicting caller value.

    Every worker kind receives `UV_CACHE_DIR=<canonical-worktree>/.uv-cache` and `UV_PYTHON_INSTALL_DIR=<canonical-worktree>/.uv-cache/python`. Caller cache variables cannot replace these values.

    Stop creating worker-local `.claude/settings.local.json` for delivery hooks or merge denials. Put the managed worker delivery hooks and native merge denials in `~/.claude-worker/settings.json`.

    Before every Claude start, migrate an existing legacy worktree-local file. Remove each recognized managed delivery hook previously written by the launcher, preserve unrelated settings, and refuse startup while an unknown command hook remains, naming that entry. Do not create a local file merely to perform migration.

    Before every start, regenerate trusted worker delivery entries rather than skipping preparation on an existing match. Replace stale managed commands and avoid duplicates.

    Regenerate launcher-managed main-checkout local agmsg and attachment hooks through the installed guard. Preserve the existing permissions object and unrelated non-hook settings.

    Every launcher-rendered command hook uses the clean prefix from item 3 and carries `onFailure: "block"`. Delivery commands also preserve `AGMSG_RESOLVE_PROJECT=0` and launcher-supplied `AGMSG_STORAGE_PATH`. A writable `run/proj.<pid>.project` marker must not override the explicit worker project.

    Retain the native merge denials `Bash(gh pr merge:*)`, `Bash(gh api -X PUT:*)`, `Bash(gh api --method PUT:*)` and `Bash(gh api graphql:*)`. These command denials do not prevent all API merge routes with shared credentials.

    Codex launches retain `--sandbox workspace-write`, `--ask-for-approval never` and existing shared Git grants. Add no Codex network-policy change or test.

    Retain these selectors:

    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_worker_launch_receives_dedicated_policy_and_private_caches`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_repeated_worker_start_replaces_stale_managed_hooks`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_add_worker_migrates_legacy_worktree_local_hooks`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_launch_adds_no_unsandboxed_route`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_linked_worktree_uses_worker_user_hooks_and_guarded_main_local_hooks`
    - `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_every_settings_hook_has_system_path_prefix`

    The legacy fixture checks the effective combination of worker user settings, main-local settings and the legacy worktree-local file. Main-local guard markers remain absent under worker launch roots. Repeated preparation retains native denials.

    The prefix test traverses both launcher-written files after initial and repeated preparation, verifies the explicit HOME and launch-variable re-exports, suppresses inherited `BASH_ENV`, and invokes delivery resolution with a conflicting writable project marker.

12. Retain the delivery-environment portion of `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_hook_descendants_do_not_execute_path_interpreters`.

    Exercise installed-style agmsg delivery fixtures with directly executed `/usr/bin/env bash` descendants. Plant a leading Bash shim in the outer environment and verify that the rendered clean prefix gives descendants `/usr/bin:/bin`, leaving the shim marker absent.

    Remove the replacement Herdr state-helper implementation and its socket-reporting/interpreter-binding fixture from this PR. Keep the existing installed state hook behind the orchestrator guard; report its unresolved execution requirements with the binding task.

    Inventory reached delivery scripts, including `session-start.sh`, `session-end.sh`, `check-inbox.sh`, `identities.sh` and additional reached descendants. Distinguish clean environment and fixed delivery PATH evidence from complete executable binding.

    Fixed PATH does not mitigate `storage.sh` sourcing a driver selected by writable team configuration. Record the traversal and plugin-authorization routes as the `dotfiles-T133-agmsg-hardening-a01` residual.

13. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` changes only the Worker Playbook step 4 sentence listing outside-sandbox worker commands.

    Its replacement is:

    > Every worker command, including gh, git push and authenticated git fetch, runs inside the worker's sandbox; no worker command runs outside it.

    Historical TLS, keyring, artifact-writing and delivery exceptions provide no authorization to leave the sandbox. Shared managed exceptions provide no worker authorization either. An unavailable operation produces a blocked PONG naming the exact command and boundary.

    Retain `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_playbook_requires_every_command_inside_sandbox`.

    In `tests/unit/test_agmsg_orchestration_docs.py`, change only the assertion of that sentence. PR #427 has merged into the recorded main base; retain its changes and run the complete module.

14. `.gitignore` adds only `.uv-cache/`.

    Retain `tests/unit/test_herdr_agents.py::HerdrAgentsTest::test_worker_uv_cache_directory_is_gitignored`.

    The existing `.agents/worklog/` ignore covers the orchestrator cache. Its ignored status does not remove either worklog/cache pattern from the static deny inventory. Consuming hardening tasks own their use of the protected orchestrator cache.

15. `scripts/validate-agent-assets.py` changes the policy checks affected by the retained exclusion change.

    Replace the platform-specific exclusion branches with one exact ordered-list check for both Darwin and Linux:

    ```text
    agmsg-dispatch *
    herdr-agents *
    {{ .chezmoi.homeDir }}/.agents/skills/agmsg/scripts/actas-claim.sh *
    ```

    Compare the home-expanded equivalent when validating rendered settings. Keep non-empty-string list validation. Reject `gh *`, additional, missing, reordered or substituted entries on either platform.

    Keep the existing managed Claude PermissionRequest wiring check and ccgate refusal unchanged. The literal `permgate claude` form remains valid because this task preserves the command. Do not introduce the structural bound-hook parser, native-binding expansion or `--check-effective-settings` mode. Codex wiring checks remain unchanged.

    Keep surrounding schema, model/effort, formatter operation marker, permission-list, sandbox, plugin and Crit checks. Preserve duplicate-hook rejection, permgate-first ordering, synchronous timeout budgets and SessionStart state-hook marker/order checks. Do not weaken those checks to accommodate prefixes.

    Retain generated-output freshness, home-path/secret scanning, tracked project-settings portability and deterministic permgate-policy validation.

    In `tests/unit/test_validate_agent_assets.py`, keep the macOS gh-exclusion and Linux extra-exclusion cases in `ValidateAgentAssetsTest::test_claude_sandbox_validator_refuses_each_forbidden_form`.

    Update `ValidateAgentAssetsTest::valid_claude_sandbox` to contain the exact three-entry list. Preserve its callers and their intended checks:

    - `test_claude_sandbox_accepts_manifest_symmetric_settings`
    - `test_claude_sandbox_rejects_each_broken_rule`
    - `test_claude_sandbox_requires_extra_codex_writable_roots`
    - `test_claude_sandbox_extra_allow_write_must_be_absolute_or_home_paths_without_globs`
    - `test_claude_sandbox_unix_sockets_must_be_absolute_or_home_paths_without_globs`

    PermissionRequest fixtures in `test_hook_composition_requires_permgate_first`, generator tests and merge tests retain the legacy command. Adjust only surrounding non-PermissionRequest forms where the retained prefix/guard change requires it.

16. The seven allowed test modules reuse existing render, merge, fake-launcher and temporary-HOME fixtures.

    Write retained behavior tests before changing implementation and preserve base-failure/final-head-success evidence. New guard/worker-renderer entrypoints may supply the baseline missing-entrypoint failure.

    Do not retain the real-uv PermissionRequest execution test, fixture interpreter discovery, planted-user-site execution control, exact-version equality test, installation-existence render tests or binary-identity deployment-check fixtures. Static user-site inventory assertions remain.

    `onFailure: "block"` requires the recorded supported Claude version and has no enforcement effect on background hooks or excluded events. Configuration inspection does not establish runtime timeout or crash handling.

    Tests create no identities, initiate no login and access no real credential store. They do not establish credential separation, live administrative enforcement or upstream agmsg hardening.

17. `.orchestration/dotfiles-T133-worker-write-boundary-a01/` contains the byte-identical dispatched `task.md`, `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md`, operator instructions and worker review evidence.

    Map the findings history to retained controls, remaining residuals or their owning tasks. In particular, report executable-binding findings as transferred under D-024-26, not fixed by this PR.

    RESULT and the report list each file or portion of amendment-6/amendment-7 binding work reverted or left unmerged. Files removed from `allowed_files` must have no final PR diff. Shared files may retain only this text's authorized changes.

## Change budget

The starting measurement is the worker's snapshot `7c3a6394` on main `69dccca9`: 876 source and 1299 test changed lines under the former 888/1335 caps, using additions plus deletions and the generated-template exclusions stated in Check.

Subtract these binding-only source estimates: 45 generator/manifest binding lines, 45 structural PermissionRequest validator lines, 40 of the former 60 orchestrator modify-script lines, 25 worker native-renderer lines, 25 validator native-renderer lines and 8 isolated-token lines. Retain 20 of the former orchestrator modify-script allocation for classification of the hooks still managed here. Also remove the 29-line replacement Herdr state helper, which is present in the measured snapshot only for execution binding. The removed source allocation is `45 + 45 + 40 + 25 + 25 + 8 + 29 = 217`; the projected source total is `876 - 217 = 659`, and the narrowed source cap is `888 - 217 = 671`, retaining the former 12-line source margin.

Subtract these binding-only test estimates: 90 real-hook execution lines, 50 structural-validator lines, 25 native-render fixture lines, 60 of the former 90 binding-merge fixture lines, 35 planted-user-site execution lines, 12 isolated-token assertion lines and 24 state-helper-only descendant fixture lines. Retain 30 merge-fixture lines for the retained managed-hook classification and the remaining delivery-environment fixture coverage. The removed measured-snapshot allocation is `90 + 50 + 25 + 60 + 35 + 12 + 24 = 296`; the projected test total is `1299 - 296 = 1003`. Remove the additional unimplemented amendment-7 allocations of 12 discovery/skip lines and 24 declaration/render/deployment-check lines as well, making the narrowed test cap `1335 - 296 - 12 - 24 = 1003`.

These subtraction-based projections are planning estimates, not a measurement of a narrowed final head. The worker records actual per-file numstat and both totals after removing the binding family. No further increase is authorized by this text.

## Out of scope

`dotfiles-T133-trusted-entrypoint-binding-a01` is the owner of the executable-binding family and is a task to be written, with:

```yaml
after:
  - dotfiles-T133-worker-write-boundary-a01
  - dotfiles-T133-ci-efficiency-followup-a04
```

It consumes the trusted interpreter resolver from `dotfiles-T133-ci-efficiency-followup-a04`. Its scope includes exact host-probed installation layouts and declarations for uv, Python and Node; corresponding mise pins; the bound and isolated PermissionRequest invocation; structural validation and binding-form migrations; bound binary-identity deployment checks whose own execution is trusted; real-uv hook execution and planted-startup tests; complete descendant binding; formatter PATH changes; and any replacement state helper needed by that binding design.

This task does not write that task file. It names the owner and prerequisites without claiming the resolver, binding implementation or its tests have landed.

`home/dot_mise/config.toml` and `home/dot_local/bin/common/executable_herdr-agent-state.sh` are removed from `allowed_files`. Revert or leave their binding-family work unmerged. Remove binding-only portions of the manifest, generator, modify scripts, validator, guard and tests while retaining their authorized write-boundary changes. Do not leave dormant binding machinery in this PR.

The managed PermissionRequest keeps its current direct command behind the managed deny rules. Its interpreter discovery, startup environment and execution remain unverified here. No sanitized-prefix claim includes that exception.

Formatter and project-map PATH repair is deferred. The clean system PATH can leave current formatter or reload dependencies unavailable; report that interim limitation explicitly. Guard fixture success does not establish Ruff, Prettier, Node or terminal-browser execution. Do not repair their scripts, add tool directories or claim preservation of their complete runtime behavior in this task.

The Codex worker network change belongs to `dotfiles-T133-codex-worker-network-a01` on a Claude seat. This Codex seat edits no Codex-boundary source. Codex shared Git grants remain unchanged.

The worker-write-boundary Python hook and gh-trusted wrapper remain dropped. No worker gh configuration directory or credential-separation substitute is added.

D-024-23 establishes that `GH_CONFIG_DIR` does not separate same-macOS-user Keychain access. Shared credentials permit worker-initiated API merges despite native command denials. Separate-user or separate-host prevention remains the operator's P1-16 decision.

P1-14 a05 and P1-6 own approval and evidence-of-record consumption. The regime obtains the SHA returned by `git ls-remote origin refs/heads/main` and reads the committed ledger through `gh api repos/mryfmo/dotfiles/contents/.orchestration/decisions.tsv?ref=<sha>` inside the sandbox. Local files, refs, replacement refs and object traversal supply no approval authority. This task implements none of those consuming mechanisms and writes no approval row.

P1-11 owns next-records-PR detection of missing acceptance or gate evidence. This task states that rule without claiming it implements detection or prevention.

`dotfiles-T133-agmsg-hardening-a01` owns upstream driver-name validation and plugin authorization outside the writable stores. The recorded `drivers.partition` traversal and `db/trusted-plugins`/plugin sourcing routes remain residuals. This task adds no new store-derived sourcing beyond installed delivery behavior.

Consuming-helper snapshots, reservation locks, full-head output identities, the common trusted-execution test helper and review-worktree relocation remain with their owning hardening tasks.

The Codex templates, Codex modify script and Codex merge tests retain the separate `permgate codex` contract. `tests/unit/test_permgate.py` retains direct testing of the unchanged permgate source. `tests/unit/test_statusline_tools.py` retains its existing statusline-render assertions. No binding-only render expression is left to make those consumers depend on deployment installations.

The worker performs no authentication change, keyring mutation, ruleset mutation, administrative installation, live settings application, global installation, session restart or merge. It edits no canonical acceptance record, decision ledger or another task's text.

## Check

`make render-check` and `make validate-agent-assets` pass. The task's own files pass the `make format` flags: `shfmt -i 4 -sr --diff`, `ruff format --config ruff.toml --check` and `prettier --check`.

The clean historical base `205fe85c` has an inherited formatting failure on 12 out-of-scope files: ten archived task shell sources, `project-map-reload.sh` and `brew.bats`. Reproduce that failure against the unchanged base and disclose exact output and per-file exit statuses in `validation.md`. This authorizes no out-of-scope repair.

Shellcheck and shfmt cover changed shell sources, including the launcher and rendered guard. Added or changed shell comments use English shdoc-compatible annotations. Changed Python receives the repository's formatting and lint checks.

`uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_claude_settings_merge tests.unit.test_herdr_agents tests.unit.test_claude_worker_settings tests.unit.test_claude_managed_settings -v` is green.

`uv run python -m unittest tests.unit.test_validate_agent_assets tests.unit.test_agmsg_orchestration_docs -v` is green.

The validation record contains every named retained red-then-green selector and complete final module outputs.

The final diff has at most 671 changed lines outside `tests/` and `.orchestration/`, excluding the regenerated `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/claude-worker-settings.json` and `home/.chezmoitemplates/claude-managed-settings.json`.

The final diff has at most 1003 changed lines under `tests/`.

Changed lines mean additions plus deletions. Record per-file numstat, base/head identities and both actual totals. Keep subtraction arithmetic in Change budget.

The validation record contains exact commands, verbatim outputs, exit statuses and tested identities. Git verification introduced or changed by this task follows the design's sanitized Git requirements, including explicit checkout selection, disabled system/global configuration, hooks/fsmonitor restrictions and disabled external diff/textconv where applicable.

Both platform renders show separate worker and orchestrator settings, exact static inventory correspondence, filesystem source-path coverage, both worklog/cache patterns, explicit policy and guard protection, user-site directory/startup-file coverage, ordinary worktree writes, worktree `.claude`/`.mcp.json` denies, narrow home denies, writable agmsg stores, empty worker user exclusions, restricted worker writes and `failIfUnavailable: true` for every Claude seat.

Managed render evidence asserts sandbox enablement, startup failure, disabled unsandboxed retries, all required anti-weakening Booleans, exactly the three ordered exclusions and exactly the Herdr socket allowance. Conflicting project/local fixtures leave the trusted render unchanged. This is configuration evidence, not live runtime enforcement.

Staging evidence shows the temporary-HOME output and exact printed `sudo install -m 0644` command for both platform destinations, including quoting, with no executed sudo marker.

Hook evidence inventories every generated, tracked, modify-script-appended and launcher-managed command. It identifies PermissionRequest separately and confirms its exact unchanged `~/.local/bin/common/permgate claude` command. Every other command rendered by this task has the clean prefix with explicit HOME and hook-variable re-exports.

Delivery evidence verifies `AGMSG_RESOLVE_PROJECT=0`, preservation of launcher-supplied `AGMSG_STORAGE_PATH`, rejection of conflicting writable project-marker selection, suppressed inherited `BASH_ENV`, and system-only PATH propagation to the tested env-bash descendant. It makes no complete executable-binding claim.

Merged-settings evidence shows legacy managed non-PermissionRequest forms replaced once, custom hooks preserved, attachment handling, repeated-merge idempotence and unchanged legacy PermissionRequest migration.

Launch evidence shows both cache variables reaching the actual worker process on every route. Claude processes additionally receive the dedicated configuration directory. Repeated preparation replaces stale hooks and retains native merge denials and Codex sandbox/approval arguments.

Linked-worktree evidence checks worker user settings, guarded main-local settings and legacy worktree-local settings together. Migration removes old managed delivery commands, preserves unrelated settings, refuses unknown command hooks and creates no new local file when absent.

Guard evidence uses complete prefixed commands. Worker roots, unrelated roots, missing launch identity, worker-repository formatter inputs and outside-anchor inputs leave payload/configuration markers absent. Positive anchored fixture cases preserve arguments, stdin and status. Report actual formatter/tool availability as deferred.

The report identifies each binding-only file or portion removed from the measured snapshot and confirms that files outside the narrowed allowlist have no final PR diff.

The report retains the agmsg sourcing residual and owner, shared managed exclusions/socket access, same-UID credential access, path-consumption races, external-process trust, hook-event failure limitations, legacy PermissionRequest exception and retained Codex shared Git grant.

No local Bats tests run. Required Bats results come from GitHub Actions. Required checks pass before RESULT; an in-scope failure retains its actual output and receives an authorized fix.

The orchestrator runs `uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md` before dispatch and at acceptance. C1 to C10 and C7b pass.

A C-80 security-profile context reviews this complete narrowing before dispatch. The review and checker result are prerequisites, not results claimed by this draft.

## Completion

Continue one implementation PR on `tools/worker-write-boundary-a01` from its recorded rebased main base `69dccca9`; retain the earlier base `205fe85c` as historical context. Do not open a second implementation PR or discard unrelated work.

Before the first push, remove the executable-binding family from the PR. Revert it or leave it unmerged on the existing branch without carrying its final diff into this task. RESULT names the removed files and shared-file portions. Keep retained tests and fixtures rather than treating the whole implementation as disposable.

Replace `.orchestration/dotfiles-T133-worker-write-boundary-a01/task.md` with the byte-identical dispatched narrowing text and report its SHA256. There is no a02 task-copy substitution under this task id.

The Completion clauses of `.orchestration/tasks/dotfiles-T133-permission-guard-gate-a05.md` apply with this task's branch, files and evidence paths, `dotfiles-T133-worker-write-boundary-followup-a01` as owner of advisory P2 findings, and `task_copy=<sha256 of .orchestration/dotfiles-T133-worker-write-boundary-a01/task.md>` in RESULT. The a05-specific PR continuation, predecessor-copy deletion, deadline and implementation requirements do not transfer. The orchestrator writes the follow-up owner task before assigning its first advisory P2.

Every worker-side fix round counts toward INV-6. The worker's pre-push review is one round at most. A surviving P0/P1 is sent in RESULT as open and stops integration; do not start another private correction/review cycle to avoid reporting it.

No `@codex review` comment is posted. Observe automatic final-head reviews within the bounded 15-minute window and record absence as `bot: none`. Required GitHub Actions checks pass before RESULT. Every feedback item has a proposed disposition; surviving P0/P1 findings remain open for the operator.

Every gh write and git write runs as a separate command without shell chaining. Every worker command remains inside its sandbox. An unavailable operation produces a blocked PONG with its exact command and boundary.

The Codex worker writes evidence at the required relative paths in its own worktree and says so in RESULT. Worker review evidence uses the `-worker-` infix. Crit-data evidence and receipts follow repository rules without a browser review or human review request. The orchestrator copies evidence before acceptance.

`AGMSG-RESULT v1` names the final head, base, branch, changed files, removed binding-family files/portions, retained new scripts and installed paths, trusted anchor, retained hook inventory, PermissionRequest exception, settings destinations, staging path, printed installation command, Bot findings/dispositions, open P0/P1 findings, exact selectors, measured totals, task-copy SHA256 and evidence paths. Distinguish historical observations from final-head results and name all pending operator steps.

Report the user-visible effects:

- Claude workers use `~/.claude-worker` and require its separate Claude login.
- Trusted-path and worktree-configuration denies also affect Bash sandbox writes.
- Agmsg stores remain writable except `db/trusted-plugins`; plugin code is denied.
- Worker user policy adds no exclusions or Herdr socket allowance, while shared managed policy retains both for every seat.
- Tracked and main-local orchestrator project hooks execute no payload in worker sessions.
- Worker caches are private.
- Every Claude seat fails when sandboxing is unavailable.
- Administrative policy requires sandboxing and disables unsandboxed retries for the orchestrator too.
- The former Linux gh exemption is removed.
- Non-PermissionRequest commands receive the clean prefix; the legacy PermissionRequest remains unchanged.
- Formatter/map tool availability and complete executable binding remain deferred to the binding task.

Report that no gh credential separation is established. Shared credentials permit worker-initiated API merges despite native denials. GitHub provides next-records-PR detection under P1-11, not prevention.

This task remains `security: true`. The orchestrator obtains a task-level audit and separate security-profile review of the final implementation head. Preserve the executable-binding class history and D-024-26 re-plan record alongside `decision-not-bound-to-execution`, `unbound-evidence` and `fail-open-on-error`. Do not reset inherited counters or relabel transferred findings as fixed.

Final-head feedback collection, task-level audit, finding dispositions, acceptance and integration follow Orchestrator Playbook step 10 in order. The gate receives `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE` and the agent review receipt. Changed heads receive fresh required evidence, and final-head security review precedes the gate.

The permission-surface change receives operator-backed approval through the existing repository process. The worker writes no approval row and treats no candidate-tree decision as authority.

Live deployment is the operator's post-merge `make update`. The operator runs `make install-managed-settings`, inspects staging and executes the printed `sudo install -m 0644` command at the detected macOS or Linux destination. Record administrative installation separately from ordinary chezmoi application.

The operator performs the Claude login with `CLAUDE_CONFIG_DIR=<absolute-home>/.claude-worker`, applies the prepared deterministic Codex permgate rule that stops approving sandbox escapes, and restarts affected sessions.

Retain the deployment record's effective-policy inspection after application and administrative installation: installed managed content, worker directory, static denies, worktree configuration protection, writable stores, worker-user/main-local/legacy hook placement, the PermissionRequest exception, failure-policy coverage and sandbox startup. Check conflicting project/local sandbox relaxations and record shared managed capabilities without exposing credentials.

This retained policy inspection does not add the removed automated binary-identity checker, its trusted launch command, executable version probes or real-uv hook execution. Those belong to the binding task.

Merge alone does not establish deployment readiness. Record the operator's application, administrative installation, login, startup checks and Codex permgate change before releasing dependent mechanisms for live operation; any mechanism requiring the deferred executable-binding contract also waits for its binding prerequisite.

## Checks (pasted by the orchestrator before each send)

The retained block below is the historical amendment-6 dispatch record carried by amendment 8. Its review result does not approve this narrowing. Before sending, the orchestrator replaces it with fresh consistency-check output, the review of these exact bytes, current counters and the D-024-26 re-plan reference.

```
narrowed text (D-024-26: the write boundary alone; the executable binding moved to trusted-entrypoint-binding-a01), 2026-10-19T11:3xZ; task-consistency-check.py: OK; C-80: .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-679166e.md.last.md Verdict: correct (the 20th review; re-plan line of 11:1xZ; C-92 guard passed)
S2: amendments 4 >= 2 source=live
detail: pr=none authors=claude-deep-dot tasks=01a152ae-8ef0-784f-801e-d4c9a4f3007f,01a152ed-0b08-7431-8fd0-5b5e43c89bd6,01a1533c-1568-7e88-8653-ef63f42314a2,01a1537c-0498-7df1-8c89-2b805cf64b57,01a1539e-59a8-7aee-8556-dd14c1e56719 results=- questions=- withdrawn=- bot_heads=- source=live
```

Local Bats, live enforcement, administrative installation, login, permgate policy changes and deployment are not performed by the worker.
Legacy PermissionRequest execution, formatter tool availability, same-UID access, shared managed capabilities, path races and agmsg sourcing remain the named residuals.