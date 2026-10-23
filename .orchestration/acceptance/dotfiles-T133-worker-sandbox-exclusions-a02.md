---
{
  "format": 1,
  "task": "dotfiles-T133-worker-sandbox-exclusions-a02",
  "head": "c8c712f15cab992463b4131ba9891c634b9f764c",
  "pr": 448,
  "ledger": [
    {
      "id": "audit:232c174:401",
      "class": "contract-restatement"
    },
    {
      "id": "audit:232c174:402",
      "class": "unsupported-claim"
    },
    {
      "id": "audit:232c174:403",
      "class": "allowed-files-gap"
    },
    {
      "id": "audit:232c174:404",
      "class": "happy-path-closing-test"
    },
    {
      "id": "4330739773",
      "class": "evidence-not-committed"
    },
    {
      "id": "4330739783",
      "class": "linux-exclusion-residual"
    },
    {
      "id": "audit:c8c712f:1",
      "class": "evidence-command-missing"
    },
    {
      "id": "audit:c8c712f:2",
      "class": "unhashed-requirement-change"
    },
    {
      "id": "audit:c8c712f:3",
      "class": "counters-snapshot-missing"
    },
    {
      "id": "audit:c8c712f:4",
      "class": "sweep-attribution"
    },
    {
      "id": "audit:c8c712f:5",
      "class": "owner-scope-gap"
    }
  ],
  "searches": [],
  "audit_findings": [
    {
      "n": "1",
      "reason": "the record now carries the command form, the live probe's exit status and the bus rows for the macOS sandboxed sends (see the 2026-10-21T03:48Z line)",
      "evidence": "sqlite3 ~/.agents/skills/agmsg/db/messages.db \"select id, created_at, read_at from messages where id in (2827, 2830);\""
    },
    {
      "n": "2",
      "reason": "advisory P2 owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01 (unhashed requirement change in TASK 2863's note)",
      "evidence": "sqlite3 ~/.agents/skills/agmsg/db/messages.db \"select id from messages where id = 2863;\""
    },
    {
      "n": "3",
      "reason": "the counters snapshot is in the record (tasks=2 amendments=1 questions=0 results=2 revises=1, S2 not reached)",
      "evidence": "scripts/regime-counters.sh --history-only dotfiles-T133-worker-sandbox-exclusions-a02"
    },
    {
      "n": "4",
      "reason": "the sweep row for run 119016057346 now attributes incident 38434651 to the upstream trusted-exec result.txt merged in by the update-branch, which the PR's own diff does not touch; GitGuardian is not a required check",
      "evidence": "git diff --name-only ac816ebdbcd076ccc060c5932c46393ff46af9f7 c8c712f15cab992463b4131ba9891c634b9f764c | grep -c trusted-exec-contract-tests-a01/result.txt"
    },
    {
      "n": "5",
      "reason": "advisory P2 owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01 (Linux runtime check needs the workflow file now in its allowed_files)",
      "evidence": "grep -c regime-linux-dispatch.yml .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md"
    }
  ]
}
---

# Acceptance record: dotfiles-T133-worker-sandbox-exclusions-a02

Lineage: reset of dotfiles-T133-worker-sandbox-exclusions-a01 (INV-6 S2, two amendments before implementation, both orchestrator brief defects). Design 5.14 item 10's Claude half: empty the worker seats' excludedCommands (`agmsg-dispatch *` and the three Linux entries), regenerate the rendered Claude settings, make the validator expect the empty list, update the two tests that assert the old lists. Evidence carried by the orchestrator: this seat sent agmsg messages 2827 and 2830 on 2026-10-20 from sandboxed Bash (Claude sandbox, herdr socket allowlisted since T130); the Codex seat a013 measured `PermissionDenied` on the same socket from its sandbox (13:39Z), the Codex half's open point.

- 2026-10-20T14:03Z-14:11Z: text written whole by the review profile from the orchestrator's brief (`worker-sandbox-exclusions-a02-prompt.md`), installed, two checker fixes by the orchestrator (`reset_of` as a list; the predecessor-copy threat row C3 requires of a reset), 125 lines, self cap 140; pre-send OK, sha256 6f95aef556842405912d7a929d19b95ba95efaa8c2b0e61c72d1ae925e5cc7fc. C-80 round 1 started 14:11Z.

## Owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01

