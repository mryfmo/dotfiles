# Acceptance: dot-orchestration-rules-T43-a01

Dispatched 2026-09-29T13:16Z (task_commit 258339f). RESULT r1 13:35Z (head
557502b, PR #214). RESULT r2 21:13Z (head 1843dd1 = fix 99c1174 + merge of
`.orchestration`-only main f45cf73).

## Round 1 review and audit

Orchestrator review of 557502b: `scripts/ua-symbol-coverage.py` (stdlib,
per-file function+class table, exit 1 on unexplained loss) reproduces the
eight T41 regressions; rule bullets in `understand-anything.md`, the Codex
mirror and the SKILL (invariant, Worker Playbook 13, Orchestrator step 3
naming `make render-check`); `make render-check` target; README sentences;
one test. CI all pass. The diff also showed the T39 sandbox becoming active
mid-task in worker-c (uv cache read-only, gh 401, phantom untracked stubs,
herdr rename failure) — recorded under T39 leg 1.

Codex audit of 557502b (`…-audit.md`): `Verdict: incorrect`, two P2s, both
reproduced by the auditor: (1) any failed `git show` counted as a deleted
file, so an invalid `--repo-ref` marked every loss explained and exited 0
(fail-open); (2) `defs < before` excused the whole decrease, including
extraction loss beyond the source deletion. **Decision (round 1): REVISE**
(sent 20:58Z, read).

## Round 2 review

99c1174 (read from origin refs): `verify_ref` rejects empty or `-`-prefixed
refs and unresolvable refs via `rev-parse --verify --quiet --end-of-options
REF^{commit}`, exit 2 before any table; a failed `git show` is "gone" only
when `git ls-tree REF -- path` is empty, otherwise exit 2 (`CoverageError`);
a decrease is explained only when `new >= min(old, defs)`; no-grammar files
never explain a decrease. Tests: unresolvable ref (3 subTests, no `leak`
file), file gone at REF, partial deletion with extra loss → REGRESSION,
partial deletion fully accounted → explained; the worker showed the old
script failing 4 of them. Real data: T41 r1 vs 72b8901 → 8 regressions
exit 1; self-compare → 0, exit 0; bad ref → exit 2. `make unit-test` 614
OK, validate ok, render-check ok (run unsandboxed because of the uv cache).
CI all pass on 1843dd1. CompactionDB 992478eb present.

Codex audit of 99c1174: queued at 21:08Z (operator paused Codex, rate
limit); run 2026-09-30 04:10Z after the operator confirmed the pause lifted.

## Round 2 audits (2026-09-30, `herdr-agents --audit`, gpt-6-astra, read-only, high)

- 99c1174 (`…-audit-99c1174.md`): **Verdict: correct**, no findings; 12
  read-only probes passed; CI not re-verified by the auditor (GitHub
  unreachable from its sandbox) — CI all pass confirmed by the orchestrator
  on 1843dd1 via `gh pr view`.
