# U401 the security-audit sweep of unit U222's round-4 head (U222d) 60415f10 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U222 head 60415f1083ce9243aa38be60649a256df91dc790 (branch `feat/ledger-row-writer` from origin/main 62e682f3; the unit adds `scripts/orchestrator/ledger-row.py` and its copy under `home/dot_local/bin/common/`, the writer of every coordinator row of the program store's `ledger.tsv`: six kinds with fixed verdict and verifier words, the audit word read from the verdict file, the sweep pin read from the manifest, two cross-row refusals and a parse-before-write through `ledger.py`; with `tests/unit/test_ledger_row.py`, one README paragraph, the manifest entry and pin and the generated outputs; round 4 removes every helper file (the temporary, the lock file, os.replace, the mode copy): the ledger's own descriptor is the advisory lock, the text is read through it, one append is written under it and fsynced, a failed or short write truncates back to the recorded length, every argv element is checked before parsing; rounds 2 and 3 added the realpath and per-component lstat rule for every file under the store, the stricter findings pattern, ENOENT-only fallthrough, the gate's separator class and no bytecode; the same 7 files against the base) from the srt worker seat `sweep-3`, so unit U222, in the trust-boundary class by its brief's TRUST section, has its sweep row at the head that merges (the sweep bullet of the Audit section, `AGENTS.md:71`). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it. The coordinator copies the set into the store.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-52/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-51 (the U222c head 238f0f55); carry its records and re-verify each at this head. The change under hunt against 62e682f3: `git diff --name-only 62e682f3 HEAD` (7 paths). The hunt reads the writer (can an argument put a tab, a newline or a second row into the ledger; can the manifest or the verdict file the lever reads be steered by a link or a planted copy; does the parse-before-write hold against a ledger changed between the read and the append; can a caller make the lever write a verdict word; what the installed copy does without `ledger.py` beside it) and whether any test fixture writes outside its scratch directory.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-52`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 60415f1083ce9243aa38be60649a256df91dc790 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 60415f10, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-52 records and re-verify each at this head with its lines re-mapped; hunt on the U222 change against 41281b99. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 60415f1083ce9243aa38be60649a256df91dc790: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-52` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 60415f1083ce9243aa38be60649a256df91dc790 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-52 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U401 status=ready_for_review pr=none head=60415f1083ce9243aa38be60649a256df91dc790 note=<count> findings validated in run-52`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U400-security-audit-sweep-u222c-head.md`.
