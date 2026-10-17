---
format: 2
task_id: dotfiles-T130-claude-sandbox-integration-a01
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - scripts/generate-agent-configs.py
  - scripts/validate-agent-assets.py
  - home/.chezmoitemplates/claude-settings-managed.json
  - home/dot_mise/config.toml
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_validate_agent_assets.py
  - tests/unit/test_claude_settings_merge.py
  - tests/unit/test_statusline_tools.py
  - home/dot_claude/modify_private_settings.json
  - tests/unit/test_supply_chain_policy.py
  - .orchestration/dotfiles-T130-claude-sandbox-integration-a01/**
after: []
threat_table:
  - control: "the PR changes home/dot_agents/agent-config.yaml (claude.sandbox: the per-OS Mach allowlist, extra_allow_write, allowedDomains, excludedCommands; claude.permissions.ask; the settings env map)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::test_claude_sandbox_renders_per_os_from_the_manifest"
  - control: "the PR changes scripts/generate-agent-configs.py (render_claude_sandbox and render_claude_settings emit the macOS and Linux variants as chezmoi conditionals)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::test_claude_sandbox_renders_per_os_from_the_manifest"
  - control: "the PR changes scripts/validate-agent-assets.py (validate_claude_sandbox and validate_claude_settings refuse the four forms of item 6 on each OS rendering)"
    disposition: "closed: tests/unit/test_validate_agent_assets.py::test_claude_sandbox_validator_refuses_each_forbidden_form"
  - control: "the PR changes home/.chezmoitemplates/claude-settings-managed.json (the rendered managed settings, applied by chezmoi into ~/.claude/settings.json at the operator's make update)"
    disposition: "residual: never hand-edited: make render-check regenerates it from the manifest and fails on any difference in CI; the validator parses both OS renderings; the live apply is the operator's step after the merge, outside this task"
  - control: "the PR changes home/dot_mise/config.toml (one line: github:shuntaka9576/blocc pinned to a version read from a pasted lookup instead of latest)"
    disposition: "residual: the version string is pasted command output in the validation file; mise install runs only at the operator's make update after the merge; no other tool entry changes"
  - control: "the PR changes tests/unit/test_generate_agent_configs.py (the per-OS rendering test and the updated assertions on ask and excludedCommands)"
    disposition: "residual: the tests render the template for darwin and linux and assert each list by value; the audit reads each case against items 2 to 5"
  - control: "the PR changes tests/unit/test_validate_agent_assets.py (one case per forbidden form of item 6, each failing the validator)"
    disposition: "residual: fixtures are manifests built in the test; the audit reads each case against item 6"
  - control: "the PR may change tests/unit/test_claude_settings_merge.py (only where it parses the raw template as JSON, which the OS conditionals break; it renders instead)"
    disposition: "residual: no assertion weakens; the diff is read by the audit against the current file"
  - control: "the PR may change tests/unit/test_statusline_tools.py (only where its four methods parse the raw template with json.loads; they render the template for the host OS first; Amendment 1)"
    disposition: "residual: no assertion weakens; the diff is read by the audit against the current file"
  - control: "the PR changes home/dot_claude/modify_private_settings.json (the chezmoi modify script that merges the managed template into ~/.claude/settings.json: it renders the two OS conditionals for the host OS before json.loads, and merges the env map key by key, existing keys preserved and the managed values winning; nothing else changes; Amendments 1 and 2)"
    disposition: "closed: tests/unit/test_claude_settings_merge.py::test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging"
  - control: "the PR changes tests/unit/test_supply_chain_policy.py (only test_mise_tools_track_latest_behind_the_cooldown: the existing held map gains github:shuntaka9576/blocc at exactly 0.6.0 with its reason; every cooldown assertion and every other latest assertion stays; Amendment 4)"
    disposition: "residual: one map entry and its reason; the diff is read by the audit against the current file, and the test keeps failing for any other tool that leaves latest"
  - control: "the live ~/.claude/settings.json env map as data the modify script must not lose (a user's own provider, proxy or runtime entries beside the four managed values; Amendment 2)"
    disposition: "closed: tests/unit/test_claude_settings_merge.py::test_modify_private_settings_keeps_the_existing_env_entries_and_lets_the_managed_values_win"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T130-claude-sandbox-integration-a01/ (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the seat could not run; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests import the renderer and the validator as the existing tests do and render text; nothing writes ~/.claude/settings.json or runs chezmoi apply; the live settings change only at the operator's make update after the merge"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow, interpreter or environment file is in allowed_files; make render-check and make unit-test run in the existing test workflow under the repository's python; the settings env map is rendered data, not an executed input"
  - control: new or renamed scripts
    disposition: "residual: none; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: origin/main has no Mach-service allowlist in the manifest, the renderer or the rendered settings, so item 2 adds one
    command: for f in home/dot_agents/agent-config.yaml scripts/generate-agent-configs.py home/.chezmoitemplates/claude-settings-managed.json; do printf '%s %s\n' "$f" "$(git show origin/main:$f | /usr/bin/grep -c allowMachLookup)"; done
    output: |-
      home/dot_agents/agent-config.yaml 0
      scripts/generate-agent-configs.py 0
      home/.chezmoitemplates/claude-settings-managed.json 0
  - claim: neither the renderer nor the rendered settings template branches on the OS today, so the per-OS output of item 1 is new
    command: for f in scripts/generate-agent-configs.py home/.chezmoitemplates/claude-settings-managed.json; do printf '%s %s\n' "$f" "$(git show origin/main:$f | /usr/bin/grep -c 'chezmoi\.os')"; done
    output: |-
      scripts/generate-agent-configs.py 0
      home/.chezmoitemplates/claude-settings-managed.json 0
  - claim: blocc is installed at latest on origin/main, the only mise entry without a pinned version that item 3 changes
    command: git show origin/main:home/dot_mise/config.toml | /usr/bin/grep -n blocc
    output: |-
      42:"github:shuntaka9576/blocc" = { version = "latest", os = ["linux/x64"] }
  - claim: the managed settings render an empty ask list and one test pins it empty, so item 4 updates that test
    command: 'printf ''%s\n'' "$(git show origin/main:home/.chezmoitemplates/claude-settings-managed.json | /usr/bin/grep -c ''"ask": \[\]'')" "$(git show origin/main:tests/unit/test_generate_agent_configs.py | /usr/bin/grep -c ''claude\["permissions"\]\["ask"\]'')"'
    output: |-
      1
      1
  - claim: pypi.org and files.pythonhosted.org are not allowed sandbox domains on origin/main, so uv fetches fail inside the Claude sandbox until item 3 adds them
    command: git show origin/main:home/dot_agents/agent-config.yaml | /usr/bin/grep -cE 'pypi\.org|files\.pythonhosted\.org' || true
    output: |-
      0
---

# AGMSG-TASK dotfiles-T130-claude-sandbox-integration-a01 — the Claude Code sandbox lets the seats' tools work inside it (one PR)

Written 2026-10-17 by the orchestrator seat from the operator's directive of 2026-10-17 21:0x JST (one batch, approved by the operator). Basis stated in the directive: the transcript study since 2026-10-14 found the in-sandbox failures of Claude seats to be the x509 OSStatus -26276 of gh and chezmoi (75 calls), mise TLS (11), cafe.github.com, gh's telemetry host (64), pypi.org (26; 64 in spark), mise writes EPERM, spark's herdr.sock EPERM (85) and gh 401 on Linux; 2,891 re-runs with dangerouslyDisableSandbox. Codex seats are unaffected: their network policy already allows com.apple.trustd.agent. Worker: the Codex seat codex-standard-dot-a004 (worker-e), named by the directive; the Claude seats are excluded because they run inside the sandbox this PR changes (a seat never edits its own execution boundary, Orchestrator Playbook step 3). The seat keeps its standard profile because the directive names it; the task-level audit on the audit profile and the Codex Bot's security review cover the trust-boundary review.

## Goal

After the operator's `make update` and seat restart (not this task), a Claude seat's sandboxed Bash runs `gh`, `chezmoi`, `mise`, `uv` and the agmsg scripts without leaving the sandbox on macOS, and without the gh keyring and herdr socket failures on Linux; every relaxation is named in the manifest, rendered per OS, and refused by the validator when it widens beyond the directive's list.

## Files (the directive's items 1 to 6)

1. Source of truth and rendering: `home/dot_agents/agent-config.yaml` (`claude.sandbox`, `claude.permissions`, the settings `env` map; add the key to the manifest and the renderer when absent) -> `scripts/generate-agent-configs.py` (`render_claude_sandbox`, `render_claude_settings`) -> `home/.chezmoitemplates/claude-settings-managed.json` -> `scripts/validate-agent-assets.py`; tests in `tests/unit/test_generate_agent_configs.py`. The rendered template carries the macOS and Linux variants as chezmoi conditionals (`{{ if eq .chezmoi.os "darwin" }} … {{ else }} … {{ end }}`) inside the JSON, so one template renders a valid settings document on each OS; `make render-check` keeps passing; the validator renders the template once per OS value and checks each rendering; any test that parses the raw template with `json.loads` renders it first (`tests/unit/test_claude_settings_merge.py` only where it does so; the four methods of `tests/unit/test_statusline_tools.py` likewise, Amendment 1). `home/dot_claude/modify_private_settings.json`, the chezmoi modify script that merges the managed template into the live `~/.claude/settings.json`, renders the two OS conditionals for the host OS (`darwin` or `linux`, from the chezmoi data it already receives or `platform.system()`) before its `json.loads`, and nothing else in it changes; one test in `tests/unit/test_claude_settings_merge.py` runs it for both OS values (Amendment 1).
2. macOS only: the sandbox network allows the Mach service `com.apple.trustd.agent` and nothing else; the manifest holds the explicit allowlist and the validator fails on any Mach service outside it. `com.apple.sysmond` joins only with a pasted live demonstration in the validation file that `pgrep` fails under the sandbox without it and works with it; otherwise it stays out and the report says so. VERIFY first, with WebFetch of code.claude.com/docs/en/sandboxing (quote the sentence in the validation file): the exact settings key for the Mach-service allowlist (the directive names `network.allowMachLookup`); if the documented key differs, use the documented one; if no such key exists, stop and send `AGMSG-PONG v1 status=blocked` with the quote. `filesystem.extra_allow_write` gains `~/.local/state/mise`, `~/Library/Caches/mise` and `~/.local/share/uv` (macOS rendering; the Linux rendering gains the two that exist there, `~/.local/state/mise` and `~/.local/share/uv`).
3. Both OSes: `network.allowedDomains` gains `pypi.org` and `files.pythonhosted.org` (not `registry.terraform.io`: spark's `terraform init` is not this repository's case). `home/dot_mise/config.toml` pins `github:shuntaka9576/blocc` to a fixed version instead of `latest` (the version read from a pasted lookup: `gh api repos/shuntaka9576/blocc/releases/latest --jq .tag_name`, or the releases page through WebFetch; never `gh release view`, which permgate refuses), so mise no longer queries mise-versions.jdx.dev; the supply-chain policy test `test_mise_tools_track_latest_behind_the_cooldown` records this one tool in its existing held map at exactly `0.6.0` with the reason (an exact pin is stricter than cooldown-latest and removes the registry query from the sandbox), every other assertion of that test unchanged (Amendment 4). The settings `env` map gains `GH_TELEMETRY=false`, `DO_NOT_TRACK=1`, `CHECKPOINT_DISABLE=1`, `AWS_EC2_METADATA_DISABLED=true`; the modify script merges `env` key by key into the live settings (every existing key preserved, the four managed values winning on their keys) instead of replacing the map, with one regression test for a live `env` holding other entries (Amendment 2). `cafe.github.com`, `datadoghq.com`, `checkpoint-api.hashicorp.com` and `api.anthropic.com` are not allowed (item 6 refuses them).
4. `claude.permissions.ask` gains gh's write operations as prefix rules: `Bash(gh pr merge:*)`, `Bash(gh pr create:*)`, `Bash(gh pr comment:*)`, `Bash(gh pr review:*)`, `Bash(gh pr close:*)`, `Bash(gh pr edit:*)`, `Bash(gh pr update-branch:*)`, `Bash(gh issue:*)`, and `gh api` with `-X`/`--method` `POST`, `PATCH`, `PUT`, `DELETE` or with `-f`/`-F` in every prefix form a rule can express (`Bash(gh api -X POST:*)`, `Bash(gh api --method POST:*)`, `Bash(gh api -f:*)`, `Bash(gh api -F:*)`, and so on). A flag after the path escapes a prefix rule; keep that limit as one `shortcut:` comment in the manifest (the integration gate remains the authority, as the SKILL says of the deny rules). The existing deny list, `Bash(gh release:*)` included, stays. `test_managed_claude_sandbox_excludes_agmsg_dispatch` and every other test that asserts `ask == []` is updated to the rendered list.
5. Linux only: `excludedCommands` gains `gh` and the top-level command that performs the seat claim and the herdr socket calls, `herdr-agents` (Amendment 3: the claim script `actas-claim.sh` runs inside `herdr-agents`, lines 655-656, and the documented matching reads only the top-level command's first word, so a nested-script entry is ineffective; the direct form `actas-claim.sh` stays listed only if the documented first-word matching reaches it, else it is dropped with the quote), by the first word Claude Code matches (VERIFY in the sandboxing page how excludedCommands matches a command; if the existing `agmsg-dispatch` entry does not match calls with arguments, correct its form the same way), because bubblewrap closes AF_UNIX and D-Bus (the gh 401 and herdr.sock EPERM). The Linux exclusion list is exactly `agmsg-dispatch`, `gh`, `herdr-agents` and, if kept, `actas-claim.sh`, and item 6's validator fails on any other entry; the permission rules still govern an excluded command (no allow rule is added for `herdr-agents`). `allowAllUnixSockets` is not used. The macOS rendering keeps `excludedCommands` at `agmsg-dispatch` only. One regression test renders the Linux settings and asserts the list by value, with the manifest comment naming the real invocation (`herdr-agents` → `actas-claim.sh`).
6. The validator fails when: the macOS rendering excludes `gh`; a Mach service outside the manifest allowlist is rendered; a telemetry or metadata domain (`cafe.github.com`, any `datadoghq.com` host, `checkpoint-api.hashicorp.com`, `api.anthropic.com`) is allowed; `allowAllUnixSockets` is true. One test case per form in `tests/unit/test_validate_agent_assets.py::test_claude_sandbox_validator_refuses_each_forbidden_form`, each a manifest built in the test that fails with the validator's message; `tests/unit/test_generate_agent_configs.py::test_claude_sandbox_renders_per_os_from_the_manifest` renders the template for `darwin` and `linux` and asserts each OS's Mach allowlist, allowWrite extras, allowedDomains, excludedCommands, ask list and env map by value.

## Out of scope

The follow-up PR of the directive's item 7 (a lint turning `diff <(…)` into temporary files, `$TMPDIR` in tests and agmsg `storage.sh`, contextdb out of `.claude/`, `ps` to `pgrep`, the Codex local review under a narrow exclusion): a separate task after this PR merges. `make update`, seat restarts and the live check: the operator's steps after the merge, never run from this task. permgate (`home/dot_agents/permgate-policy.yaml`, `executable_permgate`): untouched. `codex.sandbox_workspace_write.writable_roots`: untouched (it also renders into Claude's allowWrite; the extras go into `claude.sandbox.filesystem.extra_allow_write`).

## Check

`make render-check`, `make validate-agent-assets`, `uv run python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets tests.unit.test_claude_settings_merge -v` green, pasted in the validation file with `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and `.orchestration/` excluding `home/.chezmoitemplates/claude-settings-managed.json` (rendered output, regenerated by `make render-check`), and 1000 added lines under `tests/` (INV-2). The two VERIFY quotes (the Mach allowlist key, the excludedCommands matching rule) are in the validation file with their URL and fetch time.

## Completion

One PR from a fresh branch off `origin/main` (no other merge is a precondition; the #388 branch stays in the worktree for its own rounds). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2`, stops the PR and goes to the operator as a decision; a P2 of the Bot's first review on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50; every fix round counts toward INV-6's cap of two, C-61); the third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59); a later review's P2 and every P3 are advisory (C-61), as is any other P2, owned by `dotfiles-T130-claude-sandbox-integration-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T130-claude-sandbox-integration-followup-a01` in this task's acceptance record. The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T130-claude-sandbox-integration-a01/task.md>` and the evidence paths.

## Amendment 1 (round 1, 2026-10-17T12:4xZ)

a004's two scope questions (PONGs 12:41:02Z and 12:41:21Z), both authorized: `tests/unit/test_statusline_tools.py:33` parses the raw template with `json.loads` in four methods, so it renders the template for the host OS first, with no assertion removed; `home/dot_claude/modify_private_settings.json:46-47,187-188` reads the raw managed template, replaces sourceDir and homeDir and parses it, so the OS conditionals would break the real `chezmoi apply`: the file joins `allowed_files` (a Claude-boundary file, Codex-routable by Orchestrator Playbook step 3) for the narrow change of item 1, rendering the two OS conditionals for the host OS before `json.loads`, with one test for both OS values. Two threat rows added; nothing else changes.

## Amendment 2 (round 1, 2026-10-17T12:5xZ)

a004's security review (PONG 12:48:40Z): `merge_settings` in `home/dot_claude/modify_private_settings.json` replaces the whole existing `env` map with the four managed values, so a user's unrelated provider, proxy or runtime entries (the reviewer reproduced the loss of `CUSTOM_RUNTIME_MARKER` and `ANTHROPIC_BASE_URL`) would disappear at `chezmoi apply`: a data-loss regression the task's "nothing else changes" would have frozen. Authorized: the narrow key-by-key `env` merge (existing keys preserved, the four managed values win on their keys) and one regression test in `tests/unit/test_claude_settings_merge.py`, named in the new threat row above; item 3 says so. Nothing else changes.

## Amendment 3 (round 1, 2026-10-17T13:0xZ)

The Bot's review 5557862602 of PR #392 (head a06f646f), P1 thread 4302738193: the Linux `actas-claim.sh` exclusion never matches, because the claim script is launched inside `herdr-agents` (its lines 655-656) and the documented matching reads only the top-level command's first word (a004's quote). Decided: item 5 names `herdr-agents` as the Linux excluded command (the top-level command of the claim and of the herdr socket calls), keeps `actas-claim.sh` only if the documented matching reaches a direct invocation, bounds the Linux list exactly (item 6's validator fails on any other entry), adds no allow rule, and adds one regression test on the rendered Linux list. This is the one worker-side P0/P1 fix round of the Completion clause; nothing else changes.

## Amendment 4 (round 1, 2026-10-17T13:1xZ)

a004's blocked PONG (13:13:05Z): CI run 39034585900 fails `tests/unit/test_supply_chain_policy.py::test_mise_tools_track_latest_behind_the_cooldown` at line 379 (`latest` expected, `0.6.0` found for `github:shuntaka9576/blocc`), a file outside `allowed_files`. The directive's exact pin and the policy test's cooldown-latest rule meet here; an exact pin is the stricter of the two and removes the registry query, so the test's existing held map gains this one tool at exactly `0.6.0` with its reason, and nothing else in the test changes. The file joins `allowed_files` with its threat row; item 3 says so. The sole P1 fix round (Amendment 3) continues on the same head sequence.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T130-claude-sandbox-integration-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
premise 4: OK
premise 5: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T130-claude-sandbox-integration-a01.md
```
