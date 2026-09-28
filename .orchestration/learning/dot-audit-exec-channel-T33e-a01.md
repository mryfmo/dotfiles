# T33e learning triage

## Candidates

1. When a gate reads a tool's "last message" file (`codex exec -o`), delete
   that file inside the same command right before the tool runs. Otherwise a
   run that fails to write the file is judged by the previous run's verdict.
2. The concluding-line rule (last non-blank line) is stricter than the
   last-matching-line rule. It turns a quoted verdict followed by prose into
   `missing` instead of trusting it. In a transcript fallback, skip the
   `tokens used` count line so it is never the concluding line.
3. `scripts/validate-agent-assets.py` `SECRET_PATTERN` flags
   `*_token: <quoted value masked for the repo secret validator>` field names that appear in quoted audit transcripts
   (`design_token`, `applies_token`). Audit evidence committed under
   `.orchestration/validation/` should be redacted, or covered by the
   placeholder allowlist, before commit. Otherwise every branch fails the
   `validate` CI job. This is a rule candidate for the orchestrator's
   evidence sync.
4. The permgate bench flake has now appeared 4 times, each on the first full
   run after an edit (T33d).

## Promotion

None. These are candidates only.
