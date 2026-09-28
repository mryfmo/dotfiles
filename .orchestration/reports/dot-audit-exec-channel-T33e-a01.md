# T33e report — dot-audit-exec-channel-T33e-a01 (revision 2)

- worker: `claude-standard-dot-a005`; orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `fix/audit-exec-channel`, cut from `origin/main` = `04746ca`, rebased onto `f6b76b8` per the orchestrator ruling
- task_rev: sha256 `ccd4d3748384fb2c47d5f6b6e553640cbad5e48f7dfb11f55bbbd656b1cdb7f9`, checked
- PR: https://github.com/mryfmo/dotfiles/pull/199, head `16966386b8eb5e0f57a2e14a73774335177a062f` (rev2; rev1 head `bbd70c1`, pre-rebase `7822411`)
- status: ready_for_review (revision 2). CI is green on head 1696638: all checks pass except nix, which was skipped. Verbatim `gh pr checks 199` output is in the validation file.

## Revision 2 (AGMSG-ACCEPTANCE status=revise, 2026-09-28T09:22:26Z)

The visible-lane audit of `bbd70c1` raised one P2, confirmed by the
orchestrator (`.orchestration/validation/dot-audit-exec-channel-T33e-a01-audit.md`).

- **Cause.** In the **transcript fallback only**, the awk matched
  `/^tokens used/`, which also matches assistant prose starting with those
  words, and then dropped the next line unconditionally. Take a final
  message with a quoted `Verdict: correct`, then
  `tokens used must not hide …`, then a concluding `Verdict: incorrect`:
  the concluding line was dropped and the gate reported `correct`.
- **Fixed** in commit `1696638` on the same branch and PR #199. The awk
  now matches the footer exactly (`/^tokens used$/`) and skips the next
  line only if it is a bare count (`/^[0-9,]+$/`). Every other line is kept,
  and a `codex` header resets the pending footer state. No other changes;
  the README never described the footer skip.
- **Tests.** Two new subtests in
  `test_audit_gates_on_the_concluding_line_of_the_last_message`:
  - (m) the exact reproduction as a transcript (no last-message file):
    quoted `Verdict: correct`, `tokens used must not hide the next line`,
    concluding `Verdict: incorrect`. Expected: exit 1, `incorrect`, source
    transcript.
  - (n) a transcript whose real footer `tokens used` + `12,345` ends the
    file right after `Verdict: correct`. Expected: exit 0, `correct`, so
    the footer is still skipped.
- **Mutation baseline** against unmodified `bbd70c1` (checked as no diff
  from HEAD before the run): **1 failure**, case (m), `0 != 1`, which
  reproduces the audit finding. (n) passes on both versions, as a
  regression guard. After the fix, 19/19 audit tests pass,
  `make unit-test` passes (494 OK, no permgate flake this time),
  `make validate-agent-assets` passes, and shellcheck and shfmt are clean.
  All verbatim in the validation file.

## Changes (revision 1)

1. `home/dot_local/bin/common/executable_herdr-agents` (audit mode only)
   - **Command.** The inner command is:
     ```
     cd -- <%q DIR> && set -o pipefail && rm -f -- <%q PATH.last.md> && codex<%q audit args> exec --sandbox read-only -C <%q DIR> -o <%q PATH.last.md> <%q prompt> 2>&1 | tee -- <%q PATH>; printf '<marker>:%s\n' "$?"
     ```
     It keeps the whole-command `%q` `bash -c` quoting, the `cd` prefix, the
     nonce marker, pipefail and the `recent-unwrapped` wait unchanged.
     `--sandbox read-only` is explicit (defence in depth).
   - **Stale-file removal (my addition).** The pane command deletes
     `PATH.last.md` before codex runs, so a stale last message from an
     earlier run on the same path can never be judged. It sits after
     `set -o pipefail` so the `cd` token stays first.
   - **Prompt.** The task's text verbatim, with `<sha>` substituted, built
     with `printf -v audit_prompt` (`# shellcheck disable=SC2016`, because
     the backticks are literal prompt text).
   - **Gate.**
     - The verdict comes from the last non-blank line of `PATH.last.md`,
       which must be a whole-line
       `^[[:space:]]*Verdict: (correct|incorrect|blocked)[[:space:]]*$`.
     - A concluding line starting `Review blocked` gives `blocked`.
     - Anything else gives `missing`.
     - It exits 1 for anything but `correct`. The output is
       `Audit exit:` / `Audit evidence:` / `Audit last message:` /
       `Audit verdict:`.
   - **Fallback.** When `PATH.last.md` is missing or blank, the script
     prints `Audit verdict source: transcript` and takes the transcript
     region after the last `^codex$` line. It skips the `tokens used` line
     and the count line after it, so a transcript that ends on the count
     does not read as the concluding line, then applies the same
     concluding-line rule.
   - **Docs.** shdoc `@description` / `@option --audit` and `usage()` are
     updated.
