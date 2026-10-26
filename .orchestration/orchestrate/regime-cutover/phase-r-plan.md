# Phase R: fix the be179c71 audit and close the factory gaps

## Done predicate

1. Each of the 199 findings F001-F199 in `phase-r-assignments.tsv` is closed by a merged unit, or parked with a reason in `gates.md` or `decisions.tsv`. P1 and P2 findings are never parked without the operator's own words (standing order 22).
2. Every unit U64-U85 is merged with a `correct` ledger row for its exact head sha and green CI.
3. Both hosts run the merged head. On macOS: `make update` followed by `make doctor`, with tools=passed and runtime=passed. On Ubuntu: `chezmoi apply --exclude=scripts`, then `update-agent-assets.sh`, then `make doctor` passed. The sudo-only scripts stay with gate G11.
4. The drift watch from U81 has run once on schedule and reported.

The operator may replace this predicate (gate G12).

## Bottleneck and pacing

The audit round is what limits throughput. Each round takes 5 to 10 minutes. A trust-boundary unit has needed 3 to 7 rounds (U60 needed 5, U61 7, U62 7, U63 3). CI takes about 5 minutes, and the coordinator's drains come next. Every unit therefore follows these rules:

- **One contract per unit.** Each brief writes the unit's contract into the PR body and the audit context. This is what stopped the U62 treadmill.
- **Small, file-disjoint units.** Units run in parallel, at most 8 in flight.
- **Workers build in parallel.** Audits run in parallel too, through `codex exec`.
- **P1 first.** The P1 units open wave 1. Urgent CI work (U64) goes before everything else.

## Units and waves

| Unit | Track | Wave | Findings | Content |
| --- | --- | --- | --- | --- |
| U64 | ci | 0 | 1 (P1 1) | Run the macos-14 jobs on macos-15 as well. Gate G10 swaps the ruleset; after that, drop the macos-14 jobs. |
| U65 | install | 0 | 4 (P1 1) | Decide "real CI" from runner-specific variables, never from `CI`. |
| U66 | omp | 1 | 10 (P1 2) | omp seat containment: `--no-extensions`, project config ignored, `debug` and `AskClaude` denied, `omp-run.sh` installed as a pinned lever. |
| U85 | omp | 1 | F004 moved from U66 (P1) | OS-level containment of the yolo omp seats (sandbox-runtime or equivalent), or an operator gate if no containment fits. |
| U67 | omp | 1 | 2 (P1 1) | The bridge ignores a project-level `claude-bridge.json`, and its diag log is bounded. |
| U68 | claude-settings | 1 | 13 (P1 2) | Claude sandbox: credential masks and denies, narrower writable roots, an ask rule for unsandboxed retries, the missing domains, Linux-ignored keys. |
| U69 | claude-settings | 1 | 6 (P1 1) | Prettier runs with `--no-config`. Fix the staleness hook output, the rule frontmatter, the dead `mcp.json`, and the `/commit` command. |
| U70 | codex | 1 | 6 (P1 1) | Trust a plugin hook only at its pinned hash. Fix the PATH, the security profile sandbox, and the leftover files. |
| U71 | orchestrator | 1 | 5 (P1 1) | A merge lever that checks the ledger for the head sha. An audit lever with a scratch `CODEX_HOME`. A generic Program-Unit. Rows for each audit round. |
| U84 | cleanup | 1 | 2 (P2 1) | Remove the unreferenced old-regime records and redact personal data in the tree. Gate G14 decides the history rewrite. |
| U76 | claude-settings | 2 | 8 (P1 1) | One GitHub-write and dangerous-command set in `agent-config.yaml`, rendered to Claude ask, Codex rules and omp policies. Depends on U66, U68 and U70. |
| U72 | lint | 2 | 27 (P2 7) | A lint over one list of retired terms and paths. A single Audit source. Remove the retired references. Depends on U71 and U84. |
| U73 | engine | 2 | 18 (P2 8) | Re-record the pins to the installed versions. Doctor fails on any mismatch. Holds keep live reasons. Depends on U70. |
| U74 | engine | 2 | 20 (P2 5) | Generator, validator and doctor build the expected output set once and compare everything against it (orphans, `.codex-plugin`, omp thinking level, the `CHEZMOI_WORKING_TREE` fix). |
| U75 | engine | 2 | 21 (P2 6) | Standing rules from one source, rendered per agent (omp `RULES.md`, the Codex global contradictions, `pstack-models` managed). |
| U77 | ci | 2 | 10 (P2 4) | A skip allowlist, Dependabot for actions, pinned docs dependencies, timeouts, honest skipped workflows (gate G13), `pull_request_target` readiness. Depends on U64. |
| U78 | install | 2 | 13 (P2 1) | Install and host fixes. Host deletions go to the gate G16 handout. Depends on U65. |
| U80 | kit | 2 | 3 (P2 1) | Skills fixes. |
| U79 | docs | 3 | 30 (P2 5) | Docs accuracy: lists and numbers generated from their sources or linked. Depends on wave 2 and the U72 lint. |
| U81 | engine | 3 | factory | A scheduled drift watch: upstream deprecations and releases, pins against installed versions, and the retired-term lint. It reports as an issue. |
| U82 | tests | 3 | factory | A disposable container that runs `chezmoi apply` and doctor, for agents and CI. |
| U83 | records | 3 | factory | Gate tiering (trust-boundary units get the full audit; other units get one audit plus residual units) and the completion criterion, written in AGENTS.md and the regime SKILL. |

## Gates (see gates.md)

| Gate | Decision | Default |
| --- | --- | --- |
| G10 | Ruleset (admin only): swap the macos-14 contexts for macos-15; add `regime` and `chezmoi-apply` as required checks | None (needs admin). Until then, macos-14 brownouts block merges. |
| G11 | Ubuntu `sudo make update` | Operator runs it later. |
| G12 | Completion predicate | The predicate above. |
| G13 | Workflows that are always skipped (no secrets) | Keep the workflows; make the skip visible and drop the green claims. |
| G14 | Git history rewrite for personal data | No rewrite. Clean the tree only. |
| G15 | Codex and gh credential storage (keyring) | Keep the file store. The U68 sandbox masks and denies cover exposure. |
| G16 | Host cleanups (stale OAuth rows, backups, old tool versions, leftover worktrees) | A handout the operator runs. |
