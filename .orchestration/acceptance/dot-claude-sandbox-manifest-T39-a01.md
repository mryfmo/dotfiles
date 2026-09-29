# Acceptance: dot-claude-sandbox-manifest-T39-a01

Status: dispatched 2026-09-29T09:5xZ (task_commit d2f19ec); RESULT received
10:18Z (revision 1, ready_for_review, head 271e8ef6b300b527c1315cd93d39190767a1cf85,
PR #211, base origin/main 83b8567). Review and decision below the checklist.

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

## Adversarial review (orchestrator, from origin refs only)

- Base: `origin/main` is an ancestor of the head; commits 841e12b (carry
  minus AppArmor), 2815528 (approved defaults + herdr socket), 271e8ef
  (merge of main 83b8567, `.orchestration` only, no force push).
- Scope: 11 files changed, all inside `allowed_files`; the three dropped
  AppArmor files are absent from every commit's tree (`ls-tree` on each);
  no `BWRAP_APPARMOR_*` or `/etc/apparmor.d/bwrap` (non-userns) reference
  remains; main's four bwrap-userns files are untouched (empty diff).
- Manifest: `claude.sandbox` carries exactly the approved keys and values
  (`enabled true`, `failIfUnavailable false`, `autoAllowBashIfSandboxed
  true`, `allowUnsandboxedCommands true`, `excludedCommands []`, five GitHub
  domains, `allowUnixSockets [~/.config/herdr/herdr.sock]`); header comment
  keeps main's lines plus the PR continuation.
- Rendered template: `sandbox` sits between `permissions` and `hooks`;
  `filesystem.allowWrite` lists all FOUR Codex writable roots including
  `agmsg/ext-tools` (the PR head had three); `--check` passes via
  `uv run --with pyyaml` (bare `python3` lacks PyYAML: both outputs pasted;
  the task's bare form was my wording error, flagged in the dispatch note).
- Validator: `enabled`/`autoAllowBashIfSandboxed` must be true,
  `failIfUnavailable` must be a boolean (the PR's "must be true" would have
  rejected the approved value), allowWrite ⊇ Codex roots and passes the agmsg
  roots check, hostnames only, `allowUnixSockets` entries absolute or `~/`
  without globs. Five new tests incl. per-rule negatives.
- Doctor: `check_claude_sandbox` is presence-only (bwrap, socat on PATH;
  WARN via `warn_optional`; non-Linux prints not applicable) in a
  "Claude Code sandbox" section after "AppArmor"; the sysctl/profile logic
  stays in `check_apparmor_userns`. `test_runtime_health` fixture keeps
  `APPARMOR_USERNS_SYSCTL`.
- Packages: `bubblewrap`, `socat` added to `dependencies.sh`; bats count 18.
  CI ran the three bats test jobs green (the PR #179 failure was in the
  dropped fixture).
- README: sandbox section carries the PR text, points at the bwrap-userns
  paragraph, states the operator-visible effect, and documents the
  macOS-only scope of `allowUnixSockets` and the messaging-socket gap.
- Validation file: `Ran 610 tests` / `OK`, `agent asset validation ok`,
  render check, shellcheck/shfmt clean, the rendered `sandbox` JSON, the
  Claude Code docs excerpt for `allowUnixSockets` pasted verbatim, the new
  socket test red-then-green (3 tests).
- Gaps reported by the worker (not hidden): (a) `allowUnixSockets` is
  macOS-only; on Linux only `allowAllUnixSockets` opens sockets under the
  seccomp filter; (b) the Claude messaging socket is a per-process path and
  cannot be listed. Operator ruling 2026-09-29: merge as is and decide
  `allowAllUnixSockets` vs `excludedCommands` after the live E2E. The T39
  `[memory:decision]` text ("herdr/Claude unix sockets allowed") is therefore
  overstated for Linux; the worker recorded it verbatim and added a
  `[memory:failure]`; this record supersedes it (see Decision).
- CI: `gh pr checks 211` all pass (nix skipping). CompactionDB decision
  41736f91-68ac-4412-9874-9960402043ad present. Sandbox record: worker-c on
  `feat/claude-sandbox-manifest-r2`, clean; #179 untouched.
- Minor notes, no revise: `render_claude_sandbox` indexes
  `network.allowUnixSockets` unconditionally (manifest always has it; a
  missing key would raise KeyError at render time, which `--check` would
  surface); the validator requires `enabled: true`, so disabling later needs
  a validator change too.

## Codex audit dispositions

Two audits (`herdr-agents --audit` is per commit; 271e8ef is a plain merge
of `.orchestration` files).

- 2815528 (`…-audit.md`): no findings; `Verdict: correct`. "Live CI could
  not be verified" → CI verified by the orchestrator (all checks pass).
- 841e12b (`…-audit-841e12b.md`): `Verdict: incorrect`.
  - P2 `agent-config.yaml:202` — enabling the sandbox without a Unix-socket
    path breaks sandboxed `herdr` calls; `agmsg-dispatch` fails at its first
    `herdr pane list` and unsandboxed retries prompt. Disposition: the head
    adds `allowUnixSockets` for macOS; on Linux the gap is real and the
    operator ruled on 2026-09-29 to merge as is and choose
    `allowAllUnixSockets` or `excludedCommands` after the live E2E (checklist
    above gains the concrete `agmsg-dispatch` probe). Known gap, accepted,
    follow-up task after E2E.
  - P3 `README.md:351` — text still described `/etc/apparmor.d/bwrap`.
    Disposition: fixed in 2815528; at the head README mentions only
    `bwrap-userns` (grep verified).
  - "CI results concern 271e8ef, not 841e12b" → expected: the PR head is
    what CI runs and what merges.

## Review guard

crit-data evidence `dot-claude-sandbox-manifest-T39-a01-crit.json` (20
records, 20 resolved; approval r_5b03f8), receipt `…-receipt.md`.

## Decision

**Decision: ACCEPTED, merge; live E2E pending** (2026-09-29). Squash-merge
PR #211 without `--delete-branch`; close #179 with a pointer. The settings
become live only after the operator runs `make -C ~/.local/share/chezmoi
update` (sudo for bubblewrap/socat) and restarts Claude Code; the E2E
checklist above then runs in a fresh and a restored session before any
`failIfUnavailable: true` or socket-policy follow-up.

[memory:decision] T39 accepted: the Claude Code sandbox renders from
`claude.sandbox` (enabled, failIfUnavailable=false, GitHub-only domains,
allowWrite = Codex writable roots, `allowUnixSockets` = herdr socket, which
Claude Code honours on macOS only); Linux socket policy
(`allowAllUnixSockets` vs `excludedCommands`) is decided after the live E2E;
PR #179's own bwrap profile is dropped for main's bwrap-userns (operator
2026-09-29). Supersedes the T39 task-text wording "herdr/Claude sockets
allowed".

cost: worker-reported 0 subagent dispatches; orchestrating session n/a; two audit-lane runs.

## Review guard record

```
$ AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dot-claude-sandbox-manifest-T39-a01-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit 0
```

## Live E2E — leg 1: running session after `make update` (2026-09-29 ~13:20Z)

Operator ran `make -C ~/.local/share/chezmoi update` (canonical 258339f, drift
0). Claude Code hot-reloaded the settings: this orchestrator session's Bash
now runs under the sandbox (`Seccomp: 2`, `NoNewPrivs: 1`, writes outside the
cwd fail with a read-only filesystem). Results, in checklist order:

| Check | Result |
|---|---|
| `herdr pane list` inside the sandbox | **FAIL**: `PermissionDenied: Operation not permitted` (allowUnixSockets ignored on Linux, as documented) |
| same call retried unsandboxed via the harness | works after the permission gate (auto mode) — every herdr / agmsg-dispatch / herdr-agents call now needs that retry |
| write to `~/.agents/skills/agmsg/run` (allowWrite root) | ok |
| `history.sh dotfiles` (agmsg read) | ok |
| `git fetch` / `gh api` (GitHub hosts) | ok (git printed a harmless `.gitmodules` permission warning) |
| `.orchestration/` write in cwd | ok |
| `curl https://registry.npmjs.org/`, `https://example.com/` (NOT allowlisted) | **200 — not blocked**; egress goes through the proxy at localhost:3128 and raw TCP is blocked, but `allowedDomains` was not enforced in this hot-reloaded session |
| `curl https://api.openai.com/` | 421 (server-side misdirect; proxy let it through) |
| `mise exec npm:pnpm -- pnpm --version` | 12.5.1, no prompt |
| `make doctor` "Claude Code sandbox" | bwrap and socat found |
| `~/.codex/security.config.toml` | `model = "gpt-6-astra"` (T42 live) |

Findings: (1) the Linux socket gap is real and operational — the orchestrator's
control plane (herdr socket) fails inside the sandbox on every call; decision
needed now (`allowAllUnixSockets: true` vs `excludedCommands` for
`herdr`, `agmsg-dispatch`, `herdr-agents`). (2) `network.allowedDomains` did
not restrict egress in the hot-reloaded session; to be re-tested in leg 2
(fresh session after restart) before concluding it is a Claude Code behaviour
rather than a reload artefact.

Leg 2 (fresh session) and the `failIfUnavailable: true` flip remain pending.