2. `README.md`: the `--audit` paragraph now describes the exec channel, the
   prompt, the last-message file, the concluding-line rule, the transcript
   fallback, the residual (the gate trusts the auditor's final message), and
   the headless command
   `codex --profile audit exec --sandbox read-only -C <dir> -o <file> '<prompt>'`.
3. `tests/unit/test_herdr_agents.py`
   - (a) `test_audit_runs_codex_exec_with_the_prompt_and_last_message_file`:
     the decoded codex words are exactly
     `codex --profile audit exec --sandbox read-only -C <DIR> -o <PATH>.last.md <AUDIT_PROMPT>`.
     It also checks the stale-file `rm` target, `| tee -- <PATH>`, the
     marker, and `Audit last message:`.
   - (b)–(g) `test_audit_gates_on_the_concluding_line_of_the_last_message`
     has 10 subtests:
     - (b) correct; (b2) correct with trailing blank lines;
     - (c) a quoted `Verdict: correct` followed by a concluding sentence →
       `missing`;
     - (d) incorrect; (d2) blocked;
     - (e) concluding `Review blocked:` → `blocked`;
     - (e2) `Review blocked` mid-message but a concluding
       `Verdict: correct` → `correct`;
     - (f) empty last file with a transcript ending `Verdict: correct` →
       `correct`, source transcript; (f2) the same with a missing last file;
     - (g) both files missing → `missing`.
   - (h) `test_audit_quotes_the_last_message_path_for_a_non_ascii_out`
     (`LC_ALL=C`): the `-o` word decodes to `<out>.last.md`.
   - **Updated.** The command regex and manifest-args expectations now use
     the exec form. The T33b transcript gate test is kept; it now runs
     through the fallback and also asserts
     `Audit verdict source: transcript`.
   - **Mutation baseline** against the unmodified `origin/main` script (no
     script diff at run time): **24 failures** across 19 audit tests,
     verbatim in the validation file. After the change, 19/19 pass.

## Resolved blocker: `make validate-agent-assets` failed on origin/main 04746ca

- `ERROR: possible committed secret in .orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit.md`.
- The validator's `SECRET_PATTERN` matches two lines of that file:
  - L1523 `design_token: <quoted value masked for the repo secret validator>`
  - L1589 `applies_token: <quoted value masked for the repo secret validator>`

  These are schema field names quoted in the orchestrator's T33c audit
  transcript, a false positive. I looked only at the shape of each match
  and redacted the values when viewing.
- The file came from orchestrator commit `04746ca`. The branch's
  `.orchestration/` is identical to `origin/main`.
- Both that file and `scripts/validate-agent-assets.py` are outside T33e's
  `allowed_files`, and validator changes are forbidden. So the PR's CI
  `validate` job fails for any branch based on `04746ca`.
- Reported as `AGMSG-PONG status=blocked` (validation-only). The T33e code
  itself is complete.

**Resolution.** The orchestrator's PING (08:43:25Z) said the file was
masked on `main` in `e8cf7e1` and `f6b76b8`, and asked for a rebase. I
rebased onto `origin/main` `f6b76b8`, so my single commit is now `bbd70c1`.
The branch had already been pushed, so I republished it with
`git push --force-with-lease=fix/audit-exec-channel:7822411`, which the
ruling authorized, as in T31. After the rebase, `make validate-agent-assets`
prints "agent asset validation ok" and the full `make unit-test` passes
(494 OK); both are pasted.

## Other notes

- **Flaky test.** `test_permgate…test_bench_runs_five_layer_two_fixtures`
  failed again on the first full `make unit-test` and passed on the rerun
  (494 OK). Both runs are pasted. This is the fourth occurrence; T33d is
  queued.
- **No codex run.** No codex invocation of any kind was made: the
  `codex exec` flags come from the task's quoted `--help` facts. Live E2E is
  orchestrator-side.
- **Graph.** The understand-anything auto-update after the commit was not
  run. It is outside `allowed_files`; per T33c, graph refreshes are
  worker tasks.

## CompactionDB

[memory:decision] T33e: herdr-agents --audit runs the auditor through `codex exec` with
an explicit AGENTS.md-Audit prompt and `--output-last-message`, and gates on the
concluding line of that last-message file (`Verdict: correct|incorrect|blocked`, else
missing); the `codex review --commit` channel is retired because it neither accepts a
prompt nor produced a verdict in six live runs (operator 2026-09-28).

Id `49e942ec-7275-421a-b42f-99022239c631`; the command and output are in
the validation file.

## Effects

None outside the repository. The only writes outside the worktree were the
`.orchestration` artifacts and the local CompactionDB ledger.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
