# U244 pr-merge.sh requires the sweep row for every unit, and stops reading briefs

GOAL
The operator's goal makes the security-audit skill mandatory. The PRD narrowed that to trust-boundary units (R-48, M-08, M-19) and U242 restored it on 2026-11-06: every unit and every program milestone gets one sweep, and `pr-merge.sh` refuses a program pull request without a sweep row at the audited head. Today the lever (U147 rounds 1 to 4) decides the class by loading `brief-check.py` through a probe and looking for a `TRUST` section in the unit's brief; that probe, the brief lookup and their refusal cases exist only to tell the two classes apart. With one class there is nothing to tell apart. This unit makes the sweep row a requirement of every pull request the lever merges and deletes the brief reading whole. Nothing is widened by adding; the gate gets simpler.

SCOPE
A new branch `feat/pr-merge-sweep-every-unit` from `origin/main` d1ecd495 (your tree is `/tmp/dotfiles-wt/U244`; if it is absent, wait 30 s and look again). May write: `scripts/orchestrator/pr-merge.sh`, its deployed copy `home/dot_local/bin/common/executable_pr-merge.sh` (byte-identical to the source; find how U147 kept them in step before you copy by hand), `tests/unit/test_pr_merge.py`, the one sentence of `AGENTS.md` (line 71 at d1ecd495, the sweep bullet) and any sentence in `docs/` that says the lever reads the brief or gates trust-boundary pull requests only (grep `trust-boundary pull request` and `TRUST` under `docs/`), the lever's pin in `home/dot_agents/agent-config.yaml` only if the manifest pins `pr-merge.sh` by sha256 (grep for it; regenerate, never edit by hand), and the body file `../U244-pr-body.md` beside your tree. Not: the brief checker (briefs still carry their trust sections for it; only the merge lever stops reading them), the ledger reader, the audit lever, the records sync lever, the sweep row's shape.

CONTEXT
Measured at d1ecd495. `scripts/orchestrator/pr-merge.sh` (947 lines) reads the body's `Program-Unit: <program>/U<n>` line (`:233`, `:834-845`), finds the unit's `correct` or `carried` row (`require_verdict_row`, `:457-487`), then, per its header (`:84-119`), runs `trust_probe` (`python3 -I -S -c`, loads `brief-check.py` by path, exit 3 for no mark) over the unit's brief under `briefs/`, with refusals for a missing, ambiguous, symlinked, foreign or unreadable brief or `briefs/` directory, and only with the mark asks `ledger.py sweep <unit> <audited head>` and validates the row (`sweep_pin_probe` over the manifest's `assets.security-audit-skill.pin`, the `sweeps/<path>.json` findings file a regular file of this user under the store). `tests/unit/test_pr_merge.py` (717 lines, 20 tests) covers the probe's exit codes, the blind checker, the stale `__pycache__`, the brief lookup refusals and the row validation. Records syncs are unit `U20` pull requests (`Program-Unit: regime-cutover/U20`, PR 672 merged on a `correct` row) and today merge with no sweep row; under this unit they need one like every other unit (coordinator default under the operator's goal; the operator may exempt the records unit, which would then be one named unit, not a class).

DATA SHAPE
The gate's question shrinks from "is this unit of the class, and if so does it have the row" to "does this unit have the row". The inputs that remain: the body's unit, the audited head from `require_verdict_row`, the `ledger.py sweep` answer, the manifest's pin and the findings file. The brief, the `briefs/` directory and the checker are no longer inputs of the lever. Keep the row validation exactly as round 4 defined it (pr `-`, verifier `security-audit-skill <pin>` with the pin word a prefix of the manifest pin, evidence a findings file `sweeps/<path>.json` that is a regular file of this user under the store; a `sweep` row of any other shape is a malformed store).

