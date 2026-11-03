# U141 srt is pinned in mise, the doctor reports it beside the pin, and hcom-seat refuses another srt line

GOAL
`srt` (`@anthropic-ai/sandbox-runtime`) is the whole-process boundary of every omp seat, and it is the one seat-critical tool that tracks `latest` (`home/dot_mise/config.toml:24`), while `hcom-seat` encodes the behaviours of 0.0.81 in five places (`scripts/orchestrator/hcom-seat:219, 738, 1350, 1696, 1717`: the Seatbelt regex and glob rendering of a settings path, the writable own TMPDIR, the own-write paths, the deeper deny under an allow, the `*:*` bind grant). A release that changed any of them would move the seat boundary with no change in this repository, and no doctor check names srt today. The decisions row `srt pin:` of the store (2026-11-03, phase `truth`) decides: pin the installed 0.0.81 (`srt --version` printed `0.0.81` on this host on 2026-11-03), the bump review owned by the operator until named. After this unit mise holds srt at 0.0.81 with a `# Held:` comment the hold reader lists, `make doctor` prints the installed srt version beside the pin and fails on a difference, `hcom-seat` refuses (exit 2) before anything is made when the installed srt's major.minor differs from the line it encodes, and a unit test drives that refusal with a fake srt.

SCOPE
One branch `seat/pin-srt-and-refuse-another-line` from `origin/main`. May write: `home/dot_mise/config.toml` (the sandbox-runtime entry and its comment), `tests/unit/test_pin_records.py` and `tests/unit/test_supply_chain_policy.py` (only where they enumerate the held mise tools), `scripts/check-tools.sh` (a new `check_srt` beside `check_hcom` and its call), `tests/install/common/check_tools.bats` (three new cases), `tests/fixtures/hcom-seat/fake-tool.py` (the `srt --version` answer), `scripts/orchestrator/hcom-seat` (the version refusal and the `SRT_LINE` constant) with its copy `home/dot_local/bin/common/executable_hcom-seat` and its `claude.levers.sha256` pin line in `home/dot_agents/agent-config.yaml` (through the generator write run only), `tests/unit/test_hcom_seat.py` (the new refusal test). No other file.
Round 2 (2026-11-03, decisions row `U141 round 2:`): also `tests/unit/test_regime_start.py` (the `srt` stand-in binary answers `--version`) and `tests/unit/test_runtime_health.py` (the doctor fixture or its expected optional-warning count for the absent srt); `check_srt` and the launcher refusal are not weakened.

CONTEXT
The hold form: a `# Held:` comment directly above the entry, as `npm:prettier` has (`home/dot_mise/config.toml:36-37`); `scripts/pin_records.py mise-holds home/dot_mise/config.toml` lists the held tools (today `npm:ccstatusline`, `npm:ccusage`, `npm:prettier`, `npm:pnpm`) and `scripts/upgrade-tools.sh` skips them. The doctor: `check_hcom` at `scripts/check-tools.sh:227-237` prints `found:   hcom -> <path> (pin <version>)` and runs `--version`; `check_srt` follows the same shape, resolves srt as the seat does (`mise which srt`, else `PATH`), reads the pin from the applied mise config (`~/.config/mise/config.toml`, falling back to `home/dot_mise/config.toml` of the checkout when run there), counts a required failure when the first token of `srt --version` differs from the pin, and warns optionally with `run make update` when srt is absent; its three Bats cases follow `check_tools.bats:37-51`. The launcher: right after `pin_exec srt "${srt_path}"` (`hcom-seat:1590`) run `"${srt_path}" --version` with its status read (standing order 21: a failed or empty read is a refusal, never a pass), compare the first version token's major.minor to a constant `SRT_LINE=0.0` declared beside the 0.0.81 comment at line 219 and naming the behaviours it encodes, and `refuse` (exit 2) naming both when they differ; this runs before any seats root or process exists. The fake tool `tests/fixtures/hcom-seat/fake-tool.py` answers `srt --version` with `${FAKE_SRT_VERSION:-0.0.81}`, or exits 1 when it is `fail`. The test in `tests/unit/test_hcom_seat.py` follows the existing srt tests: `FAKE_SRT_VERSION=0.1.0` is refused with exit 2, stderr naming `0.0` and `0.1.0`, no seats root created and no omp call; `0.0.99` launches; `fail` refuses the same way.

