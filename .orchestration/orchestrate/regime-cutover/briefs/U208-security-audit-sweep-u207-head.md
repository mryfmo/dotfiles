# U208 the security-audit sweep of unit U207's head 2d0a93e4 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U207 head 2d0a93e4961463b7c65d3e7b9834a535fe04ffb3 (the two readers of a verdict's Findings section, audit-carry.py and pr-merge.sh, take the path as the first colon-free token, so a rationale may hold a location of its own) from the srt worker seat `sweep`, so unit U207, in the trust-boundary class by its brief's TRUST section, has its sweep row before its merge (the sweep bullet of the Audit section, `AGENTS.md:71`: every trust-boundary unit and every program milestone gets one sweep of the skill on a srt worker seat; its findings pass `validate-findings.cjs` and land as advisory `ledger.tsv` rows, never as a verdict). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it. The coordinator copies the findings file into the store and writes the advisory row. The run-42 records are the ones to carry and re-verify at this head with their lines re-mapped; the U207 change narrows the path group of the finding-line regex in `scripts/orchestrator/audit-carry.py` (`FINDING`) and `scripts/orchestrator/pr-merge.sh` (`finding_re`, with its generated copy and pin) from a greedy `(.+)` to the grammar's own character class, removes the now redundant second path check in both, and adds the shared fixture cases (a rationale holding `hcom-seat:1548:` reads as a finding; a first token with a colon or whitespace stays malformed): the merge gate's reading of verdict files is the trust-boundary change to read: whether any finding line can now be read as a different location than its writer meant (the disposition row names that location), and whether the two readers still agree on every fixture.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep/security-audit/run-43/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep`, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-05 on this host. The skill is installed at `~/.agents/skills/security-audit/` (`SKILL.md`, `HUNTING.md`, `VALIDATION-AND-REPORTING.md`, `RECONNAISSANCE.md`, the attack-class files, `report-schema.json`, `validate-findings.cjs`, `validate-coverage-ledger.cjs`) by `scripts/update-agent-assets.sh#update_security_audit_skill` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), with audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep` and the bus store, and gives it no network; the skill's "Universal execution safety" asks exactly that for anything the target controls, and source inspection is read-only anyway. The coordinator positioned the checkout at 2d0a93e4 before this TASK. The earlier runs sit beside the output directory as `run-1` to `run-42`; `run-42/findings.json` (the U188 round-3 head) holds eight records, all `needs_validation`, none confirmed, none of them about this lever. This head is U207, two lever changes with their shared test: the finding-line readers of `audit-carry.py` and `pr-merge.sh` read the path as the first colon-free token (the auditor's round-5 verdict of U190 repeats `hcom-seat:1548:` inside its rationale and was unreadable to both); read the two regexes and the removed path checks first, then the tests; nothing else changes.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep/security-audit/run-43`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep log -1 --format=%H` prints 2d0a93e4961463b7c65d3e7b9834a535fe04ffb3 and `git -C ~/.local/state/omp-seats/dotfiles/sweep status --porcelain` prints nothing; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files it names as each phase needs them. Resolve the full-audit setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep`, repo name `dotfiles`, output directory the one of step 1, source ref 2d0a93e4, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-42 records and re-verify each at this head with its lines re-mapped; hunt on the U207 change (`git -C ~/.local/state/omp-seats/dotfiles/sweep diff --name-only origin/main...HEAD` names six files): the regex change in both readers, the removed `PATH` and `path_re` checks, what a finding line could now be read as (a location the writer did not mean, a line number from the rationale), whether the disposition matching of `pr-merge.sh` still binds a row to the first location, and whether the two readers agree on every fixture of `tests/unit/test_pr_levers.py`. Every finding carries the fields `report-schema.json` requires: the trust boundary violated, the affected principal or resource, `file:line` evidence at this head, a safe reproduction or `needs_validation`, severity, and the smallest effective fix. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict (covered, or skipped with the reason).
4. Validate: read the usage line of each validator, then `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding to make it pass.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 2d0a93e4961463b7c65d3e7b9834a535fe04ffb3: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, then the counts by severity, the files written, and the wall time of the run.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep/security-audit/run-43` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 2d0a93e4961463b7c65d3e7b9834a535fe04ffb3 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-42 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write (a token is redacted to its first four characters); no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0 (the `hcom-worker` skill's Reply section: `hcom send --thread regime -- "<line>"`): `RESULT v1 task_id=U208 status=ready_for_review pr=none head=2d0a93e4961463b7c65d3e7b9834a535fe04ffb3 note=<count> findings validated in run-43`. Nothing else goes on the bus; the files are the report.

STANDING
`verdicts/U20-370b6f49.md` (the finding that named the unreadable verdict) and `verdicts/U190-6f66ffdc.md` (the file that must read); `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`.
