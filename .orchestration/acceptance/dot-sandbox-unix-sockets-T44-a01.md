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
  - `~/.cache/uv`. `failIfUnavailable` and `allowedDomains` untouched.
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

Codex audit of c2c1f62: queued 21:08Z (operator paused Codex); run
2026-09-30 04:14Z (`…-audit-c2c1f62.md`, gpt-6-astra, read-only, high):
**Verdict: incorrect**, two P2s.

## Audit dispositions

1. `agent-config.yaml:232` `allowAllUnixSockets: true` is unconditional, so
   the rendered `claude-settings-managed.json` (template line 59, verified at
   c2c1f62) also disables the macOS socket allowlist the same block keeps.
   Confirmed: the repo targets macOS (install/macos, `.chezmoiignore` uses
   `{{ if eq .chezmoi.os "darwin" }}`), and the generated template carries no
   OS condition. My round-1 review read "allowUnixSockets kept for macOS" as
   sufficient; it is not, because `allowAllUnixSockets` supersedes it. → r2.
2. `README.md:352` "file and network isolation stay in force" omits that any
   local Unix socket becomes reachable, so socket-mediated services (docker,
   D-Bus, other agents' control sockets) extend the trust boundary on Linux.
   Confirmed; my own round-1 impact note listed docker.sock, but the README
   sentence the operator reads does not. → r2.

Also from the 1843dd1 audit: the task file's `allowed_files` (network block
only) contradicted addendum 8 (`filesystem.extra_allow_write`). Amended in the
task file now; the worker's resolution stands.

## PR #215 feedback sweep (head c2c1f62, `…-pr-feedback.json`, 16 items)

Codex GitHub review P1 at `agent-config.yaml:232`: the all-socket relaxation is
a sandbox escape wherever docker.sock or another daemon socket is
user-accessible. Verified on the operator's host **outside the sandbox**
(the in-sandbox `id -nG` had omitted the group): user in `docker` group,
`/var/run/docker.sock` root:docker 660, user D-Bus bus and `systemd --user`
reachable, 110 listening Unix sockets; `autoAllowBashIfSandboxed: true`. So an
auto-approved sandboxed command could run `docker run -v /:/host` or
`systemd-run --user`. Confirmed P1. Remaining 15 items (runner notices, brew
tap warning, CodeRabbit skip, Codex container comment) not-applicable.

Orchestrator failure: round 1 listed "docker.sock if present" as impact and
still accepted the relaxation without a security-profile review
(`model-selection.md` requires one for trust-boundary changes).

**Decision (round 1, revised 2026-10-01): REVISE r2 — remove
`allowAllUnixSockets`, keep `extra_allow_write ~/.cache/uv`** (operator
decision). Audit finding 1 (macOS scope) becomes moot with the removal; audit
finding 2 (README trust boundary) is answered by the README sentence r2 adds.
Queued in worker-c behind T47 and T43 r3 (README overlaps T43 r3, so not a
parallel candidate). Amendment in the task file; ACCEPTANCE goes out in turn.
