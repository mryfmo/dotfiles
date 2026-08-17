# T67e: Checker error-turn diagnostics (gap #4, live-diagnosed)

task_id: T67e
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 3; live gap #4)
depends: T67d (accepted)

[memory: failure — pi-model-access-check gap #4: an API-error turn (message stopReason=error with errorMessage, e.g. subscription quota exhaustion 400) was reported as "assistant response was not exactly OK", misattributing an infrastructure failure as a content mismatch and costing a diagnosis cycle. Error turns must be surfaced as their own failure class with the errorMessage excerpt.]

## Live evidence

claude-fable-5 lane: final message
{"role":"assistant","content":[],"stopReason":"error","errorMessage":
"400 ... You're out of extra usage ..."} -> checker printed
"FAIL json: assistant response was not exactly OK".

## Fix (exact)

1. In both json and rpc lanes: when the final assistant message has
   stopReason=error (or an errorMessage field per the pinned v0.84.1
   message schema — cite lines), report
   `FAIL <lane>: provider/API error: <first 160 chars of errorMessage>`
   instead of the content-mismatch message. Content mismatch reporting
   is unchanged for non-error turns.
2. Tests: fake-pi error-turn mode (exact live shape above) -> the new
   failure class in both lanes; regression: non-error mismatch and
   exact-OK behaviors unchanged.

## Allowed files

- home/dot_local/bin/common/executable_pi-model-access-check
- tests/unit/ (matching module)
- Your artifact paths (T67e five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes;
credential-content access; real pi execution.

## Validation

make format / bash -n / unit-test / validate-agent-assets green; fake-pi
error-mode transcript; scope check.

## Completion / RESULT contract

Five artifacts; memory add (kind=failure); effects=none.
Reply `AGMSG-RESULT v1 task_id=T67e`. max_turns=10.
