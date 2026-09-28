# T32 report — dot-audit-pane-visibility-T32-a01 (revision 2)

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per the dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `feat/audit-pane-visibility` from `origin/main` = `7f3164e`
- task_rev: sha256 `f3e9313e9d899fe66a0a639272e00e8b12c45482d146ac3503c9b14561852363`,
  checked against the task file on `origin/main` 7f3164e (the hashes match)
- PR: https://github.com/mryfmo/dotfiles/pull/194, head `969187082eb056c4cdca06f279362a76d3a30a74` (rev2; rev1 head was `8af8d11`)
- status: ready_for_review (revision 2). CI is green on head 9691870: all checks pass except nix, which was skipped. Verbatim `gh pr checks 194` output is in the validation file.

## Revision 2 (AGMSG-ACCEPTANCE status=revise, 2026-09-27T23:47:09Z)

Head `9691870` on the same branch and PR #194. There was no rebase:
`origin/main` is still `7f3164e`. Both P2 findings from the pre-merge Codex
audit of `8af8d11` (`.orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md`)
are fixed:

1. **A reused audit pane could have left DIR.** The pane command now starts
   with `cd -- <%q workdir> && set -o pipefail && codex … 2>&1 | tee -- <out>; printf "<marker>:%s\n" "$?"`.
   Every run executes in DIR even after the operator `cd`'d the pane
   elsewhere; `tab create --cwd` applies only when the tab is created.
   Everything is joined with `&&`, so a failed `cd` still reaches the exit
   marker, and `$?` there is the cd's nonzero status. Without that, the wait
   would time out.
2. **An apostrophe in DIR broke the `bash -c` quoting.** The quote/control
   character check no longer runs on the raw `--out` value. It runs on the
   *resolved* `workdir` and the absolute evidence path, right after `cd` and
   `pwd -P`, before any herdr call. A failing path prints usage and exits 2
   (fail closed). I chose this route over quoting the whole command because
   the requested test expects exit 2 for such a DIR.

Tests:
- New `test_audit_runs_in_dir_even_when_the_reused_pane_moved`: the
  `pane run` command starts with `bash -c 'cd -- <DIR> && `.
- New `test_audit_rejects_a_dir_with_an_apostrophe_before_any_pane_run`:
  a DIR of `it's project` gives exit 2 with usage and no `pane run` or
  `tab create`.
- Test (b) now expects the new command string.
- Mutation baseline against `8af8d11`: 3 of 13 FAIL, namely the two new tests
  and the updated (b). On the old script the apostrophe case reached
  `Audit exit: 0` (rc 0 ≠ 2). Verbatim output is in the validation file.

Not verified: I tried a local check that ran the generated command string in
zsh with a stub CLI, but it was denied by the permission prompt and I did not
retry it. The runtime behaviour of the `cd`/pipefail/marker chain is covered
only by the exact-string unit assertions and by the orchestrator-side live
E2E.

## Changes (revision 1)

1. `home/dot_local/bin/common/executable_herdr-agents`: new mode
   `--audit <sha> [--out PATH] [--timeout SECONDS] [DIR]`.
   - Argument checks run before any herdr call, because these values end up in
     a pane command line. The sha must match `^[0-9a-fA-F]{7,40}$`, the timeout
     must be a positive integer, and `--out` must not contain `'` or control
     characters. A bad value prints usage and exits 2.
   - Resolves the pair with the existing `single_managed_workspace "<dir> agents" <dir>`,
     which exits 2 on duplicates. With no managed workspace it exits 2 with the
     `--restart-worker`-style message and names headless
     `codex --profile audit review` as the fallback.
   - New `audit_tab_ids` / `audit_pane_id` helpers. `audit_pane_id` finds the
     tab labeled `audit` and creates it only when none exists, using
     `herdr tab create --workspace W --cwd DIR --label audit --no-focus`. It
     requires exactly one audit tab holding exactly one pane, otherwise exit 2.
     It labels that pane `audit` and reuses the tab/pane on later runs. It never
     closes them.
   - Calls `wait_for_shell_prompt` (existing helper) on the audit pane before
     `pane run`. A busy pane, such as a timed-out audit still running, is
     refused with exit 2.
   - The pane command, sent with `herdr pane run`, is
     `bash -c 'set -o pipefail; codex <MODEL_PROFILE_AUDIT_CODEX_ARGS> review --commit <sha> 2>&1 | tee -- <abs out>; printf "AUDIT-EXIT-<epoch>-<pid>:%s\n" "$?"'`.
     The audit args come from `~/.agents/model-profiles.env` (default
     `--profile audit`). `--out` defaults to
     `.orchestration/validation/audit-<sha>.md`, is resolved to an absolute
     path under DIR, and its parent directory is created.
   - Waits with `herdr pane wait-output <pane> --regex 'AUDIT-EXIT-<nonce>:[0-9]+' --source recent --timeout <s*1000>`
     (default 1800 s). On timeout it exits 1 with the pane id and the evidence
     path. The exit code is read from wait-output stdout, falling back to
     `herdr pane read`. It then prints `Audit exit: N` / `Audit evidence: PATH`
     and exits 1 when N≠0.
   - Guard hardening: `empty_pane_id` also skips `.label == "audit"`, as it
     already did for `files`. The full-mode split source skips the audit pane.
     `panes_on_pane_tab`, `attach_panes_are_unambiguous`, and the full-mode
     duplicate guard are unchanged.
   - shdoc: `@description`, `@option --audit/--out/--timeout`, and `@example`
     for the new mode, plus `@description`/`@arg`/`@exitcode` on the new
     helpers. `usage()` is updated.
