---
format: 2
task_id: dotfiles-T133-install-ppa-resilience-a01-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T133-install-ppa-resilience-a01-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T133-install-ppa-resilience-a01-review-a01 — independent review of the install-ppa-resilience text

Drafted 2026-10-21T22:23Z by the orchestrator seat. The required check `test (ubuntu-24.04, client)` failed twice today on `tests/install/ubuntu/client/ghostty.bats` line 38 because the Launchpad PPA returned 503; the orchestrator authored a task that makes the ghostty installer tolerate an unreachable PPA the way the zed installer tolerates an unreachable release API (D-024-67). Security: false, no C-80.

## What to review

Amendment 2 (2026-10-21T22:27Z): your round-2 finding is answered: the live test no longer probes InRelease; it runs the installer once, requires exit 0, and branches on the installer's own retry line (absent -> installed; present -> nothing installed), so a pool-only outage is judged correctly. Judge the new bytes under the same three items; the hash below is the new one.

Amendment 1 (2026-10-21T22:25Z): your round-1 finding is answered: Item 2 now rewrites the live `[ubuntu-client] ghostty` test to branch on a live probe of the PPA (installed when 200, exit 0 plus the retry line and nothing installed otherwise) and keeps the two fake-based cases; the in-process row's selector follows. Judge the new bytes under the same three items; the hash below is the new one.

1. `.orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md` at sha256 `45fb80f66c9ca36ef5dc3595d516404b64b6060fab4bd2a2c3b7e3174a83488f` is the file you judge (57 lines); compute the hash yourself and stop with `verdict=reject` if it differs.
2. The scope is exactly the installer's PPA-failure path and two bats cases (nothing widens: same packages, same sudo form, no new dependency); the behaviour mirrors `tests/install/ubuntu/client/zed.bats` lines 157-190 ("never fails the apply"); the threat table has a row per allowed path and per orchestrator effect; residual rows name an owner that exists (the task itself, as the lineage's first text); the Checks block cites the two CI jobs and the PPA probes you can re-run (`curl -sS -o /dev/null -w '%{http_code}' https://ppa.launchpadcontent.net/mkasberg/ghostty-ubuntu/ubuntu/dists/noble/InRelease`); the caps (80/120) fit the change.
3. Read only; no file changed, nothing dispatched.

## Output

`.orchestration/dotfiles-T133-install-ppa-resilience-a01-review-a01/review.md` with the hash, one line per item and the verdict, then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T133-install-ppa-resilience-a01-review-a01 status=ready_for_review verdict=accept design_file=.orchestration/tasks/dotfiles-T133-install-ppa-resilience-a01.md design_sha256=45fb80f66c9ca36ef5dc3595d516404b64b6060fab4bd2a2c3b7e3174a83488f review=.orchestration/dotfiles-T133-install-ppa-resilience-a01-review-a01/review.md`, or the same with `verdict=reject` and the findings in the file.
