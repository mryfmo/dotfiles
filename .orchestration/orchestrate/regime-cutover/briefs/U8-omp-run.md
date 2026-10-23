# U8 omp-run.sh (W6a, minimal) — brief

GOAL
Ship `scripts/orchestrator/omp-run.sh`, the one entry point the orchestrator seat (and the coordinator today) uses to run a non-interactive omp turn in a given role: it composes the omp 18.11.3 command from the role's policy overlay, the installed extension directories and a prompt file, prints the final assistant text (or the raw JSON stream), and fails closed when any input is missing. The protected-path merge check of the old plan is dropped (the chain glue it belonged to is retired with the agmsg regime).

SCOPE
Exclusive worktree on a new branch `feat/omp-run` from `origin/main` (main is at 6f154b60 or later; U5's `scripts/orchestrator/README.md` and U6's `home/dot_agents/omp/policies/*` are on main). May write: `scripts/orchestrator/omp-run.sh`, `tests/unit/test_omp_run.py`, `tests/fixtures/omp-run/**` (a fake `omp` on PATH that records argv and emits a canned `--mode json` stream), and one new section in `scripts/orchestrator/README.md`. Nothing else.

CONTEXT (read first)
- omp flags, measured this morning (`.orchestration/validation/025-pilot-facts.md` #G1..#G1-3 and the U1 report `.orchestration/validation/025-pilot-bridge-unit-report.md` §1-§2): the session path `omp --profile <p> -e <dir> --no-session --model <provider>/<id> --approval-mode <m> --mode json -p "<prompt>"` loads extensions, prints `Failed to load extension …` on stderr when a module fails, and emits one JSON event per line (`tool_execution_start/end`, `turn_end`, `agent_end`); `--max-time <s>` bounds a turn; `--config <file>` loads an overlay (U6: strict, `Config overlay not found` / `must be a YAML mapping`); `--no-extensions` disables discovery while explicit `-e` still loads.
- Roles and overlays (U6, on main): `home/dot_agents/omp/policies/{orchestrator,worker,audit}.yml` rendered by chezmoi to `~/.agents/omp/policies/<role>.yml`; read its README for the approval shape per role. The audit role runs `always-ask` with write tools denied: in print mode a denied tool returns omp's "requires approval" text to the model (measured #G1-2), which is the intended behaviour for an auditor.
- Extension directories (decision 30, U2/U3): bridge `~/.local/lib/omp-extensions/pi-claude-bridge` (staged with its own `node_modules`, loaded by `-e <dir>`), SIWC `~/.agents/omp/extensions/openai-siwc` (rendered from `home/dot_agents/omp/extensions/openai-siwc`). Both may be absent on a machine; the script takes `--ext <dir>` (repeatable) with these two as defaults and refuses with a clear message when a named directory does not exist.
- Profiles: the seat profile name equals the role (`orchestrator`, `worker`, `audit`); omp's `modelRoles.default` per profile is rendered by U4, so `--model` is an optional override only.
- Repository conventions: shdoc comments in English (`@file`, `@brief`, `@description`, `@arg`, `@option`, `@example`); tests in Python (`uv run --no-project --with pytest -m pytest …` or the repo's unittest form), fixtures under `tests/fixtures/`.

ACCEPTANCE
1. `omp-run.sh --role audit --prompt-file f.md [--cwd DIR] [--model P/ID] [--mode json|text] [--max-time S] [--ext DIR]...` composes exactly: `omp --profile <role> --config ~/.agents/omp/policies/<role>.yml -e <ext>... --no-session --max-time <S> [--model …] --mode <mode> -p "<file contents>"` with `cwd` set, inherits the caller's HOME (seats run as the operator), and never sets `--approval-mode` (the overlay owns it). Test with the fake omp: argv recorded and compared field by field.
2. `--mode text` (default) prints the final assistant text extracted from the JSON stream's last `turn_end` (or passes omp's text output through when `--mode text` is given to omp; choose one and document); `--mode json` passes the stream through unchanged. Exit code: omp's, and 2 on any refusal.
3. Refusals (tests): missing prompt file, missing policy overlay, missing extension dir, unknown role, `Failed to load extension` seen on stderr → exit 2 with the offending path in the message (fail closed; F5 of the U1 report).
4. No secrets handling; nothing written outside `--cwd`. shellcheck clean if installed (paste).
5. README section with the role table and two examples; PR open with `Program-Unit: regime-cutover/U8`, title `feat(orchestrator): omp-run.sh, the non-interactive omp entry point per role (U8)`, English body per STANDING 14, CI green except the expected-red `regime` check (standing order 17; U13 is fixing it).

VERIFY
`uv run --no-project --with pytest -m pytest tests/unit/test_omp_run.py -q` (paste); a dry run against the real omp under `HOME=$TMPDIR/u8-home` is allowed for the refusal paths only (no extensions present → the script must refuse before calling omp; paste). Network: `api.github.com`, `github.com` only.

TIMEBOX
60 minutes.

FORBIDDEN
No real seat runs, no `~/.omp`, no edits outside SCOPE, no merge, no rebase.

REPORT
≤ 150 words: branch, head sha, PR link, CI state, test summary, the exact composed argv for the audit role, deviations.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (17 lines) before any command.
