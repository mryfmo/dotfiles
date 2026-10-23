---
format: 2
task_id: dotfiles-T133-hold-playbook-a02
kind: code
security: true
allowed_files:
  - scripts/orchestrator/hold-playbook.sh
  - tests/unit/test_hold_playbook.py
  - .orchestration/dotfiles-T133-hold-playbook-a02/**
after: [dotfiles-T133-worker-write-boundary-slice2-a01, dotfiles-T133-ci-efficiency-followup-a04]
reset_of: [dotfiles-T133-hold-playbook-a01]
threat_table:
  - control: scripts/orchestrator/hold-playbook.sh interpreter selection
    disposition: "closed: tests/unit/test_hold_playbook.py::HoldPlaybookTests::test_child_uses_trusted_interpreter_despite_checkout_config_and_path"
  - control: tests/unit/test_hold_playbook.py
    disposition: "residual: temporary fixtures exercise the retained behavior and the three class fixes; fake-tool assertions establish the consumer contract, not host installation provenance or uv internals"
  - control: .orchestration/dotfiles-T133-hold-playbook-a02/**
    disposition: "residual: current artifacts remain in this task directory; their claims are checked against the final diff, tested heads and CI rather than accepted as authority"
  - control: task-copy transition from .orchestration/dotfiles-T133-hold-playbook-a01/task.md to .orchestration/dotfiles-T133-hold-playbook-a02/task.md
    disposition: "residual: the first a02 push deletes only the predecessor task copy and adds this dispatched text byte-identically; the orchestrator compares the complete a02 copy and its own dispatch SHA-256"
  - control: branch evidence records under .orchestration/dotfiles-T133-hold-playbook-a02/
    disposition: "residual: report, validation, sandbox, learning, AutoSkill and worker review records are untrusted claims; predecessor evidence remains unchanged and explicitly historical"
  - control: task metadata
    disposition: "residual: the orchestrator checks identity, security, allowed_files, dependencies, reset_of and threat rows before dispatch and at acceptance; an incomplete checker is not evidence that missing checks passed"
  - control: metadata separators
    disposition: "residual: YAML is parsed as data from the bounded first front-matter document; the orchestrator's whole-file task-copy comparison covers separators and the body"
  - control: in-process effects
    disposition: "residual: production creates a replan and conditionally appends a pending decision under the operator's authority; these are writes contained by item 2, while tests perform them only in fixture repositories"
  - control: workflow and interpreter or environment inputs
    disposition: "residual: a trusted parent supplies the clean environment before execution; the program verifies entry state, consumes the existing resolver and uses fixed offline uv arguments and a protected private cache; no workflow or resolver file is edited"
  - control: new or renamed scripts
    disposition: "residual: none in this reset; hold-playbook.sh already exists at c206774c, its helper remains embedded, and no sibling executable or new production entry point is authorized"
  - control: orchestrator effect merge
    disposition: "residual: only the orchestrator merges PR #426 after Orchestrator Playbook step 10, with gh pr merge --squash --match-head-commit bound to the audited final head; this procedure does not prevent unrestricted same-UID credential use"
  - control: orchestrator effect update-branch
    disposition: "residual: the orchestrator updates the existing branch after dependency merges; every moved head receives the applicable fresh CI, feedback, audit, security review and gate evidence before integration"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; the worker performs no removal, and any orchestrator-forced removal records the discarded uncommitted state in acceptance"
  - control: design 5.14 item 1 write boundary
    disposition: "residual: dispatch requires the worker-write-boundary dependency and verification of its deployed protection; same-UID processes outside a seat sandbox remain outside that protection"
  - control: design 5.14 item 2 environment before execution
    disposition: "residual: item 1 requires trusted-parent pre-exec sanitization and program-side refusal; a loadable inherited library can execute before a shell statement, so the program cannot repair an untrusted parent"
  - control: design 5.14 item 3 trusted path boundaries
    disposition: "residual: item 2 confines the ledger and helper-produced artifacts with descriptor-relative no-follow opens and real-directory parent chains; the resolver owns interpreter validation, and this task does not establish path protection for other mechanisms"
  - control: design 5.14 item 4 execute the verified realpath
    disposition: "residual: the child consumes the resolver's single absolute interpreter realpath without rediscovery; descriptor-relative writes avoid reopening checked destinations, but unrestricted same-UID replacement and general evidence snapshotting remain residual"
  - control: design 5.14 item 5 output and reservation identity
    disposition: "residual: the retained replan is identified by task id and created exclusively, with exit 4 for an existing entry; this helper introduces no physical-slot reservation or head-named output, and does not implement the contract's general lock mechanism"
  - control: design 5.14 item 6 honest residuals
    disposition: "residual: named tests establish the declared class fixes only; host protection, deployment provenance, shared credentials and controls belonging to other mechanisms remain explicitly residual"
  - control: design 5.14 item 7 verification
    disposition: "residual: the retained fixture suite and item-specific red-then-green regressions verify this reset; the common trusted-execution helper and the complete four-test program for every orchestrator mechanism are not claimed implemented here"
  - control: design 5.14 item 8 committed approval and authenticated changesets
    disposition: "residual: the appended pending row is a proposal, never permission approval; this helper neither authenticates PR changesets nor authorizes integration, whose evidence provenance remains the orchestrator's responsibility"
  - control: design 5.14 item 9 private cache and shared interpreter resolver
    disposition: "residual: this consumer uses the P1-3 resolver, a protected anchored uv cache and offline configuration-free execution; the dependency owns resolver implementation and installation validation, and other consumers are outside this task"
  - control: design 5.14 item 10 commands remain inside the sandbox
    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; an operation that cannot complete there produces a blocked PONG without escalation or an alternate-tool bypass"
  - control: design 5.14 item 0 same-UID threat model
    disposition: "residual: these controls reduce accidents and prompt-injection effects, not malicious unrestricted same-UID activity; shared macOS credentials provide no independent GitHub identity boundary, and the next records PR supplies detection rather than prevention"
premises: []
---

# AGMSG-TASK dotfiles-T133-hold-playbook-a02 — plan 024 P1-13 class-level reset

Worker: `claude-standard-dot-a011`, Claude Code, `.claude/worktrees/worker-d`. Continue `tools/hold-playbook-a01` and PR #426 from `c206774cd6f0858890426379cab9aff98e3fd91c`. Keep the a01 implementation, tests, commits and historical evidence. This reset uses one PR.

The predecessor reached the C-61 round cap with its worker-side fix round and revise 2. Its update-branches do not erase those counts. The final-head security review found `interpreter-selection`, `write-containment` and `glob-traversal`; the task-level audit also reproduced `glob-equivalence-conservative`, already reported by Codex Bot thread `4310263840`. This text replaces the deficient execution, write and scope contracts at the class level rather than authorizing another a01 fix round.

Read the a01 task, its acceptance record and these final-head reviews:

- `.orchestration/validation/dotfiles-T133-hold-playbook-a01-security-c206774.md.last.md`
- `.orchestration/validation/dotfiles-T133-hold-playbook-a01-audit-c206774.md.last.md`

The Bot row `4310263840` and audit row `audit:c206774:3` are implemented by item 3 of this reset. Their historical ownership entries remain in the a01 record; the orchestrator records their transfer and eventual disposition. Other advisory work remains with `dotfiles-T133-hold-playbook-followup-a01`.

## Dispatch prerequisites — orchestrator

Both `after:` tasks must be accepted before dispatch. Verify the deployed Claude worker write boundary, the resolver on main, its exact trusted Python declaration and installed interpreter, the protected uv executable and anchored private cache. Offline PyYAML availability is a deployment prerequisite; the worker neither changes the resolver nor installs a fallback interpreter or dependency.

Every production caller must already supply the trusted-parent clean prefix specified in item 1. Caller changes outside `allowed_files` require a separate authorized task before dispatch. The fixture runner in this task is updated within `tests/unit/test_hold_playbook.py`.

The authoring checkout's checker implements C1–C10 and C7b, and its working tree lacks `tests/unit/test_task_consistency_c11_c15.py`. The checker and that test file were also read from local PR #417 objects: that revision has C11–C15, but its C11 accepts only a single identifier after the path and it has no C18. Before dispatch, the orchestrator obtains and reads the required revision supporting `tests/<path>::<Class>::<test>` and C18, reads its accompanying tests, and runs the checks below. Neither inspected revision is sufficient evidence for all required checks. Checker repair is outside this task.

## Applicable design

`$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` section 5.14 applies by reference, including items 1–10 and the same-UID threat model. The design remains an uncommitted orchestrator record in the inspected checkout; its by-reference application follows C-88 until the boundary records PR lands it. This task does not claim that it is already on main.

The following relied-on sentences are quoted verbatim under C-88.

Item 2:

> A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`).

> Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message.

> A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19).

> No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.

> Python は `-I`。

> PATH 探索で実行するものは無い。

Item 3:

> 仕組みが信頼するパス（スクリプト、台帳、証跡、worktree、lock、出力先）は realpath で解決し、`.claude/worktrees/` または manifest の worker ルート配下なら拒否（ask/hold）。

> symlink 構成要素は解決後に比較し、大小文字を区別しないファイルシステムでは同一性比較を大小文字非依存で行う。

Item 5:

> 名前には 40 桁の head を使う（7 桁で衝突させない）。

> lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。

> 物理スロット 1 つに lock 1 つ。

Item 9:

> orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。

> `UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。

> One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19).

## Item 1 — trusted execution and one interpreter resolver

`hold-playbook.sh` is a program with `#!/bin/bash -p`. Its trusted parent supplies, before exec:

```text
/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …
```

There is no self re-exec. Before record access, tool setup or effects, the program verifies and refuses invalid entry state with exit 2 and a named `hold-playbook:` diagnostic.

The actual environment contains exactly the documented allowed names: the prefix's `PATH`, `HOME` and `LANG`, plus only Bash-maintained entries needed by that invocation, explicitly enumerated and checked. No inherited `GIT_*`, `UV_*`, `PYTHON*`, `VIRTUAL_ENV`, loader variables, exported functions, shell startup variables or sanitization sentinel is accepted. Verify the fixed PATH and LANG values through absolute tools; do not use caller PATH to perform the verification.

Resolve `$0` and require its canonical absolute pathname to name a regular script under the bound repository root, outside worker roots. Refuse a symlinked script pathname. Determine the real uid's passwd home through the platform's absolute system tools and require HOME to equal it. Derive the repository from the validated script location rather than caller cwd or caller Git environment. Do not add Git discovery where the existing script needs none.

Consume `scripts/orchestrator/trusted-interpreter.sh` from that bound repository through the same trusted-parent clean prefix. It is a read-only dependency, not an editable file. Require its successful single absolute interpreter result; a missing or refusing resolver produces a named refusal before artifacts or ledger changes. There is no `command -v`, `mise which`, PATH lookup, activated-environment selection, download or interpreter fallback.

Bind uv to its verified protected absolute executable. Set `UV_CACHE_DIR` internally to the protected anchored checkout's `.agents/worklog/uv-cache`, never an inherited value. The Python child runs only in this form, with the resolver's result substituted for the interpreter:

```text
uv run --no-config --no-project --offline --python "$(trusted-interpreter.sh)" python -I …
```

Here both executable names denote their bound absolute paths; the notation does not authorize PATH discovery. Keep `yaml.safe_load`. Missing offline dependencies fail visibly without an online retry.

Add these tests to `HoldPlaybookTests`:

- `test_program_entry_verifies_clean_environment`: the clean-prefix invocation succeeds; dirty environment names, forged HOME, a forged sentinel and a symlinked `$0` produce named exit-2 refusals without record changes. Cover startup variables and exported functions. Direct dirty-loader cases use non-loadable library paths; only trusted-parent pre-exec sanitization may claim protection against a loadable library.
- `test_child_uses_trusted_interpreter_despite_checkout_config_and_path`: plant `.python-version`, poisonous `uv.toml`, a marker-writing checkout interpreter and PATH shims. Assert the exact interpreter realpath, `--no-config --no-project --offline --python`, isolated Python, the private cache, no planted configuration consumption and no marker execution. A dirty direct invocation refuses; the trusted-parent invocation uses the selected interpreter and retains the expected successful behavior.
- `test_missing_or_refused_resolver_is_named`: missing, nonzero and malformed resolver results refuse before writes, with no fallback.

The interpreter-contract test must run even when the resolver has not yet reached the branch used for authoring its red test. In that case its temporary fixture supplies a minimal resolver double at the expected sibling path returning a fixed known interpreter, and uses fake-uv argument capture to assert the consumer's interpreter, flags and cache. Wire doubles only into the copied fixture's fixed executable locations, never through a production test flag or relaxed environment rule. Label this as consumer-contract evidence. It does not validate the real resolver or uv internals.

At implementation dispatch, `after:` guarantees the real resolver exists on main. Copy and exercise that resolver for the final integration case after the orchestrator updates the branch with the dependencies. Do not skip the interpreter test because the resolver was absent during red-test preparation.

## Item 2 — contained writes through the Python child

The decisions ledger and every helper-produced artifact are opened through the Python child with `O_NOFOLLOW`. Their resolved destinations stay inside the bound repository root, and every parent component below that root is a real directory, never a symlink.

Use descriptor-relative directory traversal and final opens, with no-follow directory opens and type checks, so validation is not followed by reopening an unchecked pathname. Existing files must be regular files. Missing output entries may be created only through a validated parent chain. Account for filesystem case behavior when comparing identities and containment.

Validate all intended write destinations before creating the replan or appending a decision. Read the ledger header and tail through its validated descriptor. Append with `O_APPEND | O_NOFOLLOW`; preserve the existing header, rows and six-column serialization. Replan creation retains `O_CREAT | O_EXCL` and adds no-follow protection. Cleanup after an append failure operates through the held validated parent and removes only this invocation's newly created replan.

A symlinked ledger, a symlinked parent or an outside destination produces a named exit-2 refusal and leaves the source task, ledger, replan destinations and redirected targets unchanged. An already existing replan entry retains the specified exit 4 and never appends another decision.

Add one test for each class:

- `test_symlinked_ledger_is_refused`
- `test_symlinked_parent_is_refused`
- `test_output_outside_repository_is_refused`

The parent test covers the ledger parent and replan parent, including symlinks resolving inside and outside the repository. The outside-path test exercises the child's actual opening helper through an in-memory helper harness; it does not add a caller-selected output option or duplicate the validation algorithm in a test. Keep the existing repeated-invocation and dangling-replan-link regressions.

The ledger append is a production write under the operator's authority. These tests establish its containment; they do not describe the program as read-only or as writing only temporary files.

## Item 3 — validated scope algebra and wildcard equivalence

Before any comparison, both `covers()` and the glob validator reject:

- absolute paths, with `hold-playbook: absolute glob path`;
- `..` components, with `hold-playbook: parent component in glob`;
- empty components, with `hold-playbook: empty component in glob`.

Each refusal exits 2 before creating a replan or appending a decision. Apply validation to every `allowed_files` entry and every blast-radius glob, including unused entries. Keep the existing rejection of empty strings and record-breaking control characters. Do not apply the path-component validator to remedy prose.

Canonicalise equivalent ordinary wildcard runs before token absorption: `*?` and `?*` denote the same language, and repeated ordinary `*` tokens do not change it. Preserve slash boundaries and the distinct recursive meaning of trailing `/**`; canonicalisation must not turn that recursive token into an ordinary segment star. Retain whole-scope comparison for paths that do not yet exist.

Add:

- `test_absolute_glob_is_refused`
- `test_parent_component_glob_is_refused`
- `test_empty_component_glob_is_refused`
- `test_equivalent_wildcard_runs_are_covered`

Each refusal test covers invalid entries in both input lists and direct invocation of `covers()`, asserting the named refusal and unchanged records. Include `scripts/../../outside/**` under allowed `scripts/**`.

The equivalence test reproduces Bot thread `4310263840` and `audit:c206774:3`: allowed `dir/*?`, radius `dir/?*`. It is red against `c206774c`, where the invocation exits 3 and appends an unnecessary pending decision; after the fix it exits 0, reports coverage and leaves the ledger unchanged. Include reversed wildcard order and repeated ordinary stars, with retained tests proving that broader scopes and recursive directory globs are not incorrectly classified as covered.

## Item 4 — retained P1-13 behavior and vocabulary ownership

Retain the a01 behavior except where items 1–3 replace its mechanism.

`.orchestration/learning/classes.yaml` remains the orchestrator's tracked record, outside `allowed_files`. It maps each recorded class slug to `remedy:` and a `blast_radius:` list. A known class without a procedure has `remedy: unknown` and `blast_radius: []`. The worker does not seed, reconcile or edit this mapping, mistake records, correction records, inventories or acceptance records.

Preserve the named refusal when the vocabulary is absent, including “the orchestrator's record of plan 024 P1-13”, exit 2 and no traceback. Preserve fixture-only `--check-vocabulary <classes.yaml> <mistakes-dir>`: exit 2 lists every missing recorded slug, and exit 0 reports complete membership. No unit test reads the real learning tree. The orchestrator runs the vocabulary check against the real records at acceptance and pastes its output.

The normal command accepts exactly `<task> <class>`. Task ids match `^[A-Za-z0-9][A-Za-z0-9._-]*$`; invalid ids and unknown classes exit 2 before writes and name the refused input. Read only the source task's bounded first YAML front matter with `yaml.safe_load`. Record text remains data and is never executed.

Create `.orchestration/tasks/<task>-replan.md` containing the cause class, remedy, every blast-radius glob and the allowed entries covering it; mark uncovered globs outside `allowed_files`. Preserve the Completion placeholders and this exact line:

```text
re-plan: specification — <fill>; design — <fill>; implementation — <fill>; verification — <fill>
```

The skeleton remains a proposal until filled by the orchestrator. The source task and acceptance record remain unchanged, and the helper never dispatches or releases a hold.

All globs covered produces exit 0, establishing scope coverage only. A known unknown-remedy class is reported explicitly with its empty blast radius. An uncovered glob produces the replan, appends exactly one six-column row and exits 3:

- `id`: `D-<task>-replan`
- `when`: current UTC timestamp
- `what`: uncovered globs
- `why`: cause class
- `basis`: `hold-playbook`
- `result`: `pending`

No default or deadline consumes a default. Existing destination entries retain exit 4 and unchanged contents.

Keep all existing tests, including the three-class fixtures `colored-json-parse`, `concurrent-ff-clobber` and `records-form`, unknown remedy, vocabulary membership, whole-glob scope, literal data, preservation and repeated invocation. Adapt their runner to the clean execution contract without weakening their assertions. Shell comments remain English and shdoc-compatible.

## Item 5 — branch artifacts and scope

In the first a02 worker push, delete `.orchestration/dotfiles-T133-hold-playbook-a01/task.md` and add `.orchestration/dotfiles-T133-hold-playbook-a02/task.md` byte-identically to the dispatched a02 text. That single predecessor-file deletion is the C3 reset transition. Do not move, rewrite or delete other a01 evidence.

Write current `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence under `.orchestration/dotfiles-T133-hold-playbook-a02/`. Worker review filenames carry `-worker-`. Map each owned finding and requirement to its test selector and red/green commits.

`dispatch.sh`, `verdict.sh`, counters, hold detection, hold release, P0 enforcement, resolver implementation, workflow changes and permission changes remain outside this task. The existing P0 rule remains immediate revert PR for a defect on main and hold for an unmerged artifact. No additional script, dependency, production option or output path is introduced.

## Measurement and caps

The read-only measurement `git diff --numstat 69dccca9 c206774c` succeeded. Its code and test entries are:

```text
233	0	scripts/orchestrator/hold-playbook.sh
254	0	tests/unit/test_hold_playbook.py
```

Source estimate: retained `233 + 0 = 233`, plus `80` changed lines for item 1, `80` for item 2 and `30` for item 3 gives `233 + 80 + 80 + 30 = 423`; adding `27` lines of allowance gives a source cap of `450`.

Test estimate: retained `254 + 0 = 254`, plus `150` changed lines for item 1 and fixture migration, `90` for item 2 and `80` for item 3 gives `254 + 150 + 90 + 80 = 574`; adding `26` lines of allowance gives a test cap of `600`.

The estimates concern the resulting PR delta, count additions plus deletions and include fixture changes. These replace a01's 350/400 caps; evidence directories remain excluded from the source count.

## Check

`make format`, `shellcheck scripts/orchestrator/hold-playbook.sh`, repository-style `shfmt -i 4 -sr -d scripts/orchestrator/hold-playbook.sh` and `uv run --no-project --with pyyaml python -m unittest tests.unit.test_hold_playbook -v` have their exact commands, verbatim output, exit statuses and tested heads pasted in `.orchestration/dotfiles-T133-hold-playbook-a02/validation.md`. The shfmt flags retain the interpretation already recorded in the a01 acceptance record.

The script passes ShellCheck and shfmt, and the unit module is green. Retain the three-class expansion, decision, refusal, literal-data, unknown-remedy, vocabulary and whole-glob checks. Add every item 1–3 test, with red-before-fix and green-final-head evidence. Every behavioral script invocation uses a fixture repository, except the orchestrator's acceptance-time vocabulary check. No local Bats tests run.

An inherited formatting failure is reproduced on the unchanged base and recorded with its output. It remains a reported failure and receives no repair outside `allowed_files`.

With `git diff --numstat origin/main...HEAD`, at most **450 changed lines outside `tests/` and `.orchestration/`** are permitted.

With the same diff, at most **600 changed lines under `tests/`** are permitted.

Validation includes both totals and the complete changed-file inventory.

The **orchestrator**, before dispatch and at acceptance, runs the required format-2 task-consistency checker on `.orchestration/tasks/dotfiles-T133-hold-playbook-a02.md`, including C1–C10, C7b, C11 and C18, and reads and runs `tests/unit/test_task_consistency_c11_c15.py` from that revision. C7b is checked at one allowed-file entry per row; every closed row has exactly one existing or explicitly added `tests/<path>::<Class>::<test>` selector. C18 checks section 5.14's by-reference application and corresponding threat rows. An older checker result is not substituted.

The **orchestrator** performs the C-80 pre-dispatch security review of this exact text after prerequisites are satisfied. A surviving P0/P1 holds dispatch.

The **orchestrator** compares the branch's complete a02 task copy byte-for-byte with the dispatched a02 file, verifies its SHA-256 against the TASK line, and checks deletion of the a01 task copy in the first a02 push. A reported hash alone is not that comparison.

## Completion

One existing PR, #426, continues on `tools/hold-playbook-a01` from `c206774c`; the a01 fresh-branch requirement is superseded. Keep the predecessor implementation, tests and historical evidence, with only the mechanisms expressly replaced above and the C3 task-copy transition changed.

The inherited completion requirements are embedded here rather than imported from another task. The PR is ready for the orchestrator's integration when the ruleset's required checks are green, the bounded automatic Bot-review window has completed, every Bot thread is replied to and resolved by the orchestrator with its disposition, the validation file carries the Check's outputs, and the RESULT names every P0/P1 thread with `fixed:<sha>` or the surviving-finding rule below and every P2 thread with the disposition the worker proposes.

The orchestrator writes the advisory owner task before recording its first ownership disposition. A small in-scope P2 follows the inherited `check=` revise procedure while INV-6 permits it. A later review's P2 and every P3 are advisory, as is any other P2 outside that narrow fix procedure, owned by `dotfiles-T133-hold-playbook-followup-a01` and recorded under its ownership section in this task's acceptance record. The Bot and audit equivalence rows expressly transferred into item 3 are fixed here.

The worker's own pre-push review is one round at most. Every worker-side fix round counts toward INV-6. A surviving P0/P1 is sent in the RESULT as `open:<finding-or-thread-id>` and stops integration for the operator's decision. The third finding of one class stops further rounds until the orchestrator's re-plan.

C-61 permits at most two fix rounds in this reset, including worker-side fixes before the first RESULT; amendments and questions retain their own counters. A rebase repair qualifies only under D-024-24 and cannot hide a security fix. Preserve the stopped a01 history and counts. A review-body P0/P1 surviving the permitted worker round is reported as `open:review-<id>` with the applicable round count; do not relabel it advisory or perform another unauthorized round.

The RESULT identifies the final head, base, branch, changed files, test selectors, caps, evidence paths, task-copy hash and every Bot finding's disposition. It carries the precheck evidence required by the applicable RESULT procedure.

Use `task_copy=<sha256 of .orchestration/dotfiles-T133-hold-playbook-a02/task.md>`. Record the predecessor head, PR #426, red/green commits, requirement-to-test mapping, actual cap totals, refused commands and cost information. Worker review evidence uses the required `-worker-` infix. Historical evidence does not approve the new head.

Wait for final-head CI and the bounded automatic Bot-review window in parallel. An expired window is recorded as `bot: none`. No `@codex review` comment is issued, at ten minutes or after a fix. The orchestrator replies to and resolves review threads.

The orchestrator runs the task-level audit on the final head and dispositions every finding before the gate. Final-head CI, the feedback sweep, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. A changed head receives fresh evidence.

This task is `security: true`; the orchestrator also runs the separate security-profile review of the final head. Integration is bound to the audited head with `gh pr merge --squash --match-head-commit <audited head>`. The worker neither merges nor removes workers.

No `@codex review` comment is issued. Every `gh` write and Git write runs as an individual command without shell chaining or a wrapper combining writes. A classifier denial produces a blocked PONG naming the command and refusal.

Every `gh` command and every `git` write, including push and authenticated fetch, runs **inside the sandbox**. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-hold-playbook-a02 status=blocked` naming the exact command, failure and crossed boundary. Preserve the evidence and wait; no outside-sandbox retry, permission escalation, excluded-command workaround or alternate tool bypass is authorized.

Implementation, runtime tests and CI have not been checked by this read-only task-authoring pass. Same-UID replacement, shared credentials and deployment provenance remain residual.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```