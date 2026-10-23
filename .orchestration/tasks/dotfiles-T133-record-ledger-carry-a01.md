---
format: 2
task_id: dotfiles-T133-record-ledger-carry-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/carry-lineage.py
  - scripts/orchestrator/ledger-check.py
  - tests/unit/test_ledger_check.py
  - tests/unit/test_carry_lineage.py
  - .orchestration/dotfiles-T133-record-ledger-carry-a01/**
after: [dotfiles-T133-trusted-exec-contract-tests-a02]
rendered_forms: []
out_of_scope:
  - {path: scripts/orchestrator/chain-integrate.sh, reason: "dotfiles-T128-chain-glue-integrate-a01 owns this entrypoint; this slice neither edits nor executes it and depends on none of its callees."}
  - {path: scripts/orchestrator/orch-audit.sh, reason: "Execution binding belongs to dotfiles-T133-audit-pool-a02, not verdict-audit-pool-a04."}
  - {path: scripts/orchestrator/local-review.sh, reason: "Base-ref binding belongs to dotfiles-T128-chain-review-scripts-followup-a07 item 4."}
  - {path: scripts/orchestrator/sandbox-scan.sh, reason: "Execution binding remains with the dotfiles-T128-chain-review-scripts-followup-a07 lineage."}
  - {path: scripts/orchestrator/local-advisory.sh, reason: "Execution binding remains with the dotfiles-T128-chain-review-scripts-followup-a07 lineage."}
  - {path: scripts/orchestrator/dispatch.sh, reason: "dotfiles-T133-loop-limits-a01 owns this file; send-time recording belongs to P1-6 slice 2 afterward."}
  - {path: scripts/orchestrator/acceptance-front-matter.py, reason: "dotfiles-T133-loop-limits-a01 owns this writer, then P1-6 slice 2; carry invokes no writer subprocess."}
  - {path: scripts/orchestrator/fill_sweep.py, reason: "The existing dotfiles-T128-orchestrator-tools-a06 helper and dotfiles-T133-verdict-audit-pool-a04 consumer binding remain out of scope; no dependency or invocation here."}
  - {path: scripts/pr-feedback.py, reason: "The existing dotfiles-T128-orchestrator-tools-a06 helper and dotfiles-T133-verdict-audit-pool-a04 consumer binding remain out of scope; no dependency or invocation here."}
  - {path: scripts/require-crit-review.py, reason: "dotfiles-T129-audit-inherit-replan-json-followup-a03 owns the gate lineage; this slice only imports read_acceptance_record and neither edits nor runs the gate."}
threat_table:
  - control: scripts/orchestrator/carry-lineage.py standalone carry
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_two_predecessors"
  - control: scripts/orchestrator/ledger-check.py shared reader and row union
    disposition: "closed: tests/unit/test_ledger_check.py::LedgerCheckTest::test_prose_and_json_use_gate_reader"
  - control: tests/unit/test_ledger_check.py
    disposition: "residual: synthetic records exercise the real imported reader; final-head review checks compatibility with existing finding identifiers."
  - control: tests/unit/test_carry_lineage.py
    disposition: "residual: temporary roots and a fixture SQLite store model deployment; live delivery and host sandbox enforcement are not proved by fixtures."
  - control: .orchestration/dotfiles-T133-record-ledger-carry-a01/**
    disposition: "residual: evidence is procedural, not authenticated approval; the orchestrator compares the task-copy hash and final-head outputs."
  - control: messages.db read-only read with sender and content binding
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_dispatch_content_binding"
  - control: lineage filesystem walk under the fixed acceptance root
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_fixed_root_lineage"
  - control: audit-file first-line full-head read and collision detection
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_audit_provenance_and_collision"
  - control: carry sidecar per-source provenance
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_sidecar_provenance"
  - control: environment refusal
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_environment_refusal"
  - control: hostile Git environment and repository-local core.worktree/include.path
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_hostile_git_inputs"
  - control: shim-on-PATH executable discovery
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_shim_on_path"
  - control: worker-root inputs and destinations
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_worker_root_refusal"
  - control: audit-file swap between validation and consumption
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_swapped_audit_file"
  - control: trusted-parent runner consumer contract
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_trusted_launch"
  - control: program realpath refusal
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_program_realpath_refusal"
  - control: HOME refusal against passwd home
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_home_refusal"
  - control: input containment and record/sidecar destination binding
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_path_boundaries"
  - control: workflow and interpreter or environment inputs (trusted parent, isolated interpreter and private cache)
    disposition: "residual: test_trusted_launch exercises the supplied contract; installing the protected parent/resolver and excluding unrestricted same-UID writers remain host prerequisites."
  - control: task metadata
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_malformed_metadata_refuses"
  - control: metadata separators
    disposition: "closed: tests/unit/test_ledger_check.py::LedgerCheckTest::test_malformed_or_classless_row_refuses"
  - control: in-process effects
    disposition: "residual: isolated tests import root-bound helpers; unrestricted same-UID replacement outside seat sandboxes remains a host limitation."
  - control: new or renamed scripts
    disposition: "residual: carry-lineage.py is the only new production script; the final diff and allowlist check reject additional entrypoints."
  - control: orchestrator effect record and sidecar publication
    disposition: "residual: test_publication_failure checks staged writes and retry; two-file publication is not a transaction and an orphan sidecar may survive a failed record replacement."
  - control: orchestrator effect running carry before each chain
    disposition: "residual: test_standalone_effects proves the program is standalone; the orchestrator must record each successful pre-chain invocation and rerun for a changed record head."
  - control: orchestrator effect merge
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_standalone_effects"
  - control: orchestrator effect update-branch
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_standalone_effects"
  - control: orchestrator effect forced worker removal
    disposition: "closed: tests/unit/test_carry_lineage.py::CarryLineageTest::test_standalone_effects"
premises:
  - claim: "Historical measurements, not a claim that repaired records still reproduce the refusals."
    command: rg -n '^\*\*What happened' .orchestration/learning/mistakes/M-20261019-06-record-automation-gaps-recur.md
    output: |-
      10:**What happened.** On 2026-10-19/20 the integration chain refused five PRs at its audit precheck for missing lineage ledger rows (#402, #411, #430, #375 twice, #433), each time because the orchestrator had carried the predecessor audits' `audit:<sha7>:<n>` rows into the JSON block but not as the prose rows `ledger-check.py` reads, or not at all; and three task-level audits of the assets lineage (725b25b:4, 4e743a1:1, 9bff92b:1) found the record's `dispatch` array empty although the TASK and ACCEPTANCE lines had `read_at` timestamps on the bus. Each time the orchestrator repaired the record by hand from the lineage records or messages.db and re-ran the chain (about 10 minutes per refusal).
  - claim: "The current reader recognizes only prose rows."
    command: rg -n '^    rows = dict' scripts/orchestrator/ledger-check.py
    output: |-
      19:    rows = dict(re.findall(r"^((?:\d{6,}|audit:[0-9a-f]{7}:\d+))\t(\S+)$", Path(record).read_text(), re.MULTILINE))
  - claim: "The current precheck supplies lineage audit summaries; it is measured, not invoked by this slice."
    command: rg -n '^lineage=|"\$\{check\}" "\.orchestration/acceptance' scripts/orchestrator/orch-audit.sh
    output: |-
      56:lineage=("${v}/${family}"-a0*-audit-*.md.last.md)
      57:uv run --no-project python -I "${check}" ".orchestration/acceptance/${task}.md" "${v}/${task}-pr-feedback.json" ${lineage[@]+"${lineage[@]}"} || refuse "the ledger is incomplete" 3
  - claim: "The six historical delivery markers exist; the historical sender is not a production constant."
    command: sqlite3 -readonly "$HOME/.agents/skills/agmsg/db/messages.db" 'SELECT id,from_agent,read_at FROM messages WHERE id IN (2442,2482,2509,2529,2551,2560) ORDER BY id;'
    output: |-
      2442|claude-deep-dot|2026-10-19T05:52:31Z
      2482|claude-deep-dot|2026-10-19T08:24:50Z
      2509|claude-deep-dot|2026-10-19T11:37:22Z
      2529|claude-deep-dot|2026-10-19T12:35:57Z
      2551|claude-deep-dot|2026-10-19T20:15:36Z
      2560|claude-deep-dot|2026-10-19T20:51:09Z
  - claim: "The interim workaround fills dispatch from SQLite; it is not a parser or security pattern to copy."
    command: sed -n '1,4p' .agents/worklog/orchestrator-glue/fill-dispatch.py
    output: |-
      """fill-dispatch.py <task>: append to the acceptance record's JSON `dispatch` list every AGMSG-TASK and
      AGMSG-ACCEPTANCE line the orchestrator sent for the task (read from the agmsg messages.db, in id order), skipping
      lines already present; prints each added message id with its read_at. Interim mechanism for the
      dispatch-record-markers class until P1-6 lands it in dispatch.sh (M-20261019-06)."""
  - claim: "The gate supplies the JSON reader and fixed keys; three rows trigger S6 search and S1 replan checks."
    command: rg -n '^def read_acceptance_record|^RECORD_KEYS|^S6_CLASS_LIMIT|without a matching records search|without a re-plan' scripts/require-crit-review.py
    output: |-
      42:RECORD_KEYS = {"format", "task", "head", "pr", "ledger", "searches", "audit_findings", "dispatch", "replans"}
      48:S6_CLASS_LIMIT = 3
      749:def read_acceptance_record(path: Path) -> tuple[dict | None, str | None]:
      951:            errors.append(f"S6: class {cls} at {count} without a matching records search")
      953:            errors.append(f"S1: {cls} at {count} rows without a re-plan (C-59)")
  - claim: "Predecessor links live in task front matter, not new acceptance-block keys."
    command: rg -n --sort path '^reset_of:|^after:' .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a0[345].md
    output: |-
      .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a03.md:13:after: [dotfiles-T129-assets-omp-hcom-followup-a02]
      .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a04.md:12:after: [dotfiles-T129-assets-omp-hcom-followup-a03]
      .orchestration/tasks/dotfiles-T129-assets-omp-hcom-followup-a05.md:10:after: [dotfiles-T129-assets-omp-hcom-followup-a04]
  - claim: "This checkout has a 43-line reader; carry and both requested test modules are new."
    command: wc -l scripts/orchestrator/ledger-check.py | xargs
    output: |-
      43 scripts/orchestrator/ledger-check.py
  - claim: "The standalone program, common resolver and new test modules are absent; only this program's launch contract is a prerequisite."
    command: for p in scripts/orchestrator/carry-lineage.py scripts/orchestrator/trusted-interpreter.sh tests/unit/test_ledger_check.py tests/unit/test_carry_lineage.py; do if test -f "$p"; then printf '%s present\n' "$p"; else printf '%s absent\n' "$p"; fi; done
    output: |-
      scripts/orchestrator/carry-lineage.py absent
      scripts/orchestrator/trusted-interpreter.sh absent
      tests/unit/test_ledger_check.py absent
      tests/unit/test_carry_lineage.py absent
---

# AGMSG-TASK dotfiles-T133-record-ledger-carry-a01

🤖 I read the AGENTS.md for mryfmo/dotfiles.

## Re-plan and boundary

This is amendment 1 after the whole S2 re-plan of plan 024 P1-6 slice 1 recorded in the acceptance record. It addresses only cf4f0ca's item-7 consumer-test gap; earlier reviews a26cc07 and 6cbe954 remain closed by the re-plan. The re-plan replaces the chain-based design. The repeated excluded-command-trusts-sandbox-context family is addressed by removing chain execution from this slice, not by asserting compliant callees.

Deliver standalone `carry-lineage.py`, the existing `ledger-check.py` reader change and their tests. The orchestrator runs carry before each chain; the program never starts the chain. No chain callee is a dispatch prerequisite. Retain the out-of-scope owners above; do not migrate callees, invoke the acceptance writer, alter the gate or add production files beyond the allowlist. The sibling loop-limits task remains disjoint.

Apply agmsg-orchestration Worker Playbook step 4: all worker commands, tests, pushes and gh calls stay inside the sandbox and allowlist. A denial yields `AGMSG-PONG v1 task_id=dotfiles-T133-record-ledger-carry-a01 status=blocked` naming the exact command, failure and boundary; wait for re-tasking. Never seek an unsandboxed retry, another-tool escape or approval to cross that boundary.

## Frozen execution contract

Design 5.14 at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen (D-024-29) and applied by reference (D-024-30).

This task relies on design 5.14 item 2 by reference.
This task relies on design 5.14 item 3 by reference.
This task relies on design 5.14 item 7 by reference.
This task relies on design 5.14 item 8 by reference.
This task relies on design 5.14 item 9 by reference.

Use `tests/unit/trusted_exec_contract.py` supplied by prerequisite `dotfiles-T133-trusted-exec-contract-tests-a01` for the shim-on-PATH, hostile-Git, worker-root and swapped-file probes, its sanitized-environment assertion and `run_under_trusted_parent`; import it only in tests and do not edit it in this slice.

Before dispatch, supply the accepted trusted parent and common resolver for these two Python entrypoints alone. The absolute shell script in item 2 is the accepted parent, not a Python file. Use that parent and `<abs uv> run --no-config --no-project --isolated --offline --python <abs python> python -I <abs program> …`; consume the verified interpreter realpaths without rediscovery. The parent supplies an absolute `UV_CACHE_DIR`, protected main-checkout cache for orchestrator runs and `<worktree>/.uv-cache` for worker tests. Supply already provisioned repository-standard safe-YAML support when reading task metadata; do not add a new dependency or replacement resolver here.

The new program checks its exact allowed environment-name set, fixed PATH/LANG, own regular-file realpath under the confirmed repository root, and HOME against `pwd.getpwuid(os.getuid()).pw_dir` before reading records or writing. Enumerate the allowed names in the accepted launch contract and its fixture; reject unknown names, missing required names and relative/missing cache paths. Any refusal exits 2 with `carry-lineage: environment refused`, `carry-lineage: program realpath refused` or `carry-lineage: HOME differs from passwd home` as applicable. Never repair the environment or re-exec itself; a sentinel proves nothing. No production HOME, database, executable-directory or root override is accepted.

## Implementation

1. **One acceptance reader.** Import the root-bound gate module's `read_acceptance_record` by explicit realpath; use it in the ledger reader and carry. No second acceptance JSON parser. Preserve `ledger-check.py <record> <sweep> <audits>…` and its Bot/audit finding conventions. Union prose `<id><TAB><class>` and JSON `ledger: [{id, class}]` rows, including JSON-only records. Equal duplicate ids/classes count once; different classes refuse as `ledger-check: conflicting classes: <id>`. A missing/blank class refuses by name; malformed blocks and duplicate JSON keys retain the shared reader's refusals. Keep prose-only support; a present malformed block must not fall back to prose.
2. **Standalone interface.** `carry-lineage.py <task> --orchestrator <identity>` takes the identity from the trusted orchestrator invocation, not record content or a historical sender constant. Validate the task as a single safe identifier, refusing `..` components and path separators; require the current block's task to match and its head to be full lowercase 40-hex. Carry may import the allowed ledger helper; it runs no chain script, writer, audit, gate, send, merge, update-branch or worker-removal command.
3. **Filesystem lineage.** Walk every regular file under the fixed `.orchestration/acceptance/` root, including ignored/untracked files; confirm the anchored repository root once with git using explicit `--git-dir=<root>/.git --work-tree=<root>` and sanitized read-only root probing, then never consult git or any `GIT_*` variable again. The trusted parent supplies exactly the allowed environment names, so no `GIT_*` name is present; refuse such names before probing rather than repairing them. Git grants no inclusion/exclusion or head authority. Derive the lineage prefix by removing terminal `-a<digits>`; match an escaped anchored prefix. Read `reset_of`/`after` as safe task-front-matter data under `.orchestration/tasks/`, never new acceptance keys. Select only same-prefix records reachable transitively as predecessors of the current task. Exclude unlinked same-prefix records even when their PR matches; refuse cycles, malformed identities, unreadable required links and missing predecessor records.
4. **Path boundary.** Realpath-bind all inputs, imported helpers and fixed roots; refuse escapes, worker-root paths and case aliases on case-insensitive filesystems. Nothing under `.claude/worktrees/` or a manifest worker root is read or written. Record destination is `.orchestration/acceptance/<task>.md`; sidecar is `.orchestration/validation/<task>-carry.json`. Bind existing destinations, new-file parents and staging paths beneath those fixed roots; refuse lexical `..` before normalization. Use directory-relative no-follow opens, including O_NOFOLLOW semantics for destination/staging leaves; recheck parent identity before replacement.
5. **Carry rows and provenance.** For every predecessor audit row, keep its recorded class in both current-record prose and JSON ledger. Missing/blank class refuses as `carry-lineage: lineage row has no class: <record>:<id>`; conflicting classes refuse by name. Locate the corresponding audit file beneath the fixed validation root, snapshot its bytes and read a unique full lowercase 40-hex head from its first line. Require its prefix to match the row id; a filename sha7, inherited-only marker or current record's head cannot substitute. Missing/ambiguous origin or full head refuses before mutation. Do not silently drop a row.
6. **Collision handling.** Before deduplication, bind each `audit:<sha7>:<n>` to its origin audit path, byte SHA-256 and full head. Distinct audits sharing sha7 and finding number refuse as `carry-lineage: audit id collision: <id>` even with equal classes. Repeated references to the same bound origin remain idempotent; retain every predecessor/source association in sidecar `carried: [{id, class, record_path, audit_path, audit_sha256, head}]`. Never infer provenance from the shared Git object store.
7. **Dispatch content binding.** Open passwd-home `~/.agents/skills/agmsg/db/messages.db` with SQLite URI `mode=ro` and query-only mode; use a fixed parameterized query in message-id order. Parse TASK/ACCEPTANCE lines as data, with exact task-id matching and unique fields regardless of order. Count only `from_agent == <identity>`. A TASK line also needs `task_sha256` equal to SHA-256 of the bound dispatched `.orchestration/tasks/<task>.md` bytes. An ACCEPTANCE line also needs its full `head` to equal the current record's head or a predecessor record head in sidecar `predecessors: [{task, record_path, head}]`; validate these full heads from the selected predecessor records independently of audit-origin heads. Report every other candidate line with message id and reason, without echoing untrusted bodies; store none of those lines. The store is writable by every seat, so sender names and `read_at` alone are not authentication or permission authority.
8. **Publish.** Preserve all other JSON keys, prose, searches, replans and dispositions. Fill `dispatch` with validated exact lines, deduplicated in database order; validate existing dispatch entries too and report/remove unbound entries. Sidecar records task, current full head, trusted orchestrator identity, task-text SHA-256, the selected predecessor records and their full heads, every carried-row provenance and `dispatch_meta: [{message_id, read_at, line}]` for accepted messages, retaining duplicate-message provenance and SQL NULL as JSON null. No new acceptance-block keys. Missing/unreadable database or no content-bound TASK refuses by name. Validate all inputs before writing, recheck consumed hashes, stage 0600 outputs, publish sidecar before atomically replacing the record; reruns repair an orphan sidecar without duplicating rows. Leave predecessors, task/audit inputs and database bytes unchanged.
9. **Preserve counters.** Carry every row without synthesizing a class, records search, replan or approval. The unchanged gate must still reject three matching-class rows without the required S6 search/S1 replan; preserve an existing valid replan. Local records/sidecar are procedural bookkeeping, not permission decisions or authenticated PR content. Final PR review uses full-head GitHub content or a protected private clone as item 8 requires; carry does not fetch or evaluate a PR changeset.

Runtime record/sidecar destinations are orchestrator outputs, not worker edit permissions. The orchestrator records carry's exit and output before each chain and stops on refusal; this task does not modify that chain or claim its downstream execution is safe.

## Check

Authoring count: 227 lines including front matter and five allowed entries; limits are 250 lines and these five entries. Measured existing production baseline is the 43-line reader; carry and both test modules are absent. There is no inherited a01 line-budget arithmetic for this new slice.

Fresh estimates, to be measured: at most **400 additions plus deletions outside tests/ and .orchestration/** and **700 additions plus deletions under tests/**. These estimates cover both production programs, the reader import/union and all cases below; they are not measured implementation totals. RESULT records final per-file numstat and both totals without raising either cap; exceeding one requires re-tasking. Use `git diff --no-ext-diff --no-textconv --numstat <base40>...<head40>` on the final head; the orchestrator independently measures authenticated contents in a protected review clone.

Write the tests first and paste red/green commands, outputs and exit codes. Use the supplied isolated launch contract inside the sandbox, a temporary HOME, fixture passwd-home lookup, temporary cache and fixture messages.db. Mock passwd/root inputs only in tests, never through production switches; a real temporary HOME differing from passwd home must refuse. Fixture protected roots model production boundaries without granting the worker access to the live anchored checkout. No live store reads, record mutations or bus sends in tests.

- `tests/unit/test_ledger_check.py::LedgerCheckTest::test_prose_and_json_use_gate_reader`: prose-only, JSON-only and mixed rows; assert use of the actual shared reader; equal duplicates once, conflicting classes refused.
- `tests/unit/test_ledger_check.py::LedgerCheckTest::test_malformed_or_classless_row_refuses`: malformed delimiters/JSON, duplicate keys, invalid ledger shape and class-less prose/JSON rows refuse by name.
- `tests/unit/test_ledger_check.py::LedgerCheckTest::test_audit_regex_and_inherited_ids`: retain Bot ids, direct/inherited audit ids, misleading filenames and repeated inherited references.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_two_predecessors`: two predecessor records and audit files, one JSON-only row; both output representations retain every class, and rerun is idempotent.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_missing_class_refuses`: class-less predecessor rows in either representation refuse before publication and leave inputs/outputs unchanged.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_fixed_root_lineage`: ignored/untracked records count, transitive reset_of/after links work, unlinked same-prefix records are excluded; git listing cannot hide an input.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_audit_provenance_and_collision`: different full heads sharing sha7 and finding number refuse before deduplication; missing/ambiguous first-line heads and prefix mismatches refuse.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_sidecar_provenance`: every carried row/source has record path, audit path, matching byte SHA-256 and full first-line head; repeated references to one origin retain their provenance.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_dispatch_content_binding`: fixture TASK with matching sha stored, mismatching sha reported; foreign-head ACCEPTANCE reported; current/predecessor record heads accepted, including a predecessor with no audit rows; wrong sender/task, duplicate fields, reordered fields, duplicate lines and NULL read_at; DB unchanged.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_path_boundaries`: input symlink escape, case-alias path, worker-worktree path and lexical `..` destination each refused; exercise both record and sidecar existing leaves, new parents, staging and symlink swaps. Test case-insensitive semantics deterministically without skipping on a case-sensitive host.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_environment_refusal`: use the shared sanitized-environment assertion for extra/missing names, hostile PATH/LANG, loader/startup variables and absent/relative cache; exit 2 with the named message and no effects.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_hostile_git_inputs`: use the shared hostile-Git probe, separately exporting `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`, `GIT_CEILING_DIRECTORIES` and `GIT_ALTERNATE_OBJECT_DIRECTORIES` to attacker paths and planting fixture-repository `.git/config` `core.worktree`/`include.path`. Direct consumer injection of those names refuses before root probing or I/O; through `run_under_trusted_parent` they are absent. Exercise local configuration independently under the accepted environment so environment refusal cannot mask it. Against a clean baseline, in both successful parent runs assert the confirmed root is the fixture's given fixed root, the lineage walk reads exactly the same legitimate records, and ledger/sidecar writes land under the fixed acceptance/validation roots; compare root, record and sidecar realpaths before/after, with distinguishable attacker records and unchanged attacker paths.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_shim_on_path`: offer the shared `uv`, `python3`, `gh`, `git` and `bash` shims at PATH front to the trusted-parent runner; carry succeeds through the accepted parent, and the shared argv-marker assertion proves no shim ran.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_worker_root_refusal`: use the shared worker-root probe for existing record/audit inputs and existing/new record/sidecar destinations, also covering manifest worker roots; refuse before reads or writes there and leave fixtures unchanged.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_swapped_audit_file`: use the shared deterministic callback/barrier to replace a checked audit with an attacker symlink before consumption; the replacement is never read, attacker content is never consumed, and refusal leaves outputs unchanged. Report unsupported native case-alias subcases as unproved; the deterministic case-insensitive coverage in `test_path_boundaries` remains required.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_program_realpath_refusal`: outside-root, symlink-escaped, nonregular and worker-root program paths refuse before input reads.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_home_refusal`: forged HOME refuses; fixture passwd home succeeds without a production override.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_trusted_launch`: use shared `run_under_trusted_parent` and real supplied parent/interpreter argv, hostile BASH_ENV, fake user-site .pth/usercustomize.py, uv.toml and .venv; planted code never runs; no self re-exec or interpreter rediscovery.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_malformed_metadata_refuses`: malformed acceptance block, duplicate keys, unsafe YAML, cycles and invalid/missing predecessor links; names the failure before writes.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_publication_failure`: changed snapshots, unavailable database and failed replacement preserve the old record; orphan-sidecar retry succeeds.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_standalone_effects`: successful carry with chain/callees absent; subprocess log has no chain, writer, audit, send, merge, update-branch or worker-removal execution.
- `tests/unit/test_carry_lineage.py::CarryLineageTest::test_gate_thresholds_preserved`: unchanged gate still requires matching S6 searches and S1 replan at three rows; existing complete replan survives.

Run both new unittest modules, relevant existing reader/gate checks and repository-required checks. Do not run Bats locally; push and inspect GitHub Actions for those results. Do not count an unrun or sandbox-denied check as passing.

## Completion

Use agmsg-orchestration Codex seat worklogs (plan/todo/learn), uncommitted, with at most one active todo per owner. Create a fresh task branch and one PR with English title/description. Commit the byte-identical dispatched text under the allowed task directory as `task.md`.

In that directory write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence. RESULT names all paths, final full head/base, PR, task-copy SHA-256, changed files, final numstat/caps, threat-row checks, red/green evidence, CLI impact, residuals and `cost:` (`n/a` if unavailable). Worker artifacts stay at those relative paths in its own worktree when the main checkout is not writable.

Verify CI after the final push and follow bounded fix/review rounds. Send `AGMSG-RESULT v1 task_id=dotfiles-T133-record-ledger-carry-a01 status=ready_for_review` with evidence, or `status=blocked` with exact command/failure/boundary evidence. The orchestrator performs independent final-head/security review and Orchestrator Playbook step 10's feedback sweep, audit, acceptance and integration gate with the required evidence. Use repo-local crit-data; no browser review or worker merge.

Not checked by this authoring task: implementation, runtime tests, CI or live mutation. Risk: local records and the all-seat store remain untrusted procedural inputs; legacy audits lacking first-line full heads refuse, and protected launch deployment remains a prerequisite.

## Checks (pasted by the orchestrator before each send)

```
```