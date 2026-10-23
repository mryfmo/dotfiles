---
format: 2
task_id: dotfiles-T133-install-ppa-resilience-a02
kind: code
security: false
previous_sha256: a1c27be36e92bacc0724d9c008c9f3210af7132e07577bc83721bf2fe9127970
allowed_files:
  - install/ubuntu/client/ghostty.sh
  - install/ubuntu/client/misc.sh
  - home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl
  - home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl
  - tests/install/ubuntu/client/ghostty.bats
  - tests/install/ubuntu/client/misc.bats
  - .orchestration/dotfiles-T133-install-ppa-resilience-a02/**
after: []
threat_table:
  - {control: "install/ubuntu/client/ghostty.sh", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::an unreachable PPA never fails the apply"}
  - {control: "install/ubuntu/client/misc.sh", disposition: "closed: tests/install/ubuntu/client/misc.bats::install_misc refreshes the index before installing"}
  - {control: "home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it"}
  - {control: "home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl", disposition: "residual: it runs at every apply under the linux/debian/client guard; the installer it includes is idempotent (Item 1) and exits 0 on a PPA outage; the structural fixture and the required ubuntu-24.04 client job run it; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "tests/install/ubuntu/client/ghostty.bats", disposition: "residual: the fakes answer with exit codes and recorded argv only, never apt text; required CI runs the real module on ubuntu-24.04; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "tests/install/ubuntu/client/misc.bats", disposition: "residual: a fake sudo records its arguments; required CI runs the real module; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "the task-file copy (.orchestration/dotfiles-T133-install-ppa-resilience-a02/task.md)", disposition: "residual: byte-identical to the dispatched text; the orchestrator compares its SHA256 with the TASK line at acceptance; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "the evidence records under .orchestration/dotfiles-T133-install-ppa-resilience-a02/**", disposition: "residual: command output and learning triage; sandbox.md lists refused commands; the audit checks claims against the final head; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "APT_SOURCES_DIR (an environment input of ghostty.sh, default /etc/apt/sources.list.d)", disposition: "residual: a test seam; a caller who sets it changes only which source file its own PPA-only apt-get update reads; the live job pastes the default directory's listing; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "APT::Update::Error-Mode=any on the PPA-only refresh (Item 3)", disposition: "residual: a failing APT Post-Invoke hook on the machine makes the gate report the PPA index as not refreshed and skips Ghostty for that apply, with apt's own output printed before the retry line; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "a machine whose apt configuration sets APT::Update::Error-Mode any persistently", disposition: "residual: there every system-wide apt-get update, the one Item 5 adds to misc.sh included, fails during a PPA outage exactly as the existing refreshes do today, while the gate still skips Ghostty; changing a machine's apt policy is outside this task; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "task metadata (kind, security, allowed_files, after, threat_table, premises)", disposition: "residual: the consistency checker parses the mapping before dispatch and at acceptance; byte comparison of the task copy covers changes; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "metadata separators (the --- boundaries in the task copy and evidence records)", disposition: "residual: front matter stays YAML; the checker parses the task and byte comparison covers the whole dispatched file; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "in-process effects (apt-get and add-apt-repository run only through the existing sudo --preserve-env form)", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::an unreachable PPA never fails the apply"}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: no workflow, interpreter or dependency change; bash, apt-get and add-apt-repository as today; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "new or renamed scripts (home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl: new on this branch, which starts from main where it does not exist; a chezmoi run_after_ script guarded like run_after_05-client-install-zed.sh.tmpl that includes install/ubuntu/client/ghostty.sh)", disposition: "closed: tests/install/ubuntu/client/ghostty.bats::the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it"}
  - {control: "orchestrator effect merge", disposition: "residual: only the orchestrator merges the audited head with --match-head-commit after sweep, audit and gate; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "orchestrator effect update-branch", disposition: "residual: a moved head gets fresh CI, sweep, audit and gate before the merge; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: none planned; any discarded state is recorded at acceptance; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "orchestrator effect task copy", disposition: "residual: compared byte-for-byte and by SHA256 with the dispatched text at acceptance; owner: dotfiles-T133-install-ppa-resilience-a02"}
  - {control: "orchestrator effect records", disposition: "residual: the orchestrator owns acceptance and feedback dispositions; the worker supplies evidence only; owner: dotfiles-T133-install-ppa-resilience-a02"}
premises: []
---

# AGMSG-TASK dotfiles-T133-install-ppa-resilience-a02 — an unreachable Ghostty PPA never fails the apply (reset of a01: attribution by command scope)

Written 2026-10-22T06:58Z by the orchestrator seat as the INV-6 reset of `dotfiles-T133-install-ppa-resilience-a01` (PR #454: four RESULT heads, final audit of 460b91a5 incorrect, S2 revises 3 >= 2; D-024-83, D-024-84). The re-plan `.orchestration/plans/024-replan-install-ppa-20261022.md` (sha256 in the Checks block) is this text's source; its sections 3.2 and 4 bind it. Principle: a failure is attributed by the scope of the command that failed and by its exit code, never by apt's diagnostic text. A command that touches only the PPA failing means the PPA is unreachable; a command that touches only the local system failing is fatal as today. The user-visible promise of a01 stands: a PPA outage skips Ghostty with one retry line, exits 0, removes nothing, and the next apply retries; every other failure fails as today. Keep PACKAGES, DEPENDENCY_PACKAGES, the sudo `--preserve-env` form and English shdoc comments. Start from a fresh branch off origin/main and copy from the a01 branch only the fixtures Item 6 keeps.

## Item 1

In `install/ubuntu/client/ghostty.sh`: an `installed <package>` helper reads `dpkg-query -W -f '${db:Status-Status}'`; `installed ghostty` returns 0 at once with no apt call. The dependency phase (system-wide `apt-get update`, then `apt-get install -y "${DEPENDENCY_PACKAGES[@]}"`, both fatal as today) runs only when `installed software-properties-common` is false, so an existing machine reaches the gate without any refresh that includes the PPA. Selectors: `tests/install/ubuntu/client/ghostty.bats::the dependency phase runs only when software-properties-common is absent` (with the fake's `SPC=` empty the log shows update then install before the gate; with the default, no `apt-get update` without `-o Dir::Etc::sourcelist=` appears before the gate); `::an installed ghostty is left as it is` (zero apt calls) and `::a half-configured ghostty is installed, not skipped` are kept.

## Item 2

Locate the PPA's source file with `grep -lF "${GHOSTTY_PPA_URL}"` (`GHOSTTY_PPA_URL=ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/`, the URIs host and path of the PPA's stanza) over `${APT_SOURCES_DIR:-/etc/apt/sources.list.d}/*.sources` and `*.list`. When none exists, run `add-apt-repository -y -n "${GHOSTTY_PPA}"` (`-n`: no package-cache update); a non-zero exit prints the retry line and returns 0. A file still absent after a successful add prints one line and fails: a configuration fault, not an outage. Selectors: `::a failed PPA registration never fails the apply` (`FAIL=ppa-add`: the fake exits non-zero and writes no file; apt-get is called by the dependency phase only) and `::an existing PPA source is not re-added` (the fake source file pre-exists; the call log has no add-apt-repository).

## Item 3

The gate: `apt-get update -o Dir::Etc::sourcelist=<that file> -o Dir::Etc::sourceparts=- -o APT::Get::List-Cleanup=0 -o APT::Update::Error-Mode=any`, through the same sudo form. It reads that one source, so a non-zero exit means this PPA's index could not be refreshed, transient faults included: print the retry line and return 0. Selector: `::an unreachable PPA never fails the apply` (`FAIL=ppa-update`: the fake apt-get returns 100 only for an update whose argv carries `-o Dir::Etc::sourcelist=`; the test asserts exit 0, the retry line, the four `-o` options in that argv, and no update or install after it).

## Item 4

After the gate: the system-wide `apt-get update` as today (fatal); `apt-get install -y --download-only "${PACKAGES[@]}"` (non-zero: retry line, return 0); `apt-get install -y --no-download "${PACKAGES[@]}"` (non-zero: fatal). Selectors: `::a failed PPA package download never fails the apply` (`FAIL=download`: exit 0, retry line, no `--no-download` call), `::a failed local install stays fatal` (`FAIL=install`: `--no-download` returns 100; the script exits 100 without a retry line), `::a non-PPA apt failure still fails the apply` (`FAIL=archive` with `SPC=` empty: non-zero, no retry line). A resolver failure inside the download step is reported as `its package could not be downloaded` with exit 0, apt's output preceding the line (attribution by phase, re-plan J-2).

## Item 5

In `install/ubuntu/client/misc.sh` `install_misc`: one `sudo apt-get update` line before the install, the `install/ubuntu/client/tailscale.sh:40-41` form, so the script owns its own index refresh and the misc `run_once_` script, which chezmoi reruns on existing machines because this task's move (Item 6's structural test) changes its contents, no longer depends on a sibling's side effect. Selector: `tests/install/ubuntu/client/misc.bats::install_misc refreshes the index before installing` (a fake sudo records `$*`; line 1 is `apt-get update`, line 2 starts with `apt-get install -y`); at most 8 added lines in misc.bats.

## Item 6

The retry line is `ghostty not installed: <stage> (apt's output above); the next make update retries` with the stages `its PPA could not be registered`, `its PPA index could not be refreshed` and `its package could not be downloaded`; no locale forcing. The live `::ghostty` keeps a01's form (the real installer once, exit 0 in every case, the branch named in the output) and matches the prefix `ghostty not installed:` and the suffix `the next make update retries`; after the branch line it prints to file descriptor 3, the only output bats shows for a passing test, the installer's whole output, `ls /etc/apt/sources.list.d`, `apt-config dump | grep -i retries` and the status line of `dpkg -s ghostty`, so the job log carries the Completion's pastes; `::the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it` is kept. Delete `ppa_step`, a01's text-form fixtures (warn, mixed, otherppa, hook, summary, locale) and the tests `an apt-get update that reports a failed PPA index without a non-zero exit is an outage`, `a fetch failure from another host stays fatal even when the PPA also failed`, `a non-fetch apt error after a PPA warning stays fatal`, `apt's download-failure summary counts as a PPA outage` and `apt diagnostics are classified under a stable locale`. One fake set (`APT_FAKES` with `FAIL`, `SPC` and `STATUS`) serves every test; the fakes answer with exit codes and recorded argv only. Every `@test` name carries the `[ubuntu-client] ` prefix; the selectors in this text omit it.

## Check

Run `bash -n` and `shellcheck` on `install/ubuntu/client/ghostty.sh` and `install/ubuntu/client/misc.sh`, `shfmt -d` as the repository's format target runs it; English shdoc comments. Caps: at most 110 changed lines outside `tests/` and `.orchestration/` and at most 160 under `tests/`, measured as additions plus deletions with `git diff --numstat <merge-base> <head>` over the whole PR (C-123). Red/green: the behaviour-changing selectors (the seven new tests of Items 1-5 and the structural test) red at origin/main's installer bytes and green at the fix commit; the guards (`a half-configured ghostty is installed, not skipped`, `a non-PPA apt failure still fails the apply`, the live `ghostty`) green at both; `an installed ghostty is left as it is` records its observed state at main and green at the fix; each as a GitHub Actions `test (ubuntu-24.04, client)` run URL. Commits carry the identity git resolves from the seat's configuration (`git var GIT_AUTHOR_IDENT`), never a `-c user.name` override or a fixture identity.
Worker Playbook step 4: every command sandboxed; fresh branch `tools/install-ppa-resilience-a02` from origin/main; push without `-u`: `GIT_CONFIG_GLOBAL=/dev/null git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push https://github.com/mryfmo/dotfiles.git tools/install-ppa-resilience-a02`; on any denial send `AGMSG-PONG v1 task_id=dotfiles-T133-install-ppa-resilience-a02 status=blocked` with the exact command and boundary. Do not run bats locally (AGENTS.md Test Policy); CI runs them.
Each evidence item names its producer. Keep this text at or under 110 lines including the Checks block below.

## Completion

Write `.orchestration/dotfiles-T133-install-ppa-resilience-a02/` and commit it in the PR: task.md byte-identical to the dispatched text, report.md, validation.md (every command, status and verbatim output; the red/green pair of every selector with run URLs; from the live `test (ubuntu-24.04, client)` job's fd 3 lines (Item 6): `ls /etc/apt/sources.list.d`, the gate's apt output with no host other than the PPA's in its `Hit:`/`Get:`/`Err:` lines, `apt-config dump | grep -i retries`, the branch line and `dpkg -s ghostty`), sandbox.md, learning.md, autoskill.md, result.txt (`task_copy=<sha256 of task.md>`, literal `head=<40-hex>`). Open the PR with an English title and description; after the push wait for required CI; at most one worker Bot fix-round. Then `AGMSG-RESULT v1 task_id=dotfiles-T133-install-ppa-resilience-a02 status=ready_for_review` with pr, head, merge_base, changed_non_tests, changed_tests, the red/green pairs, task_copy and the artifact paths.

## Amendments

1. (2026-10-22T07:15Z, `previous_sha256` above) Anchor round 1 (a011) F1-F4 and four P3: the Check's red/green rule now distinguishes behaviour-changing selectors from guards (F1); Item 6 makes the live test print the Completion's evidence to fd 3 (F2); the new-scripts row names run_after_06 as new on this branch and closes it with the structural selector (F3); a residual row for a machine that sets Error-Mode any persistently is added (F4); Item 2 states `GHOSTTY_PPA_URL`, Item 4 names the download-step resolver case, Item 5's wording and the selector-prefix note are corrected (P3).

## Checks

```text
observed 2026-10-22T06:56:37Z by the orchestrator (Claude seat, sandboxed Bash); every value is pasted command output
canonical main at authoring: d06d94fd8eedcd0770c1c80c2b1596ec36109ef8 (gh api repos/mryfmo/dotfiles/branches/main --jq .commit.sha)
PPA probe: curl -sS -o /dev/null -w %{http_code} https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu/dists/noble/InRelease -> 200
re-plan: shasum -a 256 .orchestration/plans/024-replan-install-ppa-20261022.md -> e44cf7c14e1db93a744ae177ffa744eee8b62815ea8d4fe90464a4aa952e5328
a01 final audit: tail -n 1 .orchestration/validation/dotfiles-T133-install-ppa-resilience-a01-audit-460b91a.md.last.md -> Verdict: incorrect
a01 counters: scripts/regime-counters.sh dotfiles-T133-install-ppa-resilience-a01 | sed -n 2p -> S2: revises 3 >= 2 source=live
PR 454: gh pr view 454 --json state,headRefOid --jq "\(.state) \(.headRefOid)" -> OPEN 460b91a5de63719e1cf45447442e506bafca676e
```