2. Rules text:
   - `home/dot_config/claude/rules/agmsg-orchestration.md`: "pane-less" is
     replaced with the task's clause. The auditor runs visibly in the pair
     workspace's dedicated audit tab via `herdr-agents --audit <sha>` when a
     herdr workspace exists, and headless otherwise. It stays identity-less,
     read-only, and orchestrator-invoked, under the acceptance exemption.
   - `home/dot_agents/skills/agmsg-orchestration/SKILL.md`: the T30 carve-out
     sentence now carries the same clause.
3. `README.md`: one `--audit` paragraph after the `--restart-worker`/teardown
   block. It covers purpose, invocation, evidence path, timeout, the `audit`
   label, that the auditor has no identity, and the headless fallback.
4. `tests/unit/test_herdr_agents.py`:
   - The fake herdr gains `tab list`, `tab create` (appends tab `W:t2` and
     pane `W:p9`), `pane read`, and an `AUDIT-EXIT` marker reply in
     `pane wait-output`, which reads its exit code from `audit-exit.txt`.
   - 11 new tests, mapped to the task's cases:
     - (a) `test_audit_creates_the_audit_tab_once_and_reuses_it`: exactly one
       `tab create` across two runs, both `pane run`s on `w-old:p9`, and no
       call touches p1/p2.
     - (b) `test_audit_pane_command_tees_evidence_and_waits_for_a_fresh_marker`:
       checks the profile invocation, pipefail, `tee -- <abs out>` (with a
       space-escaped path), the nonce marker, a wait regex requiring
       `:[0-9]+`, and the 1800000 ms default. Also
       `test_audit_uses_manifest_audit_codex_args` and
       `test_audit_refuses_a_busy_audit_pane`.
     - (c) `test_audit_nonzero_exit_marker_fails_the_helper`, plus
       `test_audit_rejects_unsafe_arguments_before_calling_herdr`.
     - (d) `test_audit_exits_2_without_a_managed_workspace`.
     - (e) `test_audit_tab_does_not_break_attach_order_and_ratio_repair`
       (swap and resize subtests),
       `test_audit_tab_keeps_the_full_mode_duplicate_workspace_guard`,
       `test_full_mode_heal_never_starts_the_worker_in_the_audit_pane`, and
       `test_restart_worker_never_treats_the_audit_pane_as_the_worker`.
   - Mutation baseline (verbatim in the validation file): against the
     unmodified `origin/main` script, **8 of 11 FAIL**. The 3 that pass are the
     two attach/duplicate-guard regressions, which must hold before and after,
     and the argument-rejection test, where the old script also exits 2 on an
     unknown `--audit` flag.

## Deviations from task text (please adjudicate)

1. **The exit status comes from pipefail, not from `tee`.** The task's literal
   `codex … 2>&1 | tee <path>; printf 'AUDIT-EXIT:%s\n' $?` reports `tee`'s
   status, so a failing audit would read as `AUDIT-EXIT:0`. The command runs
   under `bash -c 'set -o pipefail; …'`, which also works whatever the pane's
   interactive shell is.
