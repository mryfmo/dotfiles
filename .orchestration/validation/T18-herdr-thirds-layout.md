# T18 validation evidence

All source-code commands ran in the isolated task worktree on
`feat/herdr-thirds-layout`. Live Herdr commands used task-specific scratch
workspaces only.

## Herdr CLI semantics

`herdr pane` advertised:

```text
herdr pane resize --direction left|right|up|down [--amount FLOAT] [--pane ID|--current]
```

A live right-nested `86/43/43` scratch layout was resized with:

```text
herdr pane resize --pane w18:p1 --direction left --amount 0.167
```

The resulting real layout was:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w18:p1","panes":[{"focused":true,"pane_id":"w18:p1","rect":{"height":44,"width":57,"x":26,"y":1}},{"focused":false,"pane_id":"w18:p2","rect":{"height":44,"width":58,"x":83,"y":1}},{"focused":false,"pane_id":"w18:p3","rect":{"height":44,"width":57,"x":141,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.333,"rect":{"height":44,"width":172,"x":26,"y":1}},{"direction":"right","id":"split_1_1","ratio":0.5,"rect":{"height":44,"width":115,"x":83,"y":1}}],"tab_id":"w18:t1","workspace_id":"w18","zoomed":false},"type":"pane_layout"}}
```

Right-pane verification showed that `direction left` expands the rightmost
pane and `direction right` shrinks it. The observed cell delta was relative to
the containing split width, so the implementation derives the amount from the
validated outer or inner split as appropriate.

## Unit tests

Command:

```text
python3 -m unittest tests.unit.test_herdr_agents -v
```

Exit code: `0`

```text
test_attach_ambiguous_files_panes_skip_repair ... ok
test_attach_bootstraps_agmsg_after_codex_reuse ... ok
test_attach_bootstraps_agmsg_after_codex_start ... ok
test_attach_builds_files_then_codex_around_current_claude_pane ... ok
test_attach_complete_workspace_is_idempotent ... ok
test_attach_correct_order_does_not_swap ... ok
test_attach_does_not_restart_codex_agent_from_another_tab ... ok
test_attach_equal_thirds_does_not_resize ... ok
test_attach_ignores_agmsg_bootstrap_failure ... ok
test_attach_ignores_extra_panes_on_other_tabs ... ok
test_attach_noops_for_full_mode_managed_layout ... ok
test_attach_noops_without_herdr_environment ... ok
test_attach_ratio_repair_skips_unsafe_layouts ... ok
test_attach_repairs_files_claude_codex_order ... ok
test_attach_repairs_left_nested_skew_to_equal_thirds ... ok
test_attach_repairs_skewed_widths_to_equal_thirds ... ok
test_attach_skips_agmsg_silently_when_not_installed ... ok
test_attach_skips_delivery_when_turn_hook_exists ... ok
test_attach_warns_when_multiple_agmsg_identities_exist ... ok
test_bare_herdr_in_ghostty_starts_plain_session ... ok
test_bare_herdr_outside_ghostty_uses_real_cli ... ok
test_claude_repair_skips_just_restarted_codex_pane_without_agent_field ... ok
test_claude_settings_add_herdr_attach_session_hook ... ok
test_duplicate_files_panes_fail_without_mutation ... ok
test_existing_agents_workspace_focuses_without_recreating_agents ... ok
test_existing_empty_files_pane_restarts_yazi_in_place ... ok
test_existing_files_pane_is_not_reused_for_claude_or_split_again ... ok
test_existing_files_pane_with_other_process_restarts_yazi_in_place ... ok
test_existing_workspace_adds_missing_files_pane ... ok
test_existing_workspace_restarts_missing_claude_in_empty_pane ... ok
test_existing_workspace_restarts_missing_codex_agent ... ok
test_existing_workspace_splits_when_missing_claude_has_no_empty_pane ... ok
test_files_pane_inspection_failures_do_not_start_yazi ... ok
test_files_pane_operations_propagate_failures ... ok
test_full_mode_skips_agmsg_bootstrap_for_home ... ok
test_ghostty_config_does_not_auto_start_herdr_session ... ok
test_ghostty_herdr_starts_plain_workspace ... ok
test_herdr_prefix_alt_a_runs_helper_from_active_pane ... ok
test_herdr_session_does_not_prebuild_agent_layout ... ok
test_herdr_session_execs_herdr_without_prebuilding_agents ... ok
test_herdr_session_passes_syntax_check ... ok
test_herdr_session_rejects_arguments ... ok
test_herdr_with_args_in_ghostty_uses_real_cli ... ok
test_interactive_ghostty_shell_attaches_plain_session ... ok
test_missing_yazi_fails_before_mutating_a_new_workspace ... ok
test_missing_yazi_fails_before_mutating_an_existing_workspace ... ok
test_uses_initial_workspace_pane_for_claude_and_splits_codex_right ... ok
test_yazi_edit_opener_prefers_zed_with_editor_fallback ... ok
test_zprofile_adds_common_bin_to_login_shell_path ... ok

