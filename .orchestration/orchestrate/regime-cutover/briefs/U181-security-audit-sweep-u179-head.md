# U181 the security-audit sweep of unit U179's head 90fd01fc on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U179 head 90fd01fc217e6ed9b42a46025320168e53da89b4 (PR 655) from the srt worker seat `sweep`, so unit U179, in the trust-boundary class by its brief's TRUST section, has its sweep row before its merge (the sweep bullet of the Audit section, `AGENTS.md:71`: every trust-boundary unit and every program milestone gets one sweep of the skill on a srt worker seat; its findings pass `validate-findings.cjs` and land as advisory `ledger.tsv` rows, never as a verdict). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it. The coordinator copies the findings file into the store and writes the advisory row. The run-22 records (the U172 round-3 sweep, `sweeps/U172-0c9e7a14/findings.json`) are the ones to carry and re-verify at this head; the U179 change is one new test file under `tests/unit/` (named by `git -C ~/.local/state/omp-seats/dotfiles/sweep diff --name-only origin/main...HEAD`), which reads three repository files and executes nothing, so the hunt at this head is over that file and whatever its reads touch.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep/security-audit/run-23/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep`, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-05 on this host. The skill is installed at `~/.agents/skills/security-audit/` (`SKILL.md`, `HUNTING.md`, `VALIDATION-AND-REPORTING.md`, `RECONNAISSANCE.md`, the attack-class files, `report-schema.json`, `validate-findings.cjs`, `validate-coverage-ledger.cjs`) by `scripts/update-agent-assets.sh#update_security_audit_skill` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), with audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep` and the bus store, and gives it no network; the skill's "Universal execution safety" asks exactly that for anything the target controls, and source inspection is read-only anyway. The coordinator positioned the checkout at 90fd01fc before this TASK. The earlier runs sit beside the output directory as `run-1` to `run-22`; `run-22/findings.json` holds seven records, all `needs_validation`, none confirmed (two U172 leads, five from run-1).

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep/security-audit/run-23`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep log -1 --format=%H` prints 90fd01fc217e6ed9b42a46025320168e53da89b4 and `git -C ~/.local/state/omp-seats/dotfiles/sweep status --porcelain` prints nothing; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files it names as each phase needs them. Resolve the full-audit setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep`, repo name `dotfiles`, output directory the one of step 1, source ref 90fd01fc, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-22 records and re-verify each at this head with its lines re-mapped; hunt on the U179 change (the one added file under `tests/unit/`, its reads of `home/.chezmoitemplates/claude-settings-managed.json`, `home/dot_claude/modify_private_settings.json` and `home/dot_dsh/profiles/thak/cordis.patch.yml`). Every finding carries the fields `report-schema.json` requires: the trust boundary violated, the affected principal or resource, `file:line` evidence at this head, a safe reproduction or `needs_validation`, severity, and the smallest effective fix. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict (covered, or skipped with the reason).
4. Validate: read the usage line of each validator, then `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding to make it pass.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 90fd01fc217e6ed9b42a46025320168e53da89b4: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, then the counts by severity, the files written, and the wall time of the run.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep/security-audit/run-23` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 90fd01fc217e6ed9b42a46025320168e53da89b4 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write (a token is redacted to its first four characters); no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0 (the `hcom-worker` skill's Reply section: `hcom send --thread regime -- "<line>"`): `RESULT v1 task_id=U181 status=ready_for_review pr=none head=90fd01fc217e6ed9b42a46025320168e53da89b4 note=<count> findings validated in run-23`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`.