CHANGE
1. Pin: `"npm:@anthropic-ai/sandbox-runtime" = "0.0.81"` with its `# Held:` comment naming the seat boundary and that a bump is a reviewed unit re-reading the five `hcom-seat` behaviours; `pin_records.py mise-holds` lists it; add it to the two tests that enumerate the holds.
2. Doctor: `check_srt` and its call in the check list; three Bats cases (found at the pin; another version is a required failure naming both; absent is an optional warning). Bats runs in CI only (AGENTS.md Test Policy), never on the host.
3. Launcher: the fake tool's `--version` answer; `SRT_LINE` and the refusal in `hcom-seat`; the unit test; the generator write run so the copy and the pin follow; `make render-check`.
4. `uv run --no-project --with pyyaml python -m unittest tests.unit.test_hcom_seat tests.unit.test_lever_self_check tests.unit.test_pin_records tests.unit.test_supply_chain_policy` OK; `make validate-agent-assets` exit 0.
5. Red proof: the new refusal test fails on `origin/main`'s `hcom-seat` (copy the old lever from `git show origin/main:scripts/orchestrator/hcom-seat` into scratch and point the test at it, or run the test on a scratch checkout of `origin/main`); paste the failing line.

ACCEPTANCE
1. `python3 -I scripts/pin_records.py mise-holds home/dot_mise/config.toml` lists `npm:@anthropic-ai/sandbox-runtime` and `grep -c 'sandbox-runtime" = "latest"' home/dot_mise/config.toml` prints 0. 2. `bash -c 'source scripts/check-tools.sh; check_srt; echo "req=${required_failures}"'` prints a `found:   srt ->` line whose pin equals the printed version, then `req=0`. 3. `grep -c '@test "\[common\] check_srt' tests/install/common/check_tools.bats` prints 3. 4. `grep -c 'SRT_LINE' scripts/orchestrator/hcom-seat` prints 3 or more and `bash -n scripts/orchestrator/hcom-seat` exits 0. 5. The test modules of CHANGE 4 OK (paste the Ran lines) and the red proof. 6. `make render-check` exit 0 and `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0. 7. The PR body's Contract states what is left out: no Linux measurement (a later unit), no change to the seat settings or the canary, the host `make update` is the operator's step after the merge.

VERIFY
The commands of ACCEPTANCE in the worker's tree with their result lines pasted into the PR body's Verification section; `make shellcheck`; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.

CLOSURE
allowlist: the one srt line `hcom-seat` accepts is the constant `SRT_LINE`; a bump is a reviewed edit of that constant and the pin together.

TRUST
TRUST: the unit trusts the installed srt's `--version` output as the version it is, the hold reader's reading of the `# Held:` comment, and the measured 0.0.81 behaviours the lever already encodes; it does not re-measure srt and does not change the seat settings or the canary.

TIMEBOX
60 minutes.

FORBIDDEN
No change to the seat settings, the canary or any `hcom-seat` behaviour other than the version refusal; no `make update` or `chezmoi apply` on the host; no local bats; no edit outside SCOPE; no `gh` call; no mention of any private design directory in files, commits or the PR body.

WORKER RULES (standing orders 27, 29, 31, 34; read `preferences.md` lines 23 to 45 in the store)
- Never run git or edit files in `~/Workspace/dotfiles` (the coordinator's checkout; no `git worktree add`, no commit there), never push, never open or edit a PR, never edit the live store; you stop at a committed head in your tree and the coordinator fetches it by path and pushes. Your tree is the one the coordinator names in your task, a repository of its own under `$TMPDIR/dotfiles-wt/`; every command runs with it as cwd; if you believe it is absent, stop and report, never make another. Never `git stash`. No `/tmp` literal in tracked files.
- Run every test in the foreground with a timeout and paste its result line; progress line beside your tree (`../U141-progress.txt`) every ten minutes at most; `grep -n` then bounded reads; first edit within fifteen minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Before you report: the modules named in ACCEPTANCE; `make shellcheck`; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check`; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed`.
- Write the PR body beside your tree (`../U141-pr-body.md`) with `## Summary`, `## Contract` (with a `Trusted:` sentence), `## Threat table` (`row | risk | status | evidence`, one row per changed path and one per control: the version read fails closed, the refusal runs before anything is made, the pin refresh), `## Verification` (the result lines and the red proof), the line `Program-Unit: regime-cutover/U141`, a blank line, then `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.

REPORT
Status, head sha (40 hex), files changed, the result lines, the red proof, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (order 21 fail closed, order 29); the store's decisions row `srt pin:` (2026-11-03); `scripts/orchestrator/README.md:190` (Linux unmeasured, owner U85).
