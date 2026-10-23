---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-binding-a01
kind: code
security: true
allowed_files: ["home/dot_agents/agent-config.yaml","home/.chezmoitemplates/claude-settings-managed.json","home/dot_claude*/modify_private_settings.json","scripts/generate-agent-configs.py","scripts/validate-agent-assets.py","Makefile","tests/unit/test_claude_managed_settings.py","tests/unit/test_validate_agent_assets.py","tests/unit/test_generate_agent_configs.py","scripts/orchestrator/trusted-launch.sh",".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**"]
after: [dotfiles-T133-worker-write-boundary-slice2-a01, dotfiles-T133-ci-efficiency-followup-a04]
rendered_forms: [claude-settings-managed.json, permgate claude]
out_of_scope:
  - {"path":"home/dot_mise/config.toml","reason":"dotfiles-T133-trusted-entrypoint-pins-a01 pins the real declaration before this task is sent; it is read-only here."}
  - {"path":"tests/unit/test_claude_settings_merge.py","reason":"Existing legacy/custom/idempotence cases remain valid through the modify script's native expansion; run this real module unchanged."}
  - {"path":"tests/unit/test_statusline_tools.py","reason":"Its native renderer must continue to parse the template without deployment installations; run unchanged."}
  - {"path":"tests/unit/test_herdr_agents.py","reason":"The synthetic SessionStart-only template is unaffected; retain its tests."}
  - {"path":"tests/install/common/lifecycle.bats","reason":"Legacy migration fixture data is retained; Bats runs only in GitHub Actions."}
  - {"path":"tests/fixtures/gate-evidence/pr-feedback-right.json","reason":"Historical feedback fixture text is data and is not rewritten."}
  - {"path":"scripts/orchestrator/trusted-interpreter.sh","reason":"The a04 resolver remains read-only for its existing consumers. This re-plan's launcher validates the exact Python declared by its parent-selected manifest; it must not impose the resolver's production-only pin on fixture execution."}
  - {"path":"home/dot_local/bin/common/executable_permgate","reason":"Unchanged dependency-free script, executed through explicit isolated Python rather than its shebang."}
  - {"path":"home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","reason":"Complete guard, delivery and formatter/map descendant binding is outside this split; retain its named deployment residuals."}
