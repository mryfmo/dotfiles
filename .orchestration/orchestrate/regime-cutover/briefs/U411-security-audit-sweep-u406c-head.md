# U411 the security-audit sweep of unit U406's head 1c9dceec on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U406 head 1c9dceec3b4e01cef06f6e61391b72ae17279c1a (branch `fix/router-profile-bash-sandbox-on` from origin/main 57e5345a1 with main 49891b8f (U404) merged in at round 3 (U406c), the one comment-block conflict resolved; the unit removes from `scripts/generate-agent-configs.py`'s router renderer the three `bash-sandbox disabled: true` rows and the two restated agent presets with their helpers, adds three router tests in `tests/unit/test_dsh_profile.py`, and regenerates `home/dot_dsh/profiles/router/cordis.patch.yml`; 3 files +53 -436 in round 1 and, in round 2 (U406b, head 1c9dceec), the comment and two docstrings corrected: srt is the one boundary, bash-sandbox the presets' shell provider in pass-through mode; the rendered patch unchanged) from the srt worker seat `sweep-3`, so unit U406, whose change lets dsh's bash-sandbox run inside the Router's srt seat as the shell provider upstream's presets require, in its pass-through mode under those presets, so the permission presets and the superagent activate inside srt, the one boundary, has its sweep row at the head that merges (the sweep bullet of the Audit section, `AGENTS.md:71`). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-58/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-57 (the U406b head c19788fe); this unit has no earlier swept head. The change under hunt against 57e5345a1: `git diff --name-only 57e5345a1 HEAD` (3 paths). The hunt reads what turning the harness sandbox on inside srt admits: the Router's shell executor now runs commands (upstream's presets move them to the background after 5 s), bounded by the router row of `scripts/orchestrator/hcom-seat` (its deny lists, the state root `<DSH_HOME>/router-state`, the credential root read grant, the loopback binding); the presets are now upstream's as shipped, not the kit's restatement.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-58`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 1c9dceec3b4e01cef06f6e61391b72ae17279c1a and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 1c9dceec, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-57 records and re-verify each at this head with its lines re-mapped; hunt on the U406 change against 57e5345a1. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 1c9dceec3b4e01cef06f6e61391b72ae17279c1a: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-58` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 1c9dceec3b4e01cef06f6e61391b72ae17279c1a <output-dir>/run-metadata.json` prints 1 or more.
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
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U411 status=ready_for_review pr=none head=1c9dceec3b4e01cef06f6e61391b72ae17279c1a note=<count> findings validated in run-58`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U410-security-audit-sweep-u406b-head.md`.
