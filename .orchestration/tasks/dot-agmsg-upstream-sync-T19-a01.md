# AGMSG-TASK dot-agmsg-upstream-sync-T19-a01: install agmsg from the upstream npm release through the asset manifest and retire the vendored snapshot and agmsg-dispatch (plan Phase L.7 + Phase 2)

Plan: `.agents/worklog/claude/remediation-plan-20260925.md` §Phase L.7, §Phase 2, §0 item 4. Prerequisite: PR #181 (asset manifest) merged. Repo: your nested worktree, branch `feat/agmsg-upstream-sync` from origin/main. You are `claude-standard-dot-a003`.

## Facts (verified 2026-09-25)
- Upstream: https://github.com/fujibee/agmsg (MIT), npm package `agmsg` latest 1.4.2 (published 2026-09-24), install path `~/.agents/skills/agmsg/`. Upstream ships ~40 scripts incl. `spawn.sh`, `despawn.sh`, `poke.sh`, `peek.sh`, `doctor.sh`, `fix.sh`, `team.sh`, `where.sh`, `placement-collisions.sh`, `version.sh`, terminal drivers (`drivers/`, herdr included), `release/`.
- Vendored copy `home/dot_agents/skills/agmsg/` is a 2026-06-22 snapshot (21 scripts, no VERSION, `version.sh` missing but referenced by `templates/cmd.claude-code.md`), applied by chezmoi; two local fixes in July (executable bits, writable_roots).
- `home/dot_local/bin/common/executable_agmsg-dispatch` (PR #173) reimplements what upstream `poke.sh` + the Codex bridge provide; the agmsg-orchestration SKILL step 6 mandates it.
- State dirs under `~/.agents/skills/agmsg/{teams,db,run,agents}` are live data and must survive.

## Deliverables
1. **Manifest entry**: `assets.agmsg` → `source: npm`, `upstream: agmsg` (registry) + `homepage: https://github.com/fujibee/agmsg`, `pin: 1.4.2`, `integrity: <sha512 from npm view agmsg@1.4.2 dist.integrity>`, `install_path: ~/.agents/skills/agmsg`, `installer: scripts/update-agent-assets.sh#update_agmsg`. Validator: `npm` source requires `integrity`.
2. **Installer step** `update_agmsg` in `scripts/update-agent-assets.sh`: `npm pack agmsg@<pin>` (or `npm view ... dist.tarball` + curl) into a temp dir, verify `integrity` (sha512) against the tarball, extract, and sync ONLY the code parts (`SKILL.md`, `scripts/`, `templates/`, `drivers/`, `internal/`, `lib/` — derive the list from the tarball) into `~/.agents/skills/agmsg/` with `rsync --delete` scoped to those paths, never touching `teams/ db/ run/ agents/`. `manifest_record` step with the version. Idempotent (skip when `version.sh`/VERSION already equals the pin).
3. **Retire the vendored copy**: delete `home/dot_agents/skills/agmsg/**` from chezmoi-managed files (keep nothing local; if a July fix is not upstream, open an upstream issue/PR and record the URL in the report). Ensure `chezmoi apply` does not remove the installed skill (check `.chezmoiignore`/`remove_` semantics) — the skill dir becomes installer-owned, like tode/terminal-browser.
4. **Retire agmsg-dispatch**: remove `home/dot_local/bin/common/executable_agmsg-dispatch` and `tests/unit/test_agmsg_dispatch.py`; update the agmsg-orchestration SKILL (step 4/6), `home/dot_config/claude/rules/agmsg-orchestration.md`, README: orchestrator sends with upstream `send.sh` and, for an idle herdr-paned member, wakes with upstream `poke.sh <team> <name> --body-file` (herdr driver); Codex members use upstream's Codex delivery (bridge/turn) per the upstream README. Redefine the polling rule: upstream `monitor` mode (5 s SQLite stream) is the sanctioned real-time path; no repo-local polling loops.
5. **Delivery setup**: `herdr-agents --bootstrap-agmsg` keeps only what upstream needs (`delivery.sh set monitor claude-code <dir>` default per upstream; Codex per upstream docs) and uses upstream `doctor.sh --project <dir>` output for its identity check instead of the heuristic (coordinate with the T14 guard: keep the guard until Phase 3 lands).
6. **Doctor**: `check-tools.sh` prints the installed agmsg version (`version.sh`) vs manifest pin.
7. **Docs**: README (agmsg section: installed via manifest, how to bump = Renovate/`make upgrade` L.3 later), AGENTS.md if it references the vendored path.

## Tests
- Unit: installer step with fake `npm`/tarball fixture (integrity mismatch → fail; state dirs untouched; code dirs replaced); validator `npm` source rules; SKILL/rules parity checks pass.
- Live E2E (required): run `update_agmsg` against a scratch `HOME` (fake state dirs pre-populated) and prove state survives and code updates; then, in the real environment ONLY IF the orchestrator has confirmed via ACCEPTANCE that `make update` may run (it is orchestrator-owned), stop. Do not run `make update` yourself.

## Validation (verbatim)
Unit tests; validator; generator `--check`; scratch-HOME E2E outputs; `npm view agmsg@1.4.2 dist.integrity version`; `gh pr checks`; `pr-feedback.py <n>` JSON with every item dispositioned (CodeRabbit full review once on the final head, respecting 1/hour).

## allowed_files
`home/dot_agents/agent-config.yaml`, `scripts/update-agent-assets.sh`, `scripts/validate-agent-assets.py`, `scripts/generate-agent-configs.py` (if the npm source needs rendering), `scripts/check-tools.sh`, deletion of `home/dot_agents/skills/agmsg/**` and `home/dot_local/bin/common/executable_agmsg-dispatch`, `tests/unit/test_agmsg_dispatch.py` (delete), new/updated unit tests, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md`, the Codex rules mirror, `home/dot_local/bin/common/executable_herdr-agents` (bootstrap only), `README.md`, `AGENTS.md`, `.chezmoiignore` if needed, artefacts.

## forbidden_actions
`make update`/`make upgrade`/`chezmoi apply` on the real HOME; touching `~/.agents/skills/agmsg/{teams,db,run,agents}`; merging; local bats; force-push; keeping any local fork of upstream scripts.

## Artefacts / Done signal
Standard five + pr-feedback JSON. `[memory:decision]`: "agmsg is installed from the upstream npm release pinned in the asset manifest with sha512 integrity; the vendored snapshot and agmsg-dispatch are retired; orchestrator wake uses upstream poke". RESULT via send.sh (orchestrator reads via monitor). max_turns=50.
