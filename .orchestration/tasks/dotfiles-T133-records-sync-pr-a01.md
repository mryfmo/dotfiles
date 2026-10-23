---
format: 2
task_id: dotfiles-T133-records-sync-pr-a01
kind: code
security: true
allowed_files:
  - scripts/orchestrator/records-sync.py
  - tests/unit/test_records_sync.py
  - .orchestration/dotfiles-T133-records-sync-pr-a01/**
after: []
threat_table:
  - {control: "scripts/orchestrator/records-sync.py", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_happy_path"}
  - {control: "tests/unit/test_records_sync.py", disposition: "residual: temporary stores and fake gh exercise production code without contacting GitHub; the audit checks assertions and captured requests."}
  - {control: ".orchestration/dotfiles-T133-records-sync-pr-a01/**", disposition: "residual: untrusted task records only; the orchestrator checks the complete diff and rejects executable payloads."}
  - {control: "task copy .orchestration/dotfiles-T133-records-sync-pr-a01/task.md", disposition: "residual: compare every byte and SHA-256 with this amendment's dispatched text at acceptance."}
  - {control: "evidence records report.md, validation.md, sandbox.md, learning.md and autoskill.md", disposition: "residual: compare claims with complete command output, the final diff and final-head CI before acceptance."}
  - {control: "task metadata", disposition: "residual: task-consistency checks precede dispatch and acceptance; whole-copy comparison detects metadata changes."}
  - {control: "metadata separators", disposition: "residual: parse the first YAML document and compare the complete dispatched bytes, including separators."}
  - {control: "in-process effects", disposition: "residual: production proposes records through the fixed GitHub repository; development executes fixtures only and performs no live sync."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: Commands binds the clean parent, fixed interpreter and gh; no workflow, permission policy or installed executable may be edited."}
  - {control: "new or renamed scripts", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"}
  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: shared credentials and unrestricted same-UID replacement remain; damage suppression and next-records-PR detection do not constitute prevention."}
  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: verify the actual Darwin seat sandbox before dispatch; no isolation from unrestricted same-UID processes is claimed."}
  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"}
  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"}
  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_replaced_input"}
  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: serialize each suffix, record full 40-hex heads and use non-forced updates; suffixes confer no approval or merge-slot reservation."}
  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: bus sender/hash checks detect stale bytes but cannot authenticate a store writable by the same UID."}
  - {control: "design 5.14 item 7: 検証", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_trusted_exec_contract"}
  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: canonical main and objects come from the host/repository-bound API at full SHAs; task texts and bus rows authorize no merge or permission."}
  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: use the exact installed interpreter with -I and stdlib only; no uv, provisioning, shell storage layer or shim execution."}
  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: Darwin gh calls remain sandboxed; unavailable isolation or any refused command yields a blocked PONG, with no escalation."}
  - {control: "orchestrator effect merge", disposition: "residual: the script and worker never merge or enable auto-merge; the orchestrator retains approval and final-head integration authority."}
  - {control: "orchestrator effect update-branch", disposition: "residual: only the orchestrator updates an implementation PR; any head change requires fresh CI, feedback and audit before integration."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: none requested; removal stays with herdr-agents and any forced discard is recorded by the orchestrator."}
  - {control: "token in the environment", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_token_environment"}
  - {control: "GitHub API as the only write path", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_api_only"}
  - {control: "agmsg store read", disposition: "closed: tests/unit/test_records_sync.py::RecordsSyncTest::test_dispatch_rows"}
premises:
  - claim: "The renderer appends the gh exclusion only on Linux; active sandbox availability still needs a dispatch check."
    command: |-
      /usr/bin/sed -n '387,388p' scripts/generate-agent-configs.py
    output: |-
              "excludedCommands": sandbox["excludedCommands"]
              + (sandbox.get("linux_excluded_commands", []) if os_name == "linux" else []),
  - claim: "The chezmoi manifest supplies the Git identity's name and email."
    command: |-
      /usr/bin/sed -n '47,49p' home/.chezmoi.yaml.tmpl
    output: |-
      data:
          email: {{ $email | quote }}
          name: {{ $name | quote }}
  - claim: "This authoring host is Darwin; executable and seat checks must be repeated before dispatch."
    command: |-
      /usr/bin/uname -s
    output: |-
      Darwin
---

# AGMSG-TASK dotfiles-T133-records-sync-pr-a01 — amendment 1: records synchronization through GitHub

Read the complete C-80 round 1 at `.orchestration/validation/dotfiles-T133-records-sync-pr-a01-text-security-801ad66.md.last.md` and mistake M-20261020-02. This amendment replaces the complete original text. Frozen design `.orchestration/plans/024-design-quality.md` 5.14 items 0–10 applies by reference (D-024-29/30).
Implement `scripts/orchestrator/records-sync.py <branch-suffix> <task-id>...` with Python stdlib under Commands' trusted interpreter. No shell wrapper, local git invocation, checkout, staging, push, worktree or sourced storage code exists in the records-sync runtime.
The orchestrator supplies nonempty `RECORDS_SYNC_NAME` and `RECORDS_SYNC_EMAIL` from the chezmoi manifest's `data.name` and `data.email`; use that identity for both author and committer, never local Git configuration. Reject control characters in either value.

## Commands

Definitions occur only here. The trusted launcher supplies the manifest identity; enter (parent) before other processing. Run from the verified checkout root; stop at every failed prerequisite. Never enable tracing or print credentials.
```bash
# (parent) Preserve only the sandbox proxy, temporary-directory and declared identity inputs.
/usr/bin/env -i PATH=/usr/bin:/bin TMPDIR="${TMPDIR:-/tmp}" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8 RECORDS_SYNC_NAME="${RECORDS_SYNC_NAME:?manifest name required}" RECORDS_SYNC_EMAIL="${RECORDS_SYNC_EMAIL:?manifest email required}" /bin/bash --noprofile --norc -p -o pipefail
# (a) Darwin only; obtain home from the account record.
case "$(/usr/bin/uname -s)" in Darwin) home=$(/usr/bin/id -P | cut -d: -f9);; *) printf '%s\n' 'records-sync: refused: Darwin required' >&2; exit 2;; esac || exit 2
case "$home" in /*) ;; *) exit 2;; esac
P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" TMPDIR="$TMPDIR" HTTPS_PROXY="${HTTPS_PROXY-}" HTTP_PROXY="${HTTP_PROXY-}" NO_PROXY="${NO_PROXY-}" LANG=C.UTF-8)
# (b) Bind and verify the exact interpreter, then the installed gh.
PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
[ -f "$PY" ] && [ -x "$PY" ] || exit 2
"${P[@]}" "$PY" -I -c 'import os,sys; p=os.path.realpath(sys.executable); r=os.path.realpath(os.environ["HOME"]+"/.local/share/mise/installs/python/3.15.0"); assert sys.version_info[:3]==(3,15,0) and os.path.commonpath([p,r])==r; print("python=3.15.0 binding=ok")' || exit 2
GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
case "$GH" in ""|*/mise/shims/*) exit 2;; esac
[ -f "$GH" ] && [ -x "$GH" ] || exit 2
case "$GH" in "$home"/.local/share/mise/installs/github-cli-cli/*/bin/gh) ;; *) exit 2;; esac
# (c) Read the keyring token once; this bootstrap alone reads the existing gh configuration.
GH_AUTH=$("${P[@]}" "$GH" auth token --hostname github.com) || exit 2
[ -n "$GH_AUTH" ] || exit 2
GH_CONFIG_DIR=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX") || exit 2
# (d) Carry the token by descriptor into a clean child, then only by environment, never argv.
with_token() {
  "${P[@]}" GH_CONFIG_DIR="$GH_CONFIG_DIR" RECORDS_SYNC_GH="$GH" RECORDS_SYNC_NAME="$RECORDS_SYNC_NAME" RECORDS_SYNC_EMAIL="$RECORDS_SYNC_EMAIL" /bin/bash --noprofile --norc -p -c 'IFS= read -r GH_AUTH <&3 || exit 2; exec 3<&-; export GH_TOKEN=$GH_AUTH; exec "$@"' token-env "$@" 3<<<"$GH_AUTH"
}
# (e) Unit tests, red before implementation and green after; fixtures never use the live token.
"${P[@]}" "$PY" -I tests/unit/test_records_sync.py
# (f) Authenticated base and final-head cap evidence; bind real operands before the latter.
with_token "$GH" api --hostname github.com repos/mryfmo/dotfiles/git/ref/heads/main --jq .object.sha
with_token "$GH" api --hostname github.com "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --paginate --jq '.files[] | "\(.additions)\t\(.deletions)\t\(.filename)"'
with_token "$GH" api --hostname github.com "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --jq '.files | length'
with_token "$GH" pr view "<pr>" --repo github.com/mryfmo/dotfiles --json headRefOid,changedFiles
# (g) Define the production invocation; the worker does not execute a live sync.
records_sync() { with_token "$PY" -I scripts/orchestrator/records-sync.py "$@"; }
```

All post-bootstrap gh commands use (d), the fresh configuration and token environment; production uses the equivalent explicit subprocess environment, with no token in argv, logs or errors. Run gh with cwd set to that empty config directory so repository discovery cannot load local configuration. No other executable discovery or provisioning is allowed.
The orchestrator verifies an active, available seat sandbox and no applicable gh exclusion before dispatch. This host is Darwin, where Claude seats run gh inside the sandbox (design 5.14 item 10); the current manifest's Linux-only `gh *` exclusion does not apply and is being removed by P1-15. Record `/usr/bin/uname -s` and every command in sandbox.md; any refused command produces `AGMSG-PONG v1 task_id=dotfiles-T133-records-sync-pr-a01 status=blocked`, without escalation or an alternate tool. `after: []` waives no runtime prerequisite.

## Work

1. Require a suffix and one or more unique task ids, each matching ASCII `[A-Za-z0-9][A-Za-z0-9_-]*` in full. Resolve the anchored checkout and named regular `.orchestration/tasks/<id>.md` files; refuse symlink escapes and trusted paths under `.claude/worktrees/` or manifest worker roots. Read each file once into immutable bytes; reject literal home paths matching `/(?:Users|home)/[^/\s]+` without masking or rewriting bytes.
2. Use the trusted interpreter's sqlite3 module only: `sqlite3.connect("file:" + path + "?mode=ro", uri=True)` for the canonical passwd-home agmsg `messages.db` (URI-escape the pathname first). Parameterize the query: `SELECT body FROM messages WHERE from_agent='claude-deep-dot' AND body LIKE ? ESCAPE '!' ORDER BY id DESC LIMIT 1`; bind the pattern `AGMSG-TASK v1 task_id=<id> %`, escaping each id underscore as `!_`. Require exactly one exact task-id token and one `task_sha256=<64 hex>` token in that newest row; never fall back to older rows or another sender.
3. Compare its full SHA-256 with the captured bytes. A missing/malformed row or mismatch exits 2 naming the task, `dispatched=<hash-or-missing/invalid>` and `local=<hash>`; unreadable files/store, invalid inputs and home-path refusals also exit 2 before any API write. Validate all tasks first. Recheck the latest dispatch hashes before publishing the ref; changed dispatch data refuses publication. Never reopen mutable source files to build blobs.
4. Consume `RECORDS_SYNC_GH` as Commands' validated realpath, require the fixed anchored install binding, and execute that same path throughout; reject shims, caller-selected tool directories, forged HOME and worker-root trusted inputs. Every API invocation is that bound `gh api --hostname github.com repos/mryfmo/dotfiles/...` with an explicit method; write payloads are JSON on stdin (`--input -`), never shell text. Validate every returned or interpolated object SHA as exactly 40 ASCII hex characters.
5. GET `git/ref/heads/main` for `<main40>`, then GET `git/commits/<main40>` for its tree. Inspect only `refs/heads/records/sync-dispatched-texts-<suffix>`; an existing ref must pass GET `compare/main...<ref>` with `behind_by == 0`. Pin/check its base and existing head against the captured full SHAs, using `compare/<main40>...<ref40>` for the authoritative check; a moved or non-descendant ref refuses before API writes. Only an actual not-found result means absent; other query errors fail closed.
6. For each captured text POST `git/blobs` with its bytes base64-encoded and `encoding: base64`. Require the returned SHA to equal Python's `hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()`; any mismatch exits 2 before tree, commit, ref or PR creation.
7. POST `git/trees` with `base_tree` equal to main's tree and exactly one `{path: .orchestration/tasks/<id>.md, mode: "100644", type: "blob", sha: <verified-blob40>}` entry per named text. No task-copy path or unrelated record is included.
8. POST `git/commits` with that tree, `parents: [<main40>]`, author and committer from the declared identity, and an English Conventional Commit message listing every text and its first 12 SHA-256 digits. Reuse an existing head whose tree already equals the desired tree, refreshing its PR body without an empty commit; if main already has the desired tree and no proposal is needed, report already synchronized.
9. POST `git/refs` for the exact proposal ref, or PATCH `git/refs/heads/records/sync-dispatched-texts-<suffix>` with `force: false` when it exists. A racing ref creation or non-fast-forward fails closed; never force, delete, reset, retry against another branch or write main. Print the full proposal head; serialization by suffix remains an orchestrator duty.
10. Query the fixed repository for that branch's open PR, treating query failures as failures and ambiguous results as refusals. Create with `gh pr create --repo github.com/mryfmo/dotfiles --base main --head records/sync-dispatched-texts-<suffix>` plus explicit English title and `--body-file`, or update its body with `gh pr edit <n> --repo github.com/mryfmo/dotfiles --body-file <file>`. The English body contains a Markdown table headed `Text | SHA-256 prefix`, every named text and its 12-digit prefix, and exactly `This PR is records-only.` Print its URL and full 40-hex head; never merge, auto-merge or update any other branch.

## Check

Write `tests/unit/test_records_sync.py` ending in `unittest.main()` with `RecordsSyncTest`. Use a fake gh script recording argv, stdin, cwd and redacted environment and returning canned JSON, plus a Python-built temporary SQLite store. No fake sqlite3 CLI, real git, network, keychain access or production executable override is permitted; bind temporary paths/fake gh only within test fixtures.
Include `test_sha_mismatch`, `test_missing_row`, `test_home_path`, `test_blob_sha_binding`, `test_non_descendant_ref`, `test_happy_path`, `test_body_table`, `test_reuse`, `test_bad_arguments`, `test_host_binding`, `test_dispatch_rows`, `test_replaced_input`, `test_trusted_exec_contract`, `test_token_environment` and `test_api_only`.
Assert exit 2 and both hash fields for mismatches/missing rows, with no API write; cover newest amendments, wrong senders, malformed/duplicate hashes, exact ids including underscores, multiple tasks, invalid arguments, both home-path forms and symlink escapes. Assert a bad blob SHA prevents later writes and a non-descendant ref is never moved.
Happy-path assertions check the fixed host/repository and API sequence, blob bytes/hash, exactly the named 100644 tree entries, main parent, manifest identity, complete message/body table/sentence, non-forced ref, URL/head and absence of merge. Cover existing-PR edits, unchanged reuse, API/query failures and non-fast-forward refusal.
The contract tests plant hostile PATH shims, GIT_* values, filter/rewrite configuration, GH_HOST/hosts.yml and SQLite startup configuration; none executes or redirects a call. Cover worker-root trust-path refusal, source replacement after validation (only captured verified bytes may be sent), changed dispatch data before publication, and token absence from argv/stdout/stderr. Reuse the shared contract helper if present without expanding allowed_files.
Run Commands (e) red while the production script is absent, then green after implementation; preserve both complete runs, selectors, source provenance and exit statuses. No Bats locally. Use the existing Ruff CI checks; verify final-head GitHub Actions after every push and fix in-scope failures before RESULT.
Caps are additions plus deletions: at most **180 changed lines outside tests/ and .orchestration/** and **320 changed lines under tests/**. Record Commands (f)'s authenticated dispatch base, final GitHub head, complete numstat-equivalent output and sums; refuse 300-file truncation or a file count differing from the PR's changedFiles. This complete task text is at most **160 lines**.

## Completion

Deliver on a fresh `tools/records-sync-pr-a01` implementation branch under the Worker Playbook, using the existing worker seat; no live records-sync run is required. The runtime's only writes are GitHub API/PR operations and temporary PR-body/config files, never local repository state.
Keep `.orchestration/dotfiles-T133-records-sync-pr-a01/task.md` byte-identical to this dispatch. Store report.md, validation.md, sandbox.md, learning.md, autoskill.md and worker review data beside it; record Commands references, full base/head, PR, cap sums, red/green runs, task-copy SHA-256, refusals, AutoSkill status and `cost:`. Keep plan/todo/learn uncommitted with at most one active todo per owner.
Pass the repository review gate with read local review data and a receipt; never open Crit web UI or request human review. Follow Worker Playbook step 15 and send `AGMSG-RESULT v1 task_id=dotfiles-T133-records-sync-pr-a01 status=ready_for_review pr=<url> head=<40-hex> task_copy=<sha256>` with all artifact paths. The orchestrator performs final-head security audit and integration in Orchestrator Playbook step 10; the worker never merges.
Not run by this authoring context: implementation tests, live sync, CI or deployment. Residual risks are unrestricted same-UID replacement and shared credentials; bus hashes supply no approval authority.

## Checks (pasted by the orchestrator before each send)

```
```
