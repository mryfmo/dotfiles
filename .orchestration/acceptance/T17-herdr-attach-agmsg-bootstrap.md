# T17 herdr attach agmsg bootstrap + acceptance rule — ACCEPTED

**Verdict: ACCEPT** — on branch `feat/herdr-attach-order-repair` together with
T16; PR lifecycle authorized.

Date: 2026-07-17 (Asia/Tokyo). Reviewer: orchestrator-fable5 (claude-code).

## Delivered behavior

- `bootstrap_agmsg` runs after codex start/reuse in attach, existing-workspace
  and fresh full modes: skips silently when agmsg is absent; installs the
  repo-scoped codex turn-delivery Stop hook via `delivery.sh set turn` ONLY
  when `<repo>/.codex/hooks.json` lacks the check-inbox hook (pure jq file
  check in the steady-state path — zero delivery.sh invocations, zero watcher
  risk); warns on missing/ambiguous codex identity via `identities.sh`;
  never breaks Claude startup (`|| true`, log-append).
- Fix C: agmsg-orchestration rule now requires live E2E (fresh + persisted
  restore) before accepting tasks that change live desktop behavior.

## Review rounds

- **Blocked round**: worker STOPped on the watcher-kill hazard (correct per
  original task text; orchestrator amendment crossed mid-turn). Unblocked
  with hook-file-check-gated spec.
- **Round 2 (revise)**: hook-detection jq evaluated `.command` at the
  matcher level of `.hooks.Stop[]`, returning FALSE against the real
  delivery.sh-generated nested schema → gate never engaged → `set turn` (and
  its project-scoped watcher kill) would fire on EVERY attach. Caught by
  orchestrator verification against the real hooks.json; the unit fixture was
  a hand-written flat schema. REJECTED with fixture-realism requirement.
- **Round 3 (ACCEPT)**: jq iterates `.hooks.Stop[]?.hooks[]?`, fixture copies
  the real nested schema. Independent rerun: 42/42 unit tests, shellcheck
  clean.

## Orchestrator live E2E

- Steady state on live w13 (hook present): attach → no stderr warnings,
  `delivery.sh` not invoked, watch processes 1 alive before AND after (the
  orchestrator monitor survived), codex delivery mode still `turn`. PASS.
- First-time path covered by unit tests (hook-absent → exactly one
  `set turn` call); its known one-time same-repo watcher kill is documented
  in the worker report and tracked as an upstream agmsg skill issue
  (kill scoping by project only — memory note `agmsg-delivery-kill-scoping-issue`).

## Official-upstream verification (operator-requested)

Researched openai/codex official docs and issues: repo-scoped
`.codex/hooks.json` Stop hooks are an official stable feature since
codex-cli v0.124.0 (trust-gated; this repo is trusted and the hook is loaded
per `~/.codex/config.toml` hooks.state); `notify`/agent-turn-complete is
official but user-global only (unsuitable for repo-scoped delivery);
`codex inject` was declined upstream (#11415) so pane nudges remain a
workaround; the $HOME-registration ban is corroborated by open issue #9932.
Design confirmed sound; no change required.