threat_table:
  - {"control":"home/dot_agents/agent-config.yaml","disposition":"residual: Declare exact home-relative uv, Python and node identities and compare their production versions with the read-only mise declaration; deterministic rendering supplies the launcher manifest, while protected inputs still share the OS uid."}
  - {"control":"home/.chezmoitemplates/claude-settings-managed.json","disposition":"residual: Render the PermissionRequest exec-form clean prefix with an exact absolute --manifest operand and retain onFailure block; no outer shell starts, but the hook host and first executable's loader environment remain outside launcher validation."}
  - {"control":"home/dot_claude/modify_private_settings.json","disposition":"residual: Classify the legacy form separately and compare the bound command string and ordered args array, including --manifest, exactly with the rendered canonical exec form; preserve raw quoting distinctions, custom hooks and idempotence."}
  - {"control":"home/dot_claude-worker/modify_private_settings.json","disposition":"residual: Apply the same native expansion and exact bound command/args comparison to this consumer without importing live orchestrator settings or adding an event the surface lacks."}
  - {"control":"scripts/generate-agent-configs.py","disposition":"residual: Render exact relative declarations, the launcher manifest data and exec-form command/args without filesystem discovery; ordinary generation and render-check require no installed tools or deployed manifest."}
  - {"control":"scripts/validate-agent-assets.py","disposition":"residual: Validate exact rendered command/args and expose the opt-in effective-settings identity check; checker and yaml-importing children consume the same parent-selected manifest, verified uv/Python and private cache without substituting production pins into fixtures."}
  - {"control":"Makefile","disposition":"residual: Expose concrete manifest preparation, trusted seed and deployment-check commands and give the formatter the pinned node directory; unrelated inherited recipes remain outside this boundary."}
  - {"control":"scripts/orchestrator/trusted-launch.sh","disposition":"residual: Before any declared binary executes, validate the absolute parent-selected manifest and optional fixture root, parse declarations as data, require canonical regular executable paths and compare exact versions; fixture and production inputs use these same checks, while concurrent same-UID replacement remains possible."}
  - {"control":"tests/unit/test_claude_managed_settings.py","disposition":"residual: Exercise exact exec-form rendering, migration, a real fixture-manifest uv/Python/permgate execution and the separate pinned-installation case; fixture execution proves the shared launcher path, not production installation or administrative protection."}
  - {"control":"tests/unit/test_validate_agent_assets.py","disposition":"residual: Exercise manifest containment, shim, symlink, worker-root and version refusals, quote-preserving comparisons and the clean online seed; recording fake uv cases prove argv and refusal behavior only."}
  - {"control":"tests/unit/test_generate_agent_configs.py","disposition":"closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_hooks_use_installed_permgate_paths asserts the executable leaf and the permission-request operand from args; the pins refactor rsplit form raises ValueError on the env+args command (pins audit:28dde0f:1)"}
  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/**","disposition":"residual: Only task copies, reports, manifest test data and review or validation evidence are authorized; no executable helper or alternative hook may hide under this wildcard."}
  - {"control":"task copy .orchestration/dotfiles-T133-trusted-entrypoint-binding-a01/task.md","disposition":"residual: Compare the complete dispatched file byte-for-byte and verify its SHA-256; preserve predecessor copies and the three-review history."}
  - {"control":"task metadata","disposition":"residual: Verify identity, both after dependencies, the pin prerequisite and exactly ten allowed_files entries before dispatch and acceptance; the modify-script glob has only its two named consumers."}
  - {"control":"metadata separators","disposition":"residual: Parse front matter as data with duplicate keys refused and compare the whole task copy, including both separate task texts and their separators."}
  - {"control":"in-process effects","disposition":"residual: Fixture execution writes temporary data and markers only; the effective-settings check is read-only and the worker performs no live deployment."}
  - {"control":"workflow and interpreter or environment inputs","disposition":"residual: The trusted parent names the manifest and any fixture root under the clean prefix; launcher discovery, environment overrides and production-only fixture gates are forbidden."}
  - {"control":"new or renamed scripts","disposition":"residual: Only the named launcher is added; manifest parsing and exact-path validation stay there, and no second resolver, wrapper executable or artifact-directory runtime helper is introduced."}
  - {"control":"orchestrator effect manifest provisioning","disposition":"residual: The operator materializes deterministic production manifest data under the protected repository root before enabling the changed hook; fixture manifests cannot become effective production bindings."}
  - {"control":"orchestrator effect merge","disposition":"residual: Only the orchestrator merges the reviewed final head after Playbook step 10; shared credentials remain a bypass risk."}
  - {"control":"orchestrator effect update-branch","disposition":"residual: Only the orchestrator updates the branch and refreshes evidence after any head change."}
  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; only the orchestrator may remove a worker and must record any discarded state."}
  - {"control":"design 5.14 item 0 same-UID model","disposition":"residual: These controls limit accidents and prompt injection; shared credentials and unrestricted same-UID processes remain outside prevention."}
  - {"control":"design 5.14 item 1 executable inputs","disposition":"residual: Retain P1-15 protection of policy, user-site locations, settings, rendered manifest and installed tools; executable binding alone does not protect mutable inputs."}
  - {"control":"design 5.14 item 2 trusted parent","disposition":"residual: Exec form starts /usr/bin/env -i with literal argv before the privileged launcher validates entry state and the selected manifest; the hook host and loader starting /usr/bin/env still require host-supplied clean execution or the P1-16 OS user boundary."}
  - {"control":"design 5.14 item 3 resolved boundaries","disposition":"residual: Apply canonical path, regular-file, shim, worker-root and temporary-root checks to the supplied manifest and its declarations; the explicitly named fixture root is a scoped test allowance, not a production setting."}
  - {"control":"design 5.14 item 4 verified executable","disposition":"residual: Execute only the checked declared realpaths without rediscovery and record the selected manifest identity; unrestricted same-UID replacement after validation remains possible."}
  - {"control":"design 5.14 item 5 output identity","disposition":"residual: Record full base/head identities, task-copy hash and manifest hashes; no new reservation or slot lock is introduced."}
  - {"control":"design 5.14 item 6 honest residuals","disposition":"residual: Report declaration checks, real fixture execution, the named pinned-installation skip, CI and operator-host deployment separately; no fixture or skip substitutes for production evidence."}
  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the eight named regressions and scoped hostile-input cases, recording Class::test selectors without claiming system-wide closure or treating an earlier refusal as coverage of a later check."}
  - {"control":"design 5.14 item 8 authenticated evidence","disposition":"residual: A parent-selected manifest supplies executable declarations, not permission or merge approval; integration evidence and live agmsg hardening retain their separate owners."}
  - {"control":"design 5.14 item 9 isolation and cache","disposition":"residual: Bound Python children use -I and isolated offline uv with an absolute parent-supplied private cache; the explicit online seed uses the same manifest, clean parent and verified uv/Python, retaining --no-config --no-project --isolated --with pyyaml --python and -I while omitting only --offline."}
  - {"control":"design 5.14 item 10 sandbox","disposition":"residual: Every worker command stays inside the sandbox; denial produces blocked evidence without escalation or an alternative execution surface."}
premises:
  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/uv/\" | paste -sd '|' -","output":"0|0.12|0.12.17|0.12.18|0.12.19|0.12.20|0.13|0.13.0|0.13.1|global|latest"}
  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/uv/0.13.1/\" | paste -sd '|' -","output":"uv-aarch64-apple-darwin"}
  - {"command":"realpath \"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv"}
  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/python/\" | paste -sd '|' -","output":"3|3.15|3.15.0|global|latest"}
  - {"command":"realpath \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15"}
  - {"command":"head -1 \"$HOME/.local/share/mise/installs/npm-prettier/3.9.10/bin/prettier\"","output":"#!/usr/bin/env node"}
  - {"command":"ls -1 \"$HOME/.local/share/mise/installs/node/\" | paste -sd '|' -","output":"26|26.12|26.12.0|global|latest"}
  - {"command":"realpath \"$HOME/.local/share/mise/installs/node/26.12.0/bin/node\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/installs/node/26.12.0/bin/node"}
  - {"command":"grep -nE '^(uv|python|node) = ' home/dot_mise/config.toml | paste -sd '|' -","output":"3:node = \"latest\"|5:python = \"latest\"|17:uv = \"latest\""}
  - {"command":"ls -1 .mise.toml mise.toml 2>&1 | paste -sd '|' -","output":"ls: .mise.toml: No such file or directory|mise.toml"}
  - {"command":"cat mise.toml | paste -sd '|' -","output":"[tools]"}
  - {"command":"grep -n '\"command\": \".*permgate claude\"' home/.chezmoitemplates/claude-settings-managed.json","output":"207:            \"command\": \"~/.local/bin/common/permgate claude\","}
  - {"command":"head -1 home/dot_local/bin/common/executable_permgate","output":"#!/usr/bin/env -S uv run --no-cache --script"}
  - {"command":"grep -cE '^# ///|^# dependencies[[:space:]]*=' home/dot_local/bin/common/executable_permgate","output":"0"}
  - {"command":"sed -n '179,182p' Makefile | paste -sd '|' -","output":"format:| shfmt --indent 4 --space-redirects --diff .| git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check| git ls-files -z '*.md' | xargs -0 prettier --check"}
  - {"command":"grep -cE '(^|[[:space:]])(export[[:space:]]+)?PATH[[:space:]:?+]*=' Makefile","output":"0"}
  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_agents/agent-config.yaml home/.chezmoitemplates/claude-settings-managed.json home/dot_claude/modify_private_settings.json home/dot_claude-worker/modify_private_settings.json scripts/generate-agent-configs.py scripts/validate-agent-assets.py Makefile tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":"Makefile|home/.chezmoitemplates/claude-settings-managed.json|home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/generate-agent-configs.py|scripts/validate-agent-assets.py|tests/unit/test_validate_agent_assets.py"}
  - {"command":"grep -nE '^  - (home/dot_claude-worker/modify_private_settings.json|tests/unit/test_claude_managed_settings.py)$' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | paste -sd '|' -","output":"12:  - home/dot_claude-worker/modify_private_settings.json|27:  - tests/unit/test_claude_managed_settings.py"}
  - {"command":"grep -nE '^def (render_claude_settings|render_template_text|validate_claude_settings|validate_model_profile_assets|validate_generated_agent_configs|main|render_managed_template|is_managed_permission_hook)\\(' scripts/generate-agent-configs.py scripts/validate-agent-assets.py home/dot_claude/modify_private_settings.json | paste -sd '|' -","output":"scripts/generate-agent-configs.py:400:def render_claude_settings(manifest: dict[str, Any]) -> str:|scripts/generate-agent-configs.py:1401:def main() -> None:|scripts/validate-agent-assets.py:88:def render_template_text(path: Path, os_name: str = \"darwin\") -> str:|scripts/validate-agent-assets.py:374:def validate_claude_settings(manifest: dict[str, Any], os_name: str = \"darwin\") -> None:|scripts/validate-agent-assets.py:1187:def validate_model_profile_assets(manifest: dict[str, Any]) -> None:|scripts/validate-agent-assets.py:1294:def validate_generated_agent_configs() -> None:|scripts/validate-agent-assets.py:1660:def main() -> None:|home/dot_claude/modify_private_settings.json:48:def render_managed_template(text: str) -> str:|home/dot_claude/modify_private_settings.json:68:def is_managed_permission_hook(hook: Any) -> bool:|home/dot_claude/modify_private_settings.json:196:def main() -> int:"}
  - {"command":"sed -n '400,487p' scripts/generate-agent-configs.py | wc -l | xargs","output":"88"}
  - {"command":"sed -n '88,100p;374,406p;1187,1265p;1294,1304p;1660,1685p' scripts/validate-agent-assets.py | wc -l | xargs","output":"162"}
  - {"command":"sed -n '48,55p;68,79p' home/dot_claude/modify_private_settings.json | wc -l | xargs","output":"20"}
  - {"command":"wc -l .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | xargs","output":"63 .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json 95 .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py 1781 tests/unit/test_validate_agent_assets.py 79 home/dot_mise/config.toml 2350 tests/unit/test_generate_agent_configs.py 4368 total"}
  - {"command":"ls tests/unit/test_task_consistency_c11_c15.py 2>&1 | paste -sd '|' -","output":"ls: tests/unit/test_task_consistency_c11_c15.py: No such file or directory"}
  - {"command":"sed -n '63,66p' .claude/worktrees/worker-g/tests/unit/test_task_consistency_c11_c15.py | paste -sd '|' -","output":"CASES = {|    \"C11\": (|        '\"closed: tests/unit/test_tool.py::test_tool_prints_findings\"',|        '\"closed: tests/unit/test_tool.py::two words\"',"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\" --version","output":"uv 0.13.1 (62faed335 2026-10-13 aarch64-apple-darwin)"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B --version","output":"Python 3.15.0"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/node/26.12.0/bin/node\" --version","output":"v26.12.0"}
  - {"command":"rg -l 'claude-settings-managed|is_managed_permission_hook|permgate claude' home scripts tests .github Makefile --glob '!*.md' --glob '!*.lock' | sort | paste -sd '|' -","output":"home/dot_agents/agent-config.yaml|home/dot_claude/modify_private_settings.json|scripts/validate-agent-assets.py|tests/fixtures/gate-evidence/pr-feedback-right.json|tests/install/common/lifecycle.bats|tests/unit/test_claude_settings_merge.py|tests/unit/test_generate_agent_configs.py|tests/unit/test_herdr_agents.py|tests/unit/test_statusline_tools.py|tests/unit/test_validate_agent_assets.py"}
  - {"command":"grep -nE '^class (ClaudeManagedSettingsTest|ValidateAgentAssetsTest)' .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py | paste -sd '|' -","output":".claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py:12:class ClaudeManagedSettingsTest(unittest.TestCase):|tests/unit/test_validate_agent_assets.py:84:class ValidateAgentAssetsTest(unittest.TestCase):"}
  - {"command":"sed -n '117p' .orchestration/tasks/dotfiles-T133-ci-efficiency-followup-a04.md | cut -d . -f 1-2","output":"On success print exactly one absolute interpreter realpath and exit 0. On every refusal print exactly one line `trusted-interpreter: refused: <code>` to stderr, print no interpreter on stdout, and exit 2"}
  - {"command":"printf '%s\\n' \"$PATH\" | sed \"s|$HOME|\\$HOME|g\"","output":"$HOME/.local/share/mise/shims:$HOME/.local/bin:$HOME/.local/bin/common:/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$HOME/.local/share/mise/installs/npm-openai-codex/0.162.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path:$HOME/.local/share/mise/installs/node/lts/bin:/usr/bin:/bin:/usr/sbin:/sbin"}
  - {"command":"grep -nE '^    import yaml|PyYAML is required' scripts/validate-agent-assets.py | paste -sd '|' -","output":"22:    import yaml|81:        fail(\"PyYAML is required\")|175:        fail(\"PyYAML is required to validate skill frontmatter\")"}
  - {"command":"sed -n '340,346p' .orchestration/tasks/dotfiles-T133-worker-write-boundary-a01.md | paste -sd '|' -","output":"   Its managed PermissionRequest command remains exactly:||   ```text|   ~/.local/bin/common/permgate claude|   ```||   Do not add an env prefix, guard selector, absolute uv/Python invocation or new command-form validator for this hook. Keep its existing timeout and add the task's common `onFailure: \"block\"` entry policy. The unchanged command's shebang, interpreter discovery and inherited environment are explicit residuals owned by the binding task."}
  - {"command":"head -1 .claude/worktrees/worker-e/home/dot_claude/hooks/executable_orchestrator-only.sh.tmpl","output":"#!/bin/bash"}
  - {"command":"test ! -e scripts/orchestrator/trusted-launch.sh","output":"","exit_status":0}
  - {"command":"python3 -I -B -c 'from pathlib import Path; roots=(Path(\"home\"),Path(\".claude/worktrees/worker-e/home\")); print(\"|\".join(str(p) for root in roots for p in sorted(root.glob(\"dot_claude*/modify_private_settings.json\"))))'","output":"home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude/modify_private_settings.json|.claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json"}
  - {"command":"python3 -I -B -c 'import os,pwd,stat; from pathlib import Path; h=Path(pwd.getpwuid(os.getuid()).pw_dir); u=h/\".local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv\"; r=u.resolve(strict=True); print(\"home_matches_passwd=\"+str(Path.home()==h)); print(\"uv_regular=\"+str(stat.S_ISREG(u.lstat().st_mode))); print(\"uv_symlink=\"+str(u.is_symlink())); print(\"uv_under_passwd_install_root=\"+str(r.is_relative_to(h/\".local/share/mise/installs\"))); print(\"uv_declared_equals_realpath=\"+str(u==r)); print(\"trusted_launch_exists=\"+str(Path(\"scripts/orchestrator/trusted-launch.sh\").exists()))'","output":"home_matches_passwd=True\nuv_regular=True\nuv_symlink=False\nuv_under_passwd_install_root=True\nuv_declared_equals_realpath=True\ntrusted_launch_exists=False"}
  - {"command":"rg -n '^    import yaml|PyYAML is required' scripts/generate-agent-configs.py | paste -sd '|' -","output":"14:    import yaml|34:        fail(\"PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py\")"}
  - {"command":"sed -n '1294,1298p' scripts/validate-agent-assets.py | paste -sd '|' -","output":"def validate_generated_agent_configs() -> None:|    result = subprocess.run(|        [sys.executable, str(ROOT / \"scripts/generate-agent-configs.py\"), \"--check\"],|        cwd=ROOT,|        text=True,"}
  - {"command":"/usr/bin/env -i PATH=/usr/bin:/bin HOME=\"$HOME\" LANG=C.UTF-8 \"$HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15\" -I -B scripts/generate-agent-configs.py --check","output":"ERROR: PyYAML is required: uv run --with pyyaml scripts/generate-agent-configs.py","exit_status":1}
  - {"command":"claude --version","output":"2.1.300 (Claude Code)","exit_status":0}
  - {"command":"python3 -I -B -c 'from pathlib import Path; b=(Path.home()/\".local/share/mise/installs/npm-anthropic-ai-claude-code/latest/bin/claude\").read_bytes(); s=b\"Command hooks require `command`. For exec form (no shell)\"; i=b.find(s); print(b[i:b.index(b\"\\0\",i)].decode() if i>=0 else \"missing exec-form help\")'","output":"Command hooks require `command`. For exec form (no shell), set `command` to the executable and `args` to its arguments: {\"type\": \"command\", \"command\": \"echo\", \"args\": [\"hi\"]}. For shell form, set `command` to the full shell string: {\"type\": \"command\", \"command\": \"echo hi\"}.","exit_status":0}
  - {"command":"web.open https://code.claude.com/docs/en/hooks#exec-form-and-shell-form","output":"Command hook args present selects direct executable spawn without a shell; args omitted selects shell form (sh -c on macOS/Linux). command is the executable path and args is its argument vector. Documented path placeholders include ${CLAUDE_PROJECT_DIR} and are substituted as plain strings."}
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-binding-a01 — bind trusted entrypoints to a parent-selected manifest

