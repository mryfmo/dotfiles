---
task_id: dotfiles-T128-seat-launch-args-review-a01
seat: claude-standard-dot-a003
reviewed: .orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md
reviewed_sha256: 4171f67c3fb429f7f4ff8063ab4bd89d52f7fe1b98003cd4404afaedf0b3b589
brief_sha256: 3e16afb88ebbacd8f2ccc1e22b0dbdd657be1e66aeab492b0e0282ae60620795
origin_main: b167fe0a
---

# Review: dotfiles-T128-seat-launch-args-a01 (review seat, one round)

Read-only. Sources: `scripts/check-regime-boundary.sh`, `tests/unit/test_check_regime_boundary.py`, `home/dot_local/bin/common/executable_herdr-agents` and the agmsg-orchestration SKILL on `origin/main` (`b167fe0a`); the rendered `~/.agents/model-profiles.env` (its keys and values read, nothing changed); the installed agmsg `spawn.sh`, `lib/boot-command.sh`, `drivers/types/claude-code/type.conf`, `drivers/types/codex/type.conf` and `codex-shim.sh` (code read only, no agmsg data); the codex install (`mise` npm `@openai/codex`, `bin/codex -> codex.js`, a `#!/usr/bin/env node` wrapper).

## Checks run

```text
$ shasum -a 256 .orchestration/tasks/dotfiles-T128-seat-launch-args-review-a01.md .orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md
3e16afb88ebbacd8f2ccc1e22b0dbdd657be1e66aeab492b0e0282ae60620795  .orchestration/tasks/dotfiles-T128-seat-launch-args-review-a01.md
4171f67c3fb429f7f4ff8063ab4bd89d52f7fe1b98003cd4404afaedf0b3b589  .orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md
$ the three premises, origin/main fetched (b167fe0a)
absent
0
1
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> <file>
dotfiles-T128-seat-launch-args-a01.md: OK
$ validate-agent-assets.py --mask-secrets <a copy>; cmp <copy> <file>
masked 0 match(es) in sla.md
unchanged
$ /usr/bin/grep -E '^MODEL_PROFILE_STANDARD_(CLAUDE|CODEX)_ARGS=' ~/.agents/model-profiles.env
MODEL_PROFILE_STANDARD_CLAUDE_ARGS="--model claude-opus-5-5 --effort xhigh --advisor fable"
MODEL_PROFILE_STANDARD_CODEX_ARGS="--profile standard"
$ /usr/bin/grep -n 'SESSION_NAME=' ~/.agents/skills/agmsg/scripts/spawn.sh; /usr/bin/grep -n '^name_arg=\|^resume_arg=' <claude-code type.conf>
396:SESSION_NAME="${TEAM}-${NAME}"
11:name_arg=-n
33:resume_arg=--resume
$ git show origin/main:home/dot_agents/skills/agmsg-orchestration/SKILL.md | /usr/bin/grep -c "including multiple rows for that name across teams"
1
```

What holds: the env's `KEY="value"` form and `MODEL_PROFILE_<NAME>_<KIND>_ARGS` keys; `herdr-agents --add-worker` writes the claude value (or `--profile <name> …` for codex) into spawn.sh's options file (`write_spawn_options`), and spawn.sh's boot command is `<cli> [--resume <uuid>] [model and spawn options] -n <team>-<name> "/… actas <name>"`, so a launcher-started seat carries `-n <team>-<name>` and the pairs, a resumed launcher seat still matches, and a bare `claude --resume` has no `-n`; the codex shim `exec`s the real codex in turn delivery, whose npm wrapper (`node …/bin/codex`) and native child both fit the codex selector. The boundary loop is lines 114 to 139 with `root` at line 39 and the `--report` mode at lines 35 to 38; the harness copies two scripts at its line 76 and its HOME carries no env, so the existing tests run no probe. Output lines and exit codes are stated the same in items 1, 3 and 4. The generic rows are verbatim, the two input rows are non-path controls, and the Completion clause is the template's with the S1 sentence; dispatch.sh's refusal is stated as the pending a04 row.

