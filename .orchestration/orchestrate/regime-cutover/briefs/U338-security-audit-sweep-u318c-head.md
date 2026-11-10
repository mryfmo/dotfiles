# U338 the security-audit sweep of unit U318's round-3 head (U318c) 95887598 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U318c head 95887598e57b2d51a876fde8da72517791e6ce15 (branch `fix/seat-login-preflight-root-spelling-and-predicates` from origin/main 668ba887; the unit makes `seat-login-preflight` normalise the seats root's spelling (empty, `.` and `..` components and trailing slashes dropped by parameter expansion; a relative root unreadable) before the link test, and judge each component only under a parent this user can search, refusing by name with the unsearchable directory; one launcher-side test in `tests/unit/test_hcom_seat.py` asserts the preflight's line and exit 2 pass through `hcom-seat` unchanged; the pins regenerated). The sweep is the Audit sweep rule of AGENTS.md for every unit before its pull request merges; its output is advisory and records-only.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-29/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-2`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-2` and the bus store, and gives it no network. The previous run of this seat is run-28 (the U330 head 55573b7c); this unit has no earlier swept head. The change under hunt against 668ba887: `git diff --name-only 668ba887 HEAD` (6 paths). The hunt reads the normaliser (can a spelling survive it and still follow a link: `//`, `/./`, `/../`, a trailing dot, a NUL-free but odd byte sequence; does the relative-root refusal hold for `./x` and `~`), the ancestor walk (can an unsearchable ancestor hide a link; does the walk stop at `/`), and the pass-through test's fixture, the generator's new pin, and the test fixtures for the fake `claude` and the fake hcom whose outputs a seat could shape.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-29`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 log -1 --format=%H` prints 95887598e57b2d51a876fde8da72517791e6ce15 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-2`, repo name `dotfiles`, output directory the one of step 1, source ref 95887598, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-28 records and re-verify each at this head with its lines re-mapped; hunt on the U330 change against 668ba887. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 95887598e57b2d51a876fde8da72517791e6ce15: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-29` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 95887598e57b2d51a876fde8da72517791e6ce15 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-28 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U338 status=ready_for_review pr=none head=95887598e57b2d51a876fde8da72517791e6ce15 note=<count> findings validated in run-29`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U309-security-audit-sweep-u306-head.md`.
