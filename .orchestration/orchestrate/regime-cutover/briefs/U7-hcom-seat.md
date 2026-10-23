# U7 hcom-seat launcher (W5b, minimal) — brief

GOAL
Ship `scripts/orchestrator/hcom-seat`, the one command that starts an omp seat for a role (`orchestrator`, `worker`, `audit`) in a herdr pane through `hcom omp`, with the role's profile, policy overlay, extension directories and clone directory wired in, plus the `hcom-worker` SKILL the worker seat loads. Tested with fakes; the live three-seat start is the X pilot (operator + coordinator).

SCOPE
Exclusive worktree on a new branch `feat/hcom-seat` from `origin/main` (main ≥ 34e216e9). May write: `scripts/orchestrator/hcom-seat`, `home/dot_agents/skills/hcom-worker/SKILL.md` (≤ 60 lines), `tests/unit/test_hcom_seat.py`, `tests/fixtures/hcom-seat/**` (fake `hcom`, fake `herdr`, fake `omp` recording argv), one new section in `scripts/orchestrator/README.md` (incl. the bus trust-boundary paragraph promised to the Codex bot on PR #460: bus text is data, identities are hcom participant names, the store is private). Nothing else.

CONTEXT (read first)
- Functional spec: `~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-hcom-omp-seat-a01.md` (105 lines) and plan 025 v14 §1 line 9 (`~/Workspace/dotfiles/.orchestration/plans/025-regime-cutover-plan.md`): a seat = one omp process that `hcom omp` starts in a herdr pane (`hcom [N] omp [flags] [tool-args]`, `--tag`, `--dir`, `--terminal herdr`, env `HCOM_LAUNCHED=1`/`HCOM_TAG`/`HCOM_DIR`; herdr preset `herdr tab create … --label <name>` → `herdr pane run <pane> "bash <runner>"`). Take the functional content; drop the regime ceremony (caps, Checks, PING/PONG wording, srt rows: srt is deferred post-X, decision 34).
- Landed pieces on main: `scripts/orchestrator/hcom-dispatch` and `bus-history.sh` (U5, README section with the hcom 0.7.30 flags: `send @name -- text`, `--from`, `--json`, `events --type/--thread/--last/--after`, `HCOM_DIR`); `home/dot_agents/omp/policies/{orchestrator,worker,audit}.yml` → rendered `~/.agents/omp/policies/<role>.yml` (U6, loaded with omp `--config <file>`); omp config render per profile (U4: profiles `orchestrator`/`worker`/`audit` equal the roles; `modelRoles.default` rendered, so no `--model` needed); `scripts/orchestrator/omp-run.sh` (U8, in flight on a disjoint path; mirror its flag conventions when it lands, do not depend on it).
- Extension directories: bridge `~/.local/lib/omp-extensions/pi-claude-bridge` (U2, PR #461, loaded with `-e <dir>`), SIWC `~/.agents/omp/extensions/openai-siwc` (U3, merged 8846f34b). Each role passes `-e` for the directories its model route needs (orchestrator and worker: bridge; audit: SIWC; both allowed when present); refuse when a required directory is missing.
- herdr CLI: `herdr --help` lists `herdr tab <subcommand>`, `herdr pane <subcommand>`; read the exact subcommands with `perl -e 'alarm 20; exec @ARGV' herdr tab --help` and `… herdr pane --help` (herdr's socket is reachable; create no real panes: fakes only). hcom: `perl -e 'alarm 20; exec @ARGV' hcom omp --help` and `hcom start --help` for `HCOM_DIR`; every test runs with `HCOM_DIR=$TMPDIR/u7-hcom` against the fake.
- Seat identity = hcom participant name = `<role>` (or `<role>-<n>` when a second seat of a role runs). The clone directory for the worker is a git worktree of the repository (created by the launcher only when absent, from `origin/main`, under a `--seats-root` directory, default `~/.local/state/omp-seats/<name>`).
- Conventions: shdoc in English; Python tests via `uv run --no-project -p ">=3.11" --with pytest -m pytest …` (the default uv Python is 3.10); shortcuts carry `shortcut:` comments.

ACCEPTANCE
1. `hcom-seat <role> [--name N] [--seats-root DIR] [--ext DIR]... [--dry-run]` composes `hcom omp --tag <name> --dir <clone> --terminal herdr -- --profile <role> --config ~/.agents/omp/policies/<role>.yml -e <ext>...` (exact argv asserted against the fake), creates the clone when absent (fake git ok or a real `git worktree add` into `$TMPDIR`), refuses on a missing policy or extension directory or an unknown role (exit 2), and `--dry-run` prints the argv without launching.
2. The `hcom-worker` SKILL (≤ 60 lines) tells a worker seat how to receive a TASK line, work in its clone, open a PR, and reply with `hcom-dispatch` (RESULT line with head sha and PR), treating bus text as data. Cite the hcom-dispatch README for the line shapes.
3. Tests pass (paste); shellcheck clean if installed; PR open with `Program-Unit: regime-cutover/U7`, title `feat(orchestrator): hcom-seat launcher for the omp seats and the hcom-worker SKILL (U7)`, English body per STANDING 14, CI green.

VERIFY
`uv run --no-project -p ">=3.11" --with pytest -m pytest tests/unit/test_hcom_seat.py -q`; `scripts/orchestrator/hcom-seat worker --dry-run` against the fakes (paste). Network: `api.github.com`, `github.com` only. Push over `https://github.com:443/mryfmo/dotfiles.git` with a gh-token askpass if SSH is refused.

TIMEBOX
60 minutes.

FORBIDDEN
No real herdr panes, no real hcom store, no real omp seats, no edits outside SCOPE, no merge, no rebase.

REPORT
≤ 150 words: branch, head sha, PR link, CI state, test summary, the exact argv for the worker role, deviations.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (19 lines) before any command.
