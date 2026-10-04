# AGMSG-TASK dotfiles-T97-claude-sandbox-github-calls-a01

Drafted 2026-10-04 by the orchestrator seat from the T69 audit finding (Worker Playbook step 4 vs. practice). Seat: a **Codex** worker, because `claude.sandbox` is a Claude seat's own execution boundary (T88 routing).

## Objective

Claude seats (orchestrator and workers) run `git fetch`/`git push` and every `gh` call outside their sandbox through the permission gate, although `claude.sandbox.network.allowedDomains` already lists `github.com`, `api.github.com`, `uploads.github.com`, `objects.githubusercontent.com` and `codeload.github.com`. Find out why those calls fail inside the sandbox and make them work there, so the step-4 exception written by T69 can be retired.

1. Reproduce from a Claude seat's sandboxed Bash (a scratch Claude session with the `express` profile is acceptable; never the operator's live session): `gh api user`, `gh pr view <n>`, `git fetch origin`, `git push --dry-run origin HEAD`. Record the exact failure (proxy refusal, DNS, credential store access such as `~/.config/gh/hosts.yml` or the keyring, SSH agent socket, or the auto-mode per-command `allowed_domains` requirement) with the `<sandbox_violations>` text where present.
2. Fix at the root in `home/dot_agents/agent-config.yaml` `claude.sandbox` (and only there, rendered through the generator): the missing domain(s) (for example `*.githubusercontent.com`, `ghcr.io`, the gh update check host), the credential path the sandbox must read, or the Unix socket (SSH agent) it must reach; one comment per entry with the reproduction that justifies it, as the existing entries have. If the cause is Claude Code's auto-mode proxy requiring per-command `allowed_domains`, document that no settings change can lift it and say so in the SKILL exception instead.
3. Verify from the scratch seat that the four calls above succeed inside the sandbox with no prompt, and paste the runs.
4. Update the SKILL's Worker Playbook step 4 exception text accordingly (retire it, or state the residual limit precisely), plus the rendered `claude-settings-managed.json` and the generator tests that pin the sandbox block.

Forbidden: `allowUnsandboxedCommands`, `excludedCommands` additions for `gh`/`git` (the point is to keep them sandboxed), permissions, hooks.

[memory:decision] dotfiles-T97 (orchestrator 2026-10-04): Claude seats make their GitHub calls inside the sandbox; the `claude.sandbox` block carries whatever domain, credential path or socket that needs, each justified by a reproduction, and the step-4 unsandboxed exception is retired or stated as a residual limit.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c fix/claude-sandbox-github-calls origin/main`. Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_agents/agent-config.yaml` (the `claude.sandbox` block), `home/.chezmoitemplates/claude-settings-managed.json` (rendered), `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_claude_settings_merge.py` (if it pins the sandbox block), `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (Worker Playbook step 4 sentence), `home/dot_config/claude/rules/agmsg-orchestration.md` (the matching bullet, if any)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T97-claude-sandbox-github-calls-a01.md` (written in your worktree if the main checkout is outside your write roots; the orchestrator moves them)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
make render-check
make validate-agent-assets
make unit-test
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing its reviews filtered to the head sha (agmsg-orchestration SKILL Worker Playbook step 15); fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if a Crit plan review ran.
3. Artifacts at the exact expected paths; validation with verbatim commands and raw output, PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text (from the main checkout if writable, else paste the command for the orchestrator to run); paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T97` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"`. `cost:` line. max_turns=30.

## Dispatch

- 2026-10-04 18:40Z to `codex-security-dot-a007` (Codex seat, security profile, `.claude/worktrees/worker-e`, pane wT:p8). Do items 1-3 first; item 4's SKILL sentence only after PR #253 (T69, in flight on the SKILL) has merged, with `gh pr update-branch` then. T90 follows on this seat.

## Re-task after the branch-setup block (orchestrator, 2026-10-04 19:00Z)

The branch ref `fix/claude-sandbox-github-calls` exists at origin/main; HEAD is still `chore/claude-auto-deny` with index and worktree equal to origin/main (the staged 359-file diff is the interrupted switch). Recover with `git switch fix/claude-sandbox-github-calls` (no tracking, no config write); if the index still shows the staged copy afterwards, `git reset -q` (index only; nothing of yours is lost because it equals origin/main). The stale `.git/config.lock` is gone. From now on on this seat: branches with `--no-track`, pushes as `git push origin <branch>`, PRs with `gh pr create --head <branch>`. Then continue the task from item 1.

## Re-task 2 (orchestrator, 2026-10-04 19:25Z) — documentation-only residual; auth provisioning moves to T90

The evidence is accepted: on Linux the Claude sandbox denies AF_UNIX socket creation, `allowUnixSockets` cannot grant a path there, so `gh` cannot reach the keyring and answers 401, while `git fetch`/`push` work. No settings-only fix exists within this task's boundary. Scope is therefore reduced to documentation; the credential design (a worker gh config dir with a file-stored token the sandbox can read) is folded into dotfiles-T90, which already introduces `GH_CONFIG_DIR` for worker seats.

