# U310c round 3 of U310: the profile config write holds its exclusive descriptor through the write, judges the profile boundary before any temporary, and cleans its slots on refusal

GOAL
The round-2 audit of PR 708 (head 8f393491, `verdicts/U310-8f393491.md`) returned one P1 of the same class as round 1 (symlink-write) and five lower findings:
- P1 `scripts/orchestrator/hcom-seat:982`: the temporary `mktemp` made is reopened by path for the write (`> "${temporary}"`); a concurrent dsh process that owns `agent/` can swap the path for a symlink between `mktemp` and the redirection, and the redirection then overwrites the linked host file before the later identity check refuses. The auditor reproduced it with a deterministic swap. The write must go through the descriptor that created the file, never through the path again.
- P2 `:1102`: `profile_config_check` creates its comparison temporary before `settings_judge` validates the profile boundary; with `profiles/dsh` linked to `profiles/orchestrator`, a dry run writes inside `orchestrator/agent` before refusing.
- P2 `:2601`: a `profile_config_write` refusal exits after `seat_sandbox_write` without removing either per-launch slot.
- P2 `:981`: the identity-read, temporary-write and installation branches carry no failure-injection tests (only cmp, mktemp and overlay failures are injected).
- P2 carried: the threat table still lacks a `scripts/generated-agent-outputs.json` row, and the docs and orchestrator-effect rows close without a failing selector.
- P3 `home/dot_agents/agent-config.yaml:211`: the manifest row cites the wrong selector (the collision and missing-dsh refusals are exercised by `test_omp_gateway_role_overlay_carries_the_bridge_route_the_extension_and_the_seat_providers_off`).
This is the second `incorrect` of the class; the mechanism this round adopts (no path reopen, ever) ends the class or the next round needs a `mechanism-change` row (standing order 36).

SCOPE
The same branch `feat/dsh-role-profile-route` and PR 708; the tree is `/tmp/dotfiles-wt/U310c` at 8f393491 (created by the coordinator). May write: `scripts/orchestrator/hcom-seat` and its generated copy `home/dot_local/bin/common/executable_hcom-seat` (byte-identical, regenerated), the lever pins by regeneration, `tests/unit/test_hcom_seat_dsh.py`, and the body `../U310c-pr-body.md` (the round-2 body `/tmp/dotfiles-wt/U310b-pr-body.final.md` plus a Round 3 section; the whole table corrected). Not: the generator, the manifest beyond the pin rows, the omp roles' rendered settings and launch lines, the docs.

CONTEXT
Read the round-2 helper (the mktemp write, the identity checks, the compare) and `settings_judge`'s order in the launch. Bash can create a file exclusively and keep its descriptor in one step: `set -o noclobber` (or `set -C`) makes `exec {fd}> "${path}"` fail when the path exists (O_EXCL), so a random name under `agent/` opened that way is both created and held; every write then goes to `>&${fd}`, the path is never reopened. After the write, the installation is `mv -f "${path}" "${target}"`, and the only remaining race is a swap of `${path}` between the open and the rename, which the existing identity check closes when it compares the inode of `${path}` against the inode read right after the open (both reads by `stat`; a link at `${path}` is refused by `-L` first). The compare temporary follows the same discipline and is created only after `settings_judge` has accepted the profile boundary (move the check call after the judge, keep it before any mkdir of the launch; the round-2 ordering test adjusts). Slot cleanup on refusal: every `refuse` after the slots exist runs the existing cleanup path (the sandbox slot and the state slot), the same one the signal handler uses (U272e/U272f).

DATA SHAPE
One exclusive open per temporary (`noclobber` redirection on a random name, descriptor held), one write through that descriptor, one identity check (inode and non-link) before the rename, one rename. One ordering: judge the boundary, then check, then mkdir. One cleanup path for every refusal after the slots exist.

CHANGE
1. The write helper: `noclobber` exclusive open held in a descriptor; the overlay rendering and the config write go through the descriptor; the path is never reopened; identity check then rename; every refusal closes the descriptor and removes the path.
2. `profile_config_check` runs after `settings_judge` and before any mkdir; its comparison temporary uses the same helper.
3. Every refusal after the slots are made runs the slot cleanup (the sandbox slot and the state slot); a test asserts no slot remains after a placement refusal.
4. Tests: the auditor's deterministic swap (a wrapper that replaces the temporary with a symlink to a victim file between the open and the write) leaves the victim byte-identical and the launch refuses; a linked `profiles/dsh` dry run writes nothing anywhere (the orchestrator profile's `agent/` mtime unchanged); failure injections for the identity read (`stat` failing), the write (`printf` to the descriptor failing through a full or read-only target), and the installation (`mv` failing): each refuses by name and leaves no temporary.
5. The body: Round 3 section; the threat table gains the `scripts/generated-agent-outputs.json` row, the docs row as `out-of-scope` or `residual` (a doc line has no failing test), the orchestrator-effect row with a selector (the slot-cleanup test), and the manifest row's selector corrected.

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_generate_agent_configs tests.unit.test_omp_review_security_roles_removed tests.unit.test_scratch_git` OK (count pasted; the new tests named).
2. `cmp scripts/orchestrator/hcom-seat home/dot_local/bin/common/executable_hcom-seat` exit 0; `uv run --with pyyaml scripts/generate-agent-configs.py && make render-check` exit 0; `uv run --with pyyaml scripts/validate-agent-assets.py` exit 0.
3. `make shellcheck` exit 0; `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
4. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. The auditor's three reproductions re-run on a scratch host under `/tmp/u310c/`: the deterministic swap (victim unchanged, exit 2), the linked-profile dry run (no write, exit 2), the write-failure probe (exit 2, no slot left) (pasted).
6. `grep -c '> "\${temporary' scripts/orchestrator/hcom-seat` prints 0 (no path reopen of a temporary remains; paste the grep and, if the variable is named otherwise, the equivalent).

VERIFY
ACCEPTANCE pasted into the body's Verification section; the coordinator re-runs item 5 on the pushed head.

CLOSURE
remove

TRUST
TRUST: the unit trusts the kernel's exclusive create on the descriptor it holds and the inode identity `stat` reports; it writes only inside the role's own profile at launch, never reopens a path it did not just create, reads no credential and changes no omp role's rendered settings.

TIMEBOX
60 minutes.

FORBIDDEN
No write under the real `~/.omp`, `~/.dsh`, `~/.agents`, `~/.local/state/omp-seats`, `~/Workspace` (scratch HOME under `/tmp/u310c/` only); no change to the generator or the docs; no change to the omp roles' settings or launch flags; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u310c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U310c` and the coordinator fetches it by path.
- Progress line at `../U310c-progress.txt` after every step; first edit within ten minutes. Final report to `../U310c-report.txt` before you end.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only; shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes: the path reopen is the fault, not the check after it; Make Operations Idempotent: a refusal leaves the host as it found it).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against 8f393491), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 33, 34, 35, 36, 41, 42, 44, 46); `verdicts/U310-e92b4970.md`; `verdicts/U310-8f393491.md`; `briefs/U310b-*.md`; `briefs/U272e-*.md`, `briefs/U272f-*.md` (physical path, identity; the signal handler's cleanup).
