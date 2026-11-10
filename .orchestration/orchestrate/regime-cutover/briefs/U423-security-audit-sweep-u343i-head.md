# U423 the security-audit sweep of unit U343i's head 76a5c83b on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U343f head 76a5c83bf2b6ec55cc119303f3b3f0a5c8af1582 (branch `feat/acp-broker-lever`, PR 720, round 7 of U343 on the round-6 head eb648bcd, a mechanism change of form remove: hcom-seat's router row renders `<state slot>/broker` as a denyWrite row tagged slot and makes it 0700 before the settings file (`broker_dir_make`), so the Router reads the directory and can plant, rename or unlink nothing in it; acp-broker takes the directory as made (own, 0700, empty) and leaves it at its end; tests in both modules; 9 files, +574 -220) from the srt worker seat `sweep-3`, so unit U343i has its sweep row at the head that merges (the sweep bullet of AGENTS.md:70-71: every trust-boundary unit gets one sweep before its pull request merges). The findings are advisory rows of the program ledger, never a verdict.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-66/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-65 (the U343h head eb648bcd); the earlier swept head of this unit's pull request is eb648bcd (run-65, sweeps/U422-eb648bcd). The change under hunt against eb648bcd: `git diff --name-only eb648bcd HEAD` (9 paths). The hunt reads the new deny row's position and tag against the judge (a grant and a deny overlap exempted only by a shared tag), the make's place (after the state slot exists, with the slot trap armed, before the settings file names the path) and its dry-run line, what a Router can still do inside its state slot outside the broker directory, and the broker's take (own, 0700, empty, no socket) and what it leaves. Read `verdicts/U343h-eb648bcd.md` for the round-6 findings the unit answers.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-66`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 76a5c83bf2b6ec55cc119303f3b3f0a5c8af1582 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 76a5c83b, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-65 records and re-verify each at this head with its lines re-mapped; hunt on the U343i change against eb648bcd. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 76a5c83bf2b6ec55cc119303f3b3f0a5c8af1582: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-66` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 76a5c83bf2b6ec55cc119303f3b3f0a5c8af1582 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-65 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread `regime` (the TASK arrives on that thread; reply on it with `hcom send --thread regime`) when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U423 status=ready_for_review pr=none head=76a5c83bf2b6ec55cc119303f3b3f0a5c8af1582 note=<count> findings validated in run-66`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U422-security-audit-sweep-u343h-head.md`.
