# T64: Add the `security` model profile (gpt-daybreak-blue-latest, security-audit tier)

task_id: T64
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

[memory: decision — model_profiles gains a fifth profile `security` (claude: claude-fable-5 high; codex: gpt-daybreak-blue-latest, security-audit specialist) used for security audits of pending changes — /security-review runs, permgate policy changes, redaction/secret-handling and trust-boundary work; the codex security worker identity is codex-security-<project-suffix>.]

## Background (operator facts, 2026-08-16)

gpt-daybreak-blue-latest is a security-audit specialist model. It is NOT
a general-capability tier: it gets a dedicated `security` profile rather
than replacing luna/terra. The -latest rolling alias is accepted for now;
a dated alias replaces it when one exists (recorded in project memory).

## Fix (exact)

1. home/dot_agents/agent-config.yaml — add to model_profiles, after
   `deep`:
   ```yaml
   security:
     # Security-audit tier: specialist model for auditing pending changes.
     claude: { model: claude-fable-5, effort: high }
     codex:
       model: gpt-daybreak-blue-latest
       model_reasoning_effort: high
       notify:
         ["{{ .chezmoi.homeDir }}/.local/bin/common/contextdb-codex-notify"]
   ```
   (notify included: a security worker is worker-facing like
   standard/deep. If the generator's notify handling is
   profile-agnostic this Just Works — verify.)
   Keep `interactive_profile: deep` unchanged.
2. Run the generator; regenerated outputs expected:
   home/dot*codex/modify_security.config.toml (with the T48c apply-time
   home expansion), model-profiles.env gaining
   MODEL_PROFILE_SECURITY*{CLAUDE,CODEX}\_ARGS, and any manifest updates
   the generator derives. Do NOT hand-edit generated files.
3. scripts/validate-agent-assets.py — update the model-profiles
   expectation from the fixed four to include `security` (keep the check
   strict: exactly five named profiles, security's codex model equals
   gpt-daybreak-blue-latest).
4. home/dot_config/claude/rules/model-selection.md — ONE bullet: security
   audits (security-review runs, permgate policy changes,
   redaction/secret-handling, trust-boundary code) run the Codex worker
   on the `security` profile; identity codex-security-<project-suffix>;
   acceptance stays orchestrator-side per the agmsg rules.
5. Tests: extend the existing model-profile unit coverage for the fifth
   profile (generator --check green; validator accepts current tree,
   rejects a tree missing `security`).

## Allowed files

- home/dot_agents/agent-config.yaml
- Generated outputs of scripts/generate-agent-configs.py (via the
  generator only)
- scripts/validate-agent-assets.py (profile expectation)
- home/dot_config/claude/rules/model-selection.md (one bullet)
- tests/unit/ (matching modules)
- Your artifact paths (T64 five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; dependency changes;
hand-editing generated files; changing interactive_profile; touching
other profiles' models/efforts.

## Validation

1. `uv run --with pyyaml scripts/generate-agent-configs.py --check` green.
2. `make validate-agent-assets` green (with the updated expectation).
3. `make unit-test` all green (totals + new count).
4. `make format` exit 0.
5. Local render proof: pipe an empty/existing config through the NEW
   modify_security.config.toml -> model gpt-daybreak-blue-latest, expanded
   notify path, no residual '{{'.
6. `git status --porcelain` / `git diff --stat` -> only Allowed files.

## Completion / RESULT contract

Five artifacts (T64 set); memory add with the decision fact;
effects=none.
Reply `AGMSG-RESULT v1 task_id=T64 status=ready_for_review`. max_turns=20.
