# T79b validation

## Baseline and method

- Pre-slim source baseline: commit `e1155c2`.
- T79 audit population: every row marked `kept core` or `kept core in
  tightened form` in `.orchestration/validation/T79-validation.md` (22 rows).
- T80 audit population: every kept row whose source wording was shortened
  rather than retained byte-for-byte (C009, C010, C038; 3 rows).
- Qualifier dimensions: scope, ordering, exclusivity, and condition.

## Kept-clause qualifier audit

| Source row | Pre-edit qualifier obligation | Post-T79b status |
|---|---|---|
| T79 1a | Operator request independently activates the regime. | preserved — first activation alternative |
| T79 1b | Automatic activation requires both bus availability and a resident worker **for this repository**. | repaired — repository scope restored before skill loading |
| T79 1c | agmsg becomes the always-on path during the active regime. | preserved/strengthened — `agmsg is required` until current-task opt-out |
| T79 1d | Claude is limited to lightweight read/judgment/task/acceptance work outside exemptions. | preserved — second bullet retains the exclusive allowed set |
| T79 1e | Only a current-task operator opt-out permits direct repository mutation. | preserved — current-task condition and only-after ordering both explicit |
| T79 3a | Delegate all repository-mutating work, including the class containing builds/tests/git work. | repaired — `all repository-mutating work` restored instead of narrower `repository mutations` |
| T79 3e | Only agmsg/herdr control-plane work is the control exemption. | preserved — category stays core; exact command enumeration remains moved detail |
| T79 6a | Review four dimensions including **reporting** omissions. | repaired — `reporting` scope restored |
| T79 6b | Try to refute and independently re-derive. | preserved — both ordered adversarial duties explicit |
| T79 6c | Never treat **sampled** spot checks as **full verification**. | repaired — sample and full-verification qualifiers restored verbatim |
| T79 10a | Acceptance/adversarial/review-profile work remains Claude-side. | preserved — role exclusivity explicit |
| T79 10b | Never delegate those reviews, acceptance, **or the Crit gate**. | repaired — `make require-crit-review` made an explicit non-delegable object |
| T79 10c | Crit gate is the final integration step. | preserved — final-step ordering explicit |
| T79 10d | Revisit only after worker capability surpasses the orchestrator tier. | preserved — threshold condition unchanged |
| T79 21 | Load the skill for contracts/playbooks. | preserved/strengthened — immediate full-protocol invocation subsumes both |
| T79 22a | Sync at regime or session boundaries. | preserved — both boundary alternatives explicit |
| T79 22b | Evidence-sync bookkeeping is exempt from worker delegation. | preserved — exemption remains in delegation bullet |
| T79 22e | Write pending acceptances before the mechanical commit. | preserved — write → verify → commit ordering explicit |
| T79 22f | Commit **every `.orchestration` file** and leave zero untracked tail. | repaired — canonical object restored from generalized `all evidence` wording |
| T79 22g | Mise config/lock changes get their **own chore commit** in the **upgrade session**. | repaired — commit exclusivity and session relation restored |
| T79 22h | Never leave the mise pair dirty across sessions. | preserved — prohibition unchanged |
| T79 23 | Decision completeness applies to **CompactionDB-opted-in projects**. | repaired — opt-in condition restored |
| T80 C009 | Keep plan and todo current throughout repository work. | preserved — always-update duty retained with worklog skill trigger |
| T80 C010 | Never commit plan/todo/learn worklogs. | preserved — prohibition unchanged |
| T80 C038 | Active todo limit is per owner, not repository-wide. | preserved — `owner`-scoped maximum one permits parallel owners |

Audit result: **25/25 rows inspected; 8 repaired; 17 already preserved; 0
unaudited; 0 remaining qualifier loss.** T80 required no source edit.

## Core measurement and scope

T77 estimator: English characters / 4, approximate ±20%.

| State | Characters | Estimated tokens |
|---|---:|---:|
| accepted T79 core | 1,358 | 339.50 |
| post-T79b core | 1,411 | 352.75 |

- Ceiling: ≤360 tokens — PASS with 7.25-token headroom.
- Added text is limited to kept-core qualifiers; no moved procedure regrew.
- `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: no diff.
- `home/dot_config/codex/AGENTS.md`: no diff.

## Static qualifier assertions

- PASS: all 8 repaired phrases are present.
- PASS: all three shortened T80 invariants are present.
- PASS: 25 unique audit rows, exactly 8 marked repaired.
- PASS: only `home/dot_config/claude/rules/agmsg-orchestration.md` has a
  tracked source diff; both forbidden skill/Codex-policy paths are clean.
- PASS: core is 1,411 characters / 352.75 estimated tokens.

## Command validation

| Command | Result |
|---|---|
| `make format` | PASS — shfmt diff empty |
| `env UV_CACHE_DIR=/private/tmp/t79b-uv-cache uv run python -m unittest discover -s tests/unit -p 'test_*.py' -q` | PASS — final run: 336 tests in 28.575s |
| `env UV_CACHE_DIR=/private/tmp/t79b-uv-cache uv run --with pyyaml scripts/validate-agent-assets.py` | PASS — `agent asset validation ok` after approved network retry; initial sandbox attempt could not resolve PyPI |
| `git diff --check` | PASS |
| qualifier/count/budget/scope assertions | PASS |

The unit output's four `ERROR:` lines are expected negative-fixture messages;
the unittest runner ended `OK` with exit 0.

## Plan-quality gate

- Manual checklist: passed.
- Validator / Make target: unavailable.
- Hook: unavailable.
- Subagent definition: unavailable.
- Template and CI entrypoint: unavailable.
- Unavailable exact command:
  `uv run python scripts/validate_plan_quality.py .agents/worklog/codex/plan/20260817_172519_plan.md`.

## Crit gate

- Initial `make require-crit-review`: expected evidence requirement.
- Review: finding-free resolved record `r_9969c0`.
- Evidence: `.agents/worklog/codex/review/T79b-crit-comments.json`.
- Receipt: `.agents/worklog/codex/review/T79b-receipt.md`.
- Final command:
  `env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/T79b-receipt.md make require-crit-review`.
- Result: PASS — `Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.`
