---
format: 2
task_id: dotfiles-T133-task-generator-plan-check-a05-checker
kind: code
security: true
design: 5.14 items 2, 3, 8, 9
design_review:
  design: .orchestration/plans/024-design-quality.md
allowed_files:
  - scripts/orchestrator/task-consistency-check.py
  - tests/unit/test_task_consistency_c11_c15.py
  - tests/unit/test_task_checkers.py
  - .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/**
after: []
reset_of: [dotfiles-T133-task-generator-plan-check-a04]
retained_predecessor_directories: []
expected_result_file: .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/report.md
expected_validation_file: .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/validation.md
expected_sandbox_file: .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/sandbox.md
expected_learning_file: .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/learning.md
expected_autoskill_file: .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/autoskill.md
expected_measure_file: .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/measure.md
threat_table:
  - {control: "scripts/orchestrator/task-consistency-check.py", disposition: "residual: Checker defenses start after the parent has executed; fixtures and final-head audit establish checker behavior, while pre-start execution and concurrent same-UID replacement remain outside their protection."}
  - {control: "tests/unit/test_task_consistency_c11_c15.py", disposition: "residual: Temporary repositories and observed subprocess arguments exercise the real checker; fake API responses establish protocol behavior rather than live GitHub availability."}
  - {control: "tests/unit/test_task_checkers.py", disposition: "residual: Historical fixtures retain their check coverage; changed expectations require an identified contract change and cannot conceal unrelated findings."}
  - {control: ".orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/**", disposition: "residual: Commit the dispatched copy and required evidence before RESULT; these artifacts contain no production helpers, executable workaround, credentials or approval authority."}
  - {control: "checker-side interpreter selection after startup", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_interpreter_resolution_order"}
  - {control: "gh child environment", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_gh_child_preserves_parent_tokens"}
  - {control: "canonical-main design read", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_uses_canonical_main_only"}
  - {control: "C6 canonical receipt binding and design hash", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
  - {control: "fixture and evidence symlink exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_symlink_to_applied_file_is_finding"}
  - {control: "fixture and evidence case-alias exemptions", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_case_alias_to_applied_file_is_finding"}
  - {control: "path normaliser", disposition: "residual: Each declared grammar case has a separate behavioral fixture below; filesystem identity checks remain necessary after lexical normalization and do not prevent same-UID races."}
  - {control: "C16 rule", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c16_requires_reference_and_all_item_rows"}
  - {control: "task metadata", disposition: "residual: The orchestrator verifies scope, reset lineage, empty retained-directory inventory, caps and dispatched-copy identity before sending and accepting this task."}
  - {control: "task metadata reset copies: .orchestration/dotfiles-T133-task-generator-plan-check-a04/task.md and .orchestration/dotfiles-T133-task-generator-plan-check-a05-checker/task.md", disposition: "residual: The predecessor pathname records lineage only; this fresh PR retains no predecessor directory and creates only its own byte-identical dispatched task copy."}
  - {control: "metadata separators", disposition: "residual: The complete dispatched-file digest covers the YAML separators and body; quoted probes and evidence are data rather than execution authority."}
  - {control: "in-process effects", disposition: "residual: C14 interprets only its existing fixed read-only vocabulary and requires the dispatched-byte digest; no shell, arbitrary Python operand or task-supplied executable is introduced."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: No caller or workflow edit is authorized; the unchanged parent retains PATH and its shared cache. Checker compatibility tests do not establish parent sanitization, and token values never appear in evidence."}
  - {control: "new or renamed scripts", disposition: "residual: This slice changes one existing production script and adds no resolver, wrapper, dependency, template or artifact-directory runtime code."}
  - {control: "orchestrator effect dispatch.sh keeps calling the checker unchanged", disposition: "residual: test_dispatch_env_i_invocation proves checker compatibility only; dotfiles-T133-loop-limits-a01 owns dispatch.sh and dotfiles-T133-trusted-entrypoint-binding-a01 owns executable binding before checker startup."}
  - {control: "orchestrator effect merge", disposition: "residual: The worker never merges; final integration follows Orchestrator Playbook step 10 and binds the merge to the audited head."}
  - {control: "orchestrator effect update-branch", disposition: "residual: A changed head requires refreshed applicable CI, feedback and audit evidence before integration."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: No forced removal is assigned; preserve the withdrawn branch and its evidence rather than discarding worker state."}
  - {control: "5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: Item 0 applies by reference; this slice establishes neither separate OS identities nor credential isolation."}
  - {control: "5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: Item 1 applies by reference; this task uses a Codex sandbox and makes no Claude deployment claim."}
  - {control: "5.14 item 2: 無害化した環境を最初に", disposition: "residual: Item 2 applies by reference; PATH-selected mise/uv execute before checker defenses. dotfiles-T133-loop-limits-a01 owns dispatch.sh, dotfiles-T133-trusted-entrypoint-binding-a01 owns executable binding, and dotfiles-T133-ci-efficiency-followup-a04 owns the resolver and private UV_CACHE_DIR; this slice closes no parent execution boundary."}
  - {control: "5.14 item 3: 信頼パスの境界検査", disposition: "residual: Item 3 applies by reference; normalization does not replace filesystem boundary checks or establish host isolation."}
  - {control: "5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Item 4 applies by reference; retained consumed-byte and executable-binding checks cannot exclude concurrent same-UID interference."}
  - {control: "5.14 item 5: 出力と予約の同一性", disposition: "residual: Item 5 applies by reference; this read-only checker adds no reservation or integration resource."}
  - {control: "5.14 item 6: 正直な残余", disposition: "residual: Item 6 applies by reference; the report distinguishes fixture observations, compatibility warnings and unverified deployment."}
  - {control: "5.14 item 7: 検証", disposition: "residual: Item 7 applies by reference; retain checker-specific negative controls and disclose unavailable platform coverage without claiming it passed."}
  - {control: "5.14 item 8: 承認はコミット済み台帳から読む", disposition: "closed: tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes"}
  - {control: "5.14 item 9: 私設キャッシュ", disposition: "residual: Item 9 applies by reference; unchanged dispatch selects shared ~/.cache/uv, permitting pre-checker cache poisoning. dotfiles-T133-ci-efficiency-followup-a04 owns the resolver and private UV_CACHE_DIR; dotfiles-T133-loop-limits-a01 and dotfiles-T133-trusted-entrypoint-binding-a01 own the parent and executable binding. Absolute-cache checks and fallback warnings do not mitigate this execution risk."}
  - {control: "5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Item 10 applies by reference; unavailable commands produce a blocked PONG and confer no sandbox escape."}
premises:
  - claim: The authoring checkout and observed origin/main share this revision; this is historical probe provenance, not canonical GitHub authority.
    command: |-
      git rev-parse HEAD origin/main
    output: |-
      ba318e5369b14a79d6f515e87b685c9bcb30c12e
      ba318e5369b14a79d6f515e87b685c9bcb30c12e
  - claim: Historical dispatch retains PATH and shared UV_CACHE_DIR while stripping TRUSTED_PYTHON and TRUSTED_BIN_DIR; this establishes compatibility inputs, not a sanitized execution boundary.
    command: >-
      git show ba318e5369b14a79d6f515e87b685c9bcb30c12e:scripts/orchestrator/dispatch.sh | awk 'NR >= 113 && NR <= 119 || NR == 238 {print NR ":" $0}'
    output: |-
      113:clean=(env -i PATH="${PATH}" HOME="${home}" UV_CACHE_DIR="${home}/.cache/uv")
      114:for v in LANG LC_ALL; do
      115:    [[ -z ${!v:-} ]] || clean+=("${v}=${!v}")
      116:done
      117:while IFS= read -r v; do
      118:    [[ ${v} != AGMSG_* ]] || clean+=("${v}=${!v}")
      119:done < <(compgen -e)
      238:        out="$(uvr python -I "${here}/task-consistency-check.py" --root "${root}" "${tf}" 2>&1)" || {
  - claim: The withdrawn checker requires stripped inputs, omits applied instruction kinds, ignores probe status and permits local-only designs.
    command: >-
      git show 7a201eab:scripts/orchestrator/task-consistency-check.py | awk 'NR==29 || NR==31 || NR==48 || NR==49 || NR==145 || NR==169 || NR==170 || NR==187 || NR==200 || NR==405 || NR==407 || NR==419 || NR==421 || NR==429 {print NR ":" $0}'
    output: |-
      29:PYTHON = os.environ.get("TRUSTED_PYTHON", "")
      31:    sys.exit("refused: TRUSTED_PYTHON must be set to an absolute regular file")
      48:APPLIED = (".sh", ".py", ".yaml", ".yml", ".json", ".toml")
      49:APPLIED_DIRS = ("home/", "scripts/", ".githooks/", ".github/")
      145:        sys.exit(f"refused: trusted executable binding missing: {name}")
      169:            "TRUSTED_PYTHON": str(PYTHON),
      170:            "TRUSTED_BIN_DIR": directory,
      187:    result = launch(root, executable("gh"), "api", "repos/mryfmo/dotfiles/git/ref/heads/main", "--jq", ".object.sha")
      200:    result = launch(root, executable("gh"), "api", endpoint)
      405:        if not re.search(r"[*?\[]", a) or a.startswith(("tests/fixtures/", own_dir)) or not confined(root, a):
      407:        for f in filter(None, git(root, "ls-files", "-z", "--", f":(glob){a}").stdout.split("\0")):
      419:        got, _code, err = rerun(cmd, root)
      421:        if got is None or " ".join(got.split()) != " ".join(want.split()):
      429:        fails += [f"C15 design {design} is not on origin/main"] if mine or not (present or inside.exists()) else []
  - claim: The resolver is absent from the observed main tree.
    command: |-
      git ls-tree --name-only ba318e5369b14a79d6f515e87b685c9bcb30c12e -- scripts/orchestrator/trusted-interpreter.sh
    output: ""
    exit_code: 0
  - claim: The resolver is also absent from the authoring working tree.
    command: |-
      test -e scripts/orchestrator/trusted-interpreter.sh
    output: ""
    exit_code: 1
  - claim: CI supplies token authentication through the job environment.
    command: >-
      git show ba318e5369b14a79d6f515e87b685c9bcb30c12e:.github/workflows/test.yaml | awk 'NR==57 {print NR ":" $0}'
    output: |-
      57:      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  - claim: Historical local absence only; this probe is not canonical publication evidence and must not be used for the dispatch prerequisite.
    command: |-
      git cat-file -e origin/main:.orchestration/plans/024-design-quality.md
    output: ""
    stderr: "fatal: path '.orchestration/plans/024-design-quality.md' exists on disk, but not in 'origin/main'"
    exit_code: 128
  - claim: Wholesale inheritance already consumes 389 changed production lines and 733 added test lines.
    command: |-
      git diff --numstat ba318e5369b14a79d6f515e87b685c9bcb30c12e 7a201eab -- scripts/orchestrator/task-consistency-check.py tests/unit/test_task_consistency_c11_c15.py tests/unit/test_task_checkers.py
    output: |-
      353	36	scripts/orchestrator/task-consistency-check.py
      28	11	tests/unit/test_task_checkers.py
      705	0	tests/unit/test_task_consistency_c11_c15.py
---

# AGMSG-TASK dotfiles-T133-task-generator-plan-check-a05-checker

🤖 I read the AGENTS.md for mryfmo/dotfiles.

## Goal and lineage

Amendment 1 addresses all five findings in `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a05-checker-text-security-1368f71.md.last.md`. Following the scope pattern of `dotfiles-T133-record-ledger-carry-a01` reviewed at `f3bfcc6`, this slice claims no execution-boundary closure; parent hardening remains its named owners’ deliverable.

[memory:failure] PR #417's a01 → a02 → a03 → a04 lineage was withdrawn after the complete task-level audit of `7a201eab2e77596c9a7bc421162b2f3fde25f6f7`: dispatch regression, unpublished design dependency, implementation defects, missing committed evidence and repeated finding classes without completed re-plans.

Read `.orchestration/validation/dotfiles-T133-task-generator-plan-check-a04-audit-7a201ea.md.last.md` whole and `.orchestration/acceptance/dotfiles-T133-task-generator-plan-check-a04.md`, including its `re-plan: glob-filter` decision.

[memory:decision] Plan 024 P1-12 now delivers only the checker and its tests. Start from the checker shown by `git show 7a201eab:scripts/orchestrator/task-consistency-check.py`, selectively porting its checker behavior onto a fresh branch from `origin/main`. Do not cherry-pick the withdrawn three-script implementation.

Use branch `tools/task-generator-plan-check-a05-checker` and a new PR. Preserve PR #417 and its branch as withdrawn history. `task-from-plan.py`, `plan-check.py`, the bundled template, workflows, dispatch, resolver implementation, deployment and canonical orchestration records are outside this slice.

## Dispatch prerequisite and design

Dispatch waits for boundary PR #435 to merge. Inside the sandbox, obtain canonical main with `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha` and validate the returned SHA as exactly 40 lowercase hexadecimal characters before substituting it for `<sha40>`.

Read that pinned content with `gh api 'repos/mryfmo/dotfiles/contents/.orchestration/plans/024-design-quality.md?ref=<sha40>' --hostname github.com --jq .content | base64 -d | grep -F 'Codex 席は sandbox（workspace-write）がツールの書き込み全部を自席の worktree と列挙パスに限る。'`. Require successful exits from every pipeline stage and reject malformed or missing content; a successful grep alone is insufficient.

Record #435's merged state from the fixed repository/host API, the pinned main SHA, decoded content SHA-256, commands and stage exits before sending. Never use local `origin/main`, `git cat-file`, replacement objects or a local design/digest as prerequisite authority. `after: []` expresses no worker-task dependency and does not waive this boundary.

Design 5.14 at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen under D-024-29 and applies by reference under D-024-30.
Design 5.14 item 2, 「無害化した環境を最初に」, applies by reference.
Design 5.14 item 3, 「信頼パスの境界検査」, applies by reference.
Design 5.14 item 8, 「承認はコミット済み台帳から読む」, applies by reference.
Design 5.14 item 9, 「私設キャッシュ」, applies by reference.

The pasted premises are authoring observations. Re-run applicable probes before dispatch and paste current results in Checks; historical local publication absence supplies no authority and is replaced by the API prerequisite above. Their pipelines do not extend C14's executable vocabulary or grant permission to run shell text.

## Implementation contract

1. Resolve the interpreter from `scripts/orchestrator/trusted-interpreter.sh` when present in the checker tree, using its landed interface; otherwise use supplied `TRUSTED_PYTHON`; otherwise use the real `sys.executable` and emit an explicit stderr warning naming that fallback. Validate the selected interpreter before use. An existing resolver's failure or an invalid supplied interpreter is a refusal, not a reason to fall through. Do not add interpreter PATH discovery.

   Neither `TRUSTED_PYTHON` nor `TRUSTED_BIN_DIR` may become mandatory for existing callers. Executable binding must also work when dispatch omits both, retaining checker-side defenses. No dispatch edit or outer environment prefix is an acceptable repair. Keep the existing absolute-cache requirement; dispatch supplies an absolute shared cache, satisfying that syntax check without satisfying item 9.

   These defenses begin after the parent has executed PATH-selected mise/uv, including this host’s mise shim and cached dependencies. Later interpreter validation or a fallback warning cannot undo that execution or prevent shared-cache poisoning. Parent hardening belongs to dotfiles-T133-loop-limits-a01, executable binding to dotfiles-T133-trusted-entrypoint-binding-a01, and the resolver/private UV_CACHE_DIR to dotfiles-T133-ci-efficiency-followup-a04; none is delivered or closed here.

2. C14 consumes `(stdout, exit_status, stderr)`. Every nonzero probe status produces a finding even when stdout equals the expected output, including empty stdout. Retain same-byte digest authorization, explicit warning without authorization, whitespace comparison and the fixed read-only probe vocabulary. Unsupported commands never reach a shell.

3. For `gh` children, preserve `GH_TOKEN` and `GITHUB_TOKEN` exactly when present in the parent, including testing each independently, both together and neither. CI supplies `GITHUB_TOKEN`; discarding it breaks token-authenticated runs without stored credentials. Keep other sanitization intact, bind the API host explicitly, and never print token values. This does not change dispatch's own environment forwarding.

4. C15 accepts a referenced design only from canonical GitHub main, even if the task has no invariants. Obtain its validated 40-hex SHA with `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`, then read `gh api repos/mryfmo/dotfiles/contents/<path>?ref=<sha40> --hostname github.com`. Bind every authoritative API read to this repository and host. Local-only designs produce C15 findings; API errors fail closed. Retain assignment-set and byte-equality checks. Local refs, objects, remote URL rewrites and hostile `GH_HOST` supply no design authority.

   When `design_review.receipt` is supplied, C6 validates its receipt binding and recorded design SHA-256 against the same canonical design bytes at that same pinned SHA. Compute the hash over the decoded API bytes before text parsing; absent canonical design or receipt binding, malformed/mismatched hashes and API failures cannot pass. Share that snapshot with C15; neither a mutable local design nor its matching local receipt supplies authority. The regression asserts a C6 finding for a forged local receipt naming a design absent from canonical main, and for matching local design/receipt bytes that disagree with an existing canonical design even when C15 otherwise passes; include a matching canonical control.

5. Use one shared path normaliser for every path-bearing check: scopes, threat-row path tokens, design paths, selector paths, applied-file classification and C14 file operands. Git refs remain refs. State and implement this grammar:
   - Inputs are repository-relative POSIX literal files, trailing-slash directories, or globs. Root files require no slash. Remove redundant `./` components consistently.
   - Globs use component-local `*`, `?` and bracket classes; a whole-component `**` spans zero or more components. Git pathspec magic, exclusions and absolute paths are rejected rather than interpreted as globs.
   - Reject parent traversal, including `../../x/*.py`, with a confinement finding; do not silently skip the scope. Resolve filesystem boundaries separately and reject escaping symlink matches.
   - A directory row and its child row are distinct entries. Associate normalized path tokens with their own entries; ancestor substrings must not make the child row violate C7b. A row actually naming two entries still fails.
   - Enumerate matched regular files under the scope's fixed roots, including ignored and untracked files, without following directory symlinks or scanning Git administration. The index is not exclusion authority.
   - Classify root `AGENTS.md` and `Makefile`, and `.claude/skills/<name>/SKILL.md`, as applied files. C12 requires concrete rows for applied wildcard matches. Preserve legitimate fixture-data and own-evidence exemptions only after confinement and resolved-target classification.
   - A fixture/evidence path is exempt only when its realpath lies beneath the corresponding exempt root and its classification by that resolved path agrees with the exemption. Use filesystem identity and case-insensitive comparison where applicable. An in-repository symlink or case alias that disguises an applied production file as exempt produces a finding; lexical prefixes alone never grant an exemption.

6. Add C16 under D-024-30. A `security: true` orchestrator-side task must explicitly reference design 5.14 and have exactly one threat row naming each item 0–10. Determine applicability from normalized orchestrator scope, including covering globs, without a new caller flag. Match item numbers distinctly, reject omissions and duplicates, and preserve non-applicable tasks. C16 checks references and coverage; it does not paraphrase or amend the frozen design.

7. This reset uses an explicit retained-directory inventory: `retained_predecessor_directories: []`. The new PR retains no predecessor artifact directory; `reset_of` names a04 for lineage only. Create the own task copy without importing or deleting a01–a04 artifacts. Exercise C2/C3 with this reset shape, including rejection of a predecessor scope disguised with `./`. The regime job receives this inventory and the complete changed-file list; do not disposition scope failures as deferred.

Retain C1–C15 behavior except the specified corrections, including C11 class selectors, confinement, fixed-probe non-execution and checker-specific trusted-execution negative controls. Port only checker fixtures; do not require the two deferred scripts to exist.

## Required regression fixtures

Each selector below exists in the final tree, has an identified behavioral failure against the production checker at `7a201eab`, and passes against the slice head. Include valid controls and assert the intended finding or behavior.

| Behavior | Selector |
| --- | --- |
| Resolver → supplied interpreter → warned fallback; invalid selected inputs refuse | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_interpreter_resolution_order` |
| Real checker succeeds under dispatch's exact existing invocation without either stripped variable | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_dispatch_env_i_invocation` |
| Nonzero C14 status fails despite matching stdout | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c14_rejects_failed_probe_with_matching_stdout` |
| Parent tokens survive only the intended child boundary | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_gh_child_preserves_parent_tokens` |
| Local-only design rejected without invariants; canonical repository, host and SHA used | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c15_uses_canonical_main_only` |
| Forged local receipt/design cannot pass C6; receipt hash uses the same pinned canonical bytes as C15 | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c6_receipt_uses_canonical_design_bytes` |
| Glob semantics and rejection of Git pathspec magic | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_distinguishes_globs_from_git_pathspecs` |
| Root literals and concrete applied root-file coverage | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_covers_root_files` |
| Separate directory and child rows pass; genuinely combined rows fail | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_separates_directory_and_child_rows` |
| Equivalent `./` spellings produce the same checks | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_normalises_dot_spellings` |
| Escaping scopes and symlinks produce confinement findings | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_path_grammar_rejects_escaping_scopes` |
| Exempt in-repository symlink to applied production file produces a finding; legitimate fixture control passes | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_symlink_to_applied_file_is_finding` |
| Exempt case alias to applied production file produces a finding under deterministic case-insensitive semantics | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_exempt_case_alias_to_applied_file_is_finding` |
| Applied skill instruction files require concrete rows, including untracked matches | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c12_covers_applied_skill_instructions` |
| Missing reference, missing item and duplicate item fail C16; complete table passes | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_c16_requires_reference_and_all_item_rows` |
| Empty retained inventory and reset-copy rows; hidden predecessor scope rejected | `tests/unit/test_task_consistency_c11_c15.py::TaskConsistencyC11C15Test::test_reset_scope_rejects_hidden_predecessor_artifacts` |

The dispatch fixture reproduces `env -i PATH=... HOME=... UV_CACHE_DIR=...`, optional `LANG`/`LC_ALL`, exported `AGMSG_*`, and the existing pinned offline uv launch followed by `python -I <checker> --root <root> <task>`. Assert the actual argument/environment boundary and real checker verdict; a stubbed checker or unrelated refusal is not proof. This establishes checker compatibility only, never sanitization before parent execution or private-cache protection. Case-alias fixtures exercise insensitive semantics even on a sensitive host; report unavailable native coverage separately.

## Check

Write regressions before fixes. Record checker revision and SHA256, regression-source SHA256, actual interpreter/version, expanded commands, complete stdout/stderr and exits for every historical red and final green. Import errors, unavailable dependencies, missing tests, unrelated launch refusals and zero-test runs are not red proofs.

Use temporary repositories, temporary absolute caches, synthetic token markers and the existing fixture patterns. Run the two complete checker modules with the trusted uv/interpreter, isolated Python and offline dependencies, for example `uv run --no-config --no-project --offline --python <absolute interpreter> --with pyyaml python -I -m unittest discover -s tests/unit -p 'test_task*.py' -v`. Record actual absolute bindings and commands.

Exercise the supported Python 3.12 floor and the current runner interpreter. Run `make unit-test`, required formatting checks and relevant validators. Compare any inherited failure with the unchanged base in the same environment; never label it green or repair outside scope. Do not run Bats locally. Final required GitHub Actions checks must pass before RESULT.

Paste the mutation count and per-mutation outcomes: `mutations=<observed> killed=<observed> survived=<observed>`. Temporarily disable each changed contract behavior independently and show its named fixture detects the mutation. Do not commit mutants or add a mutation framework; unexplained survivors block completion.

The complete final diff against the merge-base with `origin/main` has at most 400 changed lines outside `tests/` and `.orchestration/`, all in the one allowed production file.
The complete final diff has at most 700 added lines under `tests/`.
The task text is at most 250 lines and has exactly four allowed_files entries.

Paste `git diff --numstat origin/main...HEAD`, `git diff --name-only origin/main...HEAD`, per-file arithmetic and both totals in measure.md and RESULT. Count source additions plus deletions and test additions; also disclose test deletions. The measured a04 inventory already exceeds the test-addition cap, so selectively port fixtures. Do not raise caps, hide runtime code in artifacts or remove defenses to fit.

Run the checker on the dispatched copy and record C14's warning without `--premises-sha`; authorized C14 fixtures use their supplied trusted digest. Do not invent a digest from branch bytes as dispatch authority or add shell support for the authoring probes.

## Completion and evidence

All commands obey Worker Playbook step 4: sandbox-only. A denial or unavailable operation produces `AGMSG-PONG v1 status=blocked` with the exact command, exit, output and boundary; wait for re-tasking. Never retry through an escape, alternate tool or broader permission.

Commit report.md, validation.md, sandbox.md, learning.md and measure.md under this task's artifact directory before RESULT. Also commit the byte-identical task.md, AutoSkill status or not-used record, and worker review evidence. Verify these paths with `git ls-files` and show no required evidence remains untracked. This explicitly overrides the generic untracked-artifact handoff for this task; Codex plan/todo/learn worklogs remain uncommitted.

Use agent-side Crit data and a worker receipt in the allowed artifact directory; no browser review, publication or human review request. Run `make require-crit-review` before completion with the required evidence. Keep stopped lineage history and apply INV-6/S1; a repeated class requiring redesign is not another private patch round.

Push the fresh branch, open the new PR with an English title/body, and follow Worker Playbook's bounded CI/Bot procedure. Every correction round counts. A final evidence push requires fresh applicable CI. The worker never merges or changes canonical acceptance, decision or plan records.

Send `AGMSG-RESULT v1 status=ready_for_review` only after required checks pass. Include full head/base, branch, new PR, task-copy SHA256, changed-file inventory, retained predecessor directories `[]`, final numstat/totals, selectors, red/green and mutation counts, CI/Bot observations, proposed feedback dispositions and every artifact path. Report `cost:` with observed figures or `n/a`.

The orchestrator obtains the final-head task audit and required security review, then follows Orchestrator Playbook step 10: complete feedback sweep, dispositions, audit, acceptance record and integration gate with `PR_FEEDBACK_EVIDENCE`, `AUDIT_EVIDENCE` and `ACCEPTANCE_EVIDENCE`. No previous PR's evidence approves this head.

## Checks (pasted by the orchestrator before each send)

```
dispatch to a012 (worker-g), 2026-10-20T03:20:29Z; task-consistency-check.py: OK; C-80: 1368f71 incorrect (3 P1 + 2 P2 on the execution boundary the checker cannot provide) -> amendment 1 (P1-6 pattern), cd37b74 correct; dispatch prerequisite probed through the repository API at 2026-10-20T03:20:29Z: `gh api repos/mryfmo/dotfiles/contents/.orchestration/plans/024-design-quality.md?ref=60a6fb2b324d0381c4a6e539b37c650105154a7e --hostname github.com --jq .content | base64 -d | grep -c "hook handlers of every documented type"` printed 1 (the design is on main since boundary #435 merged 03:18:08Z); reset_of a04 (PR #417 withdrawn: 2 P1 incl. the TRUSTED_PYTHON regression; C-61 spent); fresh branch from origin/main 60a6fb2b; security: true; files disjoint from every in-flight task; measured text: 250 lines, 4 allowed files
```

Deferred checks and changes: generator, plan checker, workflows, dispatch implementation, resolver implementation, deployment and local Bats.
Residual risk: shared-UID interference and shared credentials remain; unchanged PATH-selected parent execution and shared-cache poisoning are owned residuals, and checker validation, fallback warnings and fixtures establish no execution-boundary closure or host isolation.