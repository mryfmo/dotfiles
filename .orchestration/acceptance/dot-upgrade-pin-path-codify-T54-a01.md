# Acceptance: dot-upgrade-pin-path-codify-T54-a01

Drafted 2026-10-02 after the operator's correction (orchestrator direct push
`4a75924`; text rules skipped while hook-injected directives were followed;
`make upgrade` clause permitted a direct chore commit; no mechanical guard).
Dispatched 2026-10-02T03:28:34Z (msg 679) to `claude-standard-dot-a005`
(worker-c) after T53 merged (00ce4f6). RESULT msg 680 (04:27:14Z), head
2360aea, PR #225.

## Round 1 (2360aea) → revise

- Scope delivered: rule + SKILL + README pin-flow rewrite and the
  no-implicit-opt-out activation case; `print_regime_directive` /
  `claim_seat_and_print_directive` emitting the `agmsg-orchestration:`
  SessionStart line (managed pane, unmanaged attach, pane-less summary);
  `install_main_push_guard` pre-push hook from `bootstrap_agmsg`
  (`ORCH_PUSH_MAIN=acceptance|boundary`, fast-forward only, delete refused,
  logged); mise pin tests converted to a v2026.9.12 floor (#160) with the
  exact-pin property kept by the generator `--check`; 711 unit tests OK,
  render-check OK, CI green on all matrices.
- Orchestrator review of the diff (8 files, +306/−18): rule/SKILL/README
  text accurate; floor conversion justified (exactness enforced by
  `generate-agent-configs.py --check`); guard tests run real pushes against
  a scratch bare remote. Findings: (a) the `boundary` path check uses
  `git log --name-only`, which lists nothing for merge commits, so a
  merge-only change escapes; (b) the pane-less summary now prints two lines
  while SKILL/rule/usage text still promise one.
- Codex GitHub review (3 comments on 2360aea): P1 `--no-verify` bypass →
  not-applicable (a client hook cannot be non-bypassable; task forbade
  branch-protection changes; operator-side recommendation recorded below);
  P2 marker-only replacement → revise item 2; P2 undocumented second
  SessionStart line → revise item 3.
- Codex audit (`herdr-agents --audit 2360aea`, transcript at
  `.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit.md`):
  `Verdict: incorrect`. [P1] merge diffs omitted by `git log --name-only`
  → revise item 1 (orchestrator finding a, independently reached);
  [P2] marker presence alone permits replacement → revise item 2;
  [P2] enumeration failure yields empty `outside` and logs `allowed` →
  revise item 1 (fail closed). All three accepted as correct.
- Decision: `AGMSG-ACCEPTANCE v1 task_id=T54 status=revise`; revise round 1
  appended to the task file (new task_rev in the message). PR feedback
  evidence for 2360aea
  (`.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-pr-feedback.json`)
  is superseded by the next head's sweep.

## Round 2 (c636452) → revise

- RESULT msg 682 (04:59:11Z), head c636452 on the same branch/PR. Round-1
  items verified fixed: boundary check is now `git diff --name-only
--no-renames <remote> <local>` with a pure-bash path loop and an explicit
  fail-closed refusal when the diff cannot be listed (demo and tests:
  evil-merge `src.sh` refused, deleted tree object refused); the hook is a
  constant stub exec'ing `herdr-agents --main-push-guard`, bootstrap never
  rewrites a differing hook (edited or foreign) and warns; the "one line"
  SessionStart contract updated in SKILL, README, usage text and shdoc with
  a grep proving no stale carrier; report restated the guard's scope. 715
  unit tests OK, CI green on all matrices, `mergeStateStatus: CLEAN`.
- New Codex GitHub review on c636452: P1 (`:1644`) launcher version skew
  → revise; P2 (`:1653`) lost execute bit → revise. Orchestrator confirmed
  P1 against the installed launcher (no `--main-push-guard`; its default
  branch takes the flag as DIR, runs `remove_shadowing_node_global` with
  `npm uninstall -g`, fails at `cd`) and against the Makefile (`make
upgrade` runs `agmsg-bootstrap` from source before any launcher apply;
  `make update` applies first).
- Codex audit (`herdr-agents --audit c636452`, transcript at
  `.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-audit-c636452.md`):
  `Verdict: incorrect`; [P1] stub invokes a mode the previous launcher
  lacks, blocking every push (reproduced for feature and main refs) →
  revise item 1; [P2] identical stub returns before the execute-bit check →
  revise item 2. Both accepted; the audit also noted the report's "worker
  pushes unaffected" claim omitted the version-skew case.
- Decision: `AGMSG-ACCEPTANCE v1 task_id=T54 status=revise` (round 2),
  task file section "Revise round 2" with the new task_rev.

## Round 3 (1128abb) → accepted

- RESULT msg 684 (05:45:09Z), head 1128abb, one new commit. Round-2 items
  verified fixed in the diff: bootstrap probes the launcher the stub will
  exec (`--help` contains `--main-push-guard`) and otherwise prints the
  `make update` notice and installs nothing; the stub probes the same way
  and, lacking the mode, refuses only `refs/heads/main` updates and never
  execs another mode; an identical non-executable stub gets `chmod 755`
  with a notice. Tests with an old-launcher fake and the execute-bit case;
  718 unit tests OK; render-check, validate-agent-assets exit 0; CI green
  on all 16 checks (macOS 14 and both Ubuntu matrices incl. bats);
  `mergeStateStatus: CLEAN`. No new Codex GitHub review comments on
  1128abb.
- PR feedback sweep (head 1128abb, 24 items): `fixed:c636452` for the
  marker-replacement and one-line-doc comments, `fixed:1128abb` for the
  launcher-skew and execute-bit comments, `not-applicable` for the
  `--no-verify` P1 (client hook cannot be non-bypassable; operator-side
  branch protection recommended), the two Codex review containers, the
  CodeRabbit comment/status, 14 runner notices and the Homebrew tap
  warning. Evidence:
  `.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-pr-feedback.json`.
- Codex audit (`herdr-agents --audit 1128abb`, transcript
  `…-audit-1128abb.md`): `Verdict: incorrect` with one [P2]: a stub
  installed by the c636452 body would be classified as edited and left
  unchanged. Disposition: not-applicable with evidence — c636452 is an
  intermediate commit of this unmerged PR (squash-merged), the installed
  launcher has no guard mode, and neither the main checkout nor the
  canonical clone has a `pre-push` hook or `orch-push-main.log`, so no
  predecessor stub exists anywhere. The general ceiling (a future stub text
  change needs the operator to remove the hook and rerun bootstrap) is
  documented in the report and in the warning text; accepted as a known
  limit, not a defect of this change.
- Agent review evidence:
  `.orchestration/validation/dot-upgrade-pin-path-codify-T54-a01-crit-comments.json`
  (one review-scope record, seven line records, all resolved) and receipt
  `…-review-receipt.md` (`review_outcome: addressed`).
- Gate: `BASE=origin/main PR_FEEDBACK_EVIDENCE=…-pr-feedback.json make
require-crit-review` in `.claude/worktrees/orchestrator-review` at
  1128abb → exit 2 (review required: agent lifecycle path SKILL.md, broad
  diff 9 files / 848 lines); rerun with `AGENT_REVIEWED=1
REVIEW_EVIDENCE=…-review-receipt.md` → exit 0 ("Review requirement
  satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE").
- Decision: `AGMSG-ACCEPTANCE v1 task_id=T54 status=accepted`; merge PR
  #225 by squash without `--delete-branch`: merged 2026-10-02 as `ae22603`;
  ACCEPTANCE msg 685 read by the worker at 05:53:40Z. Activation on this machine is
  operator-side: `make -C ~/.local/share/chezmoi update` applies the new
  launcher and rule, then its `agmsg-bootstrap` installs the stub in the
  canonical clone; the Workspace checkout gets the stub at the next
  `herdr-agents` pair mode or `make agmsg-bootstrap`; restart Claude Code
  so the SessionStart directive line and the updated rule load.

## Operator-side recommendation (out of task scope)

Enable GitHub branch protection on `main` (require a PR and passing checks,
block force pushes and deletion). The local pre-push guard makes the
orchestrator's default path fail; only server-side protection closes
`--no-verify` and arbitrary clients.

cost: n/a (worker runtime exposes no per-session figures)
