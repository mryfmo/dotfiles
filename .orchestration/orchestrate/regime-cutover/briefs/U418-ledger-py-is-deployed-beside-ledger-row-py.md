# U418 the ledger reader `ledger.py` is deployed beside the deployed row writer `ledger-row.py`, pinned like it, so the coordinator's deployed lever writes a row

GOAL
Table row x18 (`tests/security-sweep-gate.tsv`) is NG, measured 2026-11-10: `python3 -I ~/.local/bin/common/ledger-row.py --help` exits 2 with `refused: ~/.local/bin/common/ledger.py: no ledger.py beside the lever; the row is composed and judged through it alone`. The writer is deployed by chezmoi from `home/dot_local/bin/common/executable_ledger-row.py` and imports `ledger.py` from its own directory (`HERE`, ledger-row.py:92 and its docstring: "it needs ledger.py beside it wherever it runs"), but the source tree has no `home/dot_local/bin/common/ledger.py`, so every deployed run refuses; today's eight rows were written with the chezmoi source clone's copy `~/.local/share/chezmoi/scripts/orchestrator/ledger-row.py`, which has the reader beside it (decisions 2026-11-10T02:02:03Z). The fix deploys the reader beside the writer in the form the kit already uses for the writer itself: a byte-identical copy under `home/dot_local/bin/common/`, pinned in the manifest's `claude.levers.sha256` through the generator, and a test that holds the copy equal to `scripts/orchestrator/ledger.py`.

SCOPE
A new branch `fix/deploy-ledger-reader` from origin/main f66c4d78; the tree is the worker repository `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U418` (clean, made by worker-worktree.sh). May write: `home/dot_local/bin/common/ledger.py` (new, the copy; not `executable_`: the reader is imported, never run), `home/dot_agents/agent-config.yaml` through `scripts/generate-agent-configs.py` (the pin line `ledger.py: <sha256>` under `claude.levers.sha256`, and one sentence in the comment block that names ledger-row.py), `scripts/generate-agent-configs.py` only if the pin list is a literal there (read how `ledger-row.py` and `brief-check.py` get their pins and follow that form), `tests/unit/test_lever_self_check.py` or the test module that already holds the copy-equals-source assertions for the levers (read which one does and extend it), `scripts/orchestrator/README.md` (one sentence in the `ledger-row.py` section), the regenerated outputs, and the PR body `/tmp/dotfiles-wt/U418-pr-body.md`. Non-goals: `scripts/orchestrator/ledger.py` itself; `ledger-row.py`'s import or self-check; `deploy-kit.sh`; any other lever.

CONTEXT
`scripts/orchestrator/ledger.py` (the one reader, U122 round 6); `scripts/orchestrator/ledger-row.py` :70-71 and :92 (HERE); `home/dot_local/bin/common/executable_ledger-row.py` (the deployed writer's source; a `cmp` with the orchestrator copy is 0 today); `home/dot_local/bin/common/executable_brief-check.py` (the other deployed Python lever, the same form); the manifest's `claude.levers.sha256` block (home/dot_agents/agent-config.yaml, the lines near `brief-check.py:` and `ledger-row.py:` pins) and the comment block above it (`:870-873` names ledger-row.py and "ledger.py beside it"); `scripts/generate-agent-configs.py`: find where the pin block is produced (grep `levers` and `sha256`) and whether its member list is literal or discovered from the directory; the test module that asserts each deployed copy equals its orchestrator source (grep `executable_` in tests/unit). chezmoi names: a source file `home/dot_local/bin/common/ledger.py` lands at `~/.local/bin/common/ledger.py` with mode 0644 (no `executable_` prefix), which is what an import needs.

DATA SHAPE
One more member of the deployed lever set: `ledger.py`, a byte-identical copy of `scripts/orchestrator/ledger.py`, pinned by its sha256 in `claude.levers.sha256`, held equal by one test. No new behaviour; the writer's existing import finds it.

CHANGE
1. Test first, red at f66c4d78: `home/dot_local/bin/common/ledger.py` exists and equals `scripts/orchestrator/ledger.py` byte for byte, and the manifest holds a `ledger.py:` pin equal to its sha256 (extend the module that already asserts this for `ledger-row.py` or `brief-check.py`; if none does, add the assertions to `tests/unit/test_lever_self_check.py`). Paste the red line to `/tmp/u418/red.txt`. 2. The copy (`cp` of the orchestrator file; `cmp` 0). 3. The pin through the generator (`make render-check` form), and the one comment sentence. 4. README: one sentence. 5. Body at `/tmp/dotfiles-wt/U418-pr-body.md`: Summary (three sentences, the measured refusal quoted), Contract (the DATA SHAPE), Threat table (one row per changed path, status closed, the Verification line as evidence), Verification (ACCEPTANCE pasted), `Program-Unit: regime-cutover/U418` once at the end.

ACCEPTANCE
1. The red line at f66c4d78 and its green line at the head, pasted. 2. `uv run --with pyyaml python -m unittest tests.unit.test_lever_self_check tests.unit.test_generate_agent_configs` OK with counts, pasted. 3. `scripts/ci/run-on-lint-files.sh` (ruff format, prettier as the Makefile lint target runs them) exit 0, `make render-check` exit 0, `make validate-agent-assets` exit 0, `cmp home/dot_local/bin/common/ledger.py scripts/orchestrator/ledger.py` exit 0, pasted. 4. `git diff --stat f66c4d78 HEAD` pasted; only the copy, the test module, the manifest, the README, the generator if touched, and the generated outputs in it. 5. From a scratch directory holding copies of `home/dot_local/bin/common/executable_ledger-row.py` (as `ledger-row.py`) and `home/dot_local/bin/common/ledger.py`: `python3 -I -S <scratch>/ledger-row.py --help` exits 0 (the writer finds the reader beside it), pasted.

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator pushes the branch, opens the pull request, and the one audit (standard), the sweep and CI follow. After the merge and `make deploy-kit`: `python3 -I ~/.local/bin/common/ledger-row.py --help` exits 0 on this host and row x18 turns OK (standing order 42).

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the generator's pin form and chezmoi's naming rule for an unprefixed source file (mode 0644 at the target), and `cmp` as the equality check; it reads no store and changes no lever's logic.

TIMEBOX
30 minutes.

FORBIDDEN
No change to `scripts/orchestrator/ledger.py` or to `ledger-row.py`'s import; no pin edited by hand; no `executable_` prefix on the reader; no push; no rebase; no `git stash`; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u418/`, then read it); write the first progress line within five minutes of starting.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/.local/state/regime-store/dotfiles/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the program store; you stop at a committed head in `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U418`. The repository is yours alone; your final line is the Task return.
- Progress line at `/tmp/dotfiles-wt/U418-progress.txt` at every step; final report to `/tmp/dotfiles-wt/U418-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the test's red and green lines, the ACCEPTANCE lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 41, 42, 44, 46, 49); the U222 brief and its rounds (the writer's deploy form); decisions 2026-11-10T02:02:03Z.
