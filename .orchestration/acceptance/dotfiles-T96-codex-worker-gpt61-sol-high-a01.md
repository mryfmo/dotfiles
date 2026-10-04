# Acceptance: dotfiles-T96-codex-worker-gpt61-sol-high-a01

- **Decision:** ACCEPTED. PR #259 squash-merged to `main` as `f6320f37`; head `3a060118500090ca7ddd42ade85446dcf1a42ed8`. Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, two dispositions below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-04 15:52Z).
- **Worker:** `claude-standard-dot-a006` (worker-d, wY:p2). task_rev matched at dispatch and after the two PONG-decision appends.
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** operator directive 2026-10-04 (「指示役fable-5.1 high 監査役gpt-6 astra high 作業役 gpt-6.1 sol high/opus-5.5 high」), outside the numbered phases; routed to a Claude seat because model profiles are not an execution-boundary source.

## What was accepted (PR #259, head `3a060118500090ca7ddd42ade85446dcf1a42ed8`; one commit on `main` 40993f20)

- `model_profiles.standard.codex`: gpt-6.1-sol, high (was gpt-5.6-terra, medium). `model_profiles.audit.codex`: gpt-6-astra, high, read-only sandbox kept (was gpt-6.1-sol, xhigh). Rendered `modify_private_standard.config.toml` and `modify_private_audit.config.toml` follow; `make render-check` clean.
- `scripts/validate-agent-assets.py`: the audit-profile pin and its comment follow (operator pin 2026-10-04, T96); `ADH_PROFILE` untouched (T79 removes it).
- `home/dot_config/claude/rules/model-selection.md` line 3 and `README.md` lines 289-291 state the constellation and drop the API-key clause: both Codex models answered under the ChatGPT login in live probes (`codex --profile security exec` → gpt-6-astra OK; `codex --profile audit exec` → gpt-6.1-sol OK; 2026-10-05 00:20/00:25 JST = 2026-10-04 15:20Z/15:25Z), so the 2026-10-01 rejection no longer reproduces.
- Tests in `test_generate_agent_configs.py` and `test_validate_agent_assets.py` follow the new values.

## Decisions taken during the task

- PONG 1: `README.md` auditor sentence allowed in the same PR (same change class); the auth clause limited to what the probes proved.
- PONG 2: `[memory:decision]` last clause replaced by the probe result (CompactionDB `152b5006…`).
- Codex P2 4178257366 ("future-dated probe"): not applicable; the rule cites the JST date and the commit is stamped `2026-10-05T00:21:53+09:00`, after the probes; the Bot compared a JST date with the commit's UTC date. No text change (a UTC stamp would have moved the head for no factual gain; the validation file holds both).

## Orchestrator re-derivation

- Read the full diff (8 files, +28/−30): the two manifest mappings, the two rendered sources, the validator pin, the rule line, the README sentence, the tests. No other profile changed; the `security` profile (gpt-6-astra) and `deep`/`review`/`express` are untouched.
- The constellation matches the operator's words verbatim: orchestrator fable-5.1 high, auditor gpt-6-astra high, worker gpt-6.1-sol high / opus-5.5 high.
- CI 13/13 green on 3a060118; branch up to date; PR `clean` after the thread resolution.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, head 3a060118 | incorrect (2) → dispositions below |

audit-finding: 1 the sandbox file records unsandboxed `git push`, `gh` calls and the two `codex … exec` auth probes through the permission gate → not-applicable:the Claude-seat exception for `gh` and `git push` is the written protocol since T69 (Worker Playbook step 4, PR 253, refined by T97), and the two probes are the task's own required auth check, which needs the host keyring and network the sandbox denies; every command ran through the auto-mode permission gate and the sandbox file lists each one, so nothing was escalated agent-to-agent or hidden
audit-finding: 2 the validation block pipes `make` output through `grep`/`tail` while claiming separately captured exit statuses → not-applicable:evidence-presentation finding; the claimed results are corroborated independently by CI on 3a060118 (Unit test and formatting jobs green, 13/13 checks) and by the orchestrator's `make render-check` reading of the rendered profile sources, and no product file is affected

- Codex Bot: one thread, 4178257366 `not-applicable` (reply by the orchestrator), resolved. Bot review on the head at 15:29:37Z.
- Sweep (head 3a060118): see the masked copy `.orchestration/validation/dotfiles-T96-codex-worker-gpt61-sol-high-a01-pr-feedback.json`; every item `not-applicable` (no fix commit was needed).
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Activation (operator side, after merge)

- `make update` in the canonical clone (`~/.local/share/chezmoi`) renders `~/.codex/standard.config.toml` and `~/.codex/audit.config.toml` and `~/.agents/model-profiles.env`; then `herdr-agents --restart-worker` re-seats the pair worker with the new args (the pair worker here is a Claude seat, so only the audit lane changes on this host). The orchestrator's own `herdr-agents --audit` runs pick up gpt-6-astra high from the deployed profile.

## CompactionDB

- Worker decision `152b5006` (PONG decision 2 text); orchestrator consolidation `bbd66420-652a-4520-9193-50b9d4bd5e82`.

## Activation done (orchestrator host, 2026-10-04 16:05Z)

- `make update` in the canonical clone at f6320f37: `~/.codex/standard.config.toml` = gpt-6.1-sol/high, `~/.codex/audit.config.toml` = gpt-6-astra/high, `MODEL_PROFILE_AUDIT_CODEX_ARGS="--profile audit"`. The pair worker on this host is a Claude seat, so no `--restart-worker` is needed here; the Codex security seat (worker-e) keeps its `security` profile. Later `herdr-agents --audit` runs use gpt-6-astra high.
