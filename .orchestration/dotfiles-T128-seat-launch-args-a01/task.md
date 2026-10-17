---
format: 2
task_id: dotfiles-T128-seat-launch-args-a01
kind: code
security: false
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round22.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - scripts/orchestrator/seat-args.sh
  - scripts/check-regime-boundary.sh
  - tests/unit/test_seat_args.py
  - tests/unit/test_check_regime_boundary.py
  - .orchestration/dotfiles-T128-seat-launch-args-a01/**
after: []
threat_table:
  - control: the PR adds scripts/orchestrator/seat-args.sh, which compares a seated worker's live process arguments with its profile's rendered launch arguments, reports a seat not started by the launcher, and reports a missing probe binary as a skip
    disposition: "closed: tests/unit/test_seat_args.py::test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one"
  - control: the PR edits scripts/check-regime-boundary.sh in one place (the seated-worker loop runs seat-args.sh for each seated identity at a linked worktree and reports its non-zero result as a violation)
    disposition: "closed: tests/unit/test_check_regime_boundary.py::test_a_seated_worker_without_its_profile_arguments_is_a_violation"
  - control: the PR adds tests/unit/test_seat_args.py, the oracle of the first row (stub ps and lsof binaries printing fixture lines, a fixture model-profiles.env under a temporary HOME; no real process is read)
    disposition: "residual: the stubs print and record, nothing else; the audit reads each case against the Files items"
  - control: the PR edits tests/unit/test_check_regime_boundary.py only for the new case and for its harness, which copies the new script beside the boundary script
    disposition: "residual: one new test beside the existing ones, which stay; the harness change is the copy of one more script"
  - control: "the process list and the cwd lookup as inputs (/bin/ps and /usr/sbin/lsof)"
    disposition: "residual: read-only probes of this machine; the script signals, writes and changes nothing, and its output names pids and argv only; SEAT_ARGS_PS and SEAT_ARGS_LSOF, the test seams, replace the two binaries and are set only by the tests"
  - control: "the rendered profile file (~/.agents/model-profiles.env) as an input"
    disposition: "residual: read by a plain line parse of KEY=\"value\" by exact key, never sourced or eval'd, so a value is compared as text and cannot run (the first row's case with a command substitution in the value)"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T128-seat-launch-args-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance"
  - control: the branch evidence records under .orchestration/dotfiles-T128-seat-launch-args-a01/ (report.md, validation.md, sandbox.md, learning.md)
    disposition: "residual: prose and pasted command output; the sandbox record lists every permission-gated command; the audit reads them"
  - control: "task metadata (the front matter of the task copy: kind, allowed_files, threat_table, premises)"
    disposition: "residual: read with PyYAML by the task-consistency check C1 to C10 and C7b before dispatch and at acceptance; a changed field fails the byte comparison above"
  - control: metadata separators (the --- lines that bound the front matter of the task copy and of every evidence record)
    disposition: "residual: PyYAML splits on the first document only and the byte comparison covers the whole file"
  - control: in-process effects
    disposition: "residual: the tests run seat-args.sh and check-regime-boundary.sh as subprocesses with stub ps, lsof and identities.sh and import only the standard library; nothing is imported into another process"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: no workflow or interpreter file is in allowed_files; seat-args.sh runs /bin/ps and /usr/sbin/lsof by absolute path (the seams above in the tests) and awk, sed, cut, tr and grep from PATH as check-regime-boundary.sh does today; check-regime-boundary.sh runs seat-args.sh by the path beside itself (its own root, never the caller's directory); a PR checkout as cwd chooses nothing: neither script reads a file relative to cwd"
  - control: new or renamed scripts
    disposition: "residual: 1 new script under scripts/orchestrator, named in allowed_files and listed in the RESULT; any other new or renamed script is an undeclared change the audit fails"
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
premises:
  - claim: 'seat-args.sh does not exist on origin/main'
    command: 'git cat-file -e origin/main:scripts/orchestrator/seat-args.sh 2>/dev/null && echo present || echo absent'
    output: |-
      absent
  - claim: 'the boundary check on origin/main knows no seat-args'
    command: 'git show origin/main:scripts/check-regime-boundary.sh | /usr/bin/grep -c seat-args'
    output: |-
      0
  - claim: 'the rule that a profile change activates by a re-seat is in the SKILL on origin/main (this task is its tool half)'
    command: 'git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "Activate a worker model or profile change"'
    output: |-
      1
---

# AGMSG-TASK dotfiles-T128-seat-launch-args-a01 — a seated worker's live launch arguments compared with its rendered profile (C-60; the operator's question of 2026-10-17)

Written 2026-10-17 by the orchestrator seat after the operator's question 「なぜ、作業役のeffortがmidiumになっているのか　ルール化しているが勝手に変えるのか」 (M-20261017-05): two Claude worker seats had run since 2026-10-15 as `claude --resume <session>` processes with no `--model` or `--effort` argument while the manifest, the rendered `~/.agents/model-profiles.env`, the Codex profile configs and the user settings all read xhigh; the regime's checks read identities, panes and placement records, never a process. This task is C-60's tool half: a script that reads a seated worker's live process and compares it with the profile its identity names, run by the Stop checklist's check for every seated worker. The dispatcher's refusal of a TASK line to such a seat is the tools lineage's row (`C-60:1 tool-half` under `dotfiles-T128-orchestrator-tools-followup-a04`), pending; the `herdr-agents --attach` summary line is out of scope.

## Goal

`make check-regime-boundary` names every seated worker whose live process does not carry its profile's launch arguments, a resumed seat included, so a seat running outside the manifest is visible at every boundary and on demand.

## Files

1. `scripts/orchestrator/seat-args.sh <teams> <identity> <agent type> <project path>` (new; `<teams>` is the comma-separated list of the teams the identity has rows in at that path, since one name may sit in several teams while the launcher names the session after the one team it spawned in): the identity's grammar is `<kind>-<profile>-<suffix>[-aNNN]` (`claude-review-dot-a005`: kind claude, profile review; `codex-standard-dot-a004`: kind codex, profile standard), and a name not of that form prints `seat <identity> args=unknown-identity` and exits 2; the agent type is `claude-code` or `codex` (identities.sh's type column) and must agree with the kind. The expected arguments come from `${HOME}/.agents/model-profiles.env`, read by a plain line parse of `KEY="value"` by the exact key `MODEL_PROFILE_<PROFILE upper-cased>_<KIND upper-cased>_ARGS` (never sourced or eval'd): for claude every `--flag value` pair of the value, for codex the one pair `--profile <profile>`; a missing key prints `seat <identity> profile=<profile> kind=<kind> args=unknown-profile` and exits 2. The live process comes from `/bin/ps -axo pid=,command=` (or the binary `SEAT_ARGS_PS` names when set, the test seam); the cwd lookup is `/usr/sbin/lsof`, else `/usr/bin/lsof` (or `SEAT_ARGS_LSOF`); when the ps binary, or for a codex seat the lsof binary, is absent or not executable the script prints `seat <identity> profile=<profile> kind=<kind> args=unknown-probe` and exits 4, the skip the boundary loop honours: for claude the process whose command's first word is `claude` or ends in `/claude` and whose arguments hold the token `-n` followed by `<team>-<identity>` for any team of the list (the session name `spawn.sh` builds from the one team it spawned in); for codex the process whose first word is `codex` or ends in `/codex`, or is `node` followed by a path ending in `/codex` (the npm wrapper), and whose cwd, read as `/usr/sbin/lsof -a -p <pid> -d cwd -Fn` (or `SEAT_ARGS_LSOF`), is the project path; the first match in pid order is taken. The result is one stdout line and one exit code: `seat <identity> profile=<profile> kind=<kind> process=<pid> args=ok` and exit 0 when every expected pair occurs adjacent in the process's arguments; `… process=<pid> args=differs expected=<the pairs, space-joined> found=<the arguments>` and exit 2 otherwise; `… process=none args=unlaunched` and exit 3 when no process matches: for claude the mark of a seat started by a bare `claude --resume` instead of the launcher (no `-n` token), for codex the absence of any codex process at the project path; a codex process at the project path started by a bare `codex resume` matches the selector and is reported `args=differs` (no `--profile <profile>` pair), exit 2, so both forms of an unlaunched seat are violations, under the two different lines. The script reads no file relative to cwd, writes nothing and signals nothing; its exit codes are 0 ok, 2 differs or an unknown identity or profile, 3 unlaunched, 4 unknown-probe.
2. `scripts/check-regime-boundary.sh`: in the loop over the linked worktrees (today lines 114 to 139), for each distinct seated name per agent type at a worktree under `.claude/worktrees/` (the identities.sh rows `<team>\t<name>` grouped by name, their teams joined by commas, so a name with rows in several teams is probed once), run `"${root}/scripts/orchestrator/seat-args.sh" <teams> <name> <type> <checkout>` and append `worker <name> at <worktree>: <its stdout line>` to the violations on exit 2 or 3, and skip it on exit 4 (`args=unknown-probe`, the missing-tool rule); the existing "worker still seated" and "pane is gone" lines stay as they are; a missing or non-executable seat-args.sh, or a missing `${HOME}/.agents/model-profiles.env`, skips the probe, as the script's other missing tools skip theirs (the existing boundary tests write no env under their HOME and so stay unchanged); the orchestrator's own seat at the main checkout is not probed (the Herdr pane's claude carries no `-n` and is started by the operator). The header comment names the new check in one clause.
3. `tests/unit/test_seat_args.py` (new), run by `uv run python -m unittest` without PyYAML, importing only the standard library: stub `ps` and `lsof` binaries that print fixture lines (`lsof` prints `p<pid>` and `n<cwd>` for the pid it is asked about), a fixture `model-profiles.env` under a temporary HOME, the script run as a subprocess with `SEAT_ARGS_PS` and `SEAT_ARGS_LSOF` set; `test_seat_args_reports_a_resumed_seat_a_differing_seat_and_a_matching_one` with these cases as subTests: (a) a claude process `claude --model claude-opus-5-5 --effort xhigh --advisor fable -n t-claude-standard-dot-a001 /agmsg actas …` with the env value `--model claude-opus-5-5 --effort xhigh --advisor fable`: `args=ok`, exit 0, also when the teams argument is `other,t` (the name's second team is the spawn team) and `args=unlaunched` when it is `other` alone; (b) the only claude process is `claude --resume abc`: `process=none args=unlaunched`, exit 3; (c) the process carries `--effort high`: `args=differs`, exit 2, the line naming the expected pairs and the found arguments; (d) codex: two codex processes, the decoy `codex --profile review …` at another cwd with the lower pid and `codex --profile standard …` at the project path with the higher pid, the project path's taken by cwd and the decoy not (an implementation ignoring cwd and taking the first pid fails here): `args=ok`; the same two with the project path's process carrying `--profile review`: `args=differs`; and a bare `codex resume` at the project path: `args=differs`, exit 2; (e) no key for the profile: `args=unknown-profile`, exit 2; (f) the env value `"$(touch pwned)"` is compared as text (`args=differs`) and no `pwned` file appears; (g) an identity `claude-a005` (no profile field): `args=unknown-identity`, exit 2; (h) `SEAT_ARGS_PS` naming a missing binary, and for a codex seat `SEAT_ARGS_LSOF` missing: `args=unknown-probe`, exit 4.
4. `tests/unit/test_check_regime_boundary.py`: the harness (`setUp`) copies `scripts/orchestrator/seat-args.sh` into the temporary checkout's `scripts/orchestrator/` beside the two scripts it copies today, and writes no `.agents/model-profiles.env` under the test HOME, so the existing tests run no probe and keep their exact assertions; `test_a_seated_worker_without_its_profile_arguments_is_a_violation`: the stub `identities.sh` of the existing pane-state test's form seats `claude-standard-dot-a009` at `.claude/worktrees/b1` with two rows, teams `dotfiles` and `other`, this test alone writes `.agents/model-profiles.env` under the test HOME with `MODEL_PROFILE_STANDARD_CLAUDE_ARGS`, and `SEAT_ARGS_PS` names a stub `ps`: with `claude --resume x` the `--report` output holds the line `worker claude-standard-dot-a009 at .claude/worktrees/b1: seat claude-standard-dot-a009 profile=standard kind=claude process=none args=unlaunched`; with a matching process (the `-n other-claude-standard-dot-a009` token, the second team's, and the pairs) it does not, and the line appears at most once however many rows the name has; with `SEAT_ARGS_PS` naming a missing binary no seat-args line appears (the skip); the "worker still seated" line is present in all three. The existing tests stay.

## Out of scope

The `herdr-agents --attach` summary line; `scripts/orchestrator/dispatch.sh` (the tools a04 row `C-60:1`); the orchestrator seat at the main checkout; the manifest, the generator and the rendered env; the re-seat itself (the operator's step, C-60 method 1).

## Check

`uv run python -m unittest tests/unit/test_seat_args.py tests/unit/test_check_regime_boundary.py -v` green, pasted in the validation file with `shellcheck scripts/orchestrator/seat-args.sh scripts/check-regime-boundary.sh` and `git diff --numstat origin/main...HEAD`: at most 200 changed lines (added plus deleted) outside `tests/` and outside `.orchestration/` (plan 021 step 7.2) and 1000 added lines under `tests/` (INV-2).

## Change (round 1, 2026-10-17T03:25:01Z)

The Codex half's round 1 (P2 ×4, P3): the Completion clause copied from the gate task named that task's copy path and owner (now this task's); a bare `codex resume` at the project path matches the selector and is `args=differs`, stated as such; the codex decoy has the lower pid so a cwd-blind implementation fails the case; the probe runs only when the rendered env exists, so the existing boundary tests stay unchanged; the pasted checks section added. Nothing else changes from `3caa21ba`.

## Change (round 2, 2026-10-17T03:33:26Z)

The review seat's round 1 (a003; P2, P3): a name may have rows in several teams while the launcher names the session after its spawn team, so the script takes the comma-joined teams and accepts `-n <any of them>-<identity>`, and the boundary loop probes each name once (cases added in items 3 and 4); a missing ps or lsof binary is `args=unknown-probe`, exit 4, the skip the boundary loop honours, and lsof is looked up at /usr/sbin then /usr/bin. Nothing else changes from `4171f67c`.

## Checks (pasted by the orchestrator before each send)

```
dotfiles-T128-seat-launch-args-a01.md: OK
premise 1: OK
premise 2: OK
premise 3: OK
masked 0 match(es) in .orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md
```

## Completion

One PR from a fresh branch off `origin/main` (after PR #376 merged as f7847616; no other merge is a precondition). The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the Bot's review of the final head is in (at PR open, and once more on `@codex review` after a P0/P1 fix round: plan 020 step 2), every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the outputs above, and the RESULT names every P0/P1 thread with `fixed:<sha>` and every P2 thread with the disposition the worker proposes; the orchestrator's audit of the final head is dispositioned finding by finding before the gate, and a P0/P1 it leaves is the operator's decision. The Bot's P0 and P1 get at most one fix round, worker-side before the RESULT, each named `fixed:<sha>` in the RESULT; a P0 or P1 that survives the round is listed as `open:<thread id>` with `bot_rounds=2` (the Bot's review at PR open and its re-review after the fix round), stops the PR and goes to the operator as a decision; a P2 on this PR's own change whose fix stays within `allowed_files` and is small (one flag or a few lines plus one test) is fixed in a revise round the orchestrator sends with a `check=` while INV-6's counts allow it (C-50); any other P2 is advisory, owned by `dotfiles-T128-seat-launch-args-followup-a01`, which the orchestrator writes when the first advisory P2 appears, before the PR's dispositions (C-51), and recorded under `## Owned by dotfiles-T128-seat-launch-args-followup-a01` in this task's acceptance record. The third finding of one class on this PR stops the rounds until the orchestrator's `re-plan:` line (C-59). The orchestrator integrates (local review once per head, sweep, audit, gate) and merges with `gh pr merge --squash --match-head-commit <audited head>`. The RESULT names head, base, branch, files, every Bot thread with its disposition, the test names, the caps, `task_copy=<sha256 of .orchestration/dotfiles-T128-seat-launch-args-a01/task.md>` and the evidence paths.
