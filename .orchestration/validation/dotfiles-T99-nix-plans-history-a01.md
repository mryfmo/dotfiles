# T99 validation

Task SHA256: 33b6726f7e08fc35a456182059c871140fcafe8077c85f56a75d60dd9a428a32

## Dispatch acknowledgement
```json
{
  "argv": [
    "agmsg-dispatch",
    "dotfiles",
    "codex-security-dot-a007",
    "claude-remediation-dot",
    "wT:p1",
    "AGMSG-PONG v1 task_id=dotfiles-T99 status=active task_rev=verified branch=docs/nix-plans-history plan=move-two-docs-update-test-validate-CI-Bot;worklog-in-report-because-.agents-readonly"
  ],
  "start": "2026-10-05T06:12:11.003818+00:00",
  "end": "2026-10-05T06:12:26.307207+00:00",
  "returncode": 0,
  "stdout": "",
  "stderr": ""
}
```

## 2026-10-05T06:12:39.455271+00:00
```text
$ git rev-parse HEAD
794a80dbf74ec62399edc2a8a03e102f68049bb6
exit_code=0
```

## 2026-10-05T06:12:39.458476+00:00
```text
$ git diff origin/main --stat | tail -5
 docs/{plans => history}/nix-first-architecture.md | 2 ++
 docs/{plans => history}/nix-migration.md          | 2 ++
 plans/004-harden-and-lock-the-supply-chain.md     | 2 +-
 tests/unit/test_aws_cli_acquisition.py            | 4 ++--
 5 files changed, 11 insertions(+), 3 deletions(-)
exit_code=0
```

## 2026-10-05T06:12:39.463685+00:00
```text
$ git ls-files docs/plans docs/history
docs/history/README.md
docs/history/nix-first-architecture.md
docs/history/nix-migration.md
exit_code=0
```

