# U296 the security-audit sweep of unit U227b's head d1ffd919 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U227b head d1ffd91939e4d069b01d0e4d467c12eff971a944 (branch `feat/hcom-seat-dsh-role` from origin/main d1ecd495; the unit's change makes the kit's DSH profile renderer emit the dsh-omp-gateway insert row and the agent-default-model row for provider claude-bridge, the link: dependency in the profile package.json, removes the Ollama provider rows and the API-key route, changes the manifest's dsh model rows, and adds the updater step that links the plugin into the profile; 9 files, 425 insertions, 102 deletions; round 3 (U227c) resolves the link step's paths physically, refuses an external plugin target and relinks atomically; round 4 (U272e) merges main, the U226 build input and the U224 removal, with three conflict files resolved) from the srt worker seat `sweep-2`, so unit U227b, a lever change, has its sweep row at the head that merges (`AGENTS.md:71`). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it. The coordinator copies the findings file into the store and writes the ledger row.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-8/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-2`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep` and the bus store, and gives it no network. The previous run of this seat is run-6 (the U227b head); its records are the set to carry. The change under hunt against d1ecd495: `git diff --name-only c4195463 HEAD` (29 paths). The hunt reads the rendered rows as configuration an attacker who writes the profile could abuse (command, args, env, cwd), the updater's symlink step (target, refusals, idempotence, what a pre-existing path at the link name does), and that no key or Ollama row survives.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-8`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 log -1 --format=%H` prints d1ffd91939e4d069b01d0e4d467c12eff971a944 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-2`, repo name `dotfiles`, output directory the one of step 1, source ref d1ffd919, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-6 records and re-verify each at this head with its lines re-mapped; hunt on the U227b change against d1ecd495. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep d1ffd91939e4d069b01d0e4d467c12eff971a944: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-8` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c d1ffd91939e4d069b01d0e4d467c12eff971a944 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-6 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U296 status=ready_for_review pr=none head=d1ffd91939e4d069b01d0e4d467c12eff971a944 note=<count> findings validated in run-8`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U229-security-audit-sweep-u226-head.md`.
