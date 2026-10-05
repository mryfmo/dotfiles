# Acceptance: dotfiles-T86-codex-orchestrate-a01

- **Decision:** ACCEPTED. PR #271 squash-merged to `main` as `ddf14036`; final head `63a9b107` (diff head 0f43e161). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, one evidence disposition below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-05 01:26Z).
- **Worker:** `codex-security-dot-a007` (worker-e, wT:p8). task_rev verified at dispatch and after each PONG-decision/scope-note append.
- **Exemption declared:** acceptance and final integration; evidence sync (seven worker artifacts copied from worker-e).
- **Plan reference:** Phase 7, dotfiles-T86 (principles 4 and 5). Dispatched in parallel with T85 (soft dependency on `--directive`, now on `main`) and T82.

## What was accepted (PR #271, final head `63a9b107cd327639659b11b87b34276c32c1d3fe`; diff head 0f43e161; commits f73cc9e7, 7646ecf8, 4598d30b, b2e76efc, bb80c633, c3bd7af0, 0f43e161 plus two update-branch merges; 3 files, +838)

- `home/dot_local/bin/common/executable_codex-orchestrate` (158 lines; the restore logic overruns the 150-line budget, reported as the task allowed): requires `HERDR_AGENTS_ORCHESTRATOR_KIND=codex` and the interactive profile's Codex args from `~/.agents/model-profiles.env` (no literal model/profile flags; tested); runs only from the main checkout root; takes a private per-repository lock under `${XDG_STATE_HOME:-~/.local/state}/codex-orchestrate/locks/` before reading identities; refuses the Codex name when registered at another project (teams metadata, no pane reads) or when a different Codex identity exists at the checkout; snapshots the exchanged Claude rows and original Codex memberships into the private run directory; exchanges the non-worker Claude registrations with project/type-scoped `reset.sh`, joins the Codex identity to every exchanged team (`--team` selects only the polled inbox), sets `delivery.sh set turn codex <repo>`, and restores rows and `both` delivery on exit/INT/TERM (a failed restore keeps the lock and snapshot; README documents recovery); first prompt = `herdr-agents --directive` + operator task + the completion-protocol sentence, piped on stdin to `codex … exec -C <repo> -o <private>/<turn>.final.md -`, then `exec resume --last -` per delivered inbox body (poll every 15 s; `--timeout` 1800 s → exit 124; `--max-turns` → exit 2; `ORCHESTRATION-DONE` as the final non-blank line → exit 0); raw prompts, finals and console output only in the mode-0700 private run directory (refused under the repository, the agmsg store or TMPDIR); the repository file `.orchestration/validation/codex-orchestrate-<date>-<n>.md` holds non-secret turn status and private paths; `CODEX_ORCHESTRATE_DELIVERY=hook` is refused until T87 validates it.
- `tests/unit/test_codex_orchestrate.py`: 38 fake-CLI cases (argv sequence exec → resume --last, exchange and restore, existing seat reuse, worker seats and cross-project registrations preserved, delivery set/restore and failure handling, timeout/15-second cadence, max-turns, hook mode, lock refusal, wrong kind/arguments, missing env, no literal model flags and the 150-line bound).
- README: "Codex orchestration without a pane" section (launch, exchange and team contract, worker reply convention, exit codes, private state contract and its assumption, recovery steps, hook-mode refusal and the T87 VERIFY).
- 838 unit tests; shfmt/shellcheck clean; `make validate-agent-assets` ok; CI 13/13 green on 63a9b107; branch on `main` 2e65742c.

## Decisions taken during the task

- Revise round 1 (audit of 567c8d17: global name collision, completion protocol, multi-team reuse) grew with the Bot's round-1 findings into four fix commits and PONG decisions 3–6: transcripts and recovery state moved to a private 0700 state directory outside every child-writable root (decision 3's in-repository masked transcripts superseded by decision 4 once the Bot showed the known-pattern masker is not a secret scanner); prompts on stdin; hook mode refused until T87; private lock before identity reads; the Codex identity joins every exchanged team.

- PONG 1: the in-sandbox `codex exec` probe cannot initialize Codex (read-only runtime home) → the Stop-hook VERIFY is deferred to T87; the launcher ships the poll loop with the `poll|hook` switch.
- PONG 2: seat exchange via project-scoped `reset.sh` with a metadata snapshot (no `leave.sh`, which removes an identity from every team; no pane reads).
- Scope note from T85 (Codex thread 4179731976): delivery set/restore is part of the exchange (4598d30b).
- Codex threads: nine fixed (4179854338 → bb80c633; 4179854340, 4179898024, 4179898026, 4179898029, 4179898032 → c3bd7af0; 4179976124, 4179976127, 4179976130 → 0f43e161) and two not applicable (4179700882 `--directive` = T85 on the base; 4179700881 `HERDR_AGENTS_ORCHESTRATOR_KIND` = T84, PR #272 in flight); all replied and resolved by the orchestrator after confirming the fix commits are ancestors of the head.

## Orchestrator re-derivation

- Read the launcher in full (option parsing, kind/profile resolution, identity discovery excluding worker aliases, team/suffix derivation, lock, snapshot, reset/join/delivery sequence, restore trap, turn loop and poll); the only state it touches outside `.orchestration/validation/` is the agmsg store through the official scripts and its private snapshot dir.
- Residuals (documented): the `hook` delivery mode is refused until T87 validates it; the launcher's private-state contract relies on the managed Codex writable roots (README states the assumption); the launcher's own Python helpers run outside Claude Bash, so the enforce-uv hook does not apply to them.
- CI 13/13 green on 567c8d17; PR `clean` after the two resolutions; no Bot review on the final head within the worker's window.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, 567c8d17 (round-0 head) | incorrect (3) → global name-collision check, ORCHESTRATION-DONE instruction in the prompt, and multi-team seat reuse fixed in revise round 1 |
| task-level, final head 63a9b107 | incorrect (1) → disposition below |

audit-finding: 1 the report asserts the final RESULT delivery and the PR body update without pasted dispatch output or body evidence for the final head → not-applicable:evidence-presentation finding corroborated independently by the orchestrator — the RESULT for head 63a9b107 is in the agmsg history (01:17:32Z, received by this seat) and `gh pr view 271` shows the updated title and a 12-line body describing the private-state design with the required footer; no product file is affected

- Sweep (head 63a9b107): see the masked copy `.orchestration/validation/dotfiles-T86-codex-orchestrate-a01-pr-feedback.json`; nine `fixed:` items, the rest `not-applicable`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`; worker `…-worker-crit.json` / `…-worker-review-receipt.md` kept.

## Follow-ups

- T84 renders `HERDR_AGENTS_ORCHESTRATOR_KIND`; T87 runs the codex→claude and codex→codex legs live and settles the delivery mode.

## CompactionDB

- Orchestrator consolidation `e736dabf-7743-4c73-bfee-8e0c407f2961` (the Codex seat cannot write the main-checkout DB).
