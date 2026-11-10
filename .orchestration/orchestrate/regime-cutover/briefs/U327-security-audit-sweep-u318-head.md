# U327 the security-audit sweep of unit U318's head e0dd8cc2 on the srt worker seat

GOAL
Run the `security-audit` skill in full audit mode over this repository at the U312 head e0dd8cc221de0b19477d82c850d1f631042bef4d (branch `feat/seat-login-shared-config-dir` from origin/main 28482832; the unit makes the seats' Claude login one claude.ai login per host in the shared directory `<seats-root>/.state/claude`: every seat's bridge child and the dsh gateway child run under it as CLAUDE_CONFIG_DIR, the launcher carries it as one role-table row (write root 2 and a read root for every role, 0700 when absent, a link refused, its settings, rules, hooks, plugins, skills, commands and agents write-denied), the shim exports the directory and clears the token name, the launcher unsets a caller's token before its first child, the preflight judges `claude auth status` under the directory and prints the one operator command when absent; the token file, the setup-token text and the Keychain probe are gone from both levers; 14 files, 1076 insertions, 751 deletions; a trust-boundary change: credentials and sandbox settings).

SCOPE
No branch, no commit, no pull request, no file of the repository changes. Writes only under `~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-21/` (the output directory, created by step 1) and the skill's per-agent `scratch/` directories below it. The target is the seat's own checkout `~/.local/state/omp-seats/dotfiles/sweep-3`, positioned by the coordinator at the head before the TASK, read-only for the run: `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing before and after.

CONTEXT
Measured 2026-11-06 on this host. The skill is installed at `~/.agents/skills/security-audit/` at the pinned commit c1c8a8c1 (the manifest's `assets.security-audit-skill`), audience `omp-worker` only. The seat's containment lets it write only its own checkout, its state root `~/.local/state/omp-seats/dotfiles/.state/sweep-3` and the bus store, and gives it no network. The previous run of this seat is run-20 (the U301b head 964c6a07); its records are the set to carry. The change under hunt against 2b2415f6: `git diff --name-only 2b2415f6 HEAD` (16 paths). The hunt reads the shared directory as a grant every seat shares (what a seat can write there that another seat's bridge child or the operator's next launch reads: `.claude.json`, `.credentials.json`; what the eight denies leave open), the preflight's parse of `claude auth status` JSON (a hostile or truncated answer), the operator command it prints (an injection through the seats root path), the 0700 creation and the link refusal, and whether any path still reads the retired token file.

CHANGE
1. `mkdir -p ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-21`; confirm `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 log -1 --format=%H` prints e0dd8cc221de0b19477d82c850d1f631042bef4d and the status is clean; write both result lines into `<output-dir>/preflight.txt`.
2. Read `~/.agents/skills/security-audit/SKILL.md` whole, then the phase files as each phase needs them. Setup values: skill directory `~/.agents/skills/security-audit`, target `~/.local/state/omp-seats/dotfiles/sweep-3`, repo name `dotfiles`, output directory the one of step 1, source ref e0dd8cc2, checkout clean.
3. Run the six phases in order and write the seven shared files into the output directory. Carry the run-20 records and re-verify each at this head with its lines re-mapped; hunt on the U312 change against 2b2415f6. Every finding carries the fields `report-schema.json` requires. Coverage over volume: the coverage ledger names every top-level directory of the target with a verdict.
4. Validate: `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` and `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json`, both exit 0; paste both result lines into `<output-dir>/validation.txt`. A validation failure is fixed in the JSON, never by dropping a finding.
5. Write `<output-dir>/summary.txt`: first line `security-audit sweep e0dd8cc221de0b19477d82c850d1f631042bef4d: <count> findings, advisory`, then one line per finding `<severity><TAB><id><TAB><file:line><TAB><title>`, the counts by severity, the files written, and the wall time.

ACCEPTANCE
1. `ls ~/.local/state/omp-seats/dotfiles/.state/sweep-3/security-audit/run-21` lists `run-metadata.json architecture.md coverage-ledger.json findings.json REPORT.md FINDINGS-DETAIL.md NEEDS-VALIDATION.md preflight.txt validation.txt summary.txt`.
2. `node ~/.agents/skills/security-audit/validate-findings.cjs <output-dir>/findings.json` exit 0.
3. `node ~/.agents/skills/security-audit/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json` exit 0.
4. `grep -c e0dd8cc221de0b19477d82c850d1f631042bef4d <output-dir>/run-metadata.json` prints 1 or more.
5. `git -C ~/.local/state/omp-seats/dotfiles/sweep-3 status --porcelain` prints nothing.

VERIFY
The commands of ACCEPTANCE in the seat, their result lines pasted into `<output-dir>/validation.txt`.

CLOSURE
remove

TRUST
TRUST: the unit trusts the `security-audit` skill at its pinned commit c1c8a8c1 and the seat's srt containment as the bounds of the run, and the run-20 records as the set to carry; it changes no file of the repository, removes nothing and opens no pull request; its product is the validated findings set and the RESULT line.

TIMEBOX
300 minutes. On expiry, validate what exists, write `summary.txt` with the word `partial` after `advisory` in its first line, and send the RESULT.

FORBIDDEN
No edit, commit, branch, push or pull request; no write outside the output directory; no network; no build, test or execution of the target's code; no installation; no `gh` call; no read of a credential store or `~/.ssh`; no secret in any file you write; no absolute home directory in the findings (write `~/...`); no word of the store's `redact-words.txt`.

REPORT
One line on the team thread when the output directory holds the ten files and both validators exit 0: `RESULT v1 task_id=U327 status=ready_for_review pr=none head=e0dd8cc221de0b19477d82c850d1f631042bef4d note=<count> findings validated in run-21`. Nothing else goes on the bus; the files are the report.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (standing orders 6, 9, 11, 13, 21, 27); `AGENTS.md:70-71`; `~/.agents/skills/security-audit/SKILL.md`; `briefs/U316-security-audit-sweep-u301-head.md`.
