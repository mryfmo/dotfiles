# Acceptance: dot-sandbox-unix-sockets-T44-a01

Dispatched 2026-09-29T21:14Z (task_commit f45cf73; addenda 7–8 for the gh
keyring and uv cache). PONG 21:15Z flagged the recurring `.git/config.lock`
stub (see T39 leg 1). PING 21:45Z (finish in this turn). RESULT 21:46Z
(revision 1, head c2c1f62, PR #215, CI 12/12).

## Adversarial review (orchestrator, from origin refs only)

- Scope: seven allowed files (manifest sandbox block, generator, validator,
  generated template, two tests, README sandbox section). The manifest gains
  `network.allowAllUnixSockets: true` (comment: Linux/WSL2 seccomp, herdr
  control plane, gh keyring D-Bus, file and network isolation unchanged) and
  `filesystem.extra_allow_write: [~/.cache/uv]` — a new list outside "the
  sandbox.network block only", required by my addendum item 8; scope
  conflict resolved in favour of the explicit item (worker noted it).
- Generator: `allowAllUnixSockets` passed through only when present;
  `allowWrite` = Codex writable roots + `extra_allow_write`; no failure when
  either key is absent (tested).
- Validator: `allowAllUnixSockets` must be boolean; extra allowWrite entries
  absolute or `~/` without globs; 3 new tests (accept/reject each, generator
  output with and without the keys).
- Rendered template: `network.allowAllUnixSockets: true`, `allowUnixSockets`
  kept for macOS, five GitHub domains unchanged, allowWrite = four agmsg roots
  + `~/.cache/uv`. `failIfUnavailable` and `allowedDomains` untouched.
- README: Linux socket scope sentence and the effect paragraph name the uv
  cache and Unix sockets; T43's paragraphs untouched.
- Validation file: `--check` ok, `agent asset validation ok`, `Ran 613 …
  OK (skipped=1)`, `gh pr checks` all pass; run unsandboxed because of the uv
  cache (the very thing this task fixes). `base-ok` printed exit 1 only
  because main gained the orchestrator's `.orchestration`-only c6241bb after
  the branch point; the PR is MERGEABLE.
- CI all pass on c2c1f62 (verified on GitHub). CompactionDB 5ab13bbc present.
- Operator-visible impact once applied: sandboxed Bash can reach every local
  Unix socket (herdr, keyring, docker.sock if present) and write `~/.cache/uv`;
  everything else stays confined. The recurring `.git/config.lock` stub is
  NOT addressed here (T45 candidate).

Codex audit of c2c1f62: **queued** (operator paused Codex 21:08Z, rate
limit).

**Decision: PENDING AUDIT** (orchestrator review complete, no findings).