Worker: a Codex seat (worktree named at dispatch)

Use the security profile for this Claude-boundary change. D-024-26 split this family from P1-15. Read the last 60 lines of .orchestration/acceptance/dotfiles-T133-worker-write-boundary-a01.md and .orchestration/validation/dotfiles-T133-worker-write-boundary-a01-text-security-{f810c30,772cde0,e5c055e,5204254}.md.last.md: shebang discovery, Python startup injection, the checker's own execution, shim discovery, the real uv layout and Prettier's node must be handled together.

Read the complete binding acceptance record and these three pre-dispatch reviews:

- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-faae5f4.md.last.md
- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-8f5ac8d.md.last.md
- .orchestration/validation/dotfiles-T133-trusted-entrypoint-binding-a01-text-security-e3ae7cd.md.last.md

This is the C-92 fixture-vs-binding re-plan recorded by the acceptance record's `re-plan:` line, not a fourth repair under the predecessor design. Preserve the earlier findings and their dispositions. The new design retains round 3's exec-form hook, quote-preserving comparisons and bound online seed, and replaces its contradictory positive-fixture requirement.

The launcher validates the manifest its trusted parent explicitly names. Production passes the rendered production manifest; tests pass a fixture manifest declaring the runner's real tools. Both use the same manifest parser, exact-path checks, containment checks, version comparisons and command construction. A fixture cannot bypass a check, and a production-only resolver or hard-coded installation gate must not run before the fixture's declared interpreter.

