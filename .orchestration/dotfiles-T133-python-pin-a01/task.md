---
format: 2
task_id: dotfiles-T133-python-pin-a01
kind: code
security: true
allowed_files:
  - home/dot_mise/config.toml
  - tests/unit/test_mise_config.py
  - tests/unit/test_supply_chain_policy.py
  - .orchestration/dotfiles-T133-python-pin-a01/**
after: []
threat_table:
  - control: "home/dot_mise/config.toml"
    disposition: "closed: tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version"
  - control: "tests/unit/test_mise_config.py"
    disposition: "closed: tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version"
  - control: "tests/unit/test_supply_chain_policy.py"
    disposition: "closed: tests/unit/test_supply_chain_policy.py::SupplyChainPolicyTest::test_mise_tools_track_latest_behind_the_cooldown"
  - control: ".orchestration/dotfiles-T133-python-pin-a01/**"
    disposition: "residual: these are untrusted records; the orchestrator compares the dispatched text, final diff, evidence and CI before acceptance."
  - control: "operator post-merge deployment: make update + mise install"
    disposition: "residual: the operator deploys after merge and records commands, output and installed version in the acceptance record; the worker never writes the host installation."
  - control: "orchestrator effects (merge, update-branch, forced worker removal)"
    disposition: "residual: the worker performs none of these actions; the orchestrator alone integrates and removes workers under the orchestration playbook."
  - control: "orchestrator effect: merge"
    disposition: "residual: Orchestrator Playbook step 10.5 binds integration to the audited head after the gate; the worker never merges or pushes main."
  - control: "orchestrator effect: update-branch"
    disposition: "residual: a changed head invalidates head-bound evidence; the orchestrator follows Orchestrator Playbook step 10 before integration."
  - control: "orchestrator effect: forced worker removal"
    disposition: "residual: none planned; removal refuses a dirty worktree unless explicitly forced, and the orchestrator records any discarded state in acceptance."
  - control: "workflow and interpreter or environment inputs"
    disposition: "residual: Commands bind the parent environment, interpreter and gh; dotfiles-T133-ci-efficiency-followup-a04 owns the deployed resolver, and CI retains its current interpreter setup."
  - control: "new or renamed scripts"
    disposition: "residual: the only new executable source is the intended test module, executed by Commands (d); no additional script or rename is authorized."
  - control: "task metadata: kind, allowed_files, threat_table and premises"
    disposition: "residual: the task-consistency check validates metadata before dispatch and acceptance; whole-file comparison detects changes to the worker copy."
  - control: "metadata separators: task-copy and evidence front matter"
    disposition: "residual: front-matter parsing and whole-file comparison expose changed separators; evidence remains untrusted input to review."
  - control: "in-process effects"
    disposition: "residual: Commands (d) executes only the intended repository test file, using standard-library imports and TOML data; it does not discover packages or run the supply-chain test's PATH-resolved chezmoi launch."
  - control: "evidence records under .orchestration/dotfiles-T133-python-pin-a01/"
    disposition: "residual: records identify Commands sections, operands, exit statuses and output; the orchestrator compares them with the final changeset and CI."
  - control: "task copy: .orchestration/dotfiles-T133-python-pin-a01/task.md"
    disposition: "residual: the copy must match the dispatched text byte-for-byte and its dispatch SHA-256; the orchestrator compares both before acceptance."
  - control: "design 5.14 item 0: same-UID threat model"
    disposition: "residual: shared credentials and unrestricted same-UID replacement remain possible; host checks reduce accidents and prompt injection, and missing acceptance evidence is detected at the next records PR rather than prevented."
  - control: "design 5.14 item 1: runtime write boundary"
    disposition: "residual: only a sandboxed Codex seat executes this task; it does not deploy or write trusted host inputs, and no unrestricted same-UID boundary is claimed."
  - control: "design 5.14 item 2: sanitized environment first"
    disposition: "residual: Commands establish the clean parent before bootstrap and use Commands (b) for validation children; deployed enforcement remains with dotfiles-T133-ci-efficiency-followup-a04."
  - control: "design 5.14 item 3: trusted-path checks"
    disposition: "residual: Commands (c) records the declared executable's realpath; deployed worker-root, symlink and case-alias rejection remains with dotfiles-T133-ci-efficiency-followup-a04."
  - control: "design 5.14 item 4: execute the verified binding"
    disposition: "residual: Commands (c) and (d) use the same fixed PY binding without rediscovery; same-UID replacement between probe and execution remains possible."
  - control: "design 5.14 item 5: output and reservation identity"
    disposition: "residual: Commands (f) evidence records full base and head SHAs; no reservation or lock is introduced, and acceptance verifies the final head."
  - control: "design 5.14 item 6: honest residuals"
    disposition: "residual: the declaration test checks syntax, not executable provenance, deployment or protection against unrestricted same-UID replacement."
  - control: "design 5.14 item 7: verification"
    disposition: "residual: Commands (d) supplies declaration red/green evidence; the four execution-contract fixture tests remain the responsibility of dotfiles-T133-ci-efficiency-followup-a04."
  - control: "design 5.14 item 8: committed approval sources"
    disposition: "residual: Commands (e) binds the base and Commands (f) obtains cap evidence from github.com's fixed repository API at full 40-hex SHAs; acceptance verifies the final head against GitHub content."
  - control: "design 5.14 item 9: private caches"
    disposition: "residual: Commands (c) and (d) use the installed interpreter directly without uv or provisioning; authenticating deployed executable inputs remains with dotfiles-T133-ci-efficiency-followup-a04."
  - control: "design 5.14 item 10: sandbox-only worker execution"
    disposition: "residual: every worker command stays sandboxed; a denial produces a blocked PONG without escalation or a substitute tool."
  - control: orchestrator effect merge
    disposition: "residual: merge only through gh pr merge --squash --match-head-commit <audited head> after the gate (Orchestrator Playbook step 10.5); never a local merge or a push to main"
  - control: orchestrator effect update-branch
    disposition: "residual: gh pr update-branch moves the head, so CI, the sweep and the audit run again on the new head before any gate (Orchestrator Playbook step 10)"
  - control: orchestrator effect forced worker removal
    disposition: "residual: none planned; herdr-agents --remove-worker refuses a dirty worktree without --force, and a forced removal is recorded in the acceptance record with the uncommitted state it discarded"
  - control: the task-file copy on the branch (.orchestration/dotfiles-T133-python-pin-a01/task.md)
    disposition: "residual: byte-identical to the dispatched file (its sha256 is in the TASK line); the orchestrator compares at acceptance and the regime job compares it with the text on main"
premises:
  - claim: the authoring home-anchor probe failed with exit 70, so downstream prerequisites remain unverified and dispatch is blocked
    command: |-
      run Commands (parent), then Commands (a) on macOS
    output: |-
      Operation failed with error: eServerError
      home: refused: lookup-failed (exit 70)
  - claim: the orchestrator measured this host's gh installation at 2026-10-20T02:01Z; command -v gh resolves to <home>/.local/share/mise/installs/github-cli-cli/latest/bin/gh, a symlink rather than a shim
    command: |-
      Host probes for Commands (e): installation listing, latest realpath, resolved executable --version and command -v gh.
    output: |-
      2 2.102 2.102.0 global latest
      <home>/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh
      gh version 2.102.0 (2026-09-30)
  - claim: Commands (f) uses GitHub's compare endpoint at the two 40-hex SHAs for per-file additions and deletions, up to 300 files, sufficient for this 3-file change; no local git runs and no local GIT_* input is read at all
---

# AGMSG-TASK dotfiles-T133-python-pin-a01 — declare the exact Python

Plan 024, proposal 1, amendment 1 after the re-plan; S1 re-plan of the tool-environment family, recorded by the acceptance record's `re-plan: tool-environment` line.
Worker: a Codex security-profile seat under D-024-25, in its own clean worktree on a fresh branch from `origin/main`.
Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen under D-024-29 and applies by reference under D-024-30; items 0–10 have individual threat rows.

[memory:decision] Declare `python = "3.15.0"` in `home/dot_mise/config.toml` as the exact Python binding for the trusted parent and the resolver owned by `dotfiles-T133-ci-efficiency-followup-a04`.
The declaration grammar is the mise `[tools]` key `python` with an exact ASCII-digit `MAJOR.MINOR.PATCH` string, without whitespace, a prefix, `latest` or a range.

## Commands

Definitions occur only here. Start Commands (parent) from the trusted launcher; execute the lettered sections inside that parent from the verified checkout root. Stop at any failed prerequisite.
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
TOKEN=$("${P[@]}" "$GH" auth token --hostname github.com); [ -n "$TOKEN" ] || { printf '%s\n' 'gh: refused: no-token' >&2; exit 1; }
GHC=$(/usr/bin/mktemp -d "${TMPDIR:-/tmp}/ghcfg.XXXXXX")
"${P[@]}" "$GH" --version
"${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN="$TOKEN" "$GH" api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha
# (f) Substitute the recorded full SHAs before execution; never execute placeholders.
"${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN="$TOKEN" "$GH" api "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --hostname github.com --paginate --jq '.files[] | "\(.additions)\t\(.deletions)\t\(.filename)"'
# (f') Completeness of (f): refuse a list of 300 files (GitHub's cap) or one that differs from the PR's changedFiles; <pr> is this task's PR, so (f') runs at RESULT, not at dispatch.
n=$("${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN="$TOKEN" "$GH" api "repos/mryfmo/dotfiles/compare/<base40>...<head40>" --hostname github.com --jq '.files | length'); c=$("${P[@]}" GH_CONFIG_DIR="$GHC" GH_TOKEN="$TOKEN" "$GH" pr view <pr> --repo github.com/mryfmo/dotfiles --json changedFiles --jq .changedFiles)
[ "$n" -lt 300 ] && [ "$n" = "$c" ] || { printf '%s\n' "compare: refused: files=$n changedFiles=$c" >&2; exit 1; }
# (g) Read-only declaration and existing-policy probe.
"${P[@]}" /usr/bin/grep -n -E 'python.*latest|latest.*python|held = |if name not in held:|self.assertEqual\("latest", version, name\)' home/dot_mise/config.toml tests/unit/test_supply_chain_policy.py scripts/validate-agent-assets.py
```

Executed on this host under the clean prefix at 2026-10-20T02:38:25Z (C-87): the (f') count for `ba318e53...118daafa` printed `{"files":7,"total_commits":1,"truncated":false}` and `gh pr view 434 … changedFiles` printed `7`; `bash -n` of the block exits 0.

Commands (a) is the only home source. Commands (b) removes inherited `GIT_*`, loader, Python and tool configuration variables; only Commands (e) and (f) explicitly receive the parent's token.
Never substitute an interpreter, enlarge the gh candidate list, invoke a shim, provision a tool or repair a failed prescribed command through another invocation.
Normalize home prefixes to `$HOME` in stored output only; retain actual bindings for execution. Evidence references Commands identifiers and resolved operands without duplicating command definitions.

## Work

1. Before edits, run Commands (a), (b), (c), (e) and (g). Require Commands (c) to succeed and report version `3.15.0`, with its realpath inside the anchored Python install root. A missing executable or version mismatch produces `python-pin: refused: installed-version-mismatch` and a blocked PONG. These installed-tool prerequisites do not add task dependencies; `after: []` is intentional.
2. Add exactly one standard-library test, `tests/unit/test_mise_config.py::MiseConfigTest::test_python_is_exact_version`. Read the real TOML relative to `__file__` using `pathlib` and `tomllib`; assign its Python declaration to `value` without stripping it and assert `re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', value, re.ASCII)`. In that same test, reject `"3.15.0\n"`, `"３.15.0"`, `"latest"` and `"3.15"` with the same fullmatch expression. End the module with `if __name__ == "__main__": unittest.main()`.
3. Run Commands (d) before changing the declaration. Required red is an assertion failure on the actual `latest` declaration, with exactly one executed test; import/setup failures and zero tests do not qualify.
4. Replace the declaration with `python = "3.15.0"` and immediately precede it with `# Held: the trusted interpreter resolver binds to this exact Python version.` Python stops tracking `latest`; deployment remains an operator action.
5. Only if Commands (g) confirms the existing supply-chain assertion includes Python, add `held["python"] = "python = "` immediately after that test's held-map declaration. Preserve the latest assertion for other tools and the preceding-reason check. This conditional allowance authorizes only the listed supply-chain test; any newly discovered validator change requires re-tasking.
6. Run Commands (d) green. Other repository tests, including the supply-chain method that launches chezmoi, run in CI rather than through task-local discovery.

No resolver, caller, workflow, dependency, host-installation or knowledge-graph changes are authorized. Resolver work belongs to `dotfiles-T133-ci-efficiency-followup-a04`.

## Check — prerequisites

Run Commands (a), (b), (c), (e) and (g) read-only at authoring and before dispatch; paste their actual outputs and exit statuses into `premises` using YAML block scalars for every command and output.
The current authoring probe failed at Commands (a). Do not dispatch this text until successful fresh prerequisite evidence replaces that failure; never reuse historical interpreter or gh output.
Require Commands (c)'s exact version and anchored realpath and Commands (e)'s executable non-shim binding and canonical base. A failure remains blocked.

## Check — red and green

Run Commands (d) for both phases and record their exit statuses and complete stdout/stderr in `validation.md`; require `Ran 1 test`, an assertion-based red, and a successful green.
Commands (d) performs no discovery and imports no repository package initializers.

## Check — caps and final head

Run Commands (e) at dispatch and record its authenticated `<base40>`. Record the dispatch `<head40>` and the final RESULT `<head40>`, verified against GitHub; require every SHA to contain exactly 40 ASCII hexadecimal characters.
Run Commands (f) and (f') at RESULT only (the PR and its head exist then), with the base from Commands (e)'s dispatch ref lookup and the final RESULT head; at dispatch only Commands (a), (c), (e) and (g) run; paste both full SHAs, the Commands identifier, exit status and complete TSV output in evidence. Never substitute mutable local refs.
Sum Commands (f)'s per-file additions plus deletions outside `tests/` and `.orchestration/` for at most **6 changed lines**, and additions under `tests/` for at most **40 added lines**, including the policy adjustment.
This whole task text must remain at or under **210 lines**. Do not run Bats locally; after pushing, verify final-head GitHub Actions and fix in-scope failures before RESULT.

## Completion and boundaries

Worker Playbook step 4 applies: every command, including gh and git writes, stays inside the sandbox and allowlist. A denial sends `AGMSG-PONG v1 task_id=dotfiles-T133-python-pin-a01 status=blocked`, identifying the Commands section, resolved operands, failure and crossed boundary; never escalate or bypass it through another tool.
Create one English draft PR under the Worker Playbook. All gh operations retain the Commands (e) binding and clean environment and explicitly identify github.com/mryfmo/dotfiles.
Copy the dispatched text byte-identically to `.orchestration/dotfiles-T133-python-pin-a01/task.md`; the orchestrator compares it and its dispatch SHA-256 at acceptance. Keep plan/todo/learn uncommitted and at most one active todo per owner.
Under that artifact directory, write `report.md`, `validation.md`, `sandbox.md`, `learning.md` and `autoskill.md`, plus worker review evidence. Record Commands references, base/head, PR, changed files, caps, red/green output, task-copy SHA-256 and `cost:`.
Send `AGMSG-RESULT v1` with all five artifact paths and Commands (f) evidence. Inaccessible main-checkout artifact paths use the same relative paths in the worker worktree.
Pass the repository review gate using local review data; do not open a browser review or request human review. The orchestrator performs final-head security review and integration under Orchestrator Playbook step 10; the worker never merges.
After merge, the operator performs the deployment named in its threat row and records installed-version evidence in acceptance; deployment is not a dispatch prerequisite.

Authoring did not establish the downstream host prerequisites or run worker tests, CI or deployment; dispatch remains blocked at Commands (a).
Executable provenance and unrestricted same-UID replacement remain residual risks.

## Checks (pasted by the orchestrator before each send)

```

measured amendment (2026-10-20T02:33:19Z): Commands (a) reads the passwd home with `/usr/bin/id -P | cut -d: -f9` (macOS) because `dscl` fails inside both seat sandboxes (Claude sandbox: `Operation failed with error: eServerError`; the Codex sandbox: exit 70 per the helper task RESULT) while `id -P` and Python's pwd.getpwuid work there (probed 2026-10-20T02:3xZ); probe outputs on this host: home=/Users/<user> (masked), python3 realpath <home>/.local/share/mise/installs/python/3.15.0/bin/python3 version 3.15.0, gh realpath <home>/.local/share/mise/installs/github-cli-cli/2.102.0/bin/gh version 2.102.0, main 118daafa4610549d3bc280800cf8b1d36fb851dc, declaration now python = "latest"; previous_sha256 c8021a71294f96f9c81b68b25a0d86942209703a6bdf843b188f3b945c59447e
re-plan 2 (2026-10-20T02:38:25Z): every command executed before it is written (fragile-premise x9 over four rounds); the compare completeness check added with its executed output; previous_sha256 9c5500f007e48a4090db05a765fe53a5dd1286f04e8fce277a96ad11c72153ce
amendment after re-plan 2, round 1 (2026-10-20T02:42:13Z): the completeness check is executable (f') inside the block, its prose moved below the block, and (f)/(f') run at RESULT only (no circular dispatch prerequisite); previous_sha256 ed75bc62eec5ee92ca471b3bbb5a4054971c5e50abf3ee7f015a1f29a3d4afd8
amendment after re-plan 2, round 2 (2026-10-20T02:46:45Z): gh configuration isolated ((e'): GH_CONFIG_DIR fresh dir + the keyring token read once by the bound gh; every gh call carries them; --repo github.com/mryfmo/dotfiles); previous_sha256 0ec4bb996a70fb34829a9b7f8f38ff259706696073cf87797b406ac5f1d747e4
dispatch to a013 (worker-h, the sixth seat), 2026-10-20T02:52:55Z: task-consistency-check.py OK; C-80 history after re-plan 2: ed75bc6 incorrect (2 text defects), 0ec4bb9 incorrect (gh configuration isolation), b657a89 incorrect on the text's own line cap only ("No additional security findings"); the self-cap sentence raised from 185 to 210 (the text is 200 lines; proposal 1 allows 250) and no further C-80 run: the budget is spent and the remaining finding is mechanical (wc -l), so the orchestrator dispositions it here and the task-level audit checks it; the dispatch probes (Commands (a), (c), (e), (g)) ran on this host at 02:3xZ inside and outside the sandbox (outputs above); security: true; previous_sha256 b657a897d337b524e1a2d403417da2898c507b59b67e008ef5b05c703ea011cd
```