(no advisory rows yet; written 2026-10-20T14:17Z before the worker-sandbox-exclusions PR's first advisory disposition, C-51; the owner text carries the lineage's residual rows as items)
- 2026-10-20T14:21Z: C-80 round 1 one P2 (the owner text `dotfiles-T133-worker-sandbox-exclusions-followup-a01` did not exist) -> owner text written with the Linux runtime check as its item 2; round 2 `Verdict: correct` (`…-text-security-6f95aef.md.last.md`). Dispatched to a013 (TASK 2863, read 14:22:00Z) through send-task.sh at the reviewed bytes 6f95aef5…; the author omitted the fenced block under `## Checks`, so no checks were pasted (the dispatched bytes are the reviewed bytes; the pre-send output is in this record instead: checker OK, secret-pattern 0, 125 lines of 140).
- 2026-10-20T14:29:19Z: a013 PONG `status=blocked`: the prescribed offline `uv run` regeneration exits 2 because uv writes its default cache under `~/.cache/uv`, which the Codex sandbox denies (`Operation not permitted`); correct refusal, text defect (no UV_CACHE_DIR in the prescribed commands). Amendment 1 (2026-10-20T14:43Z) prefixes every prescribed uv command with an absolute private cache under $TMPDIR; C-80 round 3 on the amended bytes, then the amendment TASK. Row `worker:f7f3806:2 cache-path`.

worker:f7f3806:2	cache-path

## Lineage rows carried from dotfiles-T133-worker-sandbox-exclusions-a01

audit:232c174:401	contract-restatement
audit:232c174:402	unsupported-claim
audit:232c174:403	allowed-files-gap
audit:232c174:404	happy-path-closing-test
- 2026-10-21T02:49Z: integration start (R0-5): RESULT 2913 (a013, head 9e7e02ac, transported by the orchestrator) -> update-branch to main ac816ebd -> head 2d1d095d; the 7 required checks pass (GitGuardian fails on incident 38733942-class hash values, not required: sweep row). `result-evidence-check.sh` refuses by construction (`no validation.md at 2d1d095d`): the a02 RESULT keeps every artifact worker-local per the text's Worker item 5 and commits only code and the task copy; the evidence taken is the head's required CI, the task copy at the head equal to the dispatched bytes (9313f2cc), and the RESULT's test and cap claims (clean generator 91 tests, 3 unchanged validator regressions, ruff 18/18 baseline, Git caps 43/60 and 111/120). Predecessor a01 rows carried (R0 step 1b). Security review and task-level audit run on 2d1d095d.
- 2026-10-21T02:56Z: security-profile review of 2d1d095d: Verdict correct. Chain stopped at the sweep: two Codex Bot P1 threads on the head. 4330739773 (the threat table names report/validation/sandbox/learning/autoskill as residual controls but the PR holds only task.md) -> revise round 2, records only (a013 commits the five records and the worker crit evidence, masked; text unchanged 9313f2cc). 4330739783 (emptying linux_excluded_commands moves agmsg-dispatch into bubblewrap on a Linux Claude worker) -> not-applicable: design 5.14 item 10 orders the exclusions emptied, every seat is macOS, the Linux runtime check is owner followup-a01 item 2 whose file is at the head (the Bot reviewed 9e7e02ac before the update-branch).

