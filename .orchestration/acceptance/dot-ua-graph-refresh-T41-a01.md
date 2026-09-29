# Acceptance: dot-ua-graph-refresh-T41-a01

Dispatched 2026-09-29 (task_commit 72b8901). PONG blocked 11:00Z–11:03Z:
the incremental path (ARCHITECTURE_UPDATE, analyze=30) blocked at
`merge-batch-graphs` because the symbol gate has no shell parser and marks
13 unchanged `.sh` symbols (aws_cli.sh, dependencies.sh, check-tools.sh)
`unknown`. Ruling 11:03Z: (b) full rebuild, skip the futile retry, record the
failure and the upstream-issue proposal.

## Round 1 — RESULT 11:34Z (revision 1, head c3afc7a, PR #212)

Worker report: full rebuild 365 files / 31 batches, assemble review
recovered 3 apparmor_userns.sh functions, core validateGraph 844/844 nodes,
1198/1198 edges, 0 issues; before → after 853/1219 → 844/1198; 50 dispatches
(15 incremental + 35 full), 3,726,712 subagent tokens; only the three `.ua`
files in the commit; `.gitignore` already carries the two ignored paths.

Orchestrator review (origin refs): base ancestry ok; merge-tree keeps the
T42 task file main added after the branch point; the three `.ua` files only;
meta.gitCommitHash 72b8901; 0 non-tuple lineRange; masker finds 0 secret
matches in the graph; CI all pass; CompactionDB records 6704a725 and
16001714 present.

**Refutation that succeeded:** a per-file comparison of function+class nodes
between the current graph (7b69b1e) and c3afc7a shows 8 files whose source
still holds the definitions but lost nodes, 35 symbols in total:
`.claude/contextdb/contextdb/storage.py` 19→1 (34 def-like lines),
`attach_comment_files.py` 24→14, `executable_agent-fanout` 2→1,
`server/history.sh` 1→0, `docker.sh` 3→2, `tailscale.sh` 2→1, `zed.sh` 3→2,
`run_bashcov_unit_test.rb` 3→1. The 853→844 delta hid this behind 26 genuine
additions (pr-feedback.py, sandbox functions, apparmor_userns.sh). Structural
validation cannot see extraction loss; the report did not mention it.

Codex audit of c3afc7a (`…-audit.md`): `Verdict: incorrect`, one P2 — "the
rebuild deletes 35 still-existing symbol nodes across eight unchanged source
files (including 18 ContextStore methods) and 86 associated edges … the
report omits this coverage regression, which schema validation cannot
detect." Independently corroborates the orchestrator finding; disposition:
revise. "CI unavailable to the auditor" → verified by the orchestrator.

**Decision (round 1): REVISE** (sent 11:5xZ, read). Revision 2 on the same
branch: re-analyze exactly those 8 files with previousSymbols, re-merge,
re-run assemble review and validateGraph, and add a per-file table (old
symbol nodes, new symbol nodes, def-like lines at head) for every file in
both graphs proving no unexplained decrease.

[memory:failure] T41 r1: a full Understand-Anything rebuild can silently
under-extract symbols in some batches (35 nodes / 86 edges lost across 8
unchanged files) while core validateGraph reports 0 issues; graph acceptance
needs a per-file symbol-count comparison against the previous graph.

## Round 2 — RESULT 11:57Z (revision 2, head 7ee3658, PR #212)

Worker: targeted re-analysis of the 8 files in three batches (46/46 and
11/11 previousSymbols re-emitted, plus 6 qualifying ContextStore methods the
old graph lacked), re-merge 885/1325, second assemble review (languageNotes
on 2 nodes only), core validateGraph 885/885, 1325/1325, 0 issues; per-file
table for all 360 files in both graphs: 0 rows with rev2 < old; meta.json
unchanged (72b8901); +3 dispatches (53 total, 3,959,434 subagent tokens);
new `[memory:failure]` 69a96c4c and a learning candidate to gate graph
commits on the per-file comparison.

Orchestrator re-derivation on the head's graph: 885 nodes / 1325 edges;
0 files with fewer function+class nodes than the old graph; 0 old node IDs
missing; 0 non-tuple lineRange; 0 dangling edges; masker 0 secret matches;
rev2 commit touches only knowledge-graph.json and fingerprints.json; the
361-row table is present in the validation file; 27 net-new symbol nodes
include six real storage.py methods (`export_events`, `recent_files`,
`secure_storage_files`, …). CI all pass. CompactionDB 6704a725, 16001714,
69a96c4c present.

Codex audit of 7ee3658 (`…-audit-rev2.md`): no findings, `Verdict: correct`
("source-matched symbols and call edges, preserved existing nodes/edges,
validateGraph zero issues"); "CI unavailable to the auditor" → verified by
the orchestrator. Round-1 P2 dispositioned: fixed in 7ee3658.

## Review guard

crit-data evidence `dot-ua-graph-refresh-T41-a01-crit.json`, receipt
`…-receipt.md`; guard record below.

## Decision

**Decision: ACCEPTED (revision 2)** (2026-09-29). Squash-merge PR #212
without `--delete-branch`. The graph is current at 72b8901; T42 (security
profile model) will move code again, so the next refresh is due after the
T42/T40 batch. Follow-ups: the worker's learning candidate (per-file symbol
gate for graph commits) becomes a rule/check task; the upstream issue on the
`.sh` symbol gate needs operator OK before filing.

[memory:decision] T41 accepted: the `.ua/` graph is rebuilt in full at
72b8901 (885 nodes / 1325 edges) after the incremental path blocked on the
plugin's shell-less symbol gate; graph acceptance now requires a per-file
function+class node comparison against the previous graph (operator
2026-09-29).

cost: worker-reported 53 dispatches (15 incremental + 35 full + 3 repair), 3,959,434 subagent tokens; orchestrating session n/a; two audit-lane runs.

## Review guard record

```
$ AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dot-ua-graph-refresh-T41-a01-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit 0
```