- 1843dd1 (`…-audit-1843dd1.md`, the `.orchestration`-only merge):
  **Verdict: incorrect**, two P2s:
  1. T44 task file `allowed_files` says "sandbox.network block only" and
     forbids other sandbox keys while addendum 8 requires
     `filesystem.extra_allow_write`. Confirmed; not a T43 defect (the file
     arrived through the merge from main). Disposition: T44 task file
     amended by the orchestrator (see its acceptance record); the worker
     already resolved the conflict in favour of the explicit addendum.
  2. Validation :137 recorded `exit=0` after `| grep`, so the claimed gate
     exit 1 was not evidenced (my round-2 sentence "8 regressions exit 1"
     repeated the worker's claim). Confirmed. Disposition: re-derived by the
     orchestrator from git objects (script at 1843dd1, graphs 72b8901 →
     c3afc7a, `--repo-ref 72b8901`): `gate_exit=1`, `regressions: 8`;
     self-compare exit 0; unresolvable ref exit 2. Evidence gap closed; the
     r3 validation must capture exit codes without a pipe.

## PR #214 feedback sweep (head 1843dd1, `…-pr-feedback.json`, 22 items)

Codex GitHub review on 1843dd1, six inline comments, none resolved:

- P1 fail-closed on unreadable ref (script:66, outdated) → `fixed:99c1174`.
- P1 the global rule mandates `python3 scripts/ua-symbol-coverage.py`, which
  exists only in dotfiles while the rule is installed for every repository.
  Confirmed (rule bullet 6 at 1843dd1; helper lives in `scripts/`). → r3.
- P2 ×2 `--repo-ref <base>` is the wrong revision: `def_lines(REF)` explains a
  decrease only when `new >= min(old, defs)`, so reading the pre-change
  source makes every legitimate deletion a REGRESSION. The ref must be the
  revision the new graph was built from (`.ua/meta.json gitCommitHash`,
  normally HEAD); the T41 incident is still caught because unchanged source
  keeps `defs == old`. Confirmed. → r3.
- P2 `def_pattern` recognises Python only by `.py` or `python` in line 1, so
  `#!/usr/bin/env -S uv run --script` executables (permgate, 16 nodes) always
  report REGRESSION. Confirmed (script:48-51). → r3.
- P2 add the policies to the repo `AGENTS.md` → not-applicable: the policy is
  a global user rule with its Codex mirror in `home/dot_config/codex/AGENTS.md`;
  the repo `AGENTS.md` is dotfiles-scoped.
- 10 runner notices, 1 Homebrew tap-trust warning (macOS runner, no install
  path in this diff), CodeRabbit skip comment/status, 2 Codex container
  comments → not-applicable (reasons in the JSON).

**Decision (round 2): REVISE r3** — queued in worker-c behind T47 (one task
per worktree). Amendment appended to the task file; the ACCEPTANCE message
goes out when the T47 RESULT arrives. The sweep re-runs on the r3 head.

## r3 dispatch note (2026-10-01)

Msg 548 (revise) was sent 6 s after msg 547 (T47 acceptance) whose
`next_action` said "keep worker-c on fix/orchestrator-pane-profile-args until
merged"; the worker correctly PONGed blocked (msg 549) on the contradiction.
PR #217 merged as 262b492 at 07:29 JST; go sent (msg 550) with the merge as the
release condition. Orchestrator error: two instructions with a sequencing
dependency were dispatched together; send the dependent one only after its
condition is observable.

## Round 3 review (2026-10-01, RESULT msg 551, head 681957f = 12d3f80 + merge of c8fc05c)

Orchestrator re-derivation from git objects (helper at 681957f): real data
72b8901 → c3afc7a with `--repo-ref c3afc7a` exit 1, `regressions: 8`;
self-compare `--repo-ref HEAD` exit 0; `no-such-ref` exit 2; permgate row
`| 16 | 16 | 25 | ok |` (uv shebang recognised). No stale
`scripts/ua-symbol-coverage` reference outside `.orchestration`; no `.pyc`
in the tree; `dot_zshenv` puts `~/.local/bin/common` on PATH; the merge
commit adds only main's c8fc05c content. CI all pass on 681957f, CLEAN. r3
decision `c8d78aa6…` present in the main DB (worker wrote it in the main
checkout). Codex audit of 12d3f80 (`…-audit-12d3f80.md`, gpt-6-astra,
read-only): **Verdict: correct**, no findings.

PR #214 sweep on 681957f (25 items): the five r3 targets are fixed:12d3f80 (the
re-anchored uv-script comment included); two new Codex P1s:
- renames fail open (reproduced by the reviewer; confirmed by reading
  `def_lines`/`explained` logic: absent → `gone` → explained, successor
  `old == 0` → ok) → **r4**;
