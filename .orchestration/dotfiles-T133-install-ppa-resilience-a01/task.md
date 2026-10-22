---
format: 2
task_id: dotfiles-T133-install-ppa-resilience-a01
kind: code
security: false
allowed_files:
  - install/ubuntu/client/ghostty.sh
  - tests/install/ubuntu/client/ghostty.bats
  - .orchestration/dotfiles-T133-install-ppa-resilience-a01/**
after: []
threat_table:
  - {control: "install/ubuntu/client/ghostty.sh", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::an unreachable PPA never fails the apply"}
  - {control: "tests/install/ubuntu/client/ghostty.bats", disposition: "residual: the fixtures replace add-apt-repository and apt-get with fakes that return the PPA's 503; required CI runs the real module on ubuntu-24.04; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "the task-file copy (.orchestration/dotfiles-T133-install-ppa-resilience-a01/task.md)", disposition: "residual: byte-identical to the dispatched text; the orchestrator compares its SHA256 with the TASK line at acceptance; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "the evidence records under .orchestration/dotfiles-T133-install-ppa-resilience-a01/**", disposition: "residual: command output and learning triage; sandbox.md lists refused commands; the audit checks claims against the final head; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "task metadata (kind, security, allowed_files, after, threat_table, premises)", disposition: "residual: the consistency checker parses the mapping before dispatch and at acceptance; byte comparison of the task copy covers changes; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "metadata separators (the --- boundaries in the task copy and evidence records)", disposition: "residual: front matter stays YAML; the checker parses the task and byte comparison covers the whole dispatched file; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "in-process effects (the install script runs apt only through its existing sudo --preserve-env form)", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::an unreachable PPA never fails the apply (fakes), with the live ghostty test tolerant of the probe result"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: no workflow, interpreter or dependency change; the script keeps bash and apt as today; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "new or renamed scripts", disposition: "residual: none; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "orchestrator effect merge", disposition: "residual: only the orchestrator merges the audited head with --match-head-commit after sweep, audit and gate; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "orchestrator effect update-branch", disposition: "residual: a moved head gets fresh CI, sweep, audit and gate before the merge; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; any discarded state is recorded at acceptance; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "orchestrator effect task copy", disposition: "residual: compared byte-for-byte and by SHA256 with the dispatched text at acceptance; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "orchestrator effect records", disposition: "residual: the orchestrator owns acceptance and feedback dispositions; the worker supplies evidence only; owner: dotfiles-T133-install-ppa-resilience-a01"}
premises: []
---

# AGMSG-TASK dotfiles-T133-install-ppa-resilience-a01 — an unreachable Ghostty PPA never fails the apply

Written 2026-10-21T22:22Z by the orchestrator seat. On 2026-10-21 21:0xZ to 22:1xZ the Launchpad PPA `ppa:mkasberg/ghostty-ubuntu` returned HTTP 503 (InRelease and the .deb pool), and the required check `test (ubuntu-24.04, client)` failed on `tests/install/ubuntu/client/ghostty.bats` line 38 for every pull request that ran CI (#442 at b3ca1b80, #378 at 2b586637): `DOTFILES_DEBUG=1 bash install/ubuntu/client/ghostty.sh` exited 100 from apt. A required check that depends on a third party's availability is the defect; the zed installer already models the proper behaviour (`tests/install/ubuntu/client/zed.bats`: "an unreachable release API never fails the apply" and "a failed archive download never fails the apply"). The two re-runs the orchestrator requested were a stopgap; this task is the remedy.

## Item 1

In `install/ubuntu/client/ghostty.sh`: when `add-apt-repository` or the `apt-get update`/`apt-get install` that follows fails because the PPA is unreachable (apt exit 100 with a fetch failure for the PPA host), the script prints one line naming the PPA and how to retry (`make update` later), removes nothing, and exits 0; the dependency packages from the Ubuntu archive still install as today; any other failure (a broken dependency install, a non-PPA apt error) keeps failing as today. Keep PACKAGES, DEPENDENCY_PACKAGES, the sudo `--preserve-env` form and the shdoc comments.

## Item 2

In `tests/install/ubuntu/client/ghostty.bats`: (a) rewrite the live test `[ubuntu-client] ghostty` so the installer's own outcome is the oracle, not a separate probe (a pool-only outage leaves InRelease at 200 while the .deb fetch returns 503, the #378 case): the test runs the real installer once, requires exit 0 in every case, and then branches on the output: when the output carries the retry line from Item 1 (the PPA was unreachable at any step), `dpkg -s ghostty` must report the package absent and nothing half-installed; otherwise `dpkg -s ghostty` must succeed as today; the test prints which branch it took. (b) add two fake-based cases, "an unreachable PPA never fails the apply" (fakes for `add-apt-repository`/`apt-get` that return the PPA 503 as apt does; assert exit 0, the retry line, nothing installed) and "a failed PPA package download never fails the apply" (the pool fetch 503 after a successful update), modelled on `tests/install/ubuntu/client/zed.bats` lines 157-190; keep the PACKAGES and DEPENDENCY_PACKAGES tests. Red at origin/main on the behavioural assertion (the fake 503 case exits 100 today), green at the fix commit; record both shas. Never run Bats locally: red and green come from GitHub Actions runs of the branch, their URLs pasted.

## Check

Run `bash -n` and `shellcheck install/ubuntu/client/ghostty.sh`, `shfmt -d` as the repository's format target runs it; English shdoc comments. Caps: at most 80 changed lines outside `tests/` and `.orchestration/` and at most 120 under `tests/`, measured as additions plus deletions with `git diff --numstat <merge-base> <head>` over the whole PR (C-123).
Worker Playbook step 4: every command sandboxed; fresh branch `tools/install-ppa-resilience-a01` from origin/main; push without `-u`: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git tools/install-ppa-resilience-a01`; on any denial send `AGMSG-PONG v1 task_id=dotfiles-T133-install-ppa-resilience-a01 status=blocked` with the exact command and boundary.
Each evidence item names its producer. Keep this text at or under 110 lines including the Checks block below.

## Completion

Write `.orchestration/dotfiles-T133-install-ppa-resilience-a01/`: task.md byte-identical to the dispatched text, report.md, validation.md (every command, status and verbatim output; the two red/green pairs with run URLs), sandbox.md, learning.md, autoskill.md, result.txt (`task_copy=<sha256 of task.md>`, literal `head=<40-hex>`). Open the PR with an English title and description; after the push wait for required CI; at most one worker Bot fix-round. Then `AGMSG-RESULT v1 task_id=dotfiles-T133-install-ppa-resilience-a01 status=ready_for_review` with pr, head, merge_base, changed_non_tests, changed_tests, the red/green pairs, task_copy and the artifact paths.

## Amendments

1. The review (a011, round 1) found that the live `[ubuntu-client] ghostty` test still asserted `dpkg -s ghostty` succeeds, so a PPA outage would keep the required check red even after Item 1.
2. (2026-10-21T22:27Z) Round 2 found that a separate InRelease probe misjudges a pool-only outage (InRelease 200, .deb 503, the #378 case); Item 2(a) now uses the installer's own retry line as the oracle. Nothing else changes.

## Checks

```text
canonical main at authoring: 7da0cdfab9de9fbea673b82379acd4e317115065 (gh api repos/mryfmo/dotfiles/branches/main --hostname github.com --jq .commit.sha); PPA probe: curl -sS -o /dev/null -w '%{http_code}' https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu/dists/noble/InRelease -> 503 at 21:32Z and 200 at 21:37Z and 22:17Z (intermittent)
CI evidence: job 119482260780 (#442, b3ca1b80) and job 119512575084 (#378, 2b586637): "not ok 8 [ubuntu-client] ghostty" with "503 Service Unavailable" from ppa.launchpadcontent.net; zed.bats lines 157-190 are the pattern
observed 2026-10-21T22:22Z by the orchestrator (Claude seat, sandboxed Bash); every value is pasted command output
```
