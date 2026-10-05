# AGMSG-TASK dot-audit-pane-hardening-T32b-a01

## Objective

Close the two P2 findings from the first live `herdr-agents --audit` run
(audit of merge commit 6b9babc, evidence
`.orchestration/validation/dot-audit-pane-visibility-T32-a01-live-e2e.md`,
disposition in `.orchestration/acceptance/dot-audit-pane-visibility-T32-a01.md`):

1. Quoting: the inner command is assembled from nested `printf '%q'` pieces
   inside a single-quoted `bash -c '…'` string. Under `LC_ALL=C`, non-ASCII
   path characters make `%q` emit `$'…'` quoting that breaks the outer single
   quotes; shell metacharacters in such paths could become executable syntax.
   Build the complete inner command first (cd, pipefail, codex, tee, marker
   printf), then quote that ENTIRE string once with `printf '%q'` as the
   single `bash -c` argument. After this, the `'`/control-character
   fail-closed check on `${workdir}${audit_out}` becomes unnecessary — remove
   it and adjust `test_audit_rejects_a_dir_with_an_apostrophe_before_any_pane_run`
   to assert the opposite: an apostrophe DIR is ACCEPTED and the quoted
   command reaches `pane run` intact (decode the `%q` output in the test with
   `bash -c 'printf %s "$@"' _ …` or `shlex`-equivalent and assert the decoded
   inner command).
2. Wrapping: use `--source recent-unwrapped` for both the
   `herdr pane wait-output` marker wait and the follow-up `herdr pane read`,
   so a pane narrower than the marker cannot hide completion (verified: both
   subcommands list `recent-unwrapped` in `--help`).

[memory:decision] T32b: the audit pane command is quoted once as a whole
`bash -c` argument (no nested %q inside single quotes; no path-character
blocklist), and marker detection reads `recent-unwrapped` snapshots so pane
width cannot affect completion (operator 2026-09-28, from the first live
audit-lane findings).

## Repo / branch

- Work ONLY in `~/Workspace/dotfiles/.claude/worktrees/worker-c`.
- `git fetch origin`, then `git switch -c fix/audit-pane-hardening origin/main`
  (origin/main includes 6b9babc). Verify the dispatched task_rev sha256
  against this file on your base, else stop and PONG.
- If the worktree has uncommitted files, stop and report via AGMSG-PONG.

## Changes

- `home/dot_local/bin/common/executable_herdr-agents`: items 1–2 above; keep
  the sha/timeout validation, the nonce marker, the cd prefix, and the exit
  propagation exactly as they are; update shdoc comments where behavior
  changed.
- `tests/unit/test_herdr_agents.py`: (a) adjust the apostrophe test as
  described; (b) add one test that a non-ASCII `--out` path (e.g.
  `evidence/監査 audit.md`) reaches `pane run` as a single correctly quoted
  `bash -c` argument whose decoded form contains `tee -- <that path>` — run
  the helper with `LC_ALL=C` in that test; (c) assert `--source
  recent-unwrapped` on both the wait-output and pane read calls (extend the
  fake herdr if needed). Mutation baseline against the unmodified 6b9babc
  script is mandatory (paste the FAILED run).
- README: adjust the `--audit` paragraph only if a user-visible statement
  changed (probably none).

## Allowed files

- `home/dot_local/bin/common/executable_herdr-agents`
- `tests/unit/test_herdr_agents.py`
- `README.md`
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-audit-pane-hardening-T32b-a01.md` (main checkout)

## Forbidden actions

- Running a real audit or any codex invocation; creating real herdr tabs or
  panes; touching model_profiles, permgate, hooks configs, dependencies,
  validator/generator scripts, rules/SKILL text, or `reviews/ADH_Integrated_Plan/`.
- Merging; force push; local bats; `make apply`/`chezmoi apply`; writes
  outside the worktree except the listed `.orchestration` paths.

## Validation commands (paste verbatim output)

```
make validate-agent-assets
make unit-test
shellcheck home/dot_local/bin/common/executable_herdr-agents
shfmt --indent 4 --space-redirects --diff home/dot_local/bin/common/executable_herdr-agents
git -C ~/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
gh pr checks <pr-number>
```

## Completion

1. PR to `main`, English title/description ending with
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. Watch CI
   to green.
2. Artifacts at the exact expected paths; validation with verbatim outputs
   (including the mutation baseline) and the PR number/head SHA.
3. CompactionDB from the main checkout: `python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "<the [memory:decision] text above>"` — paste command and output.
4. Run `~/.agents/skills/agmsg/scripts/inbox.sh dotfiles claude-standard-dot-a005`
   at each milestone (push, CI green, before RESULT) — dispatches to this
   identity are not delivered as turn notices.
5. `AGMSG-RESULT v1` with all artifact paths; `cost:` line in the report.
   Live E2E (a real `--audit` run) is orchestrator-side at acceptance.
