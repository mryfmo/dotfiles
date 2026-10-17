---
format: 2
task_id: dotfiles-T129-anthropic-auth-route-check-followup-a01
kind: code
security: true
allowed_files:
  - scripts/validate-agent-assets.py
  - tests/unit/test_validate_agent_assets.py
  - .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/**
after: [dotfiles-T129-anthropic-auth-route-check-a01]
threat_table:
  - control: the PR edits scripts/validate-agent-assets.py only within the owned rows (item 1)
    disposition: "residual: the edits are exactly the owned rows of the lineage's acceptance record (item 1), each with its test named in report.md; the orchestrator's diff review and the task-level audit from main compare the diff against the rows"
  - control: the PR edits tests/unit/test_validate_agent_assets.py only within the owned rows (item 1)
    disposition: "residual: one fixture per owned row, red before the fix and green after; the audit reads each case against its row"
  - control: "the applied files the validator scans as a trust boundary (JSON, YAML, TOML and shell text under home/ and install/ that a PR controls)"
    disposition: "residual: the validator reads them as text and, where item 1 says so, through the standard parsers (json, tomllib, the yaml reader already used) without executing anything; a parse failure is reported, never skipped"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests import the validator as the existing tests do and run it on fixture trees in a temporary directory; nothing is applied to the live home directory"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; the validator runs where make validate-agent-assets runs, under the repository's python"
  - control: new or renamed scripts
    disposition: "residual: no new or renamed script: the owned rows name edits to the two files the lineage landed; any new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises: []
---

# AGMSG-TASK dotfiles-T129-anthropic-auth-route-check-followup-a01 — the auth-route lineage's owner task (advisory P2 of PR #389, and the structured-parse re-plan if the operator assigns it here)

Written 2026-10-17 by the orchestrator seat at the review of PR #389's round 3 (C-51: the owner task exists before the first advisory row). It owns the advisory rows recorded under `## Owned by dotfiles-T129-anthropic-auth-route-check-followup-a01` in `.orchestration/acceptance/dotfiles-T129-anthropic-auth-route-check-a01.md` (plan 020 step 1.2); it is dispatched after PR #389 is decided, to a seat the orchestrator names then.

## Goal

The lineage's re-plan `raw-line-regex` (the record of PR #389), assigned to this task by the operator's decision of 2026-10-17 22:4x JST (D-389-merge-a): the Anthropic credential check reads the structured formats (JSON, TOML, YAML) through their parsers, key names decoded and values read as data, so quoting, escaping and delimiters of a format can no longer bypass it, and only shell text keeps the line grammar (the whole-value allowlist of D-389-replan); every owned row is fixed with one fixture per row, red before and green after; no other change.

## Files

1. The re-plan (item 0 of the owned rows, class escaped-name, thread 4302758230 of PR #389, dispositioned there as a stated limit): in `scripts/validate-agent-assets.py` the check of applied files branches on the file's format: `.json` through `json.loads`, `.toml` through `tomllib`, `.yaml`/`.yml` through the yaml reader the validator already uses; every key path is walked, a key whose decoded name is `ANTHROPIC_API_KEY` or `ANTHROPIC_OAUTH_TOKEN` (and the names the current regex covers) is refused when its value is a literal (the whole-value allowlist decides: one reference, a template, or empty are accepted), a parse failure is a refusal naming the file (never a skip); shell files keep the current line grammar. The format is decided after stripping chezmoi's attribute prefixes from the basename, and a source whose content is not the target data (`modify_`, `run_`, `symlink_`, `encrypted_` sources, and `.tmpl` sources as today) is script text under the line grammar, as the validator already treats the `modify_private_*.config.toml` executables; every other `.json`, `.toml`, `.yaml` or `.yml` source is parsed (Amendment 1). Fixtures, each refused by the parsed form and not by the raw line: a TOML basic-quoted key with `\u` escapes, a JSON key with `\u` escapes, a YAML quoted key, a nested table or mapping holding the key, a literal spread over a line continuation where the format allows it; and pass cases for a reference value in each format.
2. The owned rows at dispatch (the record is the source; this list is its reading at 2026-10-17T13:4xZ): 4302758234 (class single-quoted-reference: a single-quoted `$NAME` reference is literal text in Bash, a broken credential rather than a leak; accept the reference only in double quotes or bare); 4302758239 (class json-delimiter-after-value: a JSON reference followed by a comma or a brace, which the parsed form of item 1 reads as a value and makes moot; keep one pass case). Rows added to the record after this text was written are read from the record at dispatch.

## Out of scope

Any rule not named by an owned row; the omp auth store probe (plan 023 PR D's run-time half).

## Check

`uv run python -m unittest tests/unit/test_validate_agent_assets.py -v` green and `make validate-agent-assets` (exit 0) pasted in the validation file, with `git diff --numstat origin/main...HEAD`: at most 200 changed lines outside `tests/` and `.orchestration/`, and 1000 added lines under `tests/`.

## Completion

One PR from a fresh branch off `origin/main`; PR #389 merges first (the operator's decision), so the branch starts after that merge or rebases onto it before its RESULT (the two files are the same). Caps for this task: at most 250 changed lines outside `tests/` and `.orchestration/` (the three parser branches), 1000 under `tests/`. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T129-anthropic-auth-route-check-followup-a02` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T129-anthropic-auth-route-check-followup-a01/task.md>` in the RESULT.

## Assignment (round 1, 2026-10-17T13:4xZ)

The operator's decision of 22:4x JST on PR #389 (D-389-merge-a): the surviving P1 4302758230 is dispositioned as a stated limit and #389 merges after its chain; the parser-based redesign is this task, dispatched to a007 now. The Goal and item 1 above carry it; the caps in Completion are this task's.

## Amendment 1 (round 1, 2026-10-17T13:5xZ)

a007's Q1 (PONG 13:53:53Z): 8 of the 35 tracked structured sources under home/ are chezmoi `modify_` scripts (shell text named like the target format) that fail the parsers, so "a parse failure is a refusal" would fail the validator on main. The default a007 built is adopted: the format is decided after stripping the chezmoi attribute prefixes from the basename; `modify_`, `run_`, `symlink_` and `encrypted_` sources and `.tmpl` sources are script text under the line grammar; every other `.json`/`.toml`/`.yaml`/`.yml` source is parsed and a parse failure there is a refusal (item 1 says so). The base statement is approved too: origin/main lacks `validate_anthropic_auth_route`, so the branch starts from PR #389's head 862ab31c and rebases onto origin/main after #389 merges; no PR opens before that rebase. Nothing else changes.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T129-anthropic-auth-route-check-followup-a01.md: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T129-anthropic-auth-route-check-followup-a01.md
```
