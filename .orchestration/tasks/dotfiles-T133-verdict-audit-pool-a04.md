---
format: 2
task_id: dotfiles-T133-verdict-audit-pool-a04
kind: code
security: true
allowed_files:
  - scripts/orchestrator/verdict.sh
  - .schemas/verdict.json
  - .schemas/audit.json
  - tests/unit/test_verdict.py
  - .orchestration/dotfiles-T133-verdict-audit-pool-a04/**
after: [dotfiles-T133-worker-write-boundary-a01]
reset_of: [dotfiles-T133-verdict-audit-pool-a03]
threat_table:
  - control: "scripts/orchestrator/verdict.sh (nine conditions, trusted-parent startup, fixed executable identities, contained output and explicit security metadata)"
    disposition: "residual: the regression fixtures exercise the declared execution and write controls; these controls reduce accidental and prompt-injected execution but do not isolate hostile processes sharing the orchestrator's UID."
  - control: ".schemas/verdict.json (the accept, revise and hold contract)"
    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_output_validates_against_its_schema_for_accept_revise_and_hold"
  - control: ".schemas/audit.json (the audit contract and controlled class vocabulary)"
    disposition: "residual: schema rejection is exercised by the retained validator tests; the sibling owns the separate vocabulary file and its equality test."
  - control: "tests/unit/test_verdict.py (retained behavior cases and the reset-design regressions)"
    disposition: "residual: temporary repositories and fixed fixture executables expose arguments, marker writes and side effects; they do not establish host isolation or authenticate live GitHub state."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/** (this reset task's artifacts)"
    disposition: "residual: artifacts identify their commands, tested heads and provenance; historical a03 evidence remains distinguishable from a04 final-head results."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md (dispatched task copy)"
    disposition: "residual: the first push adds the byte-identical dispatched a04 text; the TASK and RESULT bind this copy's own SHA256, which the orchestrator compares independently."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md (predecessor task-copy deletion)"
    disposition: "residual: the first push deletes only this predecessor copy under the explicit reset-bookkeeping exception; other a03 evidence remains unchanged."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/report.md"
    disposition: "residual: the report distinguishes inherited evidence, new results and retained predecessor artifacts; a local record does not authenticate its author."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/validation.md"
    disposition: "residual: validation records commands, red results, final-head results and tested heads; pasted output does not authenticate its source."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/sandbox.md"
    disposition: "residual: the record identifies refused commands and the observed boundary without claiming isolation from unrestricted same-UID processes."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/learning.md"
    disposition: "residual: reusable learning remains separate from executable policy and from predecessor evidence."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/autoskill.md"
    disposition: "residual: the run status or not-used record grants no execution or promotion authority."
  - control: ".orchestration/dotfiles-T133-verdict-audit-pool-a04/revise.yaml"
    disposition: "residual: revision instructions and selectors remain data, bounded by this task's files, caps and round allowance."
  - control: "agmsg storage route (~/.agents/skills/agmsg/scripts/lib/storage.sh; no application path exists in this task)"
    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path"
  - control: "application integration gate (make require-crit-review; no application path exists in this task)"
    disposition: "closed: tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path"
  - control: task metadata
    disposition: "residual: the orchestrator checks format-2 consistency before dispatch and at acceptance, validates security as an explicit boolean, and compares the complete dispatched task with its branch copy."
  - control: metadata separators
    disposition: "residual: the first opening and closing document separators bound safe-loaded YAML; the byte comparison also covers the body and subsequent separators."
  - control: in-process effects
    disposition: "residual: the Python child contains verdict and shadow writes; hold never appends a shadow row, and no application path exists in this task. --apply exits 2 with its named refusal; verdict never dispatches, calls the gate, executes agmsg code or merges."
  - control: workflow and interpreter or environment inputs
    disposition: "residual: a trusted parent supplies the clean environment before any exec, startup checks refuse rather than repair, and internally fixed executable paths remove the caller-bin interface; shared-UID access to installations, credentials and host state remains outside the isolation these controls provide."
  - control: new or renamed scripts
    disposition: "residual: verdict.sh remains the only implementation executable introduced by this PR; no pool executable, caller wrapper, dependency or production test-override interface is added."
  - control: orchestrator effect merge
    disposition: "residual: only the orchestrator performs the live head-matched squash merge with --repo mryfmo/dotfiles after the prescribed evidence and integration gate; verdict has no application path."
  - control: orchestrator effect update-branch
    disposition: "residual: an update-branch changes the head and invalidates head-bound evidence; the orchestrator repeats required CI, feedback collection, audit and security review for the resulting head."
  - control: orchestrator effect forced worker removal
    disposition: "residual: no forced removal is planned; any forced removal follows the existing dirty-worktree rule and records discarded uncommitted state."
  - control: "design 5.14 item 1 (worker write boundary)"
    disposition: "residual: the worker does not change its own execution boundary; Claude write isolation is not inferred from render-check, and the orchestrator verifies the deployed boundary separately."
  - control: "design 5.14 item 2 (sanitized environment before execution)"
    disposition: "residual: a trusted parent supplies the clean environment, including passwd-derived HOME, before exec; the program checks allowed names, its resolved script path and HOME and exits 2 on refusal without self re-exec. Privileged mode alone cannot prevent Linux loader execution; caller integration and shared-UID host execution remain separately assessed."
  - control: "design 5.14 item 3 (trusted path boundaries)"
    disposition: "residual: resolved executable and destination paths are checked against the declared trusted roots; a same-UID process outside a worker sandbox can still mutate host paths."
  - control: "design 5.14 item 4 (execute verified identities and consume verified contents)"
    disposition: "residual: executables run by verified realpath, consumed snapshots are rehashed immediately before use, and decision-input hashes enter the verdict; snapshots do not create a boundary against unrestricted same-UID mutation."
  - control: "design 5.14 item 5 (output and reservation identity)"
    disposition: "residual: verdict and evidence snapshot filenames and shadow rows use the full head; each audit, security, local-review and sweep input is also matched by its full-head metadata, and this verdict task introduces no reservation lock."
  - control: "design 5.14 item 6 (honest residuals)"
    disposition: "residual: startup, path and snapshot controls are reported as damage reduction; neither host isolation nor independent GitHub credentials is claimed."
  - control: "design 5.14 item 7 (verification)"
    disposition: "residual: this task supplies concrete regression selectors and final-head evidence; the shared trusted-execution test helper remains owned by P1-6 and is reused only if available without expanding this task's edit boundary."
  - control: "design 5.14 item 8 (committed approval ledger)"
    disposition: "residual: verdict evaluation supplies no permission approval; every gh call names mryfmo/dotfiles explicitly, and PR data comes from GitHub at one base/head pair captured once and recorded at full SHAs, never shared refs or objects. No application path exists in this task; shared credentials remain a residual."
  - control: "design 5.14 item 9 (private cache and absolute interpreter)"
    disposition: "residual: the shared trusted-interpreter resolver anchors the install root to the passwd home of the real uid, never HOME, and the anchored private uv cache excludes worktrees, worker-writable caches and temporary directories; until the P1-3 resolver is available, verdict holds without a private resolver or PATH fallback."
  - control: "design 5.14 item 10 (worker commands remain sandboxed)"
    disposition: "residual: every worker gh command and git write runs individually inside the sandbox; a command that cannot complete there produces a blocked PONG rather than an escape or alternate execution route."
premises: []
---

# AGMSG-TASK dotfiles-T133-verdict-audit-pool-a04 — INV-6 S1 re-plan of a03 (plan 024 P1-4a; PR #410)

Worker: a008, Claude Code, worktree `worker-f`.

This text is the independent redesign by a review-profile context other than the author of the predecessor task texts. The a03 pre-push fix round and revise 1 exhausted its C-61 allowance. The security review of `513e5d05` found caller-controlled executable selection and cached-bytecode execution; the review of `6b7e7833` found inherited `compgen` execution, acceptance of attacker-selected absolute symlink targets, uncontained output writes and an implicit non-security branch.

The a03 acceptance record contains three `env-trust-bypass` rows: `security:513e5d0:1`, `security:6b7e783:1` and `security:6b7e783:2`. Its recorded `re-plan:` line establishes INV-6 S1. Another a03 patch round is not authorized. This reset changes the execution contract so a trusted parent supplies the clean environment before exec, the program verifies and refuses without self re-exec, and no caller executable directory exists.

Read these records before implementation:

- `.orchestration/tasks/dotfiles-T133-verdict-audit-pool-a03.md`
- `.orchestration/acceptance/dotfiles-T133-verdict-audit-pool-a03.md`
- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-513e5d0.md.last.md`
- `.orchestration/validation/dotfiles-T133-verdict-audit-pool-a03-security-6b7e783.md.last.md`

The design at `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md`, section 5.14, applies by reference, including today's amendments to items 2, 8 and 9 and items 4 and 5. This absolute path identifies the orchestrator's uncommitted working copy under C-86. The task does not claim that section is already on `origin/main`.

The sentences of section 5.14 this task relies on are quoted here verbatim (C-88: the quoted sentences are normative; the path above is context, and the design file is uncommitted at authoring time):

> 2. **無害化した環境を最初に** 最初の処理として `env -i` に入り、PATH は信頼ルートで解決した絶対バイナリへのリンクだけの私設ディレクトリ（shims、空、相対は拒否）。git は毎回 `GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null -c core.hooksPath=/dev/null -c core.fsmonitor=false -c protocol.allow=never -c protocol.https.allow=always` と明示 `-C`（https だけ許す。`protocol.allow=never` 単独は必要な fetch を止める）。 検査の読み取りは `GIT_NO_LAZY_FETCH=1` で部分クローンの遅延 fetch（checkout 設定の credential.helper を起動しうる）を止め、`-c submodule.recurse=false --ignore-submodules=all` で submodule 内の status/diff（submodule 自身の設定が filter を有効化しうる）を止める。`.gitmodules` を持つ checkout は検査対象として拒否する。 `-C` は作業木を束縛しないので（repo-local の `core.worktree` が読み先を checkout 外へ向けられる）、git は `--git-dir=<checkout>/.git --work-tree=<checkout>` を明示し、`git rev-parse --show-toplevel` の realpath が checkout と一致しないときは拒否する。 premise や検査の「コマンド実行」は、固定語彙の読み取り専用プローブ（`git rev-parse <ref>`、`test -e <path>`、`grep -c <pattern> <file>` のように検査器自身が解釈する形）だけを許し、任意のシェル文字列は実行しない（本文のハッシュはコマンド文を認証するだけで、`python -I scripts/x.py` のファイル被演算子や `source ./x.sh` の中身は認証しない）。diff と show は `--no-ext-diff --no-textconv` と `-c core.attributesFile=/dev/null -c core.sshCommand=false` を付け、PR 側の `.gitattributes`（external diff、textconv、filter）が検査内容や実行物を変えないようにする。Python は `-I`。PATH 探索で実行するものは無い。 A shell script that runs under a PR-controlled or worker-controlled environment (verdict.sh, the chain glue, CI steps) is executed as a program with `#!/bin/bash -p`, never as `bash <file>`, and only by a trusted parent that supplies the clean environment before the exec: `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …` (long options before `-p`). Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but on Linux an inherited `LD_PRELOAD`/`LD_AUDIT` already executes while the loader maps `/bin/bash`, before `-p` or any statement runs, so a self re-exec inside the script is not a boundary and re-executing `"$0"` would reopen the caller's pathname (a worker-owned symlink can be swapped between the two executions); the program therefore verifies and refuses instead of repairing: its environment must consist of exactly the allowed names (checked through absolute paths `/usr/bin/env`, `/usr/bin/grep`), `$0` resolved with `realpath` must be a regular file under the repository root, and HOME must equal the passwd home of the real uid (`/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS, `/usr/bin/getent passwd <uid>` on Linux), otherwise exit 2 with a named message. A caller-set sentinel variable is not a sanitization proof, because the caller controls it (ci-efficiency a04 and verdict a04 C-80 reviews, 2026-10-19). No script accepts a caller-supplied executable directory; interpreters are the fixed absolute paths item 9 names.

> 4. **検証したものを実行し、検証した内容を渡す** 検証した実行体はその realpath で実行する（再探索しない）。検証したファイル内容は信頼ルート配下のスナップショット（0600、一意名）として渡し、使用直前に sha256 を再照合する。判断に読んだ証跡は sha256 を出力に記録する。

> 5. **出力と予約の同一性** 名前には 40 桁の head を使う（7 桁で衝突させない）。lock は信頼ルート配下の固定 inode に O_EXCL で作り、置換を inode 比較で検出する。物理スロット 1 つに lock 1 つ。

> 8. **承認はコミット済み台帳から読む** permission の決定行（`scope=permission approved_by=user diff_sha256=…`）は anchored checkout の作業コピーではなく、コミット済みの台帳から読む。読み方は `git ls-remote origin refs/heads/main` が返す commit sha を取り、GitHub API（`gh api repos/<owner>/<repo>/contents/.orchestration/decisions.tsv?ref=<sha>`、sandbox 内）でその sha の内容を取得する。ローカルの `git show` は共有 object database が書けるため中間 tree の差し替えで偽物を返しうる（第 3 回審査の所見 2）（ローカルの ref 名 `origin/main` は経由しない。`refs/replace/` も書けるので replacement を無効にする。Codex worker は `.git/objects` と `.git/refs` に書けるので ref は差し替えられるが、sha で指した object は内容アドレスで偽造できない）。作業コピーの行は提案で、記録 PR が main にマージされて初めて承認になる（PR の承認は操作者の操作）。偽造には main へのマージが要る。 The same applies to the PR content a mechanism evaluates (the verdict, the audit precheck, the counters): the changeset is read from GitHub at the 40-hex head (`gh api repos/{owner}/{repo}/compare/<base40>...<head40>`, `…/contents/<path>?ref=<head40>`) or from a private clone whose object store no worker can write; the main checkout's shared `.git/objects` and its `origin/main` ref are not evidence sources, because Codex workers write them (a04 C-80 round 1, 2026-10-19). Evidence files are named and matched by the full 40-hex head, never by a 7-character prefix. Every `gh` invocation names the repository explicitly: `gh pr`, `gh run` and `gh issue` subcommands take `--repo mryfmo/dotfiles` or the full pull-request URL, and `gh api` (which has no `--repo` flag) takes the explicit `repos/mryfmo/dotfiles/…` endpoint path, never a `{owner}/{repo}` placeholder; a `gh api graphql` call binds the repository through fixed query variables (`owner: "mryfmo"`, `name: "dotfiles"` as constants in the script, passed with `-f`/`-F`) and uses only node ids obtained from a query bound by those variables (verdict a04 C-80 round 5, 2026-10-19): the local repository configuration selects the default repository otherwise, and a matching head sha does not bind the repository because a fork can hold the same commit (verdict a04 C-80 round 2, 2026-10-19). A mechanism whose application path runs code this contract does not yet cover (the agmsg storage layer sourced by `dispatch.sh`/`history.sh`; the integration gate until its own hardening task lands) names that task as the prerequisite of its `--apply` mode and runs shadow-only until the prerequisite is merged.

> 9. **私設キャッシュ** orchestrator 側の実行は worker と共有するキャッシュ（`~/.cache/uv`、`~/.local/share/uv`、mise）から実行可能物を読まない。`UV_CACHE_DIR` を anchored checkout 配下（`.agents/worklog/uv-cache`、gitignored、worker 書き込み不可）に固定し、`uv run --no-config --no-project --offline --python <信頼ルートの絶対パスのインタプリタ>` で起動する（`--no-config` で uv の設定探索を止め、`--python` の絶対パスで cwd や親の `.venv` の発見を止める；敵対的な `.venv` と `uv.toml` を置いた fixture で検証）。hook は uv を使わず jq と python 標準ライブラリだけで動く。 One trusted interpreter resolver (`scripts/orchestrator/trusted-interpreter.sh`, P1-3 lineage) resolves `<abs>` from the repository's pinned declaration to a regular file under the tool manager's install root (the install root is anchored to the passwd home of the real uid, never to the HOME variable, which a caller can forge), refuses anything else, and every orchestrator-side script consumes it; no script keeps its own `command -v`, `mise which` or PATH fallback (ci-rerun.sh security review 44cb835, 2026-10-19). Shell code of other projects (the agmsg storage layer and its `drivers.partition` sourcing) is never sourced by an orchestrator-side mechanism; counters are read from the agmsg SQLite store read-only with a fixed query or from the pasted record. Every Python child of a trusted entrypoint runs with `-I` (isolated: no user site, no `PYTHON*` environment, no script directory on `sys.path`), so `uv run … python -I <script>` rather than `--script` for a script without declared dependencies; a test plants a `.pth` and a `usercustomize.py` in a fake user site and asserts they never execute (P1-15 amendment 5 C-80, 2026-10-19).


Host controls reduce accidents and prompt-injected damage. They do not isolate unrestricted processes sharing one UID. The design's GitHub prevention boundary is also not established while worker and orchestrator credentials remain accessible to that same UID; subsequent boundary-record checks provide detection as the design states.

## Branch and reset boundary

Continue `tools/verdict-audit-pool-a01`, PR #410, from `6b7e7833a85528440dc397c2555bc9dd603c685a`, already update-branched onto main `3f240b12`. Keep the a03 implementation, regression coverage and evidence. Create neither another implementation branch nor another PR.

The first push deletes `.orchestration/dotfiles-T133-verdict-audit-pool-a03/task.md` and adds the dispatched text byte-for-byte at `.orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md`. This single predecessor-copy deletion is the explicit reset-bookkeeping exception to `allowed_files`. Other a03 evidence remains unchanged under its original task identifier and tested heads.

The orchestrator retains the a03 acceptance history, class rows, stopped status and counters. The final inventory identifies preserved a03 evidence separately from a04 additions; preservation does not authorize further worker edits in the a03 directory. The a01/a02 artifact removals already completed by a03 are not repeated or reversed.

The split remains intact. The pool sibling owns `scripts/orchestrator/audit-pool.sh`, changes to `scripts/orchestrator/orch-audit.sh`, `.schemas/classes.yaml` and `tests/unit/test_audit_pool.py`. `audit-pool.sh` is absent at `6b7e7833`; the audit schema at that head is `.schemas/audit.json`. Neither fact authorizes recreating a split file or adding a `schemas/` mirror. PR #407 remains parked; its parking operation is not repeated.

## Goal

Produce one schema-valid verdict from nine positively checked conditions without executing inherited shell startup code, accepting caller-selected executable directories, following output symlinks or treating invalid `security` metadata as an exemption.

Retain complete feedback validation, amended-cap precedence, offline operation and finding counts. This task computes and records shadow verdicts only; `--apply` is rejected as item 6 specifies.

## Files

1. `scripts/orchestrator/verdict.sh <pr> [--loop] [--shadow]` remains Bash with `set -Eeuo pipefail`, English shdoc documentation and `jq` for JSON. Its startup and executable selection follow the Reset design below. Each condition is `{id, ok, evidence}` and becomes true only through a positive check of parsed, validated input.

   Inputs remain the PR view and checks, the acceptance record's JSON block and prose, the selected task or `--task <id>`, the audit JSON, a fresh feedback sweep, saved feedback dispositions, the task's allowed paths and caps, regime counters, the GitHub merge-base changeset and the head-specific security review. The acceptance block names the PR, task and current head and contains a ledger array. The PR is open, non-draft and based on `main`. At the start of each PR evaluation, capture `head.sha` and `base.sha` together once from `gh api repos/mryfmo/dotfiles/pulls/<pr>` as `head40` and `base40`, require both to be 40 lowercase hexadecimal characters, and bind all reads to that pair. Record both in the verdict JSON as `head` and `base`. The compare listing and file contents are read from GitHub at that captured pair; no separate current-main read replaces either value. If a second PR read is needed, compare both SHAs with the captured pair and refuse with hold, exit 20 and `verdict: PR base/head changed during evaluation` if either differs; append no shadow row and never combine reads from different pairs. This task chooses GitHub API reads, not a local clone: read the changeset through `…/compare/<base40>...<head40>` and inspected PR bytes through `…/contents/<path>?ref=<head40>`. Repository identity is fixed to `mryfmo/dotfiles` from the trusted repository declaration, not caller environment or local Git configuration. Every `gh pr`, `gh run` and `gh issue` invocation supplies `--repo mryfmo/dotfiles` or the full pull-request URL. REST `gh api` calls, including instantiated REST templates in the design quotation, use an explicit `repos/mryfmo/dotfiles/…` endpoint path, never `--repo` or a `{owner}/{repo}` placeholder. `gh api graphql` calls instead carry `-f owner=mryfmo -f name=dotfiles` (or equivalent `-F` fields), supplied from fixed `owner: "mryfmo"` and `name: "dotfiles"` constants in the script, and use only thread node ids returned by the review-thread query bound by those variables. This REST/GraphQL distinction also governs the API endpoint wording in Completion. The retained fresh sweep invokes `scripts/pr-feedback.py`: its `THREADS_QUERY` supplies owner/name, but its `THREAD_COMMENTS_QUERY` currently supplies only id/cursor. Reuse its authenticated `collect("mryfmo/dotfiles", ...)` in the fixed isolated Python child with fixed-executable REST and GraphQL callbacks defined in `verdict.sh`; the GraphQL callback supplies both fixed repository fields on every request, including node pagination, and refuses an id not returned by the bound review-thread query. Neither helper is edited; `scripts/orchestrator/fill_sweep.py` only fills saved JSON dispositions and issues no `gh` calls. A matching head SHA in a fork is not a repository binding. Missing, incomplete, truncated or unreadable API data holds; no local-head fetch or shared-object fallback is allowed.

   Condition 1 verifies that the GitHub contents response for `.orchestration/<task>/precheck.json?ref=<head40>` hashes to the record's `precheck:` value and names the head or an ancestor authenticated by GitHub compare data whose diff to the head contains only `.orchestration/<task>/` paths. The retained `PRECHECK_REQUIRED` setting is supplied explicitly as `--precheck-required 0|1`; absent or zero makes this condition's failure a warning. No environment exception is added for it.

   Condition 2 requires every required check to be present with state `SUCCESS` for the head. Empty or unreadable checks hold. Every duplicate entry for a required name must also be `SUCCESS`.

   Condition 3 requires an audit that validates against `.schemas/audit.json`, names the task and full head, has zero open P0/P1 findings, and has verdict `correct` or a non-empty set of remaining findings whose scopes are all `records`. A blocked audit holds. An incorrect audit without remaining findings fails this condition.

   Condition 4 requires saved and fresh feedback documents to name the accepted head, complete feedback identity matching with multiplicity, and a valid disposition for every fresh item. Diagnostic URLs do not determine the result.

   Condition 5 requires every path in the base-to-head diff to match an `allowed_files` entry and additions-plus-deletions totals to remain within the effective Check caps. The comparison is `gh api repos/mryfmo/dotfiles/compare/<base40>...<head40>` using the PR API's base and head, and its full `merge_base_commit.sha` identifies the merge base. Consume the complete authenticated file list and its additions/deletions; account for both names of a rename. An unreadable merge base or incomplete changeset holds. The main checkout's `.git`, including `origin/main`, replacement refs and objects, is not an evidence source. Backticked exclusions after `outside` leave the outside count; default exclusions remain `tests/` and `.orchestration/`. Item 7 retains amendment precedence.

   Condition 6 reads one orchestrator-pasted INV-6 counters block in the acceptance record, bound there to this task, PR and full head. This task chooses the pasted record rather than a live store query so verdict executes no agmsg shell code and cannot follow worker-writable `drivers.partition`. It never invokes `scripts/regime-counters.sh` or sources the agmsg storage layer. No `S1:` line is present and the parsed decimal `revises` value is below 2. A missing ledger or counters block, duplicate block, mismatched binding or unreadable count holds; an absent count is never zero.

   Condition 7 requires the numeric count of open P0/P1 findings to be zero. Findings with status `new`, `still-open` or absent count as open regardless of identifier or scope.

   Condition 8 first validates `security` as an explicit boolean. Only boolean `false` permits the non-security branch. Boolean `true` requires the security review's front-matter `head:` to equal the verdict's own full 40-hex head and its last non-blank line to be `Verdict: correct`. A sha7 filename is never a head match. Missing, null or non-boolean metadata holds with the named reason specified below.

   Condition 9 requires at least one `sha256:<hex> <path>` line in the acceptance record's prose and verifies every such line against its file. Every inspected evidence file, including audit, security, local review and saved or fresh sweep, is named with and matched against the verdict's full 40-hex head: Markdown uses front-matter `head:`, audit and local-review JSON use `head` (on every record for a JSON list), and feedback JSON uses `head_sha`. Missing, invalid or different full-head metadata holds even when a filename or sha7 prefix matches. Hashes preserve consumed bytes; they do not authenticate a local Git object or ref.

   All nine conditions passing produces `accept`. Failure of condition 6 or 7, missing or unreadable input, schema-invalid input, invalid security metadata or an internal evaluation error produces `hold`. Other failed conditions produce `revise`. The revise line remains `AGMSG-ACCEPTANCE v1 task_id=<task> status=revise previous_head=<head> reason=<failed ids> next_action=<the first failed condition's evidence, shell-safe>`. The orchestrator supplies `check=` selectors.

   The generated verdict is `.orchestration/validation/<task>-verdict-<head>.json`, using the full 40-character head under design 5.14 item 5. Its fields are `verdict`, `pr`, `head`, `base`, `task_id`, `conditions[]`, `inputs_sha256{}`, `generated_at` and optional `revise_line`, validated against `.schemas/verdict.json`. Audit, security, local-review and sweep inputs use full-head-named verified snapshots with the metadata bindings above. External producers are not edited; the orchestrator supplies the full-head-named evidence and required metadata before evaluation, retaining original artifacts separately. Historical verdict files remain untouched.

   Exit codes remain 0 for accept, 10 for revise, 20 for hold and 2 for usage or internal error, with internal error treated as hold. A destination or post-startup execution-boundary refusal holds with exit 20; the mandatory startup refusals in Reset design item 1 exit 2 with their named messages. Refusal before a usable task or head exists reports hold without inventing an output identity.

   `--apply` is unsupported and exits 2 with `verdict: --apply is not supported in this shadow-only task` before input reads or tool calls other than mandatory startup verification. No application branch, dispatch, gate call, agmsg execution or merge remains. Arguments containing `--admin` or `--auto` anywhere are refused with exit 2 before input reads or tool calls other than mandatory startup verification.

   Shadow evaluation is the default; `--shadow` is its explicit spelling. It writes the verdict JSON and, only for a non-hold verdict, appends `<pr>\t<head>\t<verdict>\t\t\t<generated_at>` to `.orchestration/validation/verdict-shadow.tsv`. Columns remain `pr`, `head`, `machine`, `human`, `agree` and `at`; the orchestrator supplies the human and agreement columns. Shadow mode sends nothing and merges nothing, invokes no dispatch, gate or agmsg code, and treats no gate conclusion as binding.

   `--loop` retains PR-number order, eligible open non-draft PRs on `main`, and an acceptance record naming each current head. Each recursive verdict invocation uses the sanitized program-entry contract and captures that PR's single base/head pair at its start as above. The loop computes and records shadow verdicts only; it never refreshes a checkout, dispatches, calls the gate, executes agmsg code or merges. Evaluation never uses the main checkout's shared refs or objects.

2. `.schemas/verdict.json` and `.schemas/audit.json` remain JSON Schema 2020-12 documents with `additionalProperties: false` at the top level and in defined item objects.

   The audit contains `head`, `task_id`, `auditor`, `generated_at`, `verdict` and findings with `id`, `priority`, `confidence`, `file`, `line`, `class`, `scope`, `rationale` and optional `status`. The controlled class enum retains the vocabulary snapshot at `b8998de162afc72d53d07679b8f0a194fcc480ff`.

   The existing stdlib schema validator remains available through `--validate` under the fixed isolated interpreter, without a new helper file or dependency. Required keys, types, enums, bounds, SHA patterns, additional-property restrictions and RFC 3339 timestamps with offsets remain checked. Date-only values, naive timestamps and invalid calendar dates fail. Runtime validation does not depend on the sibling's `orch-audit.sh --validate`.

3. The retained interpreter-selection requirement is implemented through Reset design item 2 rather than the a03 caller-bin mechanism.

   Before PR input processing, the trusted entrypoint fixes absolute executable identities and the offline PyYAML environment. Checkout `.python-version`, `.venv`, executable files, uv configuration, mise configuration and inherited tool-selection variables cannot select an interpreter or tool. Missing trusted installations or unavailable offline dependencies hold before evaluation.

   The historical interpreter regression against `85a472294d0c10835bd7235e3c76d045846a6ed9` remains identified as historical. Its marker-writing interpreter cases run again against the final implementation.

4. The a02 and a03 finding-count and feedback fixes remain acceptance requirements.

   Conditions 3 and 7 count open P0/P1 findings numerically. Empty identifiers and records scope cannot hide a finding.

   Condition 4 requires both saved and fresh `head_sha` values to equal the accepted head. Missing or invalid dispositions are counted before formatting URLs; null and empty URLs affect diagnostics only.

   Complete identity and multiplicity retain the trusted helper's `feedback_key()` and `missing_feedback()` behavior. Source, URL, level, path, line, body and author participate, with only existing exact masked-body and masked-path equivalence. One saved occurrence covers one fresh occurrence.

   Dispositions retain `parse_disposition()` validation and `commit_in_range()` semantics, but verdict checks commit membership through complete GitHub compare/commit data instead of calling the helper's local-Git range check. A fix commit exists within the authenticated base-to-head range. A not-applicable disposition has a non-empty reason and evidence command and satisfies existing level-specific reason requirements. Evidence commands remain data and are never executed.

   Neither `scripts/require-crit-review.py` nor its validator is edited. Shadow evaluation never calls the gate or treats its conclusions as binding. Retained red evidence keeps its original head; final-head green results are new evidence.

5. `tests/unit/test_verdict.py` retains the sixteen shadow behavior tests at `6b7e7833`, including schema-rule rejection, offline PyYAML refusal, numeric finding counts, feedback head binding, null diagnostic URLs, identity and multiplicity, disposition validation, amended caps and cached-bytecode refusal. Delete the three application, gate-order and post-merge checkout-refresh tests and their application-only fixtures; retain the `--admin` and `--auto` refusal controls in the no-application-path regression below.

   The a03 test named `test_verdict_ignores_caller_bin_and_path_overrides` retains its coverage of hostile PATH selection while its removed executable-directory fixture is replaced by the fixed-entrypoint fixture: direct dirty invocations refuse, and trusted-parent clean invocations preserve the verdict without executing planted tools. Neither the script nor the test source retains `VERDICT_BIN` or another production executable-directory override.

   Existing shadow positive and negative controls remain: empty checks, failed duplicate checks, blocked audits, incorrect audits without findings, missing ledgers and records, unavailable GitHub heads, unreadable GitHub merge bases, backticked cap exclusions and absent evidence hashes.

   Fixtures use temporary repositories and fake external tools whose absolute identities are established in the fixture's trusted entrypoint before invocation. They do not reintroduce caller PATH discovery or a production test-only override. The actual Python used for valid execution satisfies the interpreter boundary. All fixture lines count toward the test cap.

6. No application path exists in this task.

   Remove application code, prerequisite-ledger reads, agmsg installation checks and their tests. `verdict.sh` never dispatches, calls the gate, executes agmsg code or merges, including in `--loop`. It computes and records only the shadow verdict JSON and non-hold TSV row described in item 1. Passing `--apply` exits 2 with `verdict: --apply is not supported in this shadow-only task` before input reads or tool calls other than mandatory startup verification; no verdict or shadow row is written for that usage refusal.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_has_no_application_path` covers default, `--shadow` and `--loop` evaluation and unsupported `--apply`, including `--loop --apply`. Shadow evaluations record the schema-valid JSON with full `head` and `base` and append only the machine TSV columns for non-hold verdicts. Marker-writing gate, dispatch, history and agmsg fixtures remain untouched and no merge occurs. The `--apply` cases require the named message, exit 2, no PR or prerequisite reads and no output writes. The retained `--admin` and `--auto` controls still refuse before input reads or effect calls.

7. The retained cap-parser fix remains enforced.

   The last applicable cap declaration in text order governs, including its exclusions and outside limit. A later test-only amendment changes the test limit while retaining the outside limit.

   `test_verdict_condition_5_honors_the_latest_amended_caps` retains the original 500 versus amended 550 case with 531 changed test lines, the actual a02 test-only wording, a later lower limit, changed exclusions and changed outside limit. Unrelated conditions stay green and evidence hashes are refreshed. Its original red head remains historical.

The required check names remain `validate`, `test (ubuntu-24.04, server)`, `test (ubuntu-24.04, client)`, `test (macos-14, client)`, `public-bootstrap (ubuntu-24.04, server)`, `public-bootstrap (ubuntu-24.04, client)` and `public-bootstrap (macos-14, client)`.

## Reset design

1. **A trusted parent supplies the clean environment before exec; startup verifies and refuses.**

   `verdict.sh` has mode 0755 and shebang `#!/bin/bash -p`. A trusted parent invokes it with `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <absolute script path> …`, with long Bash options before `-p`. The parent supplies a clean environment before any exec, including the exec of `/usr/bin/env` itself; launching that prefix with inherited loader variables is not sanitization before the loader. Privileged mode discards inherited functions, `BASH_ENV`/`ENV`, `SHELLOPTS`, `BASHOPTS`, `CDPATH` and `GLOBIGNORE`, but does not enable the loader’s secure-execution mode. On Linux, inherited `LD_PRELOAD` or `LD_AUDIT` can execute before Bash’s first statement. There is no self re-exec and no reopening of caller-controlled `$0`.

   Before `set`, traps, argument processing or executable discovery, the first executable compound statement verifies privileged mode, the startup environment, the script path and HOME. A missing privileged mode refuses with exit 2 and `verdict: execute as a program`. Check environment names through absolute `/usr/bin/env` and `/usr/bin/grep`; exactly `PATH`, `HOME`, `LANG`, `PWD`, `SHLVL` and `_` are allowed, with fixed `PATH=/usr/bin:/bin` and `LANG=C.UTF-8`. An extra/missing name or wrong fixed value refuses with exit 2 and `verdict: untrusted startup environment`. A caller-set sentinel proves nothing and is not accepted.

   Resolve `$0` with the fixed absolute realpath utility and require an absolute invocation path whose realpath is a regular file under the anchored repository root; otherwise exit 2 with `verdict: untrusted script path`. Resolve the real uid through absolute `/usr/bin/id -ru` and obtain its passwd home through `/usr/bin/dscl . -read /Users/<user> NFSHomeDirectory` on macOS (the user is resolved from that real uid), or `/usr/bin/getent passwd <uid>` on Linux. Missing, ambiguous or unreadable account data, or HOME unequal to that passwd home, exits 2 with `verdict: HOME does not match passwd home`. The repository root and passwd-home lookup do not derive from caller HOME, PWD or local Git configuration. Refuse instead of repairing any failed check. No `compgen`, `unset -f` loop or PATH edit serves as the startup boundary.

   Every ordinary caller, including the loop child and test helpers, is the trusted parent for that exec and uses the exact clean prefix with the passwd home and absolute script path; no sentinel is exported or trusted. The retained `PRECHECK_REQUIRED` control is passed as the explicit `--precheck-required 0|1` argument when needed, defaults to 0, and is never inherited or retained as an environment name.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_program_discards_hostile_startup_environment` executes the program with exported functions named `compgen`, `[`, `test`, `exec`, `command`, `builtin` and `command_not_found_handle`, a marker-writing `BASH_ENV`, `LD_PRELOAD` and `LD_AUDIT` naming marker-library paths, a forged HOME containing a marker-writing interpreter, and a planted PATH. The fixture also supplies the other startup selectors discarded by privileged mode. The direct dirty invocation must exit 2 with `verdict: untrusted startup environment` and no marker; it must not repair or re-exec. The direct dirty cases use deliberately non-loadable library paths: a loadable constructor cannot be prevented after a dirty exec. Exercise a loadable marker library only through the already-trusted parent supplying the clean environment before every exec, and require no marker. The clean prefix must yield the unchanged clean verdict and conditions, so an incidental exit 2 cannot pass the positive control.

   Separate subcases exercise each named refusal: a forged HOME with otherwise allowed names and fixed values, a symlinked `$0` resolving outside the repository, and `VERDICT_SANITIZED=1` together with `GIT_CONFIG_GLOBAL`, `GIT_DIR` and `GIT_INDEX_FILE` pointing to planted files. Require the appropriate named message, exit 2, no marker or application effect and no consumption of planted configuration, objects or index. Check the clean child’s allowed-name-only environment and passwd-derived HOME. Exercise the exact long-options-before-`-p` command.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_bash_file_invocation` invokes `bash scripts/orchestrator/verdict.sh …` in a clean fixture and requires exit 2 and the named message. This negative invocation is the sole deliberate plain non-privileged Bash verdict call in the tests.

2. **Executable identities are fixed at the trusted entrypoint.**

   No caller-supplied executable directory exists. Remove `VERDICT_BIN`, its environment whitelist, symlink-directory acceptance and every equivalent caller override from the script and fixtures. Do not replace them with a differently named environment variable or CLI option.

   The trusted entrypoint fixes the absolute paths for Bash, uv, Python, gh, git, jq and required utilities before reading PR-controlled input. It executes verified realpaths without rediscovery. The repository's Python declaration is a read-only input; consume `scripts/orchestrator/trusted-interpreter.sh` from the authenticated trusted base when present. The P1-3 resolver alone resolves the pinned declaration to a regular executable file under the tool manager's install root, anchored to the passwd home of the real uid, never to HOME, and outside worktrees, worker-writable caches and `$TMPDIR`. A symlink spelling alone authenticates nothing. An absent resolver or invalid trusted installation holds rather than selecting another interpreter from PATH, mise, uv discovery or a checkout. No private resolver, `command -v` or `mise which` fallback is retained here. Implementation may proceed before `dotfiles-T133-ci-efficiency-followup-a04` lands by implementing and testing this unavailable-resolver hold with a trusted resolver fixture for successful cases; live execution stays on hold until that lineage supplies the resolver. This task therefore does not need the resolver at implementation time and adds no P1-3 `after:` dependency.

   Design 5.14 items 2, 4 and 9 apply by reference to Git invocation, executable paths, verified snapshots and private cache use. The uv invocation is `uv run --no-config --no-project --offline --python <abs>`, with uv itself an internally fixed absolute executable and `<abs>` the validated interpreter realpath. `UV_CACHE_DIR` is the anchored private cache from the design. Worker-shared uv or mise caches supply no executable. Python children use `-I`; the a03 `-B`, `sys.dont_write_bytecode` and refusal of checkout bytecode that helper imports could consume remain enforced.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_uses_only_declared_absolute_executables` verifies fixed tool identities, refusal of hostile PATH and inherited interpreter selectors, and unchanged clean-prefix execution, including an absolute symlink to a marker-writing interpreter and a forged HOME install tree that cannot become the trusted install root.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_interpreters_in_worktrees_caches_or_tmp` covers each excluded root, a non-regular target, a forged-HOME install root and a valid regular-file control under the passwd-home-anchored install root.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_executes_verified_snapshots_and_records_input_hashes` changes a validated source or input before consumption and verifies refusal or consumption of the verified snapshot, never the substituted contents, and checks the recorded input hashes.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_without_the_shared_trusted_interpreter_resolver` verifies the interim hold and absence of interpreter discovery or application effects.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_reads_pasted_counters_without_sourcing_agmsg` plants a marker-writing agmsg driver and counter executable, supplies the valid pasted counters, and requires unchanged verdicts with no marker; missing, duplicate, mismatched and unreadable counter cases hold.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_ignores_replaced_local_objects_and_refs` serves forged PR bytes through a replaced local object and forged `origin/main`, while fixed GitHub fixtures return the authentic full-head changeset and contents. It requires the clean verdict and authenticated input hashes, no local-object evidence read, and hold on incomplete API data rather than a local fallback. Cover precheck ancestry, fix-commit membership and loop shadow evaluation through the same GitHub fixtures.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_names_the_repository_on_every_gh_call` runs with a fixed fake gh that records every argument vector and asserts `--repo mryfmo/dotfiles` on every `gh pr`/`gh run`/`gh issue` call, an endpoint path beginning with `repos/mryfmo/dotfiles/` on every REST `gh api` call, and both `-f owner=mryfmo -f name=dotfiles` (or equivalent `-F` fields) on every `gh api graphql` call, with no `--repo` flag or repository placeholder on API calls. It exercises the retained collector through a bound review-thread query and node-comment pagination, verifies that every consumed thread id was returned by that bound query, and preserves the complete feedback and resolution-state results. Separate negative subcases omit owner, name or both, change either fixed value, or substitute a thread id not returned by the bound query; the fake gh rejects a GraphQL call without both correct variables, and verdict refuses the unbound input with hold, exit 20 and no shadow row. It covers PR view/checks, REST API and feedback reads and loop shadow evaluation in PR-number order. A fork fixture containing the same head SHA cannot redirect a call.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_refuses_a_changed_pr_base_or_head` supplies one initial GitHub `base40`/`head40` pair and differing SHAs on a required second read. Separate subcases change only the base, only the head and both. Each requires the named pair-change refusal, hold with exit 20 and no shadow row; the unchanged-pair control records both full SHAs and proves every compare listing and contents request uses the captured pair.

   The retained `test_verdict_pins_tools_interpreter_and_environment_before_reading_a_pr_checkout` and `test_verdict_never_imports_cached_bytecode` remain green. Unavailable offline PyYAML still holds with no online fallback.

3. **The Python child contains persistent writes.**

   Verdict JSON and shadow logging are opened through the fixed isolated Python child inside `<repo>/.orchestration/validation/`. Their resolved paths remain inside the repository and the validation directory. Symlinks, non-regular files and paths outside that boundary refuse before truncation or append. Directory-component validation and descriptor checks prevent a symlinked parent from defeating a leaf-only check.

   Both opens use `O_NOFOLLOW`; shadow logging also uses `O_APPEND`. Regular-file checks apply to the opened descriptor. Shell `>` and `>>` redirections do not open these destinations. The JSON is schema-valid before it is committed to its destination. A write refusal holds and performs neither dispatch nor merge.

   On `hold`, the shadow log receives nothing, whether absent or already populated. A contained hold JSON may still be written when task and head are known.

   New verdict filenames use the full head; every shadow row retains the full head. No reservation or lock mechanism is introduced.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_opens_outputs_without_following_symlinks` plants a symlink separately at the JSON destination and shadow-log destination, requires refusal, and verifies each target's bytes remain unchanged. It includes escaping-parent and non-regular destination controls.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_shadow_does_not_append_on_hold` checks absent and populated logs and unchanged prior bytes. The existing successful shadow-column test remains green.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_output_names_use_the_full_head` checks the full-head JSON filename and shadow identity rather than accepting a seven-character output name.

4. **Security metadata is an explicit boolean.**

   Validate the parsed task's `security` value before selecting condition 8's branch. Missing, null or non-boolean values produce condition 8 failure, overall hold with exit 20, and the named reason `security must be an explicit boolean`. They never produce `not a security task`, append a shadow row, dispatch or merge.

   Only boolean `false` permits the no-security-review branch. Boolean `true` retains the required head-specific review, with front-matter `head:` exactly equal to the verdict's full 40-hex head. A quoted `"false"` is a string and does not exempt the task.

   `tests/unit/test_verdict.py::VerdictTest::test_verdict_rejects_evidence_for_another_full_head_with_the_same_sha7` uses two distinct 40-hex heads sharing their first seven characters. Separate subcases substitute the audit, security report, local review and saved or fresh sweep; each mismatched or absent full-head field holds despite a matching prefix and a correct security verdict. Full-head-matched controls remain green.

   Add these separate tests:

   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_missing`
   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_null`
   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_string`
   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_an_integer`
   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_float`
   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_list`
   - `tests/unit/test_verdict.py::VerdictTest::test_verdict_holds_when_security_is_a_mapping`

   Each test checks the named reason, hold and absence of application effects. The true and false positive controls remain in the retained condition tests. Unreadable or malformed YAML also holds.

## Caller inventory and ownership

At `6b7e7833`, executable verdict callers are the `--loop` child invocation in `scripts/orchestrator/verdict.sh` and the helpers and direct subprocess calls in `tests/unit/test_verdict.py`. Both files are in `allowed_files`. Update every ordinary call to the trusted-parent clean-prefix form with passwd-derived HOME and an absolute script path; the explicit dirty-environment and refusal tests remain the named exceptions.

There is no direct verdict invocation in the PR head's CI workflows and no separate tracked shadow-runner executable. CI exercises the updated test helper. This task's concrete shadow command below is the shadow runner. Do not add an unused wrapper or workflow step.

The orchestrator owns the follow-up connection in `scripts/orchestrator/chain-integrate.sh` and its local glue `.agents/worklog/orchestrator-glue/integrate-pr.sh`. Before either connects to verdict execution, the orchestrator applies the same trusted-parent clean-environment-before-exec contract with passwd-derived HOME and an absolute script path. Those files are not edited by a008. Any later direct CI or shadow caller follows that contract before use.

## Measured budget

The read-only command `git diff --numstat 3f240b12 6b7e7833` produced these relevant rows:

```text
11	0	.schemas/audit.json
10	0	.schemas/verdict.json
278	0	scripts/orchestrator/verdict.sh
399	0	tests/unit/test_verdict.py
```

The implementation budget is the measured 278 script lines plus Reset design estimates of 60 for startup and callers, 95 for fixed execution and verified consumption, 90 for contained writes, 20 for explicit security metadata, 20 for pasted-counter validation, 70 for GitHub changeset reads with single-pair and explicit repository binding, and 25 for full-head evidence binding, the measured 21 schema lines and 11 lines of reserve: `278 + 60 + 95 + 90 + 20 + 20 + 70 + 25 + 21 + 11 = 690`.

The test budget is the measured 399 lines plus corresponding estimates of 200, 130, 110, 60, 50, 95 and 60 (the startup estimate adds 60 for refusal, passwd-home and loader cases), 50 for every-call repository arguments, with 41 lines of reserve: `399 + 200 + 130 + 110 + 60 + 50 + 95 + 60 + 50 + 41 = 1195`. The startup and GitHub-read estimates include the no-application-path and differing-SHA regressions respectively.

These are cumulative PR ceilings, not targets. Changed lines mean additions plus deletions; fixture changes count. No behavior, validation, assertion or trust-boundary control is removed to meet them.

## Out of scope

Pool implementation, the audit wrapper, vocabulary ownership, `dispatch.sh`, record generation, `dispositions.py`, `--second-opinion`, `hold-playbook.sh`, `integrate-seat.sh`, gate and validator changes, task-checker implementation, Makefile targets, CI changes, model configuration, worker permission configuration and live deployment remain outside this task.

Application belongs to the later task `dotfiles-T133-verdict-apply-a01`, which is not written. That task owns its own prerequisites and four-distinct-PR agreement enforcement. This task has no application path and does not implement a dormant or prerequisite-gated `--apply` mode.

The four findings from the `6b7e7833` security review belong to this reset, including its two P2 findings. They are not assigned to an advisory owner. The a03 no-bytecode fix remains in scope as retained behavior.

## Check

Write the new regressions before their implementation changes. Record each new regression's red result against `6b7e7833a85528440dc397c2555bc9dd603c685a` and green result after the fix. A red result must reach its named defect; an unrelated startup or fixture failure is not evidence. Historical a01/a02/a03 red results retain their original references and do not replace new or final-head results.

The validation file contains commands, verbatim output, exit statuses and tested heads for `make unit-test`, `make render-check`, `make format`, `shellcheck scripts/orchestrator/verdict.sh`, `shfmt -i 4 -sr -d scripts/orchestrator/verdict.sh` and `uv run python -m unittest tests.unit.test_verdict -v`. The script checks are clean and the verdict module is green. Record the executable mode and exact shebang.

Run every Reset design selector, including all seven invalid-security tests, retain all sixteen inherited shadow behavior tests and run the no-application-path and differing-SHA regressions. Record the fixed executable realpaths, trusted interpreter and cache location without exposing credentials. Confirm that no executable-directory override remains in script or test source.

The concrete shadow invocation, issued by the trusted parent with a clean environment before exec, is `/usr/bin/env -i PATH=/usr/bin:/bin HOME=<passwd home> LANG=C.UTF-8 /bin/bash --noprofile --norc -p <repo>/scripts/orchestrator/verdict.sh --shadow 410 --task dotfiles-T133-verdict-audit-pool-a04`, where `<repo>` is the anchored absolute repository root and `<passwd home>` is the real uid’s passwd home. Its JSON, exit status, tested head and unchanged shadow-log state on hold appear in `.orchestration/dotfiles-T133-verdict-audit-pool-a04/validation.md`. Hold is expected before required audit and acceptance evidence exists. No live `--apply` is exercised.

`git diff --numstat --no-renames origin/main...HEAD` shows at most 690 changed lines outside `tests/` and `.orchestration/`, including both JSON schemas, with `verdict.sh` limited to 669 physical lines.

The cumulative test cap is 1195 under `tests/` over that same complete PR diff.

Report the implementation total, test total, script length and each schema's line count separately. An inherited check failure is reproduced against the unchanged base with the same command and environment and reported as a failure, never labelled passing or repaired outside scope. Local Bats tests remain unrun; GitHub Actions supplies their required results.

The orchestrator runs the format-2 task-consistency checker before dispatch and at acceptance, covering C1 to C10, C7b, the required C11 selector grammar and C18's design-by-reference requirement. It records the checker version and actual coverage; a version lacking a check is not evidence that the check passed. Every `closed` row is checked against its single concrete selector, including the class name.

The orchestrator performs the C-80 security-profile review of this task text and threat table before dispatch. Findings enter the class table and receive dispositions before a send. The orchestrator also performs the complete task-copy byte comparison and SHA256 check; these are not worker self-attestations.

The final inventory confirms the split remains intact, identifies preserved a03 evidence, shows the a03 task-copy deletion and a04 replacement, and accounts for every new or modified path against the declared boundary.

## Completion

One branch, `tools/verdict-audit-pool-a01`, continues PR #410 from the named a03 head. The first push contains the C3 task-copy replacement. The implementation, tests and historical evidence remain; no new implementation PR, branch or repeated parking operation is created.

The Completion clause of `.orchestration/tasks/dotfiles-T129-normalised-comparison-lint-a01.md` applies with this task's branch, reset boundary and live rules taking precedence, `dotfiles-T133-verdict-audit-pool-a05` as the advisory P2 owner, `task_copy=<sha256 of .orchestration/dotfiles-T133-verdict-audit-pool-a04/task.md>` and `parked_pr=407` in the RESULT. The orchestrator writes the advisory owner task before assigning an advisory disposition and records owned findings under its matching acceptance-record section.

There is one worker-side pre-push review round at most. Every worker fix round before or after the first RESULT counts toward INV-6 under C-61, including Bot-driven fixes. A pre-push fix followed by revise 1 exhausts the two-round allowance. Predecessor counters and stopped histories remain recorded; a reset does not erase them. A third finding of one class stops further rounds until the orchestrator records the required re-plan.

A P0/P1 surviving the allowed fix round is sent as `open:<id>` in the RESULT, including review-body and local/security finding identifiers. It stops the PR for the operator's decision. It is neither silently deferred nor converted to not-applicable to permit another worker round or merge. The worker resolves no review thread.

The report and RESULT identify head, base, branch, changed files, every feedback disposition, retained and added test names, code and test totals, schema counts, script length, task-copy hash, review-round counts and evidence paths. They distinguish historical evidence from final-head validation. Record actual Bot review events rather than inventing a re-review count.

Expected worker artifacts are `.orchestration/dotfiles-T133-verdict-audit-pool-a04/report.md`, `validation.md`, `sandbox.md`, `learning.md` and `autoskill.md`; revision instructions and selectors are also recorded in `revise.yaml`. Worker review evidence uses the required `-worker-` infix. Artifacts are written at those relative paths in `worker-f`; the RESULT states their placement, and the orchestrator copies required evidence by absolute path. Plan, todo and learn worklogs remain uncommitted.

This task is `security: true`. The orchestrator performs its final-head task-level audit and separate security-profile review before the integration gate. Final-head CI, the complete feedback sweep, dispositions, audit, acceptance record, gate and merge follow Orchestrator Playbook step 10 in its prescribed order. Changed heads receive fresh required evidence. Only the orchestrator performs `gh pr merge --repo mryfmo/dotfiles --squash --match-head-commit <audited head>` after the gate. PR #410 is integrated manually.

No `@codex review` comment is posted. Observe automatic review for the bounded window, read both review bodies and inline findings, and record absence after 15 minutes as `bot: none`. Wait for the required CI checks to pass before a ready-for-review RESULT. Any new push requires checking its CI again.

Every worker `gh pr`, `gh run` and `gh issue` command supplies `--repo mryfmo/dotfiles` or the full pull-request URL, and every worker `gh api` command supplies an explicit `repos/mryfmo/dotfiles/…` endpoint path with no `--repo` flag or repository placeholder; each gh command, Git write, push and fetch is an individual command inside the sandbox, without shell chaining or a wrapper combining commands. No excluded command, unsandboxed retry, API substitution or browser path bypasses a live boundary. Anything that cannot complete there produces `AGMSG-PONG v1 task_id=dotfiles-T133-verdict-audit-pool-a04 status=blocked` naming the exact command, exit status, output and boundary; preserve the available artifacts and wait for the orchestrator to re-task.

Until plan 024 P1-14 lands, strings containing `gh pr merge` or `gh pr create` are written through the file-edit tool, not shell commands, heredocs or shell wrappers. This writing rule grants no execution authority.

Live dispatch, merge and local Bats are not exercised. No application path exists in this task; the shared-UID residual remains as stated in the design.

## Checks (pasted by the orchestrator before each send)

```
(pasted at dispatch)
```