These are two separate task files. This primary task has exactly ten allowed_files entries: eight exact implementation/test paths, one modify-script glob and one evidence wildcard. The glob authorizes only home/dot_claude/modify_private_settings.json and home/dot_claude-worker/modify_private_settings.json, each with its own threat row. An additional match requires a reviewed split. The second file below owns mise pins and the generator assertion; do not combine their front matter or dispatch this task before that prerequisite is accepted.

## Dispatch prerequisites and scope

Accept dotfiles-T133-trusted-entrypoint-pins-a01 before the Python-resolver dependency is dispatched; the historical probe says latest for all three tools. Accept both after dependencies and verify P1-15's deployed protection before sending this task.

The seven existing concrete allowlist paths were on origin/main at the recorded probe. P1-15 creates the worker modify script and ClaudeManagedSettingsTest module. Add scripts/orchestrator/trusted-launch.sh as the only new executable source. Recheck these paths and measurements on the actual dispatch baseline; refresh changed premises through a reviewed, hashed amendment before dispatch, never only in the Checks paste.

The installed a04 resolver remains read-only. Its existing consumers retain its production-pinned contract. For the scoped launcher, this re-plan explicitly replaces the earlier instruction to obtain Python unconditionally from that resolver: resolve and validate the exact Python declaration in the parent-selected manifest, using the same code for production and fixtures. Do not edit the resolver, add PATH discovery to production, or make a fixture satisfy an unrelated host's mise pin.

The root C11 test file was absent at the recorded probe, and the inspected worker-g copy accepted tests/<path>::<identifier> rather than a Class::test payload. The orchestrator must obtain and read the accepted checker/test revision before dispatch, check C1–C10, C7b and C11, and manually re-probe premises. Never execute arbitrary premise shell strings through an unchecked checker.

Each threat-table file row names one file or one allowed wildcard only. This draft makes no closed claims. Any later closed row must name exactly one selector in the form tests/<path>::<Class>::<test>; a module name, free-function selector or prose reference is insufficient.

## Applicable design — C-88 verbatim quotations

