---
format: 2
task_id: dotfiles-T124-wave1-task-validator-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-canonical.md
  design: .orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md
allowed_files:
  - scripts/validate-task.py
  - scripts/lib/high_risk_paths.py
  - scripts/check-regime-boundary.sh
  - Makefile
  - tests/unit/test_validate_task.py
  - tests/unit/test_require_crit_review.py
  - tests/unit/test_herdr_agents.py
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
  - home/dot_config/claude/rules/agmsg-orchestration.md
  - home/dot_config/claude/rules/pr-integration.md
  - home/dot_config/claude/rules/crit-review.md
  - AGENTS.md
  - README.md
invariants:
  INV-1: a PR cannot pass make require-crit-review unless the task file derived from the PR-feedback JSON name passes scripts/validate-task.py (format 2 front matter); the worker runs the validator at task start and blocks on failure; there is no dispatch-side check
  INV-2: security is derived from the design tier of the shared high-risk path module imported by the validator and the gate; declared true is allowed (ratchet up), declared false on a matching task fails; prose paths are not in the tier
  INV-8: every rule has a unit test that fails when the rule is removed, including one per gaming path; format 2 grandfathers older task files
---

# AGMSG-TASK dotfiles-T124-wave1-task-validator-a01 — T124 wave 1: the task validator and the shared high-risk tiers

Drafted 2026-10-10 by the orchestrator seat (`claude-deep-dot`, w4:p1). Wave 1 of the accepted T124 design (`.orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md`, design review rounds 1–3 by `claude-review-dot-a002`, round 3 `accept`). Read the design file first, in full, including its review receipts; this task implements INV-1, INV-2 and the INV-8 grandfather, nothing else. Kind: code; Claude seat. This task file is the first `format: 2` task file and is itself the validator's first input.

## What to build

1. `scripts/lib/high_risk_paths.py` (new): the two tiers as module constants. **Review tier** = the lists now in `scripts/require-crit-review.py` (`HIGH_RISK_PREFIXES`, `HIGH_RISK_FILES`, `HIGH_RISK_TOKENS`), moved here unchanged and imported back by the gate (behaviour of the gate unchanged; its tests prove it). **Design tier** = explicit path patterns (per the round-3 note, patterns, not prose): `install/**`, `setup.sh`, `scripts/lib/github-release.sh`, `scripts/update-agent-assets.sh`, `scripts/upgrade-tools.sh`, `home/dot_agents/agent-config.yaml` (whole), `scripts/validate-task.py`, `scripts/require-crit-review.py`, `scripts/agent-stop-gate.sh`, `scripts/check-regime-boundary.sh`, `home/dot_local/bin/common/executable_herdr-agents`, `home/dot_local/bin/common/executable_permgate`, `home/dot_codex/**`, `.claude/hooks/**`, `home/dot_claude/hooks/**`, `home/.chezmoitemplates/claude-settings-managed.json`, `home/.chezmoitemplates/codex-config-managed.toml`, `home/dot_claude/modify_private_settings.json`, `home/dot_agents/permgate-policy.yaml`, and the auth-helper files by path (find them: `git grep -ln 'gh auth\|credential' -- home install scripts` and list the ones that handle credentials; name each in the report). `scripts/lib/` holds only shell today: import the module from the script's own directory (`sys.path[0]`) and give the unit tests that load the gate by path the same path.
2. `scripts/validate-task.py` (new): `validate-task.py <task file> [--json]`; exit 0 when valid, 1 with one line per failure. Rules: YAML front matter delimited by `---`; required keys `format: 2`, `task_id` (equal to the file stem), `kind` (`code|review|docs|design`), `allowed_files` (list; `kind: review|docs|design` may omit it), `invariants` (map `INV-n: sentence`; at least one when `security` is true), `threat_model` and `trust_anchors` (required when `security` is true; `kind: code` tasks may instead point at a design task through `design_review.design`, whose keys then count), `design_review: {receipt, design}` (required when `security` is true; both paths must exist in the main checkout), `waves` (required when `allowed_files` expands to more than 15 existing files: a map of wave name → file list whose union covers `allowed_files`; otherwise the count only warns), `superseded_by` (optional task id; when present the task is `superseded`). `security` is derived: true when any `allowed_files` entry matches the design tier (glob semantics as the gate uses); a declared `security: true` is kept when no path matches; a declared `security: false` on a matching task fails. The canonical design hash: `sha256` of `json.dumps({k: design[k] for k in ("invariants","threat_model","trust_anchors")}, sort_keys=True, separators=(",",":"), ensure_ascii=False)` over the design task named in `design_review.design`; print it with `--print-design-hash` (the gate and the review receipt use the same function; export it from the module so `require-crit-review.py` can import it in wave 2a). A `format: 2` task whose `design_review.design` names another task must have `invariants` ids that are a subset of that design's ids. Files without `format: 2` are reported `legacy` and exit 0 (the grandfather).
3. `scripts/require-crit-review.py`: only the import of the moved constants (no rule change; wave 2a adds the rules). `scripts/check-regime-boundary.sh`: run the validator on every `.orchestration/tasks/*.md` with `format: 2` and report each failure as a violation; legacy files are skipped. `Makefile`: a `validate-task` convenience target is not needed; `check-regime-boundary` already exists.
4. Prose: SKILL Orchestrator Playbook (task authoring: the front matter, the two tiers, the design review before dispatch for `security: true`, the "gate from `main`" acceptance rule of the design's trust anchors stated as the procedure for step 10 from now on: `<main>/scripts/require-crit-review.py --base origin/main` with the review worktree as cwd, refused when `main` is at the audited head, which is wave 2a's rule but the procedure text lands now), Worker Playbook step 1 (run `scripts/validate-task.py <task file>` first; `status=blocked` with its output on failure), `home/dot_config/claude/rules/agmsg-orchestration.md` (one invariant line: every task is a `format: 2` file that passes the validator; security tasks carry a reviewed design), README (one paragraph under the regime section).
5. Tests (`tests/unit/test_validate_task.py`, new; `test_require_crit_review.py` for the import; `test_herdr_agents.py` for the boundary check): valid file; each missing key; `task_id` mismatch; `security` derivation for a design-tier path, a review-tier-only path (not security) and a prose path; declared false on a matching path fails; declared true on a non-matching path kept; `waves` required above 15 files and the union rule; a single all-encompassing wave is accepted by the validator (the gate's one-wave rule is wave 2a's) but flagged as a warning; the subset rule; the canonical hash is stable under key order and whitespace and changes when an invariant sentence changes; legacy files exit 0; the boundary check lists a failing `format: 2` file and skips legacy. Each test fails when its rule is removed (show one removal per rule family in the validation, as T118/T119 did).