CHANGE
1. Delete `trust_probe`, the brief and `briefs/` lookups and every refusal and exit-code sentence that exists only for them (header `@description` lines 84 to 119 and the `@exitcode 2` list, the functions, their call site). The sweep requirement runs for every pull request after `require_verdict_row` and before the checks read and the one write, as today for marked units. `ledger.py sweep` answering `none` is a refusal naming the unit, the head and the sweep rule (not a brief).
2. Keep `sweep_pin_probe` and the findings-file checks unchanged.
3. Tests: delete the probe, checker, `__pycache__`, blind-checker and brief-lookup tests; keep and retarget the row-shape tests; add one test that a unit with a plain brief (no `TRUST`) and no sweep row is refused with the rule named, and one that the same unit merges with a well-formed sweep row; keep the failing-reader and answering-reader tests (the reader's failure modes are still the lever's). Run `tests.unit.test_pr_merge tests.unit.test_pr_levers tests.unit.test_scratch_git`.
4. `AGENTS.md` line 71: the sweep bullet says every unit and every program milestone gets the sweep (drop the parenthetical that defines the class by the `TRUST` section and the trigger terms, and the sentence that scopes the refusal to trust-boundary pull requests); `pr-merge.sh` refuses a pull request whose unit has no sweep row at the audited head. One sentence each, no new rule.
5. The deployed copy identical to the source; the pin regenerated if the manifest pins the lever (state which in the body).
6. The body `../U244-pr-body.md`: Summary (the operator's goal, U242's PRD amendment, the deletion), Contract (guarantee: no pull request merges through the lever without a well-formed sweep row of its unit or a fix unit at the audited head; leaves out: who runs the sweep, the sweep's content, briefs and `brief-check.py`, records syncs' exemption which the operator may name), Threat table (one row per changed path and one per removed control: the brief probe's absence, the `briefs/` symlink checks' absence, each `closed` by the test that shows the gate no longer depends on them or `residual` naming the control that remains), Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `grep -c -E 'trust_probe|brief-check|briefs/|TRUST' scripts/orchestrator/pr-merge.sh` prints 0.
2. `cmp scripts/orchestrator/pr-merge.sh home/dot_local/bin/common/executable_pr-merge.sh` exit 0.
3. `uv run python -m unittest tests.unit.test_pr_merge tests.unit.test_pr_levers tests.unit.test_scratch_git` OK (paste the count; the two new tests named in the paste).
4. `make shellcheck` exit 0 and `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. If the manifest pins the lever: `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0 with no diff, and `grep -n pr-merge home/dot_agents/agent-config.yaml` pasted; otherwise the grep showing no pin.
6. `git diff --stat origin/main` shows the lever and its tests net negative in lines (paste it).
7. `grep -n 'trust-boundary pull request' AGENTS.md docs/ -r` prints nothing.

8. `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d`, `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` and `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0 (the Makefile `format` target), run in the tree after the last edit. (added 2026-11-06T07:20Z under standing order 44; the heads of these units were checked by the coordinator with the same commands.)
VERIFY
The ACCEPTANCE commands in your tree with their result lines pasted into the body's Verification section. The coordinator's proof after the merge is the next real merge through the deployed lever, recorded in the ledger.

CLOSURE
remove

TRUST
TRUST: the unit trusts the checkout's `ledger.py` as the one reader of the sweep row, the manifest's `assets.security-audit-skill.pin` as the reviewed pin and the store's `sweeps/` directory as the findings' home; it reads no brief, no network and no PR body field beyond the `Program-Unit` line the lever already reads, and it does not decide who runs the sweep.

TIMEBOX
60 minutes.

FORBIDDEN
No new class, flag, allowlist or exemption in the lever (an exemption for the records unit, if the operator names one, is a later unit); no change to the sweep row's shape or to `ledger.py`; no change to `brief-check.py`; no local bats; no network; no push; no `gh` call beyond none (the tests use the fake gh of `test_pr_levers`).

WORKER RULES (standing orders 21, 27, 29, 31, 34; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 50)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U244` and the coordinator fetches it by path.
- Progress line beside your tree (`../U244-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc; the header's `@description` tells the current rule, not the history of rounds 1 to 4 (one sentence may cite U147 and this unit).
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (principles Subtract Before You Add and Laziness Protocol apply: this is a deletion).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 14 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37); `AGENTS.md` (Comment Policy, Test Policy, Audit); the `decisions.tsv` rows of 2026-11-06 for U242 (phase `records`, 06:11:14Z); PR 644 (U147) as the lever's last change.
