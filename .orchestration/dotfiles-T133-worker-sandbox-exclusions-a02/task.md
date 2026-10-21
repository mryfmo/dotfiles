---
format: 2
task_id: dotfiles-T133-worker-sandbox-exclusions-a02
reset_of: [dotfiles-T133-worker-sandbox-exclusions-a01]
kind: code
security: true
allowed_files:
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - scripts/validate-agent-assets.py
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_claude_settings_merge.py
  - .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/**
after: []
threat_table:
  - control: the predecessor copy .orchestration/dotfiles-T133-worker-sandbox-exclusions-a01/task.md (reset_of)
    disposition: "residual: the a01 worker committed nothing (implementation_commits=0 in its blocked PONG), so no a01 copy exists on any branch; the a02 copy at .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md is the only task copy of the lineage and regime-ci verifies the latest copy of a reset_of lineage against the text on main"
  - control: the PR edits home/dot_agents/agent-config.yaml
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_sandbox_exclusions_render_empty_for_all_os"
  - control: the PR edits home/.chezmoitemplates/claude-settings-managed.json
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_managed_sandbox_exclusions_are_empty_for_all_os"
  - control: the PR edits scripts/validate-agent-assets.py (the validator rejects a non-empty rendered excludedCommands list)
    disposition: "closed: tests/unit/test_generate_agent_configs.py::GenerateAgentConfigsTest::test_sandbox_validator_requires_empty_exclusions"
  - control: the PR edits tests/unit/test_generate_agent_configs.py
    disposition: "residual: real manifest rendering and validator mutations exercise the production paths; final-head CI and the independent audit check the assertions"
  - control: the PR edits tests/unit/test_claude_settings_merge.py
    disposition: "residual: the existing per-OS merge regression checks the committed template red then green; final-head CI and the task-level audit from main check its assertions"
  - control: the PR edits .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/**
    disposition: "residual: this directory contains task data and evidence only; the audit compares claims with commands, message ids and the final head"
  - control: the task copy (.orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md)
    disposition: "residual: the orchestrator compares the whole-file SHA256 and bytes with the dispatched text before acceptance"
  - control: the evidence records (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: command outputs and sandbox message ids are recorded without secrets or literal home paths and independently checked at acceptance"
  - control: task metadata (reset_of, kind, security, allowed_files, after, threat_table, premises)
    disposition: "residual: the consistency checker checks the dispatched front matter and acceptance compares the byte-identical task copy"
  - control: metadata separators
    disposition: "residual: YAML boundaries remain intact and the whole-file digest covers metadata, body and the final Checks block"
  - control: in-process effects
    disposition: "residual: importing PR-controlled generator or validator code can have unrelated effects; the task-level audit from main checks those effects"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: tooling and Git retain tool, configuration and inherited environment inputs; the worker sandbox confines execution and the task-level audit from main checks inputs and effects"
  - control: new or renamed scripts
    disposition: "residual: none are authorized; final-head path review checks that the change uses the existing generator, validator and test module"
  - control: orchestrator effect merge
    disposition: "residual: the orchestrator follows Orchestrator Playbook step 10 and merges only the audited head after the gate and required checks"
  - control: orchestrator effect update-branch
    disposition: "residual: a changed head requires fresh exact-head CI, feedback sweep and audit before the step 10 gate"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none is planned; normal removal refuses a dirty tree and any forced removal records discarded state in acceptance"
  - control: "design 5.14 item 0: 脅威モデル（D-024-21）"
    disposition: "residual: host controls limit accidents and prompt injection; same-UID credentials remain shared and detection in the next record PR is not prevention"
  - control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）"
    disposition: "residual: Codex authors this Claude-boundary change; other Claude write-boundary work remains with P1-15 and is not established by empty exclusions"
  - control: "design 5.14 item 2: 無害化した環境を最初に"
    disposition: "residual: Check isolates the unit-test processes only; other repository tooling stays in the worker sandbox and is checked by the task-level audit from main"
  - control: "design 5.14 item 3: 信頼パスの境界検査"
    disposition: "residual: no trusted-path resolver changes; final-head scope review detects accidental path changes but cannot prevent same-UID substitution"
  - control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す"
    disposition: "residual: task-copy bytes and the transported full head are compared at acceptance; local evidence remains susceptible to same-UID mutation"
  - control: "design 5.14 item 5: 出力と予約の同一性"
    disposition: "residual: transport and CI messages bind the full 40-hex head; no lock or physical-slot mechanism is changed"
  - control: "design 5.14 item 6: 正直な残余"
    disposition: "residual: sandbox.md separates Claude macOS sends 2827 and 2830, the Codex probe denial, rendering-only CI, unmeasured Linux Claude sandbox runtime owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01, and unapplied live seats"
  - control: "design 5.14 item 7: 検証"
    disposition: "residual: render and validator regressions are red then green and CI checks both rendered OS variants; this task adds no trusted-execution mechanism"
  - control: "design 5.14 item 8: 承認はコミット済み台帳から読む"
    disposition: "residual: this task changes no approval reader; permission approval and final-head evidence remain subject to the orchestrator's existing integration procedure"
  - control: "design 5.14 item 9: 私設キャッシュ"
    disposition: "residual: use the launcher's worker cache and pinned interpreter; no shared cache becomes a new orchestrator execution source"
  - control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）"
    disposition: "residual: empty-list tests check configuration; Claude sandboxed sends and the Codex sandbox denial record runtime evidence; Codex networking is a separate task, Linux runtime remains unmeasured, live seats retain the exclusion until apply, and permgate remains operator-owned"
premises:
  - claim: "The shared list has one entry, Linux adds three, both rendered branches contain exclusions, and T130's Herdr socket allowlist is present."
    command: |-
      /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I -c 'from pathlib import Path; m=Path("home/dot_agents/agent-config.yaml").read_text(); t=Path("home/.chezmoitemplates/claude-settings-managed.json").read_text(); a=m.split("    excludedCommands:",1)[1].split("    linux_excluded_commands:",1)[0]; b=m.split("    linux_excluded_commands:",1)[1].split("    filesystem:",1)[0]; print("shared="+str(a.count("\n      - "))+" linux_additions="+str(b.count("\n      - "))+" rendered_sites="+str(t.count("\"excludedCommands\""))+" herdr_socket="+str(".config/herdr/herdr.sock" in m))'
    output: |-
      shared=1 linux_additions=3 rendered_sites=2 herdr_socket=True
  - claim: "The existing rendering module ends with unittest.main(), and the validator still requires the old exact Linux seat-tool list."
    command: |-
      /usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I -c 'import ast; from pathlib import Path; p=Path("tests/unit/test_generate_agent_configs.py"); t=p.read_text(); c=next(n for n in ast.parse(t).body if isinstance(n, ast.ClassDef)); v=Path("scripts/validate-agent-assets.py").read_text(); print(str(p)+" class="+c.name+" unittest.main="+str(t.rstrip().endswith("unittest.main()"))+" validator_linux_exact="+str("Linux excludedCommands must match the exact seat-tool list" in v))'
    output: |-
      tests/unit/test_generate_agent_configs.py class=GenerateAgentConfigsTest unittest.main=True validator_linux_exact=True
---

# AGMSG-TASK dotfiles-T133-worker-sandbox-exclusions-a02 — empty every rendered sandbox exclusion list

Design 5.14 of .orchestration/plans/024-design-quality.md is frozen by D-024-29 and applies by reference under D-024-30; rely on items 0–10, implementing item 10's exclusion-list change here. Worker: Codex security profile, because the affected execution boundary is Claude's; this seat has no network and the orchestrator transports its committed head. Generation, lint and Makefile recipes are the repository's own tooling run inside the worker's sandbox (design 5.14 items 2, 7, 9 by reference, D-024-30).

## Item 1

INV-6 / plan 006 S2 reset: a01 took two amendments before implementation; this whole replacement is authored by another review-profile context.
Set both `claude.sandbox.excludedCommands: []` and `linux_excluded_commands: []`; retain both keys, removing every pattern including the Linux additions. Replace the exclusion-history comments with one English sentence recording T39's 2026-10-01 Herdr PermissionDenied, T130's addition of `$HOME/.config/herdr/herdr.sock` to allowUnixSockets, and the orchestrator's sandboxed Bash messages 2827 and 2830 on 2026-10-20.
Regenerate through `uv run --no-config --no-project --offline --python "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" --with pyyaml python -I scripts/generate-agent-configs.py`; both OS branches of the managed template must retain `"excludedCommands": []`. Do not hand-edit generated output or change the generator.
Replace the validator's old list policy with an empty-list rule for both OS variants: reject every non-empty list and malformed non-list, retaining the existing missing-key default. Preserve diagnostics exercised by unchanged validator tests (`macOS.*gh` and `Linux.*excludedCommands`) without exceptions to the empty-list rule.

## Item 2

In GenerateAgentConfigsTest add the three selectors named above: render the real manifest for darwin/linux and assert empty lists; render both committed template branches and assert empty lists; import the real validator by file path and exercise empty acceptance plus non-empty and malformed refusals on both OS variants. Include agmsg-dispatch, gh, git push, herdr-agents, actas-claim and an arbitrary pattern. Update existing exclusion expectations in this module; keep `unittest.main()` and use existing fixture helpers.
Update `tests/unit/test_claude_settings_merge.py::ClaudeSettingsMergeTest::test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging`: change the old exclusion-list assertion near line 591 to `[]` for Darwin and Linux; it must fail on the committed template before regeneration and pass after regeneration, preserving the other merge and idempotence assertions.
Every new behavior must have an assertion-based red result before implementation and green afterwards, with selectors and both outcomes in report.md; missing executables, imports or dependencies do not count as red. Keep fixture tool invocations runnable under the prescribed clean PATH through absolute installed tool paths, without widening PATH or adding dependencies.

The orchestrator pastes its own macOS Claude-sandbox measurement into the acceptance record: messages 2827 and 2830 of 2026-10-20, sent from sandboxed Bash, with exact commands, exit statuses, redacted outputs and message ids.
From sandboxed Bash run `agmsg-dispatch "$TEAM" "$WORKER" "$ORCHESTRATOR" "$ORCHESTRATOR_PANE" 'AGMSG-PONG v1 task_id=dotfiles-T133-worker-sandbox-exclusions-a02 status=working reason=sandbox-dispatch-probe'`, binding recipients from the dispatch envelope. In validation.md record the exact command, sandbox/runtime identity (`network_access=false`, no Unix-socket allowlist), exit code, verbatim redacted output and any message id actually returned. The prior Codex-sandbox measurement was Herdr-socket `PermissionDenied: Operation not permitted`; record this worker's measured result without requiring successful dispatch or a delivered PONG, and never retry outside the sandbox.
This probe records the Codex half of design 5.14 item 10; the manifest's `sandbox_workspace_write.network_access = true` is a separate task. No CI step launches a Linux Claude sandbox, so `agmsg-dispatch` runtime behavior there remains unmeasured by this task, a residual owned by follow-up task `dotfiles-T133-worker-sandbox-exclusions-followup-a01`.

## Check

Worker Playbook step 4 applies: every command runs inside the sandbox; record the expected Codex probe refusal in sandbox.md as measured state; for any other refusal record it in sandbox.md and send `AGMSG-PONG v1 status=blocked`; never retry outside.
Run before implementation and after, recording commands, exit statuses and verbatim redacted outputs:
`/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_generate_agent_configs.py`
`/usr/bin/env -i PATH=/usr/bin:/bin HOME="$HOME" TMPDIR="$TMPDIR" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_claude_settings_merge.py ClaudeSettingsMergeTest.test_modify_private_settings_renders_the_os_conditionals_for_the_host_os_before_merging`
Run `make render-check`, `make validate-agent-assets`, `ruff check --config ruff.toml scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py tests/unit/test_claude_settings_merge.py` and `ruff format --config ruff.toml --check scripts/validate-agent-assets.py tests/unit/test_generate_agent_configs.py tests/unit/test_claude_settings_merge.py`; no Bats locally.

Caps: at most 60 changed lines outside `tests/` and `.orchestration/`, and at most 120 under `tests/`.
Measure summed additions plus deletions with `git diff --numstat <base40>...<head40>`; base40 is pasted at dispatch and head40 comes from RESULT.
Before completion run `make require-crit-review` and follow AGENTS.md's agent-side crit-data procedure if required, saving -worker- evidence and receipt in the allowed task directory; no browser review. The whole task file, including the orchestrator's Checks paste, stays at or under **140 lines**; author lines stay at or under **132 lines**.

## Completion

Start a fresh branch with `git switch -c security/worker-sandbox-exclusions-a02 --no-track origin/main`. Save .orchestration/dotfiles-T133-worker-sandbox-exclusions-a02/task.md byte-identical to the dispatched text; in that directory write report.md (changes, named red/green outcomes, residuals, cost), validation.md (commands/output, exit codes, Codex-sandbox probe result, actual message ids, cap totals), sandbox.md, learning.md and autoskill.md (used or not-used). Maintain Codex seat plan/todo worklogs with at most one active todo per owner; do not commit plan/todo/learn. Include a cost: line with observed figures or n/a.
Commit locally, then send `AGMSG-PONG v1 status=working head=<40-hex>` with artifact paths. The orchestrator transports that exact head to github.com/mryfmo/dotfiles, creates the English PR, verifies exact-head Actions and the Worker Playbook step 15 Bot wait, then sends a PING binding head, PR URL and `ci=green` or failed checks. Fix in-scope failures through another committed head and transport cycle; the worker performs no network operation or merge.
Only after the orchestrator's matching-head `ci=green` PING send `AGMSG-RESULT v1 task_id=dotfiles-T133-worker-sandbox-exclusions-a02 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` and artifact paths.

Out of scope: permgate (operator-owned), Codex networking, other permission changes and live apply; Linux sandbox runtime measurement remains with `dotfiles-T133-worker-sandbox-exclusions-followup-a01`. The change reaches live seats only at the next `make update` after P1-14 a05 merges; until then worker seats retain the exclusion and task-level audits keep recording the existing P1.


Amendment 1 (`previous_sha256: 6f95aef556842405912d7a929d19b95ba95efaa8c2b0e61c72d1ae925e5cc7fc`): the Codex sandbox denies writes under `~/.cache/uv` (measured by a013 at 14:29Z: `Operation not permitted`), so every uv invocation of this task uses a fresh private cache seeded from the read-only default cache: once per session run `UV_CACHE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/uv-cache-wse-a02.XXXXXX")"; case "$UV_CACHE_DIR" in /*) ;; *) echo refused: UV_CACHE_DIR not absolute; exit 1;; esac; chmod 0700 "$UV_CACHE_DIR"; cp -R "$HOME/.cache/uv/." "$UV_CACHE_DIR/"; export UV_CACHE_DIR` and paste the commands, `ls -ld "$UV_CACHE_DIR"`, `du -sh "$UV_CACHE_DIR"` and the exit codes into validation.md (mktemp creates a new directory with a random suffix and mode 0700, so no pre-existing path or symlink is reused); the exported variable then reaches every prescribed `uv run` and every `make` target that invokes uv (Makefile line 189) in the same shell; a copy that fails or a cache without `pyyaml` is reported as `AGMSG-PONG v1 status=blocked`, never worked around online. Interference by another process of the same UID with the copied entries remains the residual of design 5.14 item 9 that the a01 and a06 lineages record (no host isolation claimed).
## Checks (pasted by the orchestrator before each send)