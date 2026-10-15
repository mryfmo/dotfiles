# Review receipt: dotfiles-T128-project-map-pane-open-a01-review-a01 (round 2)

- reviewer: claude-review-dot-a001 (review seat half; the Codex half runs its first round in parallel)
- previous_receipt: round 1 sha256 `6abc06bbd54cad74386a7d5cb75612350160c901fe817eca75e07541a5b405bc` (revise on `915d7d10`, four findings; overwritten by this file)
- brief: `.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01-review-a01.md` sha256 `972e34c21369538510c1ffb719e9f9f20f2a4ec14d32ba4544444bce492c1caa` (round 1 brief plus a "Round 2" section; nothing else changed, `diff` against the round-1 copy)
- reviewed file: `.orchestration/tasks/dotfiles-T128-project-map-pane-open-a01.md` sha256 `a2c1196e1f0ba873543683f49e89f2d27629d92c2edb3e076e099efc5d81842f` (copied from the main checkout and hashed before reading)
- origin/main at review: `e3006da7` (unchanged since round 1; the Completion's base)

## What changed since round 1 (`diff` of the two copies)

- row 17 and items 1 to 3: the open call gains `--no-merge`; item 3 says the pane is its own, never a tab merged into a neighbouring terminal-browser (finding 3 applied).
- row 21 and item 2: the merged test `test_project_map_reload_hook_acts_only_on_the_map_and_never_fails` changes in one place, its nine empty-selection cases ("no browser", "no map tab", "null target", the five "invalid port" cases, "invalid target") now expect `["ls --all --json", "open <path> --split right --size 0.5 --no-merge"]`; the other hook test stays as it is (finding 1 applied; the nine names match the merged test's table, tests/unit/test_generate_agent_configs.py:1577-1618 on origin/main).
- item 1: the empty selection includes a map tab the jq filter rejects, the branch then opens a second pane, accepted as documented behaviour, the stricter filter stays the hook follow-up's `target-id-validation` row (finding 2 applied); `terminal-browser open` returns when the browser is ready and a second open is otherwise accepted the same way (finding 4 answered).
- premise 2: the command now also counts `--no-merge`; the recorded output is `3`.
- Nothing else changed (the brief's statement holds against the diff; the environment-inputs row 38 is unchanged and still exact, since `--no-merge` adds no variable argument).

## Checks (stop condition 1 to 4)

- premise 1 replayed from the main checkout (`bash -c`): `0` (equal). premise 2 replayed with the user's PATH: `3` (equal); the help text documents `--no-merge` as "Do not open the terminal-browser instance as a tab in a neighbor terminal-browser".
- `task-consistency-check.py` (origin/main copy, sha256 prefix `ba27c4da`, `--root` the main checkout): `dotfiles-T128-project-map-pane-open-a01.md: OK`. `validate-agent-assets.py --mask-secrets` on a second copy: `masked 0 match(es)`, `cmp` equal. Rows: 15 controls, 2 claims.
- the merged hook's behaviour is contradicted by nothing: the new branch sits at today's empty-selection exit (hook line 21), a listing that fails to parse still exits 0 without opening (hook line 20), and item 1 now names every state that reaches the branch. Step 7 form holds: one mechanism, one new test plus one edited expectation in the existing test, two one-sentence prose edits, no renderer or manifest change; caps by construction.
- `allowed_files` unchanged and still covers exactly the four touch points plus the evidence directory. In-flight tasks re-listed: `dotfiles-T128-orchestrator-tools-a05` and `dotfiles-T128-playbook-rules-followup-a01` are merged per their acceptance records; the two chain follow-ups' files are disjoint; the hook follow-up shares the four files and dispatches after this task merges and the boundary, as the brief states.
- the closed row's test name is verbatim in item 2; the four cases of the new test and the nine edited cases of the existing test together close the row's risk (one open call with the event's path and the fixed `--split right --size 0.5 --no-merge` arguments whenever the selection is empty; no open when the map tab is selected; exit 0 and empty output when the open fails; the empty browsers list opens). The environment-inputs row names the open call, the event's path as its only variable argument and the pane of the writing session; the Completion clause is unchanged from round 1 (plan 020 step 4).

## Findings

1. P3 (confidence high, wording only, no change required) `dotfiles-T128-project-map-pane-open-a01.md:69`: "its listed-tab cases keep `["ls --all --json"]`" also covers the merged test's "listing failure" case, which has no tab at all but keeps the same single call because the hook exits before the open (hook line 11); the table makes this unambiguous for the worker.
2. P3 (confidence medium, informational) `dotfiles-T128-project-map-pane-open-a01.md:68`: the READY wait I could find in the installed CLI bundle belongs to its `--ssh` path, so "returns when the new browser is ready" is not confirmed for the local open; item 1's fallback sentence (a second open is accepted the same way) makes the claim non-load-bearing.

Task-file verdict: dotfiles-T128-project-map-pane-open-a01: confirm
