# U274 the use-case test tables of the kit, derived now, judged on macOS first

GOAL
Standing order 41 makes completion a verify-and-fix cycle over use cases derived from each component's official documentation and from the dotfiles' own intent, and standing order 47 (2026-11-06) runs that cycle on the macOS laptop until every row is OK before the same tables run on Ubuntu. Today the store holds one table (`tests/dsh-login-route.tsv`, 60 rows, the DSH login route). This unit derives the rest: one table per use case under `tests/`, every row with a command and an expected output, so the coordinator can judge the macOS column after the operator's `make update` and a fix unit can be opened for every NG. Rows for components not yet built (dsh-superagent intake, e2e) are written as `not-started` rows, not left out.

SCOPE
A scratch tree `/tmp/dotfiles-wt/U274` (a worktree of `origin/main`, for reading and for running the rows that run inside the repository). You write the tables and the derivation note under `/tmp/dotfiles-wt/U274-tables/` (never into the store `~/Workspace/dotfiles/.orchestration/`, which the coordinator writes). Not: any repository file, any host file, any credential.

CONTEXT
The goal sentence (frame row of 2026-11-06T03:31:38Z; `handoff/08-purpose-and-goal.md` line 5, read that file whole): omp lowest, DSH workflow control, dsh-superagent intake (Slack, Outlook, Teams, GitHub), everything under the Anthropic sandbox, graphify, security skill, e2e, knowledge-work, both hosts, autonomous drive of other projects. Sources, in this order of authority: the official documentation of each component as pinned in the repository (`home/dot_agents/agent-config.yaml` is the manifest naming each asset's source, ref and commit; `docs/*.md` hold the kit's own component documents; `scripts/orchestrator/README.md` the levers), then the dotfiles' intent (`README.md`, `AGENTS.md`, the manifest's audience and purpose rows). Where a component's official documentation is not in the tree (omp, srt, DSH, dsh-superagent, graphify, security-audit-skill, e2e, knowledge-work-plugins, hcom, GitHub rulesets and Actions), fetch it read-only from the upstream named in the manifest at the pinned ref and cite URL plus path and line, as the existing table cites `dsh docs: packages/llm/llm/src/types.ts:470-475`. The existing table is the form (`tests/dsh-login-route.tsv`: `id use_case source kind command expected observed verdict ts`); this unit adds a `host` column after `kind` (values `macos` and `ubuntu`; you write `macos` rows only, the Ubuntu rows are derived by the coordinator when the macOS column is all OK).

DATA SHAPE
One TSV per use case, 10 columns (`id use_case source kind host command expected observed verdict ts`), tab-separated, no tabs or newlines inside a cell, one header row. `kind` is one of `auto` (a command that judges itself inside the repository tree, such as a unit test or `node --test` row), `host` (a command that needs the deployed kit on the laptop, such as `hcom list -v` or a seat launch), `operator` (a step only the operator can perform, such as a Keychain login or an account creation), `not-started` (the component is not built; the row names the plan item M-xx and the use case it will cover). `verdict` is `OK`, `NG` or `pending`; you run and fill `auto` rows now, and leave `host`, `operator` and `not-started` rows `pending` with `observed` empty. Each use case covers the facets of order 41: the normal path, the refusal path, a boundary, zero-touch (no human in the loop), and the both-hosts facet is the `host` column. Target: every clause of the goal sentence has at least one table, and the last clause (one change of another project flows from intake to merge with no human) is one use case whose rows are the ladder from intake to merge.

CHANGE
1. The derivation note `U274-tables/00-derivation.md`: the clause to use-case map (clause, use case file, sources with their pinned refs), and the facets each table covers; under 80 lines.
2. The tables, one per use case, named `<clause>-<use-case>.tsv` (for example `omp-seat-launch.tsv`, `dsh-workflow-turn.tsv`, `sandbox-write-denies.tsv`, `graphify-asset.tsv`, `security-sweep-gate.tsv`, `e2e-required.tsv`, `kwp-skills-visible.tsv`, `autonomous-change-flow.tsv`); the existing `dsh-login-route.tsv` is not rewritten, its rows are referenced by id where a new table would repeat them.
3. Run every `auto` row in your worktree and fill `observed`, `verdict`, `ts`; a row that fails is `NG` with the output in `observed`, not deleted and not rewritten to pass.
4. A check script `U274-tables/check-tables.py` (stdlib only, run with `python3 -I`) that refuses a table with a wrong column count, a tab or newline inside a cell, a `kind` or `host` or `verdict` outside the sets above, an `auto` row left `pending`, or a `not-started` row without an `M-` item in `expected`; paste its output over all tables.

ACCEPTANCE
1. `python3 -I U274-tables/check-tables.py U274-tables/*.tsv` exit 0 and its row counts per table pasted.
2. Every clause of the goal sentence appears in `00-derivation.md` with at least one table; the two unbuilt clauses have `not-started` rows naming M-26, M-27, M-18 (intake) and M-16 (e2e).
3. Every `source` cell names a document and a path or URL with a line or anchor; a `grep -c` of rows whose `source` is empty prints 0 per table.
4. The `auto` rows' pass and fail counts pasted per table, with the command of each NG.
5. `wc -l` of every table pasted; total rows between 80 and 240.
6. `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0 with `00-derivation.md` and the check script's docstring among the files (the note is synced into the repository's store by the next records sync, where CI's prettier runs on it).
7. `uv run python -m unittest tests.unit.test_brief_check` OK in the worktree: the brief gate the `brief-real` rows judge against is the one under test, unchanged (added 2026-11-06T12:1xZ after main's brief-check refused this brief for naming no gates; the f5 row of `autonomous-change-flow.tsv` recorded that refusal).

VERIFY
The coordinator copies the tables into the store's `tests/`, runs the `host` rows after the operator's `make update`, and opens one fix unit per NG. The Ubuntu rows are derived from the macOS rows when the macOS column is all OK (order 47).

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the manifest's pinned refs as the version of each component's documentation and the goal sentence as the clause list; it changes no repository file, reads no credential and writes nothing outside its scratch directories.

TIMEBOX
90 minutes.

FORBIDDEN
No write under `~/Workspace`, `~/.dsh`, `~/.omp`, `~/.agents`, `~/.local`; no edit of any repository file (the worktree is read and run only); no `gh` call; no push; no `make update`; no seat launch; no `/v1/messages` request; network only as read-only fetches of the official documentation named in the manifest (cite each URL); no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u274/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 60)
- Never run git write commands or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop with the tables under `/tmp/dotfiles-wt/U274-tables/` and the coordinator copies them.
- Progress line at `/tmp/dotfiles-wt/U274-progress.txt` every ten minutes at most; the derivation note within twenty minutes. Write your final report to `/tmp/dotfiles-wt/U274-report.txt` before you end.
- Comments explain a non-obvious why only, no phase narration.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Build the Lever: the check script is the artifact the coordinator reruns; Test Behavior, Not Implementation: a row asserts what the user of the kit observes).

REPORT
Status, the table list with row counts, the auto pass and fail counts, the clauses with no row beyond `not-started`, the ACCEPTANCE result lines, deviations. Under 16 lines, ending with `head=<40 hex>` (the origin/main sha your worktree is at).

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `AGENTS.md` (Test Policy); `handoff/08-purpose-and-goal.md` §1 and §3; `tests/dsh-login-route.tsv` as the form.
