# daily-<YYYY-MM-DD> the daily security-audit sweep of main's head on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at main's head named in the TASK line (`<head>`, the standing control of the Audit sweep rule C of 2026-11-18: a head whose changed paths touch no lever, policy, credential handling or deployed executable merges on its Codex audit and CI alone only while one full sweep of main's head per UTC day stands, and `pr-merge.sh` reads the day's row from the store's `daily-sweeps.tsv` before it skips such a head's own sweep row). One run per UTC day, dispatched by the coordinator with the task id `daily-<YYYY-MM-DD>`; its product is the validated findings set, the RESULT line, and the row the coordinator writes from it. The previous run of this seat is `<prev>`: carry its records and re-verify each at this head.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/<repository>/.state/<seat>/security-audit/<run>/` (the run directory named in the TASK line, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/<repository>/<seat>`, positioned by the coordinator at `<head>` before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/<repository>/<seat> status --porcelain` prints nothing before and after.

CONTEXT
The skill is installed at `~/.agents/skills/security-audit/` at the manifest's pinned commit (`assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/<repository>/.state/<seat>` and the bus store, and gives it no network. The previous run of this seat is the one the TASK line names as `<prev>`; carry its records and re-verify each at this head. The whole tree is in scope: this is the full sweep of main, not a scoped run against one change, so every top-level directory gets a verdict in the coverage ledger.

CHANGE

1. `mkdir -p ~/.local/state/omp-seats/<repository>/.state/<seat>/security-audit/<run>`; confirm `git -C ~/.local/state/omp-seats/<repository>/<seat> log -1 --format=%H` prints `<head>` and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/<repository>/<seat>`, repo name `<repository>`, output directory the one of step 1, source ref `<head>`, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the previous run's records and re-verify each at this head with its lines re-mapped; hunt over the whole tree. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep <head>: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE

1. `ls <output-dir>` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c <head> <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/<repository>/<seat> status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at the manifest's pinned commit and the seat's srt containment as the bounds of the run, and the previous run's records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line, from which the coordinator writes the day's row.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT with `status=partial`, not `ready_for_review`: `RESULT v1 task_id=daily-<YYYY-MM-DD> status=partial pr=none head=<head> note=<count> findings validated in <run>, partial`. A partial sweep is no daily sweep of main's head: the coordinator writes no daily row for it, and the per-head rule stands for every head until a full run finishes.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store, of `~/.ssh` or of the seats' token file (`<seats-root>/.state/claude-token`, which the sandbox denies); no secret in any file you write (the value of `CLAUDE_CODE_OAUTH_TOKEN` in this seat's environment is a secret: never print, echo, grep or copy it); no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=daily-<YYYY-MM-DD> status=ready_for_review pr=none head=<head> note=<count> findings validated in <run>`. Nothing else goes on the bus; the files are the report. The coordinator writes the day's row only for a RESULT with `status=ready_for_review` whose `validation.txt` holds both validators' PASS lines: it copies `findings.json` into a run-keyed directory the store does not yet hold, `test ! -e <store>/sweeps/daily-<YYYY-MM-DD>-run-<n> && mkdir <store>/sweeps/daily-<YYYY-MM-DD>-run-<n> && cp <output-dir>/findings.json <store>/sweeps/daily-<YYYY-MM-DD>-run-<n>/findings.json` (the `test ! -e` guard refuses an existing destination, so a same-day retry lands beside the earlier row's evidence and never over it), and runs `~/.local/bin/common/ledger-row.py <store> daily --head <head> --seat <seat> --run <n> --task daily-<YYYY-MM-DD> --findings sweeps/daily-<YYYY-MM-DD>-run-<n>/findings.json --swept-at <ts>` with `<ts>` the RESULT message's bus timestamp (`YYYY-MM-DDTHH:MM:SSZ`), which becomes the row's ts: the writer reads the findings file itself for the count (a JSON list of objects, else refused), refuses a `--swept-at` ahead of the clock or more than 24 hours behind it, and refuses a findings path or a seat and run an earlier row already records. That row of `daily-sweeps.tsv` is the one `pr-merge.sh` reads through `ledger.py daily 86400`. A `status=partial` RESULT (the TIMEBOX path) gets no daily row and no copy: a partial sweep does not stand for the day, and the per-head rule stands until the day's full sweep finishes.

STANDING
The program's `preferences.md` (the standing orders its sweep briefs cite); `AGENTS.md`, the "Audit" section's sweep rule; `~/.agents/skills/security-audit/SKILL.md`; the brief of `<prev>`.
