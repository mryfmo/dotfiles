# AGMSG-ACCEPTANCE dot-worker-advisor-fable-T26-a01

RESULT 2026-09-27 ~01:4xZ from claude-standard-dot-a005 (worker-c, claude-opus-5-5 high): status=ready_for_review, PR #188 head a63666bb3cbc21f8d5c1cb80e26fe0b450daba56, branch feat/worker-advisor-fable from origin/main 030273d.

## Adversarial review (orchestrator, from origin refs)

- task_rev sha256 match confirmed; worktree clean; base verified to contain T25.
- Diff scope: exactly the 11 allowed files (+192/−15).
- Manifest: standard.claude and deep.claude gain `advisor: fable`; express/review/security/adh, worker_kind, worker_profile, interactive_profile, codex values untouched.
- Generator: optional `advisor` key validated with PROFILE_VALUE_RE (PROFILE_OPTIONAL_KEYS); `--advisor <v>` appended to CLAUDE_ARGS only when set; `advisorModel` emitted after effortLevel only when the interactive profile sets advisor. Generated diff limited to model-profiles.env (STANDARD/DEEP `--advisor fable`) and claude-settings-managed.json (`"advisorModel": "fable"` — equal to the operator's pre-existing manual setting, so no behavior change at apply).
- Validator: worker-profile advisor pinned to `fable` with a truthful message. Side effect honestly disclosed by the worker: `worker_profile` is now effectively required (a missing key fails the pin as None). Accepted — the manifest sets it and the pin is the operator's intent.
- Part B (from the T25 live-E2E findings): after `/exit`, bounded `wait_for_shell_prompt`; on failure one `herdr agent send-keys <pane> Enter` (exit-confirmation dialog), then the existing fail-safe start path unchanged. Legacy `claude-orchestrator` label on the resolved worker pane is repaired via jq-guarded `herdr pane rename` after the ambiguity check and before `/exit`. `attach_panes_are_unambiguous` not weakened.
- Docs (README `--restart-worker` sentence + worker-profile paragraph; model-selection.md advisor bullet) verified against the implementation.
- Tests: generator ×3 (+settings assertion), validator pin ×1 (2 subtests), herdr ×4 with a `process-info` state-file fake; 3 Part B tests fail on the unmodified script (mutation baseline pasted in validation, FAILED failures=3); normal path asserts no stray Enter.
- Evidence: generator --check "up to date", validator ok, 455 unit tests OK (skipped=1), CI 12 checks pass on a63666b, CompactionDB id a7c20de3-85d6-460c-91e4-3264ddefda5e present in pasted output.
- Refutation attempts found no correctness, regression, security, or omission issue.

## Review guard

make require-crit-review satisfied via AGENT_REVIEWED=1 with REVIEW_EVIDENCE=.orchestration/validation/dot-worker-advisor-fable-T26-a01-receipt.md (resolved review-scope approval record r_b9d1e5, exported JSON at .orchestration/validation/dot-worker-advisor-fable-T26-a01-crit.json).

**Decision: ACCEPTED.** Merge #188 --squash (no --delete-branch while worker-c holds the branch); deploy (chezmoi apply both clones); live E2E `herdr-agents --restart-worker` — this run also live-verifies Part B (the worker has a running inbox monitor, so the exit dialog fires) — then verify the worker argv carries `--model claude-opus-5-5 --effort high --advisor fable`.

[memory:decision] T26 accepted 2026-09-27: worker claude launches carry --advisor fable from manifest claude.advisor (validator-pinned); interactive advisorModel rendered from the manifest; --restart-worker confirms the claude exit dialog once and repairs legacy worker-pane labels. PR #188 squash-merged.

cost: n/a (worker report gives no token figures)

### Live E2E addendum (2026-09-27 ~10:5x+09:00, orchestrator)
`--restart-worker` live run: Part B worked (exit-confirmation dialog confirmed, old worker exited; legacy-label repair not needed this time), but the first start failed transiently with herdr `agent_name_taken` — the exited worker's agent registration (`claude-worker-wf`, status Idle) lingered until herdr noticed the process exit. A retry ~10s later succeeded: "Herdr agents worker restarted in pane wF:p2", argv `claude --model claude-opus-5-5 --effort high --advisor fable` (operator requirement verified at process level). Follow-up candidate (small): `--restart-worker` should wait bounded for the stale registration to clear (or reuse it) before `agent start`; recorded in .orchestration/learning/rule_candidates/herdr-worker-relaunch.md.
[memory:failure] --restart-worker can fail transiently with agent_name_taken right after exiting a worker (stale herdr agent registration); bounded wait-for-release before agent start is the fix candidate (2026-09-27).
