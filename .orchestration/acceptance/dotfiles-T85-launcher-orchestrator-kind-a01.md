# Acceptance: dotfiles-T85-launcher-orchestrator-kind-a01

- **Decision:** ACCEPTED. PR #270 squash-merged to `main` as `f2d4d709`; head `20361c5d19ca70548b27f1e0269cf5d8a7e1abf1`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, one evidence disposition below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 23:28Z).
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev matched at dispatch.
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** Phase 7, dotfiles-T85 (principle 4). Dispatched in parallel with T82 and T86 (disjoint files); the dependency on T84 is soft (the variable defaults to `claude` until T84 renders it).

## What was accepted (PR #270, head `20361c5d19ca70548b27f1e0269cf5d8a7e1abf1`; commits 5643ba22, f50e6af7, 4d210709, 20361c5d; 3 files, +258/−14)

- `executable_herdr-agents`: `resolve_orchestrator_kind` (env → `~/.agents/model-profiles.env` → `claude`; invalid value exits 2); under `codex`, full mode, `--attach` and `--restart-worker` exit 2 with `herdr-agents: orchestrator_kind=codex: use codex-orchestrate` before touching Herdr, while the manifest worker seat's own `--attach` keeps its quiet exit (`is_manifest_worker_seat`, now shared with the existing quiet-exit check; other linked worktrees are refused); `--add-worker`, `--remove-worker`, `--audit`, `--bootstrap-agmsg` work under either kind and resolve the leader under the kind's agmsg identity type (`claude-code` or `codex`); `--directive` prints the `agmsg-orchestration:` line for the repository's git top level without a Herdr server, nothing outside a regime repository.
- README: two paragraphs (refusal under `codex`; `--directive`).
- Tests: nine fake-CLI cases (refusal before Herdr, env/manifest resolution and validation, non-seating modes under `codex`, attach summary under `claude`, directive with and without Herdr and for a Codex identity, worker-seat quiet exit, other-worktree refusal, `--add-worker` naming under a Codex leader); 229 herdr-agents tests, 800 total; shfmt/shellcheck clean; `make validate-agent-assets` ok.

## Decisions taken during the task

- Codex threads, all replied and resolved by the orchestrator after confirming the fix commits are ancestors of the head: 4179583135 and 4179583130 `fixed:f50e6af7`; 4179629453 `fixed:4d210709`; 4179692403 and 4179692405 `fixed:20361c5d`; 4179583126 (render `orchestrator_kind` from the manifest) not applicable — T84's scope, forbidden here; 4179692400 (`codex-orchestrate` entrypoint) not applicable — T86, in flight in parallel; 4179731976 (Codex orchestrator delivery in `--bootstrap-agmsg`) not applicable — bootstrap is unchanged here; the Codex orchestrator's delivery and identity setup belong to T86's seat exchange (scope note sent to that task).

## Orchestrator re-derivation

- Read the launcher diff in full: the gate runs after kind resolution and before any `herdr` invocation; the only exemption is the manifest worker seat's `--attach`; every `identities.sh … claude-code` lookup for the leader now uses the kind's type; `--directive` resolves `git rev-parse --show-toplevel` first.
- CI 13/13 green on 20361c5d; PR `clean` after the eight resolutions; the final head's Bot review (23:13:45Z) raised only the T86-scope item.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 20361c5d | incorrect (1) → disposition below |

audit-finding: 1 the validation transcript labelled verbatim shows three usage lines before `rc=2` where the refusal path prints the full usage text → not-applicable:evidence-presentation finding; the asserted facts (exit 2 and the refusal message before any Herdr call) are reproduced by the fake-CLI tests in the diff and by the orchestrator's reading of the gate placement, and no product file is affected; the task's verbatim rule is restated to the worker in the acceptance

- Sweep (head 20361c5d): see the masked copy `.orchestration/validation/dotfiles-T85-launcher-orchestrator-kind-a01-pr-feedback.json`; five `fixed:` items, the rest `not-applicable`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Follow-ups

- T86 (in flight): the seat exchange must also set `delivery.sh set turn codex <repo>` for the Codex orchestrator identity and restore the Claude identity's delivery on exit (from thread 4179731976).
- T84: renders `HERDR_AGENTS_ORCHESTRATOR_KIND`; until then the launcher defaults to `claude`.

## CompactionDB

- Worker decision `d8bbd1c0-537b-49c9-a9a3-d7278a5be1f8`; orchestrator consolidation `8a4aa6af-7dbd-4d0b-aaf2-d9b5357c3c41`.
