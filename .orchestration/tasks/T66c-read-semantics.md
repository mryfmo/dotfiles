# T66c: Align the Pi gate's read semantics with the workspace-write baseline

task_id: T66c
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-pi-worker-integration.md (Phase 2/4; second live E2E-π1 finding)
depends: T66b (accepted)

[memory: failure — E2E-π1 round 2: every block was a CORRECT decision under T66b, yet the worker still could not function because T66b gated reads to the workspace — stricter than the established Codex workspace-write baseline (writes workspace-scoped, reads unrestricted). Legitimate out-of-workspace reads (the agmsg SKILL contracts) were denied. Read semantics must be: allow everywhere EXCEPT sensitive-path deny patterns; writes stay workspace-scoped.]

## Live evidence (orchestrator, session 01-27-38 pi-e2e)

Blocked calls: read /Users/mryfmo/.agents/skills/agmsg-orchestration/
SKILL.md; read .../agmsg/SKILL.md; bash compound (pwd && ls && cat ...);
bash echo test. All four correctly matched T66b rules — the rules
themselves are misaligned with worker reality: workers must read
contracts/skills outside cwd. A direct in-cwd read via RPC succeeded,
confirming the mechanism works.

## Fix (exact)

1. permgate pi workspace layer, read tool ONLY: ALLOW any resolvable
   path EXCEPT paths matching a sensitive-path deny list (align with the
   existing suppression families: .env*, *credentials*, id_rsa/ssh keys,
   .ssh/, .aws/, .gnupg/, *.pem, auth.json under ~/.pi and ~/.codex and
   ~/.claude — enumerate exactly in the policy, deny-first). Unresolvable
   paths fall through to ask.
2. write/edit remain workspace-scoped exactly as T66b shipped.
3. bash lane unchanged in this task (send.sh prefix only; the shared
   read-only allow patterns already apply through the common allow layer
   — verify and STATE which bash commands are allow-listed for pi via
   that layer; if `git status` style entries do not flow to pi, wire the
   existing shared allow patterns into the pi path — reference, not
   duplication).
4. Policy: express the read rule declaratively (pi section), not
   hardcoded.
5. Tests: out-of-workspace read of a plain file ALLOW; read of each
   sensitive family DENY-or-ask (deny for the deny-listed); in-cwd write
   still ALLOW; out-of-cwd write still fall-through; claude/codex golden
   byte-parity; extension hash constant update if the extension changes
   (it should NOT need changes — reads already carry path+cwd).

## Allowed files

- home/dot_local/bin/common/executable_permgate
- home/dot_agents/permgate-policy.yaml
- scripts/validate-agent-assets.py (hash constant only if extension
  changes — avoid)
- tests/unit/ (matching modules)
- Your artifact paths (T66c five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; real pi
execution; claude/codex path changes; write/edit scope loosening; bash
lane loosening beyond the stated shared-allow verification.

## Validation

make format / unit-test / validate-agent-assets green; full diff pasted;
scope check.

## Completion / RESULT contract

Five artifacts (T66c set); memory add (kind=failure); effects=none.
Orchestrator redeploys and reruns E2E-π1 (round 3) after acceptance.
Reply `AGMSG-RESULT v1 task_id=T66c`. max_turns=15.