`$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, section 5.14, is uncommitted design input. The relied-on sentences of items 1, 2 and 9 are quoted verbatim below. The parent-selected manifest contract is this re-plan's explicit scoped replacement for an unconditional production-pinned resolver call.

> The protected-path inventory a seat's Edit denies cover is enumerated from the inputs of every trusted executable, not only the executables: it includes `~/.agents/permgate-policy.yaml` (permgate rereads it for every decision), `~/.local/lib/python*/site-packages` and every other user-site or startup-hook location of the interpreters in use (`.pth`, `usercustomize.py`, `sitecustomize.py`), `~/.claude-worker`'s hook and settings files, and the rendered guard; a text that binds an executable names its inputs in the same inventory (P1-15 amendment 5 C-80, 2026-10-19).
>
> A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.
>
> One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19). A program takes `UV_CACHE_DIR` from the environment the trusted parent supplies and refuses when it is absent or not an absolute path; it never computes a default from its own root. The orchestrator's parent prefix sets the main checkout's `.agents/worklog/uv-cache`; a worker's launcher sets `<worktree>/.uv-cache` (the P1-15 worker launch value: `.agents/` is read-only in the Codex permission profile, so a root-derived `.agents/worklog/uv-cache` cannot be created by a worker; P1-12 a03, 2026-10-19T11:28Z); tests set a temporary directory.

## Implementation contract

### Declarations and deterministic rendering

Declare production uv 0.13.1 at .local/share/mise/installs/uv/0.13.1/uv-aarch64-apple-darwin/uv, Python 3.15.0 at .local/share/mise/installs/python/3.15.0/bin/python3.15, and node 26.12.0 at .local/share/mise/installs/node/26.12.0/bin/node, relative to the real uid's passwd home. A test compares all three production versions with home/dot_mise/config.toml. No wildcard, version alias, latest, shim, traversal or missing required declaration is accepted. If accepted pins differ from these probes, stop for a re-probed amendment rather than substituting an installed version.

Rendering composes the supplied home and repository bindings with these declarations and validates shape only. It remains deterministic on a host with no installs. Use the same native expansion in both modify-script consumers and the validator renderer, with correct JSON and shell quoting, including homes and repository paths containing spaces.

Render the launcher manifest as data from the source manifest. The fixed production destination is <canonical repository root>/.agents/worklog/trusted-entrypoint-manifest, outside worker-writable roots. It is an operator-provisioned runtime data artifact, not a new tracked source file or an executable under the evidence wildcard. The operator materializes it during deployment preparation before enabling the changed hook. Tests render into their temporary fixture root. Ordinary generation and render-check compare the deterministic rendering without requiring or writing the installed production artifact.

Use one small, documented data grammar that the privileged-shell launcher can parse with fixed absolute system tools before executing any declared uv or Python. Treat every field as literal data: no source, eval, shell expansion, command substitution or declared-interpreter bootstrap. Reject malformed, duplicate, unknown or missing required fields. Declare exact relative paths and exact versions; declarations must not select arbitrary commands. The production manifest also carries the rendered worker-root inventory used by containment checks.

### Parent-selected manifest and shared checks

Every launcher invocation requires exactly one `--manifest <absolute path>` before its operation. There is no implicit manifest, environment-variable replacement or discovery fallback. The only additional root argument is one optional `--fixture-root <absolute directory>`, also supplied by the trusted parent before the operation.

Validate the launcher entry state before reading the manifest. Retain #!/bin/bash -p, English shdoc comments, the exact accepted clean environment, the canonical non-symlinked launcher pathname under its repository root and HOME equality with the real uid's passwd home. Account explicitly for Bash-maintained environment entries. Refuse rather than repairing the environment or self-re-executing.

Resolve the manifest and require a regular, non-symlinked file whose canonical path is under the repository root or, when explicitly supplied, under the canonical fixture root. Reject sibling-prefix lookalikes, path traversal and symlink escapes. A fixture root must be an existing canonical directory; it does not replace passwd HOME, the launcher repository root or the launcher's own entry checks.

Apply the same checks to every declared executable required by the selected operation:

1. Require the exact declared relative path, composed with passwd home for production or the explicitly named fixture root for fixture bindings. Do not accept an arbitrary absolute executable operand, a parent traversal or a different installation chosen by discovery.
2. Require a regular executable file, reject a symlinked binary or redirected installation component, and require the declared composed pathname to equal the canonical executable pathname.
3. Reject a `shims` path component before and after resolution.
4. Reject containment under worker-writable roots, worker caches or temporary roots, including $TMPDIR. The explicitly named fixture root is the sole scoped allowance for fixture files under temporary storage; it does not waive regular-file, symlink, shim, exact-path or version checks. Explicit worker subroots within a fixture remain forbidden.
5. Complete identity and containment checks before executing that binary, including a --version probe. Compare the reported version exactly with that manifest's declared pin, then use only the verified absolute realpath.

The production manifest pins must match the repository's mise declaration. A fixture manifest instead pins the actual versions of its real fixture tools. Comparing fixture versions with production mise pins, calling the production-only resolver first, or accepting arbitrary runner paths without the shared checks would reproduce the rejected design.

No launcher-side command -v, mise which, newest-version selection, PATH fallback, download or alternative resolver is permitted. Test-harness discovery described below is preparation of trusted fixture input, not launcher discovery.

Refusals exit 2, emit exactly one stderr line `trusted-launch: refused: <code>`, and produce no operation output. Use dirty-environment, script-path, home-mismatch, cache-path, manifest-path, manifest-shape, fixture-root, uv-path, python-path, node-path, version-mismatch or invocation for the corresponding failed check. Version probes may run only after path checks; capture their output for validation rather than leaking it into hook stdout. Preserve underlying operation exit status after successful validation. A negative test must reach and assert its intended reason, rather than passing through an earlier refusal.

### Exec-form hook and migration

The installed Claude Code probe reports 2.1.300. Its embedded hook help and the [exec-form documentation](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form) establish command plus args without an outer shell. Retain that round-3 decision.

The managed PermissionRequest hook uses the following clean prefix, with absolute rendered host bindings and the parent-selected private cache and manifest. Each args element is one argument; paths containing spaces have no embedded shell quotes. CLAUDE_PROJECT_DIR is the documented host-substituted placeholder, and CLAUDE_ENV_FILE is explicitly empty. Do not assume exec form expands arbitrary environment variables.

```json
{"command":"/usr/bin/env","args":["-i","PATH=/usr/bin:/bin","HOME=<rendered passwd-home>","LANG=C.UTF-8","TERM=dumb","CLAUDE_PROJECT_DIR=${CLAUDE_PROJECT_DIR}","CLAUDE_ENV_FILE=","UV_CACHE_DIR=<private cache>","/bin/bash","--noprofile","--norc","-p","<abs trusted launch>","--manifest","<abs rendered production manifest>","permission-request"]}
```

A fixture uses the same form, substituting its rendered manifest operand and inserting `--fixture-root`, `<abs fixture root>` immediately before permission-request. Effective production settings must match the production form exactly and must not contain --fixture-root.

This starts no sh -c, bash -c, eval, command substitution or intermediate wrapper. The launcher constructs the verified uv/Python/permgate argv. Do not fall back to shell form when exec-form support is absent: stop for a reviewed amendment.

Exec form removes the extra outer-shell startup path. The hook host's own process environment and inherited loader inputs while starting /usr/bin/env remain residual until the host supplies a clean environment at exec or the P1-16 OS user boundary exists. Neither env -i, -p nor a launcher check retroactively closes that residual.

Replace the validator's literal permgate-claude substring rule with exact equality of the command string and ordered args array against the complete rendered canonical exec form, including --manifest. Both modify scripts use that same comparison for bound-form classification. Do not join args into a shell string, compare shlex tokens, normalize strings or discard quoting from legacy comparisons.

Refuse absent args, shell-form substitutes, missing, reordered or extra args, an altered manifest operand, production --fixture-root, --script, nonisolated Python, shim paths and shell suffixes. Retain ccgate refusal, hook order, duplicate detection, synchronous timeout budgets and onFailure block.

Classify the legacy managed form separately. Replace stale managed hooks once, preserve custom hooks and converge idempotently. Retain quote-preserving raw-string distinctions for legacy shell fixtures. Keep each surface's P1-15 event inventory; do not import live orchestrator settings or add an event to a surface that lacks it. Run the existing ClaudeSettingsMergeTest legacy/custom fixtures unchanged.

### Scoped entrypoint inventory

The render regression checks exact command/args, executes the hook as [command, *args] with shell=False, and resolves the executable and interpreter operands in actual invocations under PATH=/usr/bin:/bin.

- PermissionRequest: /usr/bin/env with the literal clean-prefix args, /bin/bash --noprofile --norc -p, the canonical launcher, --manifest and optional explicitly named fixture root, then permission-request. After manifest and binary validation the parent execs `<abs uv> run --no-config --no-project --isolated --offline --python <abs python> python -I <abs permgate> claude`, preserving hook stdin, stdout and exit status.
- Deployment: the same launcher, clean prefix, production manifest and verified uv/Python perform the explicit online seed below. Subsequent checker/generator commands use isolated offline uv/Python with cached --with pyyaml and the same private cache. The checker runs validate-agent-assets.py --check-effective-settings. Its generated-config child re-enters the same parent with the same manifest and runs `<abs uv> run --no-config --no-project --isolated --offline --with pyyaml --python <abs python> python -I <abs generator> --check` from the canonical repository cwd.
- Fixture subjects: the same launcher with the explicitly named fixture manifest and root, real uv/Python and unchanged permgate bytes, together with the generator, validator and both modify scripts. Every bound Python child uses -I. A child importing yaml uses the same offline --with pyyaml pattern after explicit fixture-cache provisioning.
- Formatter interpreter check: the same launcher validates the declared node and starts its verified realpath with the probed installed Prettier script. Makefile format PATH includes node's declared bin directory so its env-node shebang resolves.

Only canonical scoped invocations are accepted. PermissionRequest accepts its selector after the required manifest arguments and constructs the fixed command internally. Other scoped operations, including the seed, must match their exact bound argv. Arbitrary executable forwarding, caller-selected executable directories and alternate executable operands are forbidden.

Add --check-effective-settings as an opt-in mode and expose the concrete trusted launch in Makefile. Ordinary validate-agent-assets and render-check stay pure. The opt-in mode reads effective installed settings, requires their exact production wiring and manifest operand, and checks existence, regular/executable identity, canonical protected paths and exact declared versions before operation execution. It consumes checked realpaths without rediscovery. It does not silently create a manifest, provision a cache, install tools or retry online.

### Private cache and explicit online seed

The trusted parent supplies an absolute UV_CACHE_DIR: protected main-checkout .agents/worklog/uv-cache for orchestrator/deploy runs, launcher-supplied <worktree>/.uv-cache for workers, and a temporary cache for tests. Parent and child refuse absent or relative caches; children do not derive defaults.

Retain round 3's bound online-seed decision. The operator's deployment sequence is: make update and deterministic production-manifest preparation, explicit private-cache seed through the trusted parent, then the isolated offline deployment check. The worker does not perform live deployment.

Use this seed command, replacing placeholders with shell-quoted absolute bound operands and using the canonical repository cwd:

```text
/usr/bin/env -i PATH=/usr/bin:/bin HOME=<rendered passwd-home> LANG=C.UTF-8 TERM=dumb CLAUDE_PROJECT_DIR=<canonical repository root> CLAUDE_ENV_FILE= UV_CACHE_DIR=<private cache> /bin/bash --noprofile --norc -p <abs trusted launch> --manifest <abs rendered production manifest> <abs uv> run --no-config --no-project --isolated --with pyyaml --python <abs python> python -I -c "import yaml"
```

The parent performs the same entry, manifest, cache, uv and Python checks before the seed as before every other bound operation. It compares executable operands with its verified manifest paths and execs only the exact PyYAML-import argv. Relative to the offline PyYAML form, only --offline is omitted. Retain --no-config, --no-project, --isolated, --with pyyaml, --python <verified abs python> and python -I. The [uv command reference](https://docs.astral.sh/uv/reference/cli/#uv-run) supplies the option semantics.

Record the selected manifest's canonical path and SHA-256, the complete seed command with expanded bound paths, output and actual exit status in validation.md. Carry the seed status and evidence into acceptance. Propagate the seed's exit status. A failed seed blocks later offline deployment commands; none downloads or seeds implicitly.

The checker and its yaml-importing generator child use that same manifest and cache through the parent. Never substitute the resolver's base Python or sys.executable directly for the uv-provided PyYAML environment.

Record the actual positive deployment result from the operator's host after make update and manifest preparation. CI fixture execution does not substitute for that host result.

## Fixture and regression contract

### Real fixture-manifest execution on runners

The harness discovers real uv by inspecting shutil.which("uv"), rejecting a shims component before and after resolution, then searching the actual mise uv install root if needed. Prefer the pinned version's directory when present and use the newest exact installed version only as a harness fallback. Handle the probed platform subdirectory rather than assuming <version>/uv. Resolve sys.executable for real Python and reject shims. Record the discovery result, canonical identities and actual versions.

The harness renders a fixture manifest with exact declarations and versions for those real tools, then supplies that manifest through --manifest and the test's canonical temporary directory through --fixture-root. HOME remains the real uid's passwd home.

The fixture must satisfy exact relative-path composition and containment. If a discovered executable is outside the permitted home/fixture binding, materialize the real executable bytes and the Python runtime support needed for a working installation under the fixture root, using regular files rather than symlink bindings. Verify the copied executable bytes against their discovered sources and verify the staged interpreter actually runs with -I. Copy necessary runtime/stdlib files; do not replace Python with a wrapper or a fake executable. Preserve unchanged real permgate bytes under the fixture root.

The launcher sees only the declared fixture paths, validates them through the production code path and compares their actual versions with the fixture pins. Do not pass a runner's external absolute sys.executable as an unchecked exception, redirect production HOME, disable a check, or force the fixture through the production-only mise resolver.

Execute the rendered hook as [command, *args] with shell=False and a fake PermissionRequest payload. Substitute only the documented host placeholder. Require real uv, real isolated Python and unchanged real permgate, with no wrapper or fake on the positive path. Assert the expected permgate decision, not merely process startup or argv recording.

Plant .pth and usercustomize.py markers in a fake user site and assert neither executes. Include hostile uv.toml, .venv and startup/PYTHON* inputs. Confirm the supplied clean prefix and isolated invocation prevent their consumption without changing real user-site files or installations.

This fixture execution is required on CI runners with setup-uv and their ordinary Python installation; it does not require the production mise installation. There is no fixture-execution skip for missing production pins. Failure to discover or prepare real fixture tools is a failed or blocked check with its exact reason, never green evidence.

### Separate pinned-installation case

Add a separate test of the exact production manifest bindings on a host with the pinned mise installation. It must execute the real bound hook path without substituting fixture pins or accepting a fallback version.

Elsewhere, skip only this pinned-installation test with the named reason `pinned-installation-unavailable`, recording the missing exact installation paths. An existing symlinked, malformed, mismatched or otherwise invalid installation is a refusal/failure, not absence and not a skip. Record every such skip in validation.md and report.md. Obtain the real host result during operator deployment; a runner's required fixture execution remains separate.

### Named regressions

Add or extend these eight regressions in the real existing classes, recording the full selectors and running their unittest dotted equivalents red before implementation and green afterward:

- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_trusted_entrypoint_manifest_matches_mise
- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_every_bound_entrypoint_resolves_with_system_path
- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_permission_request_uses_real_isolated_uv
- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_permission_request_uses_pinned_installation
- tests/unit/test_claude_managed_settings.py::ClaudeManagedSettingsTest::test_trusted_entrypoint_consumers_migrate
- tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_bound_permission_request_structure
- tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_effective_settings_checks_binary_identity
- tests/unit/test_validate_agent_assets.py::ValidateAgentAssetsTest::test_trusted_launch_validates_manifest

The manifest/mise regression checks production declarations, deterministic manifest rendering and exact version equality with the read-only mise declaration. Fixture pins are tested against their actual fixture executables, not against production versions.

The system-PATH regression checks /usr/bin/env as the hook executable, the exact clean assignments before /bin/bash --noprofile --norc -p, the canonical launcher, required manifest operand and operation. Assert shell=False, no outer-shell invocation, and exact fixture-root argument placement when testing the fixture form.

The structure and migration regressions include a hostile CLAUDE_PROJECT_DIR value containing spaces and a -- word, such as `project path -- injected`. Host substitution must preserve one args element. Both bound classifiers compare the exact command string and ordered args array; splitting the value or joining args into a shell string must fail.

Retain the round-2 quoted/unquoted legacy shell fixture pair whose shlex tokens are equal. Refuse both as the active canonical hook and preserve their raw-string distinction during legacy classification. Preserve custom hooks, stale managed-form replacement and repeated-merge idempotence.

The manifest regression exercises the actual launcher with otherwise valid fixture bindings and covers:

- A regular manifest outside both the repository and named fixture root, refused with manifest-path before any declared binary executes.
- A sibling-prefix or symlink escape outside those roots, also refused with manifest-path.
- A missing, relative or duplicated --manifest operand, malformed manifest data and an invalid fixture-root operand, with their specific refusal codes.
- A valid regular fixture manifest under the explicitly named fixture root, proving the same path accepts its declared real uv/Python without the production mise installation.

The binary-identity regression uses that accepted fixture-manifest path to reach the intended binary check. Cover a declaration naming a shim, a symlinked binary pointing to a marker-writing fake uv, and a path under an explicitly forbidden worker-writable root. Assert exit 2, the specific uv-path or python-path refusal and absent marker. A prior manifest, HOME or missing-installation refusal does not cover these cases. Also cover an exact-version mismatch after valid path checks.

In a separate non-skippable seed subcase, place an argument-recording fake uv as a regular executable at the fixture's declared canonical path. Its --version response matches the fixture pin. Execute the actual seed launch through the parent with shell=False and --manifest/--fixture-root. Assert the complete /usr/bin/env -i … /bin/bash --noprofile --norc -p prefix, verified absolute uv/Python operands and the recorded argv:

```text
run --no-config --no-project --isolated --with pyyaml --python <abs python> python -I -c "import yaml"
```

The final import is one argument. Assert absence of --offline, the exact clean environment and absolute private UV_CACHE_DIR, and seed exit-status propagation. Missing or relative caches must refuse without executing fake uv. This case uses no network and is evidence of invocation and refusal behavior only.

Also seed a fixture private cache explicitly through the same parent and isolated seed argv with real bound uv/Python, then prove the generator child's exact offline --with pyyaml argv, shared cache and successful yaml import. An isolated base-Python-only child must not satisfy this assertion. Sandbox or network denial is reported as blocked, without an outside-sandbox retry.

The fake-uv refusal and seed-recording subcases are not positive hook or deployment evidence. Structural, migration, manifest-boundary, identity and seed-recording cases never depend on the pinned-installation skip.

Exercise design item 7's hostile PATH, hostile Git environment/configuration, worker-root path and validation-to-consumption replacement cases for the scoped mechanisms, using the common helper when available. Prove no planted payload executes and state the same-UID replacement residual honestly.

No guard/delivery/state-helper descendant migration, permgate policy/source change, dependency, workflow change or worker live deployment is authorized.

## Measurement and caps

Historical touched-function spans are renderer 88, validator 13+33+79+11+26=162 and orchestrator modify 8+12=20 lines. P1-15's inspected worker modify module is 63 lines: 88+162+20+63=333 existing touched lines. The launcher has a zero-line baseline because the probed path is absent: 333+0=333. Existing target test modules total 95+1781=1876 lines.

The P1-15 files are an unmerged worker-e snapshot, not accepted-base measurements. Remeasure on the dispatch baseline and record the actual spans and file totals before implementation.

Production allowance, counted as additions plus deletions, is manifest/template 50 + renderer and manifest serialization 80 + both modify scripts 100 + validator 190 + Makefile 40 + launcher including shared manifest parsing, containment, identity and hook/seed dispatch 160 + margin 10 = 630 changed lines.

Test allowance is real execution/rendering and fixture preparation 260 + migration 100 + validator identities/refusals 220 + pin/shape checks 70 + environment/node cases 90 + pre-exec symlink case 40 + hostile quoting case 20 + yaml-child/cache case 20 + exec-form hook case 10 + online-seed prefix/argv case 30 + manifest-boundary cases 80 + separate pinned-installation case 40 = 980 changed lines.

The re-plan therefore raises the production cap from 500 to 630 and the test cap from 800 to 980 for the explicitly named manifest and fixture work. Runtime manifest data is not an executable helper. Count any tracked runtime configuration as production rather than hiding it in evidence totals. Reports and review evidence are excluded. Do not raise a cap or omit a consumer: stop for another split.

## Check

Run make unit-test, make format, make validate-agent-assets and make render-check, the eight named regressions, and unchanged tests.unit.test_claude_settings_merge, tests.unit.test_generate_agent_configs, tests.unit.test_statusline_tools and tests.unit.test_herdr_agents. Do not run Bats locally.

Record exact commands, statuses, red/green commits, discovered and staged real-tool identities, manifest hashes, fixture results, the named pinned-installation skip or host result, and baseline failures in validation.md. A failed or blocked check is not green. CI must execute the real fixture-manifest hook case without the pinned mise installation; the pinned-installation case has its separate recorded outcome.

Measure git diff --numstat origin/main...HEAD: at most 630 changed lines outside tests/ and .orchestration/, and at most 980 under tests/. Include any production configuration placed elsewhere in the production total.

The orchestrator compares the dispatched copy and TASK SHA-256 and runs the accepted base's regime-ci.py --base <base40> --head <head40> --root <base-checkout> under the trusted Python prefix. Report any unverifiable-copy warning. Check C7b row units and any C11 closed-row selectors explicitly.

Before completion run make require-crit-review with read/resolved local agent evidence and its receipt, then use Playbook step 10 at integration. Neither drafting this text nor passing a fixture authorizes deployment or merging.

## Completion

Current bindings override the historical identifiers, paths, branch/PR and deletion instructions inside the following source quotation: create tools/trusted-entrypoint-binding-a01 and one new PR from the accepted dispatch baseline; all artifacts, PONG ids and task_copy bind to dotfiles-T133-trusted-entrypoint-binding-a01, no predecessor deletion is authorized, and the orchestrator creates dotfiles-T133-trusted-entrypoint-binding-followup-a01 before advisory dispositions. Preserve the full executable-binding finding history, the C-92 fixture-vs-binding re-plan and D-024-26. The source Completion is otherwise verbatim, with the requested advisory-owner substitution.

Report the production and fixture manifest identities separately. Include the real fixture-hook outcome, pinned-installation result or named skip, each manifest/binary refusal, quote-preserving comparison evidence and bound seed evidence. The operator's later deployment result remains a distinct acceptance item; do not claim it from CI.

> Bindings for this new task: create a fresh `tools/loop-limits-a01` branch and one new PR from the dispatched baseline; predecessor head is not applicable. All current artifact paths, task-copy hashes and PONG task ids bind to `dotfiles-T133-loop-limits-a01`. Keep the first push's task copy byte-identical; no predecessor deletion is authorized. The orchestrator creates `dotfiles-T133-trusted-entrypoint-binding-followup-a01` before dispositioning advisory rows. The quotation below preserves the source Completion verbatim except for the requested advisory-owner substitution; its historical PR, branch and predecessor bindings are superseded by this paragraph.
>
> One existing PR, #424, on `tools/ci-efficiency-followup-a02`, continuing from `67e2cc98`; the predecessor’s fresh-branch requirement is superseded. Keep its implementation, tests, commits and historical evidence. In the first a04 push delete `.orchestration/dotfiles-T133-ci-efficiency-followup-a02/task.md` and add `.orchestration/dotfiles-T133-ci-efficiency-followup-a04/task.md` byte-identically to the dispatched a04 text. That single predecessor-file deletion is the reset transition authorized by C3; do not rewrite or move the predecessor’s other evidence.
>
> Write current `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence under `.orchestration/dotfiles-T133-ci-efficiency-followup-a04/`. Record the predecessor head, exact final head and base, branch, PR, changed files, row-to-test mapping, red/green commits, cap totals, evidence paths and `task_copy=<sha256 of .orchestration/dotfiles-T133-ci-efficiency-followup-a04/task.md>`. Preserve historical claims as historical; they do not approve the new head.
>
> The inherited Completion rules apply with these explicit bindings: advisory P2 and P3 belong to `dotfiles-T133-trusted-entrypoint-binding-followup-a01`, with rows recorded by the orchestrator before disposition. Do not reopen that owner’s advisory work in this task unless a narrow revise explicitly authorizes it.
>
> Every fix round counts toward INV-6, including worker-side fixes before the first RESULT; C-61 permits at most two in this task, and amendments and questions retain their own counters. A rebase repair qualifies only under D-024-24 and cannot hide a security fix. Another repeated-class finding or exhausted counter stops work for the orchestrator’s recorded re-plan; do not continue under a new label.
>
> A P0/P1 surviving the permitted worker-side fix round is sent as `open:<id>` in the RESULT, including `open:review-<id>` for a review-body finding, with the applicable round count. It stops integration for the operator’s decision; never convert it into an advisory disposition or perform another unauthorized fix round.
>
> Wait for final-head CI and the bounded automatic Bot-review window. Record `bot: none` if the window expires. **Do not post `@codex review`**, at the ten-minute mark or after a fix. The orchestrator replies to and resolves GitHub review threads.
>
> Every `gh` command and every `git` write is an individual command **inside the sandbox**, including pushes and authenticated fetches. No compound write commands, outside-sandbox retries, excluded-command workaround, permission escalation or alternate tool to bypass a denial. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-ci-efficiency-followup-a04 status=blocked` naming the exact command, failure and crossed boundary; preserve the evidence and wait.
>
> The orchestrator performs final-head review and the security-profile review, then follows Orchestrator Playbook step 10 for CI, feedback sweep, task-level audit, finding dispositions, acceptance, gate and head-bound merge. The worker does not merge or remove workers.
>
> Implementation, runtime tests and CI are not claimed checked by this task draft; dispatch remains held on the stated prerequisites. Same-UID replacement and shared-credential risks remain residual.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
Not checked: implementation, runtime tests, CI, live dispatch or operator-host deployment.
Risk: pending prerequisites, same-UID replacement, shared credentials and inherited descendant bindings remain residual.
```

