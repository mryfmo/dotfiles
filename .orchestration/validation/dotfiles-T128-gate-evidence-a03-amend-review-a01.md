---
reviewed_at: 2026-10-13T01:30:27Z
reviewer: claude-review-dot-a001
profile: review
session: 2089b04f-f9c7-498b-86c5-76f2140048d5
design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md@20d0937b9f7c6adebe6e4d5e6ad26ceb3578ae9b050bdce4f353b0a00ce9504a
task: dotfiles-T128-gate-evidence-a03-amend-review-a01
round: 2
task_file: dotfiles-T128-gate-evidence-a03-amend-review-a01@114b50af6c3361a9a7c20295c08ff53eaeac45d84c79b5cefbc8e93b25d3bf49
files:
  - dotfiles-T128-gate-evidence-a03@e8cfe390315dc3053d271a4e849febb896ff60f3a19ca5f2959f4644178935a4
previous: main 3709a6d8 copy 686806a1b6cff143 (pre-amendment)
verdicts:
  dotfiles-T128-gate-evidence-a03: confirm
---

# Amendment review: dotfiles-T128-gate-evidence-a03 amendment 1 (plan 013 A′), review-seat half, round 2

Round 1 was the Codex half alone; its P1 (no fails-when-removed test for the parse_constant refusal) is applied in this version: item 3 adds acceptance-nan.md ("pr": NaN, refused with `acceptance record: non-finite number`), nine fixtures under 120 lines, at least nine new tests, and item 2 names the refusal text. The bus line of 01:26:03Z (empty hash fields, M-20261012-26) is void; this receipt reviews the hashes the 01:29:41Z line carries, both recomputed and equal.

Stop condition, each point:

1. Diff against main's copy (git diff origin/main, numstat 8 added, 4 removed): the environment-inputs row (line 42), the ACCEPTANCE_EVIDENCE row (line 47, "JSON block"), item 2 (line 87), item 3 (line 88) and the Amendment 1 section (lines 102 to 105). Nothing else: reset_of, allowed_files, the copy rows (a01, a02, a03) and the a03 evidence directory are byte-identical to main.
2. The three threads close by construction: 4250238729 by object_pairs_hook (a duplicate key never reaches validation, refused with the named text); 4250238714 by the triple task/head/pr checked together, pr against PR_FEEDBACK_EVIDENCE's, with its own refusal text and fixture; 4250238721 by json (standard library) and pathlib, no uv, no third-party package, no subprocess, no online retry. INV-1: json.loads is a library parser, not a hand-written one, and the block is a flow mapping any YAML 1.2 reader (T718's jq path, item 3 of dotfiles-T128-orchestrator-tools-a01, agrees). INV-12: every refusal now has a fixture. Plan 011 F's field checks are unchanged; only its word "PyYAML" is superseded, as the Amendment 1 section says.
3. Checker on a copy named after the task id: OK (C1 to C10); C7b: the six allowed_files entries have one row each (lines 21, 23, 25, 31, 43, 45).

## Findings

- P3 0.7 .orchestration/tasks/dotfiles-T128-gate-evidence-a03.md:42 — the row states "C-26's check C11 replays this on the head" as an existing mechanism; C-26 and index.yaml list C11 as "T704, proposed; scratchpad replay". Say "C-26's proposed check C11 (scratchpad replay until T704 lands)". Same row, "adds no host binary call": the head comparison resolves HEAD through git, the gate's existing binary (run_git), so "no host binary beyond git, which the gate already runs" is the true sentence.
- P3 0.7 .orchestration/tasks/dotfiles-T128-gate-evidence-a03.md:87 — the S6 set is "a line that begins with classes: contains <class>" and is called "the same match as grep -rl 'classes:.*<class>'"; grep matches the pattern anywhere in the line (M-20261012-19 line 7 carries "classes:" mid-line in prose), so the gate's recomputed set and the orchestrator's pasted search (INV-6's clause) can differ and a correct paste would be refused with the S6 text. Pick one definition in both places: "a line containing classes: followed by <class>" (grep's), or the pasted command becomes grep -rl '^classes:.*<class>'.

Neither finding contradicts the design or the amended contract's checks; both are one-sentence corrections the orchestrator may fold into the dispatch note or the next amendment.

Amendment verdict: dotfiles-T128-gate-evidence-a03: confirm
