# T25 learning

- Correct ccgate metrics require the normal user HOME and an unset
  `XDG_STATE_HOME`; redirected state can look valid while containing zero
  records.
- Aggregate ccgate metrics identify tool totals, not command rows. Command
  pattern provenance must use separately counted approval/tool-use prefixes
  and label those sources honestly.
- A chezmoi executable launched through an `uv run --script` shebang should use
  `--no-cache` when hooks may execute in a filesystem-restricted sandbox.
- Read-oriented commands can still write through options such as
  `git diff --output`; deterministic allowlists need both whole-command regexes
  and explicit unsafe-option guards.
- Structured values must be screened for sensitive keys before classifier
  invocation, and audit summaries must use bounded operation classes rather
  than serialized input.
- Bash secret detection must cover header forms such as `Authorization:` and
  `Bearer` and `Cookie:`, plus basic-auth credentials embedded in URLs, not
  only assignment-like `token=...` syntax.
- A generic `version` operand is unsafe for interpreters: `python3 version`
  and `node version` execute a local file. Restrict their deterministic version
  checks to `--version`/`-V`.
- Managed hooks should use their installed executable path rather than depend
  on an interactive-shell PATH.
- Meeting a latency threshold is insufficient for LLM enablement when the
  classifier has zero successful classifications. Shadow accuracy must still
  be measured with a working authenticated CLI.
- Validate every policy field used by classification before entering the
  decision path, and convert key/type/regex errors into audited native ask.
- Supporting both hook contracts is not the same as supporting both existing
  auth domains. Route each origin to its own official CLI and forbid implicit
  cross-provider fallback.
- Secret regexes are a backstop, not a classifier trust boundary. The durable
  boundary is to send only policy-listed normalized actions and counts, never
  raw values, patches, or structured payloads.
- Confidence alone cannot make an LLM permission decision safe. Require the
  normalized action to belong deterministically to the returned category.
- Shadow enablement needs successful classification count plus p50/p95 and
  reviewable action/category/confidence evidence; latency alone is inadequate.