## Findings

- [P2] high `.orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md:75` — item 2 runs seat-args.sh "for each seated identity row (`<team>\t<name>` per agent type from identities.sh)", and item 1 matches a claude process by `-n <team>-<identity>`; but a worker identity may legitimately have rows in several teams (the SKILL's teardown bullet: "one distinct name per type at its worktree is healthy, including multiple rows for that name across teams"), and spawn.sh names the session after the one team it was spawned in (`SESSION_NAME="${TEAM}-${NAME}"`), so every other team's row finds no process and is reported `args=unlaunched`, a false violation at every boundary for a correctly launched seat. Probe once per distinct name at the worktree and accept `-n <team>-<name>` for any of its teams (or the spawn team the placement record names), and add that case to `test_seat_args.py` or the boundary test.
- [P3] medium `.orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md:74` and `:40` — `/bin/ps` and `/usr/sbin/lsof` are fixed absolute paths; on Linux lsof is usually `/usr/bin/lsof`, and a missing lsof makes every codex seat `process=none args=unlaunched` rather than skipping, while check-regime-boundary.sh's own rule is "a missing tool skips its check" (its line 27). State what seat-args.sh does when either binary is absent (for example `args=unknown-probe` and a skip in the boundary loop), or resolve them as the boundary script resolves its tools.

Task-file verdict: dotfiles-T128-seat-launch-args-a01: revise

## Round 2 (reviewed sha256 148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f, origin/main b167fe0a)

```text
$ shasum -a 256 .orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md
148f5dde8795da8a8eeb265fcbbd40be11cb27e2407c979b772dcbcba772bd8f  .orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md
$ the three premises, origin/main fetched (b167fe0a)
absent
0
1
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root <main checkout> <file>
dotfiles-T128-seat-launch-args-a01.md: OK
$ validate-agent-assets.py --mask-secrets <a copy>; cmp <copy> <file>
masked 0 match(es) in sla2.md
unchanged
```

Both round-1 findings are applied (the Change round 2 section). The P2: seat-args.sh takes the comma-joined teams and accepts `-n <any of them>-<identity>`; the boundary loop groups the identities.sh rows by name and probes each name once; case (a) covers `other,t` (ok) and `other` alone (unlaunched), and the boundary test seats the name in two teams, matches on the second team's `-n`, and asserts the line at most once. The P3: a missing ps, or for codex a missing lsof, is `args=unknown-probe`, exit 4, skipped by the loop; lsof is `/usr/sbin/lsof`, else `/usr/bin/lsof`; case (h) and the boundary test's third case cover it. Items 1, 3 and 4 state the lines and the exit codes (0, 2, 3, 4) the same way; the generic rows and the Completion clause are unchanged and match the template.

### Findings

- [P3] medium `.orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md:19` — the check-regime-boundary.sh row still says the loop "reports its non-zero result as a violation", while item 2 now reports exit 2 or 3 and skips exit 4; one clause ("on exit 2 or 3, skipping exit 4") would keep the row the audit compares against in step with item 2.
- [P3] low `.orchestration/tasks/dotfiles-T128-seat-launch-args-a01.md:25` and `:40` — the input row's control and the workflow row still name `/usr/sbin/lsof` alone ("runs /bin/ps and /usr/sbin/lsof by absolute path"), while item 1 now looks lsof up at `/usr/sbin`, then `/usr/bin`, and item 1's lsof command form (line 74) also names `/usr/sbin/lsof` alone.

Neither changes behaviour or a test; both are wording in the rows. Justified approval: the multi-team and missing-tool behaviours are specified once, consistently in items 1 to 4, and each has a case that fails when the behaviour is wrong.

Task-file verdict (round 2): dotfiles-T128-seat-launch-args-a01: confirm
