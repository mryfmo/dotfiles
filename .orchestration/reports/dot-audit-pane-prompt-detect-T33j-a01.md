# T33j report: dot-audit-pane-prompt-detect-T33j-a01 (revision 1)

- worker: `claude-standard-dot-a005`; orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`, clean before the switch
- branch: `fix/audit-pane-prompt-detect`, from `origin/main` = `d7a5947`, which includes T33i #204 as a9783ad
- task_rev: sha256 `eb2423221107e3152a204dcfd6c49481b54df0baef786566c2fd6b5476b448d6`, checked against `origin/main`
- cleanup: deleted the merged local branch `fix/orchestration-hygiene-T33i` (was `1994142`)
- PR: https://github.com/mryfmo/dotfiles/pull/205, head `4b88402f2c8108d926f6720980dff387f16d9139`
- status: ready_for_review. CI is green on head 4b88402 (all checks pass, nix skipped, macOS included); verbatim `gh pr checks 205` is in the validation file.

## Change (`home/dot_local/bin/common/executable_herdr-agents`)

1. **The foreground process decides.** `wait_for_shell_prompt` returns
   0 as soon as `herdr pane process-info` reports exactly one foreground
   process and that process is the pane's shell. That means one of:
   - its pid equals `.result.process_info.shell_pid`, when herdr reports it;
   - its argv[0] or name is a known shell, matching the existing
     `(^|/)-?(ba|z|fi)?sh$`.

   No snapshot regex is involved. Two cases still end in the bounded
   failure after 50 × 0.2 s, and their callers keep their classifications:
   - a non-shell foreground process;
   - more than one foreground process, which means the shell has a child.

   Those callers are:
   - `restart_worker_in_pane`: the submit key for the exit dialog;
   - `start_agent_in_pane`: refusal;
   - `--audit`: "busy".
2. **Prompt text via `recent-unwrapped`.** The new helper
   `pane_shows_shell_prompt` reads
   `herdr pane read <pane> --source recent-unwrapped --lines 50`. It drops
   blank lines and tests the last remaining line against the existing
   prompt regex `[$#%❯➜>]+[[:space:]]*$`. Nothing reads `--source visible`
   any more. The last-line check runs locally, so it does not depend on
   whether herdr's `wait-output` regex matches per line (then any older
   prompt line in the scrollback would match) or per snapshot. The helper
   is used in two places:
   - as the **fallback when process-info is unavailable** (the command
     fails). Before, that case just looped and failed;
   - where a drawn prompt is still required (see Deviations).
3. **README.** One added sentence: the busy check is based on the audit
   pane's foreground process, not on its visible snapshot, which can be
   stale for a background tab.

## Deviations from the task text (please review)

- **New panes still require a drawn prompt (item 1 is not applied
  literally everywhere).** `process-info` cannot distinguish two states:
  - zsh is foreground and has drawn its prompt;
  - zsh is foreground but has not yet enabled its line editor.

  The second state is the bracketed-paste startup race that
  `wait_for_shell_prompt` was written for. The function's shdoc says so,
  and `git log -S wait_for_shell_prompt` shows it dates from d91b835, the
  pane API port, long before `--audit` (6b9babc). Returning 0 on "shell
  foreground" for every caller would bring that bug back for every split.

  So the function takes an optional `prompt` argument, meaning "also
  require the prompt text from item 2". Callers that pass `prompt`:
  - both `newly_created` branches of `start_agent_in_pane`;
  - the export path of `start_claude_in_pane`, which previously also
    waited for the prompt after `pane run export …`;
  - `--audit`, but only when it has just created the audit tab (so
    `audit_tab_ids` is empty before `audit_pane_id`).

  A reused audit pane, which was the failing case, uses the process rule
  alone.
- **`restart_worker_in_pane` behaviour change.** After `/exit`, its own
  wait no longer needs prompt text once the shell is back in the
  foreground. The prompt wait still happens in the following
  `start_worker_agent … true`. The net sequence is equivalent: the
  exit-dialog and stuck tests pass, including the `== 100` process-info
  count.
- **`shell_pid`.** It is matched only when herdr reports it. I could not
  inspect real process-info output (probing panes is forbidden), so the
  field name comes from the task text. The name rule still covers
  bash/zsh/fish/sh when the field is absent.
- **Extra call.** `--audit` now runs `herdr tab list` once more, to learn
  whether it is about to create the tab. No test pins that count.
- Timing: the wait is now one 10 s budget. Before, it was up to 10 s for the
  shell plus 10 s for `wait-output`.

## Tests (`tests/unit/test_herdr_agents.py`)

The fake herdr gains:
- `visible-stale.txt`: when 1, `pane read --source visible` prints stale
  transcript text and a `wait-output --source visible` times out;
- `recent-text.txt`: the `recent-unwrapped` snapshot. The default is a
  prompt followed by trailing blank lines, which exercises the
  blank-line skipping;
- process-info states `unavailable` (the command fails) and `shell-pid`
  (argv `nu`, with pid equal to `shell_pid`).

Tests, by the task's letters:
- (a) `test_audit_trusts_a_shell_foreground_over_a_stale_visible_snapshot`,
  subtests `shell` and `shell-pid`: the visible snapshot is stale and the
  recent text is not a prompt. `--audit` proceeds (`pane run`), and nothing
  reads `visible`.
- (b) `test_audit_refuses_a_busy_audit_pane` (existing): a non-shell
  foreground process is still refused as busy, even though the default
  recent text shows a prompt.
- (c) `test_audit_falls_back_to_the_recent_unwrapped_prompt_without_process_info`:
  with a prompt the audit proceeds; with `codex output` it is refused as
  busy. Both subtests assert
  `pane read w-old:p9 --source recent-unwrapped --lines 50` and that
  nothing reads `visible`.
- extra: `test_audit_waits_for_the_prompt_on_a_new_audit_tab`: on a new tab
  with no drawn prompt, the audit exits 2 and no `pane run` happens.

**Mutation baseline** against unmodified `origin/main` `d7a5947`, with the
script copied in from `git show` and checked as no diff: **5 failures**,
namely every new subtest. (b) passes on both, as a regression guard. After
the change:
- herdr-agents tests: 126 OK;
- `make unit-test`: 525 OK (1 skipped);
- `make validate-agent-assets`: ok;
- `shellcheck -x`, `shfmt`: clean.

CI note: the prompt regex now runs through `grep -E` on runner output,
including macOS BSD grep with a multibyte bracket expression. CI covers both
platforms; see the validation file.

## CompactionDB

`[memory:decision]` T33j: herdr-agents decides "audit pane busy" from the
pane's foreground process (shell = free), not from a visible-snapshot prompt
regex, because background-tab visible snapshots can be stale (operator
2026-09-29).

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T33j: herdr-agents decides \"audit pane busy\" from the pane's foreground process (shell = free), not from a visible-snapshot prompt regex, because background-tab visible snapshots can be stale (operator 2026-09-29)."
```

The id is `5a64a0ef-d6e0-404f-b95e-a12d291cbee1`; the output is in the
validation file.

## Effects

None outside the repository. Live E2E (a real `--audit` run on the reused
pane) is orchestrator-side.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
