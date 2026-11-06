# U299 the security-audit sweep of unit U298's head 58f5ffe8 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U298 head 58f5ffe87aa5dc49330499eaf9c4b0da09377cdd (branch `fix/session-start-hook-under-bridge` from origin/main 8f31cf5c; the unit's change is the DSH hook coverage test (tests/unit/test_dsh_hook_coverage.py) now models plugin activation: the kit's hooks are inactive under the deployed profile because the hooks plugin waits for the shell service; no production code, no production code) from the srt worker seat `sweep-3`, so unit U298, in the trust-boundary class by its brief's TRUST section, has its sweep row at the head that merges (the sweep bullet of the Audit section, `AGENTS.md:71`). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it. The coordinator copies the findings file into the store and writes the ledger row.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-8/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` (`SKILL.md`, `HUNTING.md`, `VALIDATION-AND-REPORTING.md`, `RECONNAISSANCE.md`, the attack-class files, `report-schema.json`, `validate-findings.cjs`, `validate-coverage-ledger.cjs`) by `scripts/update-agent-assets.sh#update_security_audit_skill` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), with audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep` and the bus store, and gives it no network; the skill's "Universal execution safety" asks exactly that for anything the target controls, and source inspection is read-only anyway. The previous run of this seat is run-7 (the U298 head); its records are the set to carry. The change under hunt against 8f31cf5c: `git diff --name-only c4195463 HEAD` (one file).

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-8`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 58f5ffe87aa5dc49330499eaf9c4b0da09377cdd and `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files it names as each phase needs them. Resolve the full-audit setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 58f5ffe8, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-7 records and re-verify each at this head with its lines re-mapped; hunt on the U298 change against 8f31cf5c (one test module). Every finding carries the fields `report-schema.json` requires: the trust boundary violated, the affected principal or resource, `file:line` evidence at this head, a safe reproduction or `needs_validation`, severity, and the smallest effective fix. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict (covered, or skipped with the reason).
4. Validate: read the usage line of each validator, then `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding to make it pass.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 58f5ffe87aa5dc49330499eaf9c4b0da09377cdd: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, then the counts by severity, the files written, and the wall time of the run.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-8` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 58f5ffe87aa5dc49330499eaf9c4b0da09377cdd <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-7 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write (a token is redacted to its first four characters); no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0 (the `hcom-worker` skill's Reply section: `hcom send --thread regime -- "<line>"`): `RESULT v1 task_id=U299 status=ready_for_review pr=none head=58f5ffe87aa5dc49330499eaf9c4b0da09377cdd note=<count> findings validated in run-8`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U235-security-audit-sweep-u234-head.md` (the previous sweep of this seat).
