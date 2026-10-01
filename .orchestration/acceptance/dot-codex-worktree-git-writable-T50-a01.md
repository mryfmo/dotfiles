# Acceptance: dot-codex-worktree-git-writable-T50-a01

Drafted 2026-10-02 from the T40 blocker (PONG 651: a Codex worker in a
nested worktree cannot write `<main>/.git/worktrees/<name>/index.lock`).
Dispatched 2026-10-01T21:29:27Z (msg 660) to `claude-standard-dot-a005`
(worker-c) after T46 merged (bb3370a). RESULT msg 664 (22:31:40Z), head
5952ab8, PR #222.

## Round 1 (5952ab8)

- Mechanism: launcher. `codex_worktree_writable_roots` derives `<common>`
  and the worktree git dir from `git rev-parse --path-format=absolute
--git-common-dir/--git-dir`, emits
  `sandbox_workspace_write.writable_roots=[<configured agmsg roots>,
<common>/objects, <common>/refs, <common>/logs, <common>/worktrees/<name>]`
  as `-c` for the pair worker (`start_worker_agent`, all three paths) and as
  a `--config` spawn-options entry for `--add-worker`; nothing for a main
  checkout (git dir = common dir) or a non-string-array config. The project
  config candidate was rejected with evidence (absolute paths required;
  per-worktree name). README paragraph, rule and SKILL bullets added.
- Evidence (verbatim in the validation file): `codex sandbox` in 0.158.0
  runs permission profiles only (`-P workspace-write` errors, `:workspace`
  ignores legacy `writable_roots`), so the worker used (1) `codex sandbox -P
:workspace` before, (2) a scratch `CODEX_HOME` permission profile with the
  four `write` entries, (3) `codex doctor --json` effective policy showing
  the launcher value byte-identical to the hand-built one, and (4) two
  disposable `codex exec --profile express --sandbox workspace-write
--ephemeral` runs (express profile per the model-selection rule) before and
  after: the four paths writable, `hooks`/`info`/`.git`/`config`/`HEAD`/
  `packed-refs` denied, `commit`, local `fetch`, `rebase` (with the harmless
  `packed-refs.lock` notice) and local `push --dry-run` exit 0; GitHub
  fetch/push still fail on DNS (network unchanged). Tests: add-worker spawn
  options (updated) and full-mode pair worker (new), negative check at
  bb3370a; 682 OK; render-check, validate, shellcheck, shfmt clean; CI
  green Linux+macOS; CLEAN.
- Flags: the worker saw a 0-byte `.git/config.lock` and left it — on the
  host no such file exists (sandbox deny-mount stub); the stale T45 record
  in worker-c was moved to the worker's scratchpad (prefix of the committed
  version).
- Codex audit (pre-screen, 5952ab8): **incorrect**, one P2 (high
  confidence) — the awk extraction of `writable_roots` misses an indented
  key or a commented-out section header and then **replaces** the
  configured roots with the git paths alone, dropping agmsg store access; a
  multi-line array disables the grant. The generator renders a single line
  today, so the live behaviour is right, but the grant must never be able to
  drop configured roots. Valid.
- Codex GitHub review (5952ab8, 22:10:25Z): two P2s — the multi-line
  parsing defect (same root cause, other direction: grant silently skipped)
  and shallow-clone metadata (`<common>/shallow(.lock)` stays read-only, so
  `--deepen/--unshallow` still fail). The first is covered by the audit
  fix; the second is accepted as detect-and-document (no wider grant).

**Decision (round 1): REVISE r2** — parse the TOML with `tomllib`, fail
closed (no override on any parse doubt, never a reduced list), tests for
indented/multi-line and unparseable configs with a negative check, shallow
clone detection line + docs. Task amendment r2.

## Round 2 (RESULT msg 666, e334af5) and acceptance

- e334af5 verified in the diff: `tomllib` parse emitting the list as JSON;
  `[[ -e config ]] && ! configured=$(python3 …)` → stderr line and no
  override on parse/type failure or missing tomllib (fail closed); missing
  file/key starts from `[]` (nothing `-c` could narrow); `#` check kept with
  its own line; `--is-shallow-repository` = true → stderr notice, grant
  unchanged; shdoc and README updated. Three new tests (indented multi-line
  array keeps the configured roots first; unparseable config emits no
  `--config`; shallow notice) fail at 5952ab8; fixture gives the test PATH
  this interpreter as `python3`. Override bytes identical to 5952ab8 for the
  generated single-line config (`cmp` exit 0), so the recorded probes stand.
  685 OK; render-check, validate, shellcheck, shfmt clean; CI green
  Linux+macOS; CLEAN. Behaviour change acknowledged: a python3 older than
  3.11 with an existing config now means no grant (fail closed, falls back
  to operator-approved escalation).
- Codex audit of e334af5: **correct**. Ledger: 5952ab8 incorrect (P2
  parser) → fixed in e334af5; e334af5 correct.
- Sweep on e334af5 (17 items): 2 `fixed:e334af5` (Codex P2s: multi-line
  parsing, shallow metadata), 15 `not-applicable` (11 runner notices, 1
  Homebrew tap warning, Codex review container, CodeRabbit skipped comment
  and status). No Codex review of e334af5 posted by 22:55Z.
- Gate: `AGENT_REVIEWED=1 REVIEW_EVIDENCE=…-review-receipt.md BASE=origin/main
PR_FEEDBACK_EVIDENCE=…-pr-feedback.json make require-crit-review` in
  `.claude/worktrees/orchestrator-review` at e334af5 → exit 0.
- Live leg deferred: the installed launcher is still the T42 build until
  `make -C ~/.local/share/chezmoi update`; the first real codex worker seat
  after that (worker-sec reseat or a new worktree) records whether `git
commit` inside the Codex sandbox succeeds without an escalation.

**Decision: ACCEPTED** — squash-merge PR #222 without `--delete-branch`
(worker-c holds the branch). Consolidated CompactionDB decision
66d0eb9f-9ea8-4a13-9632-18b43aea05a4 added at acceptance.

cost: n/a (worker reported none)
