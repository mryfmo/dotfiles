# U5 hcom-dispatch bus (W2b / C-1) — brief

GOAL
Deliver the hcom bus glue the three omp seats will use: `scripts/orchestrator/hcom-dispatch` (send one protocol line from one seat to another with a durable receipt) and `scripts/orchestrator/bus-history.sh` (read the bus history as the records need it), tested against a private hcom store under a scratch HOME, with CI green on a PR.

SCOPE
Exclusive worktree on a new branch `feat/hcom-dispatch-bus` from `origin/main`. May write: `scripts/orchestrator/hcom-dispatch`, `scripts/orchestrator/bus-history.sh`, `scripts/orchestrator/README.md` (new section), `tests/unit/test_hcom_dispatch.py` (or a bats file under `tests/` only if the repo's CI runs bats for that directory; prefer Python tests runnable with `uv run --no-project -m pytest`), fixtures under `tests/fixtures/hcom/**`. Nothing else. `home/dot_agents/**` belongs to U4/U6; `.orchestration/**` records are the coordinator's.

CONTEXT
- Functional spec: `~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-hcom-dispatch-bus-a02.md` (169 lines): the dispatch line format, the reply routes table, the receipt, the bus read for records. Take the functional content; drop the regime ceremony (caps, Checks blocks, PING/PONG wording, allowed_files counts). The earlier branches `tools/hcom-dispatch-bus-a01` (PR #407, records only) and `tools/hcom-dispatch-bus-a02` (worktree `.claude/worktrees/worker-f`, records only) hold findings (`.orchestration/dotfiles-T129-hcom-dispatch-bus-a01/report.md`); read them, do not reuse their branches.
- hcom 0.7.30 is installed at `~/.local/bin/hcom` (PyPI wheel; see the manifest `home/dot_agents/agent-config.yaml` `assets:` lines 529-547). Read `hcom --help` and the subcommand help with `perl -e 'alarm 20; exec @ARGV' hcom …` (it is a CLI, not a TUI). Its store location is controlled by `HCOM_DIR` (plan 025 names a private `HCOM_DIR` per program); run every test against `HCOM_DIR=$TMPDIR/u5-hcom` and never the real store. Cite the hcom source or help text for every flag you rely on (upstream `https://github.com/aannoo/hcom`, version 0.7.30; the installed wheel's files are under the uv tool dir, find them with `/usr/bin/find ~/.local/share/uv -path '*hcom*' -name '*.py' | head`).
- Seats are omp processes launched by `hcom omp` in herdr panes (plan 025 v14 §1 line 9); seat identity = hcom participant name. The protocol lines are the existing TASK/RESULT/ACCEPTANCE kinds (see `.orchestration/tasks/dotfiles-T129-hcom-omp-seat-a01.md` for the seat side, 105 lines, read-only for you).
- Shell scripts need shdoc comments in English (`@file`, `@brief`, `@description`, `@arg`, `@example`).

ACCEPTANCE
1. `hcom-dispatch <team> <from> <to> <pane-or-seat> <line>` writes the message through hcom into the private store and prints one receipt line (message id, timestamp, to, kind) that `bus-history.sh` can find again; a failed send exits non-zero with the hcom error on stderr.
2. `bus-history.sh --limit N [--since TS] [--kind KIND]` prints the bus history in a stable TSV the records can paste.
3. Tests cover: a send and read round trip in the scratch store; the refusal paths (unknown team or seat, empty line, store absent); the receipt format. Paste the pytest summary line.
4. CI green on the PR (`gh pr checks` pasted). PR title `feat(orchestrator): hcom-dispatch and bus-history for the omp seats`, English body per STANDING 14.

VERIFY
`uv run --no-project -m pytest tests/unit/test_hcom_dispatch.py -q`; `shellcheck scripts/orchestrator/bus-history.sh` if shellcheck is installed (paste); `git diff --stat origin/main...HEAD`. Network: `api.github.com`, `github.com` only.

TIMEBOX
75 minutes.

FORBIDDEN
No real hcom store, no herdr commands, no omp launches, no edits outside SCOPE, no merge, no rebase of other branches.

REPORT
≤ 200 words: branch, head sha, PR link, CI state, test summary, the hcom flags you depend on with citations, deviations, follow-ups.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (16 lines) before any command.
