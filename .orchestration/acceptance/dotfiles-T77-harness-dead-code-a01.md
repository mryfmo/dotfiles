# Acceptance: dotfiles-T77-harness-dead-code-a01

- **Decision:** ACCEPTED (gate passed 2026-10-04 16:27Z); merge held until PR #258 (T97) merges, as promised to its worker. PR #260 squash-merged to `main` as `67451fc6`; head `977bdf1f757fec64ebc732dead4f55a69ad745a3`.
- **Worker:** `claude-standard-dot-a006` (worker-d, wY:p2). task_rev matched at dispatch and after the PONG-decision append.
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** Phase 4, dotfiles-T77 (principle 9). Depends on T70 (merged); serialized after T72/T76/T96 on the shared validator and manifest.

## What was accepted (PR #260, head `977bdf1f757fec64ebc732dead4f55a69ad745a3`; commits 6f8b5683, 977bdf1f; 17 files, +26/−958)

- Deleted: `herdr()` zsh wrapper and `executable_herdr-session`; `executable_agent-fanout` with its validator tokens, the `require-crit-review.py` path entry, the runtime-health tests and the `model-profiles.env` header mention (via the generator comment); `report_ccr_adoption_gates` and its phase in `upgrade-tools.sh` with the two tests and the `gh` stub arms; the deprecated `HERDR_AGENTS_CODEX_PROFILE` alias in `herdr-agents` (validator now requires `HERDR_AGENTS_WORKER_PROFILE`); `archive/CompactionDB-2.0.0.zip` (manifest note now points at `vendor/compactiondb`); the README paragraphs for all of these.
- `home/.chezmoiremove` lists `.local/bin/common/herdr-session` and `.local/bin/common/agent-fanout`, so the deployed copies disappear on the next apply (Codex P2 4178373800, fixed 977bdf1f; `tests/unit/test_chezmoiremove_agmsg.py` pins both).
- Tests: 18 removed with their subjects (7 runtime-health, 11 herdr-agents), none added (the `RETIRED` tuple in `test_chezmoiremove_agmsg.py` gains the two entries); 773 pass; `make render-check` clean; `make validate-agent-assets` ok.

## Decisions taken during the task

- Routing: item 5 (`home/dot_claude/hooks/executable_enforce-uv.sh`, a Claude PreToolUse hook) is a Claude seat's own execution boundary, so it was excluded at dispatch and goes to a Codex seat as T77b; the `[memory:decision]` was recorded without the enforce-uv clause (`fd9cacff`).
- PONG decision: `home/.chezmoiremove` and its test allowed in the same PR.
- Out of scope, left as reported: `.gitignore:10` (`.agents/runs/`, agent-fanout's output dir) and the `plans/005-*` fanout references (T78/T83 docs work).
- Coverage note: the deleted CCR test was the only `gh`-absent coverage of `make upgrade`; the phase it exercised no longer exists, so no replacement is required by this task.

## Orchestrator re-derivation

- Read the full diff (17 files): every deletion matches an item in the objective; the validator keeps its model-token guard on `herdr-agents` and swaps the alias check for `HERDR_AGENTS_WORKER_PROFILE`; the manifest note is the only `agent-config.yaml` change; `model-profiles.env` changes only through the generator comment (`render-check` clean).
- No Bot review of the final head within the worker's window (16:04:50Z–16:19:55Z); the 6f8b5683 review's single thread is fixed in the head commit.
- CI 13/13 green on 977bdf1f; branch on `main` f6320f37; PR `clean` after the thread resolution.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 977bdf1f | incorrect (1) → disposition below |

audit-finding: 1 the orchestrator's crit evidence and record claimed "2 added" tests although the diff only adds two entries to the existing `RETIRED` tuple → not-applicable:orchestrator evidence error, corrected in both the crit JSON and this record before the gate run (no test method was added; the retired-target test now pins herdr-session and agent-fanout); no product file is affected

- Codex Bot: one thread, 4178373800 `fixed:977bdf1f`, replied and resolved by the orchestrator.
- Sweep (head 977bdf1f): see the masked copy `.orchestration/validation/dotfiles-T77-harness-dead-code-a01-pr-feedback.json`; one `fixed:977bdf1f`, the rest `not-applicable`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Follow-ups

- T77b (Codex seat): `enforce-uv.sh` PreToolUse contract (VERIFY against the hooks reference; convert `"decision": "block"` if deprecated).
- Live: the next `make update` removes `~/.local/bin/common/herdr-session` and `agent-fanout` on each host.

## CompactionDB

- Worker decision `fd9cacff`; orchestrator consolidation `e4f7829e-9286-40a6-9d12-a4e55240741b`.
