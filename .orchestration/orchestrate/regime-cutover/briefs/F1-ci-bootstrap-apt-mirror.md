# U15 CI: public-bootstrap on ubuntu-24.04 stops stalling on the Azure apt mirror — brief

GOAL
The `public-bootstrap` job in `.github/workflows/remote.yaml` no longer runs 19 to 65 minutes when the GitHub-hosted runner's Azure apt mirror trickles: on Linux runners the job removes `azure.archive.ubuntu.com` from `/etc/apt/apt-mirrors.txt` before the bootstrap (apt's `mirror+file:` failover to `archive.ubuntu.com` and `security.ubuntu.com` stays), prints that file before and after as evidence, and carries `timeout-minutes: 30` so a stalled run is cancelled instead of running to GitHub's default of 360 minutes. The installers under `install/` do not change: the slow mirror is a defect of the runner image, not of the machines the dotfiles bootstrap.

SCOPE
One branch `ci/public-bootstrap-apt-mirror` from `origin/main` in your clone. May write: `.github/workflows/remote.yaml` only. May not write: `install/**`, `setup.sh`, the other workflows (if `private-bootstrap.yaml` shows the same stall, name it in the report as a follow-up), tests (read them; if one must change to accept the new step, stop and report `status=question` with the failing assertion instead of editing it).

CONTEXT
- Evidence (map review 2026-10-23T21:58:15Z, `.project-map/state.json` parts[ci-bootstrap].evidence_20261023T1415Z and decisions.tsv 2026-10-23T13:42:43Z): of 38 jobs on 2026-10-23 that ran the step "Bootstrap the checked-out public source", 25 took 7.4 to 13.6 min (median 10.2), 11 took 19 to 65 min (7 green, 4 cancelled while running); the four slow logs read (job ids 120401040047, 120434169607, 120388095735, 120461785554) all stall in apt downloads from `azure.archive.ubuntu.com` (fonts-noto-cjk 61.2 MB took 1487 s in run 3153f9ce, 955 s in b2600711; cmake 11.2 MB 229 to 269 s). Six of sixteen main pushes took 43 to 65 min. The job has no `timeout-minutes` (only `regime.yml` has one).
- Upstream: actions/runner-images#14823 (open; a contributor replied 2026-10-01 "we're aware of this issue and are currently working on the case"): the ubuntu-24.04 image sets `Acquire::Retries "1"` and `Acquire::http::Timeout "15"` since #14594, which fires only when no data arrives for 15 s, so a trickling transfer never fails over; "apt has no minimum-throughput setting"; one user deletes the azure line from `/etc/apt/apt-mirrors.txt` before retrying. actions/runner-images#15040 (2026-10-22): `apt-get update` silent 15+ min after an Azure failover on image 20261012.334.1. The runner configures apt through `mirror+file:/etc/apt/apt-mirrors.txt` with the Azure host first and the standard mirrors after it (gist by artem-zinnatullin, "Override Slow GitHub Actions APT Mirrors": keep the `mirror+file:` mechanism, remove Azure from the candidates, no network access in the step).
- GitHub docs, workflow syntax, `jobs.<job_id>.timeout-minutes`: "The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360".
- Workflow invariants pinned by tests, read both before editing: `tests/unit/test_workflow_security.py` (exact top-level `permissions`, no job-level permission overrides, actions pinned by full SHA, `persist-credentials: false` on checkout) and `tests/unit/test_workflow_orchestration_skip.py` (`REMOTE = WORKFLOWS / "remote.yaml"`: the decide step, required contexts, no job-level `if`/`needs` on a required job, "every heavy step carries its jobs decision", "both bootstrap jobs decide with the same script"). The new step is a heavy step: it must carry the same decision condition as the bootstrap step, plus `runner.os == 'Linux'` so the macos-14 leg skips it. Check the test's matcher for the exact form it accepts.
- The job matrix is ubuntu-24.04 client, ubuntu-24.04 server, macos-14 client; the step must not touch macOS.
- Your own policy overlay (`~/.agents/omp/policies/worker.yml`) denies any bash command containing `sudo ` anywhere in the line, so the new step's `sudo sed -i` must be written with your edit tool, never through a heredoc or `printf` in bash; keep `sudo` out of commit messages and PR titles, and pass the PR body with `--body-file`. A `grep 'sudo sed'` in bash will be refused too; read the file with your read tool instead.

