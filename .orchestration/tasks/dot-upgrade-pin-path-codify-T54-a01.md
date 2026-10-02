# AGMSG-TASK dot-upgrade-pin-path-codify-T54-a01

Drafted 2026-10-02 by the orchestrator (`claude-remediation-dot`, wR:p1)
after the operator's correction. Worker-c (`claude-standard-dot-a005`),
branch `chore/upgrade-pin-path` from `origin/main` (after T53 merges).
Verify the dispatched task_rev sha256 against this file; else stop and PONG
blocked. Dispatch happens only after T53 is accepted; do not start early.

## Objective

On 2026-10-02 the orchestrator diagnosed a `claude update` failure
(`claude` is the mise tool `npm:@anthropic-ai/claude-code`; `claude update`
targets npm's global prefix and cannot update it; `make upgrade` is the only
path, README "Tool versions"), had the operator run `make upgrade`, then
committed the six-file pin diff itself and pushed `4a75924` straight to
`main`: no `agmsg-orchestration` skill activation, no exemption
declaration, no `make require-crit-review`, no PR, and no expected-version
sync, so `main` went red (T53 fixed the tests). The operator's finding: text
rules were skipped while hook-enforced directives were followed, the
`make upgrade` clause literally permits a direct orchestrator commit, and
nothing mechanically blocks a direct push. Codify the fix so the failure
cannot repeat, in this order of preference: mechanism, then rule text.

