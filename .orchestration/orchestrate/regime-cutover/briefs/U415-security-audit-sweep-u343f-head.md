# U415 the security-audit sweep of unit U343f's head 22a81500 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U343f head 22a81500935360b3a0df4918a2604cd7af998de3 (branch `feat/acp-broker-lever`, PR 720, round 4 of U343 on the round-3 head fd94feae; the unit makes `push_back` in `scripts/orchestrator/acp-broker` read the worker's clone inside the worker's own srt settings (`worker_git`, mirroring `router_git`), adds `exit_line` that never refuses, keeps the traps armed through the push and the exit line, escalates the group signal TERM then KILL, and in `scripts/orchestrator/acp-seat` takes only a newline-terminated last line as the trailer and anchors `NAME` and `REF` with `\Z`; the copies under `home/dot_local/bin/common/`, `tests/unit/test_acp_broker.py`, one README sentence and the regenerated pins; 8 files, +449 -98) from the srt worker seat `sweep-3`, so unit U343f has its sweep row at the head that merges (the sweep bullet of AGENTS.md:70-71: every trust-boundary unit gets one sweep before its pull request merges). The findings are advisory rows of the program ledger, never a verdict.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-61/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-60 (the U413 head bd5106c0); the earlier swept head of this unit's pull request is fd94feae (run-35, sweeps/U362-fd94feae). The change under hunt against fd94feae: `git diff --name-only fd94feae HEAD` (8 paths). The hunt reads the two git boundaries: every git on the Router's repository runs inside the Router's settings (`router_git`), every git on the worker's clone after omp starts runs inside the worker's settings (`worker_git`), the clone before omp starts runs outside (`slot_git`) when the worker has written nothing; the pack crosses on descriptors the broker opened in the slot; the trap window; the exit line; the client's trailer rule. Read `verdicts/U343e-fd94feae.md` for the round-3 findings the unit answers.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-61`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 22a81500935360b3a0df4918a2604cd7af998de3 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 22a81500, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-60 records and re-verify each at this head with its lines re-mapped; hunt on the U343f change against fd94feae. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 22a81500935360b3a0df4918a2604cd7af998de3: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-61` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 22a81500935360b3a0df4918a2604cd7af998de3 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-60 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread `regime` (the TASK arrives on that thread; reply on it with `hcom send --thread regime`) when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U415 status=ready_for_review pr=none head=22a81500935360b3a0df4918a2604cd7af998de3 note=<count> findings validated in run-61`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U414-security-audit-sweep-u413-head.md`.
