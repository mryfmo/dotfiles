---
task_id: dotfiles-T130-claude-sandbox-integration-followup-a01
seat: claude-review-dot-a005
branch: docs/claude-sandbox-readme-a01
base: a8a747af
code_commit: bfcb0525 (the README commit 0b226806, the review-round commit bfcb0525)
pr: @PR@
task_sha256: ea5f53285ac406a1dd45f705f95fbde49714327d2c7b1ed227fdf7dcad516bbf
---

# Report: dotfiles-T130-claude-sandbox-integration-followup-a01

- Seat: `claude-review-dot-a005` in `.claude/worktrees/worker-d`, on a fresh branch `docs/claude-sandbox-readme-a01` from `origin/main` `a8a747af` (PR #392 merged); the branches of PR #387, PR #394 and PR #395 stay in the worktree for their integrations.
- Task file: dispatched 2026-10-17T16:43:09Z at `ea5f5328…`, copied byte-identical to `task.md`; the task-consistency check passes on it (validation §1a); `premises: []`.
- The orchestrator's note: the README is rewritten from the rendered settings on `main` (the template), not from the live machine, because the operator's full `make update` is deferred; under the operator's ask rules the branch is pushed and the seat stops at `gh pr create` with a blocked PONG.

## What changed

**`README.md`, "### Claude Code sandbox"** (73 added, 31 removed lines over the two commits; the only file outside `.orchestration/`): the first paragraph and the "Operator-visible effect" paragraph now say what `home/.chezmoitemplates/claude-settings-managed.json` renders for each OS, sentence by sentence:

- the renderer and the validator's four refusals (telemetry or metadata host, a Mach service other than `com.apple.trustd.agent` or one on Linux, `allowAllUnixSockets`, `gh` excluded on macOS, a Linux exclusion list other than the seat-tool list);
- `allowWrite`: the agmsg roots, then `~/.cache/uv`, `~/.local/state/mise`, `~/.local/share/uv`, and on macOS `~/Library/Caches/mise` (the old text named `~/.cache/uv` alone);
- `allowedDomains`: the five GitHub hosts and the two PyPI hosts; under the managed `defaultMode: auto` another host is refused unless the command listed it and the classifier approved (the old text said GitHub only and "other hosts prompt");
- `allowMachLookup` on macOS: `com.apple.trustd.agent`, omitted from the Linux rendering;
- `allowUnixSockets` (unchanged: the herdr socket, macOS only) and the messaging-socket note;
- `excludedCommands` per OS: macOS `agmsg-dispatch *` only; Linux adds `gh *`, `herdr-agents *` and the absolute `actas-claim.sh *`, with the upstream matching rules (Bash-rule syntax, every command in a chain, the text of the call) and the permission flow an excluded command still takes (the old text said "only `agmsg-dispatch`" and "matches the first word", and sent `gh` and herdr through the retry prompt on Linux);
- the one managed allow rule (unchanged), the 32 `ask` rules for gh's write operations named by subcommand and `gh api` form, with the prefix-rule limit and the integration gate as the authority;
- the managed `env` (the four values);
- `allowAllUnixSockets`, `failIfUnavailable` and `autoAllowBashIfSandboxed` (the ask-rule example is now the managed gh rules, not `Bash(git push:*)`, which the managed settings do not contain) and `allowUnsandboxedCommands`.

The Ubuntu bubblewrap paragraph, the nested-worktree paragraph and the plan-mode paragraph are untouched: nothing in them names a changed setting.

## The Check

`prettier --check README.md` clean (validation §3); `make validate-agent-assets` exit 0 (§3a); `git diff --numstat origin/main...HEAD` is `73 31 README.md` and nothing else (§4). The section's values were read back from the template and compared, 14 checks ok (§5); the upstream sentences the text relies on are quoted with their pages and headings (§6).

## Readings, declared

- "The rendered settings" are the template on `origin/main` (`home/.chezmoitemplates/claude-settings-managed.json`), parsed per OS; the live `~/.claude/settings.json` was not read, as the orchestrator's note says.
- "Sentence by sentence, no more": each sentence names a rendered value or quotes upstream behaviour of a named setting; the validator's refusals are named because the previous text already described the repository's rendering path and the parent task's goal makes the validator part of it. The manifest comment's reasons (certificate validation for `trustd`, bubblewrap closing Unix sockets and D-Bus) are kept as the one-clause "why".
- The value-check script of §5 (kept here so the section stays reproducible): it parses both OS blocks of the template as JSON after substituting `~` for the home-directory template variable, then asserts that the set of `host.tld` tokens in the section equals both `allowedDomains` lists; that the macOS and Linux `excludedCommands` equal the expected lists and each entry is named; that the non-agmsg `allowWrite` entries equal the expected per-OS lists and each is named; the Mach service, the socket path, the four flags, the `env` map, the allow rule and `defaultMode`; that the ask rules' subcommands and `gh api` forms equal the sets the section names; that no `git push` rule exists in `ask` or in the text; and that the ask list has 32 rules.

## Review, hook, cost

- Worker-side independent review: one round on `0b226806` by a fresh read-only subagent, `Verdict: correct`, no P0 to P2, four P3 (`dotfiles-T130-claude-sandbox-integration-followup-a01-worker-crit.json`, receipt `dotfiles-T130-claude-sandbox-integration-followup-a01-worker-review-receipt.md`). Three P3 are fixed in `bfcb0525`: the Linux socket block is the seccomp filter's, not bubblewrap's (upstream: the filter "adds Unix domain socket blocking"); `allowMachLookup` lists an additional service; the ask rules are counted (32) instead of called "every prefix form", and the prefix-rule escape is generalised to any flag order the prefixes do not spell out. One P3 is declared, not changed: the validator sentence describes the validator rather than a rendered setting (see Readings); the orchestrator decides whether it stays. The reviewer's risk note: on a Linux host without the sandbox runtime's seccomp filter, Unix sockets are not blocked at all, which the text does not say.
- No Understand-Anything hook prompt fired; no Plan Mode was used.
- cost: n/a (the runtime exposes no token or cost figure to the seat).
- CompactionDB: one decision added in this worktree's store before completion (validation §7).
