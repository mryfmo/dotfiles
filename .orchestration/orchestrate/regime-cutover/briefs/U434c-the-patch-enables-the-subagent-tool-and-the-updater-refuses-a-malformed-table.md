# U434c round 3 of U434 (PR 757, M-22 Part B, table row s21): the kit's patch enables the subagent tool the web-app bundle disables, the updater refuses a non-object dependency table, and the body states the reach

GOAL
Fix the blocking finding and the two P2 findings of verdicts/U434-1faa81f1.md (the round-2 audit of PR 757 at 1faa81f1a17a494c859caa79c55c57d447d8b352) on the same branch `feat/router-profile-acp-subagent` in the tree `/private/var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/dotfiles-wt/U345` (head 1faa81f1a17a494c859caa79c55c57d447d8b352, clean), as one new commit on top (no amend, no rebase). After this round the deployed Router profile mounts the subagent tool on the ACP provider with no overlay, the updater refuses a malformed dependency table instead of skipping the repair, and the body's Summary and Contract say what the repoint reaches.

CONTEXT (measured)
- P1 [f5 s8] cordis.patch.yml:31: the web-app bundle ships the top-level `tool-subagent` row `disabled: true` (`/tmp/u345/dump.txt:303-308`: the kit's patch row sets `config` and the row stays `disabled: true`). The round-1 real run worked only because its overlay (`/tmp/u345/overlay.yml`) restated the row with `disabled: false`. The kit's rendered row must carry `disabled: false` beside its config (the patch algorithm replaces a row's `config` wholesale and merges the other keys, measured in dump.txt), so the deployed profile mounts the tool. The second half of the finding, the superagent presets' nested `tool-subagent` rows with `provider: spawn` (Executor Sessions), stays the residual of U437 (planned design unit); this round changes no preset row (U406).
- P2 [f10 s3] package.json:16: the threat table's dependency row says `pending deploy`, which is not a permitted status. Permitted: `closed`, `residual`, `out-of-scope`. The row is `closed` by the generator test and the updater test; the coordinator's deployed measurement goes under Verification as a line the coordinator pastes after the merge, not as the row's status.
- P2 [f1 s4] update-agent-assets.sh:2717: `dsh_superagent_missing_dependencies` reads the names with `dict(json.load(...).get("dependencies", {}))`; a `dependencies: []` becomes an empty table and the branch skips the repair silently. The reader must refuse (exit 1, one stderr line naming the file and the shape) unless the file is a JSON object whose `dependencies` is an object; the caller already treats a failed read as a refusal of the step.
- The body's Summary still carries round 1's sentence `a Router subagent turn is an omp acp worker ... never an in-process child under the Router's own sandbox`; the auditor reads it as the contract. Rewrite Summary and Contract to the reach: the Router's base agent's subagent tool runs on the ACP provider through acp-seat; the superagent presets' Executor Sessions keep `provider: spawn` until U437.
- Standing order 49: fix the defect, prove it by a test, no review round beyond this.

DATA SHAPE
The patch row is a table of keys the patch algorithm merges (`id`, `disabled`) plus one `config` object it replaces whole; the kit's `tool-subagent` row gains `disabled: false`. The updater's dependency reader is a parser at the boundary: object with `dependencies` object -> names; anything else -> refusal (Boundary Discipline).

CHANGE
1. Red tests first: (a) `tests/unit/test_generate_agent_configs.py` (extend the U434 router test or add one beside it): the rendered router patch's `tool-subagent` row carries `disabled: false` directly under the row (before or after `config`, by the renderer's order) and the thak patch has no such row; (b) `tests/unit/test_update_agent_assets.py` `DshSuperagentTest`: subtests for `dependencies: []`, `dependencies: "x"`, a top-level JSON array and `dependencies` absent: the first three refuse (exit 1 and the stderr line naming the file), the absent case is an empty table (no names, no refusal). Run red at 1faa81f1, paste the red lines.
2. The generator: the `tool-subagent` row gains `disabled: false` (one line; keep `maxDepth: provider-managed`). Regenerate (`uv run --with pyyaml python scripts/generate-agent-configs.py`); `make render-check`, `make validate-agent-assets`, both `cmp` of the lever copies exit 0. `tests/unit/test_dsh_profile.py`'s row tests learn the key if they assert the row's exact text.
3. `scripts/update-agent-assets.sh` `dsh_superagent_missing_dependencies`: the python one-liner loads the file, checks `isinstance(data, dict)` and that `data.get("dependencies", {})` is a dict, else writes one line to stderr and exits 1; names printed as before. shdoc comment updated. shfmt and `lint-comparisons.py scripts/update-agent-assets.sh` exit 0.
4. Green: the tests of step 1 plus `tests.unit.test_generate_agent_configs tests.unit.test_dsh_profile tests.unit.test_scratch_git tests.unit.test_update_agent_assets`, pasted.
5. Body draft `/tmp/dotfiles-wt/U434c-pr-body.md`, rewriting `/tmp/dotfiles-wt/U434b-pr-body.md` whole: Summary and Contract in the reach form above; a `## Round 3` section after `## Round 2` naming each finding and the change; threat table: the dependency row `closed` (evidence: the two tests by name), a row for the `tool-subagent` enable (risk: the tool stays disabled and no subagent turn exists, or an enabled tool on another provider; closed: `disabled: false` with `provider: acp`, evidence test (a) and the dump line), the updater row's evidence naming the refusal subtests, the residual row `residual: U437` for the preset sessions with its gate (standing order 49); Verification keeps rounds 1 and 2 collapsed to their summary lines and the round-3 pastes in full; `Program-Unit: regime-cutover/U434` last.
6. Commit unsigned on top of 1faa81f1: `fix(router): the patch enables the subagent tool the bundle disables; the updater refuses a non-object dependency table (regime-cutover U434c, round 3 of U434)` with the footer `Program-Unit: regime-cutover/U434`.

ACCEPTANCE
1. Tests (a) and (b) red at 1faa81f1, green at the new head, pasted.
2. The four modules OK at the new head, `Ran N tests` and `OK` pasted.
3. render-check, validate-agent-assets, shfmt, ruff format --check, prettier --check, lint-comparisons on update-agent-assets.sh and hcom-seat, both cmp: exit 0, pasted.
4. `home/dot_dsh/profiles/router/cordis.patch.yml`'s `tool-subagent` row shows `disabled: false`, `provider: acp`, `toolName: subagent`, `maxDepth: provider-managed` (pasted).
5. Tree clean; `git log --oneline 1faa81f1..HEAD` shows the one commit.

VERIFY
ACCEPTANCE pasted into the report; the coordinator pushes, runs the round-3 audit, the sweep and CI, merges, deploys by `make update` in the chezmoi clone, measures `dsh --dump-config` of the deployed profile (the row enabled on `acp`) and the resolve of the package, relaunches the Router and judges row s21 by one subagent turn.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the measured dump of the bundle (dump.txt) for the row's default, the patch algorithm's merge of non-config keys as measured there, and the round-1 real run with the overlay as the proof of the enabled route; it changes one row key and one parser, no grant, no preset row.

TIMEBOX
60 minutes.

FORBIDDEN
No change to acp-broker, acp-seat, hcom-seat, the relay or the record helper; no preset row; no new grant; no pin typed by hand; no edit of `~/.dsh`; no rebase, no amend, no `git stash`; no push; no `gh` call; no network; no pipe `|` in any bash command (standing order 46: outputs under `/tmp/u434c/`); a progress line at `/tmp/dotfiles-wt/U434c-progress.txt` within five minutes and at least every 10 minutes after.

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/.local/state/regime-store/dotfiles/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the program store; you stop at the committed head in the tree. Your final line is the Task return.
- Final report to `/tmp/dotfiles-wt/U434c-report.txt`; the body draft to `/tmp/dotfiles-wt/U434c-pr-body.md`.
- Commit unsigned: `git -c commit.gpgsign=false commit`.

REPORT
Status, the head (40 hex), the ACCEPTANCE lines, deviations. Under 16 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 44, 46, 49); verdicts/U434-1faa81f1.md and verdicts/U434-8c3cfec2.md; briefs/U434b-the-acp-plugin-is-a-declared-dependency-the-updater-installs.md; /tmp/u345/dump.txt and /tmp/u345/overlay.yml; decisions 2026-11-09T06:58:42Z (U406, no preset row).
