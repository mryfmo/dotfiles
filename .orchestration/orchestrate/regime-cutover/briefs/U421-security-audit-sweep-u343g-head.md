# U421 the security-audit sweep of unit U343g's head 8a049561 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U343f head 8a0495616f792081240439165ea041609c7a385a (branch `feat/acp-broker-lever`, PR 720, round 5 of U343 on the round-4 head 22a81500, a mechanism change of form remove: the broker's exit report is a record file the connection's reaper alone writes under the Router's socket directory `<seats-root>/.state/<router seat>/broker/<id>`, the stream carries one broker line (`acp-broker: record <id>`) then the worker's bytes unread, `acp-seat` reads the record after the socket closes, and `connection_signal`, every connection trap and the trailer are deleted; `broker_cleanup` removes leftover records; 8 files, +1035 -427) from the srt worker seat `sweep-3`, so unit U343g has its sweep row at the head that merges (the sweep bullet of AGENTS.md:70-71: every trust-boundary unit gets one sweep before its pull request merges). The findings are advisory rows of the program ledger, never a verdict.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-64/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-63 (the U413 head bd5106c0); the earlier swept head of this unit's pull request is 22a81500 (run-61, sweeps/U415-22a81500). The change under hunt against 22a81500: `git diff --name-only 22a81500 HEAD` (8 paths). The hunt reads the record's boundary (the socket directory the Router's settings grant and no worker setting reaches; the record written by `printf` to a temporary then `mv -f`; what a worker can put on the stream and why none of it is read as a report), the reaper (forked before omp outside its group, signals ignored, the FIFO control pipe closed for every child by `4>&-`, TERM then KILL to the group, `slot_remove`), and the client's first-line parse (`RECORD_ID`, `STATUS_LINE`, the 4096-byte first-line limit). Read `verdicts/U343f-22a81500.md` for the round-4 findings the unit answers and `handoff/research/U343g-design.md` for the design.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-64`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 8a0495616f792081240439165ea041609c7a385a and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 8a049561, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-63 records and re-verify each at this head with its lines re-mapped; hunt on the U343g change against 22a81500. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 8a0495616f792081240439165ea041609c7a385a: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-64` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 8a0495616f792081240439165ea041609c7a385a <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-63 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread `regime` (the TASK arrives on that thread; reply on it with `hcom send --thread regime`) when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U421 status=ready_for_review pr=none head=8a0495616f792081240439165ea041609c7a385a note=<count> findings validated in run-64`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U419-security-audit-sweep-u416-head.md`.
