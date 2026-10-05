# Acceptance: dotfiles-T82-codex-compaction-hooks-a01

- **Decision:** ACCEPTED. PR #269 squash-merged to `main` as `2e65742c`; final head `9ff2ad52` (round 3). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, one disposition below) and crit evidence (`BASE=origin/main … make require-crit-review` rc=0, 2026-10-05 00:48Z). **Operator sequencing:** do not trust the three new Codex hooks in `/hooks` until T81b (vendor 2.0.0+dotfiles.9, no-follow storage binding) is merged and deployed.
- **Worker:** `claude-standard-dot-a006` (worker-d, wY:p2). task_rev matched at dispatch and after the PONG-decision append.
- **Exemption declared:** acceptance and final integration.
- **Plan reference:** Phase 5, dotfiles-T82 (principle 7). Depends on T80 and T81 (merged).

## What was accepted (PR #269, final head `9ff2ad5260908bb0d5bcbc5bb20a7f7982764700` (round 3, on main f2d4d709); round-0 head `7ee910878b1e94eff35da30307c46debeb9c97e6`; commits 4c388114, c8127bd8, 7ee91087, da04f943, 74a559c7, 94761d1a, c466231a, 9ff2ad52; 14 files)

- `home/dot_agents/agent-config.yaml`: `codex.hooks.command_hooks` with PreCompact (timeout 10), PostCompact (10) and SessionEnd (3, the Codex cap verified in T80), each running `contextdb-codex-notify` with the status message "Recording to CompactionDB"; `permission_request`, `hooks.state` and the profiles' `notify` entries unchanged.
- `home/.chezmoitemplates/codex-config-managed.toml`: three `[[hooks.<Event>]]` tables rendered by the generator (`make render-check` clean; validator hook-table comparison passes).
- Revise round 1 (da04f943): vendor `contextdb_cli.py ingest --no-maintenance` (skips the SessionEnd retention pass and the log/quarantine cleanup; `process_payload(maintenance=…)`), vendor test, CHANGELOG 2.0.0+dotfiles.8, `make manifest`, pin and `test_asset_manifest.py` literals, project copy refreshed by copying `cli.py`/`hook.py` (byte-identical; the installer cannot write a Claude seat's read-only `.claude/hooks`).
- `executable_contextdb-codex-notify`: payload from `$1` or stdin; calls `ingest --no-maintenance` with a 2-second subprocess timeout (retention stays on the explicit `prune` and on Claude's own SessionEnd hook); refuses a symlinked `.claude/contextdb` opt-in (74a559c7) and any symlink at any depth under the opt-in tree before invoking the CLI (`os.walk` without following links, 9ff2ad52; `state`, `spool`, `spool/incoming`, `spool/quarantine`, `health` must be real directories or absent; regular files are fine); `python3 -I` so a `json.py` in the session cwd cannot shadow the standard library (Codex Security P1, fixed 7ee91087; the same hardening covers the pre-existing `notify` path); failures print one stderr line and exit 0; shdoc updated.
- README operator phase: after `make update`, run `/hooks` in Codex once per machine and trust the three CompactionDB hooks and the existing permgate `PermissionRequest` hook; confirm `[hooks.state]` entries; the managed merge keeps them.
- Tests: stdin payload, argv precedence, invalid stdin, cwd shadowing regression (negative control pasted: fails without `-I`), symlinked opt-in, rendered routing, vendor `--no-maintenance`; 810 unit tests; vendor suite 90 OK; shellcheck/shfmt/ruff clean; live check with the .8 CLI via a temp HOME: `pre_compact` and `session_end|t82r1b|codex`, SessionEnd 0.14 s. Until `make update` deploys 2.0.0+dotfiles.8, the deployed .6 CLI lacks the flag and the receiver fails cleanly (stderr line, rc 0).

## Decisions taken during the task

- PONG 1: Codex P1 4179558230 (new user-config hooks are skipped until trusted) → option (a): the operator trusts them once in `/hooks`; README paragraph allowed; no hash derivation or `requirements.toml`. Follow-up task: record the trusted `hooks.state` keys as manifest pins and refresh the drifted ponytail hashes (also seen as a `make update` warning on this host). Codex P2 4179558226 (no `compact_summary` in PostCompact) → not applicable; PostCompact stays a timeline marker.
- Codex Security P1 4179583256 (receiver runs from the session cwd once trusted) → fixed 7ee91087 (`python3 -I`). All three threads replied and resolved by the orchestrator.
- Round-1 Codex threads: 4179749575 (symlinked opt-in) `fixed:74a559c7`; 4179789825 (symlinked state/spool/health children) first dispositioned as a T81b follow-up, then reopened as revise round 2 after the audit held that the deferral left the trusted hooks exposed (the wrapper now refuses symlinked children; the vendor-side hardening stays in T81b as defense in depth); 4179789828 (session cwd in a subdirectory misses the opt-in) not applicable — pre-existing receiver behaviour, T81b item 6. All replied and resolved by the orchestrator.
- Round-3 Codex threads (both not applicable, replied and resolved by the orchestrator): 4179926397 (Codex-only projects lose `errors.jsonl`/quarantine retention under `--no-maintenance`) — every opted-in project here runs both runtimes and Claude's SessionEnd hook performs that retention; moving it into the explicit vendor `prune` is T81b item 7; 4179926400 (TOCTOU between the walk and the CLI start) — needs a same-user process mutating the tree, outside the hook's threat model; atomic no-follow binding belongs in `project_paths.ensure()` (T81b item 5).
- The real Codex-session `/compact` leg on both hosts is T87 (live E2E), not performed here.

## Orchestrator re-derivation

- Read the full diff: manifest entries, rendered tables (timeouts 10/10/3), wrapper (`payload="${1:-$(cat)}"`, `python3 -I -`, ingest-only, 5-second subprocess timeout kept; Codex cuts SessionEnd at 3 s), README paragraph, tests.
- CI 13/13 green on 7ee91087, 94761d1a, c466231a and 9ff2ad52; PR `clean` after the six resolutions; project copy `cli.py`/`hook.py` byte-identical to the vendor tree at the head.

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, 7ee91087 (round-0 head) | incorrect (2) → ingest path still ran retention inside the SessionEnd budget (fixed in revise round 1 with a vendor `ingest --no-maintenance`, 2.0.0+dotfiles.8); negative-control evidence added |
| task-level, 94761d1a (round-1 head) | incorrect (2) → symlinked state/spool/health children refused by the wrapper in revise round 2; the undispositioned sweep item was the orchestrator's matcher error, corrected |
| task-level, c466231a (round-2 head) | incorrect (1) → symlinked grandchildren under spool still reached the CLI; revise round 3 refuses any symlink at any depth under the opt-in directory |
| task-level, final head 9ff2ad52 | incorrect (1) → disposition below |

audit-finding: 1 the receiver's symlink walk is separate from the vendor CLI's directory creation, so a workspace-confined process could swap `state` for a symlink between the check and `project_paths.ensure()`, which the unconfined hook then follows → not-applicable:the only complete fix is binding the storage paths with no-follow semantics where they are created, which is the vendor `project_paths.ensure()` (T81b item 5, the next task dispatched on the Claude seat); until T81b is deployed the three new hooks execute nothing, because Codex skips untrusted user-config hooks and the operator trust step is sequenced after T81b in the T81b and T87 task files and in this record; the receiver's walk remains as the first line and T81b's test covers the race shape

- Sweep (head 9ff2ad52): see the masked copy `.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-pr-feedback.json`; `fixed:7ee91087`, `fixed:74a559c7`, `fixed:9ff2ad52`, the rest `not-applicable`.
- Crit evidence `…-crit.json` (one resolved review-scope record), receipt `…-review-receipt.md`.

## Follow-ups

- T82b (to draft): hook trust-state pins (`codex.hooks.state` entries for the four config hooks once trusted) and the ponytail `trusted_hash` refresh.
- T81b (vendor 2.0.0+dotfiles.9): `project_paths.ensure()` hardening for symlinked children and grandchildren (`spool/incoming`, `spool/quarantine`) as defense in depth behind the wrapper's check; enclosing-project opt-in lookup for a session cwd below the repository root.
- Operator: after the next `make update` (deploys 2.0.0+dotfiles.8), run `/hooks` in Codex and trust the four hooks; T87 verifies `/compact` lands `pre_compact`/`post_compact` rows.

## CompactionDB

- Worker decision `92a9b538`; orchestrator consolidation `d7a25cb3-bed9-4d91-bd59-ccfcc175cf78`.
