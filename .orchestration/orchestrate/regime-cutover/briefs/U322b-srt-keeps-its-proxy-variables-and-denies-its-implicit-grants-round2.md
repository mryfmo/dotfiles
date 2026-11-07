# U322b round 2 of U322: the build's environment is sanitised before srt so srt's proxy variables reach pnpm, srt's implicit write grants are denied, and every new decision has its injection

GOAL
The round-1 audit of PR 718 (`verdicts/U322-2feb0446.md`, incorrect, class sandbox-boundary) found two blocking defects and one test gap in `build_under_srt` (`scripts/update-agent-assets.sh`). P1 (`:1941`): the function runs `srt --settings <file> -- /usr/bin/env -i HOME=... PATH=... <command>`, so the `env -i` inside srt strips the `HTTP_PROXY`, `HTTPS_PROXY` and `SANDBOX_RUNTIME` variables srt injects into its child, while srt's sandbox allows outbound connections only through those proxies; an uncached `pnpm install` cannot reach even the allowed registry (the auditor measured the variables disappearing through the fixture's fake srt and read srt 0.0.81's generated policy). P1 (`:1934`): with `filesystem.denyWrite` empty, srt 0.0.81 grants writes to `/tmp/claude`, `/private/tmp/claude` and `~/.npm/_logs` on its own, so upstream scripts can write shared host paths outside the promised build and store roots; the settings-content threat row is not closed. P2 (`:1902`, f10 s3): the helper's git-common-dir, path-resolution and settings-creation decisions have no failure-injection tests. CI at the head also fails `test (ubuntu-26.04, client)` (run 42339245827, job 128303025182); the failing test names are in `/tmp/u322b/ci-failures.txt` when the coordinator has them before you start, else read the job with `gh run view 42339245827 --job 128303025182 --log-failed` is not yours to run (no `gh`): the coordinator pastes the names into the TASK or the file.

SCOPE
The same branch `fix/dsh-harness-build-under-srt` and PR 718; the tree is `/tmp/dotfiles-wt/U322` at 2feb0446. May write: `scripts/update-agent-assets.sh` (`build_under_srt` and its call sites), `tests/unit/test_update_agent_assets.py`, `docs/deepseek-harness.md` (the paragraph, if a sentence becomes untrue), and the body `../U322b-pr-body.md` (the round-1 body `/tmp/dotfiles-wt/U322-pr-body.final.md` plus `## Round 2` and the corrected table). Not: `hcom-seat`, the superagent step, any other asset step.

CONTEXT
Read the verdict whole. Read srt 0.0.81's behaviour from the installed package (`~/.local/share/mise/installs/npm-anthropic-ai-sandbox-runtime/0.0.81/lib/node_modules/@anthropic-ai/sandbox-runtime/`, read-only): which environment variables it injects into the child (the proxy variables and `SANDBOX_RUNTIME`), and which write paths it adds when `denyWrite` is empty (its policy generation; the auditor names `/tmp/claude`, `/private/tmp/claude`, `~/.npm/_logs`). Read how `hcom-seat`'s dsh row renders `denyWrite` (the per-base deny loop of `seat_sandbox_write`, U189) for the form this kit already uses to close srt's implicit grants.

DATA SHAPE
The environment is sanitised outside srt and completed inside: `/usr/bin/env -i HOME=<HOME> PATH=<the mise shims path> DSH_HOME=<...> srt --settings <file> -- <command...>`, so srt starts from a clean environment and the child receives exactly what srt injects plus the three variables (a test asserts the fake srt sees `HOME`, `PATH` and nothing from the caller such as `AWS_PROFILE` or `GH_TOKEN`, and that the child command receives the fake srt's injected `HTTP_PROXY`). The settings carry `filesystem.denyWrite` naming srt's implicit grants (`/tmp/claude`, `/private/tmp/claude`, `~/.npm/_logs` in `pwd -P` form) and, as before, `allowWrite` of the build directory and `$DSH_HOME/.pnpm-store` only; the npm and pnpm log and cache directories are pointed inside the build directory or the store through the environment (`npm_config_cache`, `npm_config_logs_dir` or their pnpm equivalents, read the tools' documentation in the installed packages), so nothing of the build asks for a host path outside the two roots. Every decision of the helper (the git common directory read, the `pwd -P` resolutions, the settings creation, the lockfile read) has a failure injection whose refusal names the producer.

CHANGE
1. Move `env -i` outside `srt` as DATA SHAPE says; the child command gets srt's injected variables; a test with the fake `srt` recording its own environment and the command's environment asserts both sides. 2. `denyWrite` with srt's implicit grants in physical form, and the tool caches and logs redirected inside the roots; the real-srt scratch run of round 1 re-run with a build script that attempts writes to `/tmp/claude/<name>` and `~/.npm/_logs/<name>` and asserts both denied (pasted). 3. Failure injections for every decision of the helper the verdict names (git common dir, `pwd -P`, settings creation, the lockfile read), each refusing by name. 4. CI: the ubuntu-26.04 failure fixed (read the names the coordinator provides; if it is the `test_pr_audit` runner class of decisions row 2026-11-07T01:01:00Z, say so and leave it). 5. The body's table: the settings-content row closed by the real-srt assertion of CHANGE 2 and the fake-srt environment test, every row a selector; `## Round 2` naming the two P1s, the P2 and the CI line; `Program-Unit: regime-cutover/U322` once and the footer. 6. The generator; `make render-check`; `uv run --with pyyaml python scripts/validate-agent-assets.py`; `make shellcheck`; `shfmt -i 4 -sr -d scripts/update-agent-assets.sh`; `uv run ruff format --check` in the CI form; `scripts/lint-comparisons.py --changed`. 7. Commit `fix(updater): the harness build keeps srt's proxy variables, denies srt's implicit grants, and every helper decision has its injection (regime-cutover U322b)` with the trailer.

ACCEPTANCE
1. `uv run --with pyyaml python -m unittest tests.unit.test_update_agent_assets -v` OK (count pasted; the new tests named). 2. The environment test and the denyWrite test fail against 2feb0446 (the round-1 file in place, the `earlier` form the updater tests use) and pass on the head (outputs pasted). 3. The real-srt scratch run: the inside write landed, `/tmp/claude/<name>` and `~/.npm/_logs/<name>` denied, the child saw `HTTP_PROXY` set (print it from the build script), exit passed through (pasted, with the settings file). 4. `make render-check` 0; validate-agent-assets 0. 5. shellcheck 0; shfmt 0; ruff 0; lint-comparisons 0.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator re-runs item 3 on the pushed head and reads CI.

CLOSURE
remove

TRUST
TRUST: the unit trusts srt as the boundary and its injected proxy as the only network path of the build; it trusts the dsh role's deny list and srt's own implicit-grant list as what must be denied; it reads no credential, runs no real dsh outside the scratch host.

TIMEBOX
60 minutes.

FORBIDDEN
No `env -i` inside srt; no wildcard domain; no `allowLocalBinding` true; no write under the real `~/.dsh`, `~/.omp`, `~/.local/state`, `~/Workspace`; no network except the scratch run inside srt; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u322b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U322`.
- Progress line at `../U322b-progress.txt`; final report to `../U322b-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), `git diff --stat 2feb0446 HEAD`, the ACCEPTANCE lines with their outputs, the settings file pasted, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 24, 27, 29, 34, 44, 46); `verdicts/U322-2feb0446.md`; the U322 brief `briefs/U322-the-harness-build-runs-inside-srt.md`; the U189 row of units.tsv (the per-base deny loop closing srt's implicit grants in hcom-seat).
