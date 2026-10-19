---
task_id: dotfiles-T133-ci-efficiency-a02
seat: claude-standard-dot-a011
inherited_from: .orchestration/dotfiles-T133-ci-efficiency-a01/measure.md (a01 item 0b, commit 0b7c5b4c)
measured_at: 2026-10-18T04:2xZ (a01, before any change of a01; not re-measured for a02)
---

# Measurement (inherited from a01): the last 30 completed pull-request runs of test.yaml and remote.yaml

The task keeps a01's measurement as the baseline (a02 "The existing measurement … remains the measurement baseline"). Everything below the next rule is a01's record, unchanged: its method, the script, the tables, the measured failure lines and the Q4 decision. a02 adds nothing measured. Its production-registry test (`tests/unit/test_ci_rerun.py::test_the_production_flake_registry_matches_its_samples_and_no_real_failure`) pins the two lines quoted below as the signature's positive sample and a real failure's negative sample: the Snap Store HTTP 408 line, and run 39079197825's `test_validate_agent_assets` ERROR line.

---


# Measurement: the last 30 completed pull-request runs of test.yaml and remote.yaml

## How

One script (below, run from the seat's scratchpad as `python3 -I measure.py "$SCRATCH"`, exit 0) listed each workflow's last 30 completed `pull_request` runs with `gh api repos/mryfmo/dotfiles/actions/workflows/<file>/runs?event=pull_request&status=completed&per_page=30`. That is the per-workflow form of the task's `actions/runs?…&event=pull_request` query, which returns every workflow's runs mixed together. For each run the script read `created_at`, `run_started_at`, `updated_at`, `conclusion` and `run_attempt`, and through `gh api repos/mryfmo/dotfiles/actions/runs/<id>/jobs?per_page=100` each job's `created_at`, `started_at`, `completed_at`, `conclusion` and each step's `started_at`/`completed_at`. Definitions:

- Run wall time: `created_at` to `updated_at`.
- Queued: per run, the longest job queue, which is a job's `created_at` to `started_at`.
- Per-job figures: median over the 30 runs.

The jobs endpoint returns the latest attempt only, so the one run with `run_attempt > 1` had its first attempt read with `gh api …/runs/<id>/attempts/1/jobs`. The failed jobs' logs were read with `gh run view <run> [--attempt 1] --job <job> --log-failed`. That needed network to `results-receiver.actions.githubusercontent.com`, granted per command, and `XDG_CACHE_HOME=$TMPDIR/gh-cache`, because the sandbox denies `~/.cache/gh`.

<details><summary>measure.py</summary>

```python
"""Validation-only: measure the last 30 completed pull-request runs of test.yaml and remote.yaml (T133 item 0b)."""

import json
import re
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path

OUT = Path(sys.argv[1])
REPO = "repos/mryfmo/dotfiles"
FLAKE = re.compile(
    r"timed? ?out|timeout|could not resolve|connection (reset|refused|timed)|temporary failure|"
    r"\b50[234]\b|rate limit|tap|curl: \(\d+\)|unable to access|econnreset|etimedout|network",
    re.I,
)


def gh(*args):
    return subprocess.run(
        ["gh", *args], capture_output=True, text=True, check=True
    ).stdout


def ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")) if value else None


def secs(start, end):
    return (ts(end) - ts(start)).total_seconds() if start and end else None


def med(values):
    values = [v for v in values if v is not None]
    return round(statistics.median(values)) if values else None


data = {}
for workflow in ("test.yaml", "remote.yaml"):
    runs = json.loads(
        gh(
            "api",
            f"{REPO}/actions/workflows/{workflow}/runs?event=pull_request&status=completed&per_page=30",
        )
    )
    rows = []
    for run in runs["workflow_runs"]:
        jobs = json.loads(
            gh("api", f"{REPO}/actions/runs/{run['id']}/jobs?per_page=100")
        )["jobs"]
        rows.append(
            {
                "run": {
                    k: run[k]
                    for k in (
                        "id",
                        "created_at",
                        "run_started_at",
                        "updated_at",
                        "conclusion",
                        "run_attempt",
                        "head_sha",
                    )
                },
                "jobs": jobs,
            }
        )
    data[workflow] = rows
(OUT / "measure-raw.json").write_text(json.dumps(data))

lines = []
for workflow, rows in data.items():
    wall = [secs(r["run"]["created_at"], r["run"]["updated_at"]) for r in rows]
    queued = [
        max((secs(j["created_at"], j["started_at"]) or 0) for j in r["jobs"])
        for r in rows
        if r["jobs"]
    ]
    per_job, steps, failed = {}, {}, []
    for r in rows:
        for j in r["jobs"]:
            per_job.setdefault(j["name"], {"run": [], "queue": []})
            per_job[j["name"]]["run"].append(secs(j["started_at"], j["completed_at"]))
            per_job[j["name"]]["queue"].append(secs(j["created_at"], j["started_at"]))
            for s in j.get("steps") or []:
                steps.setdefault((j["name"], s["name"]), []).append(
                    secs(s.get("started_at"), s.get("completed_at"))
                )
            if j["conclusion"] == "failure":
                failed.append((r["run"]["id"], j["id"], j["name"]))
    lines.append(
        f"### {workflow} ({len(rows)} completed pull-request runs, {rows[-1]['run']['created_at']} to {rows[0]['run']['created_at']})\n"
    )
    lines.append(
        f"- run wall time (created_at to updated_at), median: {med(wall)} s; longest: {round(max(w for w in wall if w is not None))} s"
    )
    lines.append(
        f"- queued (the longest job queue of a run, job created_at to started_at), median: {med(queued)} s; longest: {round(max(queued))} s"
    )
    lines.append(
        f"- conclusions: {dict(sorted({c: [r['run']['conclusion'] for r in rows].count(c) for c in {r['run']['conclusion'] for r in rows}}.items()))}; runs with run_attempt > 1: {sum(r['run']['run_attempt'] > 1 for r in rows)}\n"
    )
    lines.append(
        "| job | runs | median run (s) | median queue (s) | longest queue (s) |"
    )
    lines.append("|---|--:|--:|--:|--:|")
    for name, v in sorted(per_job.items()):
        lines.append(
            f"| {name} | {len(v['run'])} | {med(v['run'])} | {med(v['queue'])} | {round(max(q for q in v['queue'] if q is not None))} |"
        )
    lines.append("\nThe three longest steps (median over the runs that ran them):\n")
    lines.append("| job | step | runs | median (s) |")
    lines.append("|---|---|--:|--:|")
    for (job, step), v in sorted(steps.items(), key=lambda kv: -(med(kv[1]) or 0))[:3]:
        lines.append(f"| {job} | {step} | {len(v)} | {med(v)} |")
    lines.append("\nSteps whose name names a fetch or install, median over 60 s:\n")
    lines.append("| job | step | runs | median (s) |")
    lines.append("|---|---|--:|--:|")
    for (job, step), v in sorted(steps.items(), key=lambda kv: -(med(kv[1]) or 0)):
        if (
            re.search(
                r"install|setup|fetch|download|checkout|cache|bootstrap|prepare",
                step,
                re.I,
            )
            and (med(v) or 0) > 60
        ):
            lines.append(f"| {job} | {step} | {len(v)} | {med(v)} |")
    lines.append(f"\nFailed jobs: {len(failed)}\n")
    for run_id, job_id, name in failed:
        try:
            log = gh("run", "view", str(run_id), "--job", str(job_id), "--log-failed")
        except subprocess.CalledProcessError as error:
            log = f"<log unavailable: {error.stderr.strip()[:120]}>"
        hits = [
            ln.split("\t")[-1].strip()[:200]
            for ln in log.splitlines()
            if FLAKE.search(ln.split("\t")[-1])
        ]
        lines.append(
            f"- run {run_id} job {job_id} `{name}`: {len(hits)} candidate flake line(s)"
        )
        for hit in hits[:5]:
            lines.append(f"  - `{hit}`")
    lines.append("")
(OUT / "measure-table.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
```

</details>

## Results (the script's output, verbatim)

### test.yaml (30 completed pull-request runs, 2026-10-17T15:23:28Z to 2026-10-17T23:55:00Z)

- run wall time (created_at to updated_at), median: 557 s; longest: 834 s
- queued (the longest job queue of a run, job created_at to started_at), median: 10 s; longest: 487 s
- conclusions: {'failure': 1, 'success': 29}; runs with run_attempt > 1: 0

| job | runs | median run (s) | median queue (s) | longest queue (s) |
|---|--:|--:|--:|--:|
| test (macos-14, client) | 30 | 453 | 10 | 487 |
| test (ubuntu-24.04, client) | 30 | 523 | 2 | 7 |
| test (ubuntu-24.04, server) | 30 | 351 | 2 | 3 |
| test (ubuntu-26.04, client) | 30 | 530 | 2 | 4 |

The three longest steps (median over the runs that ran them):

| job | step | runs | median (s) |
|---|---|--:|--:|
| test (macos-14, client) | Run Python unit tests | 30 | 353 |
| test (ubuntu-26.04, client) | Run Python unit tests | 30 | 251 |
| test (ubuntu-24.04, client) | Run Python unit tests | 30 | 248 |

Steps whose name names a fetch or install, median over 60 s:

| job | step | runs | median (s) |
|---|---|--:|--:|

Failed jobs: 1

- run 39079197825 job 117532515811 `test (ubuntu-24.04, client)`: 0 candidate flake line(s)

### remote.yaml (30 completed pull-request runs, 2026-10-17T15:23:28Z to 2026-10-17T23:55:00Z)

- run wall time (created_at to updated_at), median: 615 s; longest: 1203 s
- queued (the longest job queue of a run, job created_at to started_at), median: 28 s; longest: 591 s
- conclusions: {'success': 30}; runs with run_attempt > 1: 1

| job | runs | median run (s) | median queue (s) | longest queue (s) |
|---|--:|--:|--:|--:|
| private-bootstrap (macos-14, client) | 30 | 12 | 8 | 516 |
| private-bootstrap (ubuntu-24.04, client) | 30 | 8 | 2 | 3 |
| private-bootstrap (ubuntu-24.04, server) | 30 | 9 | 2 | 2 |
| public-bootstrap (macos-14, client) | 30 | 550 | 8 | 591 |
| public-bootstrap (ubuntu-24.04, client) | 30 | 590 | 2 | 3 |
| public-bootstrap (ubuntu-24.04, server) | 30 | 491 | 2 | 3 |

The three longest steps (median over the runs that ran them):

| job | step | runs | median (s) |
|---|---|--:|--:|
| public-bootstrap (ubuntu-24.04, client) | Bootstrap the checked-out public source | 30 | 574 |
| public-bootstrap (macos-14, client) | Bootstrap the checked-out public source | 30 | 535 |
| public-bootstrap (ubuntu-24.04, server) | Bootstrap the checked-out public source | 30 | 471 |

Steps whose name names a fetch or install, median over 60 s:

| job | step | runs | median (s) |
|---|---|--:|--:|
| public-bootstrap (ubuntu-24.04, client) | Bootstrap the checked-out public source | 30 | 574 |
| public-bootstrap (macos-14, client) | Bootstrap the checked-out public source | 30 | 535 |
| public-bootstrap (ubuntu-24.04, server) | Bootstrap the checked-out public source | 30 | 471 |

Failed jobs: 0



Every step with a median of 20 s or more (skipped steps excluded; from the same raw JSON, verbatim):

#### test.yaml: every step with a median of 20 s or more (skipped steps excluded)

| job | step | runs | median (s) |
|---|---|--:|--:|
| test (macos-14, client) | Run Python unit tests | 27 | 358 |
| test (ubuntu-26.04, client) | Run Python unit tests | 27 | 256 |
| test (ubuntu-24.04, client) | Run Python unit tests | 27 | 248 |
| test (ubuntu-24.04, server) | Run Python unit tests | 27 | 247 |
| test (ubuntu-26.04, client) | Run unit test | 26 | 226 |
| test (ubuntu-24.04, client) | Run unit test | 26 | 209 |
| test (macos-14, client) | Run unit test | 26 | 41 |
| test (ubuntu-24.04, server) | Run unit test | 26 | 40 |
| test (ubuntu-24.04, server) | Install tools | 27 | 20 |
| test (ubuntu-24.04, client) | Install tools | 27 | 20 |

#### remote.yaml: every step with a median of 20 s or more (skipped steps excluded)

| job | step | runs | median (s) |
|---|---|--:|--:|
| public-bootstrap (ubuntu-24.04, client) | Bootstrap the checked-out public source | 27 | 575 |
| public-bootstrap (macos-14, client) | Bootstrap the checked-out public source | 27 | 538 |
| public-bootstrap (ubuntu-24.04, server) | Bootstrap the checked-out public source | 27 | 474 |

The script's "0 candidate flake line(s)" for the one failed test.yaml job is not a reading: its log download was refused by the sandbox's network filter, as the next section shows. The logs below were read afterwards with the log host allowed.

## Failed runs and flake signatures (item 4's seed)

The window holds two failures.

1. **test.yaml run 39079197825, `test (ubuntu-24.04, client)` (PR #400, `fix/claude-pinned-merge-gate`, head `eb6af9e5`): a real failure, not a flake.** The failure lines of its `--log-failed` output:

```console
$ XDG_CACHE_HOME="$TMPDIR/gh-cache" gh run view 39079197825 --job 117532515811 --log-failed | awk -F'\t' '{print $NF}' | grep -E '##\[error\]|^[0-9TZ:.-]+ (FAIL|ERROR):|AssertionError|Traceback|FAILED \(|not ok [0-9]' | head -20 | cut -c1-240
2026-10-17T23:31:08.3855694Z ERROR: model profile standard.claude.model must be a launcher-safe string
2026-10-17T23:31:08.3856271Z ERROR: model_profiles must define the express profile
2026-10-17T23:31:14.6171151Z ERROR: worker_worktree must be a relative path under .claude/worktrees/: '/abs/.claude/worktrees/x'
2026-10-17T23:31:14.6171959Z ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/..'
2026-10-17T23:31:14.6172955Z ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/a/b'
2026-10-17T23:31:14.6173722Z ERROR: worker_worktree must be a relative path under .claude/worktrees/: '.claude/worktrees/$(x)'
2026-10-17T23:34:03.4319369Z ERROR: test_claude_gh_merge_gate_keeps_writes_on_ask_and_requires_the_hook (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_gh_merge_gate_keeps_writes_on_ask_and_requires_the_hook)
2026-10-17T23:34:03.4320796Z Traceback (most recent call last):
2026-10-17T23:34:03.4333596Z ERROR: test_claude_sandbox_validator_refuses_each_forbidden_form (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='macOS gh exclusion')
2026-10-17T23:34:03.4334515Z Traceback (most recent call last):
2026-10-17T23:34:03.4341592Z ERROR: test_claude_sandbox_validator_refuses_each_forbidden_form (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='Linux extra exclusion')
2026-10-17T23:34:03.4342511Z Traceback (most recent call last):
2026-10-17T23:34:03.4350129Z ERROR: test_claude_sandbox_validator_refuses_each_forbidden_form (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='Mach allowlist')
2026-10-17T23:34:03.4355755Z Traceback (most recent call last):
2026-10-17T23:34:03.4364451Z ERROR: test_claude_sandbox_validator_refuses_each_forbidden_form (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='all Unix sockets')
2026-10-17T23:34:03.4365849Z Traceback (most recent call last):
2026-10-17T23:34:03.4372851Z ERROR: test_claude_sandbox_validator_refuses_each_forbidden_form (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='cafe.github.com')
2026-10-17T23:34:03.4373778Z Traceback (most recent call last):
2026-10-17T23:34:03.4380584Z ERROR: test_claude_sandbox_validator_refuses_each_forbidden_form (test_validate_agent_assets.ValidateAgentAssetsTest.test_claude_sandbox_validator_refuses_each_forbidden_form) (form='datadoghq.com')
2026-10-17T23:34:03.4381630Z Traceback (most recent call last):
```

The `ERROR: model profile …` and `ERROR: worker_worktree …` lines are expected output of passing negative tests. The failure is the `test_validate_agent_assets` errors of that PR's own change.

2. **remote.yaml run 39046848147, attempt 1, `public-bootstrap (ubuntu-24.04, client)` (`portability/sandbox-a01`, head `5992fac5`): a network flake.** Attempt 2 concluded `success`. The lines before the step's exit:

```console
$ XDG_CACHE_HOME="$TMPDIR/gh-cache" gh run view 39046848147 --attempt 1 --job 117437164401 --log-failed | awk -F'\t' 'NR>=178196 && NR<=178221 {print $NF}' | grep -E 'error: cannot perform|snapcraft|chezmoi: |chezmoi apply failed|##\[error\]'
2026-10-17T15:53:34.0926260Z error: cannot perform the following tasks:
2026-10-17T15:53:34.0927711Z - Fetch and check assertions for snap "gtk-common-themes" (1535) (cannot fetch assertion: got unexpected HTTP status code 408 via GET to "https://api.snapcraft.io/v2/assertions/snap-revision/62rRwo_VHrOdajhLlnNTqUJ8gfWoZZNSFWhxn2AszCKyUAD0d8guxddMFeW5LVKP?max-format=0")
2026-10-17T15:53:34.0959984Z chezmoi: .chezmoiscripts/ubuntu/50-client-install-misc.sh: exit status 1
2026-10-17T15:53:34.0999306Z chezmoi apply failed; completed target operations may remain.
2026-10-17T15:53:34.1130542Z ##[error]Process completed with exit code 1.
```

This seeds `.github/flakes.yaml` with one signature: `snapcraft-assertion-timeout`, matching the job `^public-bootstrap \(ubuntu-` and the log text `cannot fetch assertion: got unexpected HTTP status code (408|5[0-9][0-9]) via GET to "https://api\.snapcraft\.io/`. No macOS Homebrew tap warning appears in the measured failures; test.yaml already resolves the runner image's untrusted taps in-job (`handle_ci_untrusted_taps`). So no tap signature is seeded, and one can be added with its log line when a measured run shows it. A broad "timeout" pattern was not added, because it would also match a real test that times out.

## Q4 (cache), decided

- **test.yaml: no cache.** The only steps over 60 s are the test steps themselves: `Run Python unit tests` (median 247 to 358 s) and `Run unit test` (40 to 226 s). The fetch or install steps are under 60 s; `Install tools` is 20 s on Ubuntu and under 20 s on macOS, since it is absent from the 20 s table.
- **remote.yaml: by the rule, one step qualifies**, `Bootstrap the checked-out public source`, at a median of 474 to 575 s. It is the fresh-machine bootstrap under test, not a separable fetch, so a cache changes what the job proves. Suggested follow-up (`dotfiles-T133-ci-efficiency-followup-a01` or its own task), not added here:
  1. Measure which part of `setup.sh` dominates, from the step's log timestamps.
  2. Only if verified downloads dominate, cache the mise download cache with `actions/cache`, path `~/.cache/mise` under the job's isolated HOME, key `${{ runner.os }}-${{ matrix.system }}-mise-${{ hashFiles('home/dot_mise/config.toml', 'home/dot_config/mise/config.toml.tmpl') }}`. Each install still verifies its pinned checksums.
  3. Never cache Homebrew or apt state, which is the path under test.
- Item 3 of this task already skips the bootstrap on a pull request whose diff cannot affect it. How many of the 30 measured runs it would have skipped was not measured.

## Reading of the figures

- The macOS jobs carry the long queues: `test (macos-14, client)` up to 487 s, `public-bootstrap (macos-14, client)` up to 591 s, and `private-bootstrap (macos-14, client)` up to 516 s, although it only decides and skips (median run 12 s). Moving private-bootstrap off pull requests (item 2) and skipping macOS for OS-independent diffs (item 3) both reduce that queue.
- No run in the window was superseded and cancelled, because none had a concurrency group. Item 1 adds one, so a newer head cancels the older run.