----------------------------------------------------------------------
Ran 49 tests in 7.867s

OK
```

## Static checks

Commands:

```text
shellcheck home/dot_local/bin/common/executable_herdr-agents
bash -n home/dot_local/bin/common/executable_herdr-agents
git diff --check
```

All exited `0` with no findings.

## Fresh live E2E

The modified helper created scratch workspace `w19` from
`/private/tmp/herdr-t18-fresh-e2e`.

Layout:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w19:p1","panes":[{"focused":true,"pane_id":"w19:p1","rect":{"height":44,"width":58,"x":26,"y":1}},{"focused":false,"pane_id":"w19:p3","rect":{"height":44,"width":57,"x":84,"y":1}},{"focused":false,"pane_id":"w19:p2","rect":{"height":44,"width":57,"x":141,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.667,"rect":{"height":44,"width":172,"x":26,"y":1}},{"direction":"right","id":"split_1_0","ratio":0.5,"rect":{"height":44,"width":115,"x":26,"y":1}}],"tab_id":"w19:t1","workspace_id":"w19","zoomed":false},"type":"pane_layout"}}
```

Pane labels in x-order were:

```text
w19:p1 claude-orchestrator x=26 width=58
w19:p3 codex-worker       x=84 width=57
w19:p2 files              x=141 width=57
```

After shell initialization, the real files-pane process response was:

```json
{"id":"cli:pane:process_info","result":{"process_info":{"foreground_process_group_id":13309,"foreground_processes":[{"argv":["yazi"],"argv0":"yazi","cmdline":"yazi","cwd":"/private/tmp/herdr-t18-fresh-e2e","name":"yazi","pid":13309}],"pane_id":"w19:p2","shell_pid":13062},"type":"pane_process_info"}}
```

## Persisted-session attach live E2E

The same isolated workspace was deliberately changed to `86/43/43`:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w19:p3","panes":[{"focused":false,"pane_id":"w19:p1","rect":{"height":44,"width":86,"x":26,"y":1}},{"focused":true,"pane_id":"w19:p3","rect":{"height":44,"width":43,"x":112,"y":1}},{"focused":false,"pane_id":"w19:p2","rect":{"height":44,"width":43,"x":155,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.7484,"rect":{"height":44,"width":172,"x":26,"y":1}},{"direction":"right","id":"split_1_0","ratio":0.6627907,"rect":{"height":44,"width":129,"x":26,"y":1}}],"tab_id":"w19:t1","workspace_id":"w19","zoomed":false},"type":"pane_layout"}}
```

Attach command:

```text
HERDR_ENV=1 HERDR_PANE_ID=w19:p1 HERDR_WORKSPACE_ID=w19 bash home/dot_local/bin/common/executable_herdr-agents --attach
```

Exit code: `0`

After attach:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w19:p3","panes":[{"focused":false,"pane_id":"w19:p1","rect":{"height":44,"width":57,"x":26,"y":1}},{"focused":true,"pane_id":"w19:p3","rect":{"height":44,"width":57,"x":83,"y":1}},{"focused":false,"pane_id":"w19:p2","rect":{"height":44,"width":58,"x":140,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.66506666,"rect":{"height":44,"width":172,"x":26,"y":1}},{"direction":"right","id":"split_1_0","ratio":0.49904802,"rect":{"height":44,"width":114,"x":26,"y":1}}],"tab_id":"w19:t1","workspace_id":"w19","zoomed":false},"type":"pane_layout"}}
```

