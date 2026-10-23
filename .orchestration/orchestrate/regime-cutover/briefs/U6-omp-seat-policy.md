# U6 omp seat tool policy (W2c / B-2) — brief

GOAL
Ship the per-role omp tool policies the seats will load (orchestrator, worker, audit), as files the seat launcher can point omp at, with tests that prove each policy allows what the role needs and denies what it must not, and CI green on a PR.

SCOPE
Exclusive worktree on a new branch `feat/omp-seat-policy` from `origin/main`. May write: `home/dot_agents/omp/policies/orchestrator.yml`, `home/dot_agents/omp/policies/worker.yml`, `home/dot_agents/omp/policies/audit.yml`, `home/dot_agents/omp/policies/README.md`, `tests/unit/test_omp_seat_policy.py`, fixtures under `tests/fixtures/omp-policies/**`. Nothing else. Do NOT edit `home/dot_agents/agent-config.yaml` (U4 owns it this wave); if the manifest needs a key for these files, write the exact lines into your report as a follow-up for the coordinator.

CONTEXT
- Functional spec: `~/Workspace/dotfiles/.orchestration/tasks/dotfiles-T129-omp-seat-policy-a01.md` (110 lines): the three roles, the matcher rules, the deny list for the worker (no `gh pr merge`, no pushes to `main`, no writes outside its clone), the audit role read-only, the orchestrator's allowances. Take the functional content; drop the regime ceremony (caps, Checks blocks, PING/PONG, allowed_files counts, "round 4" wording).
- omp 18.11.3 policy mechanism: find the authoritative schema in the installed source `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/src/` (search for the tool approval policy / `approvalMode` / `tools.approvalMode` / policy file loading; `src/cli/args.ts:94` has `approvalMode?: "always-ask" | "write" | "yolo"`) and in the upstream docs `https://raw.githubusercontent.com/can1357/oh-my-pi/main/docs/approval-mode.md` (and any `docs/*policy*` the index lists: `~/.local/lib/node_modules/@oh-my-pi/pi-coding-agent/dist/docs-index.generated.txt`). Cite `file:line` for the schema you implement against; if omp has no file-based tool policy, say so with the citation and ship the closest native mechanism (settings keys, `--approval-mode`, allow/deny lists) plus a one-line `shortcut:` comment.
- Measured facts to respect: `.orchestration/validation/025-v13-facts-20261023.md` §2b (on the bridge route the child Claude Code runs with `tools: []`, so omp's tool policy is the only gate for Claude-routed seats).
- Tests: Python with `uv run --no-project -m pytest`; the test loads each policy file and asserts the decisions for a fixed table of tool calls (e.g. worker: `bash: gh pr merge …` denied, `edit` inside the clone allowed, `bash: git push origin main` denied; audit: every write tool denied; orchestrator: `gh pr merge` allowed). If omp's evaluator is not callable from Python, test the files' shape and the deny patterns with a small evaluator that mirrors the documented matcher semantics, and mark it `shortcut: mirrors omp's matcher as documented at <file:line>; upgrade to omp's own evaluator when it exposes one`.

ACCEPTANCE
1. Three policy files validated against the schema you cite; `omp --profile u6 --config <policy or settings overlay> …` dry-run under `HOME=$TMPDIR/u6-home` shows omp accepts the file without error (read-only listing command, alarm-wrapped; paste output).
2. Tests pass (paste the summary line).
3. PR open, CI green, title `feat(omp): seat tool policies for orchestrator, worker and audit`, English body per STANDING 14.

VERIFY
`uv run --no-project -m pytest tests/unit/test_omp_seat_policy.py -q`; the omp dry run; `git diff --stat origin/main...HEAD`. Network: `raw.githubusercontent.com` for docs, `api.github.com`/`github.com` for the PR.

TIMEBOX
60 minutes.

FORBIDDEN
No edits outside SCOPE, no manifest edits, no real `~/.omp`, no merge, no rebase.

REPORT
≤ 200 words: branch, head sha, PR link, CI state, test summary, schema citation, the manifest lines the coordinator must add (if any), deviations, follow-ups.

STANDING
Read and obey `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` (16 lines) before any command.
