# Needs validation: dotfiles at 10a8ea3d53f99f56ba0f3c544e5477c624c64f1a

No `needs_validation` record is in this run's `findings.json`. One lead would be `needs_validation` once independently verified: `dsh-profile:thak-fs-tool-writes-workspace-git-unguarded` (`REPORT.md` section 5b). At this head it is narrowed.

**Closed under the U272 role.** The `hcom-seat dsh` role gives the harness a scratch working directory and denies the checkout's git paths (`scripts/orchestrator/hcom-seat:1236-1240`, `:1494`, `:1791-1794`).

**Open for a direct run.** The installed wrapper `~/.dsh/bin/dsh` runs the harness with no srt check (`scripts/update-agent-assets.sh:2174`), and there the thak file tool can write `<cwd>/.git`.

**Blockers.**
- Upstream runtime behaviour: the write succeeding with the presets pending.
- Deployment: whether the harness is run directly from a checkout.

**Local plan, in the required sandbox.**
1. With a scratch HOME and DSH_HOME, loopback only, make a scratch git repository the working directory.
2. Run the wrapper directly, with a stub model that answers one write to `.git/hooks/post-checkout`.
3. Check for the file. Stop without running git.

**Owner-observed.** Whether the harness is ever run outside the role, and whether the wrapper should refuse that.