Forbidden: anything else; any gate rule beyond the import; `agmsg-dispatch` changes; `make update`; thread resolution.

## Standing instruction on Bot and CI findings (operator, 2026-10-09)

Every Codex Bot finding and every CI failure on the PR is fixed at its root cause in the PR itself, not dispositioned. A `not-applicable` is reserved for a finding that is factually wrong, with the refuting command and output pasted in the reply. A finding on the task's own wording is still fixed in the PR. "Out of scope" is not a disposition for a finding on files the PR touches: report the scope gap and the orchestrator amends the allowed files. Recheck the reviews once more right before sending the RESULT. Under the accepted T124 design, this task is also subject to the reset rule by hand until wave 2b lands: two revise rounds with implementation findings, and the orchestrator writes a design reset instead of a third.

## Sandbox conduct (T119 lesson, binding)

Every command runs inside the sandbox except Worker Playbook step 4's cases (`gh`, `git push`, authenticated `git fetch`, the main-checkout CompactionDB `memory add`, the masked artifact copy, `agmsg-dispatch`). No unit test, replay, download or edit runs outside it; a capability the sandbox lacks is proven in CI or with an in-sandbox shim stated as such; a gate refusal is reported verbatim in the PONG or RESULT, never reworked. The sandbox record lists every out-of-sandbox command and carries `permission_gated_commands: <n>` in its front matter (the line INV-9 will read).

