# T67b: Model-access checker — subscription-auth lane (gap found in live run)

task_id: T67b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 3; live gap)

[memory: failure — pi-model-access-check only recognized env-key providers and SKIPped subscription-auth providers (auth.json), so the real openai-codex lane could not be exercised by the checker; the orchestrator had to run the round trip manually. Credential presence checks must cover both lanes.]

## Gap (orchestrator-verified live)

With PI_CHECK_PROVIDER=openai-codex the checker printed
"SKIP json/rpc: provider openai-codex has no documented single-key
mapping" although valid subscription credentials existed at
~/.pi/agent/auth.json, and a manual round trip succeeded (print `OK`;
RPC envelope agent_start...agent_end/agent_settled with request shape
{"id","type":"prompt","message"}).

## Fix (exact)

1. executable_pi-model-access-check: add a subscription lane — when the
   selected provider has no env-key mapping, check (read-only, no
   contents printed) that ~/.pi/agent/auth.json exists, is valid JSON,
   and contains an entry for the provider (verify the auth.json layout
   against the pinned v0.84.1 source read-only; cite lines). If present,
   RUN the json and rpc steps; if absent, SKIP with a message naming
   BOTH lanes ("set <ENV> or run /login for <provider>").
2. Encode the now-confirmed RPC request shape
   {"id","type":"prompt","message":...} and completion detection on
   agent_end (with agent_settled tolerated after) — replacing any guessed
   shape; cite this task's live confirmation in a comment.
3. Extension-step prerequisites update accordingly (runs when either
   credential lane is available).
4. Tests: fake-pi + fake auth.json fixtures — subscription lane PASS,
   missing-entry SKIP naming both lanes, malformed auth.json treated as
   absent (SKIP, never crash, never print contents); env lane unchanged.

## Allowed files

- home/dot_local/bin/common/executable_pi-model-access-check
- tests/unit/ (matching module)
- .orchestration/validation/T67-model-access.md (append a one-line note
  that the checker now covers subscription auth; keep existing results)
- Your artifact paths (T67b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; printing
or copying credential contents; real pi execution (fake-pi only; the
orchestrator re-runs the real lane after acceptance).

## Validation

make format / bash -n / unit-test / validate-agent-assets green; fixture
transcripts; scope check.

## Completion / RESULT contract

Five artifacts (T67b set); memory add with the failure fact;
effects=none. Reply `AGMSG-RESULT v1 task_id=T67b`. max_turns=15.
