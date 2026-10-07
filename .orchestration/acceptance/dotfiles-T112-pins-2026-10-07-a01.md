# Acceptance: dotfiles-T112-pins-2026-10-07-a01

- **Decision:** ACCEPTED. PR #301 head `f6789995` (one commit on main 7d3a45ee). Gate passed at that head in the orchestrator-review worktree with the PR-feedback, audit (`correct`) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0). Squash-merged to `main` as `a5edf2b7` (2026-10-07 03:49Z) with `gh pr merge 301 --squash --match-head-commit f6789995…`. RESULT received 2026-10-07 03:45Z.
- **Worker:** `claude-standard-dot-a005` (worker-c, w1A:p2). PONG `alive` at 01:01Z before dispatch (cleanup of T111).
- **Exemption declared:** acceptance and final integration; evidence-sync bookkeeping (the pins-only patch extracted read-only from the canonical clone into `.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-pins.patch`, sha256 `dda01202…`, `git apply --check` on 7d3a45ee before dispatch).
- **Origin:** the operator's `make upgrade` in the canonical clone `~/.local/share/chezmoi` left a pending pin diff mixed with an unrelated, rejected project-map draft; the regime rule says the pin diff travels as one class-pure worker PR and never stays dirty across sessions (T37 #209, T104). The operator asked on 2026-10-07 that the orchestrator carry all of this out, including the clone's clean-up, without operator steps.

## What is under acceptance (PR #301, head `f6789995`)

- `home/dot_agents/agent-config.yaml`: `assets.mise.pin` v2026.9.17, `assets.aws-cli.pin` 2.37.6 (two lines).
- `home/dot_mise/config.toml` and `mise.lock`: uv 0.12.21, yq 4.54.1, claude-code 2.1.292, ghq 1.11.2, herdr 0.9.3.
- `install/common/mise.sh`, `install/ubuntu/common/aws_cli.sh`: the rendered version constants.
- Blob identity: sha256 equal to the canonical clone for the four non-manifest files; manifest diff against origin/main is the two `pin:` lines.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, f6789995 | correct (no actionable finding: five allowed files, pins and artifacts present, four clone hashes match, all 37 configured tools match their lock entries, installer constants match the manifest, checksum and provenance protections intact; feedback snapshot matches 15 check runs plus the CodeRabbit status) |

- Sweep (f6789995): `.orchestration/validation/dotfiles-T112-pins-2026-10-07-a01-pr-feedback.json`, all items `not-applicable` (Codex quota notice; Codex security-review summary, completed without a finding; CodeRabbit skip summary and status; macOS runner capacity notices). No review thread. Crit evidence `…-crit.json` / `…-review-receipt.md`; worker-side `…-worker-crit.json` (4 informational P3, approve) / `…-worker-review-receipt.md`.
- Worker note carried forward, not applicable to this PR: the herdr lock URLs point at `github.com/ogulcancelik/herdr` because `config.toml` on main already names that backend; `gh api` shows it redirects to `herdrdev/herdr` and provenance stays `github-attestations`. Renaming the backend is a separate task if wanted. Pre-existing orphan lock entry `aqua:tak848/ccgate` 0.9.5 (ccgate removed in T28) likewise untouched.

## Parallelism

- T113 (`feat/codify-t111-lessons`) was dispatched to the same worker at this RESULT, on a fresh branch from origin/main; its files are disjoint from this PR's. After this merge the orchestrator runs `gh pr update-branch` on T113's PR.

## CompactionDB

- Worker decision `0e4d1b15-e1cf-400e-9868-5597258886ba` (main checkout, by a005). Orchestrator consolidation `543ebb07-ae61-45e8-9e04-0528c3a56323`.

cost: n/a
