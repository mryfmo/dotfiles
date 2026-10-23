---
format: 2
task_id: dotfiles-T133-install-ppa-resilience-a02-review-a01
kind: review
security: false
allowed_files:
  - .orchestration/dotfiles-T133-install-ppa-resilience-a02-review-a01/**
after: []
---

# AGMSG-TASK dotfiles-T133-install-ppa-resilience-a02-review-a01 — independent review of the install-ppa-resilience a02 text

Drafted 2026-10-22T07:04Z by the orchestrator seat. The a01 lineage (PR #454) stopped under INV-6 S2 after four RESULT rounds whose findings were symptoms of one design choice, classifying apt's diagnostic text; a separate context wrote the re-plan `.orchestration/plans/024-replan-install-ppa-20261022.md` (sha256 e44cf7c14e1db93a744ae177ffa744eee8b62815ea8d4fe90464a4aa952e5328), and the orchestrator authored the a02 text from it (D-024-83, D-024-84). Security: false, no C-80. You judge the text, not the re-plan; the re-plan is context.

## What to review

Amendment 1 (2026-10-22T07:15Z): your round-1 findings are answered: the Check's red/green rule distinguishes the behaviour-changing selectors (red at main) from the guards (green at both) (F1); Item 6 makes the live test print the installer's output, `ls /etc/apt/sources.list.d`, `apt-config dump | grep -i retries` and the `dpkg -s ghostty` status line to fd 3 so the job log carries the Completion's pastes (F2); the new-scripts row names run_after_06 as new on this branch and closes it with the structural selector (F3); a residual row for a machine that sets Error-Mode any persistently is added (F4); the four P3 are taken (GHOSTTY_PPA_URL value, the download-step resolver case, Item 5's wording, the selector-prefix note). Judge the new bytes under the same five items; the hash below is the new one.

1. `.orchestration/tasks/dotfiles-T133-install-ppa-resilience-a02.md` at sha256 `07aa7808bac382c736800927755e2455d2c4ab4144b0464527cea8f9092a17c4` is the file you judge (93 lines); compute the hash yourself and stop with `verdict=reject` if it differs.
2. Design fidelity: Items 1-6 implement the re-plan's section 3.2 (attribution by command scope and exit code; no diagnostic-text classification anywhere, including the tests) and section 4 (I-1 to I-7); every selector the Items name is a bats test name in the two named files; the deleted tests and fixtures are named; the retry line has the three stages and nothing else is parsed from apt. Report any sentence that would need apt's output text to be read.
3. Official grounding and verifiability: each apt option and chezmoi behaviour the text relies on (`-n`, `Dir::Etc::sourcelist`, `Dir::Etc::sourceparts=-`, `APT::Get::List-Cleanup=0`, `APT::Update::Error-Mode=any`, `--download-only`, `--no-download`, `db:Status-Status`, `run_after_` and `run_once_` ordering) is named exactly; the Completion's live-job pastes make the two unverified facts (the PPA source file name, `Dir::Etc::sourceparts`/`Acquire::Retries` on noble) observable; the caps sentence is the a01 sentence the regime verifier parses; red/green is required per selector.
4. Threat table and metadata: one row per allowed_files entry, per non-path control (APT_SOURCES_DIR seam, Error-Mode residual, in-process effects, workflow inputs, metadata, separators, new scripts) and per orchestrator effect; a closed row's selector exists in the Items; a residual row's control mitigates its risk and names an owner that exists (the task itself); the Checks block is pasted command output only.
5. Read only; no file changed, nothing dispatched.

## Output

`.orchestration/dotfiles-T133-install-ppa-resilience-a02-review-a01/review.md` with the hash, one line per item and the verdict, then exactly one RESULT: `AGMSG-RESULT v1 task_id=dotfiles-T133-install-ppa-resilience-a02-review-a01 status=ready_for_review verdict=accept design_file=.orchestration/tasks/dotfiles-T133-install-ppa-resilience-a02.md design_sha256=07aa7808bac382c736800927755e2455d2c4ab4144b0464527cea8f9092a17c4 review=.orchestration/dotfiles-T133-install-ppa-resilience-a02-review-a01/review.md`, or the same with `verdict=reject` and the findings in the file.
