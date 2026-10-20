---
task: dotfiles-T133-result-precheck-a01
head: a5cb73b489235bb177e346dd00dd9aca28a432e8
pr: 411
base: 99a4a80f5a5b32a70cf7eb4f4d0db5a02d113841
started: 2026-10-18T07:00:53Z
finished: 2026-10-18T07:07:55Z
findings: 3
engine: codex review --base main (profile review, read-only)
---

- [P1] Scan text content even when Git marks its diff as binary — .githooks/pre-push:19-20
- [P2] Propagate diff errors instead of recording successful checks — scripts/orchestrator/result-precheck.sh:173-174
- [P2] Reject missing and non-boolean check results — scripts/orchestrator/dispatch.sh:188-190

```text
Secret scanning can omit credential-bearing content, and precheck enforcement can accept incomplete records or failed prerequisites. Validation used read-only probes; full test suites were not run.

Full review comments:

- [P1] Scan text content even when Git marks its diff as binary — .githooks/pre-push:19-20
  If a pushed textual credential file has a matching `-diff` or `binary` attribute, this command emits only `Binary files ... differ`. The secret detector therefore sees no credential content and permits the push. The same omission affects `check_secrets` in `result-precheck.sh`. Force text output or scan text blobs independently of diff attributes, and cover this case in the closed hook control required by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Reject missing and non-boolean check results — scripts/orchestrator/dispatch.sh:188-190
  A correctly hashed record containing `checks=[{}]`, `ok: null` for unit tests, or only an unrelated successful check passes this validation. Consequently, `PRECHECK_REQUIRED=1` can send acceptance without evidence that the required checks succeeded. Require the expected checks and boolean success for executed checks, permitting null only for explicitly deferred local review; add malformed-record cases to the closed dispatch control required by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Propagate diff errors instead of recording successful checks — scripts/orchestrator/result-precheck.sh:173-174
  When `origin/main` is unavailable or no merge base exists, `git diff` fails after creating an empty output file. Because `run_check` invokes this function on the left of `||`, Bash disables `set -e` throughout the function; scanning the empty file then succeeds and records `secrets` as passing. `check_shellcheck` similarly accepts a failed diff as an empty scope. Explicitly propagate these Git failures so missing prerequisites cannot produce successful precheck evidence.
Secret scanning can omit credential-bearing content, and precheck enforcement can accept incomplete records or failed prerequisites. Validation used read-only probes; full test suites were not run.

Full review comments:

- [P1] Scan text content even when Git marks its diff as binary — .githooks/pre-push:19-20
  If a pushed textual credential file has a matching `-diff` or `binary` attribute, this command emits only `Binary files ... differ`. The secret detector therefore sees no credential content and permits the push. The same omission affects `check_secrets` in `result-precheck.sh`. Force text output or scan text blobs independently of diff attributes, and cover this case in the closed hook control required by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Reject missing and non-boolean check results — scripts/orchestrator/dispatch.sh:188-190
  A correctly hashed record containing `checks=[{}]`, `ok: null` for unit tests, or only an unrelated successful check passes this validation. Consequently, `PRECHECK_REQUIRED=1` can send acceptance without evidence that the required checks succeeded. Require the expected checks and boolean success for executed checks, permitting null only for explicitly deferred local review; add malformed-record cases to the closed dispatch control required by [AGENTS.md:78](AGENTS.md#L78).

- [P2] Propagate diff errors instead of recording successful checks — scripts/orchestrator/result-precheck.sh:173-174
  When `origin/main` is unavailable or no merge base exists, `git diff` fails after creating an empty output file. Because `run_check` invokes this function on the left of `||`, Bash disables `set -e` throughout the function; scanning the empty file then succeeds and records `secrets` as passing. `check_shellcheck` similarly accepts a failed diff as an empty scope. Explicitly propagate these Git failures so missing prerequisites cannot produce successful precheck evidence.
```