1. **Rule text** (`home/dot_config/claude/rules/agmsg-orchestration.md`,
   `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, and the Codex
   mirror `home/dot_config/codex/AGENTS.md` if it carries the clause):
   replace "Give `make upgrade` mise config/lock changes their own chore
   commit in the upgrade session" with the true procedure: the operator runs
   `make upgrade` in the canonical clone; the pending pin diff (every file it
   changed, not only the config/lock pair) travels in **one worker task** as
   a class-pure PR that also syncs the expected-version assertions in
   `tests/**` (T37 #209, T53 precedent) and passes `make require-crit-review`
   before the orchestrator merges under the acceptance exemption. State
   plainly that the orchestrator never pushes to `main` directly. Add the
   missing activation case: when the bus exists but no worker is seated, the
   orchestrator seats one (`herdr-agents --restart-worker` in the pair,
   `--add-worker` otherwise) before any repository mutation; "no worker" is
   never an implicit opt-out. Keep the `[memory:decision]` marker.
2. **Hook-injected activation**: make the regime's activation directive
   arrive the way the Monitor directive does. Extend the SessionStart
   `herdr-agents --attach` hook output (`home/dot_local/bin/common/executable_herdr-agents`,
   the `seat_claim=` line) so that, when the repository has an agmsg team and
   a manifest worker seat, it prints a one-paragraph directive: invoke the
   `agmsg-orchestration` skill before any other action, delegate
   repository-mutating work, declare exemptions in one line. Unit-test the
   output in the existing herdr-agents test module (find it; do not create a
   parallel one).
3. **Mechanical guard against direct pushes**: add the smallest check that
   makes `git push origin main` from an orchestrator seat fail unless the
   push is an acceptance merge or a `.orchestration` boundary commit. Prefer
   a repository-local `pre-push` hook installed by the existing agmsg
   bootstrap (`herdr-agents --bootstrap-agmsg`, which already writes the
   gitignored `.claude/settings.local.json` hooks) over a new install step;
   use an explicit override env (`ORCH_PUSH_MAIN=acceptance|boundary`) that
   the guard requires and logs. Document it in the rule text from item 1.
   If a cleaner mechanism exists in the repository already (for example an
   `make require-crit-review` pre-push wiring), reuse it and say so.
4. **Pin assertion design**: evaluate whether the two tests fixed in T53
   should assert a _minimum_ mise version (the arm64 aqua fix floor) instead
   of equality to a literal that duplicates `install/common/mise.sh`. If the
   equality is a supply-chain policy choice, keep it and record why in the
   report; otherwise convert to a floor so future bumps stop breaking `main`.
5. `[memory:decision]` T54: `make upgrade` pins travel by worker task + PR
   with test sync and `require-crit-review`; the orchestrator never pushes to
   `main`; regime activation is hook-injected; direct pushes from the seat
   are guarded (operator 2026-10-02).

## Allowed files

- `home/dot_config/claude/rules/agmsg-orchestration.md`,
  `home/dot_agents/skills/agmsg-orchestration/SKILL.md`,
  `home/dot_config/codex/AGENTS.md`, `README.md` (only the paragraphs that
  describe `make upgrade` pin flow or regime activation)
- `home/dot_local/bin/common/executable_herdr-agents` and its tests
- `scripts/check-regime-boundary.sh` and its tests (if item 3 lands there)
- `tests/**` for items 2–4
- `home/dot_agents/agent-config.yaml` only if a rendered file carries the
  clause (run the generator and `make render-check`; list rendered files)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-upgrade-pin-path-codify-T54-a01.md`
- `.agents/worklog/**` waived.

## Forbidden actions

Changing any pin; GitHub branch-protection changes (operator-side; mention
it as a recommendation in the report); editing `.orchestration/acceptance/**`;
merge; force-push; `--delete-branch`; local `bats`; `make update`/`upgrade`;
dependency changes; UA graph work.

## Validation (verbatim output)

`make render-check`, `make unit-test`, `make validate-agent-assets` (real
exit status), `make check-regime-boundary`, a demonstration of item 3 (a
dry-run push to `main` refused, then allowed with the override) using a
scratch remote, `git diff --stat origin/main`, `gh pr view <n> --json
url,headRefOid,mergeStateStatus`, `gh pr checks <n>`, and the CompactionDB
`memory add --kind decision --scope project` command.

## Revise round 1 (orchestrator, after 2360aea; audit `Verdict: incorrect`)

Same branch `chore/upgrade-pin-path`, same PR #225, new commit(s) on top.
Findings to fix, each with a test in `tests/unit/test_herdr_agents.py`:

1. **Boundary check compares trees and fails closed** (audit P1 + P2,
   orchestrator finding). `git log --name-only` lists no files for a merge
   commit, so a merge whose parents touch only `.orchestration/` but whose
   own resolution adds code passes `ORCH_PUSH_MAIN=boundary`. Replace the
   per-commit listing with `git diff --name-only <remote_sha> <local_sha>`
   (tree-to-tree) and refuse the push when that command fails (today a
   failed enumeration yields an empty `outside` and logs `allowed`). Tests:
   a merge-only `README.md` change is refused under `boundary`; a forced
   enumeration failure refuses with a logged reason.
2. **An edited managed hook is never silently replaced** (audit P2, Codex
   review P2 at `:1582`). Today a hook that contains the marker but differs
   from the generated body is overwritten, discarding a user's added
   checks. Required behaviour: a differing marker-bearing hook is left in
   place with a warning, while a guard-logic update still reaches the live
   hook. The simplest design that satisfies both is a stable one-line stub
   (`exec herdr-agents --main-push-guard "$@"`, or equivalent) whose logic
   lives in the launcher that `make update` already replaces; a versioned
   exact-body check is acceptable if you show how updates still land.
   Test: an edited marker-bearing hook survives bootstrap with the warning.
3. **Documentation contract** (Codex review P2 at `:1107`). The pane-less
   SessionStart path now prints two lines in a regime repository, but the
   SKILL pane-less bullet, the rule, the `--help` usage text and README still
   say "prints one line". Update every carrier (grep for `prints one line`
   and `one line naming`), keep `test_agmsg_orchestration_docs.py` parity.
4. Codex review P1 (`--no-verify` bypass) is **not** in scope: a local hook
   cannot be non-bypassable; the operator-side GitHub branch-protection
   recommendation already in your report is the disposition. Keep that
   paragraph; do not claim the hook is a hard boundary anywhere in the text.
5. Report: restate what the guard checks without overstating (audit noted
   "every pushed commit is checked" was not true for merges). Rerun the
   full validation list, including the scratch-remote demonstration with
   the new merge case, and paste it. CI green, then `AGMSG-RESULT` as before.

## Revise round 2 (orchestrator, after c636452)

Round 1's tree diff, fail-closed listing, stub design and doc fixes are
accepted. Two Codex GitHub review findings on c636452 are real; fix both on
the same branch and PR, with tests:

1. **Launcher version skew breaks every push** (Codex review P1 at
   `:1644`; orchestrator confirmed). `make upgrade` runs `agmsg-bootstrap`
   from the checkout source before the new launcher is applied, so the stub
   is installed while `command -v herdr-agents` is still the previous
   build, which has no `--main-push-guard` mode: its default branch treats
   the flag as DIR, runs `remove_shadowing_node_global` (an `npm uninstall
-g` side effect) and fails on `cd -- --main-push-guard`, so every push of
   every branch fails until `make update`. Required: (a)
   `install_main_push_guard` installs the stub only when the launcher the
   stub will exec advertises the mode (probe its `--help` for
   `--main-push-guard`), otherwise prints a notice naming the next
   `make update` and skips; (b) the stub itself probes the same way and,
   when the mode is missing, refuses only `refs/heads/main` updates with a
   clear message and lets other refs pass, so a stale launcher can never
   break worker PR pushes or run side effects. Tests: bootstrap with an
   old-launcher fake on PATH installs nothing and prints the notice; the
   stub with an old-launcher fake passes a feature-branch push and refuses
   a main push without executing the launcher's full mode.
2. **A stub that lost its execute bit stays disabled** (Codex review P2 at
   `:1653`). An identical stub without `-x` returns early before `chmod`,
   and git silently ignores a non-executable hook. Required: when the text
   matches, ensure the file is executable (`chmod 755`) and say so; test it.
3. Rerun the full validation list including the scratch-remote demo with
   the stale-launcher and lost-execute-bit cases; update the report's guard
   section and `[memory:decision]` accordingly. CI green, then
   `AGMSG-RESULT` as before.

## Completion

English PR to `main`, CI green on Linux and macOS, artifacts at the expected
paths, `AGMSG-RESULT v1` with `cost:` in the report, delivered with
`agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot
wR:p1 "<single line>"`. max_turns=40.