---
format: 2
task_id: dotfiles-T133-trusted-entrypoint-pins-a01
kind: code
security: true
allowed_files: ["home/dot_mise/config.toml","tests/unit/test_generate_agent_configs.py",".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**"]
after: []
threat_table:
  - {"control":"home/dot_mise/config.toml","disposition":"residual: Pin only uv, Python and node to the primary task's probed versions; this intentionally stops their latest-version tracking."}
  - {"control":"tests/unit/test_generate_agent_configs.py","disposition":"residual: Keep an exact source-manifest/rendered-command equality check and executable leaf/argument checks, plus explicit pin assertions; do not delete legacy fixture coverage."}
  - {"control":".orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/**","disposition":"residual: Only task copy and review/validation/report data are authorized; no helper or runtime code is placed here."}
  - {"control":"task copy .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/task.md","disposition":"residual: The orchestrator compares the full dispatched bytes and SHA-256 before accepting this prerequisite."}
  - {"control":"task metadata","disposition":"residual: This is an independent three-entry prerequisite task; it grants no write permission for the later binding implementation."}
  - {"control":"metadata separators","disposition":"residual: Parse as data with duplicate keys refused and compare the complete dispatched task copy."}
  - {"control":"in-process effects","disposition":"residual: Tests and fixture renders use temporary directories; no mise install, update, apply or live hook execution is authorized."}
  - {"control":"workflow and interpreter or environment inputs","disposition":"residual: The exact declaration is changed intentionally; trusted-entrypoint implementation remains in the primary task."}
  - {"control":"new or renamed scripts","disposition":"residual: None is authorized; retain existing generator and test helpers."}
  - {"control":"orchestrator effect merge","disposition":"residual: The orchestrator alone integrates after full final-head evidence and Playbook step 10."}
  - {"control":"orchestrator effect update-branch","disposition":"residual: A moved head requires refreshed checks and integration evidence under the orchestrator's control."}
  - {"control":"orchestrator effect forced worker removal","disposition":"residual: None is planned; the worker cannot remove seats or discard another worktree."}
  - {"control":"design 5.14 item 0 same-UID model","disposition":"residual: Exact pins do not separate OS identities or shared GitHub credentials."}
  - {"control":"design 5.14 item 1 protected inputs","disposition":"residual: The exact declaration becomes a trusted input; worker write protection remains pending until P1-15 is accepted and deployed."}
  - {"control":"design 5.14 item 2 clean environment","disposition":"residual: No new production execution path is introduced; inherited check launch trust is not established by a pin."}
  - {"control":"design 5.14 item 3 paths","disposition":"residual: The declaration path is fixed and unchanged; installation path validation belongs to the resolver and primary task."}
  - {"control":"design 5.14 item 4 verified bytes","disposition":"residual: Whole-task and final-head evidence are compared; local files remain replaceable by unrestricted same-UID processes."}
  - {"control":"design 5.14 item 5 identity","disposition":"residual: Use full head/base and task-copy SHA-256 in evidence; no new lock or reservation is created."}
  - {"control":"design 5.14 item 6 honest residuals","disposition":"residual: Pin assertions prove declarations only, not installed binary identity or successful hook execution."}
  - {"control":"design 5.14 item 7 verification","disposition":"residual: Run the pin regression red then green and retain generator/merge consumers; general hostile-execution closure is not claimed."}
  - {"control":"design 5.14 item 8 approval","disposition":"residual: Pins and local evidence are proposals until integration; neither grants permission or merge authority."}
  - {"control":"design 5.14 item 9 isolation","disposition":"residual: This task supplies exact version input only; the accepted resolver and primary task implement isolated execution and private caches."}
  - {"control":"design 5.14 item 10 sandbox","disposition":"residual: All commands stay in the sandbox; denied commands produce blocked evidence without escalation."}
