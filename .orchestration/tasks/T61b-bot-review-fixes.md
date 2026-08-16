# T61b: Root-cause fixes for PR #128 bot review findings

task_id: T61b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot
plan: PLAN-harness-composability-integration.md (Phase 7; PR #128 review)

[memory: decision — Parameterized install steps record per-identity manifest keys (function:identity) so no invocation overwrites a sibling's record, and an existing-but-unreadable installed-manifest is a doctor ERROR, never silently treated as empty.]

## Findings (chatgpt-codex-connector, both P2, orchestrator-triaged as REAL)

1. `ensure_mise_npm_agent_cli` records under ONE manifest key for BOTH the
   Claude and Codex CLI repairs; T57's wholesale-replacement semantics
   mean the second invocation in a single run erases the first CLI's
   paths/identity, so remove-agent-asset and doctor repair cannot account
   for it (scripts/update-agent-assets.sh:87 area).
2. check-agent-runtime.py treats an EXISTING but truncated/invalid/
   wrong-schema `.installed-manifest.json` as empty, so doctor can omit
   every manifest-managed finding and report healthy
   (scripts/check-agent-runtime.py:309 area).

## Fix (exact, root-cause)

1. Parameterized step keys:
   - manifest_record gains support for a step key of the form
     `<function>:<identity>` (e.g. `ensure_mise_npm_agent_cli:claude`,
     `...:codex`). Only parameterized steps use the suffix; the other
     ten single-identity steps keep bare function-name keys (T57 pinning
     amended by this ruling — note it in the report).
   - update-agent-assets.sh: the mise-CLI step records under its
     per-identity key.
   - remove-agent-asset: resolves steps generically from manifest keys
     (verify it already does; if its kind=plugin/mise inverse parses the
     identity, the explicit key suffix should REPLACE suffix-guessing
     from commands where applicable — simplify, don't duplicate).
   - doctor REPAIR step-scoped rerun: when a manifest key carries
     `:identity`, invoke the base function with that identity argument;
     the whitelist matches on the base function name.
   - STALE suggestions print the full parameterized key.
2. Manifest integrity:
   - check-agent-runtime.py: absent manifest -> unchanged (optional);
     existing but unreadable/invalid JSON/wrong `version`/non-object
     `steps` -> one ERROR finding
     (`installed manifest unreadable or invalid: <path> (<reason>)`),
     and manifest-dependent checks are SKIPPED (not silently passed) for
     that run.
   - remove-agent-asset: same condition -> error exit 1 (never treat as
     empty). Verify current behavior and pin.
3. Tests: same-run double-record of both identities preserves both
   entries; parameterized-key removal round-trip; REPAIR rerun with
   identity suffix invokes base function with the argument; corrupted
   manifest -> doctor ERROR + skipped manifest checks + remover exit 1;
   valid manifest behavior unchanged.

## Allowed files

- scripts/lib/asset-manifest.sh (key-format support)
- scripts/update-agent-assets.sh (the parameterized step's record call)
- home/dot_local/bin/common/executable_remove-agent-asset
- scripts/check-agent-runtime.py
- tests/unit/ (matching modules)
- Your artifact paths (T61b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes; changing
bare-key semantics for the ten single-identity steps; guard weakening;
touching T61a's sourcing/shellcheck changes beyond mechanical merge.

## Validation

1. shellcheck clean on touched shell files; `make format`; `bash -n`.
2. `make unit-test` all green (totals + new count).
3. `make validate-agent-assets` green.
4. Fake-HOME transcript: double-identity record -> two keys present;
   corrupted-manifest doctor/remover behavior.
5. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T61b set); memory add with the decision fact above;
effects=none expected.
Reply `AGMSG-RESULT v1 task_id=T61b status=ready_for_review`. max_turns=20.
