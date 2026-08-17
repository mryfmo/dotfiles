# T68: Pi RPC bridge + agmsg integration (π1)

task_id: T68
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-pi-worker-integration.md (Phase 4, incl. the PR #132 review addition: agmsg pi type)
depends: T66 (accepted), T67(e) gate PASSED (openai-codex/gpt-5.6-terra; RPC envelope empirically confirmed)

[memory: decision — Pi workers are driven bus-to-harness: agmsg-pi-worker holds a `pi --mode rpc` child, delivers AGMSG-TASKs as prompt requests, detects completion on agent_end, and never composes worker output itself; the agmsg registration layer accepts the new `pi` runtime type; bridge cwd is enforced to scratch/worktree paths for this plan.]

## Empirically confirmed contracts (build on these, do not re-guess)

- RPC request: `{"id":"<corr>","type":"prompt","message":"<text>"}` ->
  `{"id","type":"response","command":"prompt","success":true}`.
- Event kinds observed live: response, agent_start, turn_start,
  message_start/update/end, turn_end, agent_end (agent_settled may follow
  agent_end — tolerate).
- Extension loading via `--extension <path>` produces fatal startup
  diagnostics on failure (the permgate gate MUST be passed with
  --extension pointing at the deployed ~/.pi/agent/extensions/permgate.ts
  in addition to relying on global discovery — belt and braces; verify
  global discovery also loads it and record which mechanism the bridge
  relies on).

## Allowed files (edit boundary)

- home/dot_local/bin/common/executable_agmsg-pi-worker (NEW bridge, bash,
  shdoc)
- home/dot_agents/skills/agmsg/scripts/ (add the `pi` runtime type to the
  registration whitelist — join.sh and any sibling that validates types;
  existing types byte-identical; shfmt/shdoc style)
- home/dot_agents/agent-config.yaml (OPTIONAL pi experimental section
  under model_profiles ONLY if trivially additive; if the generator or
  validator needs more than a few lines of change to tolerate it, SKIP
  and report — the profile values await the Anthropic operator lane
  anyway; the bridge takes provider/model from env/flags for now)
- home/dot_agents/skills/agmsg-orchestration/SKILL.md (one short
  paragraph: pi worker identity `pi-<profile>-<project-suffix>`, bridge
  usage)
- scripts/validate-agent-assets.py ONLY if a trivial pi-assets addition
  is needed for the new files
- tests/unit/ (matching modules)
- Your artifact paths (T68 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; running
the REAL pi (fake-pi stub only — the orchestrator runs live E2E);
composing RESULT bodies in the bridge; ad-hoc sleep polling loops beyond
the existing agmsg delivery mechanisms; touching claude/codex delivery
configs.

## Bridge spec (fixed)

`agmsg-pi-worker --team <team> --identity <pi-...> --project <path>
[--provider P --model M] [--scratch-root <path>]`:

1. Startup: refuse unless `--project` resolves under the scratch root
   (default: require an explicit --scratch-root and prefix-match; this
   plan-scoped guard stays until T72's ruling). Verify identity via
   existing agmsg scripts (join if absent — now legal with the pi type).
2. Spawn `pi --mode rpc [--provider --model] --extension
~/.pi/agent/extensions/permgate.ts` with cwd=project.
3. Delivery loop: reuse the existing agmsg check-inbox script to fetch
   undelivered messages at (a) startup and (b) each agent_end (turn
   boundary — the Pi analog of the codex Stop hook; this is NOT an
   ad-hoc poll). For each AGMSG-TASK: send one prompt request whose
   message is the raw AGMSG-TASK body plus one fixed instruction line:
   "Execute per the task file; reply on the agmsg bus yourself using the
   send.sh contract; your final assistant text is not the RESULT."
4. Completion: on agent_end for a correlated prompt, log turn completion;
   the RESULT itself must have been sent by Pi via bash (verify nothing
   in the bridge composes or sends RESULT).
5. Failure: child exit/EOF -> send AGMSG-PONG status=blocked
   note=bridge-child-died via send.sh, exit nonzero. AGMSG-PING received
   -> reply PONG alive (bridge-level liveness only).
6. Logging: one line per lifecycle event to stderr; no message bodies
   logged beyond 80-char prefixes.

## Tests (fake-pi stub speaking the confirmed envelope)

(a) startup scratch-guard refusal; (b) task->prompt->agent_end happy
path with correlation; (c) agent_settled after agent_end tolerated;
(d) child death -> blocked PONG + nonzero; (e) PING->PONG; (f) the fixed
instruction line appended exactly once; (g) bridge never calls send.sh
with AGMSG-RESULT (assert on the stubbed send.sh spy).

## Validation

make format / bash -n / shellcheck -x on touched shell / unit-test /
validate-agent-assets green; fake-pi transcripts for (a)-(g); scope
check; join.sh type-addition diff shown with byte-identical existing-type
proof (filtered diff).

## Completion / RESULT contract

Five artifacts (T68 set); memory add with the decision fact;
effects=none. Live E2E-π1 (fresh + /resume restore) is T72,
orchestrator-run. Reply `AGMSG-RESULT v1 task_id=T68`. max_turns=30.
