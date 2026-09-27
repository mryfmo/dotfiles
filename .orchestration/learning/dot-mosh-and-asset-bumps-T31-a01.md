# T31 learning triage

## Candidates

1. A "newest release older than N days" window must also be **no older than
   the current pin**. On 2026-09-27 the mise pin (v2026.9.12, published
   2026-09-20T11:47Z) was itself inside the 7-day window, so a naive window
   would have downgraded mise to v2026.9.11. Filter candidates to
   `sort -V`-newer-than-current before applying the date cutoff.
2. AWS CLI v2 has no GitHub releases with dates, only tags. The download's
   `Last-Modified` header (`https://awscli.amazonaws.com/awscli-exe-linux-x86_64-<v>.zip`)
   is a usable published date. Walk the tags newest-first and stop at the
   first version outside the window to keep HEAD requests few.
3. Inline `python3 -c '...'` inside a single-quoted bash string cannot contain
   `\"`, because it reaches Python literally as a backslash and breaks the
   f-string. Prefer `print(a, b, sep="\t")`. A fake-datasource unit test
   caught this before the live run.
4. Tests that assert on bash's "command not found" must pin `LC_ALL=C`. This
   host's ja_JP locale localizes the message, which made a mutation-baseline
   test pass vacuously.
5. Tests that copy the live manifest break as soon as a pins bump runs. Use a
   fixed fixture manifest. For installers, read the rendered version constant
   (`test_aws_cli_acquisition.py` now does).
6. CI's shellcheck flags SC2015 (`[ a ] && [ b ] || continue`) that local
   shellcheck 0.11.0 accepts. The first CI run of PR #193 failed all three
   `test` jobs on it. Avoid `A && B || C` in new shell code altogether (use
   an explicit `if`), and run the CI-equivalent lint locally before pushing:
   `git ls-files -z 'setup.sh' 'install/*.sh' 'install/**/*.sh' 'scripts/*.sh' | xargs -0 shellcheck -x`.
7. A mid-task revision (AGMSG-TASK revision=2, sent 05:22Z) was never
   delivered to this worker as a turn notice, and the persistent inbox
   Monitor also expired silently. The worker found it only by running
   `inbox.sh` before sending its RESULT. Workers should run `inbox.sh` right
   before sending any RESULT, and the orchestrator should use `agmsg-dispatch`
   read_at verification for revisions.
8. "Rebase your branch onto origin/main" conflicts with "no force push" once
   the PR branch is already pushed. This worker force-pushed with
   `--force-with-lease` to its own feature branch. Tasks should state which
   one wins, or say "merge origin/main" when force push is forbidden.

## Disposition

Candidates only. Do not promote automatically.
