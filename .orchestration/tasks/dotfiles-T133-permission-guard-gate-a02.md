---
format: 2
task_id: dotfiles-T133-permission-guard-gate-a02
kind: code
security: true
allowed_files:
  - scripts/permission-guard.py
  - scripts/orchestrator/ruleset-request.sh
  - scripts/orchestrator/ruleset-verify.sh
  - home/dot_claude/hooks/executable_gh-merge-gate.sh
  - home/dot_agents/agent-config.yaml
  - home/.chezmoitemplates/claude-settings-managed.json
  - scripts/generate-agent-configs.py
  - scripts/validate-agent-assets.py
  - scripts/check-agent-runtime.py
  - home/dot_config/git/config.tmpl
  - tests/unit/test_gh_merge_gate.py
  - tests/unit/test_permission_guard.py
  - tests/unit/test_ruleset_scripts.py
  - tests/unit/test_generate_agent_configs.py
  - tests/unit/test_validate_agent_assets.py
  - tests/unit/test_check_agent_runtime.py
  - .orchestration/dotfiles-T133-permission-guard-gate-a02/**
after: [dotfiles-T129-anthropic-auth-route-check-followup-a02]
reset_of: [dotfiles-T133-permission-guard-gate-a01]
threat_table:
  - control: "scripts/permission-guard.py (canonical permission-surface comparison between two revisions, diff SHA256 and the matching user-approved decision row; revision names and record contents are never executed)"
    disposition: "closed: tests/unit/test_permission_guard.py::test_permission_diff_without_an_approved_decision_row_fails_and_with_it_passes"
  - control: "scripts/orchestrator/ruleset-request.sh (expected ruleset JSON for 24397953 and its diff against the live GET response; no GitHub write)"
    disposition: "closed: tests/unit/test_ruleset_scripts.py::test_ruleset_request_prints_the_diff_and_never_writes"
  - control: "scripts/orchestrator/ruleset-verify.sh (one difference per line; progress rows D1 and D2 updated only after an exact match)"
    disposition: "closed: tests/unit/test_ruleset_scripts.py::test_ruleset_verify_reports_each_difference_and_writes_progress_only_on_match"
  - control: "home/dot_claude/hooks/executable_gh-merge-gate.sh (non-executing command-position recognition, valid JSON decisions, fail-closed errors, the deployed checkout anchor, parsed acceptance and audit evidence, the operation split and records-only path checks)"
    disposition: "closed: tests/unit/test_gh_merge_gate.py::test_gate_closes_each_of_the_seven_review_classes"
  - control: "home/dot_agents/agent-config.yaml (orchestrator_checkout beside worker_worktree, gh_merge_gate_hook and removal of only the three gated ask rules)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask"
  - control: "home/.chezmoitemplates/claude-settings-managed.json (generated synchronous PreToolUse command entry)"
    disposition: "residual: the existing generator produces this file from the manifest; make render-check checks byte equality and CI rejects rendering drift."
  - control: "scripts/generate-agent-configs.py (one synchronous Bash PreToolUse command entry rendered from gh_merge_gate_hook)"
    disposition: "closed: tests/unit/test_generate_agent_configs.py::test_manifest_gates_merge_update_branch_and_create_through_the_hook_and_keeps_every_other_gh_write_on_ask"
  - control: "scripts/validate-agent-assets.py (every retained gh write ask rule checked individually and the exact deployed synchronous hook command required)"
    disposition: "closed: tests/unit/test_validate_agent_assets.py::test_gate_validator_requires_every_retained_ask_rule_and_the_exact_synchronous_hook_entry"
  - control: "scripts/check-agent-runtime.py (deployed hook content and executable status checked through the existing runtime helper)"
    disposition: "closed: tests/unit/test_check_agent_runtime.py::test_runtime_check_compares_the_deployed_gh_merge_gate_hook_with_the_source"
  - control: "home/dot_config/git/config.tmpl (removal of the GitHub HTTPS-to-SSH pushinsteadof block)"
    disposition: "residual: the two removed lines contain no credential; the existing gh credential helper remains, and chezmoi verify after the operator's make update supplies the live deployment check."
  - control: "tests/unit/test_gh_merge_gate.py (inherited cases, all T131 dry inputs, checkout and evidence binding, operation split and the production heredoc regressions)"
    disposition: "residual: temporary HOME directories, temporary Git repositories and fake gh responses exercise decisions without executing payload commands or writing to GitHub; the final-head audit reads the assertions."
  - control: "tests/unit/test_permission_guard.py (revision fixtures, canonical surface comparisons and decision-row fixtures)"
    disposition: "residual: subprocess tests use temporary repositories and decisions files; malformed inputs and rendered-only changes are tested without executing input text."
  - control: "tests/unit/test_ruleset_scripts.py (fake gh argv capture and temporary progress records)"
    disposition: "residual: fixtures assert GET-only GitHub access and progress writes only on equality; no live ruleset or live progress record is changed by the tests."
  - control: "tests/unit/test_generate_agent_configs.py (manifest anchor and hook rendering contract with the complete retained ask set)"
    disposition: "residual: fixtures render the supported darwin and linux configurations and check the anchor contract; the final-head audit reads the cases."
  - control: "tests/unit/test_validate_agent_assets.py (each retained ask rule and the exact synchronous hook entry)"
    disposition: "residual: fixture settings independently remove retained rules and substitute fake or async hook entries; no live settings are changed."
  - control: "tests/unit/test_check_agent_runtime.py (temporary deployed-hook fixtures)"
    disposition: "residual: a temporary HOME supplies missing, matching, stale and non-executable hook cases through the existing fixture style; the live runtime is untouched."
  - control: ".orchestration/dotfiles-T133-permission-guard-gate-a02/** (this reset task's branch artifacts)"
    disposition: "residual: new evidence stays within this directory, distinguishes inherited observations from final-head results and is checked against the final diff and CI before acceptance."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-permission-guard-gate-a02/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-permission-guard-gate-a01/task.md)"
    disposition: "residual: the a02 copy is byte-identical to the dispatched text and its own SHA256 appears in TASK and RESULT; the orchestrator verifies the replacement and byte identity at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-permission-guard-gate-a02/ (report.md, validation.md, sandbox.md, learning.md and the dry-probe transcripts)"
    disposition: "residual: historical probes retain their tested identities and outputs, final-head closure is recorded separately, and sandbox.md lists every refused command; the audit reads the records."
  - control: task metadata
    disposition: "residual: the orchestrator checks the front matter with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; byte identity covers the complete dispatched task."
  - control: metadata separators
    disposition: "residual: the first document separators bound the task front matter and each record's structured data; whole-file byte comparison protects the task copy."
  - control: in-process effects
    disposition: "residual: the hook executes no payload text, prints one JSON decision and exits 0, with one decision log line under XDG_STATE_HOME; the guard and ruleset helpers read revisions, records and GET endpoints, and verify writes progress only on equality; tests use temporary state and deployment waits for the operator's make update."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow file changes; CI wiring remains P1-11's regime job; bash, jq and the non-executing tokenizer provide the hook's decision path, missing tools ask, and Python guard execution uses uv run --offline with python -I."
  - control: new or renamed scripts
    disposition: "residual: one hook, one guard and two ruleset helpers are the only new executable scripts; each is declared separately in allowed_files and listed in RESULT, and the audit rejects undeclared scripts."
  - control: orchestrator effect merge
    disposition: "residual: merge uses only gh pr merge --squash --match-head-commit <audited head> after the integration gate; local merges and pushes to main remain forbidden."
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch changes the head, so CI, the feedback sweep, task-level audit and security review bind the resulting final head before the integration gate."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records the discarded uncommitted state in the acceptance record."
premises:
  - claim: none of the five new files exists on origin/main
    command: git ls-files scripts/permission-guard.py scripts/orchestrator/ruleset-request.sh scripts/orchestrator/ruleset-verify.sh home/dot_claude/hooks/executable_gh-merge-gate.sh tests/unit/test_gh_merge_gate.py | wc -l
    output: |-
      0
  - claim: PR #400's branch, the material this task rebuilds from, is at the head the T131 review assessed
    command: git rev-parse origin/fix/claude-pinned-merge-gate
    output: |-
      0b874adb9850ff9647fbc039ec3cf6cc30487488
  - claim: the tracked git config still rewrites GitHub pushes to SSH while the live config (hand-edited) does not, the mismatch D3 (d) resolves
    command: /usr/bin/grep -c 'pushinsteadof = https://github.com/' home/dot_config/git/config.tmpl
    output: |-
      1
  - claim: the manifest still asks for gh pr merge, the rule the hook replaces
    command: /usr/bin/grep -c 'Bash(gh pr merge:\*)' home/dot_agents/agent-config.yaml
    output: |-
      1
  - claim: decisions.tsv carries no permission-scoped decision row yet, so the guard's first run on this PR itself must find the row this task adds
    command: /usr/bin/grep -c 'scope=permission' .orchestration/decisions.tsv
    output: |-
      0
---

# AGMSG-TASK dotfiles-T133-permission-guard-gate-a02 — INV-6 reset of dotfiles-T133-permission-guard-gate-a01 (plan 006 S2; plan 024 P1-14 and D3 (d); deadline 2026-10-19T03:00Z)

This text is the independent redesign by a review-profile context other than the author of a01. Plan 006 INV-6 stopped a01 at S2 after the three question PONGs at 2026-10-18T09:09:18Z, 09:10:24Z and 09:23:12Z. The questions are preserved verbatim in `.agents/worklog/orchestrator-glue/p114-a02-inputs.md`. Amendment 1 and the answers to all three questions are incorporated below as task requirements.

The worker keeps its branch, commits, item-0 baseline probes and four green permission-guard tests. Seat a010, worker-e, continues this task on the existing branch. The branch stays stacked on PR #412's head `d3480fc0` at `origin/tools/anthropic-auth-route-structured` until #412 merges, then rebases onto `main`. The PR opens after that rebase. One PR carries the whole task.

The next push replaces `.orchestration/dotfiles-T133-permission-guard-gate-a01/task.md` with this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-permission-guard-gate-a02/task.md`. The orchestrator handles removal of the predecessor copy as reset bookkeeping outside the worker's edit boundary. The a01 acceptance history, dispatch hashes and stopped status remain historical records.

The five premises preserve a01's write-time observations verbatim. New reports, validation, sandbox and learning records use the a02 directory. Inherited evidence retains its original tested identities and is distinguished from final-head closure.

The design sources are `.orchestration/plans/024-design-programs.md` item (14), `.orchestration/plans/024-design-quality.md` section 5.13, decision D-024-03 (d), and the T131 review of PR #400 at `0b874adb9850ff9647fbc039ec3cf6cc30487488`. The manifest permissions, rendered Claude settings and PreToolUse hook are Claude's execution boundary, so implementation remains assigned to a Codex seat.

## Goal

A permission-surface change to the manifest or its rendered outputs fails the guard unless `.orchestration/decisions.tsv` carries the operator's decision row with that diff's SHA256. Scripts display and verify the expected ruleset against the live value without changing GitHub settings. The rebuilt merge gate binds trusted evidence to the anchored checkout, repository, task, PR and head, preserves the specified draft-create and update-branch behavior, and distinguishes actual command positions from quoted prose and heredoc contents.

A pinned, accepted, green squash merge and an eligible records-only boundary merge run without a prompt. Unsupported gated invocations and failures ask. Commands that invoke no gh command receive no decision.

## Files

0. Item 0 preserves the dry-probe baseline already recorded in `.claude/worktrees/worker-e/.orchestration/dotfiles-T133-permission-guard-gate-a01/validation.md`. The 54 baseline entries include the inherited hook decisions, validator probes and argument-expansion demonstration against PR #400 at `0b874adb`. They are reproduction evidence and carry no closure or approval claim. The four permission-guard tests already have recorded red and green results. The a02 validation record retains or references these transcripts with their original identities. After implementation, the T131 probes run against the rebuilt hook and validator, with each input, expected result, actual decision and exit status recorded in a separate closure table.

1. `scripts/permission-guard.py --base <ref> --head <ref> [--decisions .orchestration/decisions.tsv] [--manifest home/dot_agents/agent-config.yaml]` is a new Python CLI run with `python -I`, using PyYAML through `uv run --offline --with pyyaml` and the standard library otherwise. It reads both revisions of the manifest and both revisions of the rendered `home/.chezmoitemplates/claude-settings-managed.json` and `codex-config-managed.toml` as text. The permission surface is the manifest's `claude.permissions` (`allow`, `deny`, `ask`, `defaultMode`), `claude.sandbox` (`excludedCommands`, `linux_excluded_commands`, `allowMachLookup`, `filesystem.extra_allow_write`, `network`), `claude.hooks` entries whose command decides a gh write (`gh_merge_gate_hook` and any PreToolUse command hook), `orchestrator_checkout`, `codex.sandbox_workspace_write` and `codex.approval_policy`, plus the rendered files' permission, sandbox and hook surface. The surface is canonicalised for base and head with sorted keys and compact `json.dumps` output. Equal surfaces produce exit 0 and `permission surface: unchanged`. Otherwise the guard prints the unified diff of the canonical forms and its SHA256. A `D-…` row in `decisions.tsv` must contain `scope=permission`, `approved_by=user` and `diff_sha256=<that sha>` in its `basis` or `what` column. A matching row produces exit 0 with its row id. A missing row produces one violation line per changed key path and exit 1. Revision names, diff contents and record text are never evaluated as shell code.

   This PR changes the permission surface. The orchestrator writes a new decision row (the next free `D-024-NN` id; `D-024-13` is taken by the ask-rule removal of 16:27 JST) to `.orchestration/decisions.tsv` with `scope=permission approved_by=user diff_sha256=<sha>` when the final head is known. The user's directive of 2026-10-18 13:5x JST supplies the approval. The SHA is the guard's own output on `--base origin/main --head <final head>` and is pasted in the acceptance record. The worker does not edit the decision ledger. CI wiring belongs to P1-11's regime job; until that wiring lands, the orchestrator runs the guard at acceptance and pastes its output.

2. `scripts/orchestrator/ruleset-request.sh [--expected <json>]` is a new Bash script with English shdoc comments. It prints the expected JSON for `main integration gate`, ruleset id `24397953`: the seven required contexts of `tests/unit/test_workflow_orchestration_skip.py`, `strict_required_status_checks_policy: false`, no `pull_request` rule, and the retained `deletion` and `non_fast_forward` rules. It reads the live value with `gh api repos/{owner}/{repo}/rulesets/24397953` and prints the diff of the canonical JSON forms. It calls no write form of gh, and the fake gh records argv to prove this.

   `scripts/orchestrator/ruleset-verify.sh` performs the same comparison. Equality writes the current UTC time and `verified` into the `evidence` and `updated_jst` columns of rows `D1` and `D2` in `.orchestration/plans/024-progress.tsv`, using a line-index edit with an asserted anchor, and exits 0. A difference prints one line per differing key and exits 1 without writing. Tests use temporary progress records. The worker does not change the live ruleset.

3. `home/dot_claude/hooks/executable_gh-merge-gate.sh` is rebuilt from `origin/fix/claude-pinned-merge-gate` at `0b874adb`, with English shdoc comments. The T131 review is `.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/review.md`. Its seven P1 and four P2 findings are closure requirements. The hook retains #400's allow conditions 1 to 5 and its create rules, with the checkout, evidence and boundary requirements stated here.

   Command recognition follows shell quoting and shell word boundaries without executing command text. A small quote-aware tokenizer distinguishes command positions, leading environment assignments, quoted arguments, comments and heredoc bodies. The allow grammar refuses substitutions, backticks, backslashes, unquoted glob characters, redirections, separators and newlines. Quoted or concatenated binary and subcommand spellings and unresolved alias-shaped invocation forms ask. Create arguments retain ordinary quoted title and body values while expansion-bearing arguments ask. Recognition precedes the allow grammar so unrelated heredocs and prose do not trigger its refusals. Item 7 defines the production regressions.

   Decisions are encoded with `jq -n --arg`. Missing jq emits a static valid ask JSON object. The hook uses `set -euo pipefail` and an ERR trap that asks. Detector or parser failures, empty or malformed payloads, malformed GitHub responses and empty or invalid default-branch answers ask. Every decision is logged as in #400. The header names each closed class and its test.

   The checkout anchor is the manifest key `orchestrator_checkout: ~/Workspace/dotfiles`, deployed to `~/.agents/agent-config.yaml`. The hook reads that deployed, sandbox-unwritable authority. The realpath of the payload cwd's Git toplevel equals the realpath of the expanded manifest value. That toplevel's Git common directory resolves to its own `.git`, establishing a primary checkout. The origin URL's `owner/repo` equals `gh repo view --json nameWithOwner` from that cwd and the PR operation's repository, selected by `--repo` or the default. All three conditions are required. The `check-regime-boundary.sh` chezmoi-clone recipe supplies no anchor here because the orchestrator merges from the Workspace checkout.

   The anchor is required for every `gh pr merge`, including records-only boundary merges, and every non-draft `gh pr create`, including records-only creates. A worker worktree's `gh pr create --draft` retains #400's pushed-head and base conditions and requires no anchor, since a linked worktree cannot pass the primary-checkout test. A bare `gh pr update-branch <n> [--repo o/r]` remains location-independent.

   A merge remains one permitted simple command carrying a PR number, `--squash`, a full 40-hex `--match-head-commit` and only the permitted optional repository flag. The PR is open, non-draft, targets the repository's valid default branch and has exactly that head. The default branch requires status checks, and every required context is successful on that head. Unsupported flags, including `--admin`, `--auto`, `--merge` and `--rebase`, ask.

   Acceptance is read from `.orchestration/acceptance/<task>.md` under the anchored root. The JSON between its first two `---` lines is parsed with jq. Its `task` names an existing task file, its `head` equals the accepted SHA, and its latest `AGMSG-ACCEPTANCE v1` dispatch line names that task and says `status=accepted`. For a merge, its `pr` equals the requested PR number. The record's repository binding is implicit through the proven checkout anchor. No record key is added. The fixed `RECORD_KEYS` schema and `scripts/require-crit-review.py` remain unchanged.

   The audit is the regular file `.orchestration/validation/<task>-audit-<sha7>.md`, with a non-empty regular `.last.md` companion whose last non-blank line is `Verdict: correct`, or `Verdict: incorrect` with one disposition in the record's `audit_findings` per `[P0-P3]` finding line. Symlinks anywhere in the acceptance or audit paths ask. Body text quoting a head, a mismatched task or PR, an audit directory and an undispositioned incorrect verdict provide no authority.

   Create remains one permitted plain command using #400's accepted base, head, title, body, body-file, draft, fill and repository flags. It has an explicit pushed non-default head and an explicit base equal to the valid default branch or the head branch of an open PR. Draft creation retains that behavior from worker worktrees. Non-draft creation additionally passes the anchor and requires either an `orchestration/` head whose comparison against the base contains only `.orchestration/` paths or an accepted pushed tip under the parsed-record rules. Records-only comparisons require a non-empty complete file list within #400's count bound, and check both every `filename` and every present `previous_filename`.

   A records-only boundary merge uses an `orchestration/boundary-*` branch whose comparison against the base touches only `.orchestration/` paths, including rename sources. It retains the anchor, pinned merge shape, PR state, head, base and green-check requirements. Plan 020 step 3 exempts it from the acceptance-record and audit requirements.

4. `home/dot_agents/agent-config.yaml` gains `orchestrator_checkout: ~/Workspace/dotfiles` beside `worker_worktree`, with an English explanatory comment, and gains `gh_merge_gate_hook: ~/.claude/hooks/gh-merge-gate.sh` under `claude.hooks` with #400's comment. The three ask rules `Bash(gh pr merge:*)`, `Bash(gh pr create:*)` and `Bash(gh pr update-branch:*)` leave. Every other gh write stays on ask. At rebase, main's complete retained ask set is preserved and only these three gated rules are removed.

   `scripts/generate-agent-configs.py` renders the hook as one synchronous `PreToolUse` command entry matching `Bash`. The existing generator regenerates `home/.chezmoitemplates/claude-settings-managed.json`, and `make render-check` verifies it. `scripts/validate-agent-assets.py` checks the complete retained gh write ask set rule by rule and requires the exact deployed hook command as one synchronous command entry. A suffix match, an `echo` command and an async entry fail validation. `scripts/check-agent-runtime.py` compares the deployed hook with the tracked source through its existing executable-hook check.

   The manifest anchor key is accepted by `make render-check` and `make validate-agent-assets`. A refusal produces a blocked PONG with the command and output. `home/dot_config/git/config.tmpl` loses the `[url "git@github.com:"] pushinsteadof` block. HTTPS pushes use the existing gh credential helper. The live config already lacks the rewrite, and the operator's post-merge `make update` brings the tracked and deployed states into agreement.

5. `tests/unit/test_gh_merge_gate.py` retains #400's cases and adds `test_gate_closes_each_of_the_seven_review_classes`, with one sub-case per T131 dry input. Actual or unresolved unsupported gh invocation forms assert ask or refusal, never allow. Unrelated prose and heredoc inputs assert exit 0 with no decision. The cases cover quoted and concatenated executable and subcommand words, tabs and JSON control characters, detector failure, malformed and empty payloads, invalid default branches, an unrelated primary repository with the same origin, a different target repository with the same head, parsed record task/PR/head/latest-dispatch binding, symlinked evidence parents, invalid audit files and verdicts, glob-bearing create values, incomplete records comparisons and renamed sources outside `.orchestration/`.

   Honest pinned accepted green merges and records-only boundary merges from the anchored checkout assert allow. The same merge operations from a worker worktree or an unanchored primary repository ask. Non-draft creates require the anchor. Draft creates from a linked worker worktree with a pushed head and valid base retain allow, and bare update-branch remains location-independent. Item 7's command-position cases are included in the closure coverage.

   `tests/unit/test_permission_guard.py` retains the four already-green tests, including `test_permission_diff_without_an_approved_decision_row_fails_and_with_it_passes`. Coverage includes unchanged surfaces, non-permission manifest changes, rendered-only changes, sandbox and checkout-anchor changes, malformed data and bad revisions. `tests/unit/test_ruleset_scripts.py` contains the two tests named in the threat table. The existing generation, validator and runtime modules contain the tests named in their threat rows, with each retained ask rule checked independently and fake or async hooks rejected. Fixture lines count against the test cap.

6. Every new or changed test is written before its corresponding implementation change and has red-then-green evidence. The validation record includes the exact selector, command, tested revision or source identity, exit status and verbatim output for both results. Existing a01 red evidence remains valid historical evidence for an unchanged retained test, and its green result is rerun on the final a02 head. A changed assertion or added sub-case receives its own red reproduction before its implementation fix. The rebuilt-hook dry-probe closure table is recorded after implementation and supplies case-by-case evidence for the audit. An inherited green suite alone supplies no red evidence for a new regression.

7. The production observation at 2026-10-18 18:29 JST is an `argv-text-mismatch` regression requirement. The hand-applied #400 hook prompted worker seats with `not a single simple command around: gh pr merge` while a heredoc wrote test strings followed by a unit-test run, and with `around: gh pr create` while a heredoc wrote `report.md`. Neither command invoked gh.

   The hook decides the gated operation from a parsed simple command whose `argv[0]`, after leading environment assignments, is `gh` and whose subcommand is `pr merge`, `pr create` or `pr update-branch`. Words in ordinary quoted strings, comments and literal heredoc bodies provide no command position. A command that invokes gh in no command position exits 0 with no decision, regardless of those words. A compound command that invokes gh in any command position is refused as not a single simple command. No part of the submitted command text executes during recognition or decision.

   Tests in `tests/unit/test_gh_merge_gate.py` reproduce both live shapes as payload strings. The first writes test strings containing `gh pr merge` through a quoted heredoc and then runs a unit-test command. The second writes a report containing `gh pr create` through a quoted heredoc. Both assert exit 0 and empty decision output. An environment-prefixed `gh pr merge` asserts a decision, with an unsupported merge flag producing ask. A compound command with `gh pr merge` after a separator asserts refusal. The fixtures never execute those payload strings. Leading-assignment recognition introduces no additional allow form beyond the specified gate conditions.

## Out of scope

The worker seats' own allow rules (a separate task after P1-7 merges, since it edits `herdr-agents`), the `regime` CI job (P1-11), permgate (`home/dot_agents/permgate-policy.yaml`, the operator's), any Codex boundary file, the ruleset toggles themselves (the operator's; item 2 only shows and verifies), `make update` (the operator's, after this PR merges: DoD2).

## Check

`make render-check`, `make validate-agent-assets`, `make format`, `shellcheck` and `shfmt -d` on the hook and the two scripts clean, `uv run python -m unittest tests.unit.test_gh_merge_gate tests.unit.test_permission_guard tests.unit.test_ruleset_scripts tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets tests.unit.test_check_agent_runtime tests.unit.test_claude_settings_merge -v` green, `uv run --offline --with pyyaml python -I scripts/permission-guard.py --base origin/main --head HEAD` printing the diff sha (exit 1 until the orchestrator's row exists, pasted as such), all pasted in `.orchestration/dotfiles-T133-permission-guard-gate-a02/validation.md`, with `git diff --numstat origin/main...HEAD`: at most 650 changed lines outside `tests/`, `.orchestration/` and the regenerated template (the hook alone about 250), 700 under `tests/`.

Changed lines are additions plus deletions. The validation includes item 0's inherited baseline, item 6's red-then-green evidence and the final closure results for item 7. No local Bats tests run. Required Bats results come from GitHub Actions. The orchestrator runs task-consistency-check C1 to C10 and C7b before dispatch and at acceptance.

## Completion

The existing branch continues this task and produces one PR. It remains stacked on PR #412's head `d3480fc0` until #412 merges, then rebases onto main and opens the PR. The next push contains the replacement a02 task copy. The reset creates no fresh implementation branch and no second implementation PR. The deadline remains `2026-10-19T03:00Z`, which is 2026-10-19 12:00 JST.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's branch and dependency requirements, `dotfiles-T133-permission-guard-gate-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-permission-guard-gate-a02/task.md>` in RESULT. The orchestrator writes that owner task before assigning its first advisory P2. Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. The stopped a01 history remains preserved.

The no-prompt directive qualifies the inherited Bot workflow. No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required CI passes before RESULT. Every feedback item is reported with its proposed disposition, and surviving P0/P1 findings stop integration under the inherited completion rule.

A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker-side review evidence uses the required `-worker-` infix. RESULT names the head, base, branch, changed files, every Bot thread and its disposition, test names, caps, new scripts, task-copy hash and evidence paths. The orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. The orchestrator runs the task-level audit and a separate security-profile review on the final head. The `unbound-evidence`, `argv-text-mismatch` and `fail-open-on-error` classes are this PR's S1 classes. A third finding of any one class stops the artifact for redesign and never starts a fourth round. The production command-position regressions belong to `argv-text-mismatch`.

Final-head feedback collection, audit dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh required evidence. Merge uses `gh pr merge --squash --match-head-commit <audited head>`. Commands for gh and Git writes run individually, without shell chaining or a wrapper combining writes.

Live deployment and ruleset toggles remain the operator's actions. Local Bats and live payload execution are not performed; runtime deployment remains unverified until the operator's post-merge checks.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```