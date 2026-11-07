# U372 the security-audit sweep of unit U20's head 66b65fd5 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U20 head 66b65fd507e56d2c0f401891ad4ad3d0c265f8c5 (branch `records/sync-48` from origin/main ff286680; the unit's change is records sync 48: 294 masked copies of the program store under .orchestration/orchestrate/regime-cutover (ledger, units, decisions, briefs, verdicts, sweeps, tests, handoff), no code from the srt worker seat `sweep-3`, so unit U20, in the trust-boundary class by its brief's TRUST section, has its sweep row at the head that merges (the sweep bullet of the Audit section, `AGENTS.md:71`). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it. The coordinator copies the findings file into the store and writes the ledger row.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-38/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-07 on this host. The skill is installed at `~/.agents/skills/security-audit/` (`SKILL.md`, `HUNTING.md`, `VALIDATION-AND-REPORTING.md`, `RECONNAISSANCE.md`, the attack-class files, `report-schema.json`, `validate-findings.cjs`, `validate-coverage-ledger.cjs`) by `scripts/update-agent-assets.sh#update_security_audit_skill` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), with audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep` and the bus store, and gives it no network; the skill's "Universal execution safety" asks exactly that for anything the target controls, and source inspection is read-only anyway. The previous run of this seat is no earlier run of this seat (carry the sweeps/U20-2256b56c records from the store instead) (the U20 head); its records are the set to carry. The change under hunt against ff286680: `git diff --name-only c4195463 HEAD` (one file).

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-38`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 66b65fd507e56d2c0f401891ad4ad3d0c265f8c5 and `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files it names as each phase needs them. Resolve the full-audit setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 66b65fd5, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the previous run of this seat (run-37) records and re-verify each at this head with its lines re-mapped; hunt on the U20 change against ff286680 (the records of the U301 to U369 units: the acp broker rows, the Router's credential root and router-gh rows, the srt build steps, the seat token and seat login rows; what the handouts instruct the operator to run; whether any record carries a credential, a home directory or a word of the store's redact-words.txt). Every finding carries the fields `report-schema.json` requires: the trust boundary violated, the affected principal or resource, `file:line` evidence at this head, a safe reproduction or `needs_validation`, severity, and the smallest effective fix. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict (covered, or skipped with the reason).
4. Validate: read the usage line of each validator, then `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding to make it pass.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 66b65fd507e56d2c0f401891ad4ad3d0c265f8c5: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, then the counts by severity, the files written, and the wall time of the run.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-38` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 66b65fd507e56d2c0f401891ad4ad3d0c265f8c5 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the previous run of this seat (run-37) records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write (a token is redacted to its first four characters); no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0 (the `hcom-worker` skill's Reply section: `hcom send --thread regime -- "<line>"`): `RESULT v1 task_id=U372 status=ready_for_review pr=none head=66b65fd507e56d2c0f401891ad4ad3d0c265f8c5 note=<count> findings validated in run-38`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U236-security-audit-sweep-u224-round5-head.md` (the previous sweep of the two-seat form).
