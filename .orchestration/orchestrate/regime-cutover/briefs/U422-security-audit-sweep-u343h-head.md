# U422 the security-audit sweep of unit U343h's head eb648bcd on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U343f head eb648bcda56a4f3bb43d79bd9f9b44151f1d1c90 (branch `feat/acp-broker-lever`, PR 720, round 6 of U343 on the round-5 head 8a049561: the reaper writes the exit record through the pinned helper `scripts/orchestrator/acp-record-place.py` (new, with its copy, pin and `tests/unit/test_acp_record_place.py`), which opens the broker directory once with O_NOFOLLOW, holds it to the device and inode the listener read (ACP_BROKER_DIR_ID), and unlinks, creates O_EXCL|O_NOFOLLOW, writes, syncs and renames every entry relative to that descriptor; the broker holds the helper by path check, private copy and pin as hcom-seat holds profile-config-place.py; no redirection or mv into the broker directory remains; 10 files, +1489 -46) from the srt worker seat `sweep-3`, so unit U343h has its sweep row at the head that merges (the sweep bullet of AGENTS.md:70-71: every trust-boundary unit gets one sweep before its pull request merges). The findings are advisory rows of the program ledger, never a verdict.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-65/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-64 (the U413 head bd5106c0); the earlier swept head of this unit's pull request is 8a049561 (run-64, sweeps/U421-8a049561). The change under hunt against 8a049561: `git diff --name-only 8a049561 HEAD` (10 paths). The hunt reads the helper's descriptor discipline (every call relative to the held directory descriptor; the identity, owner and mode checks; the refusal and failure lines; the 4096-byte stdin limit), the broker's hold of it (the path check, the private copy's directory and mode, the pin read by sed from the manifest, the argv), how ACP_BROKER_DIR_ID travels from the listener's one stat to each connection and what a missing or forged value does, and whether any bash of the broker still names a path under the broker directory for a write. Read `verdicts/U343g-8a049561.md` for the round-5 finding the unit answers.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-65`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints eb648bcda56a4f3bb43d79bd9f9b44151f1d1c90 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref eb648bcd, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-64 records and re-verify each at this head with its lines re-mapped; hunt on the U343h change against 8a049561. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep eb648bcda56a4f3bb43d79bd9f9b44151f1d1c90: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-65` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c eb648bcda56a4f3bb43d79bd9f9b44151f1d1c90 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-64 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread `regime` (the TASK arrives on that thread; reply on it with `hcom send --thread regime`) when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U422 status=ready_for_review pr=none head=eb648bcda56a4f3bb43d79bd9f9b44151f1d1c90 note=<count> findings validated in run-65`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U421-security-audit-sweep-u343g-head.md`.
