---
task_id: dotfiles-T129-assets-omp-hcom-followup-a05
seat: claude-standard-dot-a009
branch: tools/assets-omp-hcom-followup-a05
pr: 433
base: 1eac64a832ade83f9e149be6a329f7e8fa20180f
copy_commit: 870aa65d
code_head: none (no script or test changes; the row is an evidence record)
task_sha256: 19abece963764c78868dba0631321e9070ec9b19aeeeabb42de49cc00c387a71
cost: n/a (the seat's token and time usage is not visible to the worker)
---

# Report: dotfiles-T129-assets-omp-hcom-followup-a05 (the assets lineage's owner of the a04 audit's P3)

- **Seat and task file:** `claude-standard-dot-a009` in `.claude/worktrees/worker-c`, from the AGMSG-TASK of message 2551. The dispatched file and the branch copy are byte-identical (validation §1). The task-consistency check passes (§1a).
- **Branch:** a fresh `tools/assets-omp-hcom-followup-a05` from `origin/main` `1eac64a8` (§2). `870aa65d` adds the task copy.
- **Scope:** the one row under `## Owned by dotfiles-T129-assets-omp-hcom-followup-a05` in `.orchestration/acceptance/dotfiles-T129-assets-omp-hcom-followup-a04.md` (§3). It asks for evidence, not code, so no script, test or home file changes (§4).

## Item 1: the owned row

| Row id | What this task records | Red-then-green |
|---|---|---|
| `audit:4e743a1:2` (evidence-omission): the GNU-shim red run of the `mktemp` template test is recorded with its command, shim source and output in validation.md, or report.md states the GNU conclusion as an inference from the macOS refusal | **The run itself**, in this task's validation §5. It shows the shim's source and sha256, a probe of the shim against the system `mktemp`, the red run at `725b25bf` with its traceback, a helper run that prints the download path, and the green runs, each with its command and output. §4a shows why it is a shim: this machine has no GNU coreutils `mktemp`. The a04 report's line 26, quoted in §3, claimed this run without its evidence. The claim stands, and this record is its evidence. | `tests/unit/test_update_agent_assets.py::test_update_omp_makes_its_download_directory_under_tmpdir`, the row's test (main's module, byte-identical copy). With the GNU shim first on `PATH` it is red at `725b25bf`, by assertion at line 237, the `update-agent-assets.` prefix check, after line 236 passed. The helper run shows the download at `…/sandbox-tmp/tmp.UxlSWQFE1V/omp-18.11.3.tgz`. It is green at `1eac64a8` (main, which this branch only adds records to) with the shim and without it (§5). |

- **What the shim proves and what it does not:** it reproduces GNU coreutils `mktemp`'s no-template default, `tmp.XXXXXXXXXX` under `$TMPDIR` (else `/tmp`), and its source is in §5. The probe shows it does that. The test's failure under it is the prefix check, so the old code also fails on a platform whose `mktemp` honours `TMPDIR`.
  - That conclusion about real GNU coreutils rests on the shim matching coreutils' documented default. It was not run against coreutils itself, which this machine lacks (§4a).
- **The Check:** both modules pass inside the sandbox, 36 tests (§6). The owned script and the test module are unchanged: ShellCheck and ruff are clean (§7). Caps: 0 of 120 and 0 of 400 (§8).

## Review

- **The one pre-push round:** a fresh, read-only general-purpose subagent of this seat, working inside its sandbox, returned `Verdict: correct`. The row is met, and there are no P0, P1 or P2 (the worker-crit JSON and its receipt).
- **Its reproduction:** it repeated the run itself. It is red at `725b25bf` with the shim at line 237, and without the shim at line 236 on the refusal. It is green at the head with and without the shim.
- **Its four P3 record inaccuracies**, all fixed in this records commit (the one correction round):
  - when §5 ran;
  - the `-I` claim;
  - the probe's quoted path;
  - the source of the download path.

## Completion

- **PR:** #433, opened ready for review, not as a draft, at 2026-10-19T20:29:21Z on `c5c34955`, inside the sandbox (validation §10). No `@codex review` comment is posted.
- **CI on `c5c34955`:** 11 of 11 checks pass (§11).
- **The Bot, unavailable:** both reviews the PR's opening triggered failed on Codex usage limits. The code review failed at 20:29:24Z: "Codex usage limits have been reached for code reviews". The security review failed at 20:29:30Z: "The account paying for this security review has reached its Codex usage limits". So no Bot review of this change exists. There are no review threads or review comments (§12).
  - Raising the limit is the repository admins' or the paying account's step, outside this seat. The worker posts no `@codex review`. This is for the orchestrator to decide at the gate.
- **The final head** adds only this directory's records on top of `c5c34955`. The RESULT carries its CI.
- **Open items:** no Bot thread, no advisory row and no open question. Any advisory P2 belongs to `dotfiles-T129-assets-omp-hcom-followup-a06`.