[memory:decision] dotfiles-T124 wave 1 (orchestrator 2026-10-10): every task is a `format: 2` file validated by `scripts/validate-task.py`; `security` derives from the design tier of `scripts/lib/high_risk_paths.py` (the review tier is the gate's existing lists); a security task names a reviewed design whose canonical key hash the receipt carries; legacy task files are grandfathered.

## Repo / branch

`.claude/worktrees/worker-c`: `git fetch origin`; `git switch -c feat/task-validator --no-track origin/main`.

## Validation commands (paste verbatim output, whole)

```
uv run --no-project scripts/validate-task.py .orchestration/tasks/dotfiles-T124-wave1-task-validator-a01.md; echo "rc=$?"
uv run --no-project scripts/validate-task.py .orchestration/tasks/dotfiles-T124-design-gate-and-reset-rule-a01.md --print-design-hash; echo "rc=$?"
uv run --no-project scripts/validate-task.py .orchestration/tasks/dotfiles-T118-rolling-tools-single-update-a01.md; echo "rc=$?"   (legacy)
make check-regime-boundary 2>&1 | grep -E 'validate-task|format' ; echo "rc=${PIPESTATUS[0]}"
uv run python -m unittest tests.unit.test_validate_task tests.unit.test_require_crit_review tests.unit.test_herdr_agents 2>&1 | tail -3
make unit-test 2>&1 | tail -3
shellcheck scripts/check-regime-boundary.sh; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md home/dot_config/claude/rules/agmsg-orchestration.md home/dot_agents/skills/agmsg-orchestration/SKILL.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English title `feat(regime): validate task files and derive security from a shared high-risk tier`, English body naming the design and its three review receipts; attribution footer), CI green, Bot wait per the SKILL, artifacts at the standard `dotfiles-T124-wave1-task-validator-a01` paths (masked with the repository masker), the CompactionDB `memory add` of the decision line with the command and output pasted, validation lines `invariant: INV-1 → …`, `invariant: INV-2 → …`, `invariant: INV-8 → …`, then `AGMSG-RESULT v1 task_id=dotfiles-T124-wave1-task-validator-a01` via `agmsg-dispatch dotfiles-conformance <your identity> claude-deep-dot w4:p1 "<single line>"`. max_turns=16.

## Amendment 1 (orchestrator, 2026-10-10, before any work) — two round-3 review notes applied

1. **Do not touch `scripts/require-crit-review.py`.** It is a gate source routed to the operator (waves 2a/2b). Wave 1 creates `scripts/lib/high_risk_paths.py` with the review tier as a copy of the gate's three lists and the explicit design tier; the validator imports the module; the gate keeps its own constants until wave 2a switches it to the import; `tests/unit/test_validate_task.py` asserts that the module's review tier equals the gate's constants (load the gate module by path) so no second list drifts in the interim. `scripts/require-crit-review.py` is removed from `allowed_files`; `tests/unit/test_require_crit_review.py` stays only for that equality test if it is the natural home, otherwise leave it untouched.
2. **"Gate from `main`" needs a Makefile variable.** The recipe runs `./scripts/require-crit-review.py` relative to its own directory, so it cannot run `main`'s script against another tree. Add `REVIEW_TREE` to the `require-crit-review` target: when set, the recipe runs `cd "$(REVIEW_TREE)" && "$(CURDIR)/scripts/require-crit-review.py" …` with the same environment variables, so `make -C <main> require-crit-review REVIEW_TREE=<review worktree> …` judges the review tree with `main`'s script; the refusal when `main` is at the audited head is wave 2a's rule (gate source), not yours. Update the four texts that name the gate command to the new form: `home/dot_config/claude/rules/pr-integration.md`, `home/dot_config/claude/rules/crit-review.md`, `AGENTS.md` "Agent Review Evidence", SKILL step 10.4 (all added to `allowed_files`). Test: `make -n require-crit-review REVIEW_TREE=/tmp/x` shows the `cd` and the `$(CURDIR)` script path; without the variable the recipe is unchanged.

## Amendment 2 (orchestrator, 2026-10-10) — the redesign seat (operator direction via the review seat's addendum)

The operator adopted the redesign-seat approach (addendum `.orchestration/validation/dotfiles-T124-design-gate-and-reset-rule-a01-design-review-addendum-redesign-seat.md`): after an INV-5 reset the superseding design is written by a separate seat on a new `redesign` profile, never by the orchestrator. Wave 1 takes its validator parts only:

1. `kind` gains `design` (no PR; the same front matter minus `waves`; `allowed_files` optional).
2. The validator understands the reset record `.orchestration/acceptance/<task id>-design-reset.md`: front matter `format: 2`, `reset_of: <task id>`, `redesign_task: <new design task id>`, `redesign_seat: <identity containing -redesign->`, `reason`; `validate-task.py <reset record>` checks the shape, that `redesign_task`'s file exists and is `kind: design`, that the new design's `allowed_files` (or the implementing tasks it names) overlap the abandoned task's, and marks the abandoned task `superseded` when `superseded_by` in its front matter equals `redesign_task`. The history check (a `-redesign-` RESULT before the implementing TASK) is wave 2b's gate rule, not yours; say so in the validator's help text.
3. Tests: `kind: design` valid without `allowed_files`; a reset record with a `redesign_seat` lacking `-redesign-` fails; a reset record whose `redesign_task` file is missing or not `kind: design` fails; the overlap rule.

Nothing else from the addendum lands here: the `redesign` profile and the rule text are wave 1b (after this PR, prose and manifest), the stop-gate message is wave 3a, the gate's history check is wave 2b.

## Push form (orchestrator, 2026-10-10)

The host SSH agent holds no identity and the global git config rewrites pushes to SSH, so the authorized push form (used by every task since T118) is: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles <branch>` (gh keyring login; no config file change). Use it for every push; it is not a rework of a refusal, it is the documented form.

## Amendment 3 (orchestrator, 2026-10-10) — q1 and q2 on PR #313

- **q1: bind now (default).** The receipt's `design:` must end in the canonical hash and `reviewer` must not be the orchestrator; T124's security task files fail the validator until a canonical receipt exists. The orchestrator seats a `-review-` identity now to write that receipt from PR #313's validator (`--print-design-hash`) against the accepted design, so the window is short; wave 2a anchors it in history.
- **q2: continue fixing.** INV-5(d) (Bot P1 on two heads) is met on PR #313 by the design's own count, before any RESULT or audit. The decision between a design reset and an operator waiver is the operator's, not the orchestrator's (that is INV-5's point); it is put to the operator now and recorded in the acceptance record either way. Until the operator answers, the six fixes proceed and nothing else changes. The orchestrator also notes for the design: (d) counted pre-RESULT pushes, which the Bot reviews one by one; whether (d) should count heads after the first RESULT only is a calibration question for the operator.

## Concurrency note (orchestrator, 2026-10-10)

Three in-flight tasks touch `tests/unit/test_herdr_agents.py` in disjoint hunks (wave 1 near 2834, T120 at 1823, wave 3b at 4321) and two touch `home/dot_local/bin/common/executable_herdr-agents` in disjoint regions (T120: the claude-code shadow heal near 2048; wave 3b: the audit prompt). This is an orchestrator exception to the pairwise-disjoint code-file rule, taken for throughput and recorded in each acceptance record; merge order is by readiness, and every later PR takes `gh pr update-branch` and re-runs CI, the Bot wait and the gate on the merged head. A real conflict blocks only that PR.

## Amendment 4 (orchestrator, 2026-10-10) — the tier stamp (T126 W1)

The operator asked for the approach to be re-planned (design `.orchestration/tasks/dotfiles-T126-regime-v2-a01.md`); wave 1 stays as it is with one addition: the validator derives `tier` (`docs` when every `allowed_files` path is prose, `review` when any path matches the review tier, `design` when any path matches the design tier; `security: true` is equivalent to `design`) and prints it with `--print-tier`; `home/dot_agents/agent-config.yaml` gains a `process_tiers:` map keyed by tier whose values the validator reads back verbatim (`stages`, `profiles`, `limits` as in the T126 table; the validator only checks that each tier it can derive has an entry, it enforces nothing from it yet, W5/W7 do). `tests/unit/test_validate_task.py`: tier derivation for the three cases and the missing-entry failure; `tests/unit/test_generate_agent_configs.py` only if the renderer needs to know the key (it should ignore it). `home/dot_agents/agent-config.yaml` joins `allowed_files` for that map only. On PR #313's INV-5(d) count: the T126 design redefines (d) as Bot P1 on two heads after the first RESULT, under which it did not fire; the operator's confirmation of that redefinition (or a waiver) is recorded in the acceptance record before the merge, so continue the fixes and the RESULT as planned.

## Amendment 5 (orchestrator, 2026-10-10) — q3: the six Bot findings on 0d6d5aed

Proceed with all six at their root (the standing rule; the "nothing else changes" of Amendment 3 concerned the reset decision only): reset records only under `.orchestration/acceptance/`; `home/.chezmoiscripts/**` joins the design tier; a glob entry must appear verbatim in exactly one wave; the receipt must carry `Design verdict: accept`; a security task must be listed in its design's `implementing_tasks` (the design front matter now lists the three wave tasks; not a hashed key); `trust_anchors` non-blank. The canonical receipt exists now (`…-design-review-canonical.md`, hash `06c3122a…`), and every T124 task file points at it, so the T124 security task files should pass once your validator reads it.

## Amendment 6 (orchestrator, 2026-10-10) — q4: `implementing_tasks` joins the canonical hash

Default accepted: the receipt must bind the scope it authorizes, so `implementing_tasks` is a hashed key (with `invariants`, `threat_model`, `trust_anchors`); adding a task to a design later needs a new review receipt. The orchestrator updates both designs (T124: wave 1 only; T126: wave 3b, W2b, W3 and later waves as they are drafted) and requests fresh canonical receipts from the review seat once your validator with the new key set is pushed. Send a PONG `status=alive note=pushed <sha>` right after that push so the receipts can be computed against it; the T124 task files will fail until the new receipt exists, as before. T125 is demoted to a legacy file (its `format: 2` key removed; it is superseded by T126).

## Amendment 7 (orchestrator, 2026-10-10) — q5: define the `redesign` profile in this PR

Neither default: the root fix is to define what the table names. `model_profiles.redesign` is added in this PR (`claude: { model: claude-fable-5-1, effort: xhigh }`; codex mirroring `deep`'s codex model at `model_reasoning_effort: xhigh`), `home/dot_agents/agent-config.yaml` is allowed for that block as well as the `process_tiers` map, the renderer output (`~/.agents/model-profiles.env`, the Codex profile config) gains the entries, and `tests/unit/test_generate_agent_configs.py` joins `allowed_files` for one assertion on the rendered entries. The Bot thread is answered `fixed:<sha>`. W8 (T126) shrinks to the rule text in `model-selection.md` and the SKILL's reset procedure, which W3 already carries, so W8 may disappear. Thread 4237437333 (symlinked reset record) and 4237437337 (at least one invariant for every task) as you are doing. Send the RESULT after this push and its Bot round, naming any further finding in it.

## Amendment 8 (orchestrator, 2026-10-10) — q6: the profile set is validated

Default accepted: `scripts/validate-agent-assets.py` (the required-profiles set gains `redesign`; the message says seven base profiles) and `tests/unit/test_validate_agent_assets.py` (the three pinned lines) join `allowed_files` for that change only; the rendered pair (`home/dot_codex/modify_private_redesign.config.toml`, `home/dot_agents/model-profiles.env`) joins as renderer output. Push, Bot round, RESULT.

## Revise round 1 (orchestrator, 2026-10-10) — the ten open Bot threads, all fixed at the root

All ten accepted as proposed; none is a disposition. (1) 4237326681: `Makefile` joins the design tier. (2) 4237326686: a reset's `redesign_task` must be a valid `format: 2` `kind: design` task. (3) 4237326688: a security code task that names a design omits `threat_model` and `trust_anchors` or carries values byte-equal to the design's. (4) 4237326692: reset overlap intersects the two globs as automata (the tier NFA), not tracked files. (5) 4237326697: the boundary loop enumerates `.orchestration/tasks/` including dot-prefixed names. (6) 4237326701, the design choice: grandfathering is bound to a checked-in list `scripts/legacy-task-ids.txt` of the task ids that existed before format 2 (generate it once from the current tree, one id per line, sorted); a formatless file whose id is not in the list is a validation failure, so a new task cannot opt out; the list only shrinks. (7) 4237495354: the receipt must be a distinct file under `.orchestration/validation/`, different from the design and the task. (8) 4237495358: an ordinary task validates only when its lexical parent is `.orchestration/tasks/`. (9) 4237495360: the recipe refuses a `REVIEW_TREE` whose top level is the checkout running it; the full "the gate checkout is main and not at the audited head" rule is W5's. (10) 4237495362: each referenced invariant id's sentence must equal the design's. Tests per item as before (each fails when its rule is removed); then push, CI, Bot round, `AGMSG-RESULT … round=2`. Record: this is revise round 1 of W1 under T126 INV-6; the pre-RESULT Bot rounds do not count, and from this RESULT on Bot P1 heads do.

## Revise round 2 (orchestrator, 2026-10-10) — two P2 on e6b30e96; thread 4237594826 answered by the design

4237594829: the resolved parent must equal the file's own checkout's `.orchestration/tasks` and the name must end in `.md`; 4237594831: a design's `invariants` must be a text map before the sentence comparison (a type failure is a validation failure, never a traceback). Tests for both; push, Bot round, `AGMSG-RESULT … round=3`. 4237594826 (SKILL and integration rules in the design tier) is answered on the thread with T124 INV-2 as reviewed (prose is not in the design tier; the review tier covers it) and resolved by the orchestrator. This is revise round 2 of W1: T126 INV-6 (a) reaches its count; the orchestrator puts the waiver to the operator and does not merge before the answer.
