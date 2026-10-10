---
format: 2
task_id: dotfiles-T128-v0-main-tests-a01
kind: code
security: true
design_review:
  receipt: .orchestration/validation/dotfiles-T128-regime-v3-a01-design-review-round13.md
  design: .orchestration/tasks/dotfiles-T128-regime-v3-a01.md
allowed_files:
  - .github/workflows/test.yaml
  - scripts/main-tests.sh
  - scripts/lib/contract_markers.py
  - tests/unit/regime_contract.py
  - tests/unit/test_main_tests.py
  - home/dot_agents/skills/agmsg-orchestration/SKILL.md
invariants:
  INV-12: "every rule above is exercised by a unit test that fails when the rule is removed; the PR's own workflow runs the PR's tests, and a required check main-tests (wave V0, before every other wave) fetches main's tests/unit and runs them in the PR's context in two modes: for a script outside the task.md's allowed_files it runs main's module as it is, so an undeclared change to any script fails; for a script inside allowed_files it runs only main's dormant contract tests for that module (tests marked with the regime's contract decorator, which skip in ordinary CI and run when REGIME_CONTRACT=1), so an intentional change is judged by the contract that was reviewed and merged on main before the implementation; the implementation PR promotes those contracts by removing the decorator in its own tree (main-tests judges it against main's dormant copy, so nothing stays dormant after the wave lands), main-tests fails an implementation PR (any task id not ending in -contract-a01) whose declared test module in the PR tree still carries a contract marker, and main-tests fails a design-tier implementation PR whose declared script has no dormant contract on main (an empty contract is not a pass); a design-tier code wave lands its contract tests first in a <task>-contract-a01 PR (dormant, hence mergeable), a review-tier wave may; the design-tier audit from the trusted root reads the diff; a deleted or weakened fails-when-removed test is a conformance finding; including one test per gaming path (a schema-valid task with a prose cap bypass, a revise without a named check, a revise list appended to the hashed task.md, an AGMSG-TASK without amendment= that still counts, an evidence-only relabel of a code change caught by the tree-equality check, a wave-table rewrite after review, an audit JSON edited after its history record, a receipt whose hash predates a key change, a reset record naming the author's own identity, a Bot-skipped head whose audit never starts, a single PR split only in the task file, a branch task.md claiming a legacy id, allowed_files of ['*'] or a wildcard first segment, an invariant sentence weakened under its id, a schema or AGENTS.md edited on the audited head, an undeclared script change that main-tests must fail); legacy task ids are grandfathered by the checked-in list scripts/legacy-task-ids.txt, which only shrinks and is excluded from the line cap as data"
premises:
  - claim: "the unit-test workflow runs on pull_request from the PR's own workflow file and has no path filter, and its test job is a required check"
    command: "sed -n 1,16p .github/workflows/test.yaml; gh api repos/mryfmo/dotfiles/rulesets/24397953 --jq '.rules[]|select(.type==\"required_status_checks\")|.parameters.required_status_checks[].context'"
    output: "pull_request: branches: [main]; no workflow-level path filter; required contexts include test (ubuntu-24.04, server), test (ubuntu-24.04, client), test (macos-14, client)"
  - claim: "every unit module resolves the repository root from its own file path, so main's modules must be overlaid on a complete copy of the PR tree, not run from a bare extract"
    command: "grep -l 'Path(__file__)' tests/unit/test_*.py | wc -l; ls tests/unit/test_*.py | wc -l"
    output: "34; 34"
  - claim: "main's tests/unit can be fetched into a PR job without checking out main's tree over the PR's: git fetch origin main and git archive origin/main tests/unit | tar -x -C <dir>"
    command: "git archive origin/main tests/unit | tar -t | head -3"
    output: "tests/ tests/unit/ tests/unit/test_agent_session_staleness.py"
---

# AGMSG-TASK dotfiles-T128-v0-main-tests-a01 — regime v3 wave V0: main's tests run against the PR's scripts

DRAFT; the first implementing wave (T128 INV-12, V0): lands before V1 so the oracle is on `main` before the code it judges. Design tier (workflow). Claude seat, `.claude/worktrees/worker-c`, branch `feat/main-tests` from `origin/main`. Contract-first applies from V1 onward; V0 itself ships its script and its test together because the harness it adds is the mechanism.

## What to build

