# AGMSG-TASK dotfiles-T63-codex-execpolicy-forbidden-a01

Drafted 2026-10-03 by the orchestrator seat from the approved correction plan (`.agents/worklog/claude/delegated-honking-frost.md`, Phase 1, dotfiles-T63). Worker: `claude-standard-dot-a005` in `~/Workspace/dotfiles/.claude/worktrees/worker-c`. Task ids now carry the team prefix (`dotfiles-T<n>`); `dot-` was the short form of the same series.

## Objective

Principle 1 of the target state: denial lives in the native layer. Codex today has no repository-managed execpolicy; the live `~/.codex/rules/default.rules` holds 23 `allow` prefix rules accumulated by past interactive sessions (`git push …`, `gh pr create …`, `gh run rerun`, `python3 /tmp/t40-*` wrappers) and nothing is ever forbidden. Create the chezmoi-managed rules file so that the forbidden set is declared once in the repository and overwrites the live file on every `chezmoi apply`.

1. New `home/dot_codex/rules/default.rules` (plain chezmoi file → `~/.codex/rules/default.rules`; `.gitignore:15` ignores only the repository-local `.codex/`, so this path is tracked). Content: only `prefix_rule(..., decision="forbidden")` entries for `sudo`, `rm -rf` (and `rm -fr`), `gh pr merge` (merging is the orchestrator's acceptance step), `gh release`, `npm publish`, `uv publish`, `terraform apply`, `kubectl apply`, `chezmoi apply`. No `allow` rules: the next task (T64) launches workers with `--ask-for-approval never`, under which nothing prompts and an allow rule buys nothing. Header comment (English): the file is rewritten on every `chezmoi apply`; an "always allow" that an interactive on-request session appends is reset at the next apply and shows up in `chezmoi diff`; the 23 accumulated allows are dropped deliberately; pipelines such as `curl … | sh` cannot be expressed as a prefix rule (the Claude deny list covers them), say so.
2. `README.md`: one paragraph near the Codex permission/sandbox section (around lines 600-625) stating that the execpolicy forbidden set is repository-managed, what it forbids, and that interactive "always allow" additions do not survive `chezmoi apply`.
3. Nothing else: no generator or manifest change (the file needs no rendering), no `approval_policy`/sandbox change, no edit of the live `~/.codex` (that is `make update`, operator lifecycle).

VERIFY (record in the validation file with the source): (a) the execpolicy rule syntax accepted by Codex 0.160.0 (`prefix_rule(pattern=[...], decision="forbidden")`) and where rules are loaded from (`~/.codex/rules/*.rules`); (b) `forbidden` wins when another rule allows the same prefix; (c) whether a `forbidden` match is reported to the model as a refusal (not a prompt) under `on-request` and under `never`.

[memory:decision] dotfiles-T63 (operator 2026-10-03): the Codex execpolicy forbidden set (sudo, rm -rf, gh pr merge, gh release, npm/uv publish, terraform/kubectl apply, chezmoi apply) is declared once in `home/dot_codex/rules/default.rules` and overwrites the live rules on every chezmoi apply; no repository-managed allow rules exist.

## Repo / branch

- Work ONLY in the worker-c worktree. `git fetch origin`; `git switch -c chore/codex-execpolicy-forbidden origin/main`. Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked.
- Strict status checks: if `main` moves, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_codex/rules/default.rules` (new)
- `README.md` (one paragraph in the Codex section)
- `tests/unit/test_codex_execpolicy.py` (new, optional: one test that parses the rules file and asserts every entry is `forbidden` and the listed prefixes are present) and any test that enumerates `home/dot_codex/**` files, if one exists (name it)
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dotfiles-T63-codex-execpolicy-forbidden-a01.md` (main checkout)

## Forbidden actions

- Any `allow` rule; changes to `agent-config.yaml`, generator, templates, profiles, `approval_policy`, sandbox settings, herdr-agents; editing `~/.codex/**`; `make update`/`make apply`; local bats; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git diff origin/main --stat
cat home/dot_codex/rules/default.rules
grep -c 'decision="forbidden"' home/dot_codex/rules/default.rules; grep -c 'decision="allow"' home/dot_codex/rules/default.rules   # expect N and 0
chezmoi diff --source "$PWD/home" --destination "$HOME" -- "$HOME/.codex/rules/default.rules" 2>&1 | head -60   # or an equivalent read-only diff that shows the managed content replacing the live file; do not apply
make unit-test
make validate-agent-assets
mise x node npm:prettier -- prettier --check README.md
# scratch VERIFY (read-only sandbox, scratch dir, never the live ~/.codex): a rules file with the same content loaded via -c or a scratch CODEX_HOME, then `codex exec --sandbox read-only 'run: gh pr merge 1'` → paste the refusal
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date.
2. After the final push: `gh pr checks <pr> --watch`; then wait (up to 15 min) until the Codex Bot has reviewed that head (a review with `commit_id == <head>` from a Bot user, or the Bot's 👍 reaction if it predates nothing newer); fix P0/P1 inline findings with a fix commit and repeat; record `bot: none` if nothing arrives. Do not resolve threads.
3. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA, the VERIFY results with sources.
4. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
5. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=30.

## PONG decision 1 (2026-10-03T07:56Z, status=blocked: global-option forms)

Codex Bot on 04d6e1f3: `terraform -chdir=<dir> apply`, `kubectl --context <x> apply`, `chezmoi --source <d> --config <f> apply` put arbitrary-valued global options before the subcommand, so no prefix rule matches them without forbidding the whole tool in the machine-global `~/.codex/rules`.

- Decision: **(c)**. The rules file mirrors the Claude deny list, whose `Bash(terraform apply:*)`-style patterns have exactly the same gap; forbidding `terraform`, `kubectl` or `chezmoi` wholesale would also block their read-only uses (`chezmoi diff`/`status` are legitimate worker commands) in every Codex session on the machine, not only this repository. Document in the file header and the README paragraph: prefix rules cover the documented invocation forms; global-options-first forms are outside prefix coverage for both vendors, and the sandbox (read-only / workspace-write with writable roots) is the backstop. Do not add tool-wide forbids.
- Bot threads for these two findings: list them in the report as proposed `not-applicable` with that reason (the orchestrator replies and resolves). Keep the three fixes already made in e16012eb.
- Continue to RESULT once the Codex review of the final head has completed.

## Revise round 1 (2026-10-03, after RESULT on 1f4f409a)

Per-commit audits: a0b05905 `incorrect` (5 findings, 4 fixed later in the PR), 04d6e1f3 `incorrect` (make init/setup, fixed in e16012eb/1f4f409a), e16012eb `incorrect` (2 findings, make setup fixed in 1f4f409a), 7a7c21cd `correct`, 1f4f409a `correct`. Two findings are still live on the head; fix both in one commit:

1. **`chezmoi init` aliases (audit P2 on e16012eb):** `chezmoi init -a` and `chezmoi init --apply=true` return no match. Make the rule `["chezmoi", "init", ["--apply", "--apply=true", "-a"]]` (VERIFY with `codex execpolicy check` that all three are forbidden and `chezmoi init --data=false` stays unmatched); add the two prefixes to `REQUIRED_PREFIXES` in `tests/unit/test_codex_execpolicy.py` and to the README list.
2. **Header claim about allow rules (audit P3 on a0b05905):** the header says an allow rule "buys nothing" under `--ask-for-approval never`. The auditor cites `codex-rs/core/src/exec_policy.rs` (rust-v0.160.0, around line 440): an explicit `allow` decision lets a command run without the sandbox, so allow rules do change execution permissions. VERIFY against that source and reword the sentence to the truth (for example: "allow rules are not repository-managed by policy: an explicit allow lets a command run outside the sandbox, which this repository never grants to an agent; interactive sessions may still add them, and the next apply removes them"). Same correction in the README paragraph if it repeats the claim.

Then push, wait for the Codex review of the new head, fix any new inline finding in the same round, CI green, branch up to date, new RESULT; do not resolve threads.

## Revise round 2 (2026-10-03, after RESULT on 8770ed66)

Audits: eb67299c `correct`; 34e7423f `incorrect` (`--one-shot=true`, fixed in 8770ed66); 8770ed66 `incorrect` with two live findings: `chezmoi edit --watch <target>` applies on save and is unmatched; the boolean aliases cover only `true` while pflag also accepts `1`, `t`, `T`, `TRUE`, `True` (`chezmoi init -a=1`, `--one-shot=1`, `edit --apply=1` unmatched).

Decision: stop enumerating chezmoi flag spellings. An agent has no legitimate use for `chezmoi init` (operator bootstrap) or `chezmoi edit` (opens an editor; agents edit source files directly), so forbid both subcommands wholesale: replace the `chezmoi init <aliases>` and `chezmoi edit <aliases>` rules with `["chezmoi", "init"]` and `["chezmoi", "edit"]` (keep `apply` and `update`). `chezmoi diff`, `status`, `managed`, `execute-template`, `data`, `cat` stay unmatched (verify). Update `REQUIRED_PREFIXES` (drop the alias tuples, add `("chezmoi","init")`, `("chezmoi","edit")`), the README list, and the header sentence that names the init/edit forms. One commit; push; wait for the Codex review of the new head; fix any new inline finding in the same round; CI green; branch up to date; new RESULT; do not resolve threads. If the Bot again enumerates spellings of an already-covered class, cite the header coverage statement in the report as the proposed `not-applicable` reason instead of another commit.
