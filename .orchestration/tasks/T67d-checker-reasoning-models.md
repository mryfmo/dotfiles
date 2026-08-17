# T67d: Checker robustness for reasoning models (gap #3, live-diagnosed)

task_id: T67d
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 3; live gap #3)
depends: T67c (accepted)

[memory: failure — pi-model-access-check gap #3: reasoning models (claude-fable-5) emit a thinking message before the text answer (two message_start/message_end pairs per turn); the checker's single-message assumption read the thinking content, failed the exact-OK match, exited its event loop early, and thereby missed agent_end and the extension confirmation. Assistant text must be taken from the final text message (or agent_end's message list) and the event loop must never exit before agent_end/EOF.]

## Live diagnosis (orchestrator)

`pi -p "Reply with exactly OK" --mode json --provider anthropic --model
claude-fable-5` emits: session, agent_start, turn_start,
message_start/message_end (thinking), message_start/message_end (text),
turn_end, agent_end {messages, willRetry}, agent_settled. The same
checker steps PASS with openai-codex/gpt-5.6-terra (single message).
Plain `pi -p` (print mode) returns exactly `OK` for fable-5.

## Fix (exact)

1. json step: derive the assistant reply from the LAST assistant text
   message of the turn — inspect the pinned v0.84.1 message schema
   read-only to select the correct role/content discrimination (cite
   lines); ignore thinking messages. Alternatively (if simpler and
   schema-supported) read agent_end.messages' last assistant text.
   The exact-OK comparison then applies to that text only.
2. Event loop: never exit before agent_end or EOF; a content mismatch is
   recorded but must not abort parsing (agent_end detection and the
   extension confirmation are independent of the match outcome).
3. rpc step: same last-text-message rule for any text assertions;
   completion remains response.success + agent_end (+agent_settled
   tolerance).
4. Extension confirmation: independent of lane outcomes (runs whenever a
   lane executes; its result reflects only the load signal).
5. Tests: extend the fake-pi with a reasoning-model mode emitting the
   exact double-pair sequence above — json PASS on it; single-message
   regression PASS; mismatch-but-complete run reports FAIL json while
   still PASSing rpc/extension detection.

## Allowed files

- home/dot_local/bin/common/executable_pi-model-access-check
- tests/unit/ (matching module)
- Your artifact paths (T67d five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes;
credential-content access; real pi execution (orchestrator re-runs live).

## Validation

make format / bash -n / unit-test / validate-agent-assets green;
fake-pi reasoning-mode transcripts; scope check.

## Completion / RESULT contract

Five artifacts; memory add (kind=failure); effects=none.
Reply `AGMSG-RESULT v1 task_id=T67d`. max_turns=12.
