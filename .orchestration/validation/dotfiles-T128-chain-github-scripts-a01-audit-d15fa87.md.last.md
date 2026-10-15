[P2] high implementation `scripts/orchestrator/resolve-threads.sh:65` A successful API call returning `false` still increments `resolved` and exits 0. A communication-free probe reproduced this. The declared test checks mutation requests but never checks their outcomes, so the thread-resolution row is not closed. Require `isResolved == true` before counting success.

[P2] high implementation `scripts/orchestrator/resolve-threads.sh:64` The API-provided thread ID is interpolated directly into GraphQL syntax. A malformed ID containing quotes can add an `addComment` mutation with a body outside the two permitted templates; an in-memory probe demonstrated that query construction. Use a GraphQL variable. This requires control of the API response; ordinary PR text cannot choose GitHub-assigned IDs.

[P2] high specification `.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01.md:61` The required reply templates omit the backticks that `scripts/orchestrator/fill_sweep.py:17` requires around dispositions. Consequently, a disposition obtained only from the sweep cannot be recovered from the generated reply when feedback is collected again. Both prescribed templates fail the existing parser. The contract and its tests need to cover this round trip.

[P2] high orchestration `.orchestration/validation/dotfiles-T128-chain-github-scripts-a01-pr-feedback.json:116` The unresolved response-checking defect is marked `not-applicable` solely because a follow-up owns it. That is deferral, which the standing integration rule prohibits. The follow-up is also absent from `origin/main`, making the owner-evidence command in `.orchestration/acceptance/dotfiles-T128-chain-github-scripts-a01.md:39` unreplayable.

Verified for [PR #356](https://github.com/mryfmo/dotfiles/pull/356):

- Both input hashes and the task-copy hash match. Positional arguments, first-100 query, table-before-sweep lookup, reply templates, truncation, missing/unknown-row exit 3, and dry-run behavior are preserved.
- `pr-cost.sh` retains the fields and single-header behavior. Its test covers those requirements. Stub keys correctly distinguish API paths and `--jq` expressions using post-filter answers, and distinguish GraphQL operations.
- All nine changed files are allowed; exactly two scripts were added. Bash syntax and ShellCheck checks pass.
- No examined input selects an arbitrary shell command. Fixed helpers additionally include `git`, `mkdir`, `date`, `/usr/bin/grep`, `wc`, `tr`, and `tail`; `uv` was removed. The GraphQL injection above prevents an unconditional guarantee about posted content.
- The premise holds. Saved feedback names the requested head and records 12 successful checks.

INV-2: holds `.orchestration/tasks/dotfiles-T128-chain-github-scripts-a01.md:73` — cited caps satisfied: 3 files outside orchestration records, 124 non-test changed lines, 193 added test lines.

Orchestration findings: 1

Not checked: live CI retrieval failed; full unit tests were not rerun under the read-only constraint. Probes used mocked commands and pipe-backed fd 3; no files changed.
Verdict: incorrect