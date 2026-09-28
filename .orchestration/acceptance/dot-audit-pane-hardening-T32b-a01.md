# AGMSG-ACCEPTANCE dot-audit-pane-hardening-T32b-a01

RESULT 2026-09-28T00:43:09Z from claude-standard-dot-a005 (worker-c, claude-opus-5-5 high, --advisor fable): status=ready_for_review, PR #195 head dad7bdff6592b875dc9369405fe6941fe1fc0062, branch fix/audit-pane-hardening from origin/main c48e614.

## Adversarial review (orchestrator, from origin refs and the orchestrator-review worktree)

- task_rev a4694adf… matches the task file at origin/main c48e614; the PR does not touch `.orchestration/tasks/`.
- Diff scope: 2 files (+105/−47), within the allowed files (README unchanged — no user-visible statement changed; rules/SKILL untouched as forbidden).
- Fix 1 (quoting): the complete inner command is built with one `printf -v` (`cd -- %q && set -o pipefail && codex<%q args> review --commit <sha> 2>&1 | tee -- %q; printf '<marker>:%s\n' "$?"`) and sent as `bash -c $(printf '%q' "$inner")` — quoted once, no nested `%q` inside single quotes. The `'`/control-character blocklist is removed as the task required. Orchestrator runtime check through zsh under `LC_ALL=C` with DIR `it's 監査` and `--out evidence 監査.md`: zsh parsed the `$'…'` form, the inner `false` propagated `:1` via pipefail, and `tee` created the correctly named non-ASCII file.
- Fix 2 (wrapping): `--source recent-unwrapped` on both the marker `pane wait-output` and the follow-up `pane read` (both values verified in the live CLI help during T32).
- Unchanged and verified in the diff: sha/timeout validation, nonce marker, cd prefix, pipefail exit propagation, tab reuse.
- Tests: apostrophe test flipped to acceptance with decoded cd/tee targets; new C-locale non-ASCII `--out` test; new unwrapped-source test; decoding helpers use `eval "set -- …"` under an empty PATH (safe on mis-quoted baselines). Independent re-derivation: 15 `-k audit` tests re-run OK at dad7bdf in the orchestrator-review worktree; mutation baseline 4/15 FAIL against the unmodified 6b9babc script (the baseline output shows the old non-ASCII bug decoding into 4 words); 490 unit tests OK; PR CI 12/12 pass (nix skipped).
- Worker-declared deviations ACCEPTED: single-quoted marker printf (same behavior, readable when decoded); test (c) as its own test so the baseline isolates the `recent`→`recent-unwrapped` change.
- CompactionDB: 7a2cd50a-a846-4971-a028-a03f3f766682 present in the main-checkout DB.
- Refutation attempts found no correctness, regression, security, or omission issue.

## Pre-merge Codex audit (head dad7bdf, gpt-6-astra, read-only, headless)

"No actionable regressions found" (24 Bash/Zsh round-trips, herdr supports `recent-unwrapped`) — evidence at `.orchestration/validation/dot-audit-pane-hardening-T32b-a01-audit.md`. No findings to disposition.

## Review guard

`make require-crit-review` satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-audit-pane-hardening-T32b-a01-receipt.md (resolved review-scope approval record r_5e14e4, crit session 16eb550d49a7, exported JSON at .orchestration/validation/dot-audit-pane-hardening-T32b-a01-crit.json).

**Decision: ACCEPTED.** Merge #195 --squash (no --delete-branch while worker-c holds the branch); deploy the script with a single-target `chezmoi apply ~/.local/bin/common/herdr-agents` from the canonical clone after its ff pull; live E2E `herdr-agents --audit <merge-sha>` in pair workspace wJ reusing the existing `audit` tab (acceptance criterion: no new tab, `Audit exit: 0`, evidence tee'd). Result recorded below.

[memory:decision] T32b accepted 2026-09-28: the audit pane command is assembled once and sent as a single `%q`-quoted `bash -c` argument (nested-quote and non-ASCII/C-locale path classes eliminated; the `'`/control-char blocklist removed), and marker detection uses `--source recent-unwrapped` for wait-output and pane read so pane width cannot hide completion. PR #195 squash-merged.

cost: n/a (worker report gives no token figures)

### Live E2E (orchestrator, pair workspace wJ, 2026-09-28, script deployed via single-target chezmoi apply after merge e7de371)

`herdr-agents --audit e7de371 --out .orchestration/validation/dot-audit-pane-hardening-T32b-a01-live-e2e.md --timeout 560 ~/Workspace/dotfiles` → tabs unchanged {t1, t2, t3=audit} (existing audit tab and pane wJ:p4 reused, no new tab), the real gpt-6-astra audit ran visibly, 1m35s wall clock, `Audit exit: 0`, evidence tee'd (1650 lines). The post-merge live audit of e7de371 itself reported "No actionable regressions found" (ten Bash/zsh quoting and exit-marker checks incl. apostrophes, non-ASCII paths, control characters) — no findings to disposition. Acceptance criterion met.