4330739773	evidence-not-committed
4330739783	linux-exclusion-residual
- 2026-10-21T03:10Z: round 2 (records only): a013 PONG 2941 head c8c712f1 (48 record files, masked, independent privacy check 0, task copy unchanged 9313f2cc, production/tests delta 0/0); transported by the orchestrator (transport.sh, task-id mode). Cap accounting: the text's fixed dispatch range f7f38067...head now includes 597 upstream trusted-exec test lines merged by the update-branch (#436), so the fixed-range figure (43/708) is not the PR's own change; per C-123 the integration measures `git diff --numstat <merge-base> <head>` (the PR's own diff: 43/111 at 9e7e02ac, records only after) and records both figures. Security review and chain run again on the final head after CI.
- 2026-10-21T03:48Z: task-level audit of c8c712f1 (`.orchestration/validation/dotfiles-T133-worker-sandbox-exclusions-a02-audit-c8c712f.md`): Verdict incorrect, implementation passed (34 validator cases, hashes and caps match), five P2 (1 evidence, 3 orchestration, 1 specification), dispositioned below without a worker round. (1) evidence for the macOS sandbox claim: messages 2827 (09:53:51Z) and 2830 (10:05:50Z) were ACCEPTANCE lines the orchestrator sent through `scripts/orchestrator/dispatch.sh dotfiles-conformance claude-deep-dot <seat> <pane> <line-file>` from sandboxed Bash on macOS; their exit statuses were not captured verbatim at the time, so a live probe was taken now: the same command to codex-standard-dot-a013 exited 0 and produced bus row 2950 2026-10-21T03:48:33 read_at=2026-10-21T03:48:38. (2) TASK 2863's note waived the Codex probe the text requires at line 103: an orchestrator requirement change outside a hashed amendment (third instance of the class after C-119 and C-123) -> advisory owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01, M-20261021-04 and C-125 (the pre-send contradiction check covers the dispatch line). (3) counters at the revise decision: `scripts/regime-counters.sh --history-only dotfiles-T133-worker-sandbox-exclusions-a02` -> tasks=2 amendments=1 questions=0 results=2 withdrawn=0 revises=1 (S2 not reached; snapshot taken 2026-10-21T03:48Z). (4) the GitGuardian attribution in the sweep row was wrong: incident 38434651 sits in `.orchestration/dotfiles-T133-trusted-exec-contract-tests-a01/result.txt`, which entered the PR through the update-branch merge of main (#436); the PR's own diff ac816ebd..c8c712f1 does not touch that file (0 matches); row corrected. (5) the Linux residual owner dotfiles-T133-worker-sandbox-exclusions-followup-a01 item 2 needs a workflow file: `.github/workflows/regime-linux-dispatch.yml` added to its allowed_files (undispatched text); the advisory owner row is below.

audit:c8c712f:1	evidence-command-missing
audit:c8c712f:2	unhashed-requirement-change
audit:c8c712f:3	counters-snapshot-missing
audit:c8c712f:4	sweep-attribution
audit:c8c712f:5	owner-scope-gap

audit-finding: c8c712f:1 not-applicable:the record now carries the command form, the live probe's exit status and the bus rows for the macOS sandboxed sends (see the 2026-10-21T03:48Z line); evidence=sqlite3 ~/.agents/skills/agmsg/db/messages.db "select id, created_at, read_at from messages where id in (2827, 2830);"
audit-finding: c8c712f:2 not-applicable:advisory P2 owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01 (orchestration: TASK 2863's note waived the text's Codex probe outside a hashed amendment; the implementation and records are unaffected; C-125 adds the dispatch line to the pre-send contradiction check); evidence=sqlite3 ~/.agents/skills/agmsg/db/messages.db "select substr(body, instr(body, 'no-sandboxed-dispatch-probe'), 60) from messages where id = 2863;"
audit-finding: c8c712f:3 not-applicable:the counters snapshot is in the record (tasks=2 amendments=1 questions=0 results=2 revises=1, S2 not reached); evidence=scripts/regime-counters.sh --history-only dotfiles-T133-worker-sandbox-exclusions-a02
audit-finding: c8c712f:4 not-applicable:the sweep row for run 119016057346 now attributes incident 38434651 to the upstream trusted-exec result.txt merged in by the update-branch, which the PR's own diff does not touch; GitGuardian is not a required check; evidence=git diff --name-only ac816ebdbcd076ccc060c5932c46393ff46af9f7 c8c712f15cab992463b4131ba9891c634b9f764c | grep -c trusted-exec-contract-tests-a01/result.txt
audit-finding: c8c712f:5 not-applicable:advisory P2 owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01 (its allowed_files now include .github/workflows/regime-linux-dispatch.yml; the Linux runtime residual is its item 2); evidence=grep -c regime-linux-dispatch.yml .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md

## Owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01

audit-finding: c8c712f:2 not-applicable:advisory P2 owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01 (unhashed requirement change in TASK 2863's note); evidence=sqlite3 ~/.agents/skills/agmsg/db/messages.db "select id from messages where id = 2863;"
audit-finding: c8c712f:5 not-applicable:advisory P2 owned by dotfiles-T133-worker-sandbox-exclusions-followup-a01 (Linux runtime check needs the workflow file now in its allowed_files); evidence=grep -c regime-linux-dispatch.yml .orchestration/tasks/dotfiles-T133-worker-sandbox-exclusions-followup-a01.md

