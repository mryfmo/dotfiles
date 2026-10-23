---
format: 2
task_id: dotfiles-T133-record-json-sync-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/record-json-sync.py
  - tests/unit/test_record_json_sync.py
  - .orchestration/dotfiles-T133-record-json-sync-a01/**
after: []
threat_table:
  - {control: "scripts/orchestrator/record-json-sync.py", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_syncs_rows_and_replans"}
  - {control: "tests/unit/test_record_json_sync.py", disposition: "residual: Assertion errors can conceal broken behavior; the final-head audit checks fixtures, observations and red/green evidence against the implementation."}
  - {control: ".orchestration/dotfiles-T133-record-json-sync-a01/**", disposition: "residual: Only task records are permitted under this wildcard; no executable helper or replacement implementation may be hidden in evidence."}
  - {control: "the task copy .orchestration/dotfiles-T133-record-json-sync-a01/task.md", disposition: "residual: The orchestrator compares the whole file byte-for-byte with dispatch and checks its SHA-256 before acceptance."}
  - {control: "the evidence records under .orchestration/dotfiles-T133-record-json-sync-a01/", disposition: "residual: Preserve commands, exit statuses and complete outputs; the audit compares their claims with the final diff and GitHub Actions."}
  - {control: "task metadata: kind, security, allowed_files, after, threat_table and premises", disposition: "residual: Task-consistency checks and independent task-file review run before dispatch and acceptance; task-copy equality exposes altered metadata."}
  - {control: "metadata separators", disposition: "residual: Whole-file comparison covers task-copy separators; evidence is untrusted data, and acceptance-record delimiter failures are exercised by the malformed-front-matter test."}
  - {control: "malformed acceptance-record front matter", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_malformed_front_matter_is_unchanged"}
  - {control: "acceptance-record write target", disposition: "closed: tests/unit/test_record_json_sync.py::RecordJsonSyncTest::test_task_and_output_path_are_confined"}
  - {control: "in-process effects", disposition: "residual: Only the named acceptance file is rewritten after validation; tests use temporary records, and same-UID concurrent replacement remains possible."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: Commands bind the clean parent, fixed interpreter and executable paths; no workflow or interpreter configuration changes are authorized."}
  - {control: "new or renamed scripts", disposition: "residual: Only scripts/orchestrator/record-json-sync.py is introduced; it parses data with the standard library and never evaluates prose or starts subprocesses."}
  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: Same-UID replacement and shared credentials remain possible; local JSON synchronization is process evidence, never authentication or permission approval."}
  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: Every worker action stays inside its sandbox and declared files; this task changes no deployed sandbox, permissions or trusted host inputs."}
  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Commands establish the clean parent before binding tools; the transformer launches no executable and cannot sanitize the parent that started its interpreter."}
  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: Task-id and symlink escape tests constrain the write target; they do not establish protection against unrestricted same-UID replacement."}
  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Commands reuse the probed PY binding; parse and validate the record before writing, without claiming a snapshot or concurrent-writer exclusion."}
  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: RESULT and cap evidence name full base and head SHAs; this transformer introduces no reservation, lock or head-named executable output."}
  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: The transformation tests establish record behavior only; host provenance, concurrent writes and shared credentials remain explicit residuals."}
  - {control: "design 5.14 item 7: 検証", disposition: "residual: Red/green tests cover the data transformation; they do not claim the four host-execution probes, since no execution mechanism is introduced."}
  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: This writes a local acceptance-record proposal without granting approval; committed permission decisions and final integration retain their existing authorities."}
  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: Runtime uses only the standard library under the fixed installed interpreter; worker lint caches remain seat-local and no orchestrator cache is changed."}
  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Every command including gh and push remains sandboxed; refusal produces a blocked PONG without escalation or a substitute tool."}
  - {control: "orchestrator effect merge", disposition: "residual: Only the orchestrator merges through gh pr merge --squash --match-head-commit <audited head> after Orchestrator Playbook step 10; the worker never merges or pushes main."}
  - {control: "orchestrator effect update-branch", disposition: "residual: The orchestrator refreshes CI, feedback and the task-level audit after an update-branch changes the head, before applying the integration gate."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: None is planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and any forced removal records the discarded state in acceptance."}
premises:
  - claim: "The existing glue has 28 lines; neither requested tracked path exists in the authoring checkout."
    command: |-
      "${P[@]}" "$PY" -I -c 'from pathlib import Path; p=Path(".agents/worklog/orchestrator-glue/record-json-sync.py"); print("glue_lines=" + str(len(p.read_text().splitlines()))); print("tracked_script_exists=" + str(Path("scripts/orchestrator/record-json-sync.py").exists())); print("test_module_exists=" + str(Path("tests/unit/test_record_json_sync.py").exists()))'
    output: |-
      glue_lines=28
      tracked_script_exists=False
      test_module_exists=False
  - claim: "The gate defines the ledger grammar, class grammar and four required re-plan keys; replan_complete requires non-empty text."
    command: |-
      rg -n '^LEDGER_ID =|^REPLAN_KEYS =|^CLASS_SLUG =|^def replan_complete|^    return isinstance\(entry, dict\)' scripts/require-crit-review.py
    output: |-
      37:LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")
      38:CLASS_SLUG = re.compile(r"[a-z0-9-]+")
      44:REPLAN_KEYS = ("specification", "design", "implementation", "verification")
      775:def replan_complete(entry: object) -> bool:
      776:    return isinstance(entry, dict) and all(is_text(entry.get(key)) for key in REPLAN_KEYS)
  - claim: "acceptance-front-matter.py lines 79-84 reject wrong containers, invalid class slugs, missing or extra keys and blank values before writing."
    command: |-
      sed -n '79,84p' scripts/orchestrator/acceptance-front-matter.py
    output: |-
          replans, parts = record.get("replans", {}), ", ".join(gate.REPLAN_KEYS)
          if not isinstance(replans, dict):
              parser.error(f"replans must be {{<class slug>: {{{parts}}}}}; nothing written")
          for cls, entry in replans.items():
              if not gate.CLASS_SLUG.fullmatch(cls) or not gate.replan_complete(entry) or set(entry) != set(gate.REPLAN_KEYS):
                  parser.error(f"replans.{cls} must be {{{parts}}}, each a non-empty string; nothing written")
---

# AGMSG-TASK dotfiles-T133-record-json-sync-a01 — promote acceptance-record JSON synchronization
Written 2026-10-20; amendment 1 addresses all five C-80 round-1 findings and C-104. PR #437's task-level audit e9819d4 found empty JSON ledger, replans and searches beside 18 prose rows and three re-plan lines (M-20261019-06). [memory:failure] Prose-only findings and re-plans do not populate the JSON the gate consumes.
Design 5.14 of `.orchestration/plans/024-design-quality.md` is frozen (D-024-29) and applies by reference (D-024-30); items 0–10 have individual threat rows.

## Commands
Definitions occur only here; premises quote source-authoring probes, not additional worker instructions. Start (parent) from the trusted launcher in the verified checkout root; run the lettered sections inside it. Stop dependent work at any failed prerequisite; substitute recorded operands before execution.
```bash
# (parent) Clear inherited inputs before starting the shell.
/usr/bin/env -i PATH=/usr/bin:/bin TMPDIR="${TMPDIR:-/tmp}" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 /bin/bash --noprofile --norc -p -o pipefail
# (a) Record the platform and anchor home to the real user's passwd entry.
platform=$(/usr/bin/uname -s); printf '%s\n' "$platform"
case "$platform" in
  Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
  Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
  *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
esac
rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
# (b) The clean child prefix.
P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8)
# (c) Bind and probe the exact interpreter, then use this test invocation for red and green.
PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
[ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python: refused: missing-executable' >&2; exit 1; }
"${P[@]}" "$PY" -I -c 'import os,sys; p=os.path.realpath(sys.executable); print(p, sys.version.split()[0]); assert sys.version.split()[0]=="3.15.0" and p.startswith(os.environ["HOME"]+"/.local/share/mise/installs/python/3.15.0/")' || exit 1
"${P[@]}" "$PY" -I tests/unit/test_record_json_sync.py
# (d) Resolve uv only when needed for lint; never execute a shim or provision a replacement interpreter.
UV=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/uv/latest/uv-aarch64-apple-darwin/uv")
case "$UV" in ""|*/mise/shims/*) exit 1;; "$home"/.local/share/mise/installs/uv/*/uv-aarch64-apple-darwin/uv) ;; *) exit 1;; esac
[ -f "$UV" ] && [ -x "$UV" ] || exit 1
"${P[@]}" UV_CACHE_DIR="$PWD/.uv-cache" "$UV" run --no-config --no-project --python "$PY" --with ruff ruff check scripts/orchestrator/record-json-sync.py tests/unit/test_record_json_sync.py
"${P[@]}" UV_CACHE_DIR="$PWD/.uv-cache" "$UV" run --no-config --no-project --python "$PY" --with ruff ruff format --check scripts/orchestrator/record-json-sync.py tests/unit/test_record_json_sync.py
# (e) Bind gh; every invocation gets a fresh config directory and an explicit host/repository.
GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
[ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
gh_call() {
  local GH_CONFIG_DIR; GH_CONFIG_DIR=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX") || return
  case "$1" in api) [[ "$2" == repos/mryfmo/dotfiles/* ]] || return 1; "${P[@]}" GH_CONFIG_DIR="$GH_CONFIG_DIR" "$GH" "$@" --hostname github.com;; pr|run|issue) "${P[@]}" GH_CONFIG_DIR="$GH_CONFIG_DIR" "$GH" "$@" --repo github.com/mryfmo/dotfiles;; *) return 1;; esac
}
# (f) All Git operations use the clean prefix and system Git; cap operands are full recorded SHAs.
branch=tools/record-json-sync-a01
git_clean() { "${P[@]}" /usr/bin/git "$@"; }
"${P[@]}" /usr/bin/git diff --numstat "$base40...$head40"
( GH_CONFIG_DIR=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX") || exit 1; P+=(GH_CONFIG_DIR="$GH_CONFIG_DIR"); "${P[@]}" /usr/bin/git -c credential.helper= -c "credential.helper=!$GH auth git-credential" push https://github.com/mryfmo/dotfiles.git "HEAD:$branch" )
```
Commands (a) is the only home source. Commands (parent)/(b) clear inherited `GIT_DIR`, `GIT_WORK_TREE`, `GIT_CONFIG_COUNT`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM` and other `GIT_*`, tool, loader and Python variables. Commands (e)/(f) also isolate the credential helper's configuration; authentication failure is a blocker, never permission to restore inherited configuration, rediscover tools or leave the sandbox.

## Item 1
The author read the 28-line `.agents/worklog/orchestrator-glue/record-json-sync.py`; promote its behavior below using only the standard library, without depending on that untracked file in the worker checkout. Read `scripts/orchestrator/orch-gate.sh`, `scripts/require-crit-review.py` and `scripts/orchestrator/acceptance-front-matter.py` and enumerate consumers before editing. Run from the checkout root with exactly one task-id argument; read `.orchestration/acceptance/<task>.md`. Reject task-id traversal and symlink escapes before writing.
Require an opening whole-line `---` JSON block and closing separator. Parse with `json.loads(..., object_pairs_hook=<a hook that raises on a duplicate key>)`; reject duplicate keys at any depth. Missing separators, invalid JSON, duplicate keys, non-object front matter or malformed ledger/replans containers exit 1 with stderr and leave the entire file byte-identical. Validate before opening for writing. Serialize UTF-8 with indent 2, sorted keys and ensure_ascii=False, preserving every unrelated key and every byte of prose after the closing separator.
The exact gate definition at `scripts/require-crit-review.py:37` is `LEDGER_ID = re.compile(r"\d{10,}|audit:[0-9a-f]{7}:\d+")`. Copy only complete prose lines `<id><TAB><class>` whose entire id matches that grammar and whose entire class matches `[a-z0-9-]+`: numeric review-thread ids of ten or more digits, or `audit:` plus exactly seven lowercase hex digits plus `:` plus digits. No ranges, longer audit SHAs, trailing text or near-matches enter JSON.
Initialize an absent ledger to []; validate existing rows against the gate's `{id, class}` contract, preserving valid existing entries, order and values. Append eligible prose rows in order only when their text-form id is absent; suppress repeated prose ids, including matches to existing numeric JSON ids.
C-104: all other rows (`text-security:`, `worker:`, `ci:`, `orchestrator-text:` and others) remain prose only, where the gate's S1 class table reads them. The glue's first version copied every row; the #441 chain's record step refused it with `ledger row 0 must be {id: <thread id or audit:<sha7>:<n>>, class: …}`.
Copy complete lines `re-plan: <class> (<rows>) — specification: …; design: …; implementation: …; verification: …` into `replans[<class>]`. Use exactly `"specification"`, `"design"`, `"implementation"`, `"verification"`, each a non-empty stripped string; no rows or extra key. Initialize absent replans to {}, preserve other classes, and let the last complete line for a class win. Missing/blank parts emit stderr naming the class and missing parts, contribute no entry and never overwrite an existing valid entry; other valid rows/lines still synchronize. Success, including skipped incomplete lines, exits 0; repeated runs are byte-identical.
The gate consumes the record's replans object. [memory:decision] Synchronize only ledger/replans; searches remains unchanged for acceptance-front-matter.py's existing recomputation. Do not change consumers, gates, original glue, live acceptance records, hooks, permissions, workflows, dependencies or graph data.

## Item 2
Write `tests/unit/test_record_json_sync.py` first with unittest and temporary checkout-shaped records, ending with `if __name__ == "__main__": unittest.main()`. Invoke the real script as `[sys.executable, "-I", <absolute script>, <task>]`; no source-string assertions or mocked transformation.
Use `RecordJsonSyncTest` methods `test_syncs_rows_and_replans`, `test_missing_part_warns_and_is_skipped`, `test_existing_ids_are_kept_and_second_run_is_identical`, `test_last_complete_replan_wins`, `test_malformed_front_matter_is_unchanged`, `test_task_and_output_path_are_confined`, `test_acceptance_front_matter_accepts_replans` and `test_prose_is_byte_identical`.
Fixtures cover a mixed prose table with audit, numeric-thread and excluded kinds, proving only audit/thread rows are copied; 7/40-hex and single/range forms; digit-bearing class slugs; malformed near-matches; existing JSON ids; unrelated JSON including searches; extra prose separators; Unicode; mixed LF/CRLF prose preserved byte-for-byte. Malformed-front-matter subcases include a duplicate `ledger` key and a nested duplicate key, each refused with exit 1 and the whole file unchanged. Missing-part subcases cover every required key and a valid entry followed by an incomplete line.
The compatibility test runs the actual acceptance-front-matter.py CLI and actual gate module in a temporary Git repository with a matching-head sweep and valid audit/thread ledger fixtures; assert exit 0 and preservation of the four-key replans object. Do not copy validation logic into the test or claim excluded prose ids are valid JSON ledger ids.
Exercise every new behavior red before production implementation and green afterward using Commands (c); report each selector and observed assertion failure. A skip or setup/import failure is not behavioral red.

## Check
Worker Playbook step 4 applies with design 5.14 item 10's measured facts: this host is Darwin, where the manifest's Claude seats run gh inside the sandbox (measured 2026-10-19T03:45Z). The current manifest's Linux-only exclusion does not apply here and is being removed by P1-15 under the D-024-17 revision. Record Commands (a)'s platform and every resolved command in sandbox.md. Every command, including fixtures, lint, Git, gh and messaging, stays sandboxed; any refusal stops dependent work and produces `AGMSG-PONG v1 task_id=dotfiles-T133-record-json-sync-a01 status=blocked` with the exact command and boundary, never an outside-sandbox retry or substitute tool.
Run Commands (c) before and after implementation and Commands (d) afterward; paste complete stdout/stderr and exit statuses into validation.md. Python children retain isolation. No shell file is authorized; shell scripts require English shdoc @file, @brief, @description, @arg and @exitcode comments plus shellcheck and shfmt.
Caps: at most 70 changed lines outside tests/ and .orchestration/, and at most 180 under tests/, using Commands (f)'s numstat; base40 is pasted at dispatch and head40 comes from RESULT, both full 40-hex SHAs. Count additions plus deletions and paste the numstat and both totals. Keep this whole task at or under 150 lines. Do not run Bats locally; use Commands (e) to verify final-head GitHub Actions and fix in-scope failures before RESULT.

## Completion
Use Commands (f) to start the named fresh branch from origin/main without tracking/config writes. Keep `.orchestration/dotfiles-T133-record-json-sync-a01/task.md` byte-identical to dispatch. In that directory write report.md (selectors, red/green, scope, limitations and cost), validation.md, sandbox.md, learning.md, autoskill.md and result.txt; records are data only. Keep plan/todo/learn worklogs uncommitted and at most one active todo per owner.
Complete worker agent-side review and the required repository review gate, retaining Commands (b–f)'s bindings, with repo-local resolved JSON evidence and receipt under the allowed artifact directory; never open a browser review or publish Crit. Use Commands (f) for commit/push and Commands (e) for a draft PR with an English title/body and the Worker Playbook's ready/CI/Bot sequence.
Commit/push all task changes and evidence, record final-head green CI, then send `AGMSG-RESULT v1 task_id=dotfiles-T133-record-json-sync-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with artifact paths. Report unrun checks; same-UID replacement and shared credentials remain residual risks.

## Checks (pasted by the orchestrator before each send)

```
```
