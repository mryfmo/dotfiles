# U334 the security-audit sweep of unit U310's round-4 head (U310d) 28457a6a on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U310 head 28457a6ac5ae2518254ee52066ffcb2d2680f890 (branch `feat/dsh-role-profile-route` from origin/main 2b2415f6; the unit's round 4 makes the dsh role of `hcom-seat` place the kit's rendered overlay `~/.agents/omp/profiles/dsh.yml` as the role's own `~/.omp/profiles/dsh/agent/config.yml` at launch, with the bridge extension entry at its canonical allow-list path, a `cmp` before the write and a rename from a per-launch temporary file, through a `mktemp` temporary inside `agent/` (random name, link and inode checks before and after the write, rename), with every existence read walking from HOME and testing searchability, the compare on two regular files with both statuses read, and the check before any directory is made (the round-1 verdict's P1 symlink-write and its P2s); the manifest gains `omp.gateway_roles`, the generator renders one overlay per gateway role; round 4 alone 6 files, 587 insertions, 258 deletions on top of round 1).

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-27/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-2`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-2` and the bus store, and gives it no network. The previous run of this seat is run-26 (the U318b head ad9b9456); run-20 swept the round-1 head e92b4970 of this unit; its records are the set to carry. The change under hunt against 2b2415f6: `git diff --name-only 2b2415f6 HEAD` (9 paths). The hunt reads the new mktemp write path (can any name under agent/ still be planted; is the inode check sound), the searchability walk, and the placed profile config as configuration an attacker who writes the overlay or the profile could abuse (the extension path, the model route, the providers list), the lever's link refusals and the temporary-file rename (what a pre-existing path at the target does), the generator's new render, and the dry-run output for anything a seat could learn.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-27`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 log -1 --format=%H` prints 28457a6ac5ae2518254ee52066ffcb2d2680f890 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-2`, repo name `dotfiles`, output directory the one of step 1, source ref 28457a6a, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-26 records and re-verify each at this head with its lines re-mapped; hunt on the U310 change against 2b2415f6. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 28457a6ac5ae2518254ee52066ffcb2d2680f890: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-27` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 28457a6ac5ae2518254ee52066ffcb2d2680f890 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-26 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U334 status=ready_for_review pr=none head=28457a6ac5ae2518254ee52066ffcb2d2680f890 note=<count> findings validated in run-27`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U309-security-audit-sweep-u306-head.md`.
