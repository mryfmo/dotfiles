# T32b report — dot-audit-pane-hardening-T32b-a01 (revision 1)

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per the dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c` (clean before the switch)
- branch: `fix/audit-pane-hardening` from `origin/main` = `c48e614` (includes 6b9babc)
- task_rev: sha256 `a4694adf98c32ef2818072bee50e0cdbaa2cd0ff21f1a6a2707ecc84a0980038`,
  checked against the task file on `origin/main` c48e614 (the hashes match)
- PR: https://github.com/mryfmo/dotfiles/pull/195, head `dad7bdff6592b875dc9369405fe6941fe1fc0062`
- status: ready_for_review. CI is green on head dad7bdf: all checks pass except nix, which was skipped. Verbatim `gh pr checks 195` output is in the validation file.

## Changes

1. `home/dot_local/bin/common/executable_herdr-agents`
   - **Whole-command quoting.** The inner command is built first with one
     `printf -v audit_inner` (see below). The pane then receives
     `bash -c $(printf '%q' "${audit_inner}")`, so the whole string is quoted
     once as the single `bash -c` argument, with no nested `%q` inside single
     quotes. The paths inside the inner command are `%q`-quoted for the inner
     bash, which parses `$'…'` correctly. The inner command is:
     ```
     cd -- <%q workdir> && set -o pipefail && codex<%q audit args> review --commit <sha> 2>&1 | tee -- <%q out>; printf '<marker>:%s\n' "$?"
     ```
   - **Blocklist removed.** The `'`/control-character check on
     `${workdir}${audit_out}` is gone, as the task asked.
   - **Unwrapped snapshots.** `--source recent-unwrapped` is now used for the
     marker `pane wait-output` and the follow-up `pane read`. Both
     subcommands list it in their `--help`.
   - **Unchanged:** the sha/timeout validation, the nonce marker, the `cd`
     prefix and the exit propagation. The code comments are updated (quoting
     rationale, unwrapped rationale).
2. `tests/unit/test_herdr_agents.py`
   - **Decoding helpers.** `shell_words`, `audit_inner_command` and
     `quoted_token` decode the logged `pane run` text back into shell words.
     They use `eval "set -- $1"` with an **empty PATH**, as a precaution: a
     mis-quoted string can turn `&&`/`;` into real syntax, and the empty PATH
     keeps it from launching any binary. I did not see this happen: on the
     baseline the apostrophe case exited 2 before `pane run`, and the
     non-ASCII case only mis-split into words. The
     helpers assert exactly `["bash", "-c", <inner>]` and decode the `cd` and
     `tee` targets.
   - (a) `test_audit_rejects_a_dir_with_an_apostrophe_before_any_pane_run` is
     replaced by `test_audit_accepts_a_dir_with_an_apostrophe_quoted_intact`.
     The run exits 0, and the decoded `cd` target is DIR and the `tee` target
     is the default evidence path, both intact.
   - (b) new `test_audit_quotes_a_non_ascii_out_path_under_the_c_locale`:
     with `LC_ALL=C` and `--out 'evidence/監査 audit.md'`, the `pane run`
     text is exactly one `bash -c` argument whose decoded `tee --` target
     equals the absolute path.
   - (c) new `test_audit_marker_detection_reads_unwrapped_snapshots`: checks
     `--source recent-unwrapped` on the marker wait-output and
     `pane read w-old:p9 --source recent-unwrapped --lines 200`.
   - **Adapted to decoding** (same assertions as before, now made on the
     decoded inner command): the command/tee/marker test, the cd-prefix test
     and the manifest-args test.
   - **Case removed:** the `--out "it's.md"` case of the unsafe-argument test,
     because that path is now accepted.
   - **Mutation baseline** against the unmodified 6b9babc script (the script
     had no diff against `origin/main` at that point): **4 of 15 FAIL**, all
     verbatim in the validation file. The non-ASCII case shows the old bug
     directly: the old command decodes into **4** words, with
     `…tee -- $/tmp/…/evidence/347233243346237273` and `audit.md; printf "…`.
3. `README.md`: unchanged. No user-visible statement in the `--audit`
   paragraph changed, and it never mentioned the blocklist.

## Deviations from task text

- **Marker format.** The marker printf is now `printf '<marker>:%s\n' "$?"`,
  single-quoted inside the inner command; before it was double-quoted inside
  the old single-quoted string. The behavior is the same. The format is now
  written literally so the inner command stays readable once decoded.
- **Test split.** Test (c) is its own test rather than extra assertions in the
  command test. That way the mutation baseline shows the `recent` →
  `recent-unwrapped` change failing on its own, not hidden behind the
  marker-format assertion.

## Not done / orchestrator-side

- No real audit, codex invocation, or herdr tab/pane creation was run
  (forbidden). The live E2E is orchestrator-side at acceptance.
- **Pane shell is zsh.** The decoding test uses bash `eval "set -- …"`, but
  the live pane shell is the operator's zsh. bash `%q` output uses backslash
  escapes and `$'\NNN'`, and zsh parses both. The live `--audit` run at
  acceptance is where zsh is exercised end to end.
- The understand-anything post-commit auto-update was not executed. It lies
  outside `allowed_files`, and graph rebuilds are orchestrator-tasked.

## CompactionDB

[memory:decision] T32b: the audit pane command is quoted once as a whole `bash -c`
argument (no nested %q inside single quotes; no path-character blocklist), and marker
detection reads `recent-unwrapped` snapshots so pane width cannot affect completion
(operator 2026-09-28, from the first live audit-lane findings).

Command run from the main checkout (output pasted verbatim in the validation file, id
`7a2cd50a-a846-4971-a028-a03f3f766682`). The content was passed through a shell
variable, so the backticks inside it were not command-substituted. The echoed
`$ …` line in the validation file is only a display rendering of that call.

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "$C"   # C = the [memory:decision] text above
```

## Effects

None outside the repository. The only writes outside the worktree were the
`.orchestration` artifacts and the local CompactionDB ledger.

cost: n/a (the Claude Code runtime does not expose session token/cost figures to the worker)