1. After PR #253 (T69) merges, replace the step-4 exception sentence in the SKILL (and the matching rule bullet if T69 added one) with: "Run `git fetch`/`push` and `gh` inside the sandbox first. On Linux, `gh` backed by the host keyring answers HTTP 401 there because AF_UNIX socket creation is denied and `allowUnixSockets` cannot grant a path; until dotfiles-T90 provisions a sandbox-readable worker credential, a Claude seat's `gh` calls are the one class of commands it runs outside the sandbox through the permission gate, and every other out-of-sandbox action stays a blocked PONG."
2. Keep your five artifacts as they are (the raw evidence is the value of this task); no product file change beyond the sentence.
3. PR, CI, Bot wait, RESULT. The orchestrator records the `[memory:failure]` finding in CompactionDB from your report.

### PONG decision (orchestrator, 2026-10-04 19:40Z)

Allowed files gain the worker-side review evidence, named so they do not collide with the orchestrator's: `.orchestration/validation/dotfiles-T97-claude-sandbox-github-calls-a01-worker-crit.json` and `…-worker-review-receipt.md` (in your worktree; the orchestrator moves them). The orchestrator's own `-crit.json` and `-review-receipt.md` are written at acceptance.

### Go-ahead (orchestrator, 2026-10-04 23:35Z) — PR #253 merged as 04bce61b

T69 is on `main` (04bce61b). Branch from `origin/main` 04bce61b or later with `git switch -c <branch> --no-track origin/main`; apply Re-task 2 exactly (the Worker Playbook step-4 sentence in `home/dot_agents/skills/agmsg-orchestration/SKILL.md` now reads "The sandbox's GitHub domain allowance does not make `gh`/`git push` work there yet; dotfiles-T97 investigates and fixes that, after which the exception ends." — replace that clause with the finding and the T90 pointer; the rule bullet likewise), PR, CI, Bot wait per SKILL, RESULT with the worker-side `-worker-crit.json`/`-worker-review-receipt.md` in your worktree.

### Revise round 1 (orchestrator, 2026-10-05 00:10Z) — wording on 8ffa5547

Thread 4178090986 is dispositioned `not-applicable` by the orchestrator (Claude seats fetch inside their sandbox too: a005's T95 sandbox record lists `git fetch`, branch, commit and a push as sandboxed). Two text defects remain, same two files, one commit:

1. The exception must cover `git push` as well as `gh`: a Claude seat's pushes ran outside the sandbox in T72, T76 and T95 (`git push` over HTTPS asks `gh` for credentials, so it hits the same keyring 401). Write: "a Claude seat's `gh` calls and `git push` (whose credential helper is `gh`) are the one class of commands it runs outside the sandbox through the permission gate". `git fetch` stays inside the sandbox (no credential for a public remote).
2. The SKILL step now says "every other out-of-sandbox action stays a blocked PONG" twice (once inside the new sentence, once after the two documented cases); keep only the final one.

Then the unit docs tests (`uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v 2>&1 | tail -5; echo "rc=$?"`), push, CI, Bot wait per SKILL, RESULT. The orchestrator handles the thread and the artifact transfer again.

### Round 1 addendum (orchestrator, 2026-10-05 01:10Z) — no repeated Bot wait on update-branch heads

`main` advanced twice (T76 40993f20, T96 f6320f37) during your Bot waits. The Bot wait applies to a head that carries a new diff; a `gh pr update-branch` merge commit carries none, and the Bot already waited out 68e19ef7 in full. Send the RESULT as soon as CI is green on 5b6b0d9f (or on the then-current update-branch head), with `bot=none-on-<diff-head>` naming 68e19ef7; do not wait again. The orchestrator sequences `main` so that nothing else merges before PR 258.

### Round 1 addendum 2 (orchestrator, 2026-10-05 01:20Z) — Bot thread 4178339453 dispositioned

Not applicable, replied and resolved by the orchestrator: this regime's repository is public, so a worker's `git fetch` needs no credential; a private remote is outside the worker seats' scope and would join the same keyring exception that T90 closes. No text change. Send the RESULT now for head 5b6b0d9f (CI all pass); artifacts in your worktree as before.

### Revise round 2 (orchestrator, 2026-10-05 01:30Z) — task-level audit of 5b6b0d9f is `incorrect` (1)

The auditor is right that the rule and the SKILL are installed globally (`~/.config/claude/rules`, `~/.agents/skills`), so "this repository is public" cannot scope their wording. One phrase in both sentences, one commit: make the exception read "a Claude seat's `gh` calls, `git push` and any authenticated `git fetch` (a private HTTPS remote; the credential helper is `gh`) are the one class of commands it runs outside the sandbox through the permission gate". Keep "Run `git fetch`/`push` and `gh` inside the sandbox first." Docs tests (`uv run python -m unittest tests.unit.test_agmsg_orchestration_docs -v 2>&1 | tail -5; echo "rc=$?"`), prettier on the two files, push, CI green, then RESULT; no Bot wait beyond the diff head (addendum 1 stands), and `main` stays held for PR 258.
