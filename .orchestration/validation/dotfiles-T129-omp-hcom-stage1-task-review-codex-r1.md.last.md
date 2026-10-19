Both SHA-256 hashes match, including the final recheck. All 10 premise entries reproduced their recorded output; no-match and missing-file exits were expected. Neither task contains a `design_review` or `invariants` block. Both threat tables cover their declared paths and fixed controls: 19 residual rows each, all exceeding 20 characters; no closed selectors require checking.

Installed versions are **hcom 0.7.30** and **omp 18.11.3**. Help confirms hcom’s launch flags and `send --from`, `--json`, and `--` separator; `-b` specifically means `--from bigboss`. Omp documents `--model` and `--thinking`. No hcom database exists yet, so schema and receipt semantics remain unverified.

[P1] high .orchestration/tasks/dotfiles-T129-omp-config-render-a01.md:92 Item 0b contradicts `D-omp-model-mapping`: following today’s `worker_kind: claude` selects `anthropic/claude-opus-5-5` for `standard`, whereas the operator explicitly selected the worker’s Codex model. Amend this to `standard.omp.model: openai-codex/gpt-6.1-sol`; retain `audit: openai-codex/gpt-6-astra` and `deep: anthropic/claude-fable-5-1`, and test the explicit mapping rather than provider syntax alone.

[P3] high .orchestration/tasks/dotfiles-T129-omp-config-render-a01.md:91 The dangling-symlink statement is stale: the named executable returns `omp/18.11.3`. Replace it with the installed-version evidence and the verified `--model`/`--thinking` flags; distinguish those CLI facts from still-unverified YAML reasoning and alias-resolution behavior.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:99 The specified five-column TSV cannot feed the unchanged consumers. `bus-read.sh:58` and `dispatch.sh:290` parse `●/○ [timestamp] sender → recipient: body`, including receipt state absent from this TSV. Replaying a valid proposed TSV row through the existing jq produces `open: none` and `skipped=1`; dispatch’s regex also rejects it. Define a receipt-bearing history contract and amend both consumers and fixtures; remove item 5’s “jq is unchanged” constraint.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:102 Revise detection uses the wrong field here and in item 6: the existing Message Contract, acceptance records, and `bus-read.sh` use `status=revise`, not `verdict=revise`. As specified, ordinary revise messages bypass the new refusals and do not increase the revise count. Amend both items and their positive/negative fixtures to the existing `status=` contract.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:14 `allowed_files` omits `tests/unit/test_check_regime_boundary.py`, although its setup at lines 58–77 installs an agmsg storage stub and copies only the boundary and counters scripts. Migrating counters to the new sibling reader breaks this fixture. Add this test file and its threat-table row, and permit copying/stubbing the reader in its temporary repository.

[P1] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:109 Stage 1 activates hcom-only sending/history, while hcom seating and worker delivery are deferred until stage 2 **after this PR merges**. Existing seats still receive and return messages through agmsg, so the resulting chain cannot deliver work or observe their results. Keep activation on the current bus until hcom seats and delivery are ready, or make that cutover atomic; specify preservation of in-flight task counters.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:107 The stage allocation loses requirements that plan 023’s classification explicitly transfers to C: `C-58:1` and `C-59:1` appear in neither implementation items nor the deferred list. In particular, C-59’s dispatcher refusal of a revise/amendment without the required S1 re-plan is separate from the deferred worker Stop hook. Assign these requirements explicitly to this stage or a named later stage with acceptance checks.

[P2] high .orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a01.md:115 The 260-line production cap exceeds plan 021 step 7.2’s standing 200-line cap. `D-cap-F4` authorizes 260 only for PR F4, not this task. Record a C-specific exception or split the work, and budget the reader/consumer and fixture corrections above. B’s 170/500 caps introduce no corresponding policy conflict; implementation fit remains unmeasured.

The requested PR #390 overlap command reports:

```text
 scripts/regime-counters.sh            | 17 +++++-----
 tests/unit/test_orchestrator_tools.py | 30 +++++++++++++++++
 tests/unit/test_regime_counters.py    | 62 +++++++++++++++++++----------------
 3 files changed, 71 insertions(+), 38 deletions(-)
```

Review: dotfiles-T129-omp-config-render-a01: revise
Review: dotfiles-T129-hcom-dispatch-bus-a01: revise

📝 まとめ: Completed one read-only review round; no files changed. Live delivery, auth, apply, and test suites were not run; the mapping and bus-contract issues require amendment before activation.