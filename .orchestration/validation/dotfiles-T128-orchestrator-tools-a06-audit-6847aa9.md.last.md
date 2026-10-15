[P1] high specification .orchestration/tasks/dotfiles-T128-orchestrator-tools-a06.md:41 — **The prescribed PATH still permits PR-selected code.** `orch-gate.sh:72` preserves the caller’s PATH; on this host, `gh` resolves through a mise shim. The gate launches it from the PR checkout (`require-crit-review.py:519`). Installed mise 2026.10.7 accepts plain tool-version strings without trust, including `"github:cli/cli" = "path:./payload"`; a PR-owned `payload/bin/gh` can therefore execute with host credentials. An orchestrator-owned PATH is acceptable only when its executables cannot rediscover PR-controlled configuration. Pinning Python does not establish that for `gh`. This P1 requires the operator’s decision. [Installed-version trust logic](https://github.com/jdx/mise/blob/v2026.10.7/src/config/config_file/mise_toml.rs#L3318), [shim behavior](https://mise.jdx.dev/dev-tools/shims.html), [path selection](https://mise.jdx.dev/dev-tools/versions.html#request-syntax)

[P2] high orchestration .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a06.md:9 — **Numeric thread IDs invalidate the counter ledger.** The three thread IDs are JSON numbers, while `scripts/regime-counters.sh:138` requires strings and rejects the entire ledger as `id-not-string`. Consequently, S1 loses the recorded audit classes and falls back to Bot-title detection. Store these IDs as strings.

The requested delta otherwise checks out:

- `orch-gate.sh:72` uses `env -i` with exactly `PATH`, `HOME`, `AUDIT_EVIDENCE`, `ACCEPTANCE_EVIDENCE`, `PR_FEEDBACK_EVIDENCE`, `REVIEW_EVIDENCE`, `AGENT_REVIEWED=1`, and `PYTHONSAFEPATH=1`.
- Line 58 resolves Python in the trusted root; line 74 invokes that exact interpreter with `-I -P`. A read-only probe confirmed that the Python child inherits safe-path behavior and excludes cwd.
- `tests/unit/test_orchestrator_tools.py:1041` supplies all five named hostile variables and asserts their absence through exact environment-name comparison. It allows only the eight names plus Bash’s own `PWD`, `SHLVL`, and `_`, and checks `-I -P`. It does not exercise the downstream mise shim.
- The committed a06 task matches the dispatched hash `b10dfb47257f00dd0ad05c11a977514b948fdebc7238af76a118a1ad80e2127c`; a05 records are unchanged since `a06c874e`.
- GitHub independently confirms successful final-head Actions runs and all four Python-test steps. The remaining GitGuardian failure is accurately recorded as the variable-name false positive. [PR 350](https://github.com/mryfmo/dotfiles/pull/350), [test run](https://github.com/mryfmo/dotfiles/actions/runs/38506470081)

The task has no explicit front-matter invariant map; its referenced obligations assess as follows:

INV-1: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a06.md:10 — scope and task-copy identity match.  
INV-2: holds .orchestration/validation/dotfiles-T128-orchestrator-tools-a06.md:226 — 3 files, 201 added non-test lines, 224 added test lines.  
INV-4: holds .orchestration/tasks/dotfiles-T128-orchestrator-tools-a06.md:95 — all three premises verified, including the documented line-number shift.  
INV-6: violated .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a06.md:9 — the class ledger is rejected by the counter reader.  
INV-7: holds .orchestration/acceptance/dotfiles-T128-orchestrator-tools-a06.md:71 — both reviews bind the dispatched hash.

Orchestration findings: 1

📝 まとめ: Read-only audit completed; nothing modified. One P1 remains for operator decision.

Not rerun: fixture-writing tests or the malicious-config exploit; the PATH finding rests on local resolution and installed-version source tracing.
Verdict: incorrect