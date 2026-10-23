---
format: 2
task_id: dotfiles-T133-install-ppa-resilience-a01
kind: code
security: false
previous_sha256: 9be19bd658e27bc2e559e224cb110772f07884689af8bc5be9a1b9ff278017ad
allowed_files:
  - install/ubuntu/client/ghostty.sh
  - home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl
  - home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl
  - tests/install/ubuntu/client/ghostty.bats
  - .orchestration/dotfiles-T133-install-ppa-resilience-a01/**
after: []
threat_table:
  - {control: "install/ubuntu/client/ghostty.sh", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::an unreachable PPA never fails the apply"}
  - {control: "tests/install/ubuntu/client/ghostty.bats", disposition: "residual: the fixtures replace add-apt-repository and apt-get with fakes that return the PPA's 503; required CI runs the real module on ubuntu-24.04; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "the task-file copy (.orchestration/dotfiles-T133-install-ppa-resilience-a01/task.md)", disposition: "residual: byte-identical to the dispatched text; the orchestrator compares its SHA256 with the TASK line at acceptance; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "the evidence records under .orchestration/dotfiles-T133-install-ppa-resilience-a01/**", disposition: "residual: command output and learning triage; sandbox.md lists refused commands; the audit checks claims against the final head; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "the executed smoke script (.orchestration/dotfiles-T133-install-ppa-resilience-a01/smoke.sh, run by the worker's validation on the fakes only)", disposition: "residual: it runs the installer against the fake apt and add-apt-repository under a temporary HOME and PATH and never the live apt; validation.md pastes its command and output; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "task metadata (kind, security, allowed_files, after, threat_table, premises)", disposition: "residual: the consistency checker parses the mapping before dispatch and at acceptance; byte comparison of the task copy covers changes; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "metadata separators (the --- boundaries in the task copy and evidence records)", disposition: "residual: front matter stays YAML; the checker parses the task and byte comparison covers the whole dispatched file; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "in-process effects (the install script runs apt only through its existing sudo --preserve-env form)", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::an unreachable PPA never fails the apply (fakes), with the live ghostty test tolerant of the probe result"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: no workflow, interpreter or dependency change; the script keeps bash and apt as today; owner: dotfiles-T133-install-ppa-resilience-a01"}
  - {control: "new or renamed scripts (home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl, a chezmoi run_after_ script, guarded like run_after_05-client-install-zed.sh.tmpl, that includes install/ubuntu/client/ghostty.sh)", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it"}
  - {control: "home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it"}
  - {control: "home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl", disposition: "residual: a run_after_ script runs at every chezmoi apply under the linux/debian/client guard, so the installer it includes is idempotent (dpkg -s first) and exits 0 on a PPA outage; the structural fixture above and the required ubuntu-24.04 client job run it; owner: dotfiles-T133-install-ppa-resilience-a01"}
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

Run `bash -n` and `shellcheck install/ubuntu/client/ghostty.sh`, `shfmt -d` as the repository's format target runs it; English shdoc comments. Caps: at most 110 changed lines outside `tests/` and `.orchestration/` and at most 160 under `tests/`, measured as additions plus deletions with `git diff --numstat <merge-base> <head>` over the whole PR (C-123).
Worker Playbook step 4: every command sandboxed; fresh branch `tools/install-ppa-resilience-a01` from origin/main; push without `-u`: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git tools/install-ppa-resilience-a01`; on any denial send `AGMSG-PONG v1 task_id=dotfiles-T133-install-ppa-resilience-a01 status=blocked` with the exact command and boundary.
Each evidence item names its producer. Keep this text at or under 110 lines including the Checks block below.

## Completion

Write `.orchestration/dotfiles-T133-install-ppa-resilience-a01/`: task.md byte-identical to the dispatched text, report.md, validation.md (every command, status and verbatim output; the two red/green pairs with run URLs), sandbox.md, learning.md, autoskill.md, result.txt (`task_copy=<sha256 of task.md>`, literal `head=<40-hex>`). Open the PR with an English title and description; after the push wait for required CI; at most one worker Bot fix-round. Then `AGMSG-RESULT v1 task_id=dotfiles-T133-install-ppa-resilience-a01 status=ready_for_review` with pr, head, merge_base, changed_non_tests, changed_tests, the red/green pairs, task_copy and the artifact paths.

## Amendments

1. The review (a011, round 1) found that the live `[ubuntu-client] ghostty` test still asserted `dpkg -s ghostty` succeeds, so a PPA outage would keep the required check red even after Item 1.
2. (2026-10-21T22:27Z) Round 2 found that a separate InRelease probe misjudges a pool-only outage (InRelease 200, .deb 503, the #378 case); Item 2(a) now uses the installer's own retry line as the oracle. Nothing else changes.

3. (2026-10-22T02:3xZ, `previous_sha256` above) The task-level audit of 44134e36 found that (a) `apt-get update` can exit 0 while reporting a failed PPA index, so the skip path is missed and a fresh machine fails with "Unable to locate package"; (b) any Launchpad fetch line turned a mixed failure into success; (c) a skipped install is never retried because the caller `run_once_50-client-install-misc.sh.tmpl` records completion (chezmoi: a run_once_ script runs once per content). Item 3: move the ghostty step into its own `home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl` (a `run_after_` script like `run_after_05-client-install-zed.sh.tmpl`, so it runs at every apply) that carries the same template guard as the misc and zed templates (`.chezmoi.os` linux, `.chezmoi.osRelease.idLike` debian, `.system` client) and only `include`s `install/ubuntu/client/ghostty.sh`; remove the include from the misc script; make the installer idempotent (return 0 early when `dpkg -s ghostty` succeeds). Item 1 tightens the outage detector: after `apt-get update`, the PPA counts as unreachable only when every `Failed to fetch` or `W: Failed to fetch` line names the PPA host (a fetch failure from any other host stays fatal, exit kept), and an exit-0 update whose output reports a failed PPA index is an outage too. Item 2 adds one red-then-green fixture per rule: `an apt-get update that reports a failed PPA index without a non-zero exit is an outage`, `a fetch failure from another host stays fatal even when the PPA also failed`, `the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it`. validation.md pastes each command with its verbatim output (JSON stays JSON, no prose in place of a command, the lint red run included). The caps sentence of `## Check` now reads 110 outside tests and 160 under tests (regime-ci.py reads that section).

4. (2026-10-22T04:0xZ, `previous_sha256` above) The audit of e6b645fc found three defects in amendment 3's implementation and one in its wording. (a) `ppa_step` must decide the outage from the whole failure, not from the fetch lines alone: the step is an outage only when every error line of apt's output is a PPA fetch failure (`Failed to fetch` or `W: Failed to fetch` naming the PPA host) and no other `E:` or error line is present; a PPA warning plus any other apt error (a post-update hook, a dpkg error, another host) stays fatal with the original exit kept. (b) The idempotence check is the dpkg database status, not `dpkg -s`'s exit: skip only when `dpkg-query -W -f '${db:Status-Status}' ghostty` prints `installed`; a half-configured or unpacked state runs the install (dpkg-query(1): Status-Status). (c) validation.md pastes only commands that were executed, with their output; a placeholder expression or prose in place of a command is a refusal of the RESULT. Item 2 adds one red-then-green fixture each: `a non-fetch apt error after a PPA warning stays fatal`, `a half-configured ghostty is installed, not skipped`.

5. (2026-10-22T05:0xZ, `previous_sha256` above; the one P0/P1 fix round of Worker Playbook step 15, after the local review of 059a40cf) (a) apt reports a download failure twice: per-URL `Failed to fetch` lines and a summary (`E: Failed to fetch …`, `E: Unable to fetch some archives, …`, `W: Some index files failed to download. They have been ignored, …`); Item 1 classifies both forms: the step is an outage only when every failing URL, in the per-URL lines and in the summary, names the PPA host and no other `E:` line is present. (b) The classification runs apt under `LC_ALL=C LANG=C` (set on the apt commands the step runs), so the diagnostics are the English forms above on every locale. (c) The executed smoke script has its threat row above. Item 2 adds one red-then-green fixture each: `apt's download-failure summary counts as a PPA outage`, `apt diagnostics are classified under a stable locale`.

## Checks

```text
canonical main at authoring: 7da0cdfab9de9fbea673b82379acd4e317115065 (gh api repos/mryfmo/dotfiles/branches/main --hostname github.com --jq .commit.sha); PPA probe: curl -sS -o /dev/null -w '%{http_code}' https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu/dists/noble/InRelease -> 503 at 21:32Z and 200 at 21:37Z and 22:17Z (intermittent)
CI evidence: job 119482260780 (#442, b3ca1b80) and job 119512575084 (#378, 2b586637): "not ok 8 [ubuntu-client] ghostty" with "503 Service Unavailable" from ppa.launchpadcontent.net; zed.bats lines 157-190 are the pattern
observed 2026-10-21T22:22Z by the orchestrator (Claude seat, sandboxed Bash); every value is pasted command output
```