- Codex managed PATH lacks `~/.local/bin/common`: empirically the helper
  resolves under `zsh -lc` (dot_zshenv), not under `sh -c`; the rendered
  PATH is the managed contract, so it must carry the directory → **r4**.
Remaining 18 items not-applicable (runner notices, brew tap warning,
CodeRabbit skip/status, Codex container comments, repo-AGENTS.md scope).

**Decision (round 3): REVISE r4** (task_rev 9ca1adc27c292118…); T44 r2 stays queued
behind it in worker-c.

## Round 4 review (2026-10-01, RESULT msg 553, head 6b53337)

Diff since 681957f: helper (`--old-ref`, `renames()` via `git diff -z
--name-status -M --diff-filter=R`, successor judged under `min(old, defs)`,
absent path without `--old-ref` = REGRESSION), rule/mirror/SKILL/README name
both refs, `agent-config.yaml:122` + rendered `codex-config-managed.toml`
add `~/.local/bin/common` after `~/.local/bin` (collisions=0 on this host),
5 new tests, 622 OK. Orchestrator re-derivation from git objects: real data
`--old-ref 72b8901 --repo-ref c3afc7a` exit 1 / `regressions: 8`;
self-compare exit 0; `--old-ref` without `--repo-ref` exit 2. Logic walk of
the status branch: renamed → successor counts; gone + no `--old-ref` →
REGRESSION; gone + `--old-ref` → explained; unchanged rule for present
paths. Codex audit of 6b53337 (`…-audit-6b53337.md`): **Verdict: correct**.
r4 decision `984c14d8…` present in the main DB. CI all pass, CLEAN.

PR #214 sweep on 6b53337 (28 items): renames and Codex PATH → fixed:6b53337;
two new Codex comments, both confirmed by reading the helper:
- P1 low-similarity move (`-M` default threshold → delete/add pair → old
  path explained, new path `old == 0`) — the ceiling r4 documented is a
  fail-open in a gate;
- P2 Ruby `private def` uncounted → undercounted defs explain a loss.
Common root cause: an undercounted or absent def count can explain a loss.
**Decision (round 4): REVISE r5** — unchanged-blob rule (source unchanged
between OLD and REF ⇒ any decrease is a REGRESSION), Ruby visibility prefixes,
and source-backed new paths with zero symbols fail closed (task_rev
f0445f17e351c8d7…). Orchestrator note: r3/r4 fixed symptoms one review at a time;
the root-cause framing should have been in r3.

## Round 5 review (2026-10-01, RESULT msg 555, head c878b0d)

Diff since 6b53337: helper +50/−12 and tests +42. Logic walk of the status
branch at c878b0d: `blobs()` maps every path to its blob id at OLD and REF
(one `ls-tree -r -z` each); a decrease on a path whose blob is identical at
OLD and REF — or whose rename successor keeps the blob — is REGRESSION
`source unchanged` before any def-count rule; a deleted path (absent at REF,
not renamed) still falls to `explained`; without `--old-ref` the blob maps are
empty and the r4 rules apply unchanged. New-only paths at REF with an integer
def count ≥ 1 and zero symbols are REGRESSION `new file, no symbols` unless a
rename predecessor already judges them. `RUBY_DEF` gains the visibility
prefixes. The table gains a `note` column; CLI and rule wording unchanged.
Orchestrator re-derivation from git objects: real data `--old-ref 72b8901
--repo-ref c3afc7a` exit 1, `regressions: 8`, all eight rows `source
unchanged` (the source is identical between those revisions, so every
decrease is a real T41 under-extraction); self-compare exit 0. The worker's
negative check shows all three new tests failing on the r4 script for the
logic, not the CLI. 625 tests OK, render-check and validate ok, CI all pass,
CLEAN. Codex audit of c878b0d (`…-audit-c878b0d.md`, gpt-6-astra, read-only):
**Verdict: correct**, nine behavioural checks incl. the unchanged-blob guard
across renames. r5 decision `18479d26…` present in the main DB.

