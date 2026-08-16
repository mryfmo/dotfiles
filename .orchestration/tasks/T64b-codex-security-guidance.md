# T64b: Align Codex-facing security guidance with the security profile (PR #131 bot finding)

task_id: T64b
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-deep-dot

[memory: decision — Codex-facing guidance prescribes the `security` profile for security-audit scenarios (/security-review, permgate policy, redaction/secret handling, trust-boundary code) and reserves `deep` for non-audit escalation; the Claude and Codex rule surfaces must never disagree on profile routing.]

## Finding (chatgpt-codex-connector on PR #131, orchestrator-triaged REAL)

home/dot_config/codex/AGENTS.md:103 still routes security-related work to
`--profile deep`, conflicting with the new model-selection rule that
audits run on the `security` profile.

## Fix (exact)

1. home/dot_config/codex/AGENTS.md (the line ~103 area): update the
   security-work guidance so the four audit scenarios (/security-review
   runs, permgate policy changes, redaction/secret handling,
   trust-boundary code) prescribe `--profile security`; `deep` remains
   for non-audit escalation (cross-cutting design, unknown failures).
   Match the file's existing language/style (Japanese where the
   surrounding text is Japanese).
2. Audit the SAME file and home/dot_config/claude/rules/\*.md for any
   OTHER remaining "security -> deep" routing statements and align them
   too (report the audit result; fix only genuine routing conflicts, not
   the permgate description).

## Allowed files

- home/dot_config/codex/AGENTS.md
- home/dot_config/claude/rules/\*.md (only if the audit finds a genuine
  conflicting routing statement)
- Your artifact paths (T64b five artifacts)

## Forbidden actions

git commit; git push; chezmoi apply; bats; code changes; touching
model_profiles or generated files.

## Validation

1. `make validate-agent-assets` green.
2. `git diff` full text; audit table of every security-routing statement
   across both surfaces with its post-fix profile.
3. `git status --porcelain` -> only Allowed files + artifacts.

## Completion / RESULT contract

Five artifacts (T64b set); memory add with the decision fact;
effects=none.
Reply `AGMSG-RESULT v1 task_id=T64b status=ready_for_review`. max_turns=10.
