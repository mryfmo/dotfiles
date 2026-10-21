- [P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:69 Preserving the existing cache permits a matching `head:`/`findings: 0` artifact to return success before canonical-main lookup or private fetch; an old shared-store review—or a planted artifact—therefore bypasses Item 3 entirely. Full-head equality authenticates neither provenance nor reviewed content; require authenticated cache provenance or invalidate these entries.

- [P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:34 The named test cannot close item 8: it distinguishes two fixture content sources but never establishes that workers cannot modify the private clone. Mode 0700 does not exclude same-UID workers, and the prescribed temporary root can fall within their writable per-user temporary directory. Require an enforced worker write exclusion and corresponding test, or retain this as an unresolved residual. [Sandbox documentation](https://code.claude.com/docs/en/sandboxing)

- [P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:28 The trusted-parent contract has no bound execution prerequisite: the inherited `chain-integrate.sh` directly executes the script’s `/usr/bin/env bash` entrypoint with inherited environment, while caller/launcher changes are excluded. Child Git/gh sanitization occurs too late to prevent PATH-selected shell or shell-startup execution; require the clean parent at the actual call site before claiming this mitigation.

- [P1] high .orchestration/tasks/dotfiles-T128-chain-review-scripts-followup-a08.md:36 The sandbox premise contradicts the declared Linux configuration: `home/dot_agents/agent-config.yaml` excludes `gh *` from sandboxing. Such execution produces no sandbox denial, so “blocked PONG on denial” cannot enforce confinement, and the borrowed python-pin procedure’s Codex-only protection does not transfer to this Claude worker. Require verified effective settings or a prerequisite removing the exclusion. [Excluded-command behavior](https://code.claude.com/docs/en/sandboxing)

All 26 threat rows were assessed; no required path or non-path row unit is missing. Symlink and case-alias checks are required by the referenced contract; unrestricted same-UID interference remains explicitly residual.

📝 まとめ: Completed the read-only task-text and cited-record security review; four findings remain for orchestrator disposition.

Not checked: implementation execution, fresh sandbox probes or CI; files were unchanged, and the execution/provenance gaps above remain.
Verdict: incorrect