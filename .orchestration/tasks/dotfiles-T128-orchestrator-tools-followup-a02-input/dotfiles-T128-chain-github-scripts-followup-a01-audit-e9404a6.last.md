[P2] high implementation scripts/orchestrator/resolve-threads.sh:57 A gate-valid disposition containing ``evidence=rg 'uses `example`' README.md`` is truncated at the embedded backtick when `fill_sweep.py` reads the reply. The full in-memory reproduction reports `filled 1 gaps 0` and saves an incomplete command. This silently corrupts evidence, contrary to report.md:73’s fail-closed claim; validate lossless recovery before posting and resolving.

[P3] high orchestration .orchestration/validation/dotfiles-T128-chain-github-scripts-followup-a01-pr-feedback.json:161 The CodeRabbit status disposition cites `select(.url == "None")`, but its URL is JSON `null`. Replaying the evidence command returns nothing; select the actual status item.

INV-2: holds .orchestration/tasks/dotfiles-T128-chain-github-scripts-followup-a01.md:67 — 2 files outside orchestration evidence, 25 non-test changed lines, 89 test additions.

Both premises hold at dispatch base `727180db`. Task and evidence copies match the audited head. [PR #360](https://github.com/mryfmo/dotfiles/pull/360) has successful Actions runs; CI logs confirm all 5 target tests and 40 neighboring tests passed. Bash syntax and shellcheck also pass.

Orchestration findings: 1

📝 まとめ: Read-only audit completed with two findings; nothing modified.

Not checked: live GitHub mutations or a local full-suite rerun. Risk: reply recovery can silently truncate disposition evidence.
Verdict: incorrect