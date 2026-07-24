# T16 herdr --attach layout order repair — ACCEPTED (pending PR with T17)

**Verdict: ACCEPT** — code complete and live-verified on branch
`feat/herdr-attach-order-repair`; PR will be opened after T17 lands on the
same branch (single PR for the herdr-attach fix set).

Date: 2026-07-17 (Asia/Tokyo). Reviewer: orchestrator-fable5 (claude-code).

## Review rounds

- **Round 1 (revise)**: swap-order logic desk-verified correct for all six
  pane permutations; tests 36/36. REJECTED because the new ambiguity guard
  used workspace-scoped `pane list` while `pane layout` is tab-scoped — a
  second tab in the workspace would silently block the entire attach
  (regression vs T15).
- **Round 2 (revise)**: tab filtering (`panes_on_pane_tab`) verified correct;
  37/37 tests. Orchestrator live E2E then found a real-herdr-only defect:
  `herdr pane rename` emits pane_info JSON on stdout, polluting the
  command-substituted return of `start_codex_agent`, so order repair always
  refused right after codex start. Unit mocks were silent on rename, hence
  invisible to tests. REJECTED with root-cause fix instruction.
- **Round 3 (ACCEPT)**: `rename > /dev/null` inside `start_codex_agent`
  (fixes the attach path AND the pre-existing T10-era full-mode pollution at
  the same root), mock rename now prints realistic JSON. Independent rerun:
  37/37 unit tests, `bash -n` clean.

## Orchestrator live E2E (Fix C standard applied)

1. Idempotency: attach on correct `claude|codex|files` layout → zero swaps,
   layout byte-identical. PASS.
2. Self-repair (restored-broken-session scenario): layout deliberately
   scrambled to `files|codex|claude` → attach repaired to `claude|codex|files`
   with one swap, exit 0. PASS.
3. Fresh workspace: plain workspace + simulated attach env → renamed claude
   pane, files + codex created, final order `claude|codex|files`, no
   refusing-repair stderr, exit 0. PASS (failed pre-round-3, caught the
   stdout-pollution bug).

Full herdr-process-restart restore E2E is deferred to the next natural herdr
restart; the restored-broken-layout code path is equivalent to E2E #2 and the
live w13 session state was already hand-repaired and persists correctly.

## Known accepted edge

If the codex pane was manually moved to a different tab, attach now treats
the claude tab as codex-less and attempts a fresh `herdr agent start` under
the same registration name; behavior depends on herdr duplicate-name
handling. Operator-induced corner, logged, does not affect standard flows.

## Live incident remediation (orchestrator-side, already done)

- Broken persisted w13 layout (`files 50% | claude 25% | codex 25%`)
  hand-repaired to `claude|codex|files ≈ 40/38/22` via pane swap/resize;
  herdr persists the corrected state.
- 11 stale `codex-wp*` identities removed from team
  `dotfiles-tmux-hermes-removal`; codex identity for this repo is now
  uniquely `codex-gpt56sol-dot`.