## 2026-10-05T06:12:39.465545+00:00
```text
$ git grep -n 'docs/plans/nix' ; echo "rc=$?"
.orchestration/acceptance/dotfiles-T74-bootstrap-dead-code-a01.md:28:- audit-finding: 2487b05a `flake.nix:1` nix plan documents left stale → not-applicable:`docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` and `plans/004-harden-and-lock-the-supply-chain.md` are plan prose this task was forbidden to edit; the stale lines are enumerated in the T74 report and rewritten by T78/T83
.orchestration/acceptance/dotfiles-T74-bootstrap-dead-code-a01.md:33:- T78/T83: the stale nix sentences listed in the report (`docs/plans/nix-first-architecture.md:16,58,64,70,76`; `docs/plans/nix-migration.md:23-26,33-34,37,110`; `plans/004…:44,64-65,92,109,371,386-393`).
.orchestration/acceptance/dotfiles-T78-dead-docs-adh-a01.md:13:- `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md`: one dated note each that the flake left in #247; bodies untouched (T83 decides their fate).
.orchestration/reports/dotfiles-T74-bootstrap-dead-code-a01.md:39:| 4175951412 P2 "Update Nix documentation after deleting the flake" | 2487b05a | `not-applicable`: `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` are prose owned by T78/T83, and this task forbids editing them. The stale sentences are listed below for those tasks. |
.orchestration/reports/dotfiles-T74-bootstrap-dead-code-a01.md:43:- `docs/plans/nix-first-architecture.md:16, 58, 64, 70, 76`: the flake outputs, the `home-manager switch --flake .#mryfmo-linux/darwin`, `darwin-rebuild switch --flake .#mryfmo-mac` and `nix flake check` commands.
.orchestration/reports/dotfiles-T74-bootstrap-dead-code-a01.md:44:- `docs/plans/nix-migration.md:23-26, 33-34, 37, 110`: add `flake.nix` and the `nix/**` modules, `nix flake show/check`, the "CI evaluates every declared output", and the flake.lock regression procedure.
.orchestration/reports/dotfiles-T78-dead-docs-adh-a01.md:27:   - `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` each get a dated note under the title: the flake was removed in #247, and the commands and paths below no longer apply;
.orchestration/tasks/dotfiles-T74-bootstrap-dead-code-a01.md:13:5. **Nix:** delete `flake.nix`, `flake.lock`, `nix/**`. In `.github/workflows/test.yaml` delete the `should_nix` output (line 21), its filter block (80-84) and the `nix` job (415-437). In `tests/unit/test_supply_chain_policy.py` delete `test_nix_inputs_lock_and_ci_use_2605` (460-473) and any now-unused import. `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` and `plans/004-harden-and-lock-the-supply-chain.md` mention nix: do not edit them (T78/T83 own prose); list the stale sentences in the report.
.orchestration/tasks/dotfiles-T78-dead-docs-adh-a01.md:14:6. Stale nix prose from T74 (`docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md`): add one dated note at the top of each saying the flake was removed in #247 and the commands below no longer apply; do not rewrite the bodies (T83 decides their fate).
.orchestration/tasks/dotfiles-T78-dead-docs-adh-a01.md:27:- `AGENTS.md`, `reviews/**` (delete), `.coderabbit.yaml`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (the four lines named), `home/dot_config/codex/AGENTS.md` (line 9), `.github/copilot-instructions.md` (delete), `home/dot_claude/commands/commit.md`, `plans/README.md`, `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md` (one note each), `tests/unit/test_agmsg_orchestration_docs.py` (only if it pins the deleted phrases)
.orchestration/tasks/dotfiles-T83-docs-diet-a01.md:29:- `home/dot_config/claude/rules/*.md`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_agents/skills/gh-first-workflow/SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`, `home/dot_config/codex/AGENTS.md`, `plans/005-*.md`, `docs/plans/nix-*.md` (move or delete), `plans/004-harden-and-lock-the-supply-chain.md` (the note), `.gitignore` (the one line), `tests/unit/test_agmsg_orchestration_docs.py`, `tests/unit/test_pr_feedback.py`
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-45d44292.md:4412:docs/plans/nix-first-architecture.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-45d44292.md:4413:docs/plans/nix-migration.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-45d44292.md:4734:/usr/bin/zsh -lc "python3 -B -c 'import subprocess,re; s=subprocess.check_output([\"git\",\"show\",\"45d44292:.github/workflows/test.yaml\"],text=True); line=next(l for l in s.splitlines() if \"grep -Eq\" in l and \"should\" not in l); pattern=line.split(\"grep -Eq \")[1].strip().strip(chr(39)).removesuffix(\"; then\").rstrip().rstrip(chr(39)); print(\"filter:\",pattern); print({p:bool(re.search(pattern,p)) for p in [\"ruff.toml\",\".prettierignore\",\"docs/plans/nix-migration.md\",\"plans/README.md\",\"AGENTS.md\",\"README.md\",\"tests/unit/test_generate_agent_configs.py\"]})'" in ~/Workspace/dotfiles
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-45d44292.md:4737:{'ruff.toml': False, '.prettierignore': False, 'docs/plans/nix-migration.md': False, 'plans/README.md': False, 'AGENTS.md': False, 'README.md': True, 'tests/unit/test_generate_agent_configs.py': True}
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-57021632.md:2311:{"id": "document:docs/plans/nix-first-architecture.md", "filePath": "docs/plans/nix-first-architecture.md", "summary": "Architecture plan for an optional Nix layer: chezmoi stays authoritative, initial Nix scope and package ownership, future Nix-first target, activation examples, and non-goals."}
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-57021632.md:2312:{"id": "document:docs/plans/nix-migration.md", "filePath": "docs/plans/nix-migration.md", "summary": "Phased Nix migration plan (opt-in scaffold, package-only adoption, host roles, selective config migration, optional Nix-first bootstrap) with principles and rollback notes."}
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-b5084de5.md:736:> **Drift check**: `git diff --stat e7c2808..HEAD -- setup.sh install home/dot_mise home/dot_config/sheldon home/.chezmoitemplates/chezmoiexternal.d .github/workflows flake.nix flake.lock docs/plans/nix-first-architecture.md tests`
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-e5648fa6.md:2864:> **Drift check**: `git diff --stat e7c2808..HEAD -- setup.sh install home/dot_mise home/dot_config/sheldon home/.chezmoitemplates/chezmoiexternal.d .github/workflows flake.nix flake.lock docs/plans/nix-first-architecture.md tests`
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ff37f41d.md:3407:docs/plans/nix-first-architecture.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ff37f41d.md:3408:docs/plans/nix-migration.md
.orchestration/validation/dot-formatter-hook-root-fix-T61-a01-audit-ff37f41d.md:4487:cases={'AGENTS.md':True,'CLAUDE.md':True,'README.md':True,'plans/004-harden-and-lock-the-supply-chain.md':True,'docs/plans/nix-migration.md':True,'.github/copilot-instructions.md':True,'ruff.toml':True,'.prettierignore':True,'home/dot_claude/hooks/executable_format-edited-files.py':True,'.orchestration/reports/report.md':False,'.ua/knowledge-graph.json':False,'references/example.md':False}
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:7348:      "id": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:7351:      "filePath": "docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:7362:      "id": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:7365:      "filePath": "docs/plans/nix-migration.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:19685:      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:19692:      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:19699:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:19706:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:19713:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:19720:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:19727:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:24695:        "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-herdr-agents-add-worker-T22-a01-audit-r6.md:24696:        "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:9887:      "id": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:9890:      "filePath": "docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:9902:      "id": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:9905:      "filePath": "docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:23113:      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:23120:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:23127:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:23128:      "target": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:28330:        "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-0a34a68.md:28331:        "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-12d3f80.md:2539:12d3f80:.orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit.md:796:{"baseCommit":"d906b00bff8729625b895d6f7765e3186ab5bb86","headCommit":"935e198406e5df993c84de67c695c7083f4b6b54","action":"FULL_UPDATE","deletedFiles":[".github/dependabot.yml"],"cosmeticFiles":["scripts/check-statusline-tools.py","tests/unit/test_statusline_tools.py"],"ignoredFiles":[".orchestration/acceptance/dot-agmsg-upstream-sync-T19-a01.md",".orchestration/acceptance/dot-asset-manifest-T15-a01.md",".orchestration/acceptance/dot-audit-pane-hardening-T32b-a01.md",".orchestration/acceptance/dot-audit-pane-visibility-T32-a01.md",".orchestration/acceptance/dot-audit-verdict-gate-T33b-a01.md",".orchestration/acceptance/dot-claude-sandbox-T13-a01.md",".orchestration/acceptance/dot-codex-apparmor-userns-T30-a01.md",".orchestration/acceptance/dot-env-converge-T10-a01.md",".orchestration/acceptance/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/acceptance/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/acceptance/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/acceptance/dot-orchestration-rules-T33a-a01.md",".orchestration/acceptance/dot-pr-feedback-gate-T16-a01.md",".orchestration/acceptance/dot-restart-worker-name-wait-T27-a01.md",".orchestration/acceptance/dot-three-role-constellation-T28-a01.md",".orchestration/acceptance/dot-ua-full-T9-a01.md",".orchestration/acceptance/dot-version-currency-T29-a01.md",".orchestration/acceptance/dot-worker-advisor-fable-T26-a01.md",".orchestration/acceptance/dot-worker-kind-guard-T14-a01.md",".orchestration/acceptance/dot-worker-profile-opus55-T24-a01.md",".orchestration/acceptance/refkit-P0-01.md",".orchestration/acceptance/refkit-P0-05.md",".orchestration/acceptance/refkit-P0-06.md",".orchestration/acceptance/refkit-P0-07.md",".orchestration/acceptance/refkit-P1.md",".orchestration/acceptance/refkit-P2-A.md",".orchestration/acceptance/refkit-P2-B.md",".orchestration/acceptance/refkit-P2-C.md",".orchestration/acceptance/refkit-P3.md",".orchestration/acceptance/refkit-P4.md",".orchestration/acceptance/refkit-P5.md",".orchestration/acceptance/refkit-P7.md",".orchestration/acceptance/refkit-P8-a.md",".orchestration/acceptance/refkit-P8-b.md",".orchestration/acceptance/remote-diff-01.md",".orchestration/autoskill/runs/dot-asset-manifest-T15-a01.md",".orchestration/autoskill/runs/dot-audit-pane-hardening-T32b-a01.md",".orchestration/autoskill/runs/dot-audit-pane-visibility-T32-a01.md",".orchestration/autoskill/runs/dot-audit-verdict-gate-T33b-a01.md",".orchestration/autoskill/runs/dot-codex-apparmor-userns-T30-a01.md",".orchestration/autoskill/runs/dot-env-converge-T10-a01.md",".orchestration/autoskill/runs/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/autoskill/runs/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/autoskill/runs/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/autoskill/runs/dot-orchestration-rules-T33a-a01.md",".orchestration/autoskill/runs/dot-restart-worker-name-wait-T27-a01.md",".orchestration/autoskill/runs/dot-three-role-constellation-T28-a01.md",".orchestration/autoskill/runs/dot-ua-full-T9-a01.md",".orchestration/autoskill/runs/dot-version-currency-T29-a01.md",".orchestration/autoskill/runs/dot-worker-advisor-fable-T26-a01.md",".orchestration/autoskill/runs/dot-worker-kind-guard-T14-a01.md",".orchestration/autoskill/runs/dot-worker-profile-opus55-T24-a01.md",".orchestration/autoskill/runs/remote-diff-01.md",".orchestration/learning/dot-asset-manifest-T15-a01.md",".orchestration/learning/dot-audit-pane-hardening-T32b-a01.md",".orchestration/learning/dot-audit-pane-visibility-T32-a01.md",".orchestration/learning/dot-audit-verdict-gate-T33b-a01.md",".orchestration/learning/dot-codex-apparmor-userns-T30-a01.md",".orchestration/learning/dot-env-converge-T10-a01.md",".orchestration/learning/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/learning/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/learning/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/learning/dot-orchestration-rules-T33a-a01.md",".orchestration/learning/dot-restart-worker-name-wait-T27-a01.md",".orchestration/learning/dot-three-role-constellation-T28-a01.md",".orchestration/learning/dot-ua-full-T9-a01.md",".orchestration/learning/dot-version-currency-T29-a01.md",".orchestration/learning/dot-worker-advisor-fable-T26-a01.md",".orchestration/learning/dot-worker-kind-guard-T14-a01.md",".orchestration/learning/dot-worker-profile-opus55-T24-a01.md",".orchestration/learning/remote-diff-01.md",".orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md",".orchestration/learning/rule_candidates/herdr-worker-relaunch.md",".orchestration/reports/P0-04-sources.md",".orchestration/reports/dot-asset-manifest-T15-a01.md",".orchestration/reports/dot-audit-pane-hardening-T32b-a01.md",".orchestration/reports/dot-audit-pane-visibility-T32-a01.md",".orchestration/reports/dot-audit-verdict-gate-T33b-a01.md",".orchestration/reports/dot-claude-sandbox-T13-a01.md",".orchestration/reports/dot-codex-apparmor-userns-T30-a01.md",".orchestration/reports/dot-env-converge-T10-a01.md",".orchestration/reports/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/reports/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/reports/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/reports/dot-orchestration-rules-T33a-a01.md",".orchestration/reports/dot-restart-worker-name-wait-T27-a01.md",".orchestration/reports/dot-three-role-constellation-T28-a01.md",".orchestration/reports/dot-ua-full-T9-a01.md",".orchestration/reports/dot-version-currency-T29-a01.md",".orchestration/reports/dot-worker-advisor-fable-T26-a01.md",".orchestration/reports/dot-worker-kind-guard-T14-a01.md",".orchestration/reports/dot-worker-profile-opus55-T24-a01.md",".orchestration/reports/remote-diff-01.md",".orchestration/sandboxes/dot-asset-manifest-T15-a01.md",".orchestration/sandboxes/dot-audit-pane-hardening-T32b-a01.md",".orchestration/sandboxes/dot-audit-pane-visibility-T32-a01.md",".orchestration/sandboxes/dot-audit-verdict-gate-T33b-a01.md",".orchestration/sandboxes/dot-codex-apparmor-userns-T30-a01.md",".orchestration/sandboxes/dot-env-converge-T10-a01.md",".orchestration/sandboxes/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/sandboxes/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/sandboxes/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/sandboxes/dot-orchestration-rules-T33a-a01.md",".orchestration/sandboxes/dot-restart-worker-name-wait-T27-a01.md",".orchestration/sandboxes/dot-three-role-constellation-T28-a01.md",".orchestration/sandboxes/dot-ua-full-T9-a01.md",".orchestration/sandboxes/dot-version-currency-T29-a01.md",".orchestration/sandboxes/dot-worker-advisor-fable-T26-a01.md",".orchestration/sandboxes/dot-worker-kind-guard-T14-a01.md",".orchestration/sandboxes/dot-worker-profile-opus55-T24-a01.md",".orchestration/sandboxes/remote-diff-01.md",".orchestration/tasks/dot-agmsg-upstream-sync-T19-a01.md",".orchestration/tasks/dot-asset-manifest-T15-a01.md",".orchestration/tasks/dot-audit-exec-channel-T33e-a01.md",".orchestration/tasks/dot-audit-pane-hardening-T32b-a01.md",".orchestration/tasks/dot-audit-pane-visibility-T32-a01.md",".orchestration/tasks/dot-audit-verdict-gate-T33b-a01.md",".orchestration/tasks/dot-claude-sandbox-T13-a01.md",".orchestration/tasks/dot-codex-apparmor-userns-T30-a01.md",".orchestration/tasks/dot-env-converge-T10-a01.md",".orchestration/tasks/dot-herdr-agents-add-worker-T22-a01.md",".orchestration/tasks/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/tasks/dot-herdr-worker-worktree-T11-a01.md",".orchestration/tasks/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/tasks/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/tasks/dot-orchestration-rules-T33a-a01.md",".orchestration/tasks/dot-orchestrator-guardrails-T21-a01.md",".orchestration/tasks/dot-permgate-bench-flake-T33d-a01.md",".orchestration/tasks/dot-pr-feedback-gate-T16-a01.md",".orchestration/tasks/dot-restart-worker-name-wait-T27-a01.md",".orchestration/tasks/dot-runner-label-pin-T18-a01.md",".orchestration/tasks/dot-task-contract-v2-T23-a01.md",".orchestration/tasks/dot-three-role-constellation-T28-a01.md",".orchestration/tasks/dot-ua-full-T9-a01.md",".orchestration/tasks/dot-ua-graph-refresh-T33c-a01.md",".orchestration/tasks/dot-ua-hook-regex-T12-a01.md",".orchestration/tasks/dot-ua-incremental-T20-a01.md",".orchestration/tasks/dot-version-currency-T29-a01.md",".orchestration/tasks/dot-worker-advisor-fable-T26-a01.md",".orchestration/tasks/dot-worker-kind-guard-T14-a01.md",".orchestration/tasks/dot-worker-profile-opus55-T24-a01.md",".orchestration/tasks/refkit-P0-01.md",".orchestration/tasks/refkit-P0-05.md",".orchestration/tasks/refkit-P0-06.md",".orchestration/tasks/refkit-P0-07.md",".orchestration/tasks/refkit-P1.md",".orchestration/tasks/refkit-P10.md",".orchestration/tasks/refkit-P2-A.md",".orchestration/tasks/refkit-P2-B.md",".orchestration/tasks/refkit-P2-C.md",".orchestration/tasks/refkit-P3.md",".orchestration/tasks/refkit-P4.md",".orchestration/tasks/refkit-P4b.md",".orchestration/tasks/refkit-P5.md",".orchestration/tasks/refkit-P6.md",".orchestration/tasks/refkit-P7.md",".orchestration/tasks/refkit-P8-a.md",".orchestration/tasks/refkit-P8-b.md",".orchestration/tasks/refkit-P8.md",".orchestration/tasks/refkit-P9.md",".orchestration/validation/baseline-20260925.md",".orchestration/validation/dot-asset-manifest-T15-a01.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-audit.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-crit.json",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-live-e2e.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-receipt.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-crit.json",".orchestration/validation/dot-audit-pane-visibility-T32-a01-live-e2e.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-receipt.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev2.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev3.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-crit.json",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-live-e2e.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-receipt.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01.md",".orchestration/validation/dot-claude-sandbox-T13-a01.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-audit.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-crit.json",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-receipt.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01.md",".orchestration/validation/dot-env-converge-T10-a01.md",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01-crit.json",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01-receipt.md",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/validation/dot-macos-crit-pinned-install-T17-a01-crit.json",".orchestration/validation/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-audit.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-crit.json",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-receipt.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-audit-rev3.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-audit.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-crit.json",".orchestration/validation/dot-orchestration-rules-T33a-a01-receipt.md",".orchestration/validation/dot-orchestration-rules-T33a-a01.md",".orchestration/validation/dot-restart-worker-name-wait-T27-a01-crit.json",".orchestration/validation/dot-restart-worker-name-wait-T27-a01-receipt.md",".orchestration/validation/dot-restart-worker-name-wait-T27-a01.md",".orchestration/validation/dot-three-role-constellation-T28-a01-audit.md",".orchestration/validation/dot-three-role-constellation-T28-a01-crit.json",".orchestration/validation/dot-three-role-constellation-T28-a01-receipt.md",".orchestration/validation/dot-three-role-constellation-T28-a01.md",".orchestration/validation/dot-ua-full-T9-a01.md",".orchestration/validation/dot-version-currency-T29-a01-audit.md",".orchestration/validation/dot-version-currency-T29-a01-crit.json",".orchestration/validation/dot-version-currency-T29-a01-receipt.md",".orchestration/validation/dot-version-currency-T29-a01.md",".orchestration/validation/dot-worker-advisor-fable-T26-a01-crit.json",".orchestration/validation/dot-worker-advisor-fable-T26-a01-receipt.md",".orchestration/validation/dot-worker-advisor-fable-T26-a01.md",".orchestration/validation/dot-worker-kind-guard-T14-a01.md",".orchestration/validation/dot-worker-profile-opus55-T24-a01-crit.json",".orchestration/validation/dot-worker-profile-opus55-T24-a01-receipt.md",".orchestration/validation/dot-worker-profile-opus55-T24-a01.md",".orchestration/validation/remote-diff-01.md","home/dot_mise/mise.lock"],"generatedArtifactFiles":[".ua/.understandignore",".ua/fingerprints.json",".ua/knowledge-graph.json",".ua/meta.json"],"importMapRefreshPaths":[".chezmoiroot",".claude/contextdb/config.json",".claude/contextdb/contextdb/__init__.py",".claude/contextdb/contextdb/cli.py",".claude/contextdb/contextdb/config.py",".claude/contextdb/contextdb/hook.py",".claude/contextdb/contextdb/memory.py",".claude/contextdb/contextdb/normalize.py",".claude/contextdb/contextdb/paths.py",".claude/contextdb/contextdb/probe.py",".claude/contextdb/contextdb/recall.py",".claude/contextdb/contextdb/recover_hook.py",".claude/contextdb/contextdb/recovery.py",".claude/contextdb/contextdb/redaction.py",".claude/contextdb/contextdb/semantic.py",".claude/contextdb/contextdb/spool.py",".claude/contextdb/contextdb/storage.py",".claude/contextdb/contextdb/util.py",".claude/contextdb/health/.gitkeep",".claude/contextdb/spool/incoming/.gitkeep",".claude/contextdb/spool/quarantine/.gitkeep",".claude/contextdb/state/.gitkeep",".claude/hooks/contextdb_cli.py",".claude/hooks/contextdb_hook.py",".claude/hooks/contextdb_recover.py",".claude/hooks/query_log.py",".claude/settings.json",".github/copilot-instructions.md",".github/funding.yaml",".github/workflows/agent-assets.yml",".github/workflows/docs.yml",".github/workflows/macos.yaml",".github/workflows/remote.yaml",".github/workflows/test.yaml",".github/workflows/ubuntu.yaml",".simplecov","AGENTS.md","CLAUDE.md","Dockerfile","Makefile","README.md","codecov.yml","docs/assets/stylesheets/extra.css","docs/plans/nix-first-architecture.md","docs/plans/nix-migration.md","docs/verification/acceptance/005.md","flake.nix","home/.chezmoi.yaml.tmpl","home/.chezmoiexternal.yaml.tmpl","home/.chezmoiignore","home/.chezmoiremove","home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl","home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl","home/.chezmoiscripts/common/run_once_after_03-install-sheldon.sh.tmpl","home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl","home/.chezmoiscripts/common/run_once_after_99-install-gh-extensions.sh.tmpl","home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl","home/.chezmoiscripts/macos/run_once_04-install-ghostty.sh.tmpl","home/.chezmoiscripts/macos/run_once_10-install-docker.sh.tmpl","home/.chezmoiscripts/macos/run_once_99-install-defaults.sh.tmpl","home/.chezmoiscripts/macos/run_once_after_50-install-misc.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_01-prepare-system.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_02-install-command-line-tool.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_03-install-brew.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_50-install-dependencies.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_00-setup-ssh.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_10-install-docker.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_10-install-starship.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-docker-ssh.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-install-mics.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_51-client-default-shell.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_after_04-install-aws-cli.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_before_50-common-dependencies.sh.tmpl","home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl","home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl","home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl","home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl","home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl","home/.chezmoitemplates/chezmoiignore.d/common","home/.chezmoitemplates/chezmoiignore.d/macos","home/.chezmoitemplates/chezmoiignore.d/ubuntu/client","home/.chezmoitemplates/chezmoiignore.d/ubuntu/common","home/.chezmoitemplates/chezmoiignore.d/ubuntu/server","home/.chezmoitemplates/claude-settings-managed.json","home/.chezmoitemplates/codex-config-managed.toml","home/.key.txt.age","home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl","home/dot_agents/README.md","home/dot_agents/agent-config.yaml","home/dot_agents/model-profiles.env","home/dot_agents/permgate-policy.yaml","home/dot_agents/plugins/create_marketplace.json","home/dot_agents/plugins/mryfmo-dev-workflows/.codex-plugin/plugin.json","home/dot_agents/skills/agmsg-orchestration/SKILL.md","home/dot_agents/skills/agmsg/SKILL.md","home/dot_agents/skills/agmsg/agents/openai.yaml","home/dot_agents/skills/agmsg/db/.keep","home/dot_agents/skills/agmsg/run/.keep","home/dot_agents/skills/agmsg/scripts/executable_actas-claim.sh","home/dot_agents/skills/agmsg/scripts/executable_check-inbox.sh","home/dot_agents/skills/agmsg/scripts/executable_config.sh","home/dot_agents/skills/agmsg/scripts/executable_delivery.sh","home/dot_agents/skills/agmsg/scripts/executable_history.sh","home/dot_agents/skills/agmsg/scripts/executable_hook.sh","home/dot_agents/skills/agmsg/scripts/executable_identities.sh","home/dot_agents/skills/agmsg/scripts/executable_inbox.sh","home/dot_agents/skills/agmsg/scripts/executable_init-db.sh","home/dot_agents/skills/agmsg/scripts/executable_join.sh","home/dot_agents/skills/agmsg/scripts/executable_leave.sh","home/dot_agents/skills/agmsg/scripts/executable_rename-team.sh","home/dot_agents/skills/agmsg/scripts/executable_rename.sh","home/dot_agents/skills/agmsg/scripts/executable_reset.sh","home/dot_agents/skills/agmsg/scripts/executable_send.sh","home/dot_agents/skills/agmsg/scripts/executable_session-end.sh","home/dot_agents/skills/agmsg/scripts/executable_session-start.sh","home/dot_agents/skills/agmsg/scripts/executable_team.sh","home/dot_agents/skills/agmsg/scripts/executable_watch.sh","home/dot_agents/skills/agmsg/scripts/executable_whoami.sh","home/dot_agents/skills/agmsg/scripts/lib/actas-lock.sh","home/dot_agents/skills/agmsg/scripts/lib/identifier.sh","home/dot_agents/skills/agmsg/scripts/lib/storage.sh","home/dot_agents/skills/agmsg/scripts/release/executable_sync-version.sh","home/dot_agents/skills/agmsg/teams/.keep","home/dot_agents/skills/agmsg/templates/cmd.antigravity.md","home/dot_agents/skills/agmsg/templates/cmd.claude-code.md","home/dot_agents/skills/agmsg/templates/cmd.codex.md","home/dot_agents/skills/agmsg/templates/cmd.copilot.md","home/dot_agents/skills/agmsg/templates/cmd.gemini.md","home/dot_agents/skills/convert-to-transformers/SKILL.md","home/dot_agents/skills/convert-to-transformers/references/common-pitfalls.md","home/dot_agents/skills/convert-to-transformers/references/learnings.md","home/dot_agents/skills/gh-comment-attach-files/SKILL.md","home/dot_agents/skills/gh-comment-attach-files/agents/openai.yaml","home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py","home/dot_agents/skills/gh-first-workflow/SKILL.md","home/dot_agents/skills/gh-first-workflow/agents/openai.yaml","home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md","home/dot_agents/skills/humanizer-ja/SKILL.md","home/dot_agents/skills/humanizer-ja/agents/openai.yaml","home/dot_agents/skills/humanizer-ja/references/ai-patterns-ja.md","home/dot_agents/skills/python-uv-workflow/SKILL.md","home/dot_agents/skills/python-uv-workflow/agents/openai.yaml","home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md","home/dot_agents/skills/shdoc-shell-docs/SKILL.md","home/dot_agents/skills/shdoc-shell-docs/agents/openai.yaml","home/dot_agents/skills/shdoc-shell-docs/references/shdoc-rules.md","home/dot_bash/client/bashrc","home/dot_bash/server/bashrc","home/dot_ccstatusline/settings.json","home/dot_claude/agents/express-explorer.md","home/dot_claude/commands/commit.md","home/dot_claude/commands/symlink_agmsg.md.tmpl","home/dot_claude/hooks/executable_enforce-uv.sh","home/dot_claude/hooks/executable_format-edited-files.py","home/dot_claude/modify_private_settings.json","home/dot_claude/private_mcp.json.tmpl","home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl","home/dot_claude/rules/symlink_ask-user-question.md.tmpl","home/dot_claude/rules/symlink_compactiondb.md.tmpl","home/dot_claude/rules/symlink_crit-review.md.tmpl","home/dot_claude/rules/symlink_gpu.md.tmpl","home/dot_claude/rules/symlink_latex.md.tmpl","home/dot_claude/rules/symlink_model-selection.md.tmpl","home/dot_claude/rules/symlink_ponytail.md.tmpl","home/dot_claude/rules/symlink_python.md.tmpl","home/dot_claude/rules/symlink_understand-anything.md.tmpl","home/dot_claude/skills/agmsg-orchestration/symlink_SKILL.md.tmpl","home/dot_claude/skills/agmsg/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_actas-lock.sh.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_identifier.sh.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_storage.sh.tmpl","home/dot_claude/skills/agmsg/scripts/release/symlink_sync-version.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_actas-claim.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_check-inbox.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_config.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_delivery.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_history.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_hook.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_identities.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_inbox.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_init-db.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_join.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_leave.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_rename-team.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_rename.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_reset.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_send.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_session-end.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_session-start.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_team.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_watch.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_whoami.sh.tmpl","home/dot_claude/skills/agmsg/symlink_SKILL.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.antigravity.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.claude-code.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.codex.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.copilot.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.gemini.md.tmpl","home/dot_claude/skills/convert-to-transformers/references/symlink_common-pitfalls.md.tmpl","home/dot_claude/skills/convert-to-transformers/references/symlink_learnings.md.tmpl","home/dot_claude/skills/convert-to-transformers/symlink_SKILL.md.tmpl","home/dot_claude/skills/gh-comment-attach-files/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/gh-comment-attach-files/scripts/symlink_attach_comment_files.py.tmpl","home/dot_claude/skills/gh-comment-attach-files/symlink_SKILL.md.tmpl","home/dot_claude/skills/gh-first-workflow/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/gh-first-workflow/references/symlink_gh-git-rules.md.tmpl","home/dot_claude/skills/gh-first-workflow/symlink_SKILL.md.tmpl","home/dot_claude/skills/humanizer-ja/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/humanizer-ja/references/symlink_ai-patterns-ja.md.tmpl","home/dot_claude/skills/humanizer-ja/symlink_SKILL.md.tmpl","home/dot_claude/skills/python-uv-workflow/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/python-uv-workflow/references/symlink_python-uv-rules.md.tmpl","home/dot_claude/skills/python-uv-workflow/symlink_SKILL.md.tmpl","home/dot_claude/skills/shdoc-shell-docs/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/shdoc-shell-docs/references/symlink_shdoc-rules.md.tmpl","home/dot_claude/skills/shdoc-shell-docs/symlink_SKILL.md.tmpl","home/dot_codex/modify_private_adh.config.toml","home/dot_codex/modify_private_audit.config.toml","home/dot_codex/modify_private_config.toml","home/dot_codex/modify_private_deep.config.toml","home/dot_codex/modify_private_express.config.toml","home/dot_codex/modify_private_review.config.toml","home/dot_codex/modify_private_security.config.toml","home/dot_codex/modify_private_standard.config.toml","home/dot_codex/symlink_AGENTS.md.tmpl","home/dot_config/alias/client.sh","home/dot_config/alias/common.sh","home/dot_config/alias/server.sh","home/dot_config/ccstatusline/symlink_settings.json.tmpl","home/dot_config/claude/rules/agmsg-orchestration.md","home/dot_config/claude/rules/ask-user-question.md","home/dot_config/claude/rules/compactiondb.md","home/dot_config/claude/rules/crit-review.md","home/dot_config/claude/rules/gpu.md","home/dot_config/claude/rules/latex.md","home/dot_config/claude/rules/model-selection.md","home/dot_config/claude/rules/ponytail.md","home/dot_config/claude/rules/python.md","home/dot_config/claude/rules/understand-anything.md","home/dot_config/codex/AGENTS.md","home/dot_config/ghostty/config","home/dot_config/git/config.tmpl","home/dot_config/git/ignore","home/dot_config/gwq/config.toml","home/dot_config/herdr/config.toml","home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml","home/dot_config/mise/config.toml.tmpl","home/dot_config/mise/mise.lock.tmpl","home/dot_config/powerlevel10k/p10k.zsh","home/dot_config/sheldon/plugin_sources/client/common.toml","home/dot_config/sheldon/plugin_sources/client/macos.toml","home/dot_config/sheldon/plugin_sources/client/ubuntu.toml","home/dot_config/sheldon/plugin_sources/common.toml","home/dot_config/sheldon/plugin_sources/server.toml","home/dot_config/sheldon/plugins.toml.tmpl","home/dot_config/starship.toml","home/dot_config/systemd/user/usage-snapshot.service.tmpl","home/dot_config/systemd/user/usage-snapshot.timer.tmpl","home/dot_config/tango.yml","home/dot_config/uv/uv.toml","home/dot_config/yazi/yazi.toml","home/dot_config/zed/keymap.json","home/dot_config/zed/settings.json","home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh","home/dot_local/bin/common/executable_agent-fanout","home/dot_local/bin/common/executable_agent-session-staleness","home/dot_local/bin/common/executable_agmsg-dispatch","home/dot_local/bin/common/executable_cdgwq","home/dot_local/bin/common/executable_cdw","home/dot_local/bin/common/executable_chezmoi-cd","home/dot_local/bin/common/executable_compactiondb-install","home/dot_local/bin/common/executable_contextdb-codex-notify","home/dot_local/bin/common/executable_dev","home/dot_local/bin/common/executable_fgc","home/dot_local/bin/common/executable_git-delete-merged-branches","home/dot_local/bin/common/executable_herdr-agents","home/dot_local/bin/common/executable_herdr-session","home/dot_local/bin/common/executable_permgate","home/dot_local/bin/common/executable_provision-machine-key","home/dot_local/bin/common/executable_remove-agent-asset","home/dot_local/bin/common/executable_setup-gh","home/dot_local/bin/common/executable_setup-gpg","home/dot_local/bin/common/executable_setup-python-env","home/dot_local/bin/common/executable_uv-format","home/dot_local/bin/server/cache.sh","home/dot_local/bin/server/cuda.sh","home/dot_local/bin/server/history.sh","home/dot_local/bin/server/ssh_agent.sh","home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc","home/dot_mise/config.toml","home/dot_npmrc","home/dot_profile","home/dot_vimrc","home/dot_zprofile","home/dot_zshenv","home/dot_zshrc","home/private_dot_gnupg/gpg-agent.conf.tmpl","home/private_dot_ssh/private_config","home/symlink_dot_bashrc.tmpl","install/common/chezmoi_private.sh","install/common/gh_extensions.sh","install/common/mise.sh","install/common/sheldon.sh","install/macos/arm64/prepare_arm64_system.sh","install/macos/arm64/run.sh","install/macos/common/brew.sh","install/macos/common/command_line_tool.sh","install/macos/common/defaults.sh","install/macos/common/dependencies.sh","install/macos/common/docker.sh","install/macos/common/ghostty.sh","install/macos/common/misc.sh","install/ubuntu/client/default_shell.sh","install/ubuntu/client/docker.sh","install/ubuntu/client/ghostty.sh","install/ubuntu/client/gnome_settings.sh","install/ubuntu/client/misc.sh","install/ubuntu/client/tailscale.sh","install/ubuntu/client/zed.sh","install/ubuntu/common/apparmor/bwrap-userns","install/ubuntu/common/apparmor_userns.sh","install/ubuntu/common/aws_cli.sh","install/ubuntu/common/dependencies.sh","install/ubuntu/common/setup_locale.sh","install/ubuntu/common/ssh.sh","install/ubuntu/server/misc.sh","install/ubuntu/server/setup_timezone.sh","install/ubuntu/server/ssh_server.sh","install/ubuntu/server/starship.sh","mise.toml","mkdocs.yml","nix/home-manager/default.nix","nix/nix-darwin/default.nix","nix/shared/packages.nix","plans/001-contain-starship-cleanup.md","plans/002-make-review-evidence-non-vacuous.md","plans/003-make-bootstrap-safe-and-publicly-testable.md","plans/004-harden-and-lock-the-supply-chain.md","plans/005-make-runtime-health-and-verification-truthful.md","plans/README.md","renovate.json","scripts/check-agent-runtime.py","scripts/check-statusline-tools.py","scripts/check-tools.sh","scripts/generate-agent-configs.py","scripts/generate-docs.sh","scripts/lib/asset-manifest.sh","scripts/lib/installer-pins.sh","scripts/refresh-mkdocs-toc.py","scripts/require-crit-review.py","scripts/run_bashcov_unit_test.rb","scripts/run_benchmark.sh","scripts/run_unit_test.sh","scripts/update-agent-assets.sh","scripts/upgrade-tools.sh","scripts/usage-report.py","scripts/usage-snapshot.sh","scripts/validate-agent-assets.py","setup.sh","tests/files/common.bats","tests/files/helpers.bash","tests/files/macos.bats","tests/files/ubuntu.bats","tests/install/common/check_tools.bats","tests/install/common/chezmoi_private.bats","tests/install/common/decrypt_private_key.bats","tests/install/common/gh_extensions.bats","tests/install/common/lifecycle.bats","tests/install/common/mise.bats","tests/install/common/private_layer.bats","tests/install/common/provision_machine_key.bats","tests/install/common/setup.bats","tests/install/macos/common/brew.bats","tests/install/macos/common/defaults.bats","tests/install/macos/common/docker.bats","tests/install/macos/common/ghostty.bats","tests/install/macos/common/misc.bats","tests/install/ubuntu/client/default_shell.bats","tests/install/ubuntu/client/docker.bats","tests/install/ubuntu/client/ghostty.bats","tests/install/ubuntu/client/gnome_settings.bats","tests/install/ubuntu/client/misc.bats","tests/install/ubuntu/client/tailscale.bats","tests/install/ubuntu/client/zed.bats","tests/install/ubuntu/common/dependencies.bats","tests/install/ubuntu/common/dependencies_unit.bats","tests/install/ubuntu/common/setup_locale.bats","tests/install/ubuntu/common/ssh.bats","tests/install/ubuntu/server/setup_timezone.bats","tests/install/ubuntu/server/sheldon.bats","tests/install/ubuntu/server/starship.bats","tests/unit/test_agent_session_staleness.py","tests/unit/test_agmsg_dispatch.py","tests/unit/test_agmsg_send.py","tests/unit/test_apparmor_userns.py","tests/unit/test_asset_manifest.py","tests/unit/test_aws_cli_acquisition.py","tests/unit/test_check_agent_runtime.py","tests/unit/test_claude_settings_merge.py","tests/unit/test_codex_config_merge.py","tests/unit/test_contextdb_codex_notify.py","tests/unit/test_files_fixture.py","tests/unit/test_generate_agent_configs.py","tests/unit/test_herdr_agents.py","tests/unit/test_permgate.py","tests/unit/test_release_asset_pins.py","tests/unit/test_remove_agent_asset.py","tests/unit/test_require_crit_review.py","tests/unit/test_runtime_health.py","tests/unit/test_statusline_tools.py","tests/unit/test_supply_chain_policy.py","tests/unit/test_usage_review.py","tests/unit/test_validate_agent_assets.py","tests/unit/test_workflow_security.py"],"rerunArchitecture":true,"rerunTour":true,"reason":"44 files have structural changes (>30 files) — full rebuild recommended"}
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-12d3f80.md:2543:12d3f80:.orchestration/validation/dot-ua-graph-refresh-T33c-a01.md:46:{"baseCommit":"d906b00bff8729625b895d6f7765e3186ab5bb86","headCommit":"935e198406e5df993c84de67c695c7083f4b6b54","action":"FULL_UPDATE","deletedFiles":[".github/dependabot.yml"],"cosmeticFiles":["scripts/check-statusline-tools.py","tests/unit/test_statusline_tools.py"],"ignoredFiles":[".orchestration/acceptance/dot-agmsg-upstream-sync-T19-a01.md",".orchestration/acceptance/dot-asset-manifest-T15-a01.md",".orchestration/acceptance/dot-audit-pane-hardening-T32b-a01.md",".orchestration/acceptance/dot-audit-pane-visibility-T32-a01.md",".orchestration/acceptance/dot-audit-verdict-gate-T33b-a01.md",".orchestration/acceptance/dot-claude-sandbox-T13-a01.md",".orchestration/acceptance/dot-codex-apparmor-userns-T30-a01.md",".orchestration/acceptance/dot-env-converge-T10-a01.md",".orchestration/acceptance/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/acceptance/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/acceptance/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/acceptance/dot-orchestration-rules-T33a-a01.md",".orchestration/acceptance/dot-pr-feedback-gate-T16-a01.md",".orchestration/acceptance/dot-restart-worker-name-wait-T27-a01.md",".orchestration/acceptance/dot-three-role-constellation-T28-a01.md",".orchestration/acceptance/dot-ua-full-T9-a01.md",".orchestration/acceptance/dot-version-currency-T29-a01.md",".orchestration/acceptance/dot-worker-advisor-fable-T26-a01.md",".orchestration/acceptance/dot-worker-kind-guard-T14-a01.md",".orchestration/acceptance/dot-worker-profile-opus55-T24-a01.md",".orchestration/acceptance/refkit-P0-01.md",".orchestration/acceptance/refkit-P0-05.md",".orchestration/acceptance/refkit-P0-06.md",".orchestration/acceptance/refkit-P0-07.md",".orchestration/acceptance/refkit-P1.md",".orchestration/acceptance/refkit-P2-A.md",".orchestration/acceptance/refkit-P2-B.md",".orchestration/acceptance/refkit-P2-C.md",".orchestration/acceptance/refkit-P3.md",".orchestration/acceptance/refkit-P4.md",".orchestration/acceptance/refkit-P5.md",".orchestration/acceptance/refkit-P7.md",".orchestration/acceptance/refkit-P8-a.md",".orchestration/acceptance/refkit-P8-b.md",".orchestration/acceptance/remote-diff-01.md",".orchestration/autoskill/runs/dot-asset-manifest-T15-a01.md",".orchestration/autoskill/runs/dot-audit-pane-hardening-T32b-a01.md",".orchestration/autoskill/runs/dot-audit-pane-visibility-T32-a01.md",".orchestration/autoskill/runs/dot-audit-verdict-gate-T33b-a01.md",".orchestration/autoskill/runs/dot-codex-apparmor-userns-T30-a01.md",".orchestration/autoskill/runs/dot-env-converge-T10-a01.md",".orchestration/autoskill/runs/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/autoskill/runs/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/autoskill/runs/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/autoskill/runs/dot-orchestration-rules-T33a-a01.md",".orchestration/autoskill/runs/dot-restart-worker-name-wait-T27-a01.md",".orchestration/autoskill/runs/dot-three-role-constellation-T28-a01.md",".orchestration/autoskill/runs/dot-ua-full-T9-a01.md",".orchestration/autoskill/runs/dot-version-currency-T29-a01.md",".orchestration/autoskill/runs/dot-worker-advisor-fable-T26-a01.md",".orchestration/autoskill/runs/dot-worker-kind-guard-T14-a01.md",".orchestration/autoskill/runs/dot-worker-profile-opus55-T24-a01.md",".orchestration/autoskill/runs/remote-diff-01.md",".orchestration/learning/dot-asset-manifest-T15-a01.md",".orchestration/learning/dot-audit-pane-hardening-T32b-a01.md",".orchestration/learning/dot-audit-pane-visibility-T32-a01.md",".orchestration/learning/dot-audit-verdict-gate-T33b-a01.md",".orchestration/learning/dot-codex-apparmor-userns-T30-a01.md",".orchestration/learning/dot-env-converge-T10-a01.md",".orchestration/learning/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/learning/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/learning/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/learning/dot-orchestration-rules-T33a-a01.md",".orchestration/learning/dot-restart-worker-name-wait-T27-a01.md",".orchestration/learning/dot-three-role-constellation-T28-a01.md",".orchestration/learning/dot-ua-full-T9-a01.md",".orchestration/learning/dot-version-currency-T29-a01.md",".orchestration/learning/dot-worker-advisor-fable-T26-a01.md",".orchestration/learning/dot-worker-kind-guard-T14-a01.md",".orchestration/learning/dot-worker-profile-opus55-T24-a01.md",".orchestration/learning/remote-diff-01.md",".orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md",".orchestration/learning/rule_candidates/herdr-worker-relaunch.md",".orchestration/reports/P0-04-sources.md",".orchestration/reports/dot-asset-manifest-T15-a01.md",".orchestration/reports/dot-audit-pane-hardening-T32b-a01.md",".orchestration/reports/dot-audit-pane-visibility-T32-a01.md",".orchestration/reports/dot-audit-verdict-gate-T33b-a01.md",".orchestration/reports/dot-claude-sandbox-T13-a01.md",".orchestration/reports/dot-codex-apparmor-userns-T30-a01.md",".orchestration/reports/dot-env-converge-T10-a01.md",".orchestration/reports/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/reports/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/reports/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/reports/dot-orchestration-rules-T33a-a01.md",".orchestration/reports/dot-restart-worker-name-wait-T27-a01.md",".orchestration/reports/dot-three-role-constellation-T28-a01.md",".orchestration/reports/dot-ua-full-T9-a01.md",".orchestration/reports/dot-version-currency-T29-a01.md",".orchestration/reports/dot-worker-advisor-fable-T26-a01.md",".orchestration/reports/dot-worker-kind-guard-T14-a01.md",".orchestration/reports/dot-worker-profile-opus55-T24-a01.md",".orchestration/reports/remote-diff-01.md",".orchestration/sandboxes/dot-asset-manifest-T15-a01.md",".orchestration/sandboxes/dot-audit-pane-hardening-T32b-a01.md",".orchestration/sandboxes/dot-audit-pane-visibility-T32-a01.md",".orchestration/sandboxes/dot-audit-verdict-gate-T33b-a01.md",".orchestration/sandboxes/dot-codex-apparmor-userns-T30-a01.md",".orchestration/sandboxes/dot-env-converge-T10-a01.md",".orchestration/sandboxes/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/sandboxes/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/sandboxes/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/sandboxes/dot-orchestration-rules-T33a-a01.md",".orchestration/sandboxes/dot-restart-worker-name-wait-T27-a01.md",".orchestration/sandboxes/dot-three-role-constellation-T28-a01.md",".orchestration/sandboxes/dot-ua-full-T9-a01.md",".orchestration/sandboxes/dot-version-currency-T29-a01.md",".orchestration/sandboxes/dot-worker-advisor-fable-T26-a01.md",".orchestration/sandboxes/dot-worker-kind-guard-T14-a01.md",".orchestration/sandboxes/dot-worker-profile-opus55-T24-a01.md",".orchestration/sandboxes/remote-diff-01.md",".orchestration/tasks/dot-agmsg-upstream-sync-T19-a01.md",".orchestration/tasks/dot-asset-manifest-T15-a01.md",".orchestration/tasks/dot-audit-exec-channel-T33e-a01.md",".orchestration/tasks/dot-audit-pane-hardening-T32b-a01.md",".orchestration/tasks/dot-audit-pane-visibility-T32-a01.md",".orchestration/tasks/dot-audit-verdict-gate-T33b-a01.md",".orchestration/tasks/dot-claude-sandbox-T13-a01.md",".orchestration/tasks/dot-codex-apparmor-userns-T30-a01.md",".orchestration/tasks/dot-env-converge-T10-a01.md",".orchestration/tasks/dot-herdr-agents-add-worker-T22-a01.md",".orchestration/tasks/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/tasks/dot-herdr-worker-worktree-T11-a01.md",".orchestration/tasks/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/tasks/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/tasks/dot-orchestration-rules-T33a-a01.md",".orchestration/tasks/dot-orchestrator-guardrails-T21-a01.md",".orchestration/tasks/dot-permgate-bench-flake-T33d-a01.md",".orchestration/tasks/dot-pr-feedback-gate-T16-a01.md",".orchestration/tasks/dot-restart-worker-name-wait-T27-a01.md",".orchestration/tasks/dot-runner-label-pin-T18-a01.md",".orchestration/tasks/dot-task-contract-v2-T23-a01.md",".orchestration/tasks/dot-three-role-constellation-T28-a01.md",".orchestration/tasks/dot-ua-full-T9-a01.md",".orchestration/tasks/dot-ua-graph-refresh-T33c-a01.md",".orchestration/tasks/dot-ua-hook-regex-T12-a01.md",".orchestration/tasks/dot-ua-incremental-T20-a01.md",".orchestration/tasks/dot-version-currency-T29-a01.md",".orchestration/tasks/dot-worker-advisor-fable-T26-a01.md",".orchestration/tasks/dot-worker-kind-guard-T14-a01.md",".orchestration/tasks/dot-worker-profile-opus55-T24-a01.md",".orchestration/tasks/refkit-P0-01.md",".orchestration/tasks/refkit-P0-05.md",".orchestration/tasks/refkit-P0-06.md",".orchestration/tasks/refkit-P0-07.md",".orchestration/tasks/refkit-P1.md",".orchestration/tasks/refkit-P10.md",".orchestration/tasks/refkit-P2-A.md",".orchestration/tasks/refkit-P2-B.md",".orchestration/tasks/refkit-P2-C.md",".orchestration/tasks/refkit-P3.md",".orchestration/tasks/refkit-P4.md",".orchestration/tasks/refkit-P4b.md",".orchestration/tasks/refkit-P5.md",".orchestration/tasks/refkit-P6.md",".orchestration/tasks/refkit-P7.md",".orchestration/tasks/refkit-P8-a.md",".orchestration/tasks/refkit-P8-b.md",".orchestration/tasks/refkit-P8.md",".orchestration/tasks/refkit-P9.md",".orchestration/validation/baseline-20260925.md",".orchestration/validation/dot-asset-manifest-T15-a01.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-audit.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-crit.json",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-live-e2e.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-receipt.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-crit.json",".orchestration/validation/dot-audit-pane-visibility-T32-a01-live-e2e.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-receipt.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev2.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev3.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-crit.json",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-live-e2e.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-receipt.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01.md",".orchestration/validation/dot-claude-sandbox-T13-a01.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-audit.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-crit.json",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-receipt.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01.md",".orchestration/validation/dot-env-converge-T10-a01.md",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01-crit.json",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01-receipt.md",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/validation/dot-macos-crit-pinned-install-T17-a01-crit.json",".orchestration/validation/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-audit.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-crit.json",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-receipt.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-audit-rev3.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-audit.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-crit.json",".orchestration/validation/dot-orchestration-rules-T33a-a01-receipt.md",".orchestration/validation/dot-orchestration-rules-T33a-a01.md",".orchestration/validation/dot-restart-worker-name-wait-T27-a01-crit.json",".orchestration/validation/dot-restart-worker-name-wait-T27-a01-receipt.md",".orchestration/validation/dot-restart-worker-name-wait-T27-a01.md",".orchestration/validation/dot-three-role-constellation-T28-a01-audit.md",".orchestration/validation/dot-three-role-constellation-T28-a01-crit.json",".orchestration/validation/dot-three-role-constellation-T28-a01-receipt.md",".orchestration/validation/dot-three-role-constellation-T28-a01.md",".orchestration/validation/dot-ua-full-T9-a01.md",".orchestration/validation/dot-version-currency-T29-a01-audit.md",".orchestration/validation/dot-version-currency-T29-a01-crit.json",".orchestration/validation/dot-version-currency-T29-a01-receipt.md",".orchestration/validation/dot-version-currency-T29-a01.md",".orchestration/validation/dot-worker-advisor-fable-T26-a01-crit.json",".orchestration/validation/dot-worker-advisor-fable-T26-a01-receipt.md",".orchestration/validation/dot-worker-advisor-fable-T26-a01.md",".orchestration/validation/dot-worker-kind-guard-T14-a01.md",".orchestration/validation/dot-worker-profile-opus55-T24-a01-crit.json",".orchestration/validation/dot-worker-profile-opus55-T24-a01-receipt.md",".orchestration/validation/dot-worker-profile-opus55-T24-a01.md",".orchestration/validation/remote-diff-01.md","home/dot_mise/mise.lock"],"generatedArtifactFiles":[".ua/.understandignore",".ua/fingerprints.json",".ua/knowledge-graph.json",".ua/meta.json"],"importMapRefreshPaths":[".chezmoiroot",".claude/contextdb/config.json",".claude/contextdb/contextdb/__init__.py",".claude/contextdb/contextdb/cli.py",".claude/contextdb/contextdb/config.py",".claude/contextdb/contextdb/hook.py",".claude/contextdb/contextdb/memory.py",".claude/contextdb/contextdb/normalize.py",".claude/contextdb/contextdb/paths.py",".claude/contextdb/contextdb/probe.py",".claude/contextdb/contextdb/recall.py",".claude/contextdb/contextdb/recover_hook.py",".claude/contextdb/contextdb/recovery.py",".claude/contextdb/contextdb/redaction.py",".claude/contextdb/contextdb/semantic.py",".claude/contextdb/contextdb/spool.py",".claude/contextdb/contextdb/storage.py",".claude/contextdb/contextdb/util.py",".claude/contextdb/health/.gitkeep",".claude/contextdb/spool/incoming/.gitkeep",".claude/contextdb/spool/quarantine/.gitkeep",".claude/contextdb/state/.gitkeep",".claude/hooks/contextdb_cli.py",".claude/hooks/contextdb_hook.py",".claude/hooks/contextdb_recover.py",".claude/hooks/query_log.py",".claude/settings.json",".github/copilot-instructions.md",".github/funding.yaml",".github/workflows/agent-assets.yml",".github/workflows/docs.yml",".github/workflows/macos.yaml",".github/workflows/remote.yaml",".github/workflows/test.yaml",".github/workflows/ubuntu.yaml",".simplecov","AGENTS.md","CLAUDE.md","Dockerfile","Makefile","README.md","codecov.yml","docs/assets/stylesheets/extra.css","docs/plans/nix-first-architecture.md","docs/plans/nix-migration.md","docs/verification/acceptance/005.md","flake.nix","home/.chezmoi.yaml.tmpl","home/.chezmoiexternal.yaml.tmpl","home/.chezmoiignore","home/.chezmoiremove","home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl","home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl","home/.chezmoiscripts/common/run_once_after_03-install-sheldon.sh.tmpl","home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl","home/.chezmoiscripts/common/run_once_after_99-install-gh-extensions.sh.tmpl","home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl","home/.chezmoiscripts/macos/run_once_04-install-ghostty.sh.tmpl","home/.chezmoiscripts/macos/run_once_10-install-docker.sh.tmpl","home/.chezmoiscripts/macos/run_once_99-install-defaults.sh.tmpl","home/.chezmoiscripts/macos/run_once_after_50-install-misc.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_01-prepare-system.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_02-install-command-line-tool.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_03-install-brew.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_50-install-dependencies.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_00-setup-ssh.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_10-install-docker.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_10-install-starship.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-docker-ssh.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-install-mics.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_51-client-default-shell.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_after_04-install-aws-cli.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_before_50-common-dependencies.sh.tmpl","home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl","home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl","home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl","home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl","home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl","home/.chezmoitemplates/chezmoiignore.d/common","home/.chezmoitemplates/chezmoiignore.d/macos","home/.chezmoitemplates/chezmoiignore.d/ubuntu/client","home/.chezmoitemplates/chezmoiignore.d/ubuntu/common","home/.chezmoitemplates/chezmoiignore.d/ubuntu/server","home/.chezmoitemplates/claude-settings-managed.json","home/.chezmoitemplates/codex-config-managed.toml","home/.key.txt.age","home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl","home/dot_agents/README.md","home/dot_agents/agent-config.yaml","home/dot_agents/model-profiles.env","home/dot_agents/permgate-policy.yaml","home/dot_agents/plugins/create_marketplace.json","home/dot_agents/plugins/mryfmo-dev-workflows/.codex-plugin/plugin.json","home/dot_agents/skills/agmsg-orchestration/SKILL.md","home/dot_agents/skills/agmsg/SKILL.md","home/dot_agents/skills/agmsg/agents/openai.yaml","home/dot_agents/skills/agmsg/db/.keep","home/dot_agents/skills/agmsg/run/.keep","home/dot_agents/skills/agmsg/scripts/executable_actas-claim.sh","home/dot_agents/skills/agmsg/scripts/executable_check-inbox.sh","home/dot_agents/skills/agmsg/scripts/executable_config.sh","home/dot_agents/skills/agmsg/scripts/executable_delivery.sh","home/dot_agents/skills/agmsg/scripts/executable_history.sh","home/dot_agents/skills/agmsg/scripts/executable_hook.sh","home/dot_agents/skills/agmsg/scripts/executable_identities.sh","home/dot_agents/skills/agmsg/scripts/executable_inbox.sh","home/dot_agents/skills/agmsg/scripts/executable_init-db.sh","home/dot_agents/skills/agmsg/scripts/executable_join.sh","home/dot_agents/skills/agmsg/scripts/executable_leave.sh","home/dot_agents/skills/agmsg/scripts/executable_rename-team.sh","home/dot_agents/skills/agmsg/scripts/executable_rename.sh","home/dot_agents/skills/agmsg/scripts/executable_reset.sh","home/dot_agents/skills/agmsg/scripts/executable_send.sh","home/dot_agents/skills/agmsg/scripts/executable_session-end.sh","home/dot_agents/skills/agmsg/scripts/executable_session-start.sh","home/dot_agents/skills/agmsg/scripts/executable_team.sh","home/dot_agents/skills/agmsg/scripts/executable_watch.sh","home/dot_agents/skills/agmsg/scripts/executable_whoami.sh","home/dot_agents/skills/agmsg/scripts/lib/actas-lock.sh","home/dot_agents/skills/agmsg/scripts/lib/identifier.sh","home/dot_agents/skills/agmsg/scripts/lib/storage.sh","home/dot_agents/skills/agmsg/scripts/release/executable_sync-version.sh","home/dot_agents/skills/agmsg/teams/.keep","home/dot_agents/skills/agmsg/templates/cmd.antigravity.md","home/dot_agents/skills/agmsg/templates/cmd.claude-code.md","home/dot_agents/skills/agmsg/templates/cmd.codex.md","home/dot_agents/skills/agmsg/templates/cmd.copilot.md","home/dot_agents/skills/agmsg/templates/cmd.gemini.md","home/dot_agents/skills/convert-to-transformers/SKILL.md","home/dot_agents/skills/convert-to-transformers/references/common-pitfalls.md","home/dot_agents/skills/convert-to-transformers/references/learnings.md","home/dot_agents/skills/gh-comment-attach-files/SKILL.md","home/dot_agents/skills/gh-comment-attach-files/agents/openai.yaml","home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py","home/dot_agents/skills/gh-first-workflow/SKILL.md","home/dot_agents/skills/gh-first-workflow/agents/openai.yaml","home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md","home/dot_agents/skills/humanizer-ja/SKILL.md","home/dot_agents/skills/humanizer-ja/agents/openai.yaml","home/dot_agents/skills/humanizer-ja/references/ai-patterns-ja.md","home/dot_agents/skills/python-uv-workflow/SKILL.md","home/dot_agents/skills/python-uv-workflow/agents/openai.yaml","home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md","home/dot_agents/skills/shdoc-shell-docs/SKILL.md","home/dot_agents/skills/shdoc-shell-docs/agents/openai.yaml","home/dot_agents/skills/shdoc-shell-docs/references/shdoc-rules.md","home/dot_bash/client/bashrc","home/dot_bash/server/bashrc","home/dot_ccstatusline/settings.json","home/dot_claude/agents/express-explorer.md","home/dot_claude/commands/commit.md","home/dot_claude/commands/symlink_agmsg.md.tmpl","home/dot_claude/hooks/executable_enforce-uv.sh","home/dot_claude/hooks/executable_format-edited-files.py","home/dot_claude/modify_private_settings.json","home/dot_claude/private_mcp.json.tmpl","home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl","home/dot_claude/rules/symlink_ask-user-question.md.tmpl","home/dot_claude/rules/symlink_compactiondb.md.tmpl","home/dot_claude/rules/symlink_crit-review.md.tmpl","home/dot_claude/rules/symlink_gpu.md.tmpl","home/dot_claude/rules/symlink_latex.md.tmpl","home/dot_claude/rules/symlink_model-selection.md.tmpl","home/dot_claude/rules/symlink_ponytail.md.tmpl","home/dot_claude/rules/symlink_python.md.tmpl","home/dot_claude/rules/symlink_understand-anything.md.tmpl","home/dot_claude/skills/agmsg-orchestration/symlink_SKILL.md.tmpl","home/dot_claude/skills/agmsg/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_actas-lock.sh.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_identifier.sh.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_storage.sh.tmpl","home/dot_claude/skills/agmsg/scripts/release/symlink_sync-version.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_actas-claim.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_check-inbox.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_config.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_delivery.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_history.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_hook.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_identities.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_inbox.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_init-db.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_join.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_leave.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_rename-team.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_rename.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_reset.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_send.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_session-end.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_session-start.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_team.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_watch.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_whoami.sh.tmpl","home/dot_claude/skills/agmsg/symlink_SKILL.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.antigravity.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.claude-code.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.codex.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.copilot.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.gemini.md.tmpl","home/dot_claude/skills/convert-to-transformers/references/symlink_common-pitfalls.md.tmpl","home/dot_claude/skills/convert-to-transformers/references/symlink_learnings.md.tmpl","home/dot_claude/skills/convert-to-transformers/symlink_SKILL.md.tmpl","home/dot_claude/skills/gh-comment-attach-files/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/gh-comment-attach-files/scripts/symlink_attach_comment_files.py.tmpl","home/dot_claude/skills/gh-comment-attach-files/symlink_SKILL.md.tmpl","home/dot_claude/skills/gh-first-workflow/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/gh-first-workflow/references/symlink_gh-git-rules.md.tmpl","home/dot_claude/skills/gh-first-workflow/symlink_SKILL.md.tmpl","home/dot_claude/skills/humanizer-ja/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/humanizer-ja/references/symlink_ai-patterns-ja.md.tmpl","home/dot_claude/skills/humanizer-ja/symlink_SKILL.md.tmpl","home/dot_claude/skills/python-uv-workflow/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/python-uv-workflow/references/symlink_python-uv-rules.md.tmpl","home/dot_claude/skills/python-uv-workflow/symlink_SKILL.md.tmpl","home/dot_claude/skills/shdoc-shell-docs/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/shdoc-shell-docs/references/symlink_shdoc-rules.md.tmpl","home/dot_claude/skills/shdoc-shell-docs/symlink_SKILL.md.tmpl","home/dot_codex/modify_private_adh.config.toml","home/dot_codex/modify_private_audit.config.toml","home/dot_codex/modify_private_config.toml","home/dot_codex/modify_private_deep.config.toml","home/dot_codex/modify_private_express.config.toml","home/dot_codex/modify_private_review.config.toml","home/dot_codex/modify_private_security.config.toml","home/dot_codex/modify_private_standard.config.toml","home/dot_codex/symlink_AGENTS.md.tmpl","home/dot_config/alias/client.sh","home/dot_config/alias/common.sh","home/dot_config/alias/server.sh","home/dot_config/ccstatusline/symlink_settings.json.tmpl","home/dot_config/claude/rules/agmsg-orchestration.md","home/dot_config/claude/rules/ask-user-question.md","home/dot_config/claude/rules/compactiondb.md","home/dot_config/claude/rules/crit-review.md","home/dot_config/claude/rules/gpu.md","home/dot_config/claude/rules/latex.md","home/dot_config/claude/rules/model-selection.md","home/dot_config/claude/rules/ponytail.md","home/dot_config/claude/rules/python.md","home/dot_config/claude/rules/understand-anything.md","home/dot_config/codex/AGENTS.md","home/dot_config/ghostty/config","home/dot_config/git/config.tmpl","home/dot_config/git/ignore","home/dot_config/gwq/config.toml","home/dot_config/herdr/config.toml","home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml","home/dot_config/mise/config.toml.tmpl","home/dot_config/mise/mise.lock.tmpl","home/dot_config/powerlevel10k/p10k.zsh","home/dot_config/sheldon/plugin_sources/client/common.toml","home/dot_config/sheldon/plugin_sources/client/macos.toml","home/dot_config/sheldon/plugin_sources/client/ubuntu.toml","home/dot_config/sheldon/plugin_sources/common.toml","home/dot_config/sheldon/plugin_sources/server.toml","home/dot_config/sheldon/plugins.toml.tmpl","home/dot_config/starship.toml","home/dot_config/systemd/user/usage-snapshot.service.tmpl","home/dot_config/systemd/user/usage-snapshot.timer.tmpl","home/dot_config/tango.yml","home/dot_config/uv/uv.toml","home/dot_config/yazi/yazi.toml","home/dot_config/zed/keymap.json","home/dot_config/zed/settings.json","home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh","home/dot_local/bin/common/executable_agent-fanout","home/dot_local/bin/common/executable_agent-session-staleness","home/dot_local/bin/common/executable_agmsg-dispatch","home/dot_local/bin/common/executable_cdgwq","home/dot_local/bin/common/executable_cdw","home/dot_local/bin/common/executable_chezmoi-cd","home/dot_local/bin/common/executable_compactiondb-install","home/dot_local/bin/common/executable_contextdb-codex-notify","home/dot_local/bin/common/executable_dev","home/dot_local/bin/common/executable_fgc","home/dot_local/bin/common/executable_git-delete-merged-branches","home/dot_local/bin/common/executable_herdr-agents","home/dot_local/bin/common/executable_herdr-session","home/dot_local/bin/common/executable_permgate","home/dot_local/bin/common/executable_provision-machine-key","home/dot_local/bin/common/executable_remove-agent-asset","home/dot_local/bin/common/executable_setup-gh","home/dot_local/bin/common/executable_setup-gpg","home/dot_local/bin/common/executable_setup-python-env","home/dot_local/bin/common/executable_uv-format","home/dot_local/bin/server/cache.sh","home/dot_local/bin/server/cuda.sh","home/dot_local/bin/server/history.sh","home/dot_local/bin/server/ssh_agent.sh","home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc","home/dot_mise/config.toml","home/dot_npmrc","home/dot_profile","home/dot_vimrc","home/dot_zprofile","home/dot_zshenv","home/dot_zshrc","home/private_dot_gnupg/gpg-agent.conf.tmpl","home/private_dot_ssh/private_config","home/symlink_dot_bashrc.tmpl","install/common/chezmoi_private.sh","install/common/gh_extensions.sh","install/common/mise.sh","install/common/sheldon.sh","install/macos/arm64/prepare_arm64_system.sh","install/macos/arm64/run.sh","install/macos/common/brew.sh","install/macos/common/command_line_tool.sh","install/macos/common/defaults.sh","install/macos/common/dependencies.sh","install/macos/common/docker.sh","install/macos/common/ghostty.sh","install/macos/common/misc.sh","install/ubuntu/client/default_shell.sh","install/ubuntu/client/docker.sh","install/ubuntu/client/ghostty.sh","install/ubuntu/client/gnome_settings.sh","install/ubuntu/client/misc.sh","install/ubuntu/client/tailscale.sh","install/ubuntu/client/zed.sh","install/ubuntu/common/apparmor/bwrap-userns","install/ubuntu/common/apparmor_userns.sh","install/ubuntu/common/aws_cli.sh","install/ubuntu/common/dependencies.sh","install/ubuntu/common/setup_locale.sh","install/ubuntu/common/ssh.sh","install/ubuntu/server/misc.sh","install/ubuntu/server/setup_timezone.sh","install/ubuntu/server/ssh_server.sh","install/ubuntu/server/starship.sh","mise.toml","mkdocs.yml","nix/home-manager/default.nix","nix/nix-darwin/default.nix","nix/shared/packages.nix","plans/001-contain-starship-cleanup.md","plans/002-make-review-evidence-non-vacuous.md","plans/003-make-bootstrap-safe-and-publicly-testable.md","plans/004-harden-and-lock-the-supply-chain.md","plans/005-make-runtime-health-and-verification-truthful.md","plans/README.md","renovate.json","scripts/check-agent-runtime.py","scripts/check-statusline-tools.py","scripts/check-tools.sh","scripts/generate-agent-configs.py","scripts/generate-docs.sh","scripts/lib/asset-manifest.sh","scripts/lib/installer-pins.sh","scripts/refresh-mkdocs-toc.py","scripts/require-crit-review.py","scripts/run_bashcov_unit_test.rb","scripts/run_benchmark.sh","scripts/run_unit_test.sh","scripts/update-agent-assets.sh","scripts/upgrade-tools.sh","scripts/usage-report.py","scripts/usage-snapshot.sh","scripts/validate-agent-assets.py","setup.sh","tests/files/common.bats","tests/files/helpers.bash","tests/files/macos.bats","tests/files/ubuntu.bats","tests/install/common/check_tools.bats","tests/install/common/chezmoi_private.bats","tests/install/common/decrypt_private_key.bats","tests/install/common/gh_extensions.bats","tests/install/common/lifecycle.bats","tests/install/common/mise.bats","tests/install/common/private_layer.bats","tests/install/common/provision_machine_key.bats","tests/install/common/setup.bats","tests/install/macos/common/brew.bats","tests/install/macos/common/defaults.bats","tests/install/macos/common/docker.bats","tests/install/macos/common/ghostty.bats","tests/install/macos/common/misc.bats","tests/install/ubuntu/client/default_shell.bats","tests/install/ubuntu/client/docker.bats","tests/install/ubuntu/client/ghostty.bats","tests/install/ubuntu/client/gnome_settings.bats","tests/install/ubuntu/client/misc.bats","tests/install/ubuntu/client/tailscale.bats","tests/install/ubuntu/client/zed.bats","tests/install/ubuntu/common/dependencies.bats","tests/install/ubuntu/common/dependencies_unit.bats","tests/install/ubuntu/common/setup_locale.bats","tests/install/ubuntu/common/ssh.bats","tests/install/ubuntu/server/setup_timezone.bats","tests/install/ubuntu/server/sheldon.bats","tests/install/ubuntu/server/starship.bats","tests/unit/test_agent_session_staleness.py","tests/unit/test_agmsg_dispatch.py","tests/unit/test_agmsg_send.py","tests/unit/test_apparmor_userns.py","tests/unit/test_asset_manifest.py","tests/unit/test_aws_cli_acquisition.py","tests/unit/test_check_agent_runtime.py","tests/unit/test_claude_settings_merge.py","tests/unit/test_codex_config_merge.py","tests/unit/test_contextdb_codex_notify.py","tests/unit/test_files_fixture.py","tests/unit/test_generate_agent_configs.py","tests/unit/test_herdr_agents.py","tests/unit/test_permgate.py","tests/unit/test_release_asset_pins.py","tests/unit/test_remove_agent_asset.py","tests/unit/test_require_crit_review.py","tests/unit/test_runtime_health.py","tests/unit/test_statusline_tools.py","tests/unit/test_supply_chain_policy.py","tests/unit/test_usage_review.py","tests/unit/test_validate_agent_assets.py","tests/unit/test_workflow_security.py"],"rerunArchitecture":true,"rerunTour":true,"reason":"44 files have structural changes (>30 files) — full rebuild recommended"}
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:3142:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:3143:| docs/plans/nix-migration.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:4420:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:4421:| docs/plans/nix-migration.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:5647:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:5648:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:7063:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:7064:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:7549:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-56f308c.md:7550:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md:7747:+| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md:7748:+| docs/plans/nix-migration.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md:9025:+| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md:9026:+| docs/plans/nix-migration.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md:10252:+| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01-audit-85919df.md:10253:+| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:1785:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:1786:| docs/plans/nix-migration.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:3063:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:3064:| docs/plans/nix-migration.md | 0 | 0 | - | ok |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:4290:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:4291:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:5706:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:5707:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:6192:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:6193:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:7465:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:7466:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:8676:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestration-rules-T43-a01.md:8677:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:5813:      "id": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:5816:      "filePath": "docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:5828:      "id": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:5831:      "filePath": "docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:19039:      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:19046:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:19053:      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:19054:      "target": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:24256:        "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-orchestrator-linkage-evidence-T46-a01-audit-b29ef04.md:24257:        "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T33c-a01-audit.md:796:{"baseCommit":"d906b00bff8729625b895d6f7765e3186ab5bb86","headCommit":"935e198406e5df993c84de67c695c7083f4b6b54","action":"FULL_UPDATE","deletedFiles":[".github/dependabot.yml"],"cosmeticFiles":["scripts/check-statusline-tools.py","tests/unit/test_statusline_tools.py"],"ignoredFiles":[".orchestration/acceptance/dot-agmsg-upstream-sync-T19-a01.md",".orchestration/acceptance/dot-asset-manifest-T15-a01.md",".orchestration/acceptance/dot-audit-pane-hardening-T32b-a01.md",".orchestration/acceptance/dot-audit-pane-visibility-T32-a01.md",".orchestration/acceptance/dot-audit-verdict-gate-T33b-a01.md",".orchestration/acceptance/dot-claude-sandbox-T13-a01.md",".orchestration/acceptance/dot-codex-apparmor-userns-T30-a01.md",".orchestration/acceptance/dot-env-converge-T10-a01.md",".orchestration/acceptance/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/acceptance/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/acceptance/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/acceptance/dot-orchestration-rules-T33a-a01.md",".orchestration/acceptance/dot-pr-feedback-gate-T16-a01.md",".orchestration/acceptance/dot-restart-worker-name-wait-T27-a01.md",".orchestration/acceptance/dot-three-role-constellation-T28-a01.md",".orchestration/acceptance/dot-ua-full-T9-a01.md",".orchestration/acceptance/dot-version-currency-T29-a01.md",".orchestration/acceptance/dot-worker-advisor-fable-T26-a01.md",".orchestration/acceptance/dot-worker-kind-guard-T14-a01.md",".orchestration/acceptance/dot-worker-profile-opus55-T24-a01.md",".orchestration/acceptance/refkit-P0-01.md",".orchestration/acceptance/refkit-P0-05.md",".orchestration/acceptance/refkit-P0-06.md",".orchestration/acceptance/refkit-P0-07.md",".orchestration/acceptance/refkit-P1.md",".orchestration/acceptance/refkit-P2-A.md",".orchestration/acceptance/refkit-P2-B.md",".orchestration/acceptance/refkit-P2-C.md",".orchestration/acceptance/refkit-P3.md",".orchestration/acceptance/refkit-P4.md",".orchestration/acceptance/refkit-P5.md",".orchestration/acceptance/refkit-P7.md",".orchestration/acceptance/refkit-P8-a.md",".orchestration/acceptance/refkit-P8-b.md",".orchestration/acceptance/remote-diff-01.md",".orchestration/autoskill/runs/dot-asset-manifest-T15-a01.md",".orchestration/autoskill/runs/dot-audit-pane-hardening-T32b-a01.md",".orchestration/autoskill/runs/dot-audit-pane-visibility-T32-a01.md",".orchestration/autoskill/runs/dot-audit-verdict-gate-T33b-a01.md",".orchestration/autoskill/runs/dot-codex-apparmor-userns-T30-a01.md",".orchestration/autoskill/runs/dot-env-converge-T10-a01.md",".orchestration/autoskill/runs/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/autoskill/runs/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/autoskill/runs/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/autoskill/runs/dot-orchestration-rules-T33a-a01.md",".orchestration/autoskill/runs/dot-restart-worker-name-wait-T27-a01.md",".orchestration/autoskill/runs/dot-three-role-constellation-T28-a01.md",".orchestration/autoskill/runs/dot-ua-full-T9-a01.md",".orchestration/autoskill/runs/dot-version-currency-T29-a01.md",".orchestration/autoskill/runs/dot-worker-advisor-fable-T26-a01.md",".orchestration/autoskill/runs/dot-worker-kind-guard-T14-a01.md",".orchestration/autoskill/runs/dot-worker-profile-opus55-T24-a01.md",".orchestration/autoskill/runs/remote-diff-01.md",".orchestration/learning/dot-asset-manifest-T15-a01.md",".orchestration/learning/dot-audit-pane-hardening-T32b-a01.md",".orchestration/learning/dot-audit-pane-visibility-T32-a01.md",".orchestration/learning/dot-audit-verdict-gate-T33b-a01.md",".orchestration/learning/dot-codex-apparmor-userns-T30-a01.md",".orchestration/learning/dot-env-converge-T10-a01.md",".orchestration/learning/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/learning/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/learning/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/learning/dot-orchestration-rules-T33a-a01.md",".orchestration/learning/dot-restart-worker-name-wait-T27-a01.md",".orchestration/learning/dot-three-role-constellation-T28-a01.md",".orchestration/learning/dot-ua-full-T9-a01.md",".orchestration/learning/dot-version-currency-T29-a01.md",".orchestration/learning/dot-worker-advisor-fable-T26-a01.md",".orchestration/learning/dot-worker-kind-guard-T14-a01.md",".orchestration/learning/dot-worker-profile-opus55-T24-a01.md",".orchestration/learning/remote-diff-01.md",".orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md",".orchestration/learning/rule_candidates/herdr-worker-relaunch.md",".orchestration/reports/P0-04-sources.md",".orchestration/reports/dot-asset-manifest-T15-a01.md",".orchestration/reports/dot-audit-pane-hardening-T32b-a01.md",".orchestration/reports/dot-audit-pane-visibility-T32-a01.md",".orchestration/reports/dot-audit-verdict-gate-T33b-a01.md",".orchestration/reports/dot-claude-sandbox-T13-a01.md",".orchestration/reports/dot-codex-apparmor-userns-T30-a01.md",".orchestration/reports/dot-env-converge-T10-a01.md",".orchestration/reports/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/reports/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/reports/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/reports/dot-orchestration-rules-T33a-a01.md",".orchestration/reports/dot-restart-worker-name-wait-T27-a01.md",".orchestration/reports/dot-three-role-constellation-T28-a01.md",".orchestration/reports/dot-ua-full-T9-a01.md",".orchestration/reports/dot-version-currency-T29-a01.md",".orchestration/reports/dot-worker-advisor-fable-T26-a01.md",".orchestration/reports/dot-worker-kind-guard-T14-a01.md",".orchestration/reports/dot-worker-profile-opus55-T24-a01.md",".orchestration/reports/remote-diff-01.md",".orchestration/sandboxes/dot-asset-manifest-T15-a01.md",".orchestration/sandboxes/dot-audit-pane-hardening-T32b-a01.md",".orchestration/sandboxes/dot-audit-pane-visibility-T32-a01.md",".orchestration/sandboxes/dot-audit-verdict-gate-T33b-a01.md",".orchestration/sandboxes/dot-codex-apparmor-userns-T30-a01.md",".orchestration/sandboxes/dot-env-converge-T10-a01.md",".orchestration/sandboxes/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/sandboxes/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/sandboxes/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/sandboxes/dot-orchestration-rules-T33a-a01.md",".orchestration/sandboxes/dot-restart-worker-name-wait-T27-a01.md",".orchestration/sandboxes/dot-three-role-constellation-T28-a01.md",".orchestration/sandboxes/dot-ua-full-T9-a01.md",".orchestration/sandboxes/dot-version-currency-T29-a01.md",".orchestration/sandboxes/dot-worker-advisor-fable-T26-a01.md",".orchestration/sandboxes/dot-worker-kind-guard-T14-a01.md",".orchestration/sandboxes/dot-worker-profile-opus55-T24-a01.md",".orchestration/sandboxes/remote-diff-01.md",".orchestration/tasks/dot-agmsg-upstream-sync-T19-a01.md",".orchestration/tasks/dot-asset-manifest-T15-a01.md",".orchestration/tasks/dot-audit-exec-channel-T33e-a01.md",".orchestration/tasks/dot-audit-pane-hardening-T32b-a01.md",".orchestration/tasks/dot-audit-pane-visibility-T32-a01.md",".orchestration/tasks/dot-audit-verdict-gate-T33b-a01.md",".orchestration/tasks/dot-claude-sandbox-T13-a01.md",".orchestration/tasks/dot-codex-apparmor-userns-T30-a01.md",".orchestration/tasks/dot-env-converge-T10-a01.md",".orchestration/tasks/dot-herdr-agents-add-worker-T22-a01.md",".orchestration/tasks/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/tasks/dot-herdr-worker-worktree-T11-a01.md",".orchestration/tasks/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/tasks/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/tasks/dot-orchestration-rules-T33a-a01.md",".orchestration/tasks/dot-orchestrator-guardrails-T21-a01.md",".orchestration/tasks/dot-permgate-bench-flake-T33d-a01.md",".orchestration/tasks/dot-pr-feedback-gate-T16-a01.md",".orchestration/tasks/dot-restart-worker-name-wait-T27-a01.md",".orchestration/tasks/dot-runner-label-pin-T18-a01.md",".orchestration/tasks/dot-task-contract-v2-T23-a01.md",".orchestration/tasks/dot-three-role-constellation-T28-a01.md",".orchestration/tasks/dot-ua-full-T9-a01.md",".orchestration/tasks/dot-ua-graph-refresh-T33c-a01.md",".orchestration/tasks/dot-ua-hook-regex-T12-a01.md",".orchestration/tasks/dot-ua-incremental-T20-a01.md",".orchestration/tasks/dot-version-currency-T29-a01.md",".orchestration/tasks/dot-worker-advisor-fable-T26-a01.md",".orchestration/tasks/dot-worker-kind-guard-T14-a01.md",".orchestration/tasks/dot-worker-profile-opus55-T24-a01.md",".orchestration/tasks/refkit-P0-01.md",".orchestration/tasks/refkit-P0-05.md",".orchestration/tasks/refkit-P0-06.md",".orchestration/tasks/refkit-P0-07.md",".orchestration/tasks/refkit-P1.md",".orchestration/tasks/refkit-P10.md",".orchestration/tasks/refkit-P2-A.md",".orchestration/tasks/refkit-P2-B.md",".orchestration/tasks/refkit-P2-C.md",".orchestration/tasks/refkit-P3.md",".orchestration/tasks/refkit-P4.md",".orchestration/tasks/refkit-P4b.md",".orchestration/tasks/refkit-P5.md",".orchestration/tasks/refkit-P6.md",".orchestration/tasks/refkit-P7.md",".orchestration/tasks/refkit-P8-a.md",".orchestration/tasks/refkit-P8-b.md",".orchestration/tasks/refkit-P8.md",".orchestration/tasks/refkit-P9.md",".orchestration/validation/baseline-20260925.md",".orchestration/validation/dot-asset-manifest-T15-a01.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-audit.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-crit.json",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-live-e2e.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-receipt.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-crit.json",".orchestration/validation/dot-audit-pane-visibility-T32-a01-live-e2e.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-receipt.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev2.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev3.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-crit.json",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-live-e2e.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-receipt.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01.md",".orchestration/validation/dot-claude-sandbox-T13-a01.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-audit.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-crit.json",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-receipt.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01.md",".orchestration/validation/dot-env-converge-T10-a01.md",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01-crit.json",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01-receipt.md",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/validation/dot-macos-crit-pinned-install-T17-a01-crit.json",".orchestration/validation/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-audit.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-crit.json",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-receipt.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-audit-rev3.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-audit.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-crit.json",".orchestration/validation/dot-orchestration-rules-T33a-a01-receipt.md",".orchestration/validation/dot-orchestration-rules-T33a-a01.md",".orchestration/validation/dot-restart-worker-name-wait-T27-a01-crit.json",".orchestration/validation/dot-restart-worker-name-wait-T27-a01-receipt.md",".orchestration/validation/dot-restart-worker-name-wait-T27-a01.md",".orchestration/validation/dot-three-role-constellation-T28-a01-audit.md",".orchestration/validation/dot-three-role-constellation-T28-a01-crit.json",".orchestration/validation/dot-three-role-constellation-T28-a01-receipt.md",".orchestration/validation/dot-three-role-constellation-T28-a01.md",".orchestration/validation/dot-ua-full-T9-a01.md",".orchestration/validation/dot-version-currency-T29-a01-audit.md",".orchestration/validation/dot-version-currency-T29-a01-crit.json",".orchestration/validation/dot-version-currency-T29-a01-receipt.md",".orchestration/validation/dot-version-currency-T29-a01.md",".orchestration/validation/dot-worker-advisor-fable-T26-a01-crit.json",".orchestration/validation/dot-worker-advisor-fable-T26-a01-receipt.md",".orchestration/validation/dot-worker-advisor-fable-T26-a01.md",".orchestration/validation/dot-worker-kind-guard-T14-a01.md",".orchestration/validation/dot-worker-profile-opus55-T24-a01-crit.json",".orchestration/validation/dot-worker-profile-opus55-T24-a01-receipt.md",".orchestration/validation/dot-worker-profile-opus55-T24-a01.md",".orchestration/validation/remote-diff-01.md","home/dot_mise/mise.lock"],"generatedArtifactFiles":[".ua/.understandignore",".ua/fingerprints.json",".ua/knowledge-graph.json",".ua/meta.json"],"importMapRefreshPaths":[".chezmoiroot",".claude/contextdb/config.json",".claude/contextdb/contextdb/__init__.py",".claude/contextdb/contextdb/cli.py",".claude/contextdb/contextdb/config.py",".claude/contextdb/contextdb/hook.py",".claude/contextdb/contextdb/memory.py",".claude/contextdb/contextdb/normalize.py",".claude/contextdb/contextdb/paths.py",".claude/contextdb/contextdb/probe.py",".claude/contextdb/contextdb/recall.py",".claude/contextdb/contextdb/recover_hook.py",".claude/contextdb/contextdb/recovery.py",".claude/contextdb/contextdb/redaction.py",".claude/contextdb/contextdb/semantic.py",".claude/contextdb/contextdb/spool.py",".claude/contextdb/contextdb/storage.py",".claude/contextdb/contextdb/util.py",".claude/contextdb/health/.gitkeep",".claude/contextdb/spool/incoming/.gitkeep",".claude/contextdb/spool/quarantine/.gitkeep",".claude/contextdb/state/.gitkeep",".claude/hooks/contextdb_cli.py",".claude/hooks/contextdb_hook.py",".claude/hooks/contextdb_recover.py",".claude/hooks/query_log.py",".claude/settings.json",".github/copilot-instructions.md",".github/funding.yaml",".github/workflows/agent-assets.yml",".github/workflows/docs.yml",".github/workflows/macos.yaml",".github/workflows/remote.yaml",".github/workflows/test.yaml",".github/workflows/ubuntu.yaml",".simplecov","AGENTS.md","CLAUDE.md","Dockerfile","Makefile","README.md","codecov.yml","docs/assets/stylesheets/extra.css","docs/plans/nix-first-architecture.md","docs/plans/nix-migration.md","docs/verification/acceptance/005.md","flake.nix","home/.chezmoi.yaml.tmpl","home/.chezmoiexternal.yaml.tmpl","home/.chezmoiignore","home/.chezmoiremove","home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl","home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl","home/.chezmoiscripts/common/run_once_after_03-install-sheldon.sh.tmpl","home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl","home/.chezmoiscripts/common/run_once_after_99-install-gh-extensions.sh.tmpl","home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl","home/.chezmoiscripts/macos/run_once_04-install-ghostty.sh.tmpl","home/.chezmoiscripts/macos/run_once_10-install-docker.sh.tmpl","home/.chezmoiscripts/macos/run_once_99-install-defaults.sh.tmpl","home/.chezmoiscripts/macos/run_once_after_50-install-misc.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_01-prepare-system.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_02-install-command-line-tool.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_03-install-brew.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_50-install-dependencies.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_00-setup-ssh.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_10-install-docker.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_10-install-starship.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-docker-ssh.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-install-mics.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_51-client-default-shell.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_after_04-install-aws-cli.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_before_50-common-dependencies.sh.tmpl","home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl","home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl","home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl","home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl","home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl","home/.chezmoitemplates/chezmoiignore.d/common","home/.chezmoitemplates/chezmoiignore.d/macos","home/.chezmoitemplates/chezmoiignore.d/ubuntu/client","home/.chezmoitemplates/chezmoiignore.d/ubuntu/common","home/.chezmoitemplates/chezmoiignore.d/ubuntu/server","home/.chezmoitemplates/claude-settings-managed.json","home/.chezmoitemplates/codex-config-managed.toml","home/.key.txt.age","home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl","home/dot_agents/README.md","home/dot_agents/agent-config.yaml","home/dot_agents/model-profiles.env","home/dot_agents/permgate-policy.yaml","home/dot_agents/plugins/create_marketplace.json","home/dot_agents/plugins/mryfmo-dev-workflows/.codex-plugin/plugin.json","home/dot_agents/skills/agmsg-orchestration/SKILL.md","home/dot_agents/skills/agmsg/SKILL.md","home/dot_agents/skills/agmsg/agents/openai.yaml","home/dot_agents/skills/agmsg/db/.keep","home/dot_agents/skills/agmsg/run/.keep","home/dot_agents/skills/agmsg/scripts/executable_actas-claim.sh","home/dot_agents/skills/agmsg/scripts/executable_check-inbox.sh","home/dot_agents/skills/agmsg/scripts/executable_config.sh","home/dot_agents/skills/agmsg/scripts/executable_delivery.sh","home/dot_agents/skills/agmsg/scripts/executable_history.sh","home/dot_agents/skills/agmsg/scripts/executable_hook.sh","home/dot_agents/skills/agmsg/scripts/executable_identities.sh","home/dot_agents/skills/agmsg/scripts/executable_inbox.sh","home/dot_agents/skills/agmsg/scripts/executable_init-db.sh","home/dot_agents/skills/agmsg/scripts/executable_join.sh","home/dot_agents/skills/agmsg/scripts/executable_leave.sh","home/dot_agents/skills/agmsg/scripts/executable_rename-team.sh","home/dot_agents/skills/agmsg/scripts/executable_rename.sh","home/dot_agents/skills/agmsg/scripts/executable_reset.sh","home/dot_agents/skills/agmsg/scripts/executable_send.sh","home/dot_agents/skills/agmsg/scripts/executable_session-end.sh","home/dot_agents/skills/agmsg/scripts/executable_session-start.sh","home/dot_agents/skills/agmsg/scripts/executable_team.sh","home/dot_agents/skills/agmsg/scripts/executable_watch.sh","home/dot_agents/skills/agmsg/scripts/executable_whoami.sh","home/dot_agents/skills/agmsg/scripts/lib/actas-lock.sh","home/dot_agents/skills/agmsg/scripts/lib/identifier.sh","home/dot_agents/skills/agmsg/scripts/lib/storage.sh","home/dot_agents/skills/agmsg/scripts/release/executable_sync-version.sh","home/dot_agents/skills/agmsg/teams/.keep","home/dot_agents/skills/agmsg/templates/cmd.antigravity.md","home/dot_agents/skills/agmsg/templates/cmd.claude-code.md","home/dot_agents/skills/agmsg/templates/cmd.codex.md","home/dot_agents/skills/agmsg/templates/cmd.copilot.md","home/dot_agents/skills/agmsg/templates/cmd.gemini.md","home/dot_agents/skills/convert-to-transformers/SKILL.md","home/dot_agents/skills/convert-to-transformers/references/common-pitfalls.md","home/dot_agents/skills/convert-to-transformers/references/learnings.md","home/dot_agents/skills/gh-comment-attach-files/SKILL.md","home/dot_agents/skills/gh-comment-attach-files/agents/openai.yaml","home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py","home/dot_agents/skills/gh-first-workflow/SKILL.md","home/dot_agents/skills/gh-first-workflow/agents/openai.yaml","home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md","home/dot_agents/skills/humanizer-ja/SKILL.md","home/dot_agents/skills/humanizer-ja/agents/openai.yaml","home/dot_agents/skills/humanizer-ja/references/ai-patterns-ja.md","home/dot_agents/skills/python-uv-workflow/SKILL.md","home/dot_agents/skills/python-uv-workflow/agents/openai.yaml","home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md","home/dot_agents/skills/shdoc-shell-docs/SKILL.md","home/dot_agents/skills/shdoc-shell-docs/agents/openai.yaml","home/dot_agents/skills/shdoc-shell-docs/references/shdoc-rules.md","home/dot_bash/client/bashrc","home/dot_bash/server/bashrc","home/dot_ccstatusline/settings.json","home/dot_claude/agents/express-explorer.md","home/dot_claude/commands/commit.md","home/dot_claude/commands/symlink_agmsg.md.tmpl","home/dot_claude/hooks/executable_enforce-uv.sh","home/dot_claude/hooks/executable_format-edited-files.py","home/dot_claude/modify_private_settings.json","home/dot_claude/private_mcp.json.tmpl","home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl","home/dot_claude/rules/symlink_ask-user-question.md.tmpl","home/dot_claude/rules/symlink_compactiondb.md.tmpl","home/dot_claude/rules/symlink_crit-review.md.tmpl","home/dot_claude/rules/symlink_gpu.md.tmpl","home/dot_claude/rules/symlink_latex.md.tmpl","home/dot_claude/rules/symlink_model-selection.md.tmpl","home/dot_claude/rules/symlink_ponytail.md.tmpl","home/dot_claude/rules/symlink_python.md.tmpl","home/dot_claude/rules/symlink_understand-anything.md.tmpl","home/dot_claude/skills/agmsg-orchestration/symlink_SKILL.md.tmpl","home/dot_claude/skills/agmsg/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_actas-lock.sh.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_identifier.sh.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_storage.sh.tmpl","home/dot_claude/skills/agmsg/scripts/release/symlink_sync-version.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_actas-claim.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_check-inbox.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_config.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_delivery.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_history.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_hook.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_identities.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_inbox.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_init-db.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_join.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_leave.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_rename-team.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_rename.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_reset.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_send.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_session-end.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_session-start.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_team.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_watch.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_whoami.sh.tmpl","home/dot_claude/skills/agmsg/symlink_SKILL.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.antigravity.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.claude-code.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.codex.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.copilot.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.gemini.md.tmpl","home/dot_claude/skills/convert-to-transformers/references/symlink_common-pitfalls.md.tmpl","home/dot_claude/skills/convert-to-transformers/references/symlink_learnings.md.tmpl","home/dot_claude/skills/convert-to-transformers/symlink_SKILL.md.tmpl","home/dot_claude/skills/gh-comment-attach-files/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/gh-comment-attach-files/scripts/symlink_attach_comment_files.py.tmpl","home/dot_claude/skills/gh-comment-attach-files/symlink_SKILL.md.tmpl","home/dot_claude/skills/gh-first-workflow/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/gh-first-workflow/references/symlink_gh-git-rules.md.tmpl","home/dot_claude/skills/gh-first-workflow/symlink_SKILL.md.tmpl","home/dot_claude/skills/humanizer-ja/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/humanizer-ja/references/symlink_ai-patterns-ja.md.tmpl","home/dot_claude/skills/humanizer-ja/symlink_SKILL.md.tmpl","home/dot_claude/skills/python-uv-workflow/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/python-uv-workflow/references/symlink_python-uv-rules.md.tmpl","home/dot_claude/skills/python-uv-workflow/symlink_SKILL.md.tmpl","home/dot_claude/skills/shdoc-shell-docs/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/shdoc-shell-docs/references/symlink_shdoc-rules.md.tmpl","home/dot_claude/skills/shdoc-shell-docs/symlink_SKILL.md.tmpl","home/dot_codex/modify_private_adh.config.toml","home/dot_codex/modify_private_audit.config.toml","home/dot_codex/modify_private_config.toml","home/dot_codex/modify_private_deep.config.toml","home/dot_codex/modify_private_express.config.toml","home/dot_codex/modify_private_review.config.toml","home/dot_codex/modify_private_security.config.toml","home/dot_codex/modify_private_standard.config.toml","home/dot_codex/symlink_AGENTS.md.tmpl","home/dot_config/alias/client.sh","home/dot_config/alias/common.sh","home/dot_config/alias/server.sh","home/dot_config/ccstatusline/symlink_settings.json.tmpl","home/dot_config/claude/rules/agmsg-orchestration.md","home/dot_config/claude/rules/ask-user-question.md","home/dot_config/claude/rules/compactiondb.md","home/dot_config/claude/rules/crit-review.md","home/dot_config/claude/rules/gpu.md","home/dot_config/claude/rules/latex.md","home/dot_config/claude/rules/model-selection.md","home/dot_config/claude/rules/ponytail.md","home/dot_config/claude/rules/python.md","home/dot_config/claude/rules/understand-anything.md","home/dot_config/codex/AGENTS.md","home/dot_config/ghostty/config","home/dot_config/git/config.tmpl","home/dot_config/git/ignore","home/dot_config/gwq/config.toml","home/dot_config/herdr/config.toml","home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml","home/dot_config/mise/config.toml.tmpl","home/dot_config/mise/mise.lock.tmpl","home/dot_config/powerlevel10k/p10k.zsh","home/dot_config/sheldon/plugin_sources/client/common.toml","home/dot_config/sheldon/plugin_sources/client/macos.toml","home/dot_config/sheldon/plugin_sources/client/ubuntu.toml","home/dot_config/sheldon/plugin_sources/common.toml","home/dot_config/sheldon/plugin_sources/server.toml","home/dot_config/sheldon/plugins.toml.tmpl","home/dot_config/starship.toml","home/dot_config/systemd/user/usage-snapshot.service.tmpl","home/dot_config/systemd/user/usage-snapshot.timer.tmpl","home/dot_config/tango.yml","home/dot_config/uv/uv.toml","home/dot_config/yazi/yazi.toml","home/dot_config/zed/keymap.json","home/dot_config/zed/settings.json","home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh","home/dot_local/bin/common/executable_agent-fanout","home/dot_local/bin/common/executable_agent-session-staleness","home/dot_local/bin/common/executable_agmsg-dispatch","home/dot_local/bin/common/executable_cdgwq","home/dot_local/bin/common/executable_cdw","home/dot_local/bin/common/executable_chezmoi-cd","home/dot_local/bin/common/executable_compactiondb-install","home/dot_local/bin/common/executable_contextdb-codex-notify","home/dot_local/bin/common/executable_dev","home/dot_local/bin/common/executable_fgc","home/dot_local/bin/common/executable_git-delete-merged-branches","home/dot_local/bin/common/executable_herdr-agents","home/dot_local/bin/common/executable_herdr-session","home/dot_local/bin/common/executable_permgate","home/dot_local/bin/common/executable_provision-machine-key","home/dot_local/bin/common/executable_remove-agent-asset","home/dot_local/bin/common/executable_setup-gh","home/dot_local/bin/common/executable_setup-gpg","home/dot_local/bin/common/executable_setup-python-env","home/dot_local/bin/common/executable_uv-format","home/dot_local/bin/server/cache.sh","home/dot_local/bin/server/cuda.sh","home/dot_local/bin/server/history.sh","home/dot_local/bin/server/ssh_agent.sh","home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc","home/dot_mise/config.toml","home/dot_npmrc","home/dot_profile","home/dot_vimrc","home/dot_zprofile","home/dot_zshenv","home/dot_zshrc","home/private_dot_gnupg/gpg-agent.conf.tmpl","home/private_dot_ssh/private_config","home/symlink_dot_bashrc.tmpl","install/common/chezmoi_private.sh","install/common/gh_extensions.sh","install/common/mise.sh","install/common/sheldon.sh","install/macos/arm64/prepare_arm64_system.sh","install/macos/arm64/run.sh","install/macos/common/brew.sh","install/macos/common/command_line_tool.sh","install/macos/common/defaults.sh","install/macos/common/dependencies.sh","install/macos/common/docker.sh","install/macos/common/ghostty.sh","install/macos/common/misc.sh","install/ubuntu/client/default_shell.sh","install/ubuntu/client/docker.sh","install/ubuntu/client/ghostty.sh","install/ubuntu/client/gnome_settings.sh","install/ubuntu/client/misc.sh","install/ubuntu/client/tailscale.sh","install/ubuntu/client/zed.sh","install/ubuntu/common/apparmor/bwrap-userns","install/ubuntu/common/apparmor_userns.sh","install/ubuntu/common/aws_cli.sh","install/ubuntu/common/dependencies.sh","install/ubuntu/common/setup_locale.sh","install/ubuntu/common/ssh.sh","install/ubuntu/server/misc.sh","install/ubuntu/server/setup_timezone.sh","install/ubuntu/server/ssh_server.sh","install/ubuntu/server/starship.sh","mise.toml","mkdocs.yml","nix/home-manager/default.nix","nix/nix-darwin/default.nix","nix/shared/packages.nix","plans/001-contain-starship-cleanup.md","plans/002-make-review-evidence-non-vacuous.md","plans/003-make-bootstrap-safe-and-publicly-testable.md","plans/004-harden-and-lock-the-supply-chain.md","plans/005-make-runtime-health-and-verification-truthful.md","plans/README.md","renovate.json","scripts/check-agent-runtime.py","scripts/check-statusline-tools.py","scripts/check-tools.sh","scripts/generate-agent-configs.py","scripts/generate-docs.sh","scripts/lib/asset-manifest.sh","scripts/lib/installer-pins.sh","scripts/refresh-mkdocs-toc.py","scripts/require-crit-review.py","scripts/run_bashcov_unit_test.rb","scripts/run_benchmark.sh","scripts/run_unit_test.sh","scripts/update-agent-assets.sh","scripts/upgrade-tools.sh","scripts/usage-report.py","scripts/usage-snapshot.sh","scripts/validate-agent-assets.py","setup.sh","tests/files/common.bats","tests/files/helpers.bash","tests/files/macos.bats","tests/files/ubuntu.bats","tests/install/common/check_tools.bats","tests/install/common/chezmoi_private.bats","tests/install/common/decrypt_private_key.bats","tests/install/common/gh_extensions.bats","tests/install/common/lifecycle.bats","tests/install/common/mise.bats","tests/install/common/private_layer.bats","tests/install/common/provision_machine_key.bats","tests/install/common/setup.bats","tests/install/macos/common/brew.bats","tests/install/macos/common/defaults.bats","tests/install/macos/common/docker.bats","tests/install/macos/common/ghostty.bats","tests/install/macos/common/misc.bats","tests/install/ubuntu/client/default_shell.bats","tests/install/ubuntu/client/docker.bats","tests/install/ubuntu/client/ghostty.bats","tests/install/ubuntu/client/gnome_settings.bats","tests/install/ubuntu/client/misc.bats","tests/install/ubuntu/client/tailscale.bats","tests/install/ubuntu/client/zed.bats","tests/install/ubuntu/common/dependencies.bats","tests/install/ubuntu/common/dependencies_unit.bats","tests/install/ubuntu/common/setup_locale.bats","tests/install/ubuntu/common/ssh.bats","tests/install/ubuntu/server/setup_timezone.bats","tests/install/ubuntu/server/sheldon.bats","tests/install/ubuntu/server/starship.bats","tests/unit/test_agent_session_staleness.py","tests/unit/test_agmsg_dispatch.py","tests/unit/test_agmsg_send.py","tests/unit/test_apparmor_userns.py","tests/unit/test_asset_manifest.py","tests/unit/test_aws_cli_acquisition.py","tests/unit/test_check_agent_runtime.py","tests/unit/test_claude_settings_merge.py","tests/unit/test_codex_config_merge.py","tests/unit/test_contextdb_codex_notify.py","tests/unit/test_files_fixture.py","tests/unit/test_generate_agent_configs.py","tests/unit/test_herdr_agents.py","tests/unit/test_permgate.py","tests/unit/test_release_asset_pins.py","tests/unit/test_remove_agent_asset.py","tests/unit/test_require_crit_review.py","tests/unit/test_runtime_health.py","tests/unit/test_statusline_tools.py","tests/unit/test_supply_chain_policy.py","tests/unit/test_usage_review.py","tests/unit/test_validate_agent_assets.py","tests/unit/test_workflow_security.py"],"rerunArchitecture":true,"rerunTour":true,"reason":"44 files have structural changes (>30 files) — full rebuild recommended"}
.orchestration/validation/dot-ua-graph-refresh-T33c-a01.md:46:{"baseCommit":"d906b00bff8729625b895d6f7765e3186ab5bb86","headCommit":"935e198406e5df993c84de67c695c7083f4b6b54","action":"FULL_UPDATE","deletedFiles":[".github/dependabot.yml"],"cosmeticFiles":["scripts/check-statusline-tools.py","tests/unit/test_statusline_tools.py"],"ignoredFiles":[".orchestration/acceptance/dot-agmsg-upstream-sync-T19-a01.md",".orchestration/acceptance/dot-asset-manifest-T15-a01.md",".orchestration/acceptance/dot-audit-pane-hardening-T32b-a01.md",".orchestration/acceptance/dot-audit-pane-visibility-T32-a01.md",".orchestration/acceptance/dot-audit-verdict-gate-T33b-a01.md",".orchestration/acceptance/dot-claude-sandbox-T13-a01.md",".orchestration/acceptance/dot-codex-apparmor-userns-T30-a01.md",".orchestration/acceptance/dot-env-converge-T10-a01.md",".orchestration/acceptance/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/acceptance/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/acceptance/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/acceptance/dot-orchestration-rules-T33a-a01.md",".orchestration/acceptance/dot-pr-feedback-gate-T16-a01.md",".orchestration/acceptance/dot-restart-worker-name-wait-T27-a01.md",".orchestration/acceptance/dot-three-role-constellation-T28-a01.md",".orchestration/acceptance/dot-ua-full-T9-a01.md",".orchestration/acceptance/dot-version-currency-T29-a01.md",".orchestration/acceptance/dot-worker-advisor-fable-T26-a01.md",".orchestration/acceptance/dot-worker-kind-guard-T14-a01.md",".orchestration/acceptance/dot-worker-profile-opus55-T24-a01.md",".orchestration/acceptance/refkit-P0-01.md",".orchestration/acceptance/refkit-P0-05.md",".orchestration/acceptance/refkit-P0-06.md",".orchestration/acceptance/refkit-P0-07.md",".orchestration/acceptance/refkit-P1.md",".orchestration/acceptance/refkit-P2-A.md",".orchestration/acceptance/refkit-P2-B.md",".orchestration/acceptance/refkit-P2-C.md",".orchestration/acceptance/refkit-P3.md",".orchestration/acceptance/refkit-P4.md",".orchestration/acceptance/refkit-P5.md",".orchestration/acceptance/refkit-P7.md",".orchestration/acceptance/refkit-P8-a.md",".orchestration/acceptance/refkit-P8-b.md",".orchestration/acceptance/remote-diff-01.md",".orchestration/autoskill/runs/dot-asset-manifest-T15-a01.md",".orchestration/autoskill/runs/dot-audit-pane-hardening-T32b-a01.md",".orchestration/autoskill/runs/dot-audit-pane-visibility-T32-a01.md",".orchestration/autoskill/runs/dot-audit-verdict-gate-T33b-a01.md",".orchestration/autoskill/runs/dot-codex-apparmor-userns-T30-a01.md",".orchestration/autoskill/runs/dot-env-converge-T10-a01.md",".orchestration/autoskill/runs/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/autoskill/runs/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/autoskill/runs/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/autoskill/runs/dot-orchestration-rules-T33a-a01.md",".orchestration/autoskill/runs/dot-restart-worker-name-wait-T27-a01.md",".orchestration/autoskill/runs/dot-three-role-constellation-T28-a01.md",".orchestration/autoskill/runs/dot-ua-full-T9-a01.md",".orchestration/autoskill/runs/dot-version-currency-T29-a01.md",".orchestration/autoskill/runs/dot-worker-advisor-fable-T26-a01.md",".orchestration/autoskill/runs/dot-worker-kind-guard-T14-a01.md",".orchestration/autoskill/runs/dot-worker-profile-opus55-T24-a01.md",".orchestration/autoskill/runs/remote-diff-01.md",".orchestration/learning/dot-asset-manifest-T15-a01.md",".orchestration/learning/dot-audit-pane-hardening-T32b-a01.md",".orchestration/learning/dot-audit-pane-visibility-T32-a01.md",".orchestration/learning/dot-audit-verdict-gate-T33b-a01.md",".orchestration/learning/dot-codex-apparmor-userns-T30-a01.md",".orchestration/learning/dot-env-converge-T10-a01.md",".orchestration/learning/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/learning/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/learning/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/learning/dot-orchestration-rules-T33a-a01.md",".orchestration/learning/dot-restart-worker-name-wait-T27-a01.md",".orchestration/learning/dot-three-role-constellation-T28-a01.md",".orchestration/learning/dot-ua-full-T9-a01.md",".orchestration/learning/dot-version-currency-T29-a01.md",".orchestration/learning/dot-worker-advisor-fable-T26-a01.md",".orchestration/learning/dot-worker-kind-guard-T14-a01.md",".orchestration/learning/dot-worker-profile-opus55-T24-a01.md",".orchestration/learning/remote-diff-01.md",".orchestration/learning/rule_candidates/agmsg-worker-identity-delivery.md",".orchestration/learning/rule_candidates/herdr-worker-relaunch.md",".orchestration/reports/P0-04-sources.md",".orchestration/reports/dot-asset-manifest-T15-a01.md",".orchestration/reports/dot-audit-pane-hardening-T32b-a01.md",".orchestration/reports/dot-audit-pane-visibility-T32-a01.md",".orchestration/reports/dot-audit-verdict-gate-T33b-a01.md",".orchestration/reports/dot-claude-sandbox-T13-a01.md",".orchestration/reports/dot-codex-apparmor-userns-T30-a01.md",".orchestration/reports/dot-env-converge-T10-a01.md",".orchestration/reports/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/reports/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/reports/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/reports/dot-orchestration-rules-T33a-a01.md",".orchestration/reports/dot-restart-worker-name-wait-T27-a01.md",".orchestration/reports/dot-three-role-constellation-T28-a01.md",".orchestration/reports/dot-ua-full-T9-a01.md",".orchestration/reports/dot-version-currency-T29-a01.md",".orchestration/reports/dot-worker-advisor-fable-T26-a01.md",".orchestration/reports/dot-worker-kind-guard-T14-a01.md",".orchestration/reports/dot-worker-profile-opus55-T24-a01.md",".orchestration/reports/remote-diff-01.md",".orchestration/sandboxes/dot-asset-manifest-T15-a01.md",".orchestration/sandboxes/dot-audit-pane-hardening-T32b-a01.md",".orchestration/sandboxes/dot-audit-pane-visibility-T32-a01.md",".orchestration/sandboxes/dot-audit-verdict-gate-T33b-a01.md",".orchestration/sandboxes/dot-codex-apparmor-userns-T30-a01.md",".orchestration/sandboxes/dot-env-converge-T10-a01.md",".orchestration/sandboxes/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/sandboxes/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/sandboxes/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/sandboxes/dot-orchestration-rules-T33a-a01.md",".orchestration/sandboxes/dot-restart-worker-name-wait-T27-a01.md",".orchestration/sandboxes/dot-three-role-constellation-T28-a01.md",".orchestration/sandboxes/dot-ua-full-T9-a01.md",".orchestration/sandboxes/dot-version-currency-T29-a01.md",".orchestration/sandboxes/dot-worker-advisor-fable-T26-a01.md",".orchestration/sandboxes/dot-worker-kind-guard-T14-a01.md",".orchestration/sandboxes/dot-worker-profile-opus55-T24-a01.md",".orchestration/sandboxes/remote-diff-01.md",".orchestration/tasks/dot-agmsg-upstream-sync-T19-a01.md",".orchestration/tasks/dot-asset-manifest-T15-a01.md",".orchestration/tasks/dot-audit-exec-channel-T33e-a01.md",".orchestration/tasks/dot-audit-pane-hardening-T32b-a01.md",".orchestration/tasks/dot-audit-pane-visibility-T32-a01.md",".orchestration/tasks/dot-audit-verdict-gate-T33b-a01.md",".orchestration/tasks/dot-claude-sandbox-T13-a01.md",".orchestration/tasks/dot-codex-apparmor-userns-T30-a01.md",".orchestration/tasks/dot-env-converge-T10-a01.md",".orchestration/tasks/dot-herdr-agents-add-worker-T22-a01.md",".orchestration/tasks/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/tasks/dot-herdr-worker-worktree-T11-a01.md",".orchestration/tasks/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/tasks/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/tasks/dot-orchestration-rules-T33a-a01.md",".orchestration/tasks/dot-orchestrator-guardrails-T21-a01.md",".orchestration/tasks/dot-permgate-bench-flake-T33d-a01.md",".orchestration/tasks/dot-pr-feedback-gate-T16-a01.md",".orchestration/tasks/dot-restart-worker-name-wait-T27-a01.md",".orchestration/tasks/dot-runner-label-pin-T18-a01.md",".orchestration/tasks/dot-task-contract-v2-T23-a01.md",".orchestration/tasks/dot-three-role-constellation-T28-a01.md",".orchestration/tasks/dot-ua-full-T9-a01.md",".orchestration/tasks/dot-ua-graph-refresh-T33c-a01.md",".orchestration/tasks/dot-ua-hook-regex-T12-a01.md",".orchestration/tasks/dot-ua-incremental-T20-a01.md",".orchestration/tasks/dot-version-currency-T29-a01.md",".orchestration/tasks/dot-worker-advisor-fable-T26-a01.md",".orchestration/tasks/dot-worker-kind-guard-T14-a01.md",".orchestration/tasks/dot-worker-profile-opus55-T24-a01.md",".orchestration/tasks/refkit-P0-01.md",".orchestration/tasks/refkit-P0-05.md",".orchestration/tasks/refkit-P0-06.md",".orchestration/tasks/refkit-P0-07.md",".orchestration/tasks/refkit-P1.md",".orchestration/tasks/refkit-P10.md",".orchestration/tasks/refkit-P2-A.md",".orchestration/tasks/refkit-P2-B.md",".orchestration/tasks/refkit-P2-C.md",".orchestration/tasks/refkit-P3.md",".orchestration/tasks/refkit-P4.md",".orchestration/tasks/refkit-P4b.md",".orchestration/tasks/refkit-P5.md",".orchestration/tasks/refkit-P6.md",".orchestration/tasks/refkit-P7.md",".orchestration/tasks/refkit-P8-a.md",".orchestration/tasks/refkit-P8-b.md",".orchestration/tasks/refkit-P8.md",".orchestration/tasks/refkit-P9.md",".orchestration/validation/baseline-20260925.md",".orchestration/validation/dot-asset-manifest-T15-a01.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-audit.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-crit.json",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-live-e2e.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01-receipt.md",".orchestration/validation/dot-audit-pane-hardening-T32b-a01.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-audit.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-crit.json",".orchestration/validation/dot-audit-pane-visibility-T32-a01-live-e2e.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01-receipt.md",".orchestration/validation/dot-audit-pane-visibility-T32-a01.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev2.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit-rev3.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-audit.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-crit.json",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-live-e2e.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01-receipt.md",".orchestration/validation/dot-audit-verdict-gate-T33b-a01.md",".orchestration/validation/dot-claude-sandbox-T13-a01.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-audit.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-crit.json",".orchestration/validation/dot-codex-apparmor-userns-T30-a01-receipt.md",".orchestration/validation/dot-codex-apparmor-userns-T30-a01.md",".orchestration/validation/dot-env-converge-T10-a01.md",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01-crit.json",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01-receipt.md",".orchestration/validation/dot-herdr-worker-relaunch-T25-a01.md",".orchestration/validation/dot-macos-crit-pinned-install-T17-a01-crit.json",".orchestration/validation/dot-macos-crit-pinned-install-T17-a01.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-audit.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-crit.json",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01-receipt.md",".orchestration/validation/dot-mosh-and-asset-bumps-T31-a01.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-audit-rev3.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-audit.md",".orchestration/validation/dot-orchestration-rules-T33a-a01-crit.json",".orchestration/validation/dot-orchestration-rules-T33a-a01-receipt.md",".orchestration/validation/dot-orchestration-rules-T33a-a01.md",".orchestration/validation/dot-restart-worker-name-wait-T27-a01-crit.json",".orchestration/validation/dot-restart-worker-name-wait-T27-a01-receipt.md",".orchestration/validation/dot-restart-worker-name-wait-T27-a01.md",".orchestration/validation/dot-three-role-constellation-T28-a01-audit.md",".orchestration/validation/dot-three-role-constellation-T28-a01-crit.json",".orchestration/validation/dot-three-role-constellation-T28-a01-receipt.md",".orchestration/validation/dot-three-role-constellation-T28-a01.md",".orchestration/validation/dot-ua-full-T9-a01.md",".orchestration/validation/dot-version-currency-T29-a01-audit.md",".orchestration/validation/dot-version-currency-T29-a01-crit.json",".orchestration/validation/dot-version-currency-T29-a01-receipt.md",".orchestration/validation/dot-version-currency-T29-a01.md",".orchestration/validation/dot-worker-advisor-fable-T26-a01-crit.json",".orchestration/validation/dot-worker-advisor-fable-T26-a01-receipt.md",".orchestration/validation/dot-worker-advisor-fable-T26-a01.md",".orchestration/validation/dot-worker-kind-guard-T14-a01.md",".orchestration/validation/dot-worker-profile-opus55-T24-a01-crit.json",".orchestration/validation/dot-worker-profile-opus55-T24-a01-receipt.md",".orchestration/validation/dot-worker-profile-opus55-T24-a01.md",".orchestration/validation/remote-diff-01.md","home/dot_mise/mise.lock"],"generatedArtifactFiles":[".ua/.understandignore",".ua/fingerprints.json",".ua/knowledge-graph.json",".ua/meta.json"],"importMapRefreshPaths":[".chezmoiroot",".claude/contextdb/config.json",".claude/contextdb/contextdb/__init__.py",".claude/contextdb/contextdb/cli.py",".claude/contextdb/contextdb/config.py",".claude/contextdb/contextdb/hook.py",".claude/contextdb/contextdb/memory.py",".claude/contextdb/contextdb/normalize.py",".claude/contextdb/contextdb/paths.py",".claude/contextdb/contextdb/probe.py",".claude/contextdb/contextdb/recall.py",".claude/contextdb/contextdb/recover_hook.py",".claude/contextdb/contextdb/recovery.py",".claude/contextdb/contextdb/redaction.py",".claude/contextdb/contextdb/semantic.py",".claude/contextdb/contextdb/spool.py",".claude/contextdb/contextdb/storage.py",".claude/contextdb/contextdb/util.py",".claude/contextdb/health/.gitkeep",".claude/contextdb/spool/incoming/.gitkeep",".claude/contextdb/spool/quarantine/.gitkeep",".claude/contextdb/state/.gitkeep",".claude/hooks/contextdb_cli.py",".claude/hooks/contextdb_hook.py",".claude/hooks/contextdb_recover.py",".claude/hooks/query_log.py",".claude/settings.json",".github/copilot-instructions.md",".github/funding.yaml",".github/workflows/agent-assets.yml",".github/workflows/docs.yml",".github/workflows/macos.yaml",".github/workflows/remote.yaml",".github/workflows/test.yaml",".github/workflows/ubuntu.yaml",".simplecov","AGENTS.md","CLAUDE.md","Dockerfile","Makefile","README.md","codecov.yml","docs/assets/stylesheets/extra.css","docs/plans/nix-first-architecture.md","docs/plans/nix-migration.md","docs/verification/acceptance/005.md","flake.nix","home/.chezmoi.yaml.tmpl","home/.chezmoiexternal.yaml.tmpl","home/.chezmoiignore","home/.chezmoiremove","home/.chezmoiscripts/common/run_once_after_01-setup-chezmoi-private.sh.tmpl","home/.chezmoiscripts/common/run_once_after_02-install-mise.sh.tmpl","home/.chezmoiscripts/common/run_once_after_03-install-sheldon.sh.tmpl","home/.chezmoiscripts/common/run_once_after_06-install-agent-assets.sh.tmpl","home/.chezmoiscripts/common/run_once_after_99-install-gh-extensions.sh.tmpl","home/.chezmoiscripts/common/run_once_before_01-decrypt-private-key.sh.tmpl","home/.chezmoiscripts/macos/run_once_04-install-ghostty.sh.tmpl","home/.chezmoiscripts/macos/run_once_10-install-docker.sh.tmpl","home/.chezmoiscripts/macos/run_once_99-install-defaults.sh.tmpl","home/.chezmoiscripts/macos/run_once_after_50-install-misc.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_01-prepare-system.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_02-install-command-line-tool.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_03-install-brew.sh.tmpl","home/.chezmoiscripts/macos/run_once_before_50-install-dependencies.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_00-setup-ssh.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_10-install-docker.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_10-install-starship.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-docker-ssh.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-install-mics.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_50-setup-locale.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_51-client-default-shell.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_52-client-install-zed.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_53-client-install-tailscale.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_99-client-gnome-defaults.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_after_04-install-aws-cli.sh.tmpl","home/.chezmoiscripts/ubuntu/run_once_before_50-common-dependencies.sh.tmpl","home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl","home/.chezmoiscripts/ubuntu/run_onchange_after_60-enable-usage-snapshot-timer.sh.tmpl","home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl","home/.chezmoitemplates/chezmoiexternal.d/macos.yaml.tmpl","home/.chezmoitemplates/chezmoiexternal.d/ubuntu.yaml.tmpl","home/.chezmoitemplates/chezmoiignore.d/common","home/.chezmoitemplates/chezmoiignore.d/macos","home/.chezmoitemplates/chezmoiignore.d/ubuntu/client","home/.chezmoitemplates/chezmoiignore.d/ubuntu/common","home/.chezmoitemplates/chezmoiignore.d/ubuntu/server","home/.chezmoitemplates/claude-settings-managed.json","home/.chezmoitemplates/codex-config-managed.toml","home/.key.txt.age","home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist.tmpl","home/dot_agents/README.md","home/dot_agents/agent-config.yaml","home/dot_agents/model-profiles.env","home/dot_agents/permgate-policy.yaml","home/dot_agents/plugins/create_marketplace.json","home/dot_agents/plugins/mryfmo-dev-workflows/.codex-plugin/plugin.json","home/dot_agents/skills/agmsg-orchestration/SKILL.md","home/dot_agents/skills/agmsg/SKILL.md","home/dot_agents/skills/agmsg/agents/openai.yaml","home/dot_agents/skills/agmsg/db/.keep","home/dot_agents/skills/agmsg/run/.keep","home/dot_agents/skills/agmsg/scripts/executable_actas-claim.sh","home/dot_agents/skills/agmsg/scripts/executable_check-inbox.sh","home/dot_agents/skills/agmsg/scripts/executable_config.sh","home/dot_agents/skills/agmsg/scripts/executable_delivery.sh","home/dot_agents/skills/agmsg/scripts/executable_history.sh","home/dot_agents/skills/agmsg/scripts/executable_hook.sh","home/dot_agents/skills/agmsg/scripts/executable_identities.sh","home/dot_agents/skills/agmsg/scripts/executable_inbox.sh","home/dot_agents/skills/agmsg/scripts/executable_init-db.sh","home/dot_agents/skills/agmsg/scripts/executable_join.sh","home/dot_agents/skills/agmsg/scripts/executable_leave.sh","home/dot_agents/skills/agmsg/scripts/executable_rename-team.sh","home/dot_agents/skills/agmsg/scripts/executable_rename.sh","home/dot_agents/skills/agmsg/scripts/executable_reset.sh","home/dot_agents/skills/agmsg/scripts/executable_send.sh","home/dot_agents/skills/agmsg/scripts/executable_session-end.sh","home/dot_agents/skills/agmsg/scripts/executable_session-start.sh","home/dot_agents/skills/agmsg/scripts/executable_team.sh","home/dot_agents/skills/agmsg/scripts/executable_watch.sh","home/dot_agents/skills/agmsg/scripts/executable_whoami.sh","home/dot_agents/skills/agmsg/scripts/lib/actas-lock.sh","home/dot_agents/skills/agmsg/scripts/lib/identifier.sh","home/dot_agents/skills/agmsg/scripts/lib/storage.sh","home/dot_agents/skills/agmsg/scripts/release/executable_sync-version.sh","home/dot_agents/skills/agmsg/teams/.keep","home/dot_agents/skills/agmsg/templates/cmd.antigravity.md","home/dot_agents/skills/agmsg/templates/cmd.claude-code.md","home/dot_agents/skills/agmsg/templates/cmd.codex.md","home/dot_agents/skills/agmsg/templates/cmd.copilot.md","home/dot_agents/skills/agmsg/templates/cmd.gemini.md","home/dot_agents/skills/convert-to-transformers/SKILL.md","home/dot_agents/skills/convert-to-transformers/references/common-pitfalls.md","home/dot_agents/skills/convert-to-transformers/references/learnings.md","home/dot_agents/skills/gh-comment-attach-files/SKILL.md","home/dot_agents/skills/gh-comment-attach-files/agents/openai.yaml","home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py","home/dot_agents/skills/gh-first-workflow/SKILL.md","home/dot_agents/skills/gh-first-workflow/agents/openai.yaml","home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md","home/dot_agents/skills/humanizer-ja/SKILL.md","home/dot_agents/skills/humanizer-ja/agents/openai.yaml","home/dot_agents/skills/humanizer-ja/references/ai-patterns-ja.md","home/dot_agents/skills/python-uv-workflow/SKILL.md","home/dot_agents/skills/python-uv-workflow/agents/openai.yaml","home/dot_agents/skills/python-uv-workflow/references/python-uv-rules.md","home/dot_agents/skills/shdoc-shell-docs/SKILL.md","home/dot_agents/skills/shdoc-shell-docs/agents/openai.yaml","home/dot_agents/skills/shdoc-shell-docs/references/shdoc-rules.md","home/dot_bash/client/bashrc","home/dot_bash/server/bashrc","home/dot_ccstatusline/settings.json","home/dot_claude/agents/express-explorer.md","home/dot_claude/commands/commit.md","home/dot_claude/commands/symlink_agmsg.md.tmpl","home/dot_claude/hooks/executable_enforce-uv.sh","home/dot_claude/hooks/executable_format-edited-files.py","home/dot_claude/modify_private_settings.json","home/dot_claude/private_mcp.json.tmpl","home/dot_claude/rules/symlink_agmsg-orchestration.md.tmpl","home/dot_claude/rules/symlink_ask-user-question.md.tmpl","home/dot_claude/rules/symlink_compactiondb.md.tmpl","home/dot_claude/rules/symlink_crit-review.md.tmpl","home/dot_claude/rules/symlink_gpu.md.tmpl","home/dot_claude/rules/symlink_latex.md.tmpl","home/dot_claude/rules/symlink_model-selection.md.tmpl","home/dot_claude/rules/symlink_ponytail.md.tmpl","home/dot_claude/rules/symlink_python.md.tmpl","home/dot_claude/rules/symlink_understand-anything.md.tmpl","home/dot_claude/skills/agmsg-orchestration/symlink_SKILL.md.tmpl","home/dot_claude/skills/agmsg/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_actas-lock.sh.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_identifier.sh.tmpl","home/dot_claude/skills/agmsg/scripts/lib/symlink_storage.sh.tmpl","home/dot_claude/skills/agmsg/scripts/release/symlink_sync-version.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_actas-claim.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_check-inbox.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_config.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_delivery.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_history.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_hook.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_identities.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_inbox.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_init-db.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_join.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_leave.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_rename-team.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_rename.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_reset.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_send.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_session-end.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_session-start.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_team.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_watch.sh.tmpl","home/dot_claude/skills/agmsg/scripts/symlink_whoami.sh.tmpl","home/dot_claude/skills/agmsg/symlink_SKILL.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.antigravity.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.claude-code.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.codex.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.copilot.md.tmpl","home/dot_claude/skills/agmsg/templates/symlink_cmd.gemini.md.tmpl","home/dot_claude/skills/convert-to-transformers/references/symlink_common-pitfalls.md.tmpl","home/dot_claude/skills/convert-to-transformers/references/symlink_learnings.md.tmpl","home/dot_claude/skills/convert-to-transformers/symlink_SKILL.md.tmpl","home/dot_claude/skills/gh-comment-attach-files/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/gh-comment-attach-files/scripts/symlink_attach_comment_files.py.tmpl","home/dot_claude/skills/gh-comment-attach-files/symlink_SKILL.md.tmpl","home/dot_claude/skills/gh-first-workflow/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/gh-first-workflow/references/symlink_gh-git-rules.md.tmpl","home/dot_claude/skills/gh-first-workflow/symlink_SKILL.md.tmpl","home/dot_claude/skills/humanizer-ja/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/humanizer-ja/references/symlink_ai-patterns-ja.md.tmpl","home/dot_claude/skills/humanizer-ja/symlink_SKILL.md.tmpl","home/dot_claude/skills/python-uv-workflow/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/python-uv-workflow/references/symlink_python-uv-rules.md.tmpl","home/dot_claude/skills/python-uv-workflow/symlink_SKILL.md.tmpl","home/dot_claude/skills/shdoc-shell-docs/agents/symlink_openai.yaml.tmpl","home/dot_claude/skills/shdoc-shell-docs/references/symlink_shdoc-rules.md.tmpl","home/dot_claude/skills/shdoc-shell-docs/symlink_SKILL.md.tmpl","home/dot_codex/modify_private_adh.config.toml","home/dot_codex/modify_private_audit.config.toml","home/dot_codex/modify_private_config.toml","home/dot_codex/modify_private_deep.config.toml","home/dot_codex/modify_private_express.config.toml","home/dot_codex/modify_private_review.config.toml","home/dot_codex/modify_private_security.config.toml","home/dot_codex/modify_private_standard.config.toml","home/dot_codex/symlink_AGENTS.md.tmpl","home/dot_config/alias/client.sh","home/dot_config/alias/common.sh","home/dot_config/alias/server.sh","home/dot_config/ccstatusline/symlink_settings.json.tmpl","home/dot_config/claude/rules/agmsg-orchestration.md","home/dot_config/claude/rules/ask-user-question.md","home/dot_config/claude/rules/compactiondb.md","home/dot_config/claude/rules/crit-review.md","home/dot_config/claude/rules/gpu.md","home/dot_config/claude/rules/latex.md","home/dot_config/claude/rules/model-selection.md","home/dot_config/claude/rules/ponytail.md","home/dot_config/claude/rules/python.md","home/dot_config/claude/rules/understand-anything.md","home/dot_config/codex/AGENTS.md","home/dot_config/ghostty/config","home/dot_config/git/config.tmpl","home/dot_config/git/ignore","home/dot_config/gwq/config.toml","home/dot_config/herdr/config.toml","home/dot_config/herdr/plugins/config/herdr-file-viewer/config.toml","home/dot_config/mise/config.toml.tmpl","home/dot_config/mise/mise.lock.tmpl","home/dot_config/powerlevel10k/p10k.zsh","home/dot_config/sheldon/plugin_sources/client/common.toml","home/dot_config/sheldon/plugin_sources/client/macos.toml","home/dot_config/sheldon/plugin_sources/client/ubuntu.toml","home/dot_config/sheldon/plugin_sources/common.toml","home/dot_config/sheldon/plugin_sources/server.toml","home/dot_config/sheldon/plugins.toml.tmpl","home/dot_config/starship.toml","home/dot_config/systemd/user/usage-snapshot.service.tmpl","home/dot_config/systemd/user/usage-snapshot.timer.tmpl","home/dot_config/tango.yml","home/dot_config/uv/uv.toml","home/dot_config/yazi/yazi.toml","home/dot_config/zed/keymap.json","home/dot_config/zed/settings.json","home/dot_config/zsh/plugins/chezmoi-notify/chezmoi-notify.plugin.zsh","home/dot_local/bin/common/executable_agent-fanout","home/dot_local/bin/common/executable_agent-session-staleness","home/dot_local/bin/common/executable_agmsg-dispatch","home/dot_local/bin/common/executable_cdgwq","home/dot_local/bin/common/executable_cdw","home/dot_local/bin/common/executable_chezmoi-cd","home/dot_local/bin/common/executable_compactiondb-install","home/dot_local/bin/common/executable_contextdb-codex-notify","home/dot_local/bin/common/executable_dev","home/dot_local/bin/common/executable_fgc","home/dot_local/bin/common/executable_git-delete-merged-branches","home/dot_local/bin/common/executable_herdr-agents","home/dot_local/bin/common/executable_herdr-session","home/dot_local/bin/common/executable_permgate","home/dot_local/bin/common/executable_provision-machine-key","home/dot_local/bin/common/executable_remove-agent-asset","home/dot_local/bin/common/executable_setup-gh","home/dot_local/bin/common/executable_setup-gpg","home/dot_local/bin/common/executable_setup-python-env","home/dot_local/bin/common/executable_uv-format","home/dot_local/bin/server/cache.sh","home/dot_local/bin/server/cuda.sh","home/dot_local/bin/server/history.sh","home/dot_local/bin/server/ssh_agent.sh","home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc","home/dot_mise/config.toml","home/dot_npmrc","home/dot_profile","home/dot_vimrc","home/dot_zprofile","home/dot_zshenv","home/dot_zshrc","home/private_dot_gnupg/gpg-agent.conf.tmpl","home/private_dot_ssh/private_config","home/symlink_dot_bashrc.tmpl","install/common/chezmoi_private.sh","install/common/gh_extensions.sh","install/common/mise.sh","install/common/sheldon.sh","install/macos/arm64/prepare_arm64_system.sh","install/macos/arm64/run.sh","install/macos/common/brew.sh","install/macos/common/command_line_tool.sh","install/macos/common/defaults.sh","install/macos/common/dependencies.sh","install/macos/common/docker.sh","install/macos/common/ghostty.sh","install/macos/common/misc.sh","install/ubuntu/client/default_shell.sh","install/ubuntu/client/docker.sh","install/ubuntu/client/ghostty.sh","install/ubuntu/client/gnome_settings.sh","install/ubuntu/client/misc.sh","install/ubuntu/client/tailscale.sh","install/ubuntu/client/zed.sh","install/ubuntu/common/apparmor/bwrap-userns","install/ubuntu/common/apparmor_userns.sh","install/ubuntu/common/aws_cli.sh","install/ubuntu/common/dependencies.sh","install/ubuntu/common/setup_locale.sh","install/ubuntu/common/ssh.sh","install/ubuntu/server/misc.sh","install/ubuntu/server/setup_timezone.sh","install/ubuntu/server/ssh_server.sh","install/ubuntu/server/starship.sh","mise.toml","mkdocs.yml","nix/home-manager/default.nix","nix/nix-darwin/default.nix","nix/shared/packages.nix","plans/001-contain-starship-cleanup.md","plans/002-make-review-evidence-non-vacuous.md","plans/003-make-bootstrap-safe-and-publicly-testable.md","plans/004-harden-and-lock-the-supply-chain.md","plans/005-make-runtime-health-and-verification-truthful.md","plans/README.md","renovate.json","scripts/check-agent-runtime.py","scripts/check-statusline-tools.py","scripts/check-tools.sh","scripts/generate-agent-configs.py","scripts/generate-docs.sh","scripts/lib/asset-manifest.sh","scripts/lib/installer-pins.sh","scripts/refresh-mkdocs-toc.py","scripts/require-crit-review.py","scripts/run_bashcov_unit_test.rb","scripts/run_benchmark.sh","scripts/run_unit_test.sh","scripts/update-agent-assets.sh","scripts/upgrade-tools.sh","scripts/usage-report.py","scripts/usage-snapshot.sh","scripts/validate-agent-assets.py","setup.sh","tests/files/common.bats","tests/files/helpers.bash","tests/files/macos.bats","tests/files/ubuntu.bats","tests/install/common/check_tools.bats","tests/install/common/chezmoi_private.bats","tests/install/common/decrypt_private_key.bats","tests/install/common/gh_extensions.bats","tests/install/common/lifecycle.bats","tests/install/common/mise.bats","tests/install/common/private_layer.bats","tests/install/common/provision_machine_key.bats","tests/install/common/setup.bats","tests/install/macos/common/brew.bats","tests/install/macos/common/defaults.bats","tests/install/macos/common/docker.bats","tests/install/macos/common/ghostty.bats","tests/install/macos/common/misc.bats","tests/install/ubuntu/client/default_shell.bats","tests/install/ubuntu/client/docker.bats","tests/install/ubuntu/client/ghostty.bats","tests/install/ubuntu/client/gnome_settings.bats","tests/install/ubuntu/client/misc.bats","tests/install/ubuntu/client/tailscale.bats","tests/install/ubuntu/client/zed.bats","tests/install/ubuntu/common/dependencies.bats","tests/install/ubuntu/common/dependencies_unit.bats","tests/install/ubuntu/common/setup_locale.bats","tests/install/ubuntu/common/ssh.bats","tests/install/ubuntu/server/setup_timezone.bats","tests/install/ubuntu/server/sheldon.bats","tests/install/ubuntu/server/starship.bats","tests/unit/test_agent_session_staleness.py","tests/unit/test_agmsg_dispatch.py","tests/unit/test_agmsg_send.py","tests/unit/test_apparmor_userns.py","tests/unit/test_asset_manifest.py","tests/unit/test_aws_cli_acquisition.py","tests/unit/test_check_agent_runtime.py","tests/unit/test_claude_settings_merge.py","tests/unit/test_codex_config_merge.py","tests/unit/test_contextdb_codex_notify.py","tests/unit/test_files_fixture.py","tests/unit/test_generate_agent_configs.py","tests/unit/test_herdr_agents.py","tests/unit/test_permgate.py","tests/unit/test_release_asset_pins.py","tests/unit/test_remove_agent_asset.py","tests/unit/test_require_crit_review.py","tests/unit/test_runtime_health.py","tests/unit/test_statusline_tools.py","tests/unit/test_supply_chain_policy.py","tests/unit/test_usage_review.py","tests/unit/test_validate_agent_assets.py","tests/unit/test_workflow_security.py"],"rerunArchitecture":true,"rerunTour":true,"reason":"44 files have structural changes (>30 files) — full rebuild recommended"}
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:10573:+      "id": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:10576:+      "filePath": "docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:10600:+      "id": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:10603:+      "filePath": "docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:11712:-      "id": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:11715:-      "filePath": "docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:11736:-      "id": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:11739:-      "filePath": "docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19374:-      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19381:-      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19388:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19395:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19402:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19409:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19416:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19630:+      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19641:+      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19652:+      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19663:+      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19674:+      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19685:+      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19696:+      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:19697:+      "target": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:25582:         "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:25583:         "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:25856:+        "document:docs/plans/nix-first-architecture.md"
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:36973:+      "id": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:36976:+      "filePath": "docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:37000:+      "id": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:37003:+      "filePath": "docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:38112:-      "id": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:38115:-      "filePath": "docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:38136:-      "id": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:38139:-      "filePath": "docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44239:-      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44246:-      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44253:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44260:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44267:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44274:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44281:-      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44495:+      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44506:+      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44517:+      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44528:+      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44539:+      "source": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44550:+      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44561:+      "source": "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:44562:+      "target": "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:50447:         "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:50448:         "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T36-a01-audit.md:50721:+        "document:docs/plans/nix-first-architecture.md"
.orchestration/validation/dot-ua-graph-refresh-T41-a01-audit-rev2.md:1088:| `docs/plans/nix-first-architecture.md` | 0 | 0 | 0 | - | - | yes |
.orchestration/validation/dot-ua-graph-refresh-T41-a01-audit-rev2.md:1089:| `docs/plans/nix-migration.md` | 0 | 0 | 0 | - | - | yes |
.orchestration/validation/dot-ua-graph-refresh-T41-a01-audit.md:4583:        "document:docs/plans/nix-first-architecture.md",
.orchestration/validation/dot-ua-graph-refresh-T41-a01-audit.md:4584:        "document:docs/plans/nix-migration.md",
.orchestration/validation/dot-ua-graph-refresh-T41-a01.md:391:| `docs/plans/nix-first-architecture.md` | 0 | 0 | 0 | - | - | yes |
.orchestration/validation/dot-ua-graph-refresh-T41-a01.md:392:| `docs/plans/nix-migration.md` | 0 | 0 | 0 | - | - | yes |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md:765:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md:766:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md:1396:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md:1397:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md:2601:ADD EDGE {'source': 'document:docs/plans/nix-migration.md', 'target': 'document:docs/plans/nix-first-architecture.md', 'type': 'related', 'direction': 'forward', 'weight': 0.5}
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit-rev1.md:3983:document:docs/plans/nix-migration.md -> document:docs/plans/nix-first-architecture.md related 
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md:653:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md:654:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md:2473:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md:2474:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01-audit.md:4216:('document:docs/plans/nix-migration.md', 'document:docs/plans/nix-first-architecture.md', 'related')
.orchestration/validation/dot-ua-graph-refresh-T55-a01.md:72:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01.md:73:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01.md:703:| docs/plans/nix-first-architecture.md | 0 | 0 | - | ok |  |
.orchestration/validation/dot-ua-graph-refresh-T55-a01.md:704:| docs/plans/nix-migration.md | 0 | 0 | - | ok |  |
.orchestration/validation/dotfiles-T72-bootstrap-ci-pins-a01-audit-d5856e2.md:2572:{"id": "document:docs/plans/nix-migration.md", "filePath": "docs/plans/nix-migration.md", "summary": "Phased Nix migration plan (opt-in scaffold, package-only adoption, host roles, selective config migration, optional Nix-first bootstrap) with principles and rollback notes."}
.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-audit-60688d49.md:1705:   382	        ownership = (ROOT / "docs/plans/nix-first-architecture.md").read_text()
.orchestration/validation/dotfiles-T73-tool-versions-from-config-a01-audit-60688d49.md:1706:   383	        migration = (ROOT / "docs/plans/nix-migration.md").read_text()
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:1327:5. **Nix:** delete `flake.nix`, `flake.lock`, `nix/**`. In `.github/workflows/test.yaml` delete the `should_nix` output (line 21), its filter block (80-84) and the `nix` job (415-437). In `tests/unit/test_supply_chain_policy.py` delete `test_nix_inputs_lock_and_ci_use_2605` (460-473) and any now-unused import. `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` and `plans/004-harden-and-lock-the-supply-chain.md` mention nix: do not edit them (T78/T83 own prose); list the stale sentences in the report.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:1418:| 4175951412 P2 "Update Nix documentation after deleting the flake" | 2487b05a | `not-applicable`: `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` are prose owned by T78/T83, and this task forbids editing them. The stale sentences are listed below for those tasks. |
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:1422:- `docs/plans/nix-first-architecture.md:16, 58, 64, 70, 76`: the flake outputs, the `home-manager switch --flake .#mryfmo-linux/darwin`, `darwin-rebuild switch --flake .#mryfmo-mac` and `nix flake check` commands.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:1423:- `docs/plans/nix-migration.md:23-26, 33-34, 37, 110`: add `flake.nix` and the `nix/**` modules, `nix flake show/check`, the "CI evaluates every declared output", and the flake.lock regression procedure.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:1472:## flake / should_nix / nix/ -> test.yaml:21,80-84,415-437; test_supply_chain_policy.py:461-477; flake.nix; nix/**; prose in docs/plans/nix-*.md and plans/004-*.md (not edited)
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3067:## flake / should_nix / nix/ -> test.yaml:21,80-84,415-437; test_supply_chain_policy.py:461-477; flake.nix; nix/**; prose in docs/plans/nix-*.md and plans/004-*.md (not edited)
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3631:/usr/bin/zsh -lc 'git show 2487b05a:docs/plans/nix-migration.md' in ~/Workspace/dotfiles
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3847:2487b05a:docs/plans/nix-first-architecture.md:10:- The new Nix files are opt-in and should not change existing machines unless a user explicitly runs Home Manager or nix-darwin commands.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3848:2487b05a:docs/plans/nix-first-architecture.md:19:- A nix-darwin output:
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3849:2487b05a:docs/plans/nix-first-architecture.md:58:nix run github:nix-community/home-manager/release-26.05 -- switch --flake .#mryfmo-linux
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3850:2487b05a:docs/plans/nix-first-architecture.md:64:nix run github:nix-community/home-manager/release-26.05 -- switch --flake .#mryfmo-darwin
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3851:2487b05a:docs/plans/nix-first-architecture.md:67:nix-darwin on Apple Silicon macOS:
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3852:2487b05a:docs/plans/nix-first-architecture.md:70:sudo darwin-rebuild switch --flake .#mryfmo-mac
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3853:2487b05a:docs/plans/nix-first-architecture.md:76:nix flake check --no-build --no-update-lock-file
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3854:2487b05a:docs/plans/nix-first-architecture.md:77:nix eval --no-update-lock-file .#homeConfigurations.mryfmo-linux.activationPackage.drvPath
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3855:2487b05a:docs/plans/nix-first-architecture.md:78:nix eval --no-update-lock-file .#homeConfigurations.mryfmo-darwin.activationPackage.drvPath
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3856:2487b05a:docs/plans/nix-first-architecture.md:79:nix eval --no-update-lock-file .#darwinConfigurations.mryfmo-mac.system.drvPath
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3857:2487b05a:docs/plans/nix-first-architecture.md:82:The nix-darwin configuration enables Homebrew management, but `homebrew.enable` does not install Homebrew itself. Install Homebrew before activating nix-darwin if Homebrew management is needed.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3858:2487b05a:docs/plans/nix-migration.md:23:- Add `flake.nix`.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3859:2487b05a:docs/plans/nix-migration.md:26:- Add a minimal nix-darwin module at `nix/nix-darwin/default.nix`.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3860:2487b05a:docs/plans/nix-migration.md:33:nix flake show --no-update-lock-file
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3861:2487b05a:docs/plans/nix-migration.md:34:nix flake check --no-build --no-update-lock-file
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3862:2487b05a:docs/plans/nix-migration.md:37:If Nix is unavailable on a machine, CI evaluates every declared output on Linux and macOS. Never hand-edit `flake.lock`; regenerate it with `nix flake lock`.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3863:2487b05a:docs/plans/nix-migration.md:57:- nix-darwin activation does not assume Homebrew is already installed beyond documented behavior.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3864:2487b05a:docs/plans/nix-migration.md:96:This should remain separate from `setup.sh` unless the repository owner decides to change the default bootstrap model. A future bootstrap may install Nix, activate Home Manager or nix-darwin, and then run chezmoi for public and private dotfiles.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3865:2487b05a:docs/plans/nix-migration.md:100:Home Manager standalone rollback is generally handled with Home Manager generations. nix-darwin rollback is handled with system generations. Package-only changes should be low risk, but any future file ownership migration must include explicit rollback instructions because ownership collisions can block activation or overwrite expected state.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3866:2487b05a:docs/plans/nix-migration.md:110:For flake input regressions, revert the Git commit that changed `flake.nix` or `flake.lock`, then re-run the relevant Home Manager or nix-darwin switch command.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3867:2487b05a:plans/004-harden-and-lock-the-supply-chain.md:9:> **Drift check**: `git diff --stat e7c2808..HEAD -- setup.sh install home/dot_mise home/dot_config/sheldon home/.chezmoitemplates/chezmoiexternal.d .github/workflows flake.nix flake.lock docs/plans/nix-first-architecture.md tests`
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:3880:/usr/bin/zsh -lc 'git show 2487b05a:docs/plans/nix-first-architecture.md' in ~/Workspace/dotfiles
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:4683:/usr/bin/zsh -lc "git grep -n -F -e 'nix-first-architecture' -e 'nix-migration' 2487b05a -- README.md docs mkdocs.yml scripts ':"'!docs/plans/nix-first-architecture.md'"' ':"'!docs/plans/nix-migration.md'"'" in ~/Workspace/dotfiles
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:4705:- [P2] High confidence `flake.nix:1` (deleted) — Removing the flake leaves `docs/plans/nix-first-architecture.md:58–79` advertising activation and evaluation commands that now fail because their flake is absent. Update or retire those instructions alongside the removal.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md:4717:- [P2] High confidence `flake.nix:1` (deleted) — Removing the flake leaves `docs/plans/nix-first-architecture.md:58–79` advertising activation and evaluation commands that now fail because their flake is absent. Update or retire those instructions alongside the removal.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-2487b05a.md.last.md:2:- [P2] High confidence `flake.nix:1` (deleted) — Removing the flake leaves `docs/plans/nix-first-architecture.md:58–79` advertising activation and evaluation commands that now fail because their flake is absent. Update or retire those instructions alongside the removal.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:1137:| 4175951412 P2 "Update Nix documentation after deleting the flake" | 2487b05a | `not-applicable`: `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` are prose owned by T78/T83, and this task forbids editing them. The stale sentences are listed below for those tasks. |
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:1141:- `docs/plans/nix-first-architecture.md:16, 58, 64, 70, 76`: the flake outputs, the `home-manager switch --flake .#mryfmo-linux/darwin`, `darwin-rebuild switch --flake .#mryfmo-mac` and `nix flake check` commands.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:1142:- `docs/plans/nix-migration.md:23-26, 33-34, 37, 110`: add `flake.nix` and the `nix/**` modules, `nix flake show/check`, the "CI evaluates every declared output", and the flake.lock regression procedure.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:1317:      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Update Nix documentation after deleting the flake**\n\nThis deletion leaves the public Nix documentation unusable: `docs/plans/nix-first-architecture.md:53-79` still presents activation and evaluation commands for the removed `.#mryfmo-linux`, `.#mryfmo-darwin`, and `.#mryfmo-mac` outputs, while `docs/plans/nix-migration.md:21-37` calls the scaffold an initial implementation. Those commands now fail because neither `flake.nix` nor its outputs exist; retire or update these pages in the same change so users are not directed to a nonexistent setup path.\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.",
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:1321:      "disposition": "not-applicable:nix plan documents (docs/plans/nix-*.md, plans/004) are prose owned by the documentation tasks T78/T83; the stale lines are enumerated in the T74 report and this PR removes the flake, its CI job and its test"
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:1356:      "body": "Disposition (orchestrator acceptance): not-applicable for this PR. `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` and `plans/004-harden-and-lock-the-supply-chain.md` are plan prose that the dead-code task was forbidden to edit; the stale sentences are enumerated line by line in the T74 report and are rewritten by the documentation tasks dotfiles-T78/T83, which own those files. The code, CI job and test that made the flake live are all removed here.",
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:1445:## flake / should_nix / nix/ -> test.yaml:21,80-84,415-437; test_supply_chain_policy.py:461-477; flake.nix; nix/**; prose in docs/plans/nix-*.md and plans/004-*.md (not edited)
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:1589:5. **Nix:** delete `flake.nix`, `flake.lock`, `nix/**`. In `.github/workflows/test.yaml` delete the `should_nix` output (line 21), its filter block (80-84) and the `nix` job (415-437). In `tests/unit/test_supply_chain_policy.py` delete `test_nix_inputs_lock_and_ci_use_2605` (460-473) and any now-unused import. `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` and `plans/004-harden-and-lock-the-supply-chain.md` mention nix: do not edit them (T78/T83 own prose); list the stale sentences in the report.
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-audit-c0ea3e7f.md:2493:      "disposition": "not-applicable:nix plan documents (docs/plans/nix-*.md, plans/004) are prose owned by the documentation tasks T78/T83; the stale lines are enumerated in the T74 report and this PR removes the flake, its CI job and its test"
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-pr-feedback.json:140:      "body": "**<sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub>  Update Nix documentation after deleting the flake**\n\nThis deletion leaves the public Nix documentation unusable: `docs/plans/nix-first-architecture.md:53-79` still presents activation and evaluation commands for the removed `.#mryfmo-linux`, `.#mryfmo-darwin`, and `.#mryfmo-mac` outputs, while `docs/plans/nix-migration.md:21-37` calls the scaffold an initial implementation. Those commands now fail because neither `flake.nix` nor its outputs exist; retire or update these pages in the same change so users are not directed to a nonexistent setup path.\n\nUseful? React with \ud83d\udc4d\u00a0/ \ud83d\udc4e.",
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-pr-feedback.json:144:      "disposition": "not-applicable:nix plan documents (docs/plans/nix-*.md, plans/004) are prose owned by the documentation tasks T78/T83; the stale lines are enumerated in the T74 report and this PR removes the flake, its CI job and its test"
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01-pr-feedback.json:179:      "body": "Disposition (orchestrator acceptance): not-applicable for this PR. `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md` and `plans/004-harden-and-lock-the-supply-chain.md` are plan prose that the dead-code task was forbidden to edit; the stale sentences are enumerated line by line in the T74 report and are rewritten by the documentation tasks dotfiles-T78/T83, which own those files. The code, CI job and test that made the flake live are all removed here.",
.orchestration/validation/dotfiles-T74-bootstrap-dead-code-a01.md:18:## flake / should_nix / nix/ -> test.yaml:21,80-84,415-437; test_supply_chain_policy.py:461-477; flake.nix; nix/**; prose in docs/plans/nix-*.md and plans/004-*.md (not edited)
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:613:6. Stale nix prose from T74 (`docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md`): add one dated note at the top of each saying the flake was removed in #247 and the commands below no longer apply; do not rewrite the bodies (T83 decides their fate).
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:626:- `AGENTS.md`, `reviews/**` (delete), `.coderabbit.yaml`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (the four lines named), `home/dot_config/codex/AGENTS.md` (line 9), `.github/copilot-instructions.md` (delete), `home/dot_claude/commands/commit.md`, `plans/README.md`, `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md` (one note each), `tests/unit/test_agmsg_orchestration_docs.py` (only if it pins the deleted phrases)
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:686:   - `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` each get a dated note under the title: the flake was removed in #247, and the commands and paths below no longer apply;
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:732: docs/plans/nix-first-architecture.md               |   3 +
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:733: docs/plans/nix-migration.md                        |   3 +
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:772:$ mise x node npm:prettier -- prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/codex/AGENTS.md docs/plans/nix-first-architecture.md docs/plans/nix-migration.md; echo "rc=$?"
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:1240:6. Stale nix prose from T74 (`docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md`): add one dated note at the top of each saying the flake was removed in #247 and the commands below no longer apply; do not rewrite the bodies (T83 decides their fate).
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:1253:- `AGENTS.md`, `reviews/**` (delete), `.coderabbit.yaml`, `home/dot_agents/skills/agmsg-orchestration/SKILL.md` (the four lines named), `home/dot_config/codex/AGENTS.md` (line 9), `.github/copilot-instructions.md` (delete), `home/dot_claude/commands/commit.md`, `plans/README.md`, `docs/plans/nix-first-architecture.md`, `docs/plans/nix-migration.md`, `plans/004-harden-and-lock-the-supply-chain.md` (one note each), `tests/unit/test_agmsg_orchestration_docs.py` (only if it pins the deleted phrases)
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:1504:diff --git a/docs/plans/nix-first-architecture.md b/docs/plans/nix-first-architecture.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:1506:--- a/docs/plans/nix-first-architecture.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:1507:+++ b/docs/plans/nix-first-architecture.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:1517:diff --git a/docs/plans/nix-migration.md b/docs/plans/nix-migration.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:1519:--- a/docs/plans/nix-migration.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:1520:+++ b/docs/plans/nix-migration.md
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:2577:{"filePath": "docs/plans/nix-first-architecture.md", "summary": "Architecture plan for an optional Nix layer: chezmoi stays authoritative, initial Nix scope and package ownership, future Nix-first target, activation examples, and non-goals."}
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:2578:{"filePath": "docs/plans/nix-migration.md", "summary": "Phased Nix migration plan (opt-in scaffold, package-only adoption, host roles, selective config migration, optional Nix-first bootstrap) with principles and rollback notes."}
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:2647:    71	$ mise x node npm:prettier -- prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/codex/AGENTS.md docs/plans/nix-first-architecture.md docs/plans/nix-migration.md; echo "rc=$?"
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:2743:    27	   - `docs/plans/nix-first-architecture.md` and `docs/plans/nix-migration.md` each get a dated note under the title: the flake was removed in #247, and the commands and paths below no longer apply;
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01-audit-8d536a3.md:3000:/usr/bin/zsh -lc "python3 -B -c 'import subprocess,json; from pathlib import Path; base=\"6534df0f769fe5c12aa6e26e5355651e7a45f636\"; head=\"8d536a38\"; git=lambda *a: subprocess.check_output([\"git\",*a],text=True); rows=[x.split(\"\\t\") for x in git(\"diff\",\"--name-status\",base,head).splitlines()]; allowed={\"AGENTS.md\",\".coderabbit.yaml\",\".prettierignore\",\".github/copilot-instructions.md\",\"home/dot_agents/skills/agmsg-orchestration/SKILL.md\",\"home/dot_config/codex/AGENTS.md\",\"home/dot_claude/commands/commit.md\",\"plans/README.md\",\"docs/plans/nix-first-architecture.md\",\"docs/plans/nix-migration.md\",\"plans/004-harden-and-lock-the-supply-chain.md\",\"tests/unit/test_agmsg_orchestration_docs.py\"}; assert all(p in allowed or (s==\"D\" and p.startswith(\"reviews/ADH_Integrated_Plan/\")) for s,p in rows); deleted=[p for s,p in rows if p.startswith(\"reviews/\")]; assert len(deleted)==198; assert not git(\"ls-tree\",\"-r\",\"--name-only\",head,\"reviews\"); assert not git(\"status\",\"--porcelain\"); print(\"Allowed paths: 209/209; baseline deletions: 198/198; audited tree clean\"); plans=[\"docs/plans/nix-first-architecture.md\",\"docs/plans/nix-migration.md\",\"plans/004-harden-and-lock-the-supply-chain.md\"]; [(lambda old,new: (None if new[:2]+new[5:]==old else (_ for _ in ()).throw(AssertionError(p))))(git(\"show\",base+\":\"+p).splitlines(),git(\"show\",head+\":\"+p).splitlines()) for p in plans]; print(\"All three Nix plan bodies unchanged apart from three inserted note lines\"); print(\"Commit reference exists:\",Path(\"home/dot_agents/skills/gh-first-workflow/references/gh-git-rules.md\").is_file())'
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01.md:31: docs/plans/nix-first-architecture.md               |   3 +
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01.md:32: docs/plans/nix-migration.md                        |   3 +
.orchestration/validation/dotfiles-T78-dead-docs-adh-a01.md:71:$ mise x node npm:prettier -- prettier --check home/dot_agents/skills/agmsg-orchestration/SKILL.md home/dot_config/codex/AGENTS.md docs/plans/nix-first-architecture.md docs/plans/nix-migration.md; echo "rc=$?"
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-7ee9108.md:1919:docs/plans/nix-first-architecture.md
.orchestration/validation/dotfiles-T82-codex-compaction-hooks-a01-audit-7ee9108.md:1920:docs/plans/nix-migration.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md:6979:docs/plans/nix-first-architecture.md
.orchestration/validation/dotfiles-T90-github-identity-separation-a01-audit-e2d5c9a.md:6980:docs/plans/nix-migration.md
.ua/fingerprints.json:2419:    "docs/plans/nix-first-architecture.md": {
.ua/fingerprints.json:2420:      "filePath": "docs/plans/nix-first-architecture.md",
.ua/fingerprints.json:2429:    "docs/plans/nix-migration.md": {
.ua/fingerprints.json:2430:      "filePath": "docs/plans/nix-migration.md",
.ua/knowledge-graph.json:7375:      "id": "document:docs/plans/nix-first-architecture.md",
.ua/knowledge-graph.json:7378:      "filePath": "docs/plans/nix-first-architecture.md",
.ua/knowledge-graph.json:7389:      "id": "document:docs/plans/nix-migration.md",
.ua/knowledge-graph.json:7392:      "filePath": "docs/plans/nix-migration.md",
.ua/knowledge-graph.json:21794:      "target": "document:docs/plans/nix-first-architecture.md",
.ua/knowledge-graph.json:24579:      "source": "document:docs/plans/nix-first-architecture.md",
.ua/knowledge-graph.json:24586:      "source": "document:docs/plans/nix-migration.md",
.ua/knowledge-graph.json:24593:      "source": "document:docs/plans/nix-migration.md",
.ua/knowledge-graph.json:24600:      "source": "document:docs/plans/nix-migration.md",
.ua/knowledge-graph.json:24607:      "source": "document:docs/plans/nix-migration.md",
.ua/knowledge-graph.json:24614:      "source": "document:docs/plans/nix-first-architecture.md",
.ua/knowledge-graph.json:24615:      "target": "document:docs/plans/nix-migration.md",
.ua/knowledge-graph.json:24747:      "source": "document:docs/plans/nix-migration.md",
.ua/knowledge-graph.json:24748:      "target": "document:docs/plans/nix-first-architecture.md",
.ua/knowledge-graph.json:30502:        "document:docs/plans/nix-first-architecture.md",
.ua/knowledge-graph.json:30503:        "document:docs/plans/nix-migration.md",
rc=0
exit_code=0
```

## 2026-10-05T06:12:39.496311+00:00
```text
$ git grep -n 'docs/plans/nix' -- ':!.orchestration' ':!.ua'; echo "rc=$?"
rc=1
exit_code=0
```

## 2026-10-05T06:12:39.503927+00:00
```text
$ uv run --no-project python -m unittest tests.unit.test_aws_cli_acquisition 2>&1 | tail -3
Ran 10 tests in 0.168s

OK
exit_code=0
```

## Independent review gate
```text
$ AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-review-receipt.md make require-crit-review
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit_code=0
```

```text
$ git commit -m "docs: archive historical Nix plans"
[docs/nix-plans-history 43eeb915] docs: archive historical Nix plans
 5 files changed, 11 insertions(+), 3 deletions(-)
 create mode 100644 docs/history/README.md
 rename docs/{plans => history}/nix-first-architecture.md (96%)
 rename docs/{plans => history}/nix-migration.md (96%)
exit_code=0
```

```text
$ ['git', 'push', 'origin', 'docs/nix-plans-history']
remote: 
remote: Create a pull request for 'docs/nix-plans-history' on GitHub by visiting:        
remote:      https://github.com/mryfmo/dotfiles/pull/new/docs/nix-plans-history        
remote: 
To github.com:mryfmo/dotfiles.git
 * [new branch]        docs/nix-plans-history -> docs/nix-plans-history
exit_code=0
```

```text
$ ['gh', 'pr', 'create', '--base', 'main', '--head', 'docs/nix-plans-history', '--title', 'docs: archive historical Nix plans', '--body-file', '/tmp/t99-pr-body.md']
https://github.com/mryfmo/dotfiles/pull/277
exit_code=0
```

## 2026-10-05T06:12:39.735818+00:00
```text
$ make unit-test 2>&1 | tail -3
Ran 865 tests in 218.600s

OK
exit_code=0
```

## 2026-10-05T06:16:18.468331+00:00
```text
$ uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
agent asset validation ok
rc=0
Installed 1 package in 3ms
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/acceptance/dotfiles-T83-docs-diet-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T83-docs-diet-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/autoskill/runs/dotfiles-T98-evidence-home-path-masking-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T83-docs-diet-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/learning/dotfiles-T98-evidence-home-path-masking-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T83-docs-diet-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/reports/dotfiles-T98-evidence-home-path-masking-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T83-docs-diet-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/sandboxes/dotfiles-T98-evidence-home-path-masking-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T98-evidence-home-path-masking-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/tasks/dotfiles-T99-nix-plans-history-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-a536af5.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-a536af5.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-b9acaa3.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-audit-b9acaa3.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T81b-compactiondb-vendor-hygiene-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T83-docs-diet-a01-audit-914c765.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T83-docs-diet-a01-audit-914c765.md.last.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T83-docs-diet-a01-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T83-docs-diet-a01-pr-feedback.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T83-docs-diet-a01-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles: .orchestration/validation/dotfiles-T83-docs-diet-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/autoskill/runs/dotfiles-T99-nix-plans-history-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/learning/dotfiles-T99-nix-plans-history-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/reports/dotfiles-T99-nix-plans-history-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/sandboxes/dotfiles-T99-nix-plans-history-a01.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-crit.json
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-review-receipt.md
WARN: regime-boundary: untracked .orchestration file in ~/Workspace/dotfiles/.claude/worktrees/worker-e: .orchestration/validation/dotfiles-T99-nix-plans-history-a01.md
WARN: regime-boundary: additional worker workspace still open: dotfiles worker worker-d (herdr-agents --remove-worker)
WARN: regime-boundary: additional worker tab still open in dotfiles: dotfiles:codex-security-dot-a007 (herdr-agents --remove-worker)
exit_code=0
```

## 2026-10-05T06:16:33.153873+00:00
```text
$ mise x node npm:prettier -- --check docs/history README.md 2>&1 | tail -3
mise ERROR "--check" couldn't exec process: No such file or directory
mise ERROR Version: 2026.10.1 linux-arm64 (2026-10-03)
mise ERROR Run with --verbose or MISE_VERBOSE=1 for more information
exit_code=1
```

## 2026-10-05T06:16:33.174465+00:00
```text
$ mise x node npm:prettier -- prettier --check docs/history README.md 2>&1 | tail -3
Checking formatting...
All matched files use Prettier code style!
exit_code=0
```

## 2026-10-05T06:16:33.425717+00:00
```text
$ cat mkdocs.yml .github/workflows/docs.yml
site_name: Dotfiles Docs
site_description: Generated reference for shell-based dotfiles automation.
docs_dir: docs
site_dir: site

theme:
  name: material
  features:
    - navigation.top
    - content.code.copy

plugins:
  - search
  - toc-md:
      output_path: catalog.md
      ignore_page_pattern: 'index.*\.md$|catalog.*\.md$'

extra_css:
  - assets/stylesheets/extra.css

markdown_extensions:
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true
  - pymdownx.highlight
  - pymdownx.superfences
name: Docs

on:
  workflow_dispatch:
  push:
    branches: [main]
    paths:
      - ".github/workflows/docs.yml"
      - "Makefile"
      - "README.md"
      - "mkdocs.yml"
      - "scripts/**"
      - "install/**"
      - "home/.chezmoiscripts/**"
      - "home/dot_claude/hooks/**"
      - "home/dot_config/alias/**"
      - "home/dot_local/bin/**"

concurrency:
  group: docs-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-24.04

    steps:
      - name: Configure Git defaults
        run: git config --global init.defaultBranch main

      - name: Checkout repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
        with:
          fetch-depth: 0

      - name: Setup uv
        uses: astral-sh/setup-uv@c18668ad3cf93ea998bef934396af7bb5c839dc7 # v10.2.0
        with:
          enable-cache: false

      - name: Pin mise from install/common/mise.sh
        run: |
          # MISE_VERSION renders from assets.mise in agent-config.yaml; the
          # variable stays outside MISE_*, which mise reads as its own settings.
          pin="$(sed -n 's/^readonly MISE_VERSION="v\(.*\)"$/\1/p' install/common/mise.sh)"
          test -n "${pin}"
          echo "DOTFILES_MISE_VERSION=${pin}" >> "${GITHUB_ENV}"

      - name: Setup mise
        uses: jdx/mise-action@c2a87611a18de5b3828c5652fe268e992400cb5c # v4
        with:
          version: ${{ env.DOTFILES_MISE_VERSION }}
          install: false
          cache: true

      - name: Trust mise config
        run: mise trust --yes

      - name: Install mise tools
        run: mise install

      - name: Configure git author
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

      - name: Deploy docs
        run: make deploy
exit_code=0
```

## 2026-10-05T06:16:33.428628+00:00
```text
$ git diff --check
exit_code=0
```

## 2026-10-05T06:16:33.432415+00:00
```text
$ make require-crit-review
Native agent review required before completion.
- review-sensitive path changed: .orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-crit.json
- broad diff touches 7 files
- broad diff changes 595 lines
Use the active agent's review path, not a browser by default:
- Codex: retrieve Crit comments/status data, review it inside the task, then address findings.
- Claude Code: retrieve Crit comments/status data, review it inside the task, then address findings.
- Use browser Crit review only when the user explicitly asks for Crit web UI or Crit data is unavailable.
Record a receipt with `review_surface:`, `reviewer:`, and `review_outcome:`.
For agent judgment, locate the review with `crit status --json`, then save `crit comments --all --json <review.json>` to a repo-local JSON file.
Evidence must contain at least one resolved record; for a finding-free review, add and resolve one review-scope approval record.
This local evidence is process evidence, not reviewer authentication.
Then use `review_surface: crit-data`, `reviewer: codex` or `reviewer: claude-code`, and `review_source: <json path>`.
After addressing review feedback, rerun with AGENT_REVIEWED=1 or CRIT_REVIEWED=1 plus REVIEW_EVIDENCE=<path>.
make: *** [Makefile:179: require-crit-review] Error 1
exit_code=2
```

## 2026-10-05T06:16:33.486740+00:00
```text
$ crit status --json
{
  "branch": "docs/nix-plans-history",
  "daemon": {
    "running": false
  },
  "review_file": "~/.crit/reviews/de6bf519ecac/review.json",
  "review_file_exists": false,
  "sessions": [],
  "vcs": "git"
}
exit_code=0
```

## Progress dispatch
```json
{
  "argv": [
    "agmsg-dispatch",
    "dotfiles",
    "codex-security-dot-a007",
    "claude-remediation-dot",
    "wT:p1",
    "AGMSG-PONG v1 task_id=dotfiles-T99 status=active pr=277 head=43eeb915 local=10-focused+865-unit-PASS assets=PASS review=approved CI=pending;task-prettier-command-missing-executable-corrected-prettier-command-PASS;only-old-path-refs-archived-.orchestration-and-.ua"
  ],
  "start": "2026-10-05T06:17:20.497871+00:00",
  "end": "2026-10-05T06:17:30.797999+00:00",
  "returncode": 0,
  "stdout": "",
  "stderr": ""
}
```

## CI 2026-10-05T06:16:13.916844+00:00
```text
$ gh pr checks 277 --watch
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

changes	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
private-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
changes	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
validate	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
changes	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

changes	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

changes	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

public-bootstrap (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, server)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
test (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
public-bootstrap (ubuntu-24.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
test (ubuntu-26.04, client)	pending	0	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
test (ubuntu-26.04, client)	pass	7m50s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
test (ubuntu-26.04, client)	pass	7m50s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
exit_code=0
```

## Final diff-head Bot wait
Started 2026-10-05T06:25:50.985549+00:00; head 43eeb9153f54de4a03614b7edb4c6b606f312509.
```json
[
  {
    "at": "2026-10-05T06:25:51.635431+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:25:51.979483+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:26:22.388353+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:26:22.749670+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```

## CI/Bot progress dispatch
```json
{
  "argv": [
    "agmsg-dispatch",
    "dotfiles",
    "codex-security-dot-a007",
    "claude-remediation-dot",
    "wT:p1",
    "AGMSG-PONG v1 task_id=dotfiles-T99 status=active pr=277 head=43eeb915 CI=all-green bot-wait-start=2026-10-05T06:25:51Z bot-wait-deadline=2026-10-05T06:40:52Z final-head-review-or-comment=none-yet"
  ],
  "start": "2026-10-05T06:26:17.012711+00:00",
  "end": "2026-10-05T06:26:27.305311+00:00",
  "returncode": 0,
  "stdout": "",
  "stderr": ""
}
```
```json
[
  {
    "at": "2026-10-05T06:26:53.163229+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:26:53.522626+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:27:23.945406+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:27:24.282316+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:27:54.739891+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:27:55.080814+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:28:25.514609+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:28:25.916361+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:28:56.455985+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:28:56.787077+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:29:28.241103+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:29:28.618784+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:29:59.057678+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:29:59.402458+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:30:29.802784+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:30:30.194434+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:31:00.640903+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:31:01.077876+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:31:31.528539+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:31:31.879784+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:32:02.323922+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:32:02.695060+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:32:33.120296+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:32:33.469783+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:33:03.894104+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:33:04.266898+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:33:34.708479+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:33:35.090652+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:34:05.518198+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:34:05.879674+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:34:36.305418+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:34:36.681776+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:35:07.118865+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:35:07.472057+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:35:37.922551+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:35:38.261426+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:36:08.788093+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:36:09.228283+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:36:39.648392+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:36:39.989893+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:37:10.486878+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:37:10.828824+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:37:41.265872+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:37:41.624043+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:38:12.086450+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:38:12.451448+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:38:42.892215+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:38:43.244554+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:39:13.701224+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:39:14.102290+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:39:44.519756+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:39:44.875230+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:40:15.345942+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:40:15.700454+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:40:46.142316+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:40:46.528312+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
[
  {
    "at": "2026-10-05T06:41:17.165544+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/reviews",
      "--jq",
      ".[]|select(.user.type==\"Bot\" and .commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.commit_id,.submitted_at]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "at": "2026-10-05T06:41:17.605161+00:00",
    "argv": [
      "gh",
      "api",
      "--paginate",
      "repos/mryfmo/dotfiles/pulls/277/comments",
      "--jq",
      ".[]|select(.in_reply_to_id == null and .user.type==\"Bot\" and .original_commit_id==\"43eeb9153f54de4a03614b7edb4c6b606f312509\")|[.id,.original_commit_id,.path,.body]|@tsv"
    ],
    "returncode": 0,
    "stdout": "",
    "stderr": ""
  }
]
```
```json
{
  "start": "2026-10-05T06:25:50.985549+00:00",
  "end": "2026-10-05T06:41:17.605289+00:00",
  "elapsed_seconds": 926.62,
  "head": "43eeb9153f54de4a03614b7edb4c6b606f312509",
  "bot": "none"
}
```

## Final check 2026-10-05T06:41:28.244484+00:00
```text
$ git fetch origin
exit_code=0
```

## Final check 2026-10-05T06:41:28.246480+00:00
```text
$ git rev-parse HEAD origin/main
43eeb9153f54de4a03614b7edb4c6b606f312509
794a80dbf74ec62399edc2a8a03e102f68049bb6
exit_code=0
```

## Final check 2026-10-05T06:41:28.250557+00:00
```text
$ git rev-list --left-right --count origin/main...HEAD
0	1
exit_code=0
```

## Final check 2026-10-05T06:41:28.256493+00:00
```text
$ git diff origin/main --stat | tail -5
 docs/{plans => history}/nix-first-architecture.md | 2 ++
 docs/{plans => history}/nix-migration.md          | 2 ++
 plans/004-harden-and-lock-the-supply-chain.md     | 2 +-
 tests/unit/test_aws_cli_acquisition.py            | 4 ++--
 5 files changed, 11 insertions(+), 3 deletions(-)
exit_code=0
```

## Final check 2026-10-05T06:41:28.260212+00:00
```text
$ git ls-files docs/plans docs/history
docs/history/README.md
docs/history/nix-first-architecture.md
docs/history/nix-migration.md
exit_code=0
```

## Final check 2026-10-05T06:41:29.516049+00:00
```text
$ gh pr checks 277
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
changes	pass	18s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639452509	
private-bootstrap (macos-14, client)	pass	9s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452577	
private-bootstrap (ubuntu-24.04, client)	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452465	
private-bootstrap (ubuntu-24.04, server)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452586	
public-bootstrap (macos-14, client)	pass	6m35s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452599	
public-bootstrap (ubuntu-24.04, client)	pass	8m30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452588	
public-bootstrap (ubuntu-24.04, server)	pass	7m36s	https://github.com/mryfmo/dotfiles/actions/runs/37271558495/job/111639452582	
test (macos-14, client)	pass	6m28s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691324	
test (ubuntu-24.04, client)	pass	7m14s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691382	
test (ubuntu-24.04, server)	pass	5m34s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691406	
test (ubuntu-26.04, client)	pass	7m50s	https://github.com/mryfmo/dotfiles/actions/runs/37271558517/job/111639691338	
validate	pass	30s	https://github.com/mryfmo/dotfiles/actions/runs/37271558555/job/111639452579	
exit_code=0
```

## Final check 2026-10-05T06:41:30.286021+00:00
```text
$ gh api repos/mryfmo/dotfiles/pulls/277 --jq '.mergeable_state' 
clean
exit_code=0
```

## Final check 2026-10-05T06:41:30.692649+00:00
```text
$ gh api graphql -f query='{repository(owner:"mryfmo",name:"dotfiles"){pullRequest(number:277){reviewThreads(first:100){nodes{id isResolved comments(first:100){nodes{body path line originalCommit{oid}}}}}}}' 
{"errors":[{"message":"Expected NAME, actual: (none) (\"\") at [1, 179]","locations":[{"line":1,"column":179}]}]}gh: Expected NAME, actual: (none) ("") at [1, 179]
exit_code=1
```

## Final check (GraphQL syntax corrected where applicable)
```text
$ ['gh', 'api', 'graphql', '-f', 'query=query {\n repository(owner: "mryfmo", name: "dotfiles") {\n  pullRequest(number: 277) {\n   reviewThreads(first: 100) { nodes { id isResolved } pageInfo { hasNextPage } }\n  }\n }\n}']
{"data":{"repository":{"pullRequest":{"reviewThreads":{"nodes":[],"pageInfo":{"hasNextPage":false}}}}}}exit_code=0
```

## Final check (GraphQL syntax corrected where applicable)
```text
$ ['git', 'status', '--short']
?? .orchestration/autoskill/runs/dotfiles-T99-nix-plans-history-a01.md
?? .orchestration/learning/dotfiles-T99-nix-plans-history-a01.md
?? .orchestration/reports/dotfiles-T99-nix-plans-history-a01.md
?? .orchestration/sandboxes/dotfiles-T99-nix-plans-history-a01.md
?? .orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-crit.json
?? .orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-review-receipt.md
?? .orchestration/validation/dotfiles-T99-nix-plans-history-a01.md
exit_code=0
```

## Final check (GraphQL syntax corrected where applicable)
```text
$ ['bash', '-c', 'AGENT_REVIEWED=1 REVIEW_EVIDENCE=.orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-review-receipt.md make require-crit-review']
Review requirement satisfied by AGENT_REVIEWED=1 with REVIEW_EVIDENCE.
exit_code=0
```

## Final check (GraphQL syntax corrected where applicable)
```text
$ ['bash', '~/.agents/skills/agmsg/scripts/inbox.sh', 'dotfiles', 'codex-security-dot-a007']
No new messages.
exit_code=0
```

## RESULT dispatch receipt
```json
{
  "argv": [
    "agmsg-dispatch",
    "dotfiles",
    "codex-security-dot-a007",
    "claude-remediation-dot",
    "wT:p1",
    "AGMSG-RESULT v1 task_id=dotfiles-T99 status=done pr=277 head=43eeb9153f54de4a03614b7edb4c6b606f312509 branch=docs/nix-plans-history CI=green bot=none bot-wait=2026-10-05T06:25:50Z..06:41:17Z unresolved_threads=none mergeable=clean artifacts=worker-e-untracked report=.orchestration/reports/dotfiles-T99-nix-plans-history-a01.md validation=.orchestration/validation/dotfiles-T99-nix-plans-history-a01.md sandbox=.orchestration/sandboxes/dotfiles-T99-nix-plans-history-a01.md learning=.orchestration/learning/dotfiles-T99-nix-plans-history-a01.md autoskill=.orchestration/autoskill/runs/dotfiles-T99-nix-plans-history-a01.md review=.orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-crit.json receipt=.orchestration/validation/dotfiles-T99-nix-plans-history-a01-worker-review-receipt.md memory=orchestrator-records cost:n/a"
  ],
  "start": "2026-10-05T06:42:25.499990+00:00",
  "end": "2026-10-05T06:42:30.797969+00:00",
  "returncode": 0,
  "stdout": "",
  "stderr": ""
}
```
