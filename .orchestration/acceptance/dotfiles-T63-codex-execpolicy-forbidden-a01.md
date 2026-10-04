# Acceptance: dotfiles-T63-codex-execpolicy-forbidden-a01

- **Decision:** ACCEPTED after PONG decision 1 and two revise rounds. PR #235 squash-merged to `main` as `c6de5156` (final head `ddb7bf16785644e83a7f5cf49b93ea55846d6e73`, base `910ba6f5`). Merged without `--delete-branch` while worker-c holds `chore/codex-execpolicy-forbidden`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev `012c39f6…` → `28393b19…` (PONG 1) → `4258ed09…` (round 1) → `7f7a1751…` (round 2); all matched.
- **Exemption declared:** acceptance and final integration; the orchestrator mutated no repository code.
- **Plan reference:** correction plan Phase 1, dotfiles-T63 (principle 1: denial in the native layer, Codex side).

## What was accepted (3 files; 11 commits)

- `home/dot_codex/rules/default.rules` (new, plain chezmoi file → `~/.codex/rules/default.rules`): 19 `prefix_rule` entries, all `decision="forbidden"`, 0 allow rules, each with justification and load-time `match`/`not_match` examples. Forbidden: `sudo` (also `/usr/bin/sudo`, `/bin/sudo`, `/usr/local/bin/sudo`, `/run/wrappers/bin/sudo`); `rm` recursive+force in combined, split and separated `-v` orderings; `gh pr merge`; `gh release`; `npm publish`, `uv publish`; `terraform apply|destroy`; `kubectl apply|delete`; `chezmoi apply`, `chezmoi update`, all of `chezmoi init` and `chezmoi edit`; `make setup|init|update|apply|upgrade|watch|reset|reset-config|clean|deploy`; `./setup.sh`, `setup.sh`. Header: rewritten on every `chezmoi apply`; the 23 live allows are dropped deliberately; allow rules are not managed because an explicit allow lets a command run outside the sandbox (Codex `bypass_sandbox`); forbidden is a refusal under every approval policy and wins over allow; Codex reads rules at startup (restart after `make update`); prefix coverage limits (global-option-first forms, flags after operands, `make -C`, script-spawned commands) with the sandbox as backstop, for Codex and the Claude deny list alike; pipelines are covered by the Claude deny list.
- `README.md`: one paragraph in the Codex section stating the same.
- `tests/unit/test_codex_execpolicy.py` (new): parses the rules with `ast`, asserts forbidden-only with justifications and that `REQUIRED_PREFIXES` ⊆ covered prefixes.

## Orchestrator re-derivation

- `codex execpolicy check --rules <head file> --pretty` on 40+ commands across the rounds: every listed prefix returns `forbidden`; `rm -r x`, `gh pr view`, `gh pr create`, `terraform plan`, `kubectl get`, `chezmoi diff|status|managed`, `make unit-test|render-check|docs`, `git push origin b` return no match; the documented gaps (`rm build -rf`, `rm -r -fv x`, `terraform -chdir=x apply`) are unmatched as stated. (My first table showed no matches for everything because zsh does not word-split `$c`; `${=c}` fixed the harness, not the rules.)
- Header allow-rule sentence verified against the auditor's citation (`exec_policy.rs`, `Decision::Allow → ExecApprovalRequirement::Skip { bypass_sandbox }`).
- Every Bot and audit fix read in the diffs; `chezmoi diff` evidence in the validation file shows the 23 live allow lines replaced.

## Decisions during the task

- **PONG decision 1 (option c):** global options with arbitrary values before the subcommand cannot be prefix rules without forbidding whole tools machine-wide; documented as outside coverage, sandbox is the backstop; no tool-wide forbids for terraform/kubectl/chezmoi-read commands.
- **Scope extensions accepted** (all from Bot or audit findings fixed at the root): absolute sudo paths, split/separated rm forms, lifecycle make targets incl. `clean` and `deploy` (worker initiative; publish-class, force-pushes the docs site), `./setup.sh`, `chezmoi update`, `chezmoi init`/`edit` wholesale.
- **Revise round 2 stop rule:** stop enumerating flag spellings; forbid `chezmoi init`/`edit` wholesale (no agent use); further spellings of covered classes are `not-applicable` under the header coverage statement.
- **E2E `codex exec` refusal not demonstrated** (scratch project layer did not load for `codex exec`); accepted on the deterministic checker (same code path). Operator post-apply check: `codex execpolicy check --rules ~/.codex/rules/default.rules -- gh pr merge 1` → `forbidden`.

## Audit (per commit)

| commit | verdict | findings → disposition |
|---|---|---|
| a0b05905 | incorrect | rm forms → fixed:04d6e1f3/e16012eb; make/init → fixed:04d6e1f3/e16012eb/1f4f409a; global-option limit undocumented → fixed:7a7c21cd; README restart → fixed:04d6e1f3; allow-rule claim false → fixed:eb67299c |
| 04d6e1f3 | incorrect | make init/setup → fixed:e16012eb/1f4f409a |
| e16012eb | incorrect | make setup → fixed:1f4f409a; init aliases → superseded by c58e4835 (init forbidden wholesale) |
| 7a7c21cd, 1f4f409a, eb67299c | correct | — |
| 34e7423f | incorrect | --one-shot=true → fixed:8770ed66, superseded by c58e4835 |
| 8770ed66 | incorrect | edit --watch, boolean aliases → fixed:c58e4835 |
| c58e4835, 7e83ed9c, ddb7bf16 | correct | — (ddb7bf16 is the final head) |

## Codex Bot

- 17 inline threads over 7 reviewed heads: 14 fixed in-PR, 3 not-applicable (terraform `-chdir`, chezmoi `--source … apply`, grouped `rm -r -fv`) with reasons; all replied and resolved by the orchestrator; `mergeable_state` clean; the final head received the Bot's thumbs-up. Sweep (head ddb7bf16): 62 items, 0 failure/warning, all dispositioned.

## Gate

- `.claude/worktrees/orchestrator-review` at ddb7bf16 with evidence copies: `BASE=origin/main PR_FEEDBACK_EVIDENCE=… AGENT_REVIEWED=1 REVIEW_EVIDENCE=… make require-crit-review` exit 0. Copies removed.

## CompactionDB

- Worker decision `9ccb9164-013d-4f77-b034-407ad252d0d0` (original set). Amended at acceptance with the final set; see the acceptance-time `memory add` below.

## Operator follow-up

- `make update` on each clone deploys the rules file and (T61) the formatters; restart running Codex sessions afterwards (`herdr-agents --restart-worker` for the pair worker). Then `codex execpolicy check --rules ~/.codex/rules/default.rules -- gh pr merge 1` → `forbidden`.
- Lesson for the regime (codify in T69/T83): Bot reviews that enumerate spellings of a covered class are non-convergent; the coverage statement is the stop rule and the orchestrator decides when to invoke it.
