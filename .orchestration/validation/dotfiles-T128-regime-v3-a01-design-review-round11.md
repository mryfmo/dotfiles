---
reviewed_at: 2026-10-10T22:54:26Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@07b621d1fe2f0a5616b39b87807df0d08b06243cd6060cdc680f894d2b353eeb
design_hash_kind: whole-file sha256 (the canonical hash tool is V1's deliverable)
task: dotfiles-T128-design-review-a01
round: 11
previous: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round9.md
supersedes_round: 10 (its findings are folded in here; no round-10 receipt was written because v11 replaced v10 before the round-10 review closed)
premises:
  1: holds (uv run --no-project --with jsonschema --with pyyaml prints 4.26.0 6.0.3)
  2: holds (troubleshooting and events pages)
  3: holds for the CLI part; the server-side strict flag rests on the fact sheet's source read
  4: holds (headless page)
  5: holds (best-practices page, verbatim)
  6: holds (stat and history)
  7: holds (both hooks pages)
  8: holds (5168 usage entries in the named transcript)
  9: holds (20 rows by default; the whole history with a limit)
  10: holds (events page, workflow_dispatch sentence)
  11: holds (headless page, the --add-dir skills exception)
  12: holds (auto-mode-config page; the rewording caveat is now in INV-1)
  13: holds (securely-using-pull_request_target page: "GitHub adds a default policy that blocks workflows triggered by pull_request_target"; "On November 2, 2026, GitHub will enforce the default policy for affected repositories"; "Currently runs in evaluate mode"; "create or update an applicable Actions event policy that explicitly allows pull_request_target"; does not apply to private or internal repositories)
---

# Design review: dotfiles-T128-regime-v3-a01, round 11 (INV-1 guard wording, INV-12 two-mode main-tests, V0; round 10 folded in)

## Round 10 items, confirmed in v11

- INV-1: the waiver's owner is V3a (implementing_tasks maps V3a to INV-6 and INV-1; the V3a bullet names the script and the ask rule and declares the four-boundary operator PR with a Codex security review); the record lives under $XDG_STATE_HOME/regime/waivers/ outside the sandbox write roots; v11 states the directory as the guard and the ask rule as the second layer. Accepted.
- INV-5: refusal clause restored inside the sentence (any file under .claude/, exit 2 blocked, codex path); one valid audit per head with a stale manifest replaced by a new audit of the same head; the runner computes the input manifest and overwrites a model-supplied value. Accepted.
- INV-2: a -contract-a01 task id is compared with its implementing task's entry. Accepted.
- INV-6: the release path names the state directory. Accepted.
- The 2026-11-02 Actions policy: premise 13 holds on the cited page; the operator action is named in V1c (line 53) and in section 9. Accepted.

## Round 11

INV-1: accepted (above).

INV-12: rejected on two clauses of the two-mode rule; the rule itself is the right union of the round-9 split and the Codex contract-first ask.
(a) Dormant forever: nothing says when a contract stops being dormant. As written, a contract merged in <task>-contract-a01 skips in ordinary CI before and after the implementation lands, so the rule it pins is tested only on the implementation PR's main-tests run. Right: the implementation PR removes the contract decorator from the tests it satisfies (its allowed_files already lists the module), so they become ordinary tests on merge; main-tests on that PR still runs main's dormant copy. One clause.
(b) Empty contract: a design-tier implementation PR whose declared script has no contract test on main runs nothing for that script in mode (b) and passes, so "contract PRs required for design-tier waves" has no enforcement. Right: main-tests fails a design-tier task.md (tier from the copy, --print-tier) when a declared module on main contains no contract test. One clause.
Note for V0: the module for a declared script should be taken from the task.md's allowed_files entries under tests/unit/, not from a stem rule (see the task-review receipt), and the undeclared mode should run every other main module rather than a mapped one, so a script with no module cannot slip through.

INV-2, INV-3, INV-4, INV-5, INV-6, INV-7, INV-8, INV-9, INV-10, INV-11: accepted; INV-2 and INV-5 verified byte-identical through the task files, INV-6 by its v10 clause, the others not byte-diffed against v10 and stated by the Round-11 section as unchanged.

## Process note

Eleven Claude rounds and three Codex rounds on one design, with round 10 superseded before its review closed and round 11 dispatched while round 10 was in progress. Each design edit now costs two receipts, a boundary push and a pointer update in five task files. The next revision should wait for both reviewers' round-11 results, fold them with the Codex items, and go out once; a round dispatched while the previous one is open is the amendment pattern INV-4 counts.

Design verdict: revise
