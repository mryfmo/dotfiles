# T74: Pi source removal + surgical mixed-file edits + pi->cli lane rename

task_id: T74
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: .orchestration/tasks/PLAN-pi-pivot.md (Phase 1)
analysis: .orchestration/analysis/pi-pivot-decision.md (inventory §2 — FOLLOW IT EXACTLY; any hunk not classified there -> ask via agmsg)

[memory: decision — Pi is removed as a third agent per operator ruling; the permgate machine-readable lane survives renamed pi->cli with its workspace-write, strict-resolution, and sensitive-read machinery intact, and every shared-asset hunk (send.sh SQL safety, trusted-runtime codex receiver, shdoc conversions) is retained.]

## Work order

1. Delete every file in inventory §2a (pure Pi): home/dot*pi/\*\*, the three
   executables (agmsg-pi-worker, pi-model-access-check,
   pi-session-evidence), tests pi*_.test.mjs / pi\___types.d.ts /
   test_pi_\*.py / test_agmsg_pi_worker.py / fixtures/pi_sessions/\*\*.
   Do NOT touch home/dot_mise (T75 orchestrator chore).
2. Surgical edits per §2b:
   - executable_permgate + permgate-policy.yaml + test_permgate.py:
     rename provider `pi` -> `cli` (mechanism byte-preserved otherwise;
     claude/codex goldens must stay byte-identical — regression test).
   - join.sh: remove the `pi` type from the whitelist and usage strings
     (restore pre-#134 wording for those lines).
   - whoami.sh: keep the shdoc conversion; remove pi-type documentation.
   - check-inbox.sh: remove the bridge-only env controls; keep shdoc.
   - SKILL.md: remove the pi-worker paragraph.
   - validate-agent-assets.py (+ its tests): remove the pi-assets
     category entirely.
3. Repo-wide residue check: `grep -riE '\bpi\b' home scripts tests`
   filtered to non-historical references — justify every remaining hit in
   the report (e.g. unrelated words); zero unjustified references.
4. Gates: make format / unit-test / validate-agent-assets / shellcheck on
   touched shell. List every DELETED test by name in the validation
   artifact (no silent count shrink).

## Allowed files

Everything named in inventory §2a/§2b plus tests/unit and your artifact
paths. FORBIDDEN: home/dot_mise/**, vendor/**, anything in §2c (shared
assets), .orchestration history.

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; touching
§2c shared-asset hunks; runtime teardown (T75).

## Completion / RESULT contract

Five artifacts (T74 set); memory add with the decision fact;
effects=none. Reply `AGMSG-RESULT v1 task_id=T74`. max_turns=25.