1. `scripts/main-tests.sh <base-ref>`: when the diff `$(git merge-base <base> HEAD)..HEAD` touches `scripts/**` or `home/dot_local/bin/**`: copy the PR's working tree to a temporary directory (`git archive HEAD | tar -x -C <tmp>`, so the test modules' own-path `ROOT` resolution lands on a complete tree), overlay `main`'s `tests/unit` on it (`git archive <base> tests/unit | tar -x -C <tmp>`, main's modules replacing the PR's), read the single `.orchestration/*/task.md` in the range with PyYAML (`uv run --no-project --with pyyaml`; the task id, its `allowed_files` and the `tests/unit/*.py` entries among them; a boundary PR has none and the whole run is in undeclared mode), and run in `<tmp>`: (a) undeclared mode: every main module other than the task's declared `tests/unit` entries, as it is; (b) declared mode: each declared module from main's copy with `REGIME_CONTRACT=1` (ordinary tests skip, `@contract` tests run), failing with `main-tests: no contract on main for <module>` when the task.md is design tier and main's copy has no `@contract` test (the tier is the task.md's stamped `tier:` key, which V1's schema keeps and requires to equal the derived tier; a missing stamp is treated as design, so V0 needs neither `high_risk_paths.py` nor `--print-tier`, which do not exist yet); (c) promotion check: when the task id does not end in `-contract-a01`, the PR's own copy of each declared module (read from HEAD, not the overlay) must carry no contract decorator, detected with Python's `ast`: any decorator that resolves to the `contract` name imported from `regime_contract` under any alias (`from regime_contract import contract [as X]`, `import regime_contract [as Y]` then `@Y.contract`, and `skipUnless(os.environ.get('REGIME_CONTRACT')…)` written inline), else fail with `main-tests: contract still dormant in <module>` (other ways of writing a skip are the design-tier audit's to catch); exit by the combined result; print `main-tests: no script change` and exit 0 when no script changed. A module main has and the PR deletes still runs (it is main's copy). shdoc header; the ast check may live in a small Python helper beside the script (`scripts/lib/contract_markers.py`), and the PR cap is the size bound.
1b. `tests/unit/regime_contract.py`: the decorator `contract` = `unittest.skipUnless(os.environ.get('REGIME_CONTRACT') == '1', 'dormant contract')`, and a note that a contract PR (`<task>-contract-a01`) ships only such tests so it merges before the implementation, and that the implementation PR removes the decorator from the contracts it satisfies (they become ordinary tests in its tree; main-tests still judges the PR against main's dormant copy), so nothing stays dormant after the wave lands.
2. `.github/workflows/test.yaml`: a job `main-tests` (ubuntu-24.04, `needs: changes`, always reports: runs the script, which exits 0 on an unrelated diff) with `fetch-depth: 0` and `git fetch origin main`; the operator lists it as a required check at acceptance.
3. `tests/unit/test_main_tests.py`: scratch repository with a `main` branch carrying a test module (ordinary tests and one contract test, each resolving `ROOT` from its own path as the real modules do) and PR branches that (a) change an undeclared script so main's ordinary test fails, (b) change a declared script whose contract fails under `REGIME_CONTRACT=1` while its ordinary test is skipped, (b2) a task.md stamped `tier: design` (and one with no stamp) declaring a module with no contract on main fails with the no-contract message while one stamped `tier: review` passes, (b3) an implementation PR whose declared module still carries `@contract` fails with the still-dormant message while a `-contract-a01` task id passes, (b4) the same under the aliases `import regime_contract as rc` / `@rc.contract`, `from regime_contract import contract as c` / `@c`, and an inline `skipUnless(os.environ.get('REGIME_CONTRACT') == '1')`, (c) delete the test module (main's copy still runs and fails), (d) change no script (skip path). Each fails when its rule is removed.
4. SKILL Worker Playbook: the two-mode protocol in one paragraph (a design-tier code wave lands `<task>-contract-a01` first with dormant `@contract` tests, mergeable because they skip in ordinary CI; the implementation PR declares the script in `allowed_files`, `main-tests` activates main's contracts against it and fails a design-tier PR with no contract on main; the implementation PR removes the decorator from the contracts it satisfies, and `main-tests` fails it while any remains; undeclared script changes meet main's ordinary tests).

## Validation

the module under `make unit-test`; `shellcheck scripts/main-tests.sh`; YAML-parse the workflow; `scripts/main-tests.sh origin/main` on your own branch pasted; `invariant: INV-12 → …` lines.

## First commit

Copy this task file byte-identical to `.orchestration/dotfiles-T128-v0-main-tests-a01/task.md`; evidence beside it.

## Completion

Draft PR within 30 minutes (`feat(ci): run main's unit tests against a pull request's scripts`), CI, Bot wait, artifacts, `memory add`, RESULT via `agmsg-dispatch … claude-deep-dot w5:p1`. max_turns=10. Forbidden: anything else; `make update`; thread resolution.
