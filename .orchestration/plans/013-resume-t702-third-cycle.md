# Plan 013: T702 (PR #329) a03 head: the Bot's first round names a third binding row; the decision for the operator

> **Executor instructions**: plan 007 S7 report form. Nothing below is executed until the operator chooses. Every figure is pasted command output of 2026-10-12/13 (UTC).
>
> **Drift check (at planning time, 2026-10-13 01:20Z)**: `origin/main` `3709a6d8`; PR #329 `OPEN`, head `c36fcd35` (`mergeStateStatus=BEHIND`), CI `SUCCESS:12`; Bot review `5493539294` on `c36fcd35` with three P1 threads (4250238714, 4250238721, 4250238729). Worker `claude-standard-dot-a002`: bus 781 (16:22:10Z, head pushed) and 782 (01:05:56Z, `status=question`): the two code fixes are local and unpushed; its default is to push them at 01:45Z unless told to hold. Plan 012 B (operator, 01:05Z) puts T718's first slice before T703's merge, and T702 integrates after T703 (thread 4248232955, step 10.4).

## Status

- **Execution**: DECIDED 2026-10-13 01:2xZ: option A′ (operator, AskUserQuestion); hold PING 783 to a002 at 01:12:46Z. R1 amendment 1 written 01:3xZ (sha 6d6bfc03…, C1 to C10 OK; review task dotfiles-T128-gate-evidence-a03-amend-review-a01); review pair: five rounds (Codex found a missing parse_constant test, two leftover count sentences, the stale introduction; the seat an addendum on the fixture row), agreement on `1b8ba5b4…` at 01:41Z (seat bus 802, Codex r5). R2 done: boundary PR #335 merged (`720517b1`), amendment line sent 01:46:09Z (bus 805). R3 next: the worker's push, CI, Bot; R4 held until T703 merges (update-branch, audit, acceptance record with the JSON block, gate, merge).
- **Priority**: P1 (T702 is the gate; its a03 counters stand at `questions=1 amendments=0 revises=0`: one more of either is INV-6's reset)
- **Planned at**: main `3709a6d8`, 2026-10-13 01:20Z

## Situation

- The three threads on `c36fcd35` (Bot, 16:28Z):
  - 4250238714 (`scripts/require-crit-review.py:804`): "A positive `pr` is accepted without comparing it to the `pr` in `PR_FEEDBACK_EVIDENCE` … Pass the swept PR number into this validation and require equality". Class `acceptance-record-binding`. The ledger's earlier binding rows: 4248232964 (a01, `acceptance-record-binding`: the record found by task name only) and 4249544762 (a02, slugged `record-head-binding`: "require a machine-readable head binding and compare it with the current HEAD"). Two slugs for one class, assigned by the orchestrator; counted as one class, this is its third row: the third S1 cycle on T702 (after `search-command-scan` 14:20Z and `acceptance-dispositions` 15:23Z) and S7 again.
  - 4250238721 (`task.md:42`): "This row claims there are no interpreter or environment inputs, but the change makes every PR-mode gate invoke external `uv`, resolve `pyyaml` (retrying online if it is not cached), and invoke `grep`. On an offline integration host without the package cached, the mandatory gate cannot validate any acceptance record; an online run also resolves an unpinned package at this host-side trust boundary." The worker's live evidence: the uv cache was pruned during the night and the gate could not load any record offline until PyYAML was fetched again. A task-text change (the threat row), so an amendment of a03. Class `threat-row-missing` (second on the lineage after 4248232976).
  - 4250238729 (`require-crit-review.py:730`): "`yaml.safe_load` silently keeps the last occurrence of a duplicate mapping key … Use a loader that rejects duplicate mapping keys". New class `yaml-duplicate-keys` (one).
- S6 search, pasted (01:12Z):

```text
$ /usr/bin/grep -rl 'classes:.*\(acceptance-record-binding\|record-head-binding\)' .orchestration/learning/mistakes/
(grep rc=1)
$ uv run --no-project .claude/hooks/contextdb_cli.py memory search record-binding
No matches.
```

  No record for the class: this plan's mistake record (M-20261012-24, below) is the first.
- The a03 contract (task file `686806a1`) lists the record's identity fields as `format`, `task`, `head` (= `HEAD`), `pr`. The gate checked `task` after a01 and `head` after a02; `pr` was never compared with the swept PR. With the `pr` check the triple is complete: the record has no further identity field, so the class ends with this row rather than with a later one.
- How the gate head resolves its parser (`git show refs/remotes/pr/329:scripts/require-crit-review.py`): lines 723 to 748 run PyYAML "in a uv-provided interpreter: the gate's own python3 has no third-party packages", with an online retry when the cache is empty; line 914 runs `grep -rl`. Host check (01:12Z): `/usr/bin/python3 -c 'import yaml'` → `ModuleNotFoundError: No module named 'yaml'`; `uv run --no-project --offline --with pyyaml` → `uv offline ok 6.0.3` (cached again now).
- uv's documentation on hashes (`docs.astral.sh/uv/pip/compile/`, fetched 01:15Z): "To check runtime dependencies with `uv pip install` or `uv pip sync`, use `--require-hashes`." Nothing on the page covers `uv run --with` or `--with-requirements`, so hash-pinning the gate's PyYAML through `uv run` is undocumented.

## Root cause

The record's identity was bound one field per round (task → head → pr) instead of as the triple the contract lists; the orchestrator also gave the second row a different slug, so the ledger did not show the class at two. The parser dependency row was copied from a02 ("none") after the a03 contract had introduced a third-party parser at the gate: the row was not re-derived from the new diff.

## Options (today's medians: amendment text 10 to 15 min, worker fix round 20 to 30 min, CI 8.5, Bot 5 to 14, integration 25; T702 integrates after T703, which under plan 012 B is about 2 h 15 to 2 h 45 away)

| | Option | Rounds | Wall to a Bot-reviewed head | Risk |
|---|---|---|---|---|
| **A′** | **Amendment 1 of a03: the record's machine part stays between the `---` lines but is a JSON object (valid YAML, so T718's writers and any YAML reader still read it); the gate parses it with the standard library (`json.loads` with `object_pairs_hook` refusing duplicate keys, `parse_constant` refusing NaN and Infinity) and compares `pr` with the swept PR; the uv/PyYAML/online-retry code is deleted; the environment-inputs row becomes "none" truthfully, with `grep` replaced by `pathlib` globbing or named as the one host binary. The worker's two local fixes are folded in.** | 1 amendment, 1 fix round | about 55 to 65 min | one Bot round on the smaller loader; a further question or amendment resets a03 (INV-6); deviates from plan 011 F's word "PyYAML" (the field checks are unchanged) |
| A | Amendment 1 of a03: keep PyYAML; the threat row names uv, PyYAML and grep as inputs, pins `pyyaml==6.0.3` and requires the cache (`--offline` first, online retry only with the operator's consent); duplicate keys refused by a SafeLoader subclass; `pr` compared | 1 amendment, 1 fix round | about 50 to 60 min | the gate keeps a network-resolved package it cannot hash-verify through `uv run` (undocumented), so the provenance half of 4250238721 stays residual; the Bot may return to it |
| C | Hold a03 unpushed until T703 merges (plan 012 B), then push the fixes and the amendment once, so one Bot round sees the final base | same as A′ or A, later | the same work after about 2 h 30 | the worker's seat is idle meanwhile (T715 cannot start on it while a03 is open), and nothing is learned earlier |
| D | Reset to a04 | 1 reset, 1 worker round | about 60 min plus | nothing structural changes: the three findings are three small checks, and a reset spends the INV-6 cycle on the same code |

**Recommendation: A′.** It removes the dependency class instead of documenting it, closes the binding triple, and is the smaller gate. **Without A′: A.**

## Records

- M-20261012-24 (classes `acceptance-record-binding`, `threat-row-missing`) and C-26 (binding as the whole identity triple at once; the environment row re-derived from the diff by the checker: a task whose diff adds a subprocess call or an import outside the standard library fails C11 unless the row names it) are written with this plan.

## Steps after the decision (filled when it arrives)

- A′ or A: R1 amendment text (hashed, review-seat confirmation); R2 `AGMSG-TASK … amendment=1` to a002, which pushes fixes and amendment evidence; R3 CI, Bot, sweep; R4 held until T703 merges, then update-branch, audit, acceptance record (its front matter now in the amended form), gate, merge.
- C: R1 `hold` to a002 now; R2 as above after T703.
