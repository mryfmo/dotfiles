# omp seat tool policies

One omp settings overlay per seat role. chezmoi applies them to `~/.agents/omp/policies/<role>.yml`, and the seat launcher passes the role's file as `--config ~/.agents/omp/policies/<role>.yml` when it starts omp. On the pi-claude-bridge route the child Claude Code runs with `tools: []`, so these overlays are the only tool gate for a Claude-routed seat.

| File               | Seat         | Mode         | Tool denies                                                 | Bash rules                                                                                                                                                                                                |
| ------------------ | ------------ | ------------ | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `orchestrator.yml` | orchestrator | `yolo`       | `eval`                                                      | denies `gh pr merge … --admin`, allows the audited `gh pr merge <n> --squash --match-head-commit <sha>`, then the common denies, then `gh pr create`, `gh pr ready`, `gh pr comment` and every `git push` |
| `worker.yml`       | worker       | `yolo`       | `eval`                                                      | the common denies, then every push whose target branch is `main`                                                                                                                                          |
| `audit.yml`        | audit        | `always-ask` | `edit`, `write`, `ast_edit`, `eval`, `task`, `manage_skill` | the common denies, then read-only `git` and `gh` allows (`status`, `diff`, `log`, `show`, `rev-parse`, `ls-files`, `pr view`, `pr diff`, `pr checks`, `run view`, `api repos/…`), then a catch-all deny   |

The common denies are the same list in every file: `sudo`, `rm -rf`, `curl`/`wget` piped to `sh` or `bash`, `gh release`, `npm publish`, `uv publish`, `terraform apply`, `kubectl apply`, `gh pr merge`/`edit`/`close`/`review`/`update-branch`, `gh issue`, and `gh api` with a `POST`/`PATCH`/`PUT`/`DELETE` method or a `-f`/`-F`/`--field`/`--raw-field` body. `tests/unit/test_omp_seat_policy.py` fails when the three copies drift.

## Mechanism (omp 18.11.3, `@oh-my-pi/pi-coding-agent`)

- `tools.approvalMode` (`src/tools/settings.ts:311-318`) is `always-ask`, `write` or `yolo`. `always-ask` auto-approves read-tier tools only; a write or exec tool without an explicit rule prompts, and a headless seat fails a prompt instead of allowing the call (`docs/approval-mode.md`, "a call that still requires a prompt fails").
- `tools.approval.<tool>: allow | deny | prompt` (`src/tools/settings.ts:295-305`) is honoured in every mode; a user `deny` is absolute (`src/tools/approval.ts:249-257`).
- `bash.patterns` (`src/exec/settings.ts:134-145`) is an ordered list of `{match, approval}` rules over the `bash` tool's command. `*` is the only wildcard; whitespace runs collapse to one space before matching (`src/tools/bash.ts:239-249`). The first matching rule wins. A `deny` matches the whole command or any one segment split on `;`, `&&`, `||`, `|`, `&`, parentheses and newlines; an `allow` must match the whole command and never a line with shell control characters (`src/tools/bash.ts:281-314`). A matched deny is absolute even in `yolo`; a matched allow runs at the `write` tier (`src/tools/bash.ts:533-540, 578`).
- `--config <file>` loads a strict per-process overlay: a missing file, invalid YAML or a top-level list is a hard error at start, so a seat never starts without its policy (`docs/settings.md`, "One-shot overlays").

## Limits

- Approval is not containment. An allowed program keeps the seat's filesystem, network and subprocess access; the operating-system account and the worktree remain the boundary (`docs/settings.md`, "Bash command approval patterns").
- `bash.patterns` do not reach a shell started through `eval`, so every file sets `tools.approval.eval: deny`.
- shortcut: omp 18.11.3 has no per-path write rule, so "no writes outside the clone" for the worker rests on its worktree and account; add a path rule when omp ships one.
- shortcut: the worker's push rules cover `git push … main`, `… HEAD:main`, `… <branch>:main` and the `git -c … push` spelling; `+main` and `refs/heads/main` pass here and stop at the GitHub ruleset that makes `main` PR-only. A commit message that contains both `push` and `main` is refused by the same rules; reword it.
- The test's evaluator mirrors omp's matcher (`src/tools/bash.ts:239-314, 504-588`; `src/tools/approval.ts:207-323`); omp exposes no evaluator to call, so a divergence shows up only in a live seat.

## Verify

```bash
uv run python -m unittest tests.unit.test_omp_seat_policy -v
```

Dry-run a file against the installed omp without touching the real `~/.omp`:

```bash
HOME="$TMPDIR/omp-home" omp models ls --config home/dot_agents/omp/policies/worker.yml --json > /dev/null
```

A read-back of the parsed values uses the same scratch HOME: copy the file to `$TMPDIR/omp-home/.omp/agent/config.yml`, then `omp config get bash.patterns --json`.
