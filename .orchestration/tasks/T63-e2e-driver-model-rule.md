# T63: Regulate E2E test-subject session models via the express profile (docs only)

task_id: T63
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

[memory: decision — Disposable E2E test-subject agent sessions launch with the express profile args from ~/.agents/model-profiles.env (MODEL_PROFILE_EXPRESS_CLAUDE_ARGS / _CODEX_ARGS), never with ad-hoc --model flags; harness behavior under test is model-independent, so the cheapest profile is the regulated default.]

## Background (operator decision 2026-08-16)

Live-E2E test-subject sessions were launched with an ad-hoc
`claude --model haiku`, which is outside the model-selection rule that
models are named only in model_profiles. The operator ruled: regulate
E2E drivers via the express profile. (Also ruled, recorded separately:
gpt-daybreak-blue-latest adoption is deferred pending verification.)

## Fix (exact, docs only)

1. home/dot_config/claude/rules/model-selection.md: add ONE bullet in the
   existing style: disposable E2E/test-subject agent sessions launch with
   the express profile args sourced from `~/.agents/model-profiles.env`
   (`MODEL_PROFILE_EXPRESS_CLAUDE_ARGS` / `MODEL_PROFILE_EXPRESS_CODEX_ARGS`);
   ad-hoc --model flags remain prohibited even for throwaway sessions.
2. home/dot_config/claude/rules/agmsg-orchestration.md: ONE bullet in the
   live-E2E clause area: orchestrator-driven E2E test-subject panes obey
   the same express-profile rule.
3. Match existing bullet style (English), no other edits.

## Allowed files

- home/dot_config/claude/rules/model-selection.md
- home/dot_config/claude/rules/agmsg-orchestration.md
- Your artifact paths (T63 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; any code change.

## Validation

1. `make validate-agent-assets` green.
2. `git diff` full text; consistency with model_profiles and
   model-profiles.env variable names (quote the env lines).
3. `git status --porcelain` -> only Allowed files + artifacts.

## Completion / RESULT contract

Five artifacts (T63 set); memory add with the decision fact;
effects=none.
Reply `AGMSG-RESULT v1 task_id=T63 status=ready_for_review`. max_turns=10.