2. **The exit marker carries a per-run nonce** (`AUDIT-EXIT-<epoch>-<pid>:N`).
   `herdr pane wait-output` also searches output already on screen (per its
   `--help`: "The selected snapshot is searched immediately, including
   existing output"). Because the audit pane is reused, a fixed `AUDIT-EXIT:`
   would match the previous run's marker at once. The wait regex requires
   digits after the colon, so the command line echoed in the pane (`…:%s`)
   cannot match itself.
3. **Tab-scoped filtering does not hide the audit pane from every mode, so I
   hardened two selectors.** The task says the audit tab is covered by the
   tab-scoped filtering. That holds for `--attach`, where `panes_on_pane_tab`
   runs before the guard, and for the duplicate-workspace guard. It does not
   hold for full-mode heal: `empty_pane_id` picks the worker and claude panes
   from the _unfiltered_ workspace list (worker L1057 / claude L1073 on the
   new file) before `panes_on_pane_tab` runs at L1084; `--restart-worker` falls back to it at L1019. The mutation baseline
   proves it: the old script ran
   `agent start codex-worker-w-old --kind codex --pane w-old:p9`, starting the
   worker inside the audit pane. With an audit tab present,
   `--restart-worker`'s third fallback would also have refused with a
   misleading "ambiguous" error. The fix excludes the `audit` label in
   `empty_pane_id` and in the full-mode split source. No guard was weakened.
4. `herdr tab create --label audit` sets the label when the tab is created, so
   no separate `tab rename` call is needed (herdr 0.9.1 `tab create --help`
   lists `--label`).
5. The audit args come from `MODEL_PROFILE_AUDIT_CODEX_ARGS` in
   `~/.agents/model-profiles.env` (default `--profile audit`), following the
   model-selection rule that audit args are sourced from that variable rather
   than hard-coded.
6. Extra flags: `--out` as specified, and `--timeout SECONDS` for the
   "generous timeout flag".
7. The tab is created with `--no-focus` so the operator's current view is not
   taken over. The audit tab is visible in the tab bar and stays open.

8. **Process: the PING arrived late.** `AGMSG-PING` (sent 2026-09-27T23:30:34Z)
   reached me neither as a turn notice nor through the inbox Monitor. The
   Monitor expired after 30 minutes with no events, so I re-armed it. I found
   the PING only by running `inbox.sh` right before sending this RESULT, and
   PONGed right away. This matches the T31 revision-2 delivery miss. I have
   not established a root cause. The Monitor watches `watch.sh … claude-code`
   for this session, while messages are addressed to `claude-standard-dot-a005`.

## Not done / orchestrator-side

- The refusal path in `audit_pane_id` for an ambiguous audit tab or pane (two
  `audit` tabs, or several panes on the audit tab → exit 2) has no dedicated
  test. It exits through a failed command substitution under `set -e`, the
  same pattern `single_managed_workspace` relies on, which is tested.

- No real audit, codex invocation, or real herdr tab/pane creation was run
  (forbidden). The live E2E `--audit` run is orchestrator-side at acceptance.
  The herdr facts I relied on came from read-only `--help` and `tab list`/`pane list` output.
- `make require-crit-review` was not run worker-side. It is the
  orchestrator's final integration step.
- The understand-anything post-commit auto-update prompt was not executed.
  Graph rebuilds are repository mutations outside this task's `allowed_files`,
  and the rules route them through an orchestrator-issued task.
- Read-only herdr probing: I ran `herdr tab list`, `herdr pane list`, and
  one `pane wait-output --match … --timeout 1000` against the orchestrator
  pane `wJ:p1` to learn the output shape. It timed out and mutated nothing.
  I am flagging it because reading panes is discouraged; I did not repeat it.

## CompactionDB

[memory:decision] T32: herdr-agents --audit <commit> runs the Codex audit visibly in a
dedicated audit tab (tee to validation evidence, exit-marker wait, tab reused); auditor
stays identity-less/read-only/orchestrator-invoked; headless invocation is the no-herdr
fallback (operator 2026-09-27).

Command run from the main checkout (output pasted verbatim in the validation file, id `7091c219-a3da-4732-888c-7b08a8e1b4f7`):

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T32: herdr-agents --audit <commit> runs the Codex audit visibly in a dedicated audit tab (tee to validation evidence, exit-marker wait, tab reused); auditor stays identity-less/read-only/orchestrator-invoked; headless invocation is the no-herdr fallback (operator 2026-09-27)"
```

## Effects

None outside the repository. Nothing under `$HOME` was written, and no install,
apply, or external registration was made. The only non-repo writes were the
`.orchestration` artifacts listed below and the local CompactionDB ledger.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
