# Rule candidate: validate agent assets before every boundary commit; audit transcripts can trip the secret validator

Observed 2026-09-28: the boundary commit 04746ca (T33c artifacts) turned the
main "Agent assets" workflow red: `validate-agent-assets.py` flagged
"possible committed secret" in the T33c audit evidence. The Codex audit
transcript quoted plugin schema fields `design_token: <quoted value masked for the repo secret validator>` /
`applies_token: <quoted value masked for the repo secret validator>`, which match `SECRET_PATTERN`'s
`token\s*[:=]\s*["'][^"']+["']` clause. False positive, but a red main and a
blocked worker (T33e PONG) until the two evidence files were masked
(e8cf7e1, f6b76b8). The first fix commit was pushed before the validator was
re-run correctly (a `| tail` swallowed the exit status) — orchestrator process
error.

Candidate rules:
1. Orchestrator boundary commits run `make validate-agent-assets` (real exit
   status) before `git commit`; a failure is fixed before pushing.
2. `herdr-agents --audit` (or the evidence writer) masks `SECRET_PATTERN`
   matches in the tee'd transcript on the way to `.orchestration/validation/`
   (write `<redacted>` and count them in the `Audit …` summary), so quoted
   reviewed content never blocks the boundary commit — an audit transcript is
   reviewed content plus tool output and must be treated as untrusted data.
3. Alternatively exempt `*-audit*.md` under `.orchestration/validation/` from
   the committed-secret scan; rejected for now because real credentials could
   leak through an auditor's tool output.
