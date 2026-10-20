---
format: 2
task_id: dotfiles-T133-pre-send-check-a01
kind: code
security: false
allowed_files:
  - scripts/orchestrator/pre-send.sh
  - tests/unit/test_pre_send.py
  - .orchestration/dotfiles-T133-pre-send-check-a01/**
after: []
threat_table:
  - control: the PR edits scripts/orchestrator/pre-send.sh
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_all_refusals_are_reported"
  - control: the PR edits tests/unit/test_pre_send.py
    disposition: "residual: temporary fixtures exercise the real preflight and checker; final-head CI and the task-level audit verify the assertions"
  - control: the task-file copy (.orchestration/dotfiles-T133-pre-send-check-a01/task.md)
    disposition: "residual: byte-identical to the dispatched text; the orchestrator compares its SHA256 with the TASK line at acceptance"
  - control: the evidence records under .orchestration/dotfiles-T133-pre-send-check-a01/** (report.md, validation.md, sandbox.md, learning.md, autoskill.md)
    disposition: "residual: records contain command output and learning triage; sandbox.md lists refused commands, and the audit checks claims against the final head"
  - control: task metadata (kind, security, allowed_files, after, threat_table, premises)
    disposition: "residual: the consistency checker reads the front matter before dispatch and at acceptance; byte comparison detects a changed task copy"
  - control: metadata separators (the --- boundaries in the task copy and evidence records)
    disposition: "residual: front matter remains YAML; the checker parses the task and byte comparison covers the entire dispatched file"
  - control: in-process effects
    disposition: "closed: tests/unit/test_pre_send.py::PreSendTest::test_fenced_bash_syntax"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file changes; isolated Python and no-config offline uv use the pinned interpreter, while same-UID cache mutation remains possible"
  - control: new or renamed scripts
    disposition: "residual: the sole new script is scripts/orchestrator/pre-send.sh; shdoc, shellcheck and shfmt cover it, and no other script is added or renamed"
  - control: orchestrator effect merge
    disposition: "residual: gh pr merge --squash --match-head-commit <audited head> follows the gate under Orchestrator Playbook step 10; no local merge or push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, requiring fresh final-head CI, feedback sweep and audit before the gate under Orchestrator Playbook step 10"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty tree without --force, and any forced removal records discarded state in acceptance"
premises:
  - claim: "The local glue has 39 lines, both target files are absent, and the checker and validator already exist; promotion needs no dependency or caller change."
    command: |-
      python3 -I -c 'from pathlib import Path; p=Path(".agents/worklog/orchestrator-glue/pre-send.sh"); print("glue lines:", len(p.read_bytes().splitlines())); print("new paths absent:", all(not Path(x).exists() for x in ("scripts/orchestrator/pre-send.sh", "tests/unit/test_pre_send.py"))); print("dependencies present:", all(Path(x).is_file() for x in ("scripts/orchestrator/task-consistency-check.py", "scripts/validate-agent-assets.py")))'
    output: |-
      glue lines: 39
      new paths absent: True
      dependencies present: True
  - claim: "The glue's root depth, floating interpreter and missing --no-config must change when promoted."
    command: |-
      sed -n '7,9p' .agents/worklog/orchestrator-glue/pre-send.sh
    output: |-
      root=$(cd "$(dirname "$0")/../../.." && pwd)
      PY=$HOME/.local/share/mise/installs/python/latest/bin/python3
      uv run --no-project --offline --python "$PY" --with pyyaml python -I "$root/scripts/orchestrator/task-consistency-check.py" "$f" || { echo "checker: refused"; rc=1; }
---

# AGMSG-TASK dotfiles-T133-pre-send-check-a01 — promote the final-byte task preflight

Written 2026-10-20 after M-20261020-01 (a refused string survived in an amendment note), M-20261020-03 (dispatch followed a failed edit), and C-102 (owner sections must exist and carry work). Read those records in .orchestration/learning/ and the untracked 39-line glue at `$HOME/Workspace/dotfiles/.agents/worklog/orchestrator-glue/pre-send.sh` (read-only reference, absent from origin/main). This task supplies a reusable preflight; the loop-limits lineage later calls it from dispatch.sh --next and owns amendment-hash/failed-edit dispatch control.

Design 5.14 (.orchestration/plans/024-design-quality.md), frozen by D-024-29, applies by reference under D-024-30: rely on items 0 (threat model), 2 (clean environment and isolated Python), 4 (checked contents and digest), 6 (honest residuals), 9 (no-config/offline pinned interpreter), and 10 (sandbox-only commands); this security:false preflight detects mistakes and does not establish a hostile same-UID trust boundary.

## Item 1

Promote the glue into executable scripts/orchestrator/pre-send.sh, adapting repository-root lookup to its new location (two parents). It accepts exactly one task-text path and never edits it or executes its prose. Use English shdoc comments with @file, @brief, @description, @arg and @exitcode. Implement these checks on the final task bytes, including front matter, notes and the Checks block:

- Consistency: run `uv run --no-config --no-project --offline --python "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" --with pyyaml python -I "$root/scripts/orchestrator/task-consistency-check.py" --root "$root" "$task"`; a nonzero result is a refusal, including tool/dependency failure.
- Secret pattern: extract and compile only the SECRET_PATTERN assignment from scripts/validate-agent-assets.py, as the glue does, rather than importing its unrelated module-level initialization; never copy the regex. Scan every line; report matching line numbers/counts without echoing matched material. Run the standard-library helper with the same pinned Python and -I.
- Literal homes: refuse macOS and Linux home-directory literals, including a home name without a trailing slash; allow $HOME and <home>.
- Self cap: recognize both `at or under **N lines**` and `at or under N lines` with numeric N; compare with `wc -l`, refuse above the cap, accept equality, and allow a text without a self cap.
- Shell syntax: run `/bin/bash -n` on every fenced bash block, including later blocks after an earlier failure; never execute a block.
- Owner work: when the text reads `## Owned by <self>` from a named record, self means its task_id and relative record paths resolve from the repository root. Require that exact section in that record, bounded by the next level-two heading. With at most one `## Item` heading require at least one nonempty `<id>\t<class>` row or `- ` bullet inside the section; with additional Items an empty existing section is allowed. A missing record or section always refuses.
- Completion: run all applicable checks despite refusals; exit 0 only when all pass, otherwise 1, with one single-line named reason per failed check. For readable input, including refused input, print `sha256: <64 lowercase hex>` last on stdout, hashing the unchanged file bytes. Argument/read failures exit 1 with a named reason.

## Item 2

Add tests/unit/test_pre_send.py using unittest, TemporaryDirectory, fixture task texts and records, ending with `unittest.main()`. Exercise the real preflight and consistency checker without network access or changes to live records. Write and run all new tests before creating the script: each new behavior must be red then green, named with both outcomes in report.md; refusal assertions require exit 1 and their named diagnostic so a missing script cannot pass them. Construct refused secret/home fixtures from fragments and redact evidence rather than committing forbidden literal examples.

Use PreSendTest methods: test_consistency_refusal; test_secret_pattern_matches_validator (independently extract the validator assignment and compare matching fixture lines/counts, including a non-match and a hit in the final Checks block); test_literal_home_refusal (both platforms); test_self_cap (both spellings, equal, over, absent, and wc newline counting); test_fenced_bash_syntax (multiple blocks, later syntax failure, and a valid side-effect sentinel that must never execute); test_owner_section_and_rows (missing record/section even with another Item, empty sole Item, each row form, rows outside the section, and empty section with another Item); test_all_refusals_are_reported (simultaneous failures still yield each named reason and the last digest); test_passes_and_prints_final_sha256 (a valid task, exit 0, exact hashlib digest of its final bytes). Cover argument/read refusals in test_input_refusal. No fixture source duplicates SECRET_PATTERN.

## Check

Worker Playbook step 4: every command runs inside the sandbox; any boundary refusal is recorded in sandbox.md and sent as `AGMSG-PONG v1 status=blocked`, never retried outside. Run the module before implementation and after, pasting commands, exit statuses and verbatim redacted output into validation.md:

`/usr/bin/env -i PATH="$(dirname "$(command -v uv)"):/usr/bin:/bin" HOME="$HOME" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I tests/unit/test_pre_send.py`

Run `bash -n scripts/orchestrator/pre-send.sh`, `shellcheck -x scripts/orchestrator/pre-send.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/pre-send.sh`, `ruff check --config ruff.toml tests/unit/test_pre_send.py` and `ruff format --config ruff.toml --check tests/unit/test_pre_send.py`. Caps: at most 90 changed lines outside `tests/` and `.orchestration/`, and at most 220 under `tests/`. The caps are measured as summed additions plus deletions in `git diff --numstat <base40>...<head40>`; base40 is pasted at dispatch and head40 comes from RESULT. This whole task text stays at or under **110 lines**.

Do not run Bats locally. After the final push verify GitHub Actions for the exact final head with `gh pr checks <pr> --repo mryfmo/dotfiles --watch`, fix in-scope failures and repeat before RESULT; follow Worker Playbook step 15 for the bounded Bot wait and findings. Before completion run `make require-crit-review` and, if required, follow AGENTS.md's crit-data receipt procedure; keep evidence with -worker- filenames under this task's allowed directory and never open a browser review.

## Completion

Use a fresh branch `tools/pre-send-check-a01` from origin/main (`git switch -c tools/pre-send-check-a01 --no-track origin/main`). Save .orchestration/dotfiles-T133-pre-send-check-a01/task.md byte-identical to the dispatched text. In that directory write report.md (implementation, named red/green outcomes, residuals, cost), validation.md (commands/output and cap totals), sandbox.md, learning.md and autoskill.md (used or not-used); do not commit plan/todo/learn worklogs. No changes to dispatch.sh, the checker, validator, workflows or the untracked glue.

Push inside the sandbox with `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push -u https://github.com/mryfmo/dotfiles.git <branch>`; open with `gh pr create --repo mryfmo/dotfiles` using an English title and body. Once final-head checks pass send `AGMSG-RESULT v1 task_id=dotfiles-T133-pre-send-check-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` and the artifact paths; no merge by the worker.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T07:24Z before send 2 (amendment 1, answering a008's blocked RESULT of 07:21:20Z) to a008: the cap sentence now backticks `tests/` and `.orchestration/` and keeps the numstat command in its own sentence, because regime-ci's cap parser reads the excluded paths from the backticked items of the `outside …` span (it had taken the numstat command and counted 851 lines against 90 on head 44d3bb4c); nothing else changed; previous_sha256 907cb3d4735fa9803827aa5b358e3db98a5ee57aa622b97fe138431b4fe43f5b; task-consistency-check.py OK; SECRET_PATTERN 0; home paths 0
the glue this promotes: .agents/worklog/orchestrator-glue/pre-send.sh (39 lines, 2026-10-20), its mistakes M-20261020-01 and M-20261020-03, correction C-102; the last dispatched python-pin text was refused by CI on a secret-pattern match the glue now catches before every send
counters at paste: task=dotfiles-T133-pre-send-check-a01 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=none..none (-) sourc; branch point for the caps: origin/main 60a6fb2b324d0381c4a6e539b37c650105154a7e; task SHA256 in the AGMSG-TASK line, computed over these final bytes
```
