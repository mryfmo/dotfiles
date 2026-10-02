# Report: dot-upgrade-pin-path-codify-T54-a01

- worker: claude-standard-dot-a005 (claude-code, standard profile), worktree worker-c
- task_rev: edba9d79d973bc84c1692137f8bd099366144b5a1aa2dfb397b146264b8750c0 for Revise round 2, after 94a4a4a0…1c92 for round 1 and 92670f30…84f6 for round 0. I checked each with sha256sum and each matches.
- branch: `chore/upgrade-pin-path` from origin/main 00ce4f6e (T53 merged as #224). There are three commits, all pushed: **2360aea** (round 0), **c636452** (round 1) and **1128abb** (round 2).
- PR: https://github.com/mryfmo/dotfiles/pull/225, head `1128abb326d4a1fb0f50d5b505adbbb9f85de270`. The PR description is updated for round 2. mergeStateStatus is CLEAN. CI on 1128abb is green: every check passes and `nix` is skipped. In each `test` job (macOS 14 and both Ubuntu jobs) the steps `Run Python unit tests` and bats `Run unit test` succeeded.
- cost: n/a. The runtime exposes no per-session figures. I used two advisor consultations (round 0) and no subagents.

## Changes

1. **Rule text** (`home/dot_config/claude/rules/agmsg-orchestration.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, README "Tool versions" and the zenbu pin paragraph):
   - **Pin flow:** "Give `make upgrade` mise config/lock changes their own chore commit" and the SKILL's "separate chore" sentence are replaced with the true procedure. The operator runs `make upgrade` in the canonical clone. The whole pin diff, not only the config/lock pair, travels in one worker task as a class-pure PR that also syncs the `tests/**` expected versions (T37 #209, T53 #224). It passes `make require-crit-review` before the orchestrator merges it under the acceptance exemption.
   - **Activation case:** when the bus exists but no worker is seated, the orchestrator seats one before any mutation, with `herdr-agents --restart-worker` in the pair or `--add-worker <worktree>` otherwise. "No worker" is never an implicit opt-out. Both the rule and the SKILL activation bullet say so, and they also note that the SessionStart hook prints this as an `agmsg-orchestration:` line.
   - **New bullet in the rule and the SKILL:** the orchestrator never pushes a repository change to `main`. Its only direct pushes are the boundary commit (`ORCH_PUSH_MAIN=boundary`) and a locally made acceptance merge (`ORCH_PUSH_MAIN=acceptance`). The pre-push guard enforces this and logs each decision. The SKILL Stop checklist now says to push the boundary commit with `ORCH_PUSH_MAIN=boundary`, so the guard does not break the regime's own procedure.
   - **Not changed:** the Codex `AGENTS.md` does not carry the clause. `agent-config.yaml` has only a pin comment, and no rendered file carries the clause. Neither was changed; the grep is in the validation file, and `make render-check` stays clean.
2. **Hook-injected activation** (`executable_herdr-agents`):
   - **`print_regime_directive`** prints one `agmsg-orchestration:` line, but only when DIR is a git main checkout, has exactly one orchestrator (non `-aNNN`) claude-code identity, and the manifest names a worker worktree. The line says:
     - invoke the skill before any other action;
     - delegate repository mutations, `make upgrade` pin diffs included;
     - seat a worker first if none is seated;
     - declare exemptions in one line;
     - do not push to main without the guard override.
   - **`claim_seat_and_print_directive`** wraps both SessionStart `--self` claim sites, the managed pane and the unmanaged attach. It prints the directive after `seat_claim=` unless the claim was `skipped` for a pane that is not the orchestrator's.
   - **Plain-shell start:** the pane-less summary prints the same directive as its second line, which covers the "no worker seated" case.
   - **Silent cases:** the launcher-side claim (`start_claude_in_pane`) and worktree-seated sessions stay silent.
3. **Main-push guard** (`main_push_guard` behind `herdr-agents --main-push-guard`, plus the stub installer `install_main_push_guard` called from `bootstrap_agmsg`). This is the round-1 design.
   - **Where it is installed:** `bootstrap_agmsg` is reached by `herdr-agents --bootstrap-agmsg` (which `make update`/`make upgrade` run through `make agmsg-bootstrap`) and by the full mode, the unmanaged attach mode and `--restart-worker`. It writes `$(git rev-parse --git-path hooks)/pre-push`, only in a git main checkout with an orchestrator agmsg identity.
   - **The hook is a fixed stub:** it finds `herdr-agents` on PATH or at `~/.local/bin/common/herdr-agents`, and execs `--main-push-guard` only when that launcher's `--help` advertises the mode. The checks therefore change with the launcher that `make update` already replaces, and the hook file never needs rewriting. With no such launcher, missing or older than the guard, the stub itself refuses only `refs/heads/main` updates and lets every other ref pass. A stale launcher therefore never breaks worker PR pushes, and its other modes never run (round 2).
   - **When bootstrap installs it:** only once the launcher the stub would exec advertises the mode. `make upgrade` bootstraps from the checkout source before `make update` applies the new launcher, so until then bootstrap prints a notice naming the next `make update` and installs nothing. The `--help` probe is captured into a variable, not piped into `grep -q`, which under `pipefail` could SIGPIPE the launcher and read as stale (round 2).
   - **What bootstrap does not touch:** it never replaces an existing pre-push hook that differs from the stub, whether a foreign hook or an edited stub; it warns instead. An identical stub that lost its execute bit is made executable again, with a notice, because git silently skips a non-executable hook (round 2). It never writes into a `core.hooksPath` outside the repository's git dir.
   - **What the guard checks, for a pushed `refs/heads/main` update only:**
     - `ORCH_PUSH_MAIN` must be `acceptance` or `boundary`;
     - deleting main is refused;
     - an update that is not a fast-forward of the remote main is refused, including when the remote sha is unknown locally;
     - for `boundary`, the tree diff `git diff --name-only <remote> <local>` must list only `.orchestration/` paths. This is not a per-commit check: it compares the two trees, so a merge's own resolution counts. If the diff cannot be listed, the push is refused;
     - `acceptance` is logged but not checked further.

     Every decision is printed and appended to `<git-common-dir>/orch-push-main.log`. Other refs pass untouched.
   - **Not a hard boundary:** a local hook can be bypassed with `git push --no-verify`. The rule, SKILL and README say so, and name GitHub branch protection as the server-side boundary.
   - **Not active in the running pair yet:** the managed-pane SessionStart path (`HERDR_AGENTS_LAYOUT=managed`) exits right after the seat claim and never calls `bootstrap_agmsg`. The live wR pair's `.git/hooks/pre-push` therefore appears only when the operator runs `make update`, which is also when the new `herdr-agents` is applied. Until then, the directive line names a guard that is not installed in the orchestrator's own seat.
   - **Existing mechanisms:** none existed to reuse. There was no pre-push wiring, no `core.hooksPath`, and no pre-commit config.
4. **Pin assertion design:** both tests now assert a **floor** of v2026.9.12 instead of equality.
   - **Floor source:** #160 verified on a VM that v2026.9.12 is the first release with the Linux arm64 aqua bin-path fix (`[memory:decision]` 7b773deb). The bats test name, "mise pin includes the Linux arm64 aqua bin-path fix", already describes a floor.
   - **Why equality was not a supply-chain choice:** exactness of the pin is already enforced elsewhere. `generate-agent-configs.py --check`, run by `validate-agent-assets` in the CI agent-assets workflow and by `make render-check`, keeps `install/common/mise.sh` `MISE_VERSION` byte-identical to `agent-config.yaml` `assets.mise.pin`, and `release-shasums` verification covers integrity. The equality literal only duplicated the pin.
   - **What the Python test still checks:** that the pin is an exact `vN.N.N`, with no range or tag.
   - **Bats compare:** a portable integer compare (no `sort -V`). I checked it in plain bash with versions on both sides of the floor.
   - **Left alone:** the `cargo:eza` "0.23.5" literal in the same test has the same shape, but it is out of scope and recorded as a learning candidate.
5. **Tests** (`tests/unit/test_herdr_agents.py`, in the existing module):
   - two directive tests: the managed pane with and without a manifest seat, and a skipped pane printing no directive;
   - four guard tests that run real pushes against a scratch bare remote, including `--dry-run`:
     - override required;
     - boundary path check;
     - acceptance allowed;
     - another branch untouched;
     - rewind and delete refused;
     - log written;
     - idempotent reinstall;
     - foreign hook kept;
     - no orchestrator identity, no hook.
   - Round 1 adds four guard tests:
     - `test_main_push_guard_checks_a_merge_by_its_tree_diff`: an evil merge, whose parents touch only `.orchestration/` but whose resolution adds `README.md`, is refused under `boundary`. The test also asserts that the old per-commit listing would not show `README.md`;
     - `test_main_push_guard_fails_closed_when_the_changes_cannot_be_listed`: the remote main commit is readable but its tree object is deleted, and the push is refused with the logged reason;
     - `test_bootstrap_keeps_an_edited_main_push_guard_stub`;
     - `test_main_push_guard_stub_without_a_launcher_refuses_only_main` (round 1 had refused every push; round 2 refuses main only).
   - Round 2 adds three tests:
     - `test_main_push_guard_stub_with_an_old_launcher_refuses_only_main`: the old launcher's full mode never runs;
     - `test_bootstrap_skips_the_guard_while_the_launcher_predates_it`: bootstrap installs nothing and prints the notice;
     - `test_bootstrap_restores_the_execute_bit_of_the_stub`.

     Guard tests now bootstrap with the branch launcher on PATH (`bootstrap_guard`), since an install requires the probe to pass.

     The round-0 guard tests now run the stub against this branch's launcher placed on PATH.
   - The plain-start "names the seated worker" test now expects the directive line as well.
   - `test_agmsg_orchestration_docs.py` adds three invariants to the rule/SKILL parity check (`ORCH_PUSH_MAIN=boundary`, the never-pushes sentence, the no-implicit-opt-out sentence).
   - **Scope:** these three invariants support item 1, while `allowed_files` lists `tests/**` for items 2–4. They pin the rule text this task changes. If the orchestrator reads the scope strictly, they can be removed as one hunk without affecting anything else.

## Validation

- `make render-check`: exit 0.
- `make unit-test`: 718 tests OK (skipped=2), exit 0. This is the round-2 run, after the last edit; round 1 had 715 and round 0 had 711.
- `make validate-agent-assets`: exit 0. The WARNs are untracked orchestrator-side `.orchestration` files.
- shfmt (`-i 4 -sr`) and shellcheck on `herdr-agents`: clean.
- `make check-regime-boundary`: **exit 2**. Every violation is an untracked orchestrator-side `.orchestration` file: T53 acceptance and audit evidence, the T54 task file, and a pr-feedback JSON in `orchestrator-review`. None is from this branch. This is pasted verbatim and left for the orchestrator's boundary commit.
- Item 3 demonstration: the scratch bare remote runs for round 0 and round 1 are pasted in the validation file. The round-1 run adds two cases: the evil merge refused (`not: src.sh`), and a diff that cannot be listed refused (`fails closed`).
  - plain `--dry-run` refused;
  - `boundary` with a README commit refused;
  - `acceptance` allowed;
  - a push to another branch untouched;
  - plain push of a `.orchestration`-only commit refused;
  - `boundary` push of that commit allowed;
  - a delete with `acceptance` refused;
  - log contents shown.
- bats: not run locally. CI runs the floor assertion.

## Revise round 1: finding dispositions

1. **The boundary check missed merge diffs and failed open** (audit P1 + P2; orchestrator finding). **fixed:c636452.** The check is now tree to tree, using `git diff --name-only <remote> <local>`. A listing failure refuses the push with a logged reason, instead of producing an empty change list that was logged as allowed. The per-path loop is pure bash, so no external tool failure can empty the list. Tests: the merge and fail-closed cases listed above.
2. **A managed hook was silently replaced** (audit P2; Codex review P2). **fixed:c636452.** The hook is now a fixed stub, and its logic lives in `herdr-agents --main-push-guard`, which `make update` replaces. Bootstrap writes the stub only where no pre-push hook exists. A hook that differs from the stub, edited or foreign, is left in place with a warning. Test: `test_bootstrap_keeps_an_edited_main_push_guard_stub`.
   - **Guard updates still reach a live hook:** the stub text is constant, so a guard-logic update needs no hook rewrite. It lands when `make update` applies the new launcher.
   - **Stub changes need a manual step:** a future change to the stub text itself would need the operator to delete the hook and rerun bootstrap. This is stated in the warning.
3. **The one-line doc contract was stale** (Codex review P2). **fixed:c636452.** The SKILL pane-less bullet, the README pane-less paragraph, the `--help` attach text, the script header and the `print_plain_start_summary` description now describe a summary line followed by the directive line. The rule's directive sentence names both the Herdr-pane and the pane-less case. The `--help` bootstrap sentence and a usage line now describe `--main-push-guard`. The grep for `prints one line`, `one line naming`, `one-line SessionStart`, `one-line bring-up` and `every pushed commit` leaves only `check-regime-boundary.sh`, which is about violations; it is in the validation file. `test_agmsg_orchestration_docs.py` parity still passes.
4. **`--no-verify` bypass** (Codex review P1). **not-applicable:** a local hook cannot be made non-bypassable, as the task states. Branch protection is the disposition, and the text now says the hook is not a security boundary, so nothing claims a hard boundary.
5. **The report overstated the check.** **fixed:** section 3 above now says what the guard checks: a tree diff, not every pushed commit, with `acceptance` unchecked beyond logging.

## Revise round 2: finding dispositions

1. **Launcher version skew broke every push** (Codex review P1 at `:1644`). **fixed:1128abb.** The skew is real today: the installed `~/.local/bin/common/herdr-agents --help` has no `--main-push-guard`, while this branch's does. Both probes are pasted in the validation file. The fix has two parts:
   - (a) Bootstrap installs the stub only when the launcher the stub will exec advertises the mode, and otherwise prints the `make update` notice.
   - (b) The stub probes the same way. Without the mode it refuses only `refs/heads/main` updates, never execs the launcher's other modes, and lets other refs pass.

   Tests: the old launcher passes a feature-branch push, refuses a main push and never runs its full mode; bootstrap with the old launcher installs nothing.
2. **A stub that lost its execute bit stayed disabled** (Codex review P2 at `:1653`). **fixed:1128abb.** When the text matches, bootstrap now runs `chmod 755` on a non-executable stub and says so. Test: `test_bootstrap_restores_the_execute_bit_of_the_stub`.
3. **Validation rerun:** the full list is rerun, including the scratch-remote demo with the stale-launcher, bootstrap-skip and lost-execute-bit cases. The report's guard section and the `[memory:decision]` are updated. CI is in the validation file.

## User-visible impact (AGENTS.md "Dotfiles safety")

- **Who it covers:** the guard installs at the operator's next `make update` in the canonical clone. Because it lives in the common git dir, it then also covers the operator's own `git push origin main` from that clone and its linked worktrees. The override is `ORCH_PUSH_MAIN=acceptance|boundary`, and each use is logged.
- **Unaffected:** pushes of any other branch, including worker PR branches.
- **New context line:** orchestrator SessionStart output gains one directive line.
- **Branch protection (recommended, operator-side; out of scope for this task):** `acceptance` is a logged pass, not validated, as the task specified. Anyone with shell access can also bypass a local hook with `--no-verify`. Turning on branch protection for `main` on GitHub (require a PR and passing checks, block force pushes and deletion) would close both gaps on the server side.

## CompactionDB

`python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'T54: …'` was run in the main checkout. Memory id: **834ba299-4226-4f5a-910e-fd19e49c8aa8**. Round 1 added the stub and tree-diff decision as memory id **485d3eb6-a3e7-4047-8625-b53b1a7a60ad**, and round 2 added the launcher-probe decision as **595b7377-9e28-45a7-bcd8-f603c328396c**.

[memory:decision] T54: `make upgrade` pins travel by worker task + PR with test sync and `require-crit-review`; the orchestrator never pushes to `main`; regime activation is hook-injected; direct pushes from the seat are guarded (operator 2026-10-02).

[memory:decision] T54 round 2: the pre-push stub execs `herdr-agents --main-push-guard` only when the launcher's `--help` advertises it; otherwise it refuses only `refs/heads/main` updates, and bootstrap installs the stub only once the launcher has the mode; a stub that lost its execute bit is made executable again.

## Notes

- **Not run against the live checkout:** `herdr-agents --bootstrap-agmsg` and `make update`. The live `.git/hooks` is unchanged, so the guard is **not yet active** for the orchestrator. It installs at the operator's next `make update` in the canonical clone, or at the next full, unmanaged-attach or `--restart-worker` run.
- **Formatter hook:** a PostToolUse formatter reflowed the whole herdr-agents test module after one Edit. I restored it, and the final diff contains only the intended hunks (`git diff --stat` is in the validation file).
- **Understand-Anything hook:** it did not fire in this task.
