# U435 the security-audit sweep of unit U434's head 8c3cfec2 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U434 head 8c3cfec25f49a3f5e63501e8c20631cf37806205 (branch `feat/router-profile-acp-subagent`, PR 757, U434 (M-22 Part B, table row s21) on main 5b99f2c3: the Router's dsh profile gains a `subagent-acp` insert whose command is `acp-seat --socket $ACP_BROKER_SOCK --name router` and a `tool-subagent` row on the ACP provider, hcom-seat's router row exports `ACP_BROKER_SOCK=<state slot>/broker/sock`, acp-seat defaults `--repo` to its cwd and `--ref` to HEAD; 13 paths against main: home/dot_agents/agent-config.yaml, home/dot_dsh/profiles/router/cordis.patch.yml, home/dot_local/bin/common/executable_acp-seat, home/dot_local/bin/common/executable_hcom-seat, scripts/generate-agent-configs.py, scripts/generated-agent-outputs.json, scripts/orchestrator/README.md, scripts/orchestrator/acp-seat, scripts/orchestrator/hcom-seat, tests/unit/test_acp_broker.py, tests/unit/test_dsh_profile.py, tests/unit/test_generate_agent_configs.py, tests/unit/test_hcom_seat_dsh.py) from the srt worker seat `sweep-3`, so unit U434 has its sweep row at the head.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-76/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host; the seat login renewed 2026-11-10T21:58Z. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-75 (the U343j head 5b99f2c3); the earlier swept head of this unit's pull request is 5b99f2c3 (run-75, sweeps/U432-5b99f2c3). The change under hunt against 5b99f2c3: `git diff --name-only 5b99f2c3 HEAD` (13 paths: the two levers and their copies, the generator and its outputs, the router patch, the manifest pins, the README and four test modules). The hunt reads the new renderer and the private-copy steps (the copy directories under ~/.local/state/hcom-seat, what is hashed and what runs or is sourced, the manifest copy the broker set reads), the FIFO readiness read (what a broker's stdout can make hcom-seat do), the router row's socket grant (the one directory, no other role), the broker's start and stop by hcom-seat (what a Router can do to a broker started beside it; the stop in the trap and at the end), the dsh-row and worker renderings' byte identity, and re-verifies the run-75 records at this head.state/broker-logs` (its mode, its parent, whether any seat's settings could reach it, the header-name refusal), and re-verifies the run-75 records at this head. Read `verdicts/U343j-5b99f2c3.md` for the round-7 findings the unit answers.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-76`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints 8c3cfec25f49a3f5e63501e8c20631cf37806205 and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref 8c3cfec2, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-75 records and re-verify each at this head with its lines re-mapped; hunt on the U434 change against 5b99f2c3. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep 8c3cfec25f49a3f5e63501e8c20631cf37806205: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-76` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c 8c3cfec25f49a3f5e63501e8c20631cf37806205 <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-75 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread `regime` (the TASK arrives on that thread; reply on it with `hcom send --thread regime`) when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U435 status=ready_for_review pr=none head=8c3cfec25f49a3f5e63501e8c20631cf37806205 note=<count> findings validated in run-76`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U432-security-audit-sweep-u343i-head.md`.
