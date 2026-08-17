# T67c: Checker credential-lane precedence (gap #2 from the live Anthropic run)

task_id: T67c
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 3; live gap #2)
depends: T67b (accepted); DISPATCH AFTER T68 completes (sequential regime)

[memory: failure — pi-model-access-check gap #2: providers WITH an env-key mapping (anthropic) never fell through to the subscription lane, so with ANTHROPIC_API_KEY unset but a valid auth.json subscription entry the checker SKIPped although a direct claude-fable-5 round trip succeeded. Lane precedence must be: env var set -> env lane; else auth.json entry -> subscription lane; else SKIP naming both.]

## Gap (orchestrator-verified live)

PI_CHECK_PROVIDER=anthropic PI_CHECK_MODEL=claude-fable-5 ->
"SKIP json/rpc: ANTHROPIC_API_KEY is not set" while
`pi -p ... --provider anthropic --model claude-fable-5` returned OK under
subscription auth.

## Fix (exact)

1. executable_pi-model-access-check: lane selection becomes, per
   provider: (1) documented env var set -> env lane; (2) else auth.json
   contains a valid provider entry -> subscription lane; (3) else SKIP
   naming BOTH lanes. Applies uniformly to all providers (T67b's
   no-mapping case becomes a natural subset).
2. Tests: anthropic-with-authjson-no-env -> subscription lane RUN;
   anthropic-with-env -> env lane (unchanged); neither -> SKIP names
   both; openai-codex behavior from T67b unchanged (regression).
3. Update the operator form's coverage note line accordingly (living
   doc).

## Allowed files

- home/dot_local/bin/common/executable_pi-model-access-check
- tests/unit/ (matching module)
- .orchestration/validation/T67-model-access.md (coverage note line only)
- Your artifact paths (T67c five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes;
credential-content access; real pi execution.

## Validation

make format / bash -n / unit-test / validate-agent-assets green; fixture
transcripts; scope check.

## Completion / RESULT contract

Five artifacts; memory add (kind=failure); effects=none.
Reply `AGMSG-RESULT v1 task_id=T67c`. max_turns=12.
