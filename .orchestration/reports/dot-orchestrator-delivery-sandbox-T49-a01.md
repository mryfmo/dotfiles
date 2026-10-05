# Report: dot-orchestrator-delivery-sandbox-T49-a01

- status: ready_for_review
- worker: claude-standard-dot-a005 (worktree `.claude/worktrees/worker-c`)
- task_rev: 00ba4a201e6124f143134244eab52f40caabd5b07c7cf6d583cbd10b546cc844, verified at dispatch and re-checked before commit.
- branch: `fix/orchestrator-delivery-sandbox` from origin/main 9b60b4b. The worktree had been detached at origin/main after T44 merged.
- commit / head sha: `4452516050bc438eb814e59c101653b220a8396d` (all CI checks pass, nix skipped; mergeStateStatus CLEAN)
- PR: https://github.com/mryfmo/dotfiles/pull/219
- cost: 0 subagent dispatches, 1 advisor consult; about 85k context tokens consumed (session budget counter; no per-task figure exposed)

## Real-CLI probe: how the pane's claude pid is resolved

Verified on the worker's **own** pane only (`$HERDR_PANE_ID` = `wN:p2`). No other pane was read, and `herdr agent read` / `pane read` were not used. Verbatim output is in the validation file.

| Source | Command | Result on wN:p2 |
|---|---|---|
| session id (launcher side) | `herdr agent list` → `.result.agents[] \| select(.pane_id==P and .agent=="claude") \| .agent_session.value` | `bd93da57-…` |
| claude pid (launcher side) | `herdr pane process-info --pane P` → `.result.process_info.foreground_processes[] \| select(.name=="claude") \| .pid` | `15760` |
| both (in-pane, SessionStart) | `$CLAUDE_CODE_SESSION_ID`, `$CLAUDE_PID` (Claude Code exports both to every subprocess) | `bd93da57-…`, `15760`, and `ps` shows 15760 is `claude` |