premises:
  - {"command":"grep -nE '^(uv|python|node) = ' home/dot_mise/config.toml | paste -sd '|' -","output":"3:node = \"latest\"|5:python = \"latest\"|17:uv = \"latest\""}
  - {"command":"git ls-tree -r --name-only origin/main -- home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | paste -sd '|' -","output":"home/dot_mise/config.toml|tests/unit/test_generate_agent_configs.py"}
  - {"command":"wc -l .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py tests/unit/test_validate_agent_assets.py home/dot_mise/config.toml tests/unit/test_generate_agent_configs.py | xargs","output":"63 .claude/worktrees/worker-e/home/dot_claude-worker/modify_private_settings.json 95 .claude/worktrees/worker-e/tests/unit/test_claude_managed_settings.py 1781 tests/unit/test_validate_agent_assets.py 79 home/dot_mise/config.toml 2350 tests/unit/test_generate_agent_configs.py 4368 total"}
  - {"command":"grep -nE '^    def test_managed_hooks_use_installed_permgate_paths' tests/unit/test_generate_agent_configs.py | paste -sd '|' -","output":"1417:    def test_managed_hooks_use_installed_permgate_paths(self) -> None:"}
  - {"command":"sed -n '1417,1422p' tests/unit/test_generate_agent_configs.py | wc -l | xargs","output":"6"}