Residual ceilings, documented in the docstring: a move plus rewrite below
git's rename threshold that keeps *some* nodes is judged only by the
zero-symbol check; def-line counting remains a heuristic for *changed* files
(unchanged files are now exempt from it).

PR #214 sweep on c878b0d: see the JSON (dispositions below).

PR #214 sweep on c878b0d (31 items): r5 targets fixed:c878b0d (the
re-anchored low-similarity comment included); re-anchored uv-script comment
fixed:12d3f80; two new Codex comments, both confirmed by reading the helper:
- P1 `:184` a source-backed new path with 2 defs and 1 node passes (the r5
  ceiling) — an incomplete graph can be approved;
- P2 `:52` `SHELL_DEF` rejects valid name characters (`foo?`), so a changed
  shell file can have a loss `explained` by an undercount.
Both are the same remaining flaw: a regex def count may still *explain* a loss
on changed files or *pass* a new file. **Decision (round 5): REVISE r6** —
def counts never explain (only git-structural deletion/rename do), def counts
only flag (new path: REGRESSION when new < defs), shell name characters
broadened (task_rev 95d26e4f096aed46…). Queued behind T48 in worker-c. Orchestrator
note: this is the framing r3 should have carried; five review rounds were
spent narrowing a heuristic that should not have been load-bearing.

## Round 6 / 6-b review (2026-10-01, RESULT msg 564, head 56f308c = afb2c9d + merge c8cc4e4 + 56f308c)

Orchestrator re-derivation from git objects at 56f308c: real data exit 1,
`regressions: 8` (all `source unchanged`; both `pr-feedback` files back to
`ok`); self-compare exit 0. Logic walk: a decrease is `explained` only when
`defs is None and --old-ref and not renamed`; renamed → successor count only;
new path REGRESSION only when defs ≥ 1 and new == 0 and not a judged successor.
627 tests OK; CI all pass; CLEAN. The worker caught my r6 item 2 miscalibration
with the 138/185 measurement (decision 4629b961… superseded by 635d9dd5…).
Audits: afb2c9d **incorrect** (P2: `SHELL_DEF` now counts commented-out
definitions such as `#disabled() { :; }` → r7); 56f308c **correct** (the
138/185 measurement and the eight regressions independently re-verified).
Orchestrator error: the audit loop enumerated `c878b0d..branch` and so also
audited main's merged commits 0a34a68 (T48; recorded in its acceptance) and
85919df (`.orchestration`; P3 on the learning note's
`PYTHONDONTWRITEBYTECODE=1` advice — confirmed wrong, note corrected by the
orchestrator in this round).

PR #214 sweep on 56f308c (37 items): r6 targets fixed:afb2c9d; Codex `:184`
(partially covered new file) **not-applicable** on the 138/185 measurement
(def-line counts overcount UA nodes; documented ceiling); `:52` shell names
fixed:afb2c9d; two new live comments, both confirmed by reading the helper:
P1 `:159` a new grammar file absent from both graphs is invisible to the
gate; P2 `:55` a `def` inside a Python string literal counts as a definition
and trips the zero-symbol check. **Decision (round 6): REVISE r7** — skip
comment lines, Python defs via `ast`, missing-from-graph check scoped to
covered directories (task_rev fe4ce5714923a8ea…).

Delivery note: until this round the orchestrator's Stop-hook delivery was
silently skipping (actas lock held under the bare session id from sandboxed
Bash while the hook computes the composite id) — RESULTs 546–564 were found by
direct DB reads; fixed by re-claiming with the composite id (codified as T49).

## Round 7 review (2026-10-01, RESULT msg 567 — delivered by the repaired Stop hook — head 72746d4)