The two routes agree. `herdr agent start` returns no pid, and `herdr agent list` carries no pid, so the pid comes from `pane process-info` (herdr's process API) rather than `pgrep`. `herdr pane process-info --help` shows `--pane <ID>`; the positional form is rejected (`unknown option`).

## Changes (one commit, 4452516)

1. **`home/dot_local/bin/common/executable_herdr-agents`:** new `claim_orchestrator_seat <workdir> <pane_id> [--self]`, placed after `is_main_checkout`.
   - **Guards, in order, all before any herdr call:**
     - `actas-claim.sh` and `identities.sh` exist;
     - the workdir is a git main checkout;
     - there is exactly one non-worker (no `-aNNN`) claude-code identity there, the same filter `ensure_worker_identity` uses.

     A worker pane in its worktree, a non-repo directory, or an ambiguous registration returns silently.
   - **Launcher side (no `--self`):** the sid and pid come from the two herdr probes above. The claim runs as `AGMSG_SELF_NAME=off AGMSG_RESOLVE_PROJECT=0 actas-claim.sh <workdir> claude-code <identity> <sid>.<pid>`. `AGMSG_SELF_NAME=off` is upstream's own switch (terminal-registry.sh). Without it, `actas-claim.sh` would rename *the caller's* pane, meaning the terminal running `herdr-agents`, to the orchestrator label, which `load_seat_labels` would then misread as the seat.
   - **`--self` (the SessionStart hook inside the pane):** it uses `CLAUDE_CODE_SESSION_ID`/`CLAUDE_PID` with self-naming on, because the caller *is* the pane. The environment is used only on this path, so a caller's own `CLAUDE_*` (for example an orchestrator running `herdr-agents` from its Bash) never leaks into a launcher-side claim.
   - **Output:**
     - `seat_claim=ok owner=<sid>.<pid>`;
     - `seat_claim=unresolved` when the sid or a numeric pid is missing, in which case nothing is claimed, so it never writes a bare-id lock;
     - `seat_claim=failed <first status line>` when `actas-claim.sh` refuses, for example `status=held owner=…`. This third outcome is not named in the task.
   - **Call sites:**
     - the end of `start_claude_in_pane`, which is the single function both the full-mode start and the existing-workspace heal (the task's "--attach heal") go through, so there is no second code path;
     - the `--attach` argument block right after the HERDR env check and **before** the `HERDR_AGENTS_LAYOUT=managed` early exit. The orchestrator pane `herdr-agents` creates is managed, so its SessionStart hook would otherwise exit before claiming.
   - The header gains one `@description` sentence. `shellcheck` is clean.
2. **`scripts/check-agent-runtime.py`** (`scripts/check-regime-boundary.sh` does not exist; T46 is not merged, so this is the task's stated fallback): new `orchestrator_seat_lock_warnings(project, skill_dir, proc)`, wired into `check()` (`make doctor`).
   - For the non-worker claude-code identities at the repository, it reads `run/actas.<team>__<name>.session` and warns when the owner has no `.<digits>` suffix while a `claude` process has its cwd in the repository (via `/proc/<pid>/comm` and `cwd`).
   - Off Linux the `/proc` scan finds nothing, and the check is silent by design.
   - It checks only the legacy lock path the task names. The id-keyed path `actas.<key>.session` is not resolved.
3. **`home/dot_agents/skills/agmsg-orchestration/SKILL.md`:**
   - one bullet in "Identity, delivery, and storage": the composite lock, the `cat` check, the silent skip from a sandboxed claim, the `herdr-agents` claim and `seat_claim=` output, the doctor WARN, the Monitor "no longer alive" limitation, turn delivery as the working path, and the worker's `agmsg-dispatch` wake;
   - one addition to Worker Playbook step 11: RESULT/PONG to a herdr-paned orchestrator go through `agmsg-dispatch <team> <worker> <orchestrator> <pane_id>`, not bare `send.sh`.
4. **`home/dot_config/claude/rules/agmsg-orchestration.md`:** one bullet with the same content in rule form.
5. **Tests:**
   - `test_herdr_agents.py`, 3 new tests:
     - pane start claims `sid-test.4343` (the call log pins `resolve=0 self_name=off`);
     - pane start without a session prints `seat_claim=unresolved` and makes no `actas-claim` call;
     - the SessionStart `--attach` in a **managed** pane claims `sid-self.777` with `self_name=on`.

     The fake herdr reports the orchestrator session and a foreground `claude` for `w-test:p1` only when a flag file is set and only after `agent start claude-orchestrator`, so the shell-prompt waits are unaffected. `run_helper` and `run_attach_helper` now drop `CLAUDE_CODE_SESSION_ID`/`CLAUDE_PID`, which `make unit-test` inherits from the running Claude session.
   - `test_check_agent_runtime.py`, 2 new tests with a fake agmsg dir and a fake `/proc`:
     - a bare id warns, and the worker's own bare lock (`-a005`) is not reported;
     - a composite id is quiet, and no live claude is quiet.

     `test_check_includes_ua_core_warnings` now patches the new check, so it never scans the real machine.
   - **Negative check:** all five new tests fail against the origin/main scripts (3 FAIL, 2 ERROR for the missing function).

## Deviations and notes

- **`agmsg-dispatch` form:** the real CLI is `agmsg-dispatch <team> <from> <to> <pane_id> <message>`, with a pane id like `wN:p1`, not `<socket>:<pane>` as the task wrote. The docs use the real form and add that the dispatch needs the herdr socket, so from sandboxed Bash on Linux it goes through the unsandboxed retry.
- **Full-mode timing:** right after `herdr agent start`, herdr may not have the session yet. The launcher-side claim then prints `seat_claim=unresolved`, and the SessionStart `--self` claim in the same pane lands `ok`. This is expected, not a failure. I added no wait.
- **`/clear` and `/compact`:** these give a new sid in the same claude process. The old composite's pid is still alive, so `actas-claim.sh` will likely answer `status=held`, printed as `seat_claim=failed status=held owner=…`. This is documented, not fixed, because it is upstream's liveness rule.
- **Mirror check:** `home/dot_config/codex/AGENTS.md` does not mirror the agmsg rule (no `agmsg-dispatch`/`actas` mention), so no mirror gap.
- **Live lock untouched:** the live orchestrator lock `run/actas.dotfiles__claude-remediation-dot.session` was never read, claimed or touched. The doctor tests use fakes. The real doctor was not run against it.
- **Understand-Anything hook:** it fired after the commit. I did not act on it.
- **Effect:** at the operator's next `chezmoi apply`, the next pair start or SessionStart in the orchestrator pane writes the lock as `<sid>.<pid>`, visible in `cat ~/.agents/skills/agmsg/run/actas.dotfiles__claude-remediation-dot.session` and in `herdr-agents.log` as `seat_claim=ok owner=…`.

[memory:decision] T49: the orchestrator seat lock must hold the composite `<sid>.<pid>`; a claim from sandboxed Bash writes a bare sid and the Stop-hook delivery then skips silently (`other:`), and a `watch.sh` Monitor cannot run under the pid-namespaced sandbox — herdr-agents claims the seat outside the sandbox at pane start and a herdr-paned orchestrator is woken by worker `agmsg-dispatch` (operator correction 2026-10-01).

## CompactionDB (main checkout)

Memory id **2b18cc6f-8995-4b14-bff0-db7e1e127512**. The command and output are in the validation file:

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] text above>"
```

## Effects

None outside the repository working tree. The launcher and doc changes take effect at the operator's `chezmoi apply`.

## Revision 2 (orchestrator status=revise 04:17:07Z; amendment r2; task_rev 3c71b553…1890 verified)

All four findings are fixed in **50ebfdc**, on 4452516, and amendment r2-b is in **68ac54d** on top. There was no force push. PR #219 head: `1fa2a483fad7ad2dc8e7f24ec606d9d80985b51a` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

1. **`--self` no longer depends on `CLAUDE_CODE_SESSION_ID`/`CLAUDE_PID`** (Codex GitHub P1).
   - **Session id:** the `--attach` block reads the SessionStart payload from stdin with the same pattern as upstream `check-inbox.sh`:
     - a `[ ! -t 0 ]` guard;
     - a 2 s bound: first `timeout 2 cat` as upstream, replaced in 99d734b by bash's own `read -r -t 2 -d ''` (see the CI fix below);
     - `sed` extraction of `"session_id"`.

     It exports the value to `claim_orchestrator_seat` as `HOOK_SESSION_ID`. Precedence is the payload, then `CLAUDE_CODE_SESSION_ID`, then the herdr `agent list` lookup on `$HERDR_PANE_ID`.
   - **Pid:** the new `claude_ancestor_pid` walks `ppid` from `$$`, at most 20 hops, to the first ancestor whose `comm` is `claude`, as upstream `agmsg_agent_pid` does. Like upstream, `AGMSG_AGENT_PID` overrides it: a numeric value is used as is, and a set but empty value skips the walk. Precedence is the walk, then `CLAUDE_PID`, then `herdr pane process-info --pane $HERDR_PANE_ID`.
   - A bare id is still never written (`seat_claim=unresolved`).
2. **Same-session bare lock is repaired** (audit P2 `:421`). On `status=held team=<T> owner=<X>` with `<X>` equal to our bare session id, a subshell sources upstream `lib/actas-lock.sh` (with `SKILL_DIR` exported) and calls `actas_lock_release <T> <identity> <sid>`. That function is upstream's owner-exact delete: it removes the lock only when the owner token matches exactly, and it resolves the id-keyed or legacy path itself. The claim then runs again and prints `seat_claim=ok owner=<sid>.<pid> replaced_bare_lock=yes`. Any other owner stays `seat_claim=failed <status line>`, with no release. The doctor WARN's repair line now reads "Run `herdr-agents --attach` from the orchestrator pane outside the sandbox (it replaces a same-session bare lock)".
3. **Wake path without worker escalation** (audit P1 SKILL; operator decision). `claude.sandbox.excludedCommands: [agmsg-dispatch]` has a comment that carries:
   - the E2E evidence: from sandboxed Bash the herdr socket is PermissionDenied (T39 leg 1), and outside the sandbox `agmsg-dispatch` delivered msgs 545–577 with `read_at` within seconds; the script inserts one agmsg row and sends a herdr wake;
   - the **verified matching semantics** from code.claude.com/docs/en/settings-reference (`sandbox.excludedCommands`): "Name commands … array of command names … For compound commands or pipes, Claude Code checks only the first word", so this is a first-word name match, not a prefix or glob;
   - **"An excluded command still goes through permission prompts unless a rule allows it."**

   The template is regenerated (only `excludedCommands` changed) and `make render-check` is green. No validator or test pinned `excludedCommands: []` on the real manifest; the generator sample test's `[]` is a synthetic manifest.

   Docs:
   - SKILL step 11 and the rule bullet now say that workers send RESULT/PONG to a herdr-paned orchestrator with `agmsg-dispatch`, which the manifest excludes from sandboxing: it runs outside the sandbox from the first attempt, with no failed sandboxed run, no unsandboxed retry and no escalation. Claude Code still applies its permission rules, and Codex workers are outside this setting. The "unsandboxed retry" wording for the dispatch is gone.
   - README: `agmsg-dispatch` is removed from the list of retry-prompt commands, and one passage covers the new entry, its evidence, the first-word match, permission rules, and Codex being unaffected.

   **Gap found, then closed by r2-b:** the docs quote above means `excludedCommands` alone does **not** remove the prompt. The manifest's `permissions` has only `deny` and `ask` rules, so without `permissions.allow: Bash(agmsg-dispatch:*)`, or a permgate rule, the worker's dispatch still raises a normal permission prompt, answered by the human. That is not agent escalation, but it is not prompt-free either. Adding the allow rule was outside r2's `allowed_files`, so 50ebfdc did not add it. I flagged it in the PONG (msg 580), and the orchestrator answered with amendment r2-b (below).
4. **Tests** (audit P2), 4 new:
   - `test_session_start_attach_reads_the_hook_payload_and_herdr_pid`: stdin `{"session_id":"sid-stdin",…}`, no `CLAUDE_*` variables, `AGMSG_AGENT_PID=""`, and the pid from the fake `pane process-info --pane w-attach:p1` give `seat_claim=ok owner=sid-stdin.4343`.
   - `test_seat_claim_replaces_a_same_session_bare_lock`: the first claim answers `held … owner=sid-stdin`, which leads to `actas_lock_release dotfiles claude-remediation-dot sid-stdin skill_dir=<home>/.agents/skills/agmsg`, a second claim, and `replaced_bare_lock=yes`.
   - `test_seat_claim_held_by_another_session_fails_without_release`: owner `other-sid.999` gives `seat_claim=failed status=held …` and no release.
   - `test_managed_claude_sandbox_excludes_agmsg_dispatch`: the rendered template contains `agmsg-dispatch`.

   Changed tests:
   - The r1 `--self` env test now sets `AGMSG_AGENT_PID=""`. The ppid walk itself is **not unit-testable**: the suite may run under a real claude, as it does here, and the walk would find it. The override pins the env fallback instead.
   - `run_attach_helper` passes stdin explicitly (payload or `/dev/null`).

   Negative check (§r2): all 4 fail against 4452516.

**Checks** (verbatim in the r2 validation section, every exit captured directly):
- `make render-check`: up to date, exit 0.
- `make unit-test`: 643 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: ok, exit 0.
- `shellcheck`: exit 0.
- `gh pr checks 219`.
- base-ok: **exit 1**, because origin/main gained 3b851b0, which touches **only `.orchestration`** (T44 r2 acceptance). The amendment asks for one commit, so I did not add a merge commit. The PR is CLEAN and the branch's code base is current.

### Live verification checklist (orchestrator, after the operator's `make update` and relaunch)

Acceptance is final only after both legs show every item:

| # | Item | Leg A: fresh pair start (`herdr-agents` full mode) | Leg B: persisted restore (herdr session restore, then SessionStart) |
|---|---|---|---|
| 1 | `~/.config/herdr/herdr-agents.log` has `seat_claim=ok owner=<sid>.<pid>` for the orchestrator pane. A preceding launcher-side `unresolved` is expected in leg A. | ☐ | ☐ |
| 2 | `cat ~/.agents/skills/agmsg/run/actas.dotfiles__claude-remediation-dot.session` shows `<sid>.<pid>`, and `<pid>` is the pane's `claude` (`herdr pane process-info --pane wN:p1`) | ☐ | ☐ |
| 3 | A worker RESULT/PONG is delivered by the orchestrator's Stop hook (`decision: block` with the message) with no manual `messages.db` read | ☐ | ☐ |
| 4 | The worker's `agmsg-dispatch <team> <worker> <orchestrator> wN:p1 "…"` from a sandboxed Claude worker runs unsandboxed on the first attempt, raises **no permission prompt** (the `Bash(agmsg-dispatch:*)` allow rule), and wakes p1 | ☐ | ☐ |
| 5 | If a bare lock was left from before: `seat_claim=ok … replaced_bare_lock=yes` once, then item 2 holds | ☐ | ☐ |

**Notes**
- The Understand-Anything hook fired after the commit. I did not act on it.
- The live orchestrator lock was not read or touched.
- CompactionDB (main checkout): **ea6729a4-36ed-4206-8638-05ea265a01e0** for r2. The r1 decision 2b18cc6f stays valid; r2 adds the resolution, repair and dispatch exclusion.

[memory:decision] T49 r2: the SessionStart seat claim takes the session id from the hook payload on stdin and the pid from the nearest claude ancestor (env and herdr lookups as fallbacks), replaces a lock held by its own bare session id via the owner-exact actas_lock_release, and agmsg-dispatch is in claude.sandbox.excludedCommands so Claude workers wake a herdr-paned orchestrator without a sandbox failure or retry (Claude Code still applies permission rules: an allow rule is needed for no prompt) (2026-10-01).

cost (revision 2): 0 subagent dispatches; about 45k context tokens consumed this round (session budget counter; no per-task figure exposed).

## Revision 2-b (amendment r2-b, task_rev 42057013…2bef verified; PING 04:41:07Z)

One more commit, **68ac54d**, on 50ebfdc (no force push). PR #219 head: `1fa2a483fad7ad2dc8e7f24ec606d9d80985b51a` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

- **Manifest:** `home/dot_agents/agent-config.yaml` `claude.permissions.allow: [Bash(agmsg-dispatch:*)]`, with the comment "The only managed allow rule: agmsg-dispatch inserts one agmsg row and sends a herdr wake, the sanctioned worker-to-orchestrator wake (T49)".
- **Generator:** `scripts/generate-agent-configs.py` renders `permissions.allow` when the manifest has it. Before this, the generator emitted only `deny`, `defaultMode` and `ask`, so this one passthrough is required for the rule to reach the template. The generator is not named in r2-b's allowed files, but the amendment's "regenerate the template" depends on it. The sample manifests without `allow` still render without it.
- **Validator:** `scripts/validate-agent-assets.py` had no shape check on `allow`. The new `validate_claude_permissions_allow` requires a list of non-empty strings and is called from `validate_claude_settings` on the rendered template.
- **Tests:**
  - `test_managed_claude_sandbox_excludes_agmsg_dispatch` also asserts that the rendered `permissions.allow == ["Bash(agmsg-dispatch:*)"]`;
  - the new `test_claude_permissions_allow_must_list_non_empty_rules` accepts `{}`, `[]` and the rule, and rejects a string, `[""]` and `[3]`.
- **Template:** regenerated. The only change is the new `allow` array, and `make render-check` is green. The rendered values are `{"permissions.allow": ["Bash(agmsg-dispatch:*)"], "sandbox.excludedCommands": ["agmsg-dispatch"]}`.
- **README, SKILL and rule:** the managed settings allow `Bash(agmsg-dispatch:*)`, so the dispatch runs without a prompt. The README also states the impact.
- **The settings merge** (`modify_private_settings.json`) replaces the whole managed `permissions` key, as it already did for `deny`/`ask`. Local `permissions.allow` entries in `~/.claude/settings.json` were already overwritten before this change, so there is no new loss.

**User-visible impact: this is the first managed `permissions.allow` entry. After the operator's next `make update` / `chezmoi apply`, every Claude session using the managed settings can run `agmsg-dispatch` without confirmation, and outside the Bash sandbox (via `excludedCommands`).**

**Checks** (verbatim in the r2-b validation section, every exit captured directly):
- `make render-check`: exit 0.
- `make unit-test`: 644 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- `gh pr checks 219`.

CompactionDB (main checkout): **5e42e6d7-dca0-41d6-aed3-753992e76359**.

[memory:decision] T49 r2-b: the managed Claude settings carry exactly one permissions.allow rule, Bash(agmsg-dispatch:*), because sandbox.excludedCommands alone still prompts; every Claude session using the managed settings can run agmsg-dispatch without confirmation (operator decision 2026-10-01).

## CI fix after r2-b (99d734b)

CI on 68ac54d failed. There were two causes:
- **`public-bootstrap` (3 jobs):** `chezmoi: .local/share/fonts/Hack: https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/Hack.zip: 500 Internal Server Error`. This is an external download failure, unrelated to this PR, and it passes on rerun.
- **`test (macos-14, client)`:** the three stdin-based seat-claim tests saw `seat_claim=unresolved`. The macOS runner has no GNU `timeout`, so the `command -v timeout` guard skipped the payload read, which is the same fail-open behaviour as upstream. `test (ubuntu-latest, client)` passed all Python tests; fail-fast cancelled its later step.

**Fix:** the payload read now uses bash's own `IFS= read -r -t 2 -d '' hook_payload || true`. It keeps the 2 s bound, ends at EOF, works in bash 3.2, and needs no coreutils. On the operator's Linux host the behaviour is unchanged.

Checks at 99d734b: `make render-check`, `make unit-test` (644 tests OK), `make validate-agent-assets` and `shellcheck` all pass. CI is in the r2-b validation section.

This is one commit more than r2-b's "one more commit", because it is a CI-required fix.

## Revision 2-c (amendment r2-c, task_rev 853c3ef0…bb5a verified; PING 05:06:26Z)

This round fixes the remaining P2 from the audit of 50ebfdc, in one more commit, **1fa2a48**, on 99d734b. There was no force push. PR #219 head: `1fa2a483fad7ad2dc8e7f24ec606d9d80985b51a` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

- **The problem:** `actas-claim.sh` stops at the first `held` team and rolls back the teams it already claimed. The single release-and-retry therefore failed for an identity registered in two teams that both hold same-session bare locks.
- **The fix:** `claim_orchestrator_seat` now loops. The bound is `teams` = the number of distinct teams `identities.sh <repo> claude-code` lists for the identity. While the claim answers `status=held team=<T> owner=<our bare sid>`:
  - it releases that team's lock through upstream's owner-exact `actas_lock_release <T> <identity> <sid>`;
  - it claims again;
  - it allows at most `teams` releases, so `teams + 1` claim attempts.

  When a claim succeeds after any release, it prints `seat_claim=ok owner=<sid>.<pid> replaced_bare_lock=yes`. Any other owner, a release failure, or the bound reached ends as `seat_claim=failed <status line>`.
- **Tests** (2 new):
  - `test_seat_claim_replaces_same_session_bare_locks_in_every_team`: the fake answers `held team-a owner=sid-stdin`, then `held team-b owner=sid-stdin`, then `ok`. The run releases team-a, then team-b, makes 3 claims, and ends `replaced_bare_lock=yes`.
  - `test_seat_claim_fails_when_a_later_team_is_held_by_another_session`: team-a is held by our bare id and team-b by `other-sid.999`. The run releases team-a only and ends with `seat_claim=failed status=held team=team-b owner=other-sid.999`.

  The fake `actas-claim.sh` now answers from a per-call sequence. The earlier single-team tests use the same fake with one `held` entry.
- **Negative check against 99d734b** (validation r2-c section): the every-team test **fails** there; the old code printed `seat_claim=failed status=held team=team-b owner=sid-stdin`. The other-owner test passes on both versions, because a single retry also ends in `failed` there. It pins the correct behaviour but does not discriminate the change.

**Checks at 1fa2a48** (verbatim in the r2-c validation section):
- `make render-check`: exit 0.
- `make unit-test`: 646 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- CI on both OSes: `gh pr checks 219` is in the validation file.

CompactionDB (main checkout): r2 **ea6729a4-36ed-4206-8638-05ea265a01e0**, r2-b **5e42e6d7-dca0-41d6-aed3-753992e76359**; r2-c changes no decision.

## Revision 2-d (amendment r2-d, task_rev 79622c2b…e219 verified; PING 05:23:34Z) and 2-e (amendment r2-e, appended to the task file after that dispatch; current task file sha256 34fe33e0…)

Two more commits on 1fa2a48, with no force push:
- **e4903a1**, r2-d: test plus comment.
- **63d4e03**, r2-e: fix plus test.

PR #219 head: `9dc4e539f8ac004edc026327189cf74a5c7f0d97` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

**r2-d (audit of 99d734b, P2).** On a `read -t` timeout, bash 3.2 discards the partial payload, while bash 4+ keeps it. I kept `read -t`, so there is no GNU `timeout` dependency. The comment now states that on bash 3.2 the herdr lookup (`herdr agent list` → `agent_session.value`) then supplies the session id, so the claim still lands, and that the result is `seat_claim=unresolved` only when that lookup fails too.
- New regression test `test_session_start_attach_claims_when_the_hook_keeps_stdin_open`: a producer thread writes `{"session_id":"sid-self"}` with no newline into an `os.pipe`, keeps it open for 3 s, then closes it. With `AGMSG_AGENT_PID=777`, the test expects `seat_claim=ok owner=sid-self.777`.
- The fake `herdr agent list` now also reports that sid for `w-attach:p1`. Linux CI (bash 5) passes through the kept payload. macOS CI (`/bin/bash` 3.2, which the test PATH resolves) passes through the herdr fallback.
- `run_attach_helper` gained a `stdin_fd` option.

**r2-e (Codex GitHub comment `:464`).** On a persisted-session restore, the new claim is `<sid>.<new pid>` while the lock may still hold `<sid>.<old pid>`. Upstream reclaims a positively dead pid, but a "cannot tell" or reused pid stayed held, and the repair released only a bare `sid`.
- A held owner now counts as ours when it is the bare `sid` **or** `<sid>.<digits>` (`${owner%.*} == sid` and a numeric `${owner##*.}`). A process with our session id can only be this session's predecessor.
- That **exact owner token** is released with `actas_lock_release <team> <identity> <owner>`, and the claim is retried in the same bounded per-team loop.
- **The output flag is renamed `replaced_bare_lock=yes` → `replaced_stale_lock=yes`.** The docstring and loop comment are updated, and the doctor hint now reads "(it replaces a same-session stale lock)". No SKILL, rule or README text named the flag.
- New test `test_seat_claim_replaces_a_same_session_composite_lock_of_another_pid`: held `owner=sid-stdin.111` leads to `actas_lock_release dotfiles claude-remediation-dot sid-stdin.111`, a re-claim, and `seat_claim=ok owner=sid-stdin.4343 replaced_stale_lock=yes`.
- The other-owner tests (`other-sid.999`) still end in `failed` without a release.
- **Negative check against e4903a1:** the new test fails there with `seat_claim=failed status=held team=dotfiles owner=sid-stdin.111`.

**Checks at 63d4e03** (verbatim in the r2-d/e validation section):
- `make render-check`: exit 0.
- `make unit-test`: 648 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- `gh pr checks 219` on both OSes.

**Live checklist addition** for leg B, the persisted restore: if the lock still held `<sid>.<old pid>`, expect `seat_claim=ok … replaced_stale_lock=yes` once (checklist item 5 now reads "stale" rather than "bare").

## Revision 2-f (amendment r2-f, task_rev 0799cfd5…6ed3 verified; PING 05:46:37Z)

One more commit, **9dc4e53**, on 63d4e03. There was no force push. PR #219 head: `9dc4e539f8ac004edc026327189cf74a5c7f0d97` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

**The problem** (audit of 63d4e03, P1): parallel `claude --resume`/`--continue` processes share a session id, so releasing a held `<our sid>.<other pid>` could take a **live** sibling's seat.

**The rule now:**
- A same-session composite owner is stale only when its pid is positively dead.
- A bare `<sid>` owner stays ours, because it can only come from a sandboxed claim of this session.
- A live or unprovable pid ends the loop as `seat_claim=failed`, with no release.

**Liveness check:** `ps -p <pid>` instead of matching the `kill -0` "No such process" message. The kill message is locale-dependent; this host's locale is Japanese, and the message would read そのようなプロセスはありません. `ps -p` reports any visible process, including one owned by another user (the EPERM case), so such a pid counts as alive, matching the amendment's "EPERM counts as alive". The hook and the launcher run outside the sandbox, so pids are visible.

**Wording:** the docstring and the doctor hint now say "stale lock: bare, or same-session composite whose pid is dead".

**Tests:**
- `test_seat_claim_replaces_a_same_session_composite_lock_of_a_dead_pid` (renamed from the r2-e test): the owner is `sid-stdin.<pid of a spawned and reaped child>`, which gets released, re-claimed, and ends `replaced_stale_lock=yes`.
- `test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_pid`: the owner is `sid-stdin.<test process pid>`, which gives `seat_claim=failed status=held …` and no release.

**Negative check against 63d4e03:** the live-pid test **fails** there (the old code printed `seat_claim=ok … replaced_stale_lock=yes`, releasing the live owner). The dead-pid test passes on both versions, as the expected outcome is the same.

**Checks at 9dc4e53:**
- `make render-check`: exit 0.
- `make unit-test`: 649 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- CI on both OSes: in the validation file.

## Revision 3 (orchestrator status=revise 06:09:38Z; amendment r3; task_rev bcea5859…ec72 verified)

All three items are fixed in one commit, **9b658a9**, on 9dc4e53. There was no force push. PR #219 head: `229896a9ae08370d64d1002219d59946a1ca9dcc` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

1. **SessionStart claim limited to the orchestrator pane** (P2 `:1432`).
   - **The check:** in `--self`, `claim_orchestrator_seat` reads the pane's label with `herdr pane list --workspace <ws>` and requires either `claude-orchestrator` (legacy) or `<team>:<identity>`, the self-named orchestrator seat label, for any team in which `identities.sh` lists the identity. Any other Claude pane in the main checkout prints `seat_claim=skipped reason=not-orchestrator-pane` and claims nothing.
   - **Managed panes:** `herdr-agents` labels a managed pane (`rename_pane_unless_seat_named … claude-orchestrator`) before it starts claude, so the claim stays in the early `--attach` path and exits right after.
   - **Unmanaged panes:** the claim moved to just after the attach flow's `rename_pane_unless_seat_named "${claude_pane_id}" claude-orchestrator`, so it runs after that flow has excluded worker panes and labelled this pane.
   - **Alternative not used:** the amendment's "or the first pane of the managed workspace" check is not needed, because the label check already covers it.
   - **Test:** `test_session_start_attach_skips_a_pane_that_is_not_the_orchestrator` uses a `claude-worker` label, expects `skipped`, and checks there is no `actas-claim` call. It fails against 9dc4e53, which claimed (`seat_claim=ok owner=sid-stdin.4343`). The other `--self` fixtures now label `w-attach:p1` as `<team>:claude-remediation-dot`.
   - **Not tested:** the unmanaged-pane path (claim after the attach rename) has no separate test.
2. **Payload kept on macOS** (P1 `:1429`).
   - **Byte-wise read:** the single `read -t 2 -d ''` is replaced with byte-wise accumulation, `while IFS= read -r -t 2 -n 1 hook_byte; do hook_payload+="${hook_byte}"; done`, which ends on EOF or the first 2 s timeout. bash 3.2 then loses at most the byte in flight. Newlines are dropped, which is harmless for the one-line `session_id` extraction.
   - **Herdr retry:** the `herdr agent list` lookup stays the fallback and retries up to 3 times, 1 s apart, while the session is not listed. That covers herdr not knowing it right after start. It applies to both the launcher side and `--self`.
   - **Test:** `test_session_start_attach_claims_when_the_hook_keeps_stdin_open` now runs with the fake herdr lookup returning **nothing**, so only the payload path can produce `seat_claim=ok owner=sid-self.777`. On this host (bash 5.2) the old code also passes it. The bash 3.2 proof is the macOS CI job, where the test PATH resolves `/bin/bash` 3.2.
3. **Manifest comment on `permissions.allow`:** it now quotes the docs **verbatim**, checked against code.claude.com/docs/en/permissions: "Claude Code is aware of shell operators, so a rule like `Bash(safe-cmd *)` won't give it permission to run the command `safe-cmd && other-cmd`. … A rule must match each subcommand independently." It adds: "excludedCommands matches the first word only; the allow rule still requires every subcommand to match, so a chained command prompts". The render output is unchanged, since the comment is manifest-only.

**Checks at 9b658a9** (verbatim in the r3 validation section):
- `make render-check`: exit 0.
- `make unit-test`: 650 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- `gh pr checks 219` on both OSes.

**Live checklist addition** for both legs: a Claude pane in the main checkout that is *not* the orchestrator (for example a second claude) logs `seat_claim=skipped reason=not-orchestrator-pane` and leaves the lock unchanged.

**CI at 9b658a9:** every job succeeded, including `test (macos-14, client)` (job list in the validation file). So the payload-only open-pipe test passed on macOS `/bin/bash` 3.2, which settles r3 item 2.

## Revision 3-b (amendment r3-b, task_rev a7dde83f…486d verified; PING 06:36:51Z)

One more commit, **229896a**, on 9b658a9. There was no force push.

**The problem** (audit of 9b658a9, P2): the byte-wise `read -t 2` restarted its timeout on every byte, so a producer that trickles input held the hook past its budget.

**The fix:**
- The loop is now `hook_deadline=$((SECONDS + 2)); while ((SECONDS < hook_deadline)) && IFS= read -r -t 1 -n 1 hook_byte; do …; done`, an overall deadline of about 2–3 s.
- EOF still ends it early.
- With an incomplete payload, the herdr lookup supplies the session id.
- The comment states the deadline.

**Test** `test_session_start_attach_bounds_a_trickling_hook_payload`:
- **Setup:** a producer writes one byte every 0.5 s for 6 s, and the fake herdr lookup answers `sid-herdr`.
- **Result:** the hook finished in under 4.5 s and gave `seat_claim=ok owner=sid-herdr.777` (herdr fallback, payload incomplete).
- **Negative check against 9b658a9:** it **fails** there, with **6.04 s** elapsed (the old per-byte timeout kept reading).

**Checks at 229896a:**
- `make render-check`: exit 0.
- `make unit-test`: 651 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- CI on both OSes: in the validation file.

PR #219 head: `229896a9ae08370d64d1002219d59946a1ca9dcc` (final head; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

## Revision 3-c (orchestrator status=revise 07:07:24Z; amendment r3-c; task_rev 24e712f2…ffd1 verified)

One commit, **11d87f3**, on 229896a. There was no force push. PR #219 head: `00268f174098f19fdbaede7bf5540b4c42674ca6` (final head, after the 00268f1 CI fix; all CI checks pass on Linux and macOS, nix skipped; mergeStateStatus CLEAN).

**The problem** (Codex GitHub comment `:490`): on a restore, a recycled pid makes `ps -p` succeed, so a stale `<sid>.<old pid>` lock was kept and the new claim ended `failed`.

**The fix:** a same-session composite owner is now live only when `ps -o comm= -p <pid>` is `claude`. The script compares the basename, because macOS `ps` prints the executable path.
- A dead pid (empty output) and a recycled pid that is not claude are both stale. That exact owner is released, and the claim retries.
- A running claude with our session id stays a parallel `--resume`/`--continue` sibling and gives `seat_claim=failed`, with no release.
- The docstring, loop comment and doctor hint now say "same-session composite whose pid is dead or not a claude process".

**Tests:**
- `test_seat_claim_keeps_a_same_session_composite_lock_of_a_live_claude` (renamed from the live-pid test) now uses a real live process whose comm is `claude`: `sleep` copied to `<tmp>/claude` and run with `30`. The test expects `seat_claim=failed status=held …` and no release, and cleans the process up with `addCleanup` kill/wait.
- New `test_seat_claim_replaces_a_same_session_composite_lock_of_a_recycled_pid`: the owner is `sid-stdin.<this test's python pid>`, a live process that is not claude. The test expects a release, a re-claim and `replaced_stale_lock=yes`.
- The dead-pid test is unchanged and still passes.

**Negative check against 229896a:** the recycled-pid test **fails** there (`seat_claim=failed status=held team=dotfiles owner=sid-stdin.<pid>`). The live-claude test passes on both versions, as the outcome is the same.

**Checks at 11d87f3:**
- `make render-check`: exit 0.
- `make unit-test`: 652 tests OK (1 skipped), exit 0.
- `make validate-agent-assets`: exit 0.
- `shellcheck`: exit 0.
- CI on both OSes: in the validation file.

**CI fix after r3-c (00268f1).** CI on 11d87f3 failed only in `test (macos-14, client)`: `PermissionError: [Errno 1] Operation not permitted: '…/claude'`. The live-claude test used `shutil.copy2` of `/bin/sleep`, and macOS refuses to copy that file's flags. The Ubuntu jobs passed every Python test; fail-fast then cancelled their later steps (`##[error]The operation was canceled.`). The fix is test-only: `shutil.copyfile` (contents) plus `chmod 0o755`. There is no product change. The failing `gh pr checks` output is pasted alongside the final one.
