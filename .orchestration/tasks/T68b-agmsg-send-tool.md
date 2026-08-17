# T68b: First-class agmsg_send tool for Pi workers (root fix for the RESULT lane)

task_id: T68b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 2/4; E2E rounds 3-4 root cause)
depends: T66d, T68 (accepted)

[memory: decision — Pi workers send bus messages through a first-class extension-registered agmsg_send tool (typed params, argv-array spawn of send.sh, from-identity pinned to the worker's own), replacing the string-prefix bash lane, which is removed; models compose tool calls reliably where they fail at exact command strings.]

## Root cause (two live rounds)

Round 3: model used `~/` form -> prefix mismatch (fixed by T66d).
Round 4: model wrapped in `/bin/bash -lc '...'` -> mismatch again.
String-prefix gating of a model-composed command is an arms race; the
correct design is a dedicated tool.

## Fix (exact)

1. NEW extension home/dot_pi/agent/extensions/agmsg.ts:
   - `registerTool` `agmsg_send` with typed params {team: string,
     to: string, body: string} (from is NOT a parameter — see 3).
   - Implementation: spawn
     `<home>/.agents/skills/agmsg/scripts/send.sh` with an ARGV ARRAY
     [team, from, to, body] via execFile (no shell), 10s timeout;
     tool result = one line success/failure.
   - promptSnippet/promptGuidelines (per the pinned registerTool schema —
     cite lines): state that AGMSG-RESULT messages must be sent with this
     tool.
2. `from` identity: the extension reads env `AGMSG_PI_IDENTITY` (set by
   the bridge) and uses it as `from` unconditionally. Empty/unset ->
   tool returns an error (never guesses).
3. Bridge (executable_agmsg-pi-worker): export AGMSG_PI_IDENTITY to the
   pi child; add `--extension ~/.pi/agent/extensions/agmsg.ts` alongside
   permgate.ts; update the fixed instruction line to
   "send your AGMSG-RESULT using the agmsg_send tool".
4. permgate pi: REMOVE the bash send.sh prefix lane (T66b/T66d) entirely
   — the bash lane returns to pure ask/deny + shared allows; add a
   deterministic ALLOW for toolName `agmsg_send`... NO — simpler and
   safer: the permgate extension only gates bash/read/write/edit;
   agmsg_send is a different tool name and is not gated (document this
   explicitly in the extension comment and the report: the tool's safety
   comes from its constrained construction, not from permgate).
5. Update SHA-256 integrity constants for changed/new extensions; tests:
   tool registered with the pinned schema shape; argv-array spawn
   asserted (no shell); missing identity -> error; success/failure
   results; permgate bash lane no longer matches send.sh (regression:
   send.sh via bash now falls through to ask); goldens intact.

## Allowed files

- home/dot_pi/agent/extensions/agmsg.ts (NEW)
- home/dot_pi/agent/extensions/permgate.ts (only if the send.sh lane
  removal touches it — the lane lives in executable_permgate; avoid
  extension changes if possible)
- home/dot_local/bin/common/executable_permgate (remove the send.sh
  prefix lane)
- home/dot_local/bin/common/executable_agmsg-pi-worker (env + extension
  flag + instruction line)
- home/dot_agents/permgate-policy.yaml (remove the lane's policy bits if
  any)
- scripts/validate-agent-assets.py (hash constants)
- tests/unit/ (matching modules)
- Your artifact paths (T68b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; real pi
execution; claude/codex path changes; gating-scope changes beyond the
stated lane removal.

## Validation

make format / bash -n / unit-test / validate-agent-assets green
(+ts check); full diffs pasted; scope check.

## Completion / RESULT contract

Five artifacts (T68b set); memory add with the decision fact;
effects=none. Orchestrator redeploys and runs E2E-π1 round 5.
Reply `AGMSG-RESULT v1 task_id=T68b`. max_turns=20.
