# U419 the security-audit sweep of unit the U416 head 3ee60e98 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U20 head 3ee60e987c04e28f31fbb84d48f622af80b8b204 (branch `feat/router-settings-apply-admission-cell`, PR 751; the unit makes `scripts/orchestrator/router-settings-apply` and its copy write a third settings block, `policy`, with the github Source's `admission.pulls.unlistedUnaddressed` cell set from the manifest scalar `observe_admission` (`inferred` or `ignore`, a third word refused), between the eval and source writes; the generator and validate-agent-assets admit the key; tests in `tests/unit/test_router_settings_apply.py`; 8 files, +351 -79) from the srt worker seat `sweep-3`, so unit U416 has its sweep row at the head that merges (the sweep bullet of AGENTS.md:70-71: every trust-boundary unit gets one sweep before its pull request merges). The findings are advisory rows of the program ledger, never a verdict.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-63/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-62 (the U20 head 3ee60e98). The change under hunt against origin/main f66c4d78: `git diff --name-only f66c4d78 HEAD` (8 paths). The hunt reads what the lever now writes to the Management API: the policy value is the view as read with one cell changed (rules, allowed list and other Sources carried); the manifest scalar is a two-word table, anything else refused before any request; the only peer stays the loopback port with the fixed header; what a `policy` save changes upstream (policyVersion; no restart).

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-63`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 3ee60e987c04e28f31fbb84d48f622af80b8b204 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 3ee60e98, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-62 records and re-verify each at this head with its lines re-mapped; hunt on the U416 change against f66c4d78. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 3ee60e987c04e28f31fbb84d48f622af80b8b204: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-63` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 3ee60e987c04e28f31fbb84d48f622af80b8b204 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-62 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread `regime` (the TASK arrives on that thread; reply on it with `hcom send --thread regime`) when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U419 status=ready_for_review pr=none head=3ee60e987c04e28f31fbb84d48f622af80b8b204 note=<count> findings validated in run-63`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U417-security-audit-sweep-records-sync-55.md`.
