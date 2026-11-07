# U362 the security-audit sweep of unit U343's head (U343c) fd94feae on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U343e head (the mechanism change: the worker's directory is the broker's slot cloned from a header-named ref) fd94feaeb19322d9f17ff99f122e7ff900e4987e (branch `fix/dsh-harness-build-under-srt` from origin/main 668ba887; the unit makes `update_deepseek_harness` in `scripts/update-agent-assets.sh` run the harness build and the profile install inside srt through one function `build_under_srt` (a 0600 settings file the step creates, writes under the build directory and `$DSH_HOME/.pnpm-store` only, the dsh role's deny list, the lockfile's registry hosts, `env -i`, the exit passed through, the U272 canary before the first build), with 11 new tests in `tests/unit/test_update_agent_assets.py` and one docs paragraph; round 2 moves `env -i` outside srt so the child keeps srt's injected proxy variables, denies srt's implicit grants `/tmp/claude`, `/private/tmp/claude` and `~/.npm/_logs`, redirects the tool caches and logs inside the roots, and adds the helper's failure injections; round 3 re-keys the network-bounds exemption to the rewritten record line, moves the store's scratch TMPDIR to `<store>/tmpdir`, and allows the one `/tmp/claude` deny word in the portability guard's exact table; round 4 derives the `/private/tmp/claude` spelling from the one word and denies it when `/private/tmp` is a directory, adds the resolver injections and the table rows; round 5 adds the two module hooks the harness-coverage test demands of tests/unit/test_sandbox_portability.py). The sweep is the Audit sweep rule of AGENTS.md for every unit before its pull request merges; its output is advisory and records-only.

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-35/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-34 (the U343e head (the mechanism change: the worker's directory is the broker's slot cloned from a header-named ref) 0fc4740b); this unit has no earlier swept head. The change under hunt against 668ba887: `git diff --name-only 668ba887 HEAD` (3 paths). The hunt reads the new function (can a build directory or settings path be redirected through a link; does the deny list cover every credential root the dsh role denies; can a lockfile line widen the hosts; does a failed producer or a non-zero srt exit ever read as success; does the canary run before the first upstream command), the docs paragraph for a claim the code does not make, and the test fixtures for the fake `srt`, `pnpm` and `node` whose argv the tests record.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-35`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints fd94feaeb19322d9f17ff99f122e7ff900e4987e and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref fd94feae, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-34 records and re-verify each at this head with its lines re-mapped; hunt on the U343 change against 668ba887. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep fd94feaeb19322d9f17ff99f122e7ff900e4987e: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-35` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c fd94feaeb19322d9f17ff99f122e7ff900e4987e <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-34 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U362 status=ready_for_review pr=none head=fd94feaeb19322d9f17ff99f122e7ff900e4987e note=<count> findings validated in run-35`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U309-security-audit-sweep-u306-head.md`.
