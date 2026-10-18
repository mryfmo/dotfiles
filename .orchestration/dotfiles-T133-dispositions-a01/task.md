---
format: 2
task_id: dotfiles-T133-dispositions-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/dispositions.py
  - scripts/orchestrator/orch-gate.sh
  - tests/unit/test_dispositions.py
  - tests/unit/test_orch_gate_path.py
  - .orchestration/dotfiles-T133-dispositions-a01/**
after: []
threat_table:
  - control: "the PR adds scripts/orchestrator/dispositions.py (reads the sweep JSON and git as data, proposes fixed:<commit> or demands not-applicable per thread, verifies the three refutation forms; executes only git read commands, the named unittest selector and a fetch of the named URL; never evaluates sweep text)"
    disposition: "closed: tests/unit/test_dispositions.py::test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise"
  - control: "the PR edits scripts/orchestrator/orch-gate.sh in one place (the dispositions re-validation of PR_FEEDBACK_EVIDENCE before the gate, refusing with exit 2 under DISPOSITIONS_REQUIRE_REFUTATION=1 and reporting otherwise)"
    disposition: "closed: tests/unit/test_orch_gate_path.py::test_orch_gate_revalidates_the_dispositions_before_the_gate"
  - control: "tests/unit/test_dispositions.py (temporary repositories, a fixture sweep JSON, a stub unittest selector, a file URL for the source form)"
    disposition: "residual: fixtures are temporary repositories and files built by the test; the audit reads each case and its assertion"
  - control: "tests/unit/test_orch_gate_path.py (the one re-validation case, in the module's existing fake-binary style)"
    disposition: "residual: the fake gate records its argv and the case asserts the refusal happens before it runs; the audit reads the case"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-dispositions-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: "the branch evidence records under .orchestration/dotfiles-T133-dispositions-a01/ (report.md, validation.md, sandbox.md, learning.md)"
    disposition: "residual: prose and pasted command output; the sandbox record lists every command the sandbox refused; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, security, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: dispositions.py writes only its --out file; the test: form runs the named unittest selector of the checked-out repository, the source: form fetches the named URL read-only; the gate wrapper gains one subprocess before the gate; nothing live changes"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; dispositions.py runs under uv run --no-project python -I with the standard library only; orch-gate.sh keeps its private PATH of resolved binaries"
  - control: new or renamed scripts
    disposition: "residual: one new script, dispositions.py, named here; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: neither new file exists on origin/main
    command: git ls-files scripts/orchestrator/dispositions.py tests/unit/test_dispositions.py | wc -l
    output: |-
      0
  - claim: a sweep item of pr-feedback.py carries source, author, bot, level, path, line, body, url, the source's extra state and disposition, so the thread's commit comes from gh when the item lacks it
    command: sed -n '133,143p' scripts/pr-feedback.py | /usr/bin/grep -o '"[a-z]*"' | tr '\n' ' '
    output: |-
      "source" "author" "login" "slug" "" "bot" "level" "path" "line" "body" "" "url" "disposition" "" 
  - claim: orch-gate.sh invokes the gate once with PR_FEEDBACK_EVIDENCE, the point before which the re-validation runs
    command: /usr/bin/grep -c 'PR_FEEDBACK_EVIDENCE="${sweep}"' scripts/orchestrator/orch-gate.sh
    output: |-
      1
  - claim: the orch-gate tests live in tests/unit/test_orch_gate_path.py (fake binaries on a private PATH), the module the one new case joins
    command: /usr/bin/grep -c 'def test_orch_gate_' tests/unit/test_orch_gate_path.py
    output: |-
      3
  - claim: audit-pool.sh is not on origin/main (it is PR #410's), so the --second-opinion mode of programs item (16) is a later task
    command: git ls-files scripts/orchestrator/audit-pool.sh | wc -l
    output: |-
      0
  - claim: the gate already holds the disposition and commit validators dispositions.py reuses
    command: /usr/bin/grep -n 'def commit_in_range\|def parse_disposition' scripts/require-crit-review.py | cut -c1-24
    output: |-
      389:def commit_in_range(
      397:def parse_disposition(
---

# AGMSG-TASK dotfiles-T133-dispositions-a01 — disposition candidates and refutation forms (plan 024 P1-10, programs item (5); the item (16) second opinion is a later task)

Written 2026-10-18 by the orchestrator seat from plan 024 (`024-todo.md` row P1-10, `024-design-programs.md` item (5), `024-design-quality.md` 5.13 refutation forms). Today every Bot thread's disposition is typed by hand into an extra TSV; this tool proposes `fixed:<commit>` from git and refuses an empty not-applicable. Seat: a Claude seat.

## Goal

For a PR head, every review-comment item of the sweep gets a machine proposal: `fixed:<commit>` when a commit between the thread's commit and the head touches the thread's hunk, otherwise a demand for `not-applicable:` with one of the three refutation forms. The gate wrapper re-validates the saved dispositions in that mode before the gate runs.

## Files

1. `scripts/orchestrator/dispositions.py <pr> <head> --feedback <sweep.json> [--out <json>] [--require-refutation] [--commits <json>]` (new, Python, `python -I`, standard library only, shdoc-style module docstring in English). For each item with `source` `review_comment` (and each badged `review` item that names a path and line): the thread's commit is the item's `original_commit_id` when the sweep carries it, else `--commits <json>` (a map url → commit, the test and cache form), else `gh api repos/{owner}/{repo}/pulls/comments/<id> --jq .original_commit_id` (gh resolved from PATH; a failure is a hold line, never a guess). `git diff <commit>..<head> -- <path>` is parsed for a hunk whose new-side or old-side range covers `line`; when one exists, `git log --format=%H <commit>..<head> -- <path>` is walked to the newest commit whose diff against its parent touches that range, and the proposal is `fixed:<that commit>`; otherwise the proposal is `not-applicable:` with an empty reason to be filled. The output JSON (`--out`, default stdout) is the sweep with `proposal` added per item and the existing `disposition` untouched. Refutation forms for a not-applicable disposition (5.13): `test:<selector>` (the selector runs as `uv run --no-project python -m unittest <selector>` in the checkout, and the form is accepted only on exit 0, with the run's last line recorded), `source:{url, fetched_at, quote}` (the URL is fetched, the quote must occur in the page text, the page's sha256 is recorded; `file://` URLs are accepted for tests), `diff:<range>` (accepted only when `git diff <range> -- <path>` has no hunk covering the line). `--require-refutation` exits 1 and prints one line per not-applicable disposition that carries none of the three forms or whose form fails verification; the `evidence=<command>` form used by today's records is reported as `legacy-evidence` and counts as a failure only under `--require-refutation`. Exit codes: 0 ok, 1 a disposition failed the requirement, 2 usage or a hold (gh failure, unreadable sweep).
2. `scripts/orchestrator/orch-gate.sh`: before the gate runs, one step `dispositions.py <pr> <head> --feedback "${sweep}" --require-refutation` under `DISPOSITIONS_REQUIRE_REFUTATION=1` refuses with exit 2 and the tool's lines; without the variable the same command runs without `--require-refutation` and its lines are printed as a report (the records of today's PRs still carry the legacy form; the flip is a decision row). The PR number and head come from the wrapper's existing arguments; the step uses the wrapper's private PATH.
3. Tests `tests/unit/test_dispositions.py`: `test_dispositions_proposes_fixed_for_a_changed_hunk_and_demands_not_applicable_otherwise` (a temporary repository: a thread commit, a fix commit touching the line, a head; the proposal names the fix commit; a second thread on an untouched line gets the not-applicable demand; `--commits` supplies the commits), `test_require_refutation_fails_without_a_form_and_accepts_each_of_the_three` (the legacy `evidence=` form fails; `test:` with a stub selector that passes is accepted and one that fails is refused; `source:` with a `file://` page containing the quote is accepted and a missing quote refused; `diff:` with an untouched range is accepted and a touching range refused), `test_dispositions_holds_on_an_unreadable_sweep_or_a_missing_commit` (exit 2 with the reason). `tests/unit/test_orch_gate_path.py::test_orch_gate_revalidates_the_dispositions_before_the_gate` (in the module's fake-binary style: with `DISPOSITIONS_REQUIRE_REFUTATION=1` and a sweep whose not-applicable lacks a form, the wrapper exits 2 and the fake gate records no run; without the variable the fake gate runs and the report line is printed). Fixture lines count against the test cap.
4. `report.md` states the proposal rule, the three forms and their verification, the legacy-evidence transition (how many of today's records carry it: `grep -l "evidence=" .orchestration/validation/*-pr-feedback.json | wc -l`, pasted), and the later task for item (16) (`audit-pool.sh --second-opinion`, after PR #410).

## Out of scope

`audit-pool.sh --second-opinion` (item (16), after PR #410 merges), `scripts/require-crit-review.py` (its validators are imported or re-implemented read-only, not edited), `fill_sweep.py` and `pr-feedback.py` (the sweep stays as it is), the chain scripts (they call the gate wrapper), flipping `DISPOSITIONS_REQUIRE_REFUTATION` (a decision row).

## Check

`make format`, `uv run python -m unittest tests.unit.test_dispositions tests.unit.test_orch_gate_path -v` green, `shellcheck` and `shfmt -d` on orch-gate.sh clean, `uv run --no-project python -I scripts/orchestrator/dispositions.py 409 4fe243803971bd5ba8ab45f8ede5cfb4dd37f719 --feedback .orchestration/validation/dotfiles-T133-ci-efficiency-a02-pr-feedback.json` run once with its output pasted (a real sweep; `gh` resolves the thread commits), all pasted in `.orchestration/dotfiles-T133-dispositions-a01/validation.md`, with `git diff --numstat origin/main...HEAD`: at most 350 changed lines outside `tests/` and `.orchestration/`, 450 under `tests/`.

## Completion

One PR from a fresh branch off `origin/main`. The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies as written, with `dotfiles-T133-dispositions-followup-a01` as the owner of any advisory P2 (written by the orchestrator when the first one appears) and `task_copy=<sha256 of .orchestration/dotfiles-T133-dispositions-a01/task.md>` in the RESULT; the RESULT also carries `precheck=` when `scripts/orchestrator/result-precheck.sh` has merged (PR #411), else `precheck=pending-411`. `security: true`: the orchestrator runs the task-level audit and the security-profile review on the final head. No `@codex review` comment; single commands for every gh and git write; a classifier denial is a blocked PONG. Until P1-14 lands, any string containing the words gh pr merge or gh pr create is written with the file-edit tool, never in a Bash heredoc or echo.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T133-dispositions-a01.md: OK
premises 1 to 6: outputs pasted at write time (2026-10-18 22:4x JST)
masked 0 match(es) in .orchestration/tasks/dotfiles-T133-dispositions-a01.md
```
