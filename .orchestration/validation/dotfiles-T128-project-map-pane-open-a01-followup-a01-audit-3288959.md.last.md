[P2] confidence=0.99 implementation home/dot_claude/hooks/executable_project-map-reload.sh:40 — Checking the suffix after `realpath` rejects valid maps when `.project-map` or `index.html` is a symlink to a differently named target; the hook exits before opening or reloading anything.

[P2] confidence=0.99 implementation home/dot_claude/hooks/executable_project-map-reload.sh:56 — `realpath` preserves spelling on case-insensitive macOS filesystems. Case aliases of the same repository compare unequal, causing repeated pane creation instead of reloading the existing map; confirmed against same-file directory aliases.

[P2] confidence=0.98 orchestration .orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:64 — History contains three RESULTs, reaching INV-6’s `revises=2` threshold, but acceptance contains neither the required counter snapshot nor an explicit disposition of that threshold. The S1 re-plan alone does not establish S2 continuation authority.

The task declares no invariant map; its cited constraints were checked:

INV-2: holds .orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:70 — Two non-artifact files, 46 source changes and 279 test additions satisfy the caps.

INV-6: violated .orchestration/acceptance/dotfiles-T128-project-map-pane-open-a01-followup-a01.md:64 — Threshold accounting and release evidence are missing.

Both premises hold at the dispatch base. Source hashes and the amended task hash match the evidence and dispatch history. Following failed gh-first access, the GitHub connector confirmed the final head and successful CI; [macOS CI](https://github.com/mryfmo/dotfiles/actions/runs/39025363755/job/117375179549) passed all 12 focused tests. Bash syntax, ShellCheck and 29 isolated canonicalizer/guard checks also passed.

Orchestration findings: 1

📝 まとめ: [PR 379](https://github.com/mryfmo/dotfiles/pull/379) audited without modifications; two implementation defects and one orchestration evidence gap remain. Local full-suite/Bats and live E2E were not run.
Verdict: incorrect