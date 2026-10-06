# AGMSG-TASK dotfiles-T108-one-login-per-machine-a01

Drafted 2026-10-06 by the orchestrator seat from the operator's decision A (`.orchestration/validation/github-auth-design-2026-10-05.md` §16). Supersedes T107 (cancelled; PR #292 closed unmerged). Kind: launcher (`herdr-agents`), gate (`require-crit-review.py`), doctor, check-tools, renderer (model-profiles.env part), manifest keys, `scripts/gh-auth-stores.sh`, Makefile, `setup.sh`, Codex execpolicy (`home/dot_codex/rules/default.rules`, Codex's boundary → Claude seat allowed), README, tests. Not touched: Claude permission/sandbox/hook blocks, permgate. Dispatched to `claude-standard-dot-a005` (worker-c, wT:p2).

## Objective: one GitHub login per machine, every seat acts as it

1. **herdr-agents**: remove the worker GitHub config selection (`worker_github_config_dir`, `worker_github_shell_env`, `codex_worker_github_config`, `spawn_worker_with_github`'s GH_CONFIG_DIR/GH_TOKEN environment, the `shell_environment_policy.set.GH_CONFIG_DIR` override, `notice_missing_worker_github_credential` and its call sites). Worker panes inherit the user's gh configuration like any shell. Tests follow (the T90 and T102 tests are deleted or inverted: no `GH_CONFIG_DIR` in a worker pane's environment).
2. **Gate** `scripts/require-crit-review.py`: remove the GitHub role gate (worker hosts.yml probe, ruleset approval/bypass checks, author≠merger and approval requirements, their notices). Everything else (PR feedback evidence, audit evidence and dispositions, crit evidence) is unchanged. Tests follow.
3. **Manifest and renderer**: remove `owner_gh_config_dir`, `work_gh_config_dir`, `worker_gh_config_dir` and the `*_GH_CONFIG_DIR` rendering; `make render-check` clean.
4. **Login step**: `scripts/gh-auth-stores.sh` becomes the single-store form (gh's default directory): `gh auth status` → skip, else `gh auth login --hostname github.com --git-protocol https` (default storage, no `--insecure-storage`: the OS keyring where present, gh's own plain-text fallback otherwise), tty-only, token env cleared first, no `setup-git`. Keep `make gh-auth` and the `setup.sh` step (mise shims on PATH). Rename the script if you wish (`gh-auth.sh`); update the Makefile target and `setup.sh`.
5. **Doctor and check-tools**: replace the three-store findings with one: the default store holds exactly one working login (`found:` with the login name) or a WARN with the `make gh-auth` hint; remove `check_github_identities` (two-login comparison) from `check-tools.sh`.
6. **Codex execpolicy** `home/dot_codex/rules/default.rules`: keep `gh pr merge` forbidden; add forbidden prefix rules for `gh api -X PUT`, `gh api --method PUT`, `gh api graphql` with the justification "merging and auto-merge are the orchestrator's acceptance step"; `match`/`not_match` examples (`gh api repos/o/r/pulls/1/reviews` stays allowed).
7. **README**: the GitHub roles / operator-phase section says: every seat on a machine acts as that machine's GitHub account (one `gh auth login`, `make gh-auth` when empty, `make update` never prompts); what protects `main` under one account (PR-only, required checks, conversation resolution, linear history, force-push and deletion blocks; native denial of merge commands in worker seats; the integration gate); that required approvals and bypass actors are not used; delete the three-store table, the `encrypted_private_hosts.yml` sentence, the T90 account-separation text and the ruleset PUT/approval instructions that depend on two accounts. Keep it short; the design report holds the reasoning.
8. **Tests**: everything above; `make unit-test`, validator rc=0, `bash -n`/shellcheck on the shell files, prettier on README. Docs parity tests that pin removed sentences follow.

Forbidden: Claude `permissions`/`sandbox`/`hooks` blocks and their rendered files, `modify_private_settings.json`, permgate; `make update`/`apply`; thread resolution; local bats; printing any credential.

[memory:decision] dotfiles-T108 (operator 2026-10-06, decision A): every seat on a machine acts as that machine's single GitHub account; the T90/T102/T103 role separation is removed; `main` is protected by actor-independent rulesets, native denial of merge commands in worker seats, and the integration gate.

## Repo / branch

worker-c; discard the T107 branch first (`git switch --detach origin/main`, `git branch -D fix/gh-stores-per-machine`, drop its uncommitted edits); `git fetch origin`; `git switch -c feat/one-login-per-machine --no-track origin/main` (main at e0027811 or later); verify task_rev against the main checkout's task file.

## Allowed files

`home/dot_local/bin/common/executable_herdr-agents`, `scripts/require-crit-review.py`, `scripts/generate-agent-configs.py`, `home/dot_agents/agent-config.yaml` (the gh store keys only), `home/dot_agents/model-profiles.env` (rendered), `scripts/gh-auth-stores.sh` (or its rename), `Makefile` (the `gh-auth` target), `setup.sh` (`authenticate_github`), `scripts/check-agent-runtime.py`, `scripts/check-tools.sh`, `home/dot_codex/rules/default.rules`, `README.md`, `tests/**`. Artifacts at the standard seven `dotfiles-T108-one-login-per-machine-a01` paths in the main checkout (Claude seat, through the permission gate), masked.

## Validation commands (paste verbatim output, whole)

```
grep -rn 'GH_CONFIG_DIR\|gh-worker\|gh-work\b\|worker_gh_config_dir\|owner_gh_config_dir\|role gate\|encrypted_private_hosts' home scripts setup.sh Makefile README.md tests; echo "rc=$? (expect no match except README prose explaining what was removed, if any)"
bash -n setup.sh scripts/*.sh home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
shellcheck setup.sh scripts/gh-auth*.sh scripts/check-tools.sh home/dot_local/bin/common/executable_herdr-agents; echo "rc=$?"
make render-check
make unit-test 2>&1 | tail -3
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
mise x node npm:prettier -- prettier --check README.md 2>&1 | tail -2
gh pr checks <pr>
```

## Completion

PR to `main` (English, attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of the decision line in the main checkout, `AGMSG-RESULT v1 task_id=dotfiles-T108` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"`. max_turns=25.

### PONG decision 1 (orchestrator, 2026-10-06 04:05Z) — option (a): the SKILL, the rule and the docs test join the allowed files

Add `home/dot_agents/skills/agmsg-orchestration/SKILL.md`, `home/dot_config/claude/rules/agmsg-orchestration.md` and `tests/unit/test_agmsg_orchestration_docs.py` to the allowed files for the two-account passages only: SKILL step 10/10.5 merge procedure becomes `gh pr merge --squash` (the REST `PUT …/merge` path existed only to merge without self-approval under a required-approval rule, which decision A drops); the Worker Playbook sentence about `WORKER_GH_CONFIG_DIR`/hosts.yml and "approval from another login" goes; the README "GitHub role setup activation" reference goes; the rule's `main` bullet names `gh pr merge --squash` as the only merge procedure; the docs test's pinned tokens follow (remove the T90/T90b provisioning tokens, keep the invariants). The Codex execpolicy PUT/graphql ban binding a Codex orchestrator is accepted: `gh pr merge` is already forbidden for every Codex seat since T63, so a Codex orchestrator's merge path is a separate follow-up, not this task. Keep the SKILL/rule edits to those passages; the grep in the validation block is then expected to return no match.

## Revise round 1 (orchestrator, 2026-10-06 05:05Z) — audit of b66f4297: `incorrect` (1 P2, 1 P3)

1. **Head binding of the merge (P2, `SKILL.md:169`).** The REST path carried `sha=<head>`; its replacement `gh pr merge <pr> --squash` would merge a newer CI-green head on the evidence of the audited one. Write the merge procedure as `gh pr merge <pr> --squash --match-head-commit <audited head sha>` in SKILL step 10/10.5, the agmsg-orchestration rule bullet and the README's merge mention, and pin the `--match-head-commit` token in the docs test.
2. **Sandbox record (P3, `sandboxes/…:15`).** "No command ran gh against the real gh configuration" contradicts the recorded authenticated `gh pr create`, `gh pr checks` and API polling. Limit the statement to the fake-HOME tests, and say that credential *use* through gh is the normal path while no credential *value* was read or printed.

Then push, CI, Bot wait on the final head, `AGMSG-RESULT v1 … round=1`. No `make update`.
