[P2] high orchestration .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-followup-a01.md:26 — The report, validation, and sandbox files named as audit inputs are absent from both the audit and main checkouts. I recovered them from worker-g’s untracked task directory; synchronize them before acceptance so the evidence survives worktree reuse/removal.

[P3] high conformance .orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-followup-a01.md:25 — The worker posted the manual `@codex review` request despite the automatic-window-only constraint. The acknowledged deviation remains a conformance finding; retaining the resulting review does not satisfy that restriction.

No implementation defect found. Both helpers isolate imports from `/` while preserving descriptor 9 and lock lifetime. The regression covers hostile modules and packages. Changed files match the worker-tested versions; syntax and diff checks pass. GitHub confirms all four final-head Python test jobs passed. [PR #422](https://github.com/mryfmo/dotfiles/pull/422) was checked through the connector after `gh` failed to connect.

Task invariants: no numbered `INV-*` entries are declared. Item 1 holds at `home/dot_local/bin/common/executable_herdr-agents:1834` and `:1901`, with coverage at `tests/unit/test_herdr_agents.py:2243`.

Orchestration findings: 1

Not rerun: local tests or live Herdr operations; nothing modified. Evidence synchronization remains necessary before acceptance.
Verdict: incorrect