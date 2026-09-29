# Acceptance: dot-claude-sandbox-manifest-T39-a01

Status: task authored 2026-09-29 (not yet dispatched; follows T38 because both
touch README.md and one worker seat is available). Decision pending RESULT.

## Live E2E checklist (acceptance criterion, pre-written)

T39 changes live Bash behaviour for every Claude Code session on this host.
Per the agmsg-orchestration skill, acceptance requires live end-to-end
verification in BOTH a fresh session and a restored session. It can only run
after merge, `make -C ~/.local/share/chezmoi update` (operator: sudo for the
new apt packages bubblewrap and socat), and a Claude Code restart. Until then
the record stays at "merged, E2E pending" (T32 pattern: merge, then E2E
appended).

Fresh session and restored session, each:

- [ ] `claude` starts with the rendered `sandbox` block active (`/status` or
      settings dump shows `enabled: true`, `failIfUnavailable: false`).
- [ ] `herdr pane list` from Bash works through `network.allowUnixSockets`
      (no unsandboxed-retry prompt).
- [ ] agmsg Stop hook (`check-inbox.sh`) writes to the allowWrite roots
      (`~/.agents/skills/agmsg/{db,teams,run,ext-tools}`) without a prompt.
- [ ] `git push` / `gh pr checks` reach the GitHub domains without a prompt.
- [ ] Worker worktree: `mise exec npm:pnpm -- pnpm --version` records whether
      a network prompt appears (registry host is not allowlisted).
- [ ] Headless auditor `codex --profile audit exec …` records whether a
      network prompt appears (OpenAI hosts are not allowlisted).
- [ ] `.orchestration/` writes in the cwd succeed.
- [ ] `make doctor` shows the new "Claude Code sandbox" section with bwrap
      and socat present.

Observed prompt counts and any failure go in this record; a follow-up task
flips `failIfUnavailable` to `true` only after both sessions pass.
