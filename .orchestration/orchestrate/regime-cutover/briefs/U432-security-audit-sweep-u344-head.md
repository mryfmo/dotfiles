# U432 the security-audit sweep of unit U344b's head a65bc8ed on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U344b head a65bc8ed76a1631d9c9fe53f070b3d01d1c68954 (branch `feat/router-row-starts-acp-broker`, PR 755, U344 (M-24 part 2) on main c414f19b: the router row of hcom-seat renders network.allowUnixSockets with the Router's broker directory alone, starts acp-broker after its settings and before the shim and stops it in the trap and at the end; one settings renderer seat-settings-render.sh, sourced by both levers, renders the rows each computes; the five residual rows of U344 closed in the broker; 11 files changed in round 2 (+978 -332) on the merge of main; against main c414f19b the pull request's 13 paths) from the srt worker seat `sweep-3`, so unit U344b has its sweep row at the head that merges (the sweep bullet of AGENTS.md:70-71: every trust-boundary unit gets one sweep before its pull request merges). The findings are advisory rows of the program ledger, never a verdict.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-75/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-74 (the U343j head c414f19b); the earlier swept head of this unit's pull request is c414f19b (run-74, sweeps/U431-c414f19b). The change under hunt against c414f19b: `git diff --name-only c414f19b HEAD` (13 paths: the two levers and their copies, the new renderer and its copy, the manifest, the generated outputs, the README, the hcom-orchestration SKILL.md line, three test modules). The hunt reads the new renderer and the private-copy steps (the copy directories under ~/.local/state/hcom-seat, what is hashed and what runs or is sourced, the manifest copy the broker set reads), the FIFO readiness read (what a broker's stdout can make hcom-seat do), the router row's socket grant (the one directory, no other role), the broker's start and stop by hcom-seat (what a Router can do to a broker started beside it; the stop in the trap and at the end), the dsh-row and worker renderings' byte identity, and re-verifies the run-74 records at this head.state/broker-logs` (its mode, its parent, whether any seat's settings could reach it, the header-name refusal), and re-verifies the run-74 records at this head. Read `verdicts/U343j-c414f19b.md` for the round-7 findings the unit answers.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-75`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints a65bc8ed76a1631d9c9fe53f070b3d01d1c68954 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref a65bc8ed, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-74 records and re-verify each at this head with its lines re-mapped; hunt on the U344b change against c414f19b. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep a65bc8ed76a1631d9c9fe53f070b3d01d1c68954: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-75` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c a65bc8ed76a1631d9c9fe53f070b3d01d1c68954 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-74 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread `regime` (the TASK arrives on that thread; reply on it with `hcom send --thread regime`) when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U432 status=ready_for_review pr=none head=a65bc8ed76a1631d9c9fe53f070b3d01d1c68954 note=<count> findings validated in run-75`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U431-security-audit-sweep-u343i-head.md`.
