# AGMSG-TASK dotfiles-T93-gate-masked-feedback-bodies-a01

Drafted 2026-10-04 by the orchestrator seat; follow-up to T68 (PR #246) and T91 (PR #245, merged 312fef3f). Dispatch only after #246 has merged (same file, `scripts/require-crit-review.py`).

## Objective

`collected_feedback_errors()` compares every collected item with `feedback_key()` = (source, url, level, path, line, body), byte for byte. When a Bot comment quotes a key-shaped string (PR #245, thread r4176194980 quoted `…-sk-<20 letters>-review-receipt.md`), the saved `-pr-feedback.json` cannot both match the live collection and pass `validate_no_obvious_secrets()`; the orchestrator had to feed the gate a verbatim copy and save a masked one (T91 acceptance record, receipt `gate_input_note`). Make the two tools agree:

1. In `scripts/require-crit-review.py`, compare bodies after masking with the validator's own masker: load `mask_secret_matches` from `scripts/validate-agent-assets.py` (import by path, as the tests already load the validator) and apply it to the `body` of every collected and every evidence item before building `feedback_key`. Everything else in the identity stays byte-exact. State in the docstring that a masked body is accepted because masking is the repository's documented way to keep evidence scannable and the url still identifies the item.
2. `read_scannable_text()` in `scripts/validate-agent-assets.py` currently skips a file that contains a NUL byte; for `.orchestration/**` text artifacts that is a bypass (T91 audit). Fail the scan with the path and the first NUL offset instead of skipping, for files under `.orchestration/`; other binary detection unchanged. (Confirm first that no committed `.orchestration` file holds a NUL; the T91 round-3 scan reported none.)
3. Tests: `tests/unit/test_require_crit_review.py` — a collected item whose body holds a key-shaped token matches an evidence item whose body has it masked, and an evidence item with a different body still fails; `tests/unit/test_validate_agent_assets.py` — a NUL byte in a `.orchestration/validation/*.md` fixture fails the scan with the offset, a NUL in a non-`.orchestration` binary is still skipped.
4. One sentence in `home/dot_config/claude/rules/pr-integration.md` (and its Codex mirror bullet) saying evidence bodies may be masked with `--mask-secrets`.

Forbidden: any other change to the gate's review-evidence or audit logic; new CLI flags.

[memory:decision] dotfiles-T93 (orchestrator 2026-10-04): the integration gate compares PR-feedback bodies after the validator's secret masking, so saved evidence may be masked; the secret scan fails, rather than skips, an `.orchestration` text file that contains a NUL byte.

## Repo / branch

- Work ONLY in your own worktree. `git fetch origin`; `git switch -c fix/gate-masked-feedback-bodies origin/main` (the commit that merged #246 or later). Verify the dispatched task_rev; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `scripts/require-crit-review.py`, `scripts/validate-agent-assets.py`, `tests/unit/test_require_crit_review.py`, `tests/unit/test_validate_agent_assets.py`, `home/dot_config/claude/rules/pr-integration.md`, `home/dot_config/codex/AGENTS.md` (the PR 統合 gate bullet only)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T93-gate-masked-feedback-bodies-a01.md` (main checkout)

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
uv run python -m unittest tests.unit.test_require_crit_review tests.unit.test_validate_agent_assets 2>&1 | tail -3
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check home/dot_config/claude/rules/pr-integration.md home/dot_config/codex/AGENTS.md
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; wait (≤15 min) for the Codex Bot on that head by listing `gh api repos/mryfmo/dotfiles/pulls/<pr>/reviews --paginate --jq '.[]|select(.user.type=="Bot")|[.commit_id,.submitted_at]|@tsv'`; fix P0/P1 inline findings and repeat; do not resolve threads. The RESULT names every unresolved thread with `fixed:<sha>` or a proposed `not-applicable:<reason>`, and `plan-mode-used=<worktree>` if Plan Mode was used.
3. Artifacts at the exact expected paths; validation with verbatim outputs (masked with `--mask-secrets` where a sample is key-shaped, and say so), PR number, head SHA.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste the exact command and output.
5. `AGMSG-RESULT v1 task_id=dotfiles-T93` via `agmsg-dispatch dotfiles <your identity> claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=25.

## Dispatch

- 2026-10-04 10:40Z to `claude-standard-dot-a005` (worker-c, wT:p2) after its T71 acceptance (PR #249 merged as 65915b93). Branch from `origin/main` 65915b93 or later; `scripts/validate-agent-assets.py` and `scripts/require-crit-review.py` are free (T68, T71 merged). Keep the earlier branches untouched.

## Revise round 1 (orchestrator, 2026-10-04 13:50Z) — task-level audit of dd155f2b is `incorrect`

1. **P2, identity fields.** The masked comparison may apply to `body` and `path` only (a key-shaped file path is the one legitimate reason to mask a path); `source`, `url` and `level` stay byte-exact, as the task said. Adjust `feedback_key(masked=True)` and the test.
2. **P2 (and the Bot thread 4176920521, whose `not-applicable` the audit rejects as "later").** Make the repository secret scan JSON-aware: when a scanned file parses as JSON, scan each string value (and each object key) individually instead of the serialized text, so a body ending in an assignment prefix no longer matches across field boundaries and the documented masked workflow is never blocked by the scan. Non-JSON files keep the text scan. Thread 4176920521 becomes `fixed:<sha>`; the orchestrator re-replies.
3. **P2, object keys.** `mask_json_strings` masks dictionary keys too (a key-shaped member name must not survive), consistent with item 2's key scanning.
4. **P2, evidence.** Paste the pre-change NUL count and the positive-control run (commands and raw output) in the validation file.

One commit for items 1-3 with tests; artifact edit for item 4; `gh pr update-branch 251` if `main` moved; CI; Bot (paginated listing); RESULT. Interleave with T95 as you see fit. Standing directive applies.

## Revise round 2 (orchestrator, 2026-10-04 15:00Z) — task-level audit of aa5b061e is `incorrect`

1. **P2, NUL check after the UTF-16 branch.** In `read_scannable_text`, the UTF-16 BOM decode returns before the NUL rejection, so a BOM-prefixed `.orchestration` artifact with a NUL at offset 2 bypasses the scan. Check for `.orchestration` NUL bytes before any BOM-specific decode (a UTF-16 text file legitimately holds NULs, so for `.orchestration` reject UTF-16 outright: evidence is UTF-8 text). Test: a BOM-prefixed fixture with a NUL and a key-shaped string fails with the offset.
2. **P2, masked key collision.** Two distinct keys that mask to the same name collapse to one member and the earlier value is lost while `--mask-secrets` reports success. Reject the collision (fail with the path and the two original keys) rather than merging; test it.
3. **P3, report.** Update the final-head summary: body and path only are masked (source, url, level, line exact); 781 tests.

One commit for items 1-2 with tests; artifact edit for item 3; `gh pr update-branch 251` if `main` moved; CI; Bot (paginated listing); RESULT. Standing directive applies.
