# dot-mkt-mode-T1-a01 report

status: ready_for_review
cost: n/a

## Result

- F1: `update_codex_crit` now normalizes the existing chezmoi-managed `~/.agents/plugins/marketplace.json` to mode 0644 immediately after `crit install codex-plugin --force`.
- F1: Real Crit in the credential-free VM produced byte-identical marketplace content on both runs; only mode normalization is required.
- F2: The fresh scratch-user proof ran two full target cycles. The second `chezmoi apply --verbose --exclude=scripts` emitted no drift, both Crit runs ended at mode 0644, both content diffs were clean, and final chezmoi status was empty.
- F3: Added one focused source-and-mock unit test that recreates Crit's umask-002 mode 0664 and requires normalization to 0644.
- [memory:decision] After Crit rewrites the chezmoi-managed marketplace file, the shared `update_codex_crit` path owns the single 0644 normalization; no other Crit-created file is changed.

## Validation

- Focused regression test: RED at 0664, then GREEN at 0644.
- Required `adh-test` two-cycle proof: passed with real pinned Crit and scratch cleanup.
- 363 Python unit tests: passed.
- Bash syntax, ShellCheck, shfmt, `git diff --check`, and agent asset validation: passed.
- Crit-data review: resolved finding-free approval `r_b70307`; final gate passed.
- Full verbatim evidence: `.orchestration/validation/dot-mkt-mode-T1-a01.md`.

## CompactionDB

Memory command and output are recorded in validation. Decision ID: `91c32f19-a3a5-495d-9dac-7a3d3bd83658`.

## Constraints honored

- No commit, push, local bats, Codex login, credential transfer, mise config/lock edit, or `home/` source change.
- VM access used only `limactl shell adh-test`.
- Scratch user `dotmktcheck` and its home were removed after every attempt.
- No persistent external side effects remain.
