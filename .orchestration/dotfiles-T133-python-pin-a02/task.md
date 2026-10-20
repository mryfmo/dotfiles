---
format: 2
task_id: dotfiles-T133-python-pin-a02
reset_of: [dotfiles-T133-python-pin-a01]
kind: code
security: true
allowed_files:
  - home/dot_mise/config.toml
  - tests/unit/test_mise_config.py
  - .orchestration/dotfiles-T133-python-pin-a02/**
after: []
threat_table:
  - {control: "home/dot_mise/config.toml", disposition: "closed: tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version"}
  - {control: "tests/unit/test_mise_config.py", disposition: "closed: tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version"}
  - {control: ".orchestration/dotfiles-T133-python-pin-a02/**", disposition: "residual: these are untrusted records; the orchestrator compares the dispatched text, final diff, evidence and CI before acceptance."}
  - {control: "operator post-merge deployment: make update + mise install", disposition: "residual: the operator deploys after merge and records commands, output and installed version in the acceptance record; the worker never writes the host installation."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: Commands bind the parent environment, interpreter and gh; dotfiles-T133-ci-efficiency-followup-a04 owns the deployed resolver, and CI retains its current interpreter setup."}
  - {control: "new or renamed scripts", disposition: "residual: no new or renamed script is authorized; Commands (d) executes only the inherited intended test module."}
  - {control: "task metadata: kind, allowed_files, threat_table and premises", disposition: "residual: the task-consistency check validates metadata before dispatch and acceptance; whole-file comparison detects changes to the worker copy."}
  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input to review."}
  - {control: "in-process effects", disposition: "residual: Commands (d) executes only the intended repository test file, using standard-library imports and TOML data; it does not discover packages or run the supply-chain test's PATH-resolved chezmoi launch."}
  - {control: "evidence records under .orchestration/dotfiles-T133-python-pin-a02/", disposition: "residual: records identify Commands sections, operands, exit statuses and output; the orchestrator compares them with the final changeset and CI."}
  - {control: "task copy: .orchestration/dotfiles-T133-python-pin-a02/task.md", disposition: "residual: the copy must match the dispatched text byte-for-byte and its dispatch SHA-256; the orchestrator compares both before acceptance."}
  - {control: "predecessor copy: .orchestration/dotfiles-T133-python-pin-a01/task.md", disposition: "residual: unchanged on the branch at its a01 dispatched bytes (SHA-256 30185a5a…); regime-ci checks only the latest copy of a reset_of lineage, and the orchestrator compares the predecessor copy with the a01 dispatch at acceptance."}
  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: shared credentials and unrestricted same-UID replacement remain possible; host checks reduce accidents and prompt injection, and missing acceptance evidence is detected at the next records PR rather than prevented."}
  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: only a sandboxed Codex seat executes this task; it does not deploy or write trusted host inputs, and no unrestricted same-UID boundary is claimed."}
  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: Commands establish the clean parent before bootstrap and use Commands (b) for validation children; deployed enforcement remains with dotfiles-T133-ci-efficiency-followup-a04."}
  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: Commands (c) records the declared executable's realpath; deployed worker-root, symlink and case-alias rejection remains with dotfiles-T133-ci-efficiency-followup-a04."}
  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: Commands (c) and (d) use the same fixed PY binding without rediscovery; same-UID replacement between probe and execution remains possible."}
  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: Commands (f) evidence records full base and head SHAs; no reservation or lock is introduced, and acceptance verifies the final head."}
  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: the declaration test checks syntax, not executable provenance, deployment or protection against unrestricted same-UID replacement."}
  - {control: "design 5.14 item 7: 検証", disposition: "residual: Commands (d) supplies declaration red/green evidence; the four execution-contract fixture tests remain the responsibility of dotfiles-T133-ci-efficiency-followup-a04."}
  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: Commands (e) binds the base and Commands (f) obtains cap evidence from github.com's fixed repository API at full 40-hex SHAs; acceptance verifies the final head against GitHub content."}
  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: Commands (c) and (d) use the installed interpreter directly without uv or provisioning; authenticating deployed executable inputs remains with dotfiles-T133-ci-efficiency-followup-a04."}
  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: every worker command stays sandboxed; a denial produces a blocked PONG without escalation or a substitute tool."}
  - {control: "orchestrator effect merge", disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"}
  - {control: "orchestrator effect update-branch", disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"}
premises:
  - claim: "Commands (a), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      case "$(/usr/bin/uname -s)" in
        Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
        Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
        *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
      esac
      rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
      case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
    output: |-
      exit=0 home=$HOME
      absolute: yes
  - claim: "Commands (b), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" LANG=C.UTF-8)
    output: |-
      P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME=$HOME LANG=C.UTF-8)
  - claim: "Commands (c), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
      [ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python-pin: refused: missing-executable' >&2; exit 1; }
      "${P[@]}" "$PY" -I -c 'import sys, os; print(os.path.realpath(sys.executable), sys.version.split()[0])'
    output: |-
      exists+executable: yes
      $HOME/.local/share/mise/installs/python/3.15.0/bin/python3.15 3.15.0
      exit=0
  - claim: "Commands (e), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
      printf '%s\n' "$GH"
      case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
      [ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
      "${P[@]}" "$GH" --version
    output: |-
      GH=$HOME/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh
      shim-check: ok
      executable: yes
      gh version 2.102.0 (2026-09-30)
      exit=0
  - claim: "Commands (g), successfully probed read-only by the orchestrator at 2026-10-20T04:31:20Z against a01 sha 30185a5a…."
    command: |-
      "${P[@]}" /usr/bin/grep -n -E 'python.*latest|latest.*python|held = |if name not in held:|self.assertEqual\("latest", version, name\)' home/dot_mise/config.toml tests/unit/test_supply_chain_policy.py scripts/validate-agent-assets.py
    output: |-
      home/dot_mise/config.toml:5:python = "latest"
      tests/unit/test_supply_chain_policy.py:374:        held = {"fd": "fd = ", "npm:pnpm": '"npm:pnpm" = ', "http:bats": '[tools."http:bats"]'}
      tests/unit/test_supply_chain_policy.py:381:            if name not in held:
      tests/unit/test_supply_chain_policy.py:382:                self.assertEqual("latest", version, name)
      exit=0
---

# AGMSG-TASK dotfiles-T133-python-pin-a02 — reset the exact Python declaration

This text is the independent-context reset after INV-6 S2 (tasks=3 amendments=2 questions=1 results=5 revises=4, including round=0 blocked-RESULT closures); the a01 findings history is in `.orchestration/acceptance/dotfiles-T133-python-pin-a01.md`.
Plan 024; continue PR #437 on `task/dotfiles-T133-python-pin-a01` from `e9819d458b93bfba08352832be6b47f95780aeb8`, worker a013 (Codex, worker-h); do not create a branch or PR.
Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen under D-024-29 and applies by reference under D-024-30; items 0–10 have individual threat rows.
[memory:decision] Declare `python = "3.15.0"` in `home/dot_mise/config.toml` as the exact Python binding for the trusted parent and the resolver owned by `dotfiles-T133-ci-efficiency-followup-a04`.
The declaration grammar is the mise `[tools]` key `python` with an exact ASCII-digit `MAJOR.MINOR.PATCH` string, without whitespace, a prefix, `latest` or a range.

## Commands

Definitions occur only here; premises quote the executed probes. Start Commands (parent) from the trusted launcher; execute the lettered sections inside that parent from the verified checkout root. Stop at any failed prerequisite.
```bash
# (parent) Clear inherited inputs before starting the shell; never print the token.
/usr/bin/env -i PATH=/usr/bin:/bin LANG=C.UTF-8 /bin/bash --noprofile --norc -p -o pipefail
# (a) Anchor home to the real user's account record.
case "$(/usr/bin/uname -s)" in
  Darwin) home=$(/usr/bin/id -P | cut -d: -f9);;
  Linux) home=$(getent passwd "$(id -un)" | cut -d: -f6);;
  *) printf '%s\n' 'home: refused: unsupported-platform' >&2; exit 1;;
esac
rc=$?; [ "$rc" -eq 0 ] || { printf 'home: refused: lookup-failed (exit %s)\n' "$rc" >&2; exit "$rc"; }
case "$home" in /*) ;; *) printf '%s\n' 'home: refused: not-absolute' >&2; exit 1;; esac
# (b) The clean child prefix.
P=(/usr/bin/env -i PATH=/usr/bin:/bin HOME="$home" LANG=C.UTF-8)
# (c) Bind and probe the exact interpreter.
PY="$home/.local/share/mise/installs/python/3.15.0/bin/python3"
[ -f "$PY" ] && [ -x "$PY" ] || { printf '%s\n' 'python-pin: refused: missing-executable' >&2; exit 1; }
"${P[@]}" "$PY" -I -c 'import sys, os; print(os.path.realpath(sys.executable), sys.version.split()[0])'
# (d) Execute the intended file directly, for both red and green.
"${P[@]}" "$PY" -I tests/unit/test_mise_config.py
# (e) Bind gh, print and check the binding, then obtain the canonical base.
GH=$(/usr/bin/readlink -f "$home/.local/share/mise/installs/github-cli-cli/latest/bin/gh")
printf '%s\n' "$GH"
case "$GH" in ""|*/mise/shims/*) printf '%s\n' 'gh: refused: missing-or-shim' >&2; exit 1;; esac
[ -f "$GH" ] && [ -x "$GH" ] || { printf '%s\n' 'gh: refused: not-executable' >&2; exit 1; }
# (e') Isolate gh's persistent configuration (hosts.yml api_host can redirect requests): a fresh config dir and the keyring token read once by the bound gh.
GH_AUTH=$("${P[@]}" "$GH" auth token --hostname github.com); [ -n "$GH_AUTH" ] || { printf '%s\n' 'gh: refused: no-token' >&2; exit 1; }
GHC=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX")
"${P[@]}" "$GH" --version
"${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha
# (f) Substitute the recorded full SHAs before execution; never execute placeholders.
"${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --hostname github.com --paginate --jq '.files[] | "\(.additions)\t\(.deletions)\t\(.filename)"'
# (f') Completeness of (f): refuse a list of 300 files (GitHub's cap) or one that differs from the PR's changedFiles; <pr> is this task's PR, so (f') runs at RESULT, not at dispatch.
n=$("${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" api "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --hostname github.com --jq '.files | length'); c=$("${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN=$GH_AUTH "$GH" pr view <pr> --repo github.com/mryfmo/dotfiles --json changedFiles --jq .changedFiles)
[ "$n" -lt 300 ] && [ "$n" = "$c" ] || { printf '%s\n' "compare: refused: files=$n changedFiles=$c" >&2; exit 1; }
# (g) Read-only declaration and existing-policy probe.
"${P[@]}" /usr/bin/grep -n -E 'python.*latest|latest.*python|held = |if name not in held:|self.assertEqual\("latest", version, name\)' home/dot_mise/config.toml tests/unit/test_supply_chain_policy.py scripts/validate-agent-assets.py
```

Commands (a) is the only home source; (b) removes inherited tool, loader, Python and `GIT_*` configuration. Only the prescribed authenticated gh calls receive the parent's token.
Never substitute an interpreter, enlarge the gh candidate list, invoke a shim, provision a tool or repair a failed command through another invocation. Normalize home prefixes to `$HOME` only in stored output.

## Work

1. Continue the named head with implementation unchanged, including the inherited supply-chain Python exception; add only the new task copy and evidence under `.orchestration/dotfiles-T133-python-pin-a02/`. Preserve `.orchestration/dotfiles-T133-python-pin-a01/` as the predecessor copy.
2. Verify the inherited config is `python = "3.15.0"`, immediately preceded by `# Held: the trusted interpreter resolver binds to this exact Python version.` Python stops tracking `latest`; deployment remains an operator action.
3. Verify the single standard-library test `tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version` reads the real TOML relative to `__file__` using `pathlib` and `tomllib`, assigns the declaration to `value` without stripping, and asserts `re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', value, re.ASCII)`; the same expression rejects `"3.15.0\n"`, `"３.15.0"`, `"latest"` and `"3.15"`. The module ends with `if __name__ == "__main__": unittest.main()`.
4. Preserve the predecessor's Commands (d) assertion-based red on the actual `latest` declaration, exactly one test, with source/head provenance; do not undo the implementation to repeat it. Run Commands (d) green directly; record complete stdout/stderr and exit statuses in `validation.md`, distinguishing inherited red evidence from this execution.
5. No resolver, caller, workflow, dependency, host-installation, knowledge-graph or predecessor-artifact changes are authorized; newly discovered implementation work requires re-tasking.

## Check — prerequisites

The orchestrator executed the successful read-only Commands (a), (b), (c), (e) binding/version and (g) probes sequentially inside Commands (parent) before this dispatch at 2026-10-20T04:31:20Z; `premises` contains their exact commands and outputs.
Commands (d), (e') and (f)/(f') were not run in that probe: test execution, token read and PR compare belong to the worker/RESULT. The probed checkout's `latest` output is the source baseline, not the continued PR's implementation.
Before worker validation, repeat (a), (b), (c), (e)'s binding/version probe and (g); require version `3.15.0`, its realpath inside the anchored Python install root, and executable non-shim gh. A missing executable or version mismatch produces `python-pin: refused: installed-version-mismatch` and a blocked PONG; `after: []` adds no task dependency.

## Check — caps and final head

The worker runs Commands (e) and (e') at dispatch and records its authenticated canonical `<base40>`; record the initial and final `<head40>` verified against GitHub, each exactly 40 ASCII hexadecimal characters.
Run Commands (f) and (f') at RESULT with that dispatch base and final RESULT head; use PR 437, record both full SHAs, resolved operands, exit statuses and complete TSV output, and never substitute mutable local refs.
Sum Commands (f)'s per-file additions plus deletions outside `tests/` and `.orchestration/` for at most **6 changed lines**, and additions under `tests/` for at most **40 added lines**, including the inherited policy adjustment; measure the whole PR through the GitHub compare API.
This whole text must remain at or under **190 lines**. Commands (d) performs no discovery or repository-package imports; require `Ran 1 test` and green. Other tests run in CI; do not run Bats locally. After pushing, verify final-head GitHub Actions and report any failure without changing implementation.

## Completion and boundaries

Worker Playbook step 4 applies: every command, including gh and git writes, stays inside the sandbox and allowlist. A denial sends `AGMSG-PONG v1 task_id=dotfiles-T133-python-pin-a02 status=blocked` with the Commands section, resolved operands, failure and crossed boundary; never escalate or bypass through another tool.
All gh operations retain the Commands (e) binding and clean environment and explicitly identify github.com/mryfmo/dotfiles; continue the existing English PR under the Worker Playbook.
Copy this text byte-identically to `.orchestration/dotfiles-T133-python-pin-a02/task.md`; the orchestrator compares the whole copy and dispatch SHA-256 at acceptance. Keep plan/todo/learn uncommitted and at most one active todo per owner.
Under that directory, write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and worker review evidence; record Commands references, base/head, PR, changed files, caps, red/green provenance, task-copy SHA-256 and `cost:`.
Send `AGMSG-RESULT v1` with all five artifact paths and Commands (f)/(f') evidence; inaccessible main-checkout artifact paths use the same relative paths in the worker worktree.
Pass the repository review gate with local review data; never open a browser review or request human review. The orchestrator performs final-head security review and integration under Orchestrator Playbook step 10; the worker never merges.
After merge, the operator runs `make update` and `mise install`, recording commands, output and installed-version evidence in acceptance; deployment is not a dispatch prerequisite.
Not performed by this authoring context: worker tests, CI or deployment. Executable provenance and unrestricted same-UID replacement remain residual risks.

## Checks (pasted by the orchestrator before each send)

```
pasted 2026-10-20T04:49Z before send 1 to a013 (Codex, worker-h): reset of dotfiles-T133-python-pin-a01 after INV-6 S2 (a01 counters at 04:31Z: tasks=3 amendments=2 questions=1 results=5 revises=4; audit e9819d4 P1); task-consistency-check.py OK (C3 predecessor-copy row present); validate-agent-assets.py SECRET_PATTERN 0; bash -n OK; literal home paths 0; 176 lines (self cap 190)
C-80 round 1 of this text: 68fd5f2 `Verdict: correct`; the probes in premises were executed read-only by the orchestrator at 2026-10-20T04:31:20Z (Commands (a),(b),(c),(e),(g)); PR #437 continues on task/dotfiles-T133-python-pin-a01 from head e9819d45 (implementation 09c81cc3 unchanged); the a01 copy stays as the predecessor copy
this text's counters at paste: task=dotfiles-T133-python-pin-a02 tasks=0 amendments=0 questions=0 results=0 withdrawn=0 revises=0 first_result_head=none bot_p1_heads_after_result=unknown audits=unknown wall=none..none (-) source=li; task SHA256 in the AGMSG-TASK line, computed over these final bytes; the read marker is recorded in the acceptance record
```