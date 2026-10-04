# dotfiles-T68-gate-audit-evidence-a01 — report (status: ready_for_review)

Worker: `claude-standard-dot-a006` (Claude Code, `standard`), worktree `.claude/worktrees/worker-d`.
PR: https://github.com/mryfmo/dotfiles/pull/246 — branch `feat/gate-audit-evidence` from `origin/main` 138e6a72.

Commits:
- `abf9933f` task
- `83074eea` review fix 1
- `22efc32c` review fix 2
- `46f14681` review fix 3
- `3ba270d6` `gh pr update-branch` merge of main 8922f13b (#247)

Final head `3ba270d66778dab382e9cb055f55199e6d6c328d`:
- CI all pass (nix skipped);
- up to date with `origin/main` 8922f13b;
- `mergeable_state` = `blocked` while Codex threads are unresolved; threads were not resolved, per the task.

Task file revisions verified with `sha256sum` (outputs in validation, "Task file revision verification"):
- `3959867c…` (dispatch)
- `fcbe596a…` (PONG decision 1)
- `9e175902…` (revise round 1)
- `de14890f…` (revise round 2)

PONG decision 2 (`7d991601…`) was taken from its dispatch message and not hashed; this corrects the earlier claim.

## What the gate does now (`scripts/require-crit-review.py`)

`make require-crit-review` with `BASE` additionally runs `audit_errors(root, head, task)` when the change needs review and not every changed path is under `.orchestration/`. The failure output lists the review triggers and the audit errors together.

- **Env:** `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS`, as constants next to `PR_FEEDBACK_EVIDENCE`. No new CLI flags; `--base` help mentions the requirement.
- **Location:** `AUDIT_EVIDENCE` must be repo-local under `.orchestration/validation/`, checked on the given and the link-resolved path. This is `feedback_path_error`'s rule, via the new `orchestration_path_error`; the PR-feedback code is unchanged.
- **Name:** `<task>-audit-<sha7..40>.md`, checked on both names. `<task>` must equal the `<task>` of `PR_FEEDBACK_EVIDENCE`'s `<task>-pr-feedback.json`, and `HEAD` must start with the sha.
- **Verdict source:** the same as `herdr-agents`.
  - `<file>.last.md` when it has non-blank content; the companion must also pass the repo-local `validation/` check.
  - Otherwise only the transcript's final `codex` block. That is a port of herdr-agents' awk: text after the last line that is exactly `codex`, skipping the `tokens used` footer and a bare count.
  - The verdict is the last non-blank line, matched against `^\s*Verdict: (correct|incorrect|blocked)\s*$`.
- **Outcomes:**
  - `correct` passes.
  - `blocked` or missing fails.
  - `incorrect` needs at least one `[P0-P3]` finding (a Markdown list marker is allowed) in the verdict source. It also needs `AUDIT_DISPOSITIONS` under `.orchestration/acceptance/`, with exactly one `audit-finding: <n> … not-applicable:<reason ≥ 20 chars>` line per finding, numbered 1..N in audit order. Duplicate, unnumbered or out-of-range lines are errors. A `fixed:` is rejected because it moves `HEAD` and needs a fresh audit. This reuses `PR_FEEDBACK_DISPOSITION` and `FAILURE_REASON_MIN_CHARS`.

Rule text:
- `home/dot_config/claude/rules/pr-integration.md` has one new bullet.
- `home/dot_config/codex/AGENTS.md` gate bullet is the Japanese mirror, added per PONG decision 1.

Both show `herdr-agents --audit <head-sha> --task <task>`, the same-task binding, the numbered dispositions and the `.orchestration`-only exemption.

GNU make passes `AUDIT_*` from the environment or the command line to the recipe, so no Makefile change was needed; probe pasted in validation.

## Tests (`tests/unit/test_require_crit_review.py`, 69 pass)

- new helper `audit_guard`;
- missing evidence, with the trigger reason still printed;
- a correct audit;
- wrong sha, other task, outside `validation/`, and a bad name;
- `.last.md` precedence, including an empty `.last.md`, and a `.last.md` symlink outside the repo;
- transcript fallback reading only the final codex block (quoted `Verdict: correct` ignored; a later codex block overrides; the footer is skipped);
- blocked and missing verdicts;
- `incorrect` with no, `fixed:`, short-reason, missing, unnumbered-repeat, duplicate, out-of-range and complete dispositions;
- `incorrect` without findings;
- `.orchestration`-only PRs (one file, and five files with a broad diff).

The existing `--base` tests are unchanged: their success cases are docs-only, so no review is required.

## Codex review threads and proposed dispositions

| Thread | Head | Finding | Disposition |
| --- | --- | --- | --- |
| 4175944623 P1 | abf9933f | repeated generic dispositions counted per finding | `fixed:83074eea` |
| 4175944624 P2 | abf9933f | Codex AGENTS.md gate bullet | `fixed:83074eea` (scope added in PONG decision 1) |
| 4175944626 P2 | abf9933f | bulleted findings not counted | `fixed:83074eea` |
| 4175944628 P2 | abf9933f | broad `.orchestration`-only PR asked for audit | `fixed:83074eea` |
| 4175981346 P2 | 83074eea | root AGENTS.md:51, SKILL, gh-first-workflow, Makefile comment | `not-applicable:` T69 rewrites those recipes (PONG decision 2) |
| 4175981351 P2 | 83074eea | audit not bound to the feedback task | `fixed:22efc32c` |
| 4176028652 P2 | 22efc32c | rule omits `--audit <sha> --task <task>` | `fixed:46f14681` |
| 4176028656 P2 | 22efc32c | `.last.md` symlink outside the repo | `fixed:46f14681` |
| 4176028658 P2 | 22efc32c | transcript fallback read the whole transcript | `fixed:46f14681` |

Final head 3ba270d6: no new review or inline comment. The Codex Bot reacted `+1` at 2026-10-04T03:58:27Z, after the 46f14681 push and the update-branch.

## Reporting notes

- **Verdict-source deviation.** The task says to use `.last.md` "if it exists". The gate uses it only when non-blank, and otherwise uses the transcript's final codex block, mirroring herdr-agents exactly, so the gate and the audit tab cannot disagree.
- **Disposition format.** The disposition line format now requires a finding number (`audit-finding: <n> …`). This addition is needed for the P1 fix, and both rule mirrors document it.
- **Diff sizing.** `is_ignored` still excludes only the PR-feedback JSON from diff sizing. The learning file covers the untracked-audit-transcript sizing point; the shared sizing logic was not changed, as the task forbade.
- **Not run:** the real gate against a live PR, which is orchestrator-side.

[memory:decision] dotfiles-T68 (operator 2026-10-03): `make require-crit-review` with BASE requires `AUDIT_EVIDENCE=<.orchestration/validation/<id>-audit-<sha7>.md>` whose sha matches HEAD and whose last `Verdict:` is `correct`, or `incorrect` with every finding dispositioned `not-applicable` in the acceptance record (`AUDIT_DISPOSITIONS`); `.orchestration`-only PRs are exempt.

CompactionDB, run in the main checkout outside the sandbox:

```
$ cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "dotfiles-T68 (operator 2026-10-03): \`make require-crit-review\` with BASE requires \`AUDIT_EVIDENCE=<.orchestration/validation/<id>-audit-<sha7>.md>\` whose sha matches HEAD and whose last \`Verdict:\` is \`correct\`, or \`incorrect\` with every finding dispositioned \`not-applicable\` in the acceptance record (\`AUDIT_DISPOSITIONS\`); \`.orchestration\`-only PRs are exempt."
5a73b2dc-d0e5-42aa-b935-87078b55547a
$ python3 .claude/hooks/contextdb_cli.py memory search dotfiles-T68
5a73b2dc-d0e5-42aa-b935-87078b55547a [project/decision] dotfiles-T68 (operator 2026-10-03): `make require-crit-review` with BASE requires `AUDIT_EVIDENCE=<.orchestration/validation/<id>-audit-<sha7>.md>` whose sha matches HEAD and whose last `Verdict:` is `correct`, or `incorrect` with every finding dispositioned `not-applicable` in the acceptance record (`AUDIT_DISPOSITIONS`); `.orchestration`-only PRs are exempt.
```

cost: n/a (the Claude Code runtime does not expose per-session token or cost figures to the worker)

## Revise round 1 (task_rev 9e175902…): task-level audit of 3ba270d6 was `incorrect`

Fix commit `5168613a` `fix(review-gate): take the audit verdict only from the audit's own last message`. The final head is `5168613a5ea297cbe7a101cedb055986bd64c5b2`. CI is all pass (nix skipped). `origin/main` = 8922f13b, and the branch is up to date with it.

1. **P1, companion symlink to another task's or an older audit.** The new `audit_name_error(name, head, task)` is shared by the audit file and its companion.
   - The resolved `.last.md` must be named exactly `<audit>.md.last.md`, and its stripped name must pass the same task and HEAD-sha-prefix check.
   - Tests: a companion symlinked to `other-audit-abcdef0.md.last.md` or to `test-audit-0000000.md.last.md` inside `validation/` fails with "resolves to …; it must be this audit's own last message". A companion symlinked outside the repo still fails the location check.
2. **P1/P2, transcript fallback and empty `.last.md`.**
   - The gate now requires `<audit>.md.last.md` with non-blank content and reads the verdict only from it; a missing or empty companion is "verdict is missing … re-run the audit".
   - `final_codex_block` and its tests are deleted (`grep -c` in the head file = 0).
   - Both rule mirrors say the verdict is taken only from `<file>.last.md`, which must exist with content.
3. **P3, evidence.** The validation file and this report now show the CompactionDB command exactly as run, with the verbatim `--content`, UUID `5a73b2dc-d0e5-42aa-b935-87078b55547a`, and the `memory search dotfiles-T68` output.

Checks:
- Guard tests: 68 pass, run from `git archive 5168613a`.
- `make unit-test`: 710 OK.
- `make validate-agent-assets`: ok.

Codex Bot on 5168613a raised one new P2, 4176238899: "restore the audit runner's transcript fallback". Proposed disposition: `not-applicable:` this round's decision deliberately removed the gate's transcript fallback, because it accepted quoted repository text as a verdict (audit P1). herdr-agents may keep its own display fallback, but the gate requires codex's final message (`.last.md`). An audit whose `codex exec -o` wrote no final message must be re-run, not accepted from the transcript.

The orchestrator has already replied on the earlier nine threads (fixed: 83074eea ×4, 22efc32c, 46f14681 ×3; not-applicable to T69 ×1).

## Revise round 2 (task_rev de14890f…): evidence corrections only

The head stays `5168613a`: no commit, no push.
1. The learning note's item 1 described the removed `.last.md` transcript fallback. It now records that the gate reads the verdict only from a non-blank `<audit>.md.last.md`, and why: the transcript fallback accepted quoted text.
2. The validation file gains "Task file revision verification", with a fresh `sha256sum` of the current task file (`de14890f…`, matching the dispatch) and the earlier verifications cited verbatim from the session log (`3959867c…`, `fcbe596a…`, `9e175902…`). PONG decision 2 (`7d991601…`) is stated as not hashed. The revision line at the top of this report was corrected to match.
