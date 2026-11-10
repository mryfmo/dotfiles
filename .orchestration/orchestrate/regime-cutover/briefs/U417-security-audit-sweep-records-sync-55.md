# U417 the security-audit sweep of unit the records sync 55 head 8ff06747 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U20 head 8ff06747d2252459bb9986686c4d4b360e21e228 (branch `records/sync-55`, PR 750, the first records sync from the derived store: 188 files under `.orchestration/orchestrate/regime-cutover/`, today's units U413 to U416, their briefs, verdicts, sweeps, the handoff note and the i2 table row; no file outside the store changes) from the srt worker seat `sweep-3`, so the records unit U20 has its sweep row at the head that merges (the sweep bullet of AGENTS.md:70-71: every trust-boundary unit gets one sweep before its pull request merges). The findings are advisory rows of the program ledger, never a verdict.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-62/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-61 (the U20 head 8ff06747). The change under hunt against origin/main f66c4d78: `git diff --name-only f66c4d78 HEAD` (188 paths, all records under the store). The hunt reads the records as published text: no secret, no home path, no redact word, no credential in any copied file; the records-sync lever masks and scans before publishing, and the sweep is the second reader.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-62`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 8ff06747d2252459bb9986686c4d4b360e21e228 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 8ff06747, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-61 records and re-verify each at this head with its lines re-mapped; hunt on the records change against f66c4d78. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 8ff06747d2252459bb9986686c4d4b360e21e228: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-62` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 8ff06747d2252459bb9986686c4d4b360e21e228 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-61 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread `regime` (the TASK arrives on that thread; reply on it with `hcom send --thread regime`) when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U417 status=ready_for_review pr=none head=8ff06747d2252459bb9986686c4d4b360e21e228 note=<count> findings validated in run-62`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U415-security-audit-sweep-u343f-head.md`.