Branch-only diff since 56f308c: helper +72/−10, tests +27. Read in full:
`count_defs` skips `#` lines and uses `ast.walk` for Python (regex only on
`SyntaxError`/`ValueError`); `blobs()` keeps `(mode, blob)`;
`missing_from_graph` enumerates grammar files at REF (suffix or 100755 +
grammar shebang) absent from both graphs in directories the new graph covers,
appended as `missing from graph` rows counted in `files:`/`regressions:`.
Measurement first: no candidates at the graph's own revision 72b8901; at HEAD
exactly the two files this PR added (genuine omissions). Orchestrator
re-derivation from git objects: real data exit 1 / 8; self-compare exit 0;
0 `missing from graph` rows on real data. 630 tests OK; CI all pass; CLEAN.
Codex audit of 72746d4: **incorrect** — P2 the shebang probe ignores a
`git show` failure (fail-open on an unreadable candidate), P3 the blob
equality now compares `(mode, blob)` so a chmod-only change hides the
informational `source unchanged` note. Both confirmed by reading the diff.
PR #214 sweep on 72746d4 (37 items): `:159` and `:55` → fixed:72746d4; the
rest unchanged; no new comments. **Decision (round 7): REVISE r8** (two
small fixes, task_rev c5991cd247aa4d7e…).

## Round 8 review and acceptance (2026-10-01, RESULT msg 569, head 1b6741b)

Diff since 72746d4: `missing_from_graph` raises `CoverageError` on a failed
`git show` for a 100755 candidate (exit 2, no table); the `source unchanged`
check compares blob ids only; two tests with negative checks against 72746d4
(r7 exits 0 / prints no note). Orchestrator re-derivation: real data exit 1 /
8 (`source unchanged`), self-compare with both refs at the graph's
`gitCommitHash` exit 0. 632 tests OK; CI all pass; CLEAN. Codex audit of
1b6741b: **Verdict: correct** (six behavioural checks). PR #214 sweep on
1b6741b: no new comments; 37 items = 13 fixed + 24 not-applicable (reasons in
the JSON; the two not-fixed Codex P1s rest on the measured 138/185 ceiling).

Final shape of the gate (`ua-symbol-coverage <old> <new> --old-ref <old graph
rev> --repo-ref <new graph rev>`): only git-structural facts explain a
decrease (deletion, or a rename whose successor keeps the count); every other
decrease is REGRESSION to be cited; def-line counts (comment-free, Python via
`ast`) only flag zero-symbol new files and grammar files missing from the
graph in covered directories; unresolvable refs and unreadable candidates exit
2. Residual, documented: partial under-extraction of a brand-new or
heavily rewritten moved file is not detectable from the count.

Audits across the PR (gpt-6-astra, read-only): 557502b incorrect→fixed r2;
99c1174 correct; 1843dd1 incorrect→dispositioned (T44 task scope; exit
evidence re-derived); 12d3f80 correct; 6b53337 correct; c878b0d correct;
afb2c9d incorrect→fixed r7; 56f308c correct; 72746d4 incorrect→fixed r8;
1b6741b correct. CompactionDB: r1 decision 992478eb… (names the removed
`scripts/` path) and the pending-threshold clause 4629b961… are retracted at
acceptance; c8d78aa6 (r3), 984c14d8 (r4), 18479d26 (r5), 635d9dd5 (r6-b),
67792095 (r7), 4bac6923 (r8) stand.

Orchestrator lessons (codified via T46/T49, recorded here): the heuristic
should never have been load-bearing (r3 framing); audit loops must enumerate
`origin/main..branch`, not `<prev>..branch`; order-dependent dispatches go one
at a time; the seat lock must be composite for turn delivery to work.

cost: worker ~136k+30k+32k+20k+45k+25k+15k context tokens across rounds (session counters; no per-task figure)

**Decision: ACCEPTED.** Merge PR #214 (squash, no `--delete-branch`; worker-c
holds the branch) after the integration gate; T44 r2 is dispatched next.