The post-attach pane list identified Claude, Codex, and files in that x-order,
and the files process remained `yazi`.

## Existing-workspace missing-files live E2E

This follow-up validates the P2 automated review finding. A fresh isolated
workspace was created, then its files pane was closed. Before full-mode
repair:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w1A:p1","panes":[{"focused":true,"pane_id":"w1A:p1","rect":{"height":44,"width":86,"x":26,"y":1}},{"focused":false,"pane_id":"w1A:p3","rect":{"height":44,"width":86,"x":112,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.5,"rect":{"height":44,"width":172,"x":26,"y":1}}],"tab_id":"w1A:t1","workspace_id":"w1A","zoomed":false},"type":"pane_layout"}}
```

Re-running the modified helper found the existing workspace, created files,
and reused safe ratio repair. After:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w1A:p1","panes":[{"focused":true,"pane_id":"w1A:p1","rect":{"height":44,"width":57,"x":26,"y":1}},{"focused":false,"pane_id":"w1A:p3","rect":{"height":44,"width":57,"x":83,"y":1}},{"focused":false,"pane_id":"w1A:p4","rect":{"height":44,"width":58,"x":140,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.3333333,"rect":{"height":44,"width":172,"x":26,"y":1}},{"direction":"right","id":"split_1_1","ratio":0.49888405,"rect":{"height":44,"width":115,"x":83,"y":1}}],"tab_id":"w1A:t1","workspace_id":"w1A","zoomed":false},"type":"pane_layout"}}
```

The files pane process response contained `"name":"yazi"`. Workspace `w1A`
and `/private/tmp/herdr-t18-existing-repair-e2e` were removed afterward.

## Cleanup

Commands:

```text
herdr workspace close w18
herdr workspace close w19
rm -rf /private/tmp/herdr-t18-resize-semantics /private/tmp/herdr-t18-fresh-e2e
```

Both close commands returned `{"result":{"type":"ok"}}`; the scratch
directories were removed.

## Git and GitHub

Commit:

```text
ec3526cc8c421f6a7a203f3057d880dc1ec4daa7
feat(herdr): repair agent layout to equal thirds
dc79fce6bdf8b8498178dac920af7ff520ecc831
fix(herdr): repair reused workspace after files split
```

PR:

```text
https://github.com/mryfmo/dotfiles/pull/78
```

`gh pr view 78` confirmed base `main`, head
`feat/herdr-thirds-layout`, the English title/description, and exactly these
two changed files:

```text
home/dot_local/bin/common/executable_herdr-agents
tests/unit/test_herdr_agents.py
```

Final status at head `dc79fce6bdf8b8498178dac920af7ff520ecc831`
from `gh pr checks 78 --watch`:

```text
changes                                      pass
validate                                     pass
test (macos-14, client)                      pass
test (ubuntu-latest, client)                 pass
test (ubuntu-latest, server)                 pass
private-bootstrap (macos-14, client)         pass
private-bootstrap (ubuntu-latest, client)    pass
private-bootstrap (ubuntu-latest, server)    pass
public-bootstrap (macos-14, client)          pass
public-bootstrap (ubuntu-latest, client)     pass
public-bootstrap (ubuntu-latest, server)     pass
nix                                          skipping
CodeRabbit                                   pass
```

GitHub Codex added one P2 inline finding after the first push. It was
reproduced, fixed, unit-tested, live-tested, and answered on the thread.
The PR description was refreshed for the complete two-commit diff. The second
Actions run and CodeRabbit check passed.

## Accepted deployment and operator live repair

The orchestrator accepted T18 and explicitly authorized merge, deployment,
and ratio-only repair of operator workspace `w13`.

### Merge

`gh pr merge 78 --squash --delete-branch` merged PR #78. Local branch deletion
was deferred because the task worktree still held the branch. GitHub reported:

```text
state=MERGED
mergedAt=2026-07-17T09:03:00Z
mergeCommit=680d65f802ec1e55c3027c8c37a1b24ed758ec9a
```

