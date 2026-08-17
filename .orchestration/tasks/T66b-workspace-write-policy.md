# T66b: Workspace-write policy for the Pi gate (E2E-π1 live finding)

task_id: T66b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 2/4 junction; live design gap)
depends: T66, T68 (accepted)

[memory: failure — Live E2E-π1 proved the fail-closed gate and the RPC worker are incompatible as shipped: the pi worker's session recorded four "blocked by policy" tool results, no file was written, and no RESULT was sent — non-interactive ask->deny blocks ALL productive work. The fix is deterministic workspace-write semantics (Codex sandbox philosophy): in-workspace file tools and the exact agmsg send.sh command are policy-ALLOWED; everything else keeps ask->deny.]

## Live evidence (orchestrator)

Session 2026-08-17T01-01-26 ... pi-e2e: 13 entries, 4x "blocked by
policy", hello.txt never created, no RESULT on the bus; bridge/join/
prompt/turn machinery all functioned correctly.

## Fix (exact)

1. Extension (home/dot_pi/agent/extensions/permgate.ts): include the
   session cwd in the normalized action JSON sent to `permgate pi`
   (field `cwd`); also send `path` resolved as given (no resolution in
   the extension — permgate decides).
2. permgate pi provider (executable_permgate): add a deterministic
   WORKSPACE layer evaluated between deny and allow patterns, pi
   provider only:
   - tools write/edit/read: ALLOW iff the realpath-resolved path (against
     cwd; reject on resolution failure) is strictly under cwd
     (prefix-match after normalization, `..` escapes rejected) AND cwd is
     non-root. Outside-cwd -> fall through (ask -> deny in RPC).
   - tool bash: ALLOW iff the command, after trimming, begins with the
     exact expanded prefix `<home>/.agents/skills/agmsg/scripts/send.sh `
     followed by arguments containing NO shell metacharacters
     (`; | & $ \` > < (`) — the worker's RESULT lane; everything else
     unchanged.
   - Existing deny patterns keep absolute precedence (a denied pattern
     inside cwd is still denied).
3. Policy file (permgate-policy.yaml pi section): add a
   `workspace_write: true` switch so the layer is explicit, default true
   for pi, absent/false for claude/codex (their harnesses have native
   permission systems — no behavior change; pin by golden test).
4. Tests: in-cwd write/edit/read ALLOW; `..` escape and absolute
   outside-path fall through to deny; send.sh exact-prefix ALLOW;
   send.sh with `;` injection -> not allowed; arbitrary bash still deny;
   catastrophic deny precedence inside cwd; claude/codex outputs
   byte-identical (golden); extension sends cwd (argv/stdin assert).
5. Update the SHA-256 integrity constant for the changed extension.

## Allowed files

- home/dot_pi/agent/extensions/permgate.ts
- home/dot_local/bin/common/executable_permgate
- home/dot_agents/permgate-policy.yaml
- scripts/validate-agent-assets.py (hash constant only)
- tests/unit/ (matching modules)
- Your artifact paths (T66b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; real pi
execution; ANY claude/codex decision-path change; weakening deny
precedence; LLM classifier enabling.

## Validation

make format / bash -n / unit-test / validate-agent-assets green (+ ts
check per T66 choice); full diff of the permgate workspace layer pasted;
scope check.

## Completion / RESULT contract

Five artifacts (T66b set); memory add (kind=failure) with the fact
above; effects=none. Orchestrator re-runs E2E-π1 live after acceptance.
Reply `AGMSG-RESULT v1 task_id=T66b`. max_turns=20.
