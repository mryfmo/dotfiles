# U394 the security-audit sweep of unit U393's head 195ce731 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U393 head 195ce731dd002a6922c4e64d73f62e54ea5924ff (branch `fix/regime-store-move-drops-the-sync-gate` from origin/main 41281b99; the unit removes from `scripts/orchestrator/regime-store-move` and its copy under `home/dot_local/bin/common/` the comparison of the live store with origin/main (the fetch of main, the masker run under uv, the hash-object comparison and the `a records sync is still due` refusal), whose verdict becomes `ready: <n> live files; the derived store is absent`, with `tests/unit/test_regime_store_move.py` reshaped (two new tests, the obsolete ones removed), the README paragraph and the pin regenerated; 6 files, +286 -547) from the srt worker seat `sweep-2`, so unit U393, in the trust-boundary class by its brief's TRUST section, has its sweep row at the head that merges (the sweep bullet of the Audit section, `AGENTS.md:71`). This unit changes no code and opens no pull request; its product is the validated findings set under the seat's state root and the RESULT line that names it. The coordinator copies the set into the store.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-53/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-2`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-2` and the bus store, and gives it no network. The previous run of this seat is run-52 (the U221e head 89a533f0); this unit has no earlier swept head. The change under hunt against 41281b99: `git diff --name-only 41281b99 HEAD` (6 paths). The hunt reads what the lever still does before the move (the walk of the live store and its shape checks, the store root hold, the derived-store judgement, the scratch directory, the procedure it prints) for a path a same-user writer could steer, a read whose failure passes as an absence, or a printed line that could run something other than the operator intends, and whether removing the comparison lets the printed procedure lose a record (it does not: the copy is the whole live store, line 3 proves it).

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-53`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 log -1 --format=%H` prints 195ce731dd002a6922c4e64d73f62e54ea5924ff and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-2`, repo name `dotfiles`, output directory the one of step 1, source ref 195ce731, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-53 records and re-verify each at this head with its lines re-mapped; hunt on the U393 change against 41281b99. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 195ce731dd002a6922c4e64d73f62e54ea5924ff: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-2/security-audit/run-53` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 195ce731dd002a6922c4e64d73f62e54ea5924ff <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-2 status --porcelain` prints nothing.

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
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U394 status=ready_for_review pr=none head=195ce731dd002a6922c4e64d73f62e54ea5924ff note=<count> findings validated in run-53`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U391-security-audit-sweep-u221e-head.md`.
