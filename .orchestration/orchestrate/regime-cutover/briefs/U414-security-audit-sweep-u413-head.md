# U414 the security-audit sweep of unit U413's head bd5106c0 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U413 head bd5106c06ea2343faa920c7a3a0600219e55b4e9 (branch `feat/pr-audit-daybreak-program-option` from origin/main 305d4f53b; the unit adds `--cyber-program <standard|daybreak_blue>` to `scripts/orchestrator/pr-audit.sh` and its copy under `home/dot_local/bin/common/` (a two-row case table; daybreak_blue puts `--cyber-access-program daybreak_blue -c model=gpt-6-sol` in the exec argv), two tests in `tests/unit/test_pr_audit.py`, one README sentence and the regenerated pin; 6 files, +132 -11) from the srt worker seat `sweep-3`, so unit U413, whose change lets the coordinator select the Daybreak Blue program for an audit turn, has its sweep row at the head that merges (the sweep bullet of the Audit section, `AGENTS.md:71`). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-60/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-55 (the U406 head da0b4e01); this unit has no earlier swept head. The change under hunt against 57e5345a1: `git diff --name-only 57e5345a1 HEAD` (6 paths). The hunt reads what the option admits: the option's value is read from argv and matched against two literal words (anything else refused before any call), the model override rides on argv while the scratch config keeps its pin, a daybreak_blue turn runs under reduced cyber safeguards inside the same read-only permission profile and sandbox probes; the probes carry neither argument.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-60`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints bd5106c06ea2343faa920c7a3a0600219e55b4e9 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref bd5106c0, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-59 records and re-verify each at this head with its lines re-mapped; hunt on the U413 change against 57e5345a1. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep bd5106c06ea2343faa920c7a3a0600219e55b4e9: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-60` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c bd5106c06ea2343faa920c7a3a0600219e55b4e9 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-53 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U414 status=ready_for_review pr=none head=bd5106c06ea2343faa920c7a3a0600219e55b4e9 note=<count> findings validated in run-60`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U412-security-audit-sweep-records-sync-54.md`.