`git pull --ff-only` updated local main from `23013e8` to `680d65f`; Git
created and reapplied an autostash, preserving unrelated mise and
orchestration changes.

### Deployment

Targeted command:

```text
chezmoi apply --verbose ~/.local/bin/common/herdr-agents
```

Verification:

```text
330:function repair_attach_pane_ratio() {
602:    ensure_files_pane "${panes_json}" "${claude_pane_id}" "${workdir}" 0.667
649:    ensure_files_pane "${panes_json}" "${codex_pane_id}" "${workdir}" 0.667
683:start_files_pane "${root_pane_id}" "${workdir}" 0.667
deployed_matches_source=true
```

### w13 before

Pane list identified:

```text
w13:p8  claude-orchestrator  agent=claude
w13:pE  codex-worker         agent=codex
w13:p2  files
```

The task message named the current IDs correctly for Claude/workspace; the
older `w13:pA` Codex ID no longer existed, so the live pane list's `w13:pE`
was used for process verification.

Layout:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w13:pE","panes":[{"focused":false,"pane_id":"w13:p8","rect":{"height":44,"width":35,"x":26,"y":1}},{"focused":true,"pane_id":"w13:pE","rect":{"height":44,"width":34,"x":61,"y":1}},{"focused":false,"pane_id":"w13:p2","rect":{"height":44,"width":103,"x":95,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.4,"rect":{"height":44,"width":172,"x":26,"y":1}},{"direction":"right","id":"split_1_0","ratio":0.5,"rect":{"height":44,"width":69,"x":26,"y":1}}],"tab_id":"w13:t1","workspace_id":"w13","zoomed":false},"type":"pane_layout"}}
```

Process identities before repair:

```text
w13:p8  claude.exe pid=98094 shell_pid=6922
w13:pE  node pid=98164; codex pid=98188 shell_pid=98164
w13:p2  yazi pid=6955 shell_pid=4554
```

### Deployed live command

Run from `/Users/mryfmo/Workspace/dotfiles` with the deployed common bin first
on `PATH`:

```text
HERDR_ENV=1 HERDR_PANE_ID=w13:p8 HERDR_WORKSPACE_ID=w13 HERDR_AGENTS_LAYOUT= herdr-agents --attach
```

Exit code: `0`

```text
Herdr agents workspace: w13
```

### w13 after

Layout:

```json
{"id":"cli:pane:layout","result":{"layout":{"area":{"height":44,"width":172,"x":26,"y":1},"focused_pane_id":"w13:pE","panes":[{"focused":false,"pane_id":"w13:p8","rect":{"height":44,"width":57,"x":26,"y":1}},{"focused":true,"pane_id":"w13:pE","rect":{"height":44,"width":57,"x":83,"y":1}},{"focused":false,"pane_id":"w13:p2","rect":{"height":44,"width":58,"x":140,"y":1}}],"splits":[{"direction":"right","id":"split_0_root","ratio":0.66550386,"rect":{"height":44,"width":172,"x":26,"y":1}},{"direction":"right","id":"split_1_0","ratio":0.5,"rect":{"height":44,"width":114,"x":26,"y":1}}],"tab_id":"w13:t1","workspace_id":"w13","zoomed":false},"type":"pane_layout"}}
```

Computed summary:

```text
order=claude-orchestrator|codex-worker|files
widths=57/57/58
target=57.333333333333336
within_tolerance=true
```

Process identities after repair were unchanged:

```text
w13:p8  claude.exe pid=98094 shell_pid=6922
w13:pE  node pid=98164; codex pid=98188 shell_pid=98164
w13:p2  yazi pid=6955 shell_pid=4554
```

No pane or process was closed or restarted.

### Task cleanup

```text
git worktree remove /private/tmp/dotfiles-t18
git branch -D feat/herdr-thirds-layout
git push origin --delete feat/herdr-thirds-layout
t18_worktree_removed=true
```

The final main worktree head is
`680d65f802ec1e55c3027c8c37a1b24ed758ec9a`. A read-only layout query after
cleanup still returned `57/57/58` for `w13:p8`, `w13:pE`, and `w13:p2`.
