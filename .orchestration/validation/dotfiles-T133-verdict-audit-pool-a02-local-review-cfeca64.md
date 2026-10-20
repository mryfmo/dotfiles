---
task: dotfiles-T133-verdict-audit-pool-a02
head: cfeca64a46426acb927c6e7b83958055c35df6d7
pr: 410
base: 3e41e36abc949acd7e6b4859c1a22df9e665c8d4
started: 2026-10-18T20:27:49Z
finished: 2026-10-18T20:36:50Z
findings: 4
engine: codex review --base main (profile review, read-only)
---

- [P1] Validate the decoded slot before arithmetic evaluation — scripts/orchestrator/audit-pool.sh:107-109
- [P2] Give the pool a worktree separate from integration — scripts/orchestrator/audit-pool.sh:108-110
- [P2] Mask the decoded audit JSON before retaining it — scripts/orchestrator/orch-audit.sh:168-171
- [P2] Refresh the trusted checkout between loop merges — scripts/orchestrator/verdict.sh:83-84

```text
The queue permits command execution through filenames, and JSON extraction can reintroduce masked secrets. Shared worktrees and stale checkouts also disrupt integration. Syntax checks and read-only reproductions passed; filesystem-writing tests were not run.

Full review comments:

- [P1] Validate the decoded slot before arithmetic evaluation — scripts/orchestrator/audit-pool.sh:107-109
  A request named `t BASH_VERSINFO[$(id >&2)0]+.request` makes the space-delimited picker result put filename text into `slot`. Bash evaluates that text in `((slot == 1))`, executing the embedded command before request-field validation. I reproduced this with a harmless marker. Reject malformed basenames and decode an unambiguous numeric slot before arithmetic; the pool's residual threat control does not mitigate this boundary ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Mask the decoded audit JSON before retaining it — scripts/orchestrator/orch-audit.sh:168-171
  If the fenced JSON contains an escaped sensitive string, such as a token prefix encoded as `\u0067hp_`, the Markdown masker misses it. The checker subsequently decodes the escape and writes the plaintext token into the retained JSON after masking has finished. An in-memory reproduction confirmed this. Apply the existing JSON-aware masker to the extracted document and revalidate it; the stated masking control currently misses this new artifact ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Give the pool a worktree separate from integration — scripts/orchestrator/audit-pool.sh:108-110
  When slot 1 is active, it occupies the same canonical worktree used by `orch-gate.sh` and `chain-integrate.sh`. Those wrappers require a clean tree, so the pool's active audit files prevent integration of an already completed PR. Overlapping checkout/cleanup operations can also reset or remove another operation's files because the queue lock does not coordinate these wrappers. Use pool-specific worktrees, including slot 1, or a shared lock covering their entire use.

- [P2] Refresh the trusted checkout between loop merges — scripts/orchestrator/verdict.sh:83-84
  With `--loop --apply`, merging a PR that changes `scripts/`, `.schemas/`, or `.orchestration/tasks/` makes the subsequent fetch advance `origin/main` while leaving this checkout unchanged. Every later child then fails the trusted-checkout equality guard, so subsequent ready PRs are refused while the loop still exits successfully. Safely refresh or restart the trusted checkout between merged PRs rather than only fetching.
The queue permits command execution through filenames, and JSON extraction can reintroduce masked secrets. Shared worktrees and stale checkouts also disrupt integration. Syntax checks and read-only reproductions passed; filesystem-writing tests were not run.

Full review comments:

- [P1] Validate the decoded slot before arithmetic evaluation — scripts/orchestrator/audit-pool.sh:107-109
  A request named `t BASH_VERSINFO[$(id >&2)0]+.request` makes the space-delimited picker result put filename text into `slot`. Bash evaluates that text in `((slot == 1))`, executing the embedded command before request-field validation. I reproduced this with a harmless marker. Reject malformed basenames and decode an unambiguous numeric slot before arithmetic; the pool's residual threat control does not mitigate this boundary ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Mask the decoded audit JSON before retaining it — scripts/orchestrator/orch-audit.sh:168-171
  If the fenced JSON contains an escaped sensitive string, such as a token prefix encoded as `\u0067hp_`, the Markdown masker misses it. The checker subsequently decodes the escape and writes the plaintext token into the retained JSON after masking has finished. An in-memory reproduction confirmed this. Apply the existing JSON-aware masker to the extracted document and revalidate it; the stated masking control currently misses this new artifact ([AGENTS.md:78](AGENTS.md#L78)).

- [P2] Give the pool a worktree separate from integration — scripts/orchestrator/audit-pool.sh:108-110
  When slot 1 is active, it occupies the same canonical worktree used by `orch-gate.sh` and `chain-integrate.sh`. Those wrappers require a clean tree, so the pool's active audit files prevent integration of an already completed PR. Overlapping checkout/cleanup operations can also reset or remove another operation's files because the queue lock does not coordinate these wrappers. Use pool-specific worktrees, including slot 1, or a shared lock covering their entire use.

- [P2] Refresh the trusted checkout between loop merges — scripts/orchestrator/verdict.sh:83-84
  With `--loop --apply`, merging a PR that changes `scripts/`, `.schemas/`, or `.orchestration/tasks/` makes the subsequent fetch advance `origin/main` while leaving this checkout unchanged. Every later child then fails the trusted-checkout equality guard, so subsequent ready PRs are refused while the loop still exits successfully. Safely refresh or restart the trusted checkout between merged PRs rather than only fetching.
```