---

# AGMSG-TASK dotfiles-T133-trusted-entrypoint-pins-a01 — prerequisite split for exact tool pins

Worker: a Codex seat (worktree named at dispatch)

This is the second, separate task file, with exactly three allowed_files entries. Accept it before dispatching ci-efficiency-followup-a04 or the primary binding task. The primary task above contains the shared host probes and C-88 quotations; these bind the version choices here and do not authorize the primary implementation in this prerequisite.

Pin uv=0.13.1, python=3.15.0 and node=26.12.0 in home/dot_mise/config.toml, replacing only those latest values. Add one English comment explaining the trusted-entrypoint pins; preserve every other tool and setting. Do not install or apply anything.

In GenerateAgentConfigsTest add test_trusted_entrypoint_mise_versions_are_exact, red before the config change and green afterward. Refactor test_managed_hooks_use_installed_permgate_paths to compare the complete rendered PermissionRequest command with the real manifest declaration rendered through the existing template helper; retain exactly one managed entry, permgate executable-leaf/claude-argument checks and the Codex assertion. Keep synthetic legacy-command fixtures. The primary task adds strict bound-sequence and parent-selected-manifest validation.

Measured declaration: 79 lines; touched existing test: 6 lines at 1417–1422 in a 2350-line module. Source allowance is 3 additions+3 deletions+1 reason comment+1 margin=8 lines; fixture/assertion work 60+margin 20=80 test lines. Enforce these separate caps with git diff --numstat origin/main...HEAD; evidence is excluded, executable source is not.

Check: make unit-test, make format, make validate-agent-assets, make render-check, tests.unit.test_generate_agent_configs and the new pin regression. Do not run Bats locally. Use the primary task's accepted-checker and regime-copy checks for this task's own id/copy; report blocked or baseline-failing checks honestly.

Completion: create tools/trusted-entrypoint-pins-a01 and one PR; write task.md, report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review evidence under .orchestration/dotfiles-T133-trusted-entrypoint-pins-a01/. The primary task's quoted Completion round, sandbox, CI/Bot and integration rules apply with this task's own identifiers; no predecessor deletion is authorized. Advisory owner is dotfiles-T133-trusted-entrypoint-binding-followup-a01, created before disposition. Only the orchestrator integrates; no deployment is claimed.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
Not checked: implementation, runtime tests, CI or deployment.
Risk: the primary binding work and same-UID/shared-credential residuals remain.
```

## Orchestrator note (2026-10-21T08:31Z): the pins test moves with the command form

The pins PR (#449, head 28dde0f5) refactored `test_managed_hooks_use_installed_permgate_paths` to split the rendered PermissionRequest command with `rsplit(" ", 1)` and assert the permgate executable leaf and the `claude` argument; that assertion encodes the pre-binding shell form and raises ValueError on this task's `command: "/usr/bin/env"` plus `args` form (audit:28dde0f:1 of the pins lineage). `tests/unit/test_generate_agent_configs.py` is therefore in this task's allowed_files: the worker updates that test together with the command form, asserting the executable leaf and the `permission-request` operand from `args` instead of a split string, and keeps the exact-pins test green. Its former out_of_scope row read: "dotfiles-T133-trusted-entrypoint-pins-a01 removes the installed-template legacy literal pin without relaxing synthetic legacy migration cases"; that constraint still holds (the synthetic legacy migration cases stay unrelaxed), only the ownership of the file moved here.