ACCEPTANCE
1. `public-bootstrap` has `timeout-minutes: 30` at job level (over twice the normal maximum of 13.6 min; a cancelled run is a visible signal, a 47-minute green one is not).
2. A new step before "Bootstrap the checked-out public source", Linux-only and gated by the decide output, in `shell: bash` with `set -euo pipefail`, that: prints `/etc/apt/apt-mirrors.txt` or the line `apt-mirrors.txt absent; nothing to change` when the file does not exist; removes every line containing `azure.archive.ubuntu.com` with `sudo sed -i`; fails the job if the file existed and no `priority:` line remains; prints the file after the edit. No network access in the step. A one-line comment names the upstream issue (#14823) as the reason.
3. `make unit-test` green locally (paste the summary line); `uv run --no-project python -m unittest tests.unit.test_workflow_security tests.unit.test_workflow_orchestration_skip -q` green (paste).
4. PR open from your branch, title `ci(remote): public-bootstrap drops the Azure apt mirror on Linux runners and gets a 30-minute timeout`, body with `Program-Unit: regime-cutover/U15`, the two upstream links, the evidence paragraph above, and the footer (STANDING 14). CI green (`gh pr checks <n> --watch`, paste).
5. From the PR's own run: for the ubuntu-24.04 client and server jobs, paste the step's before and after mirror lines, the number of apt `Get:` lines naming `azure.archive.ubuntu.com` (expect 0) and `archive.ubuntu.com` (expect > 0) from the bootstrap step log (`gh run view <run id> --log --job <job id> | grep -c ...`), and the job durations (`gh api repos/mryfmo/dotfiles/actions/runs/<run id>/jobs --jq '.jobs[] | [.name, .started_at, .completed_at] | @tsv'`). The macOS job's duration unchanged.

VERIFY
The commands above. Network: `api.github.com`, `github.com` only.

TIMEBOX
2 hours. On expiry, push what you have, report the partial findings and stop.

FORBIDDEN
No change under `install/` or to `setup.sh`; no step-level `timeout-minutes` that would hide the apt behaviour; no `apt-get` options added anywhere; no retries loop around the bootstrap; no edits outside SCOPE; no merge, rebase, force-push or PR close.

REPORT
Shape per STANDING 12, under 200 words: status, branch, head sha, PR link, CI state, the pasted before/after mirror lines, the `Get:` counts, the job durations, deviations, follow-ups (name `private-bootstrap.yaml` if it shows the same stall). Then the RESULT line per the hcom-worker skill, with the `bus-history.sh` row as proof of delivery.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` before any command (its line 20 is this unit's regime: you are the omp worker seat).

## Threat table

The change edits a required check's job (`public-bootstrap`), so it is a trust-boundary change (AGENTS.md "Orchestration records and trust-boundary code"). One row per `allowed_files` entry, per non-path control and per orchestrator effect; dispositions in the three forms of the agmsg-orchestration SKILL.

| control | disposition |
| --- | --- |
| `.github/workflows/remote.yaml` (the only file in SCOPE; the job's permissions, action pins, checkout settings, required-context shape and the decision gating of every heavy step) | closed: `tests/unit/test_workflow_orchestration_skip.py::test_every_heavy_step_carries_its_jobs_decision` (with `tests/unit/test_workflow_security.py::test_workflows_have_exact_top_level_permissions`, `::test_workflows_have_no_job_level_permission_overrides`, `::test_external_actions_use_full_commit_shas`, `::test_checkout_does_not_persist_credentials_without_explicit_exemption`; 29 tests OK on f225d5d2; CI `validate` green) |
| `timeout-minutes: 30` on the required `public-bootstrap` check (non-path control: a slow run is cancelled instead of reported green late) | residual: the normal band is 7.4 to 13.6 min and the mirror step removes the only measured cause (8.3 and 9.0 min on this head against 47.1 min on main b2600711), so a cancellation now marks a new defect; a cancelled required check blocks the merge until `scripts/orchestrator/ci-rerun.sh` or a rerun, never a silent pass |
| The step "Drop the Azure apt mirror from the runner image" (non-path control: `sudo sed -i` on `/etc/apt/apt-mirrors.txt`, an input of the runner image, never of the pull request; Linux-only and gated by the decide output) | residual: the step prints the file before and after and fails the job when no `priority:` line remains; this head's run prints `priority:2` and `priority:3` after the edit on both ubuntu jobs (120715225526, 120715225551) and the bootstrap log has 0 `Get:` lines from `azure.archive.ubuntu.com` and 100 / 55 from `archive.ubuntu.com` |
| An image without `/etc/apt/apt-mirrors.txt` (in-process effect of the step: a no-op) | residual: the step prints `apt-mirrors.txt absent; nothing to change` and exits 0, so the job keeps the image's own mirror list and the 30-minute timeout bounds the old failure mode visibly |
| `private-bootstrap.yaml` (same bootstrap, same image, outside SCOPE) | out-of-scope: U23 |
| Merge (orchestrator effect) | residual: the coordinator merges with `gh pr merge 480 --squash --match-head-commit f225d5d2` after this table and the ledger row; the base has not moved since the branch was cut, so no update-branch; no forced removal |
