---
format: 2
task_id: dotfiles-T133-permission-guard-gate-a03
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
  - .orchestration/dotfiles-T133-permission-guard-gate-a03/**
after: [dotfiles-T129-anthropic-auth-route-check-followup-a02]
reset_of: [dotfiles-T133-permission-guard-gate-a02]
threat_table:
  - control: "scripts/permission-guard.py (canonical permission-surface comparison between two revisions, diff SHA256 and the matching user-approved decision row; revision names and record contents are never executed)"
    disposition: "closed: tests/unit/test_permission_guard.py::test_permission_diff_without_an_approved_decision_row_fails_and_with_it_passes"
  - control: "scripts/orchestrator/ruleset-request.sh (expected ruleset JSON for 24397953, duplicate-preserving comparison against the live GET response and no GitHub write)"
    disposition: "closed: tests/unit/test_ruleset_scripts.py::test_ruleset_comparison_preserves_duplicate_rule_types"
  - control: "scripts/orchestrator/ruleset-verify.sh (one difference per occurrence and key, with duplicate rule types retained; progress rows D1 and D2 updated only after an exact match)"
    disposition: "closed: tests/unit/test_ruleset_scripts.py::test_ruleset_comparison_preserves_duplicate_rule_types"
  - control: "home/dot_claude/hooks/executable_gh-merge-gate.sh (three-outcome recognition, raw metacharacter exclusion, POSIX shlex only for allow candidates, one normalised-text regex for ask, valid JSON decisions, fail-closed errors, checkout and evidence binding, operation rules and records-only path checks)"
    disposition: "residual: command names assembled from variables or parameter expansion remain outside static name recognition; an invocation with no visible gated-word pattern can evade the ask test, and permgate and the auto-mode classifier provide the next layer. The spelling x=g; ${x}h illustrates the assembled-name residual; a visible pr merge still matches the ask test."
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
  - control: "tests/unit/test_gh_merge_gate.py (the table-driven corpus, metacharacter property test, checkout and evidence binding, operation split and production heredoc regressions)"
    disposition: "residual: temporary HOME directories, temporary Git repositories and fake gh responses exercise all three outcomes without executing payload commands or writing to GitHub; the final-head audit reads the assertions and the documented residual."
  - control: "tests/unit/test_permission_guard.py (revision fixtures, canonical surface comparisons and decision-row fixtures)"
    disposition: "residual: subprocess tests use temporary repositories and decisions files; malformed inputs and rendered-only changes are tested without executing input text."
  - control: "tests/unit/test_ruleset_scripts.py (fake gh argv capture, duplicate-rule fixtures and temporary progress records)"
    disposition: "residual: fixtures assert GET-only GitHub access, separately reported duplicate occurrences and progress writes only on equality; no live ruleset or live progress record is changed by the tests."
  - control: "tests/unit/test_generate_agent_configs.py (manifest anchor and hook rendering contract with the complete retained ask set)"
    disposition: "residual: fixtures render the supported darwin and linux configurations and check the anchor contract; the final-head audit reads the cases."
  - control: "tests/unit/test_validate_agent_assets.py (each retained ask rule and the exact synchronous hook entry)"
    disposition: "residual: fixture settings independently remove retained rules and substitute fake or async hook entries; no live settings are changed."
  - control: "tests/unit/test_check_agent_runtime.py (temporary deployed-hook fixtures)"
    disposition: "residual: a temporary HOME supplies missing, matching, stale and non-executable hook cases through the existing fixture style; the live runtime is untouched."
  - control: ".orchestration/dotfiles-T133-permission-guard-gate-a03/** (this redesign task's branch artifacts)"
    disposition: "residual: new evidence stays within this directory, distinguishes inherited observations from final-head results and is checked against the final diff and CI before acceptance."
  - control: "the task-file copy on the branch (.orchestration/dotfiles-T133-permission-guard-gate-a03/task.md) replaces the reset_of task's copy (.orchestration/dotfiles-T133-permission-guard-gate-a02/task.md)"
    disposition: "residual: the a03 copy is byte-identical to the dispatched text and its own SHA256 appears in TASK and RESULT; the orchestrator verifies the replacement and byte identity at acceptance."
  - control: "the branch evidence records under .orchestration/dotfiles-T133-permission-guard-gate-a03/ (report.md, validation.md, sandbox.md, learning.md and the dry-probe transcripts)"
    disposition: "residual: historical probes retain their tested identities and outputs, final-head closure is recorded separately, and sandbox.md lists every refused command; the audit reads the records."
  - control: task metadata
    disposition: "residual: the orchestrator checks the front matter with task-consistency-check C1 to C10 and C7b before dispatch and at acceptance; byte identity covers the complete dispatched task."
  - control: metadata separators
    disposition: "residual: the first document separators bound the task front matter and each record's structured data; whole-file byte comparison protects the task copy."
  - control: in-process effects
    disposition: "residual: the hook executes no payload text and exits 0 with one JSON decision or empty output, logging each decision under XDG_STATE_HOME; the guard and ruleset helpers read revisions, records and GET endpoints, and verify writes progress only on equality; tests use temporary state and deployment waits for the operator's make update."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow file changes; CI wiring remains P1-11's regime job; bash, jq and Python standard-library shlex and re provide the hook's decision path, missing tools ask, and Python guard execution uses uv run --offline with python -I."
  - control: new or renamed scripts
    disposition: "residual: one hook, one guard and two ruleset helpers are the only new deployable executable scripts; each is declared separately in allowed_files and listed in RESULT, and the audit rejects undeclared scripts."
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

# AGMSG-TASK dotfiles-T133-permission-guard-gate-a03 — S1 redesign of dotfiles-T133-permission-guard-gate-a02 (plan 024 P1-14 and D3 (d); deadline 2026-10-19T03:00Z)

This text is the independent redesign by a review-profile context. The a02 artifact stopped at S1 on `2026-10-18T10:30:50Z`. Its independent review found three `argv-text-mismatch` findings, comprising the lineage's third S1 row. The artifact went to redesign and received no fourth round. The class table and the orchestrator's `re-plan:` line remain in `.orchestration/acceptance/dotfiles-T133-permission-guard-gate-a02.md`.

The withdrawn requirement came from the orchestrator's a02 item 7. Static command-position recognition cannot establish that indirect shell execution is harmless prose. This redesign replaces that promise with the three outcomes in item 3 and carries the duplicate-ruleset finding into item 8.

The worker keeps its branch, commits, item-0 baseline probes, four green permission-guard tests and a02 artifacts. Seat a010, worker-e, continues on `tools/permission-guard-gate-a01`. The branch stays stacked on PR #412's head `d3480fc0` at `origin/tools/anthropic-auth-route-structured` until #412 merges, then rebases onto `main`. The PR opens after that rebase. One PR carries the whole task. The deadline remains `2026-10-19T03:00Z`.

The next push replaces `.orchestration/dotfiles-T133-permission-guard-gate-a02/task.md` with this dispatched text's byte-identical copy at `.orchestration/dotfiles-T133-permission-guard-gate-a03/task.md`. The orchestrator handles removal of the predecessor task copy as reset bookkeeping outside the worker's edit boundary. The a01 S2 history, a02 S1 history, dispatch hashes, stopped statuses and original artifacts remain historical records.

The five premises preserve the predecessor's write-time observations verbatim. New reports, validation, sandbox and learning records use the a03 directory. Inherited evidence retains its original tested identities and is distinguished from final-head closure. The worker does not rewrite the a02 artifacts to claim approval or completed evidence.

The design sources are `.orchestration/plans/024-design-programs.md` item (14), `.orchestration/plans/024-design-quality.md` section 5.13, decision D-024-03 (d), the T131 review of PR #400 at `0b874adb9850ff9647fbc039ec3cf6cc30487488`, and the a02 acceptance record's `re-plan:` line. The manifest permissions, rendered Claude settings and PreToolUse hook are Claude's execution boundary, so implementation remains assigned to a Codex seat.

## Goal

A permission-surface change to the manifest or its rendered outputs fails the guard unless `.orchestration/decisions.tsv` carries the operator's decision row with that diff's SHA256. Scripts display and verify the expected ruleset against the live value without changing GitHub settings or collapsing duplicate rule types.

The rebuilt merge gate allows only the specified metacharacter-free shlex argv forms when their operation conditions hold. It binds trusted evidence to the anchored checkout, repository, task, PR and head, and preserves the specified draft-create and update-branch behavior. Otherwise, text carrying the specified gated-word patterns asks, and every other command receives no decision.

A pinned, accepted, green squash merge and an eligible records-only boundary merge run without a prompt. Recognition and decision execute no part of the submitted command text. Variable-assembled names remain a documented residual covered by permgate and the auto-mode classifier as the next layer.

## Files

0. Item 0 preserves the dry-probe baseline already recorded in `.claude/worktrees/worker-e/.orchestration/dotfiles-T133-permission-guard-gate-a01/validation.md`. The 54 baseline entries include the inherited hook decisions, validator probes and argument-expansion demonstration against PR #400 at `0b874adb`. They are reproduction evidence and carry no closure or approval claim. The four permission-guard tests already have recorded red and green results.

   The a02 artifacts remain at `.claude/worktrees/worker-e/.orchestration/dotfiles-T133-permission-guard-gate-a02/`. They include `independent-review.md`, `finding-classes.json`, `report.md` and `validation.md`. The a02 report records 279 green tests and a 54-entry replay against hook SHA256 `321cfe997a2d1496bc370d3d5b07730a56b74be3eb643084ddb3e83f5df4ba93`; those results missed the independent review's counterexamples and close nothing by themselves. The a03 validation record retains or references the original transcripts, source identities, failures and evidence limitations.

   After implementation, the T131 probes and the redesigned corpus run against the rebuilt hook and validator. A separate closure table records each input, its a03 expected result, actual decision, exit status and tested source identity. Historical expectations remain intact, and each expectation changed by this redesign is identified explicitly.

1. `scripts/permission-guard.py --base <ref> --head <ref> [--decisions .orchestration/decisions.tsv] [--manifest home/dot_agents/agent-config.yaml]` is a new Python CLI run with `python -I`, using PyYAML through `uv run --offline --with pyyaml` and the standard library otherwise. It reads both revisions of the manifest and both revisions of the rendered `home/.chezmoitemplates/claude-settings-managed.json` and `codex-config-managed.toml` as text. The permission surface is the manifest's `claude.permissions` (`allow`, `deny`, `ask`, `defaultMode`), `claude.sandbox` (`excludedCommands`, `linux_excluded_commands`, `allowMachLookup`, `filesystem.extra_allow_write`, `network`), `claude.hooks` entries whose command decides a gh write (`gh_merge_gate_hook` and any PreToolUse command hook), `orchestrator_checkout`, `codex.sandbox_workspace_write` and `codex.approval_policy`, plus the rendered files' permission, sandbox and hook surface. The surface is canonicalised for base and head with sorted keys and compact `json.dumps` output. Equal surfaces produce exit 0 and `permission surface: unchanged`. Otherwise the guard prints the unified diff of the canonical forms and its SHA256. A `D-…` row in `decisions.tsv` must contain `scope=permission`, `approved_by=user` and `diff_sha256=<that sha>` in its `basis` or `what` column. A matching row produces exit 0 with its row id. A missing row produces one violation line per changed key path and exit 1. Revision names, diff contents and record text are never evaluated as shell code.

   This PR changes the permission surface. The Decision row section governs its approval record. The worker does not edit the decision ledger. CI wiring belongs to P1-11's regime job; until that wiring lands, the orchestrator runs the guard at acceptance and pastes its output.

2. `scripts/orchestrator/ruleset-request.sh [--expected <json>]` is a new Bash script with English shdoc comments. It prints the expected JSON for `main integration gate`, ruleset id `24397953`: the seven required contexts of `tests/unit/test_workflow_orchestration_skip.py`, `strict_required_status_checks_policy: false`, no `pull_request` rule, and the retained `deletion` and `non_fast_forward` rules. It reads the live value with `gh api repos/{owner}/{repo}/rulesets/24397953` and prints the diff of the canonical JSON forms. It calls no write form of gh, and the fake gh records argv to prove this.

   `scripts/orchestrator/ruleset-verify.sh` performs the same comparison. Equality writes the current UTC time and `verified` into the `evidence` and `updated_jst` columns of rows `D1` and `D2` in `.orchestration/plans/024-progress.tsv`, using a line-index edit with an asserted anchor, and exits 0. A difference prints one line per differing key and exits 1 without writing. Tests use temporary progress records. The worker does not change the live ruleset. Item 8 governs duplicate rule types in both scripts.

3. `home/dot_claude/hooks/executable_gh-merge-gate.sh` is rebuilt from `origin/fix/claude-pinned-merge-gate` at `0b874adb`, with English shdoc comments. The T131 review is `.claude/worktrees/worker-e/.orchestration/dotfiles-T131-claude-pinned-merge-gate-review-a01/review.md`. Its seven P1 and four P2 findings remain tracked in the closure table. This redesign replaces their command-recognition and prose expectations with the three outcomes below. The checkout, evidence, JSON, error, validator and records-only findings remain closure requirements. The hook retains #400's allow conditions 1 to 5 and its create rules, subject to the recognition contract and the checkout, evidence and boundary requirements stated here.

   The hook has exactly three outcomes: allow, ask and no decision. All outcomes exit 0. Allow and ask emit valid hook decision JSON. No decision emits empty stdout. No submitted command text is executed, evaluated, sourced or passed to a shell for recognition or decision.

   Allow requires raw command text containing none of `;`, `&`, `|`, `<`, `>`, `(`, `)`, backtick, `$`, backslash, newline, `*`, `?`, `[`, `]`, `{`, `}`, `#` or `~`. This exclusion applies everywhere, including quoted text and the first word; `#` and `~` have no boundary exemption. Space and tab are the permitted word separators. Other ASCII control characters are excluded from allow. Python `shlex` in POSIX mode splits the candidate into argv without expansion or execution. Its `argv[0]` is exactly `gh`, `argv[1]` is exactly `pr`, and `argv[2]` is exactly `merge`, `create` or `update-branch`. The remaining argv satisfies that operation's permitted grammar and conditions below. Ordinary single and double quotes are permitted through shlex; quoted or concatenated spellings receive the same argv checks.

   The ask detector removes every single quote, double quote, backtick and backslash from the raw text and collapses whitespace runs to one space. One regex over that normalised text matches whole-word `gh` followed anywhere later by whole-word `merge`, `create` or `update-branch`, or the bigram `pr merge`, `pr create` or `pr update-branch`. Matching uses case-sensitive regex word boundaries, with the hyphen in `update-branch` literal. The detector examines the whole text, including prose, comments, quoted arguments, wrappers, pipelines and heredoc bodies. It uses no tokenizer or command-position analysis.

   The regex establishes whether the text carries gated words before shlex is attempted for an allow candidate. Text matching the regex asks whenever any allow condition fails. The reason names the matching gated words and the failed condition. A metacharacter prevents allow but does not alone create an ask. Every other command receives no decision. Missing tools, unreadable or malformed payloads, detector failures and failures while checking an allow candidate ask.

   Decisions are encoded with `jq -n --arg`. Missing jq emits a static valid ask JSON object. The hook uses `set -euo pipefail` and an ERR trap that asks. Parser failures on allow candidates, empty or malformed payloads, malformed GitHub responses and empty or invalid default-branch answers ask. Every decision is logged as in #400. The header names each closed class and its test and states the residual.

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

5. `tests/unit/test_gh_merge_gate.py` retains #400's applicable cases and uses `test_gate_closes_each_of_the_seven_review_classes` as a table-driven test over the T131 dry inputs and the redesigned regression corpus. Each row records the payload text, fixture conditions and expected outcome. The assertions check exit status, empty output for no decision, valid decision JSON otherwise, and the gated words in ask reasons.

   The table includes quoted and concatenated executable and subcommand words, tabs and JSON control characters, detector failure, malformed and empty payloads, invalid default branches, an unrelated primary repository with the same origin, a different target repository with the same head, parsed record task/PR/head/latest-dispatch binding, symlinked evidence parents, invalid audit files and verdicts, glob-bearing create values, incomplete records comparisons and renamed sources outside `.orchestration/`.

   The table includes the two live heredoc shapes observed at 2026-10-18 18:29 JST. The heredoc writing test strings containing `gh pr merge` followed by a unit-test command asks. The heredoc writing a report containing `gh pr create` asks. Their payload strings are data and never execute.

   The table includes the worker review's `env -S 'gh pr merge 7 --admin'`, `printf '%s' 'gh pr merge 7 --admin' | bash`, and the heredoc whose delimiter contains a backslash-newline and whose body contains `$(gh pr merge 7 --admin)`. Each asks. A bracket test carrying the gated words, such as `[ -n 'gh pr merge' ]`, asks. The review's original plain `[ -f README.md ]` and `[[ -f README.md ]]` receive no decision because they contain no gated-word match. This distinction follows the three-outcome contract and removes the old executable-name heuristic.

   Honest pinned accepted green merges and records-only boundary merges from the anchored checkout assert allow. The same merge operations from a worker worktree or an unanchored primary repository ask. Non-draft creates require the anchor. Draft creates from a linked worker worktree with a pushed head and valid base assert allow under #400's header rules, including an open stacked base whose parent has no acceptance. Bare update-branch remains location-independent and asserts allow.

   Plain unrelated commands assert exit 0 and empty output. Historical T131 expectations are annotated where the new contract changes them. Prose and heredocs carrying gated words now ask. A command such as `gh land 7 --admin` has no gated-word match and receives no decision from this hook. Literal quoted or concatenated words that shlex resolves to the permitted argv remain subject to all operation conditions; the T131 `--admin` examples ask.

   `test_no_shell_metacharacter_input_is_allowed` is one property test implemented with the standard library and the existing unittest fixture style. It iterates the whole corpus and a generated set of insertions of every metacharacter listed in item 3 into honest merge, boundary-merge, draft-create and update-branch commands. Insertions cover word starts, word interiors, separators and quoted argument values, including `#` and `~` at and away from the first word boundary. Every input containing a listed metacharacter asserts an outcome other than allow. The property preserves the distinction between ask and no decision established by the corpus.

   `tests/unit/test_permission_guard.py` retains the four already-green tests, including `test_permission_diff_without_an_approved_decision_row_fails_and_with_it_passes`. Coverage includes unchanged surfaces, non-permission manifest changes, rendered-only changes, sandbox and checkout-anchor changes, malformed data and bad revisions. `tests/unit/test_ruleset_scripts.py` retains `test_ruleset_request_prints_the_diff_and_never_writes` and `test_ruleset_verify_reports_each_difference_and_writes_progress_only_on_match` and adds item 8's duplicate-rule regression. The existing generation, validator and runtime modules contain the tests named in their threat rows, with each retained ask rule checked independently and fake or async hooks rejected. Fixture lines count against the test cap.

6. Every new or changed test is written before its corresponding implementation change and has red-then-green evidence. The validation record includes the exact selector, command, tested revision or source identity, exit status and verbatim output for both results. Existing a01 red evidence remains valid historical evidence for an unchanged retained test, and its green result is rerun on the final a03 head. A changed assertion or added sub-case receives its own red reproduction before its implementation fix. The rebuilt-hook dry-probe closure table is recorded after implementation and supplies case-by-case evidence for the audit. An inherited green suite alone supplies no red evidence for a new regression.

   Uncommitted source identities are recorded with content SHA256 values before each red run and after its fix. The missing intermediate identities disclosed by the a02 report remain an evidence limitation; they are not reconstructed by assumption. New or changed regression assertions receive complete a03 red-then-green evidence. The 54 baseline probes, the earlier four green permission-guard tests and the a02 green suite remain reproduction evidence and close no new finding by themselves.

7. The withdrawn clause is a02 item 7's promise that a command invoking gh in no parsed command position receives no decision regardless of words in prose, comments or heredoc bodies. The associated command-position tokenizer and the requirement that both live heredoc shapes produce empty output are withdrawn. The replacement is exactly item 3's metacharacter-free allow grammar, normalised gated-word ask test and no-decision remainder. The recognition change is about forty lines replacing the quote-aware tokenizer; it adds no shell parser or execution-based dry parse.

   A Bash command whose prose carries the gated words asks, so seats write such prose with the file-edit tool. The SKILL sentence stating that practice is the orchestrator's responsibility and lies outside this task's files.

   A command name assembled from variables or parameter expansion remains a residual of static recognition. The example `x=g; ${x}h pr merge` assembles the command name; its visible `pr merge` still asks under this contract. An invocation whose command and gated words are all assembled, such as `x=g; y=p; z=mer; ${x}h ${y}r ${z}ge`, contains no required literal pattern and can receive no decision. Permgate and the auto-mode classifier provide the next layer. The hook's threat row and report state this residual without claiming that static recognition closes it.

8. The ruleset comparison in `scripts/orchestrator/ruleset-request.sh` and `scripts/orchestrator/ruleset-verify.sh` preserves duplicate rule types. Canonicalisation retains every rule occurrence. A map keyed only by rule type or a set that drops occurrences does not satisfy this requirement. Two differing rules of one type produce two separately reported differences, never one collapsed difference.

   `tests/unit/test_ruleset_scripts.py::test_ruleset_comparison_preserves_duplicate_rule_types` is written before the fix and records red-then-green evidence for both scripts. Its fixtures include two differing rules with the same type and assert two differences, and a duplicate-bearing expected value whose last rule matches the live value while an earlier occurrence differs or is missing. Request reports the differences and uses only GET access. Verify exits 1 and leaves the temporary progress record byte-identical. An exactly matching duplicate-bearing pair compares equal and permits only the existing temporary progress update. The regression closes the a02 independent review's `ruleset-comparison` finding at `ruleset-request.sh:59`.

## Decision row

This PR changes the permission surface. The orchestrator writes a new decision row, using the next free `D-024-NN` id, to `.orchestration/decisions.tsv` with `scope=permission approved_by=user diff_sha256=<sha>` when the final head is known. `D-024-13` is taken by the ask-rule removal of 16:27 JST. The user's directive of 2026-10-18 13:5x JST supplies the approval. The SHA is the guard's own output on `--base origin/main --head <final head>` and is pasted in the acceptance record. The worker does not edit the decision ledger.

CI wiring belongs to P1-11's regime job. Until that wiring lands, the orchestrator runs the guard at acceptance and pastes its output.

## Out of scope

The worker seats' own allow rules belong to a separate task after P1-7 merges, since that task edits `herdr-agents`. The `regime` CI job belongs to P1-11. Permgate at `home/dot_agents/permgate-policy.yaml`, any Codex boundary file, the ruleset toggles themselves and post-merge `make update` remain outside this task. The ruleset toggles and `make update` remain the operator's actions; item 2 only shows and verifies the ruleset, and deployment follows DoD2.

The SKILL sentence directing seats to write gated-word prose with the file-edit tool is the orchestrator's responsibility. No SKILL file is added to `allowed_files`. The worker does not edit predecessor task texts, predecessor evidence, acceptance records or the decision ledger. Reset bookkeeping remains the orchestrator's responsibility.

## Check

`make render-check`, `make validate-agent-assets` and `make format` pass. `shellcheck` and `shfmt -d` on the hook and the two ruleset scripts are clean. `uv run python -m unittest tests.unit.test_gh_merge_gate tests.unit.test_permission_guard tests.unit.test_ruleset_scripts tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets tests.unit.test_check_agent_runtime tests.unit.test_claude_settings_merge -v` is green.

`uv run --offline --with pyyaml python -I scripts/permission-guard.py --base origin/main --head HEAD` prints the diff SHA. Its exit 1 before the orchestrator's decision row exists is pasted as such. All commands, verbatim outputs, exit statuses and tested identities are pasted in `.orchestration/dotfiles-T133-permission-guard-gate-a03/validation.md`.

`git diff --numstat origin/main...HEAD` shows at most 650 changed lines outside `tests/`, `.orchestration/` and the regenerated template, with the hook alone about 250, and at most 700 changed lines under `tests/`. Changed lines are additions plus deletions. The final inventory and totals are recorded against the final head. Shlex and the regex engine are Python standard-library modules, and this redesign adds no dependency.

The validation includes item 0's inherited baseline, item 6's complete red-then-green evidence, the table-driven three-outcome corpus, the metacharacter property test, the duplicate-ruleset regression and the final closure table. Historical a02 formatting, validation and review-gate failures remain recorded as failures. They are not labelled passing checks.

No local Bats tests run. Required Bats results come from GitHub Actions. The orchestrator runs task-consistency-check C1 to C10 and C7b before dispatch and at acceptance.

## Completion

The existing branch continues this task and produces one PR. It remains stacked on PR #412's head `d3480fc0` until #412 merges, then rebases onto main and opens the PR. The next push contains the replacement a03 task copy. The redesign creates no fresh implementation branch and no second implementation PR. The deadline remains `2026-10-19T03:00Z`, which is 2026-10-19 12:00 JST.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's branch and dependency requirements, `dotfiles-T133-permission-guard-gate-followup-a01` as the owner of any advisory P2, and `task_copy=<sha256 of .orchestration/dotfiles-T133-permission-guard-gate-a03/task.md>` in the RESULT. The orchestrator writes that owner task before assigning its first advisory P2. Item 8's duplicate-rule defect belongs to this task and is not deferred as advisory work. Every worker-side fix round, before or after the first RESULT, counts toward INV-6 under C-61. The stopped a01 and a02 histories remain preserved.

The no-prompt directive qualifies the inherited Bot workflow. No `@codex review` comment is posted. Automatic final-head reviews are observed within the bounded 15-minute window, and absence is recorded as `bot: none`. Required CI passes before RESULT. Every feedback item is reported with its proposed disposition, and surviving P0/P1 findings stop integration under the inherited completion rule.

A Codex seat writes evidence at the same relative paths in its worktree and says so in RESULT. Worker-side review evidence uses the required `-worker-` infix. RESULT names the head, base, branch, changed files, every Bot thread and its disposition, test names, caps, new scripts, task-copy hash and evidence paths. The report distinguishes preserved a02 evidence from new final-head evidence and states the accepted prose cost and indirect-execution residual. The orchestrator copies worktree evidence by absolute path before review.

This task is `security: true`. The orchestrator runs the task-level audit and a separate security-profile review on the final head. The S1 classes are `argv-text-mismatch`, `unbound-evidence` and `fail-open-on-error`. A third finding of any one class stops the artifact for redesign and never starts a fourth round. The a02 artifact remains stopped, and this redesign does not erase its class table or recast its findings as approvals.

Final-head feedback collection, audit dispositions, acceptance and the integration gate follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh required evidence. Merge uses `gh pr merge --squash --match-head-commit <audited head>`. Commands for gh and Git writes run individually, without shell chaining or a wrapper combining writes.

Live deployment and ruleset toggles remain the operator's actions. Local Bats and live payload execution are not performed; runtime deployment remains unverified until the operator's post-merge checks. Static recognition retains the variable-assembled-name residual stated in the hook's threat row.

## Amendment 1 (round 1, 2026-10-18T23:0xZ): the Bot's three P1 on PR #420 at 6b4a832e, the scope and the test cap

The automatic Bot review 5565416782 found three P1 of three different classes (none reaches S1; the task's S1 classes stay argv-text-mismatch, unbound-evidence and fail-open-on-error): (1) 4309105816, class legacy-record-abort: a legacy acceptance record (plain prose, YAML or non-object JSON) anywhere the hook scans aborts the scan before the matching record is read; the hook reads only the named task's record `.orchestration/acceptance/<task>.md`, treats a record whose first block is not a JSON object as "no acceptance" for that task (ask), and never aborts on another task's record; the candidate record's task, head, PR and audit strictness stays as written. (2) 4309105821, class path-confinement: on the draft auto-allow path `--body-file` may name any readable file on the host; the hook allows a body file only when it is a regular, non-symlink file whose resolved path lies under the invoking Git worktree (the payload cwd's toplevel), outside `.git/`, with no `..` after resolution; anything else asks; worker drafts keep working. (3) 4309105826, class missing-input: `ruleset-verify.sh` writes to `.orchestration/plans/024-progress.tsv`, which a fresh clone lacks (the ledger is the orchestrator's live record, outside this task's files, and the task forbids editing it); the write becomes optional: `--progress <tsv>` names the ledger, and without the flag (or with an absent file) the script prints the comparison and exits with its result code only; `ruleset-request.sh` is unchanged. The fix of all three is the one worker-side fix round of Worker Playbook step 15 (not a revise), with one red-then-green test per finding in the module beside each file. The test cap is 780 lines under `tests/` for this task (the three regressions add about 60 lines; no case is removed); the source cap stays 650. This is INV-6's first amendment (C-61); the counters are pasted below.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```