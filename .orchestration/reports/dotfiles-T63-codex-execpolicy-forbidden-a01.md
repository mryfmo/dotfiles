# Report: dotfiles-T63-codex-execpolicy-forbidden-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c. Branch `chore/codex-execpolicy-forbidden` from `origin/main` 910ba6f5, with commits `a0b05905` (the change), `04d6e1f3`, `e16012eb` (Codex fixes), `7a7c21cd` (PONG decision 1 documentation) `1f4f409a` (`make setup`) `eb67299c` (revise round 1) `34e7423f` (Codex P2s on eb67299c) `8770ed66` (Codex findings on 34e7423f) `c58e4835` (revise round 2), `7e83ed9c` (`./setup.sh`) and `ddb7bf16` (`make clean`/`deploy`), both Codex findings on c58e4835; the final head is `ddb7bf16`.
- **PR:** #235, https://github.com/mryfmo/dotfiles/pull/235.
- **task_rev:** `012c39f6…`, matched.
- **Status:** ready_for_review. CI, `mergeable_state` and the Codex Bot state on the final head are in the validation file.

## Change (3 files)

- **`home/dot_codex/rules/default.rules` (new):** a plain chezmoi file that becomes `~/.codex/rules/default.rules`. It contains 7 `prefix_rule` entries, all `decision="forbidden"`, that cover 10 prefixes:
  - `sudo`
  - `rm -rf` and `rm -fr` (one pattern with alternatives)
  - `gh pr merge`
  - `gh release`
  - `npm publish` and `uv publish` (alternatives)
  - `terraform apply` and `kubectl apply` (alternatives)
  - `chezmoi apply`

  Each rule has a `justification` naming the sanctioned alternative, plus `match`/`not_match` examples that Codex validates at load time. The file has **0 allow rules**. The English header states:
  - the file is rewritten on every `chezmoi apply`;
  - an interactive "always allow" is reset by the next apply and shows in `chezmoi diff` until then;
  - the 23 accumulated allows are dropped deliberately;
  - forbidden is a refusal under every approval policy and wins over allow;
  - pipelines such as `curl … | sh` cannot be expressed as a prefix rule, and the Claude deny list covers them.
- **`README.md`:** one paragraph after the Codex escalation paragraph (around line 620): the forbidden set is repository-managed, what it forbids, and that interactive "always allow" additions do not survive `chezmoi apply`.
- **`tests/unit/test_codex_execpolicy.py` (new):** parses the rules file with `ast`, expands the alternatives, and asserts that every rule is `forbidden` with a justification and that the covered prefixes equal the declared set exactly. No existing test enumerates `home/dot_codex/**`; I grepped for that.

Nothing else changed: no generator, manifest, `approval_policy`, sandbox or live `~/.codex` change. The read-only `chezmoi diff` (pasted) shows the 23 live allow lines replaced by the managed content.

## VERIFY (sources and outputs in the validation file)

- **(a) Syntax and loading:**
  - `prefix_rule(pattern=[...], decision?, justification?, match?, not_match?)`, where a list element in `pattern` denotes alternatives and `decision` is one of `allow|prompt|forbidden` (`codex-rs/execpolicy/README.md` at `rust-v0.160.0`, lines 5–22).
  - Rules load from `<config folder>/rules/*.rules` for every config layer, low to high precedence (`codex-rs/core/src/exec_policy.rs` at `rust-v0.160.0`: `RULES_DIR_NAME = "rules"`, `RULE_EXTENSION = "rules"`, `load_exec_policy`). For the user layer this is `~/.codex/rules/*.rules`, and `default.rules` is the file that interactive approvals amend.
  - `codex execpolicy check --rules home/dot_codex/rules/default.rules …` (CLI 0.160.0) loads the file, so the `match`/`not_match` examples validate. It returns `forbidden` for all 10 forbidden commands and no match for 9 neighbours (`rm <file>`, `gh pr view`, `gh pr create`, `npm install`, `uv run pytest`, `terraform plan`, `kubectl get`, `chezmoi diff`, `git status`).
- **(b) Precedence:** "the effective decision is the strictest severity across all matches (forbidden > prompt > allow)" (execpolicy README line 95). Measured: `gh pr merge 1` gives `forbidden` with this file plus a scratch file that allows `gh pr merge`, and `allow` with the scratch file alone.
- **(c) Refusal, not a prompt:** in `exec_policy.rs`, `Decision::Forbidden => ExecApprovalRequirement::Forbidden { reason: derive_forbidden_reason(...) }` does not consult `approval_policy`. Only the `prompt` branch does, through `prompt_is_rejected_by_policy`. So a forbidden match is a refusal under both `on-request` and `never`, and the model receives "`<cmd>` rejected: <justification>" (`derive_forbidden_reason`). `zsh -lc`/`bash -lc` wrappers are unwrapped before matching (`shell-command/src/bash.rs`: `extract_bash_command` accepts Zsh, Bash and Sh).
- **End-to-end `codex exec`: NOT shown.** I ran two attempts with the express profile (`MODEL_PROFILE_EXPRESS_CODEX_ARGS` = `--profile express`), `--sandbox read-only`, and a scratch git repo holding the rules as a project layer (`.codex/rules/default.rules`, then also an empty `.codex/config.toml`), trusted through `-c projects."<scratch>".trust_level="trusted"`. Both times the model ran `zsh -lc 'gh pr merge 1'` and gh answered "no git remotes found", so the scratch project layer did not load the rules. The likely cause is that the `-c` trust override does not enable a project layer for `codex exec`. I did not copy or link the live `~/.codex` credentials into a scratch `CODEX_HOME`, and I did not edit `~/.codex`. The deployment path is the **user layer**, which the source shows is loaded.
  - **Operator post-apply check:** after `make update`, run `codex execpolicy check --rules ~/.codex/rules/default.rules gh pr merge 1` (expect `forbidden`), and optionally an exec run as above but without the scratch project.

## Codex Bot

On `a0b05905` the bot left three P2 findings, all valid. I fixed them in `04d6e1f3`; the operator rule is to fix a Bot finding at its root, not defer it.

| Thread | Fix |
|---|---|
| P2 Block split recursive rm flags | Added `["rm", ["-r","-R","--recursive"], ["-f","--force"]]`, the reverse order, and `-Rf`/`-fR` in the combined rule, each with load-time `match` examples. `rm -r x` stays unmatched (checked). |
| P2 Prevent make targets from bypassing chezmoi apply | Added `["make", ["update","apply","upgrade","watch","reset","reset-config"]]`: `update`, `apply` and `watch` run `chezmoi apply`, `upgrade` is operator lifecycle, and `reset`/`reset-config` change chezmoi state. `make unit-test`, `format` and `render-check` stay unmatched. The header and README state the limits that remain: flags after operands, `make -C <dir>`, and commands spawned by scripts. |
| P2 Restart Codex after replacing its rules | The header and README say that Codex reads rules at startup, so running sessions must restart after `make update` (`herdr-agents --restart-worker` for the pair worker). |

**Scope note for the orchestrator.** The forbidden set now goes beyond the task's list: the split `rm` forms and the six `make` targets are added. The recorded CompactionDB decision text lists the original set. If you accept the extension, consolidate an amended decision at acceptance. The file now has **11** forbidden rules and still **0** allow rules.

The bot review state of the then-final head `04d6e1f3` is in the validation file (`bot:` line).

## CompactionDB

```
cd ~/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T63 (operator 2026-10-03): the Codex execpolicy forbidden set (sudo, rm -rf, gh pr merge, gh release, npm/uv publish, terraform/kubectl apply, chezmoi apply) is declared once in `home/dot_codex/rules/default.rules` and overwrites the live rules on every chezmoi apply; no repository-managed allow rules exist.'
9ccb9164-013d-4f77-b034-407ad252d0d0
```

[memory:decision] dotfiles-T63 (operator 2026-10-03): the Codex execpolicy forbidden set (sudo, rm -rf, gh pr merge, gh release, npm/uv publish, terraform/kubectl apply, chezmoi apply) is declared once in `home/dot_codex/rules/default.rules` and overwrites the live rules on every chezmoi apply; no repository-managed allow rules exist.

## Artifacts

- validation: `.orchestration/validation/dotfiles-T63-codex-execpolicy-forbidden-a01.md`
- sandbox: `.orchestration/sandboxes/dotfiles-T63-codex-execpolicy-forbidden-a01.md`
- learning: `.orchestration/learning/dotfiles-T63-codex-execpolicy-forbidden-a01.md`
- autoskill: `.orchestration/autoskill/runs/dotfiles-T63-codex-execpolicy-forbidden-a01.md`

cost: n/a for the session. The two scratch `codex exec` runs reported 9,071 and 9,036 tokens (express profile).

## Codex review of 04d6e1f3: four findings (two P1); decision needed

Fixed in `e16012eb`:

- **P1 Block the absolute sudo path.** `sudo` now also matches `/usr/bin/sudo` (which `setup.sh` uses), `/bin/sudo`, `/usr/local/bin/sudo` and `/run/wrappers/bin/sudo`.
- **P2 Cover combined rm force/recursive flags.** Every ordering of `r|R` and `f`, alone or with `v`, is covered (`-rfv`, `-vRf`, …). `rm -rv` stays unmatched.
- **P2 Cover alternate chezmoi apply entry points, in part.** `chezmoi init --apply` and `make init` are forbidden.

**Open, and the orchestrator's decision:** the P1 `terraform -chdir=<dir> apply` and the rest of the P2, `chezmoi --source <dir> --config <file> apply` (Makefile:65-67). `kubectl --context <c> apply` has the same shape.

In each, a global option with an **arbitrary value** comes before the subcommand. execpolicy prefix rules match fixed tokens with listed alternatives and have no wildcard, so these forms cannot be forbidden without forbidding the whole tool (`["terraform"]`, `["kubectl"]`, `["chezmoi"]`). These rules live in the global `~/.codex` and apply in every repository on the machine. Forbidding the whole tool would also block `terraform plan`, `kubectl get` and `chezmoi diff` everywhere, which goes beyond the task's stated set.

**Options:**
- **(a)** Forbid the whole `terraform` and `kubectl` tools, and keep `chezmoi` limited to `apply` and `init --apply`.
- **(b)** Forbid all three whole tools.
- **(c)** Keep the subcommand rules, and state in the header and README that global-option forms are outside prefix-rule coverage, with the sandbox and network denial as the backstop.

The PONG asks the orchestrator to choose.

## PONG decision 1 applied (task_rev `28393b19…`): option (c), commit `7a7c21cd`

The rules header and the README paragraph now state the following. Prefix rules cover the documented invocation forms only. Global options with arbitrary values placed before the subcommand (`terraform -chdir=<dir> apply`, `kubectl --context <c> apply`, `chezmoi --source <d> --config <f> apply`), flags after the operands, `make -C <dir>`, and commands a script spawns are outside prefix coverage, for Codex and the Claude Code deny list alike. The sandbox (read-only, or workspace-write with its writable roots) is the backstop. No tool-wide forbids were added, and the three fixes from `e16012eb` are kept.

**Proposed dispositions for the orchestrator's sweep. I did not reply to or resolve any thread.**

| Thread | Disposition |
|---|---|
| P2 Block split recursive rm flags (a0b05905) | fixed:`04d6e1f3` |
| P2 Prevent make targets from bypassing chezmoi apply (a0b05905) | fixed:`04d6e1f3` (`make init` added in `e16012eb`) |
| P2 Restart Codex after replacing its rules (a0b05905) | fixed:`04d6e1f3` |
| P1 Block the absolute sudo path (04d6e1f3) | fixed:`e16012eb` |
| P2 Cover combined rm force/recursive flags (04d6e1f3) | fixed:`e16012eb` |
| P2 Cover alternate chezmoi apply entry points (04d6e1f3) | `chezmoi init --apply` and `make init` fixed in `e16012eb`. Proposed **not-applicable** for the `chezmoi --source <d> --config <f> apply` part: global options with arbitrary values before the subcommand cannot be matched by a prefix rule without forbidding the whole tool in the machine-global `~/.codex/rules`, which would also block `chezmoi diff`/`status`. The sandbox is the backstop (PONG decision 1, option c, documented in `7a7c21cd`). |
| P2 Forbid the setup make target (e16012eb) | fixed:`1f4f409a` (`make setup` added to the forbidden make targets; it runs `./setup.sh`, which reaches `chezmoi apply`). I found this thread while reading back the validation file. Codex had reviewed `e16012eb` before my doc push, and I had not polled that head. |
| P1 Block Terraform applies with global options (04d6e1f3) | Proposed **not-applicable**: `terraform -chdir=<dir> apply` puts an arbitrary-valued global option before the subcommand, which a prefix rule cannot match without forbidding all of `terraform` (including `plan`) in every Codex session on the machine. The sandbox is the backstop (PONG decision 1, option c, documented in `7a7c21cd`). |

## Revise round 1 (task_rev `4258ed09…`), commit `eb67299c`

1. **`chezmoi init` aliases (audit P2 on e16012eb).** The rule is now `["chezmoi", "init", ["--apply", "--apply=true", "-a"]]` with load-time match examples. The README list and `REQUIRED_PREFIXES` gain the two new forms. Checked with `codex execpolicy check`: `chezmoi init --apply`, `--apply=true` and `-a` are all `forbidden`; `chezmoi init --data=false` and a bare `chezmoi init` stay unmatched.
2. **Allow-rule claim (audit P3 on a0b05905).** **My header was wrong.** It said that an allow rule "buys nothing" under `--ask-for-approval never`. In `codex-rs/core/src/exec_policy.rs` at `rust-v0.160.0` (lines 439–453, pasted), `Decision::Allow` maps to `ExecApprovalRequirement::Skip { bypass_sandbox: … }`, which is true when every parsed command segment is explicitly allowed. An allow rule therefore lets that command run **outside the sandbox**. The header now gives the correct reason no allow rules are managed: they would grant a sandbox bypass, which this repository never gives an agent. Interactive sessions may add allow rules, and the next apply removes them. The README did not repeat the claim; its "no allow rules / reset by the next apply" sentence was already accurate.

### Codex review of `eb67299c`: two P2 findings, fixed in `34e7423f`

| Thread | Fix |
|---|---|
| P2 Forbid separated verbose recursive rm flags | Four ordered rules cover a separate `-v`/`--verbose` placed before or between the recursive and force flags (`rm -r -v -f`, `rm -v -r -f`, `rm -v -f -r`, `rm -f -v -r`). A trailing `-v` already matched the two-flag rules. `rm -v -r` and `rm -r -v` without force stay unmatched (checked). |
| P2 Forbid the chezmoi init one-shot apply mode | `--one-shot` joins the `chezmoi init` alternatives (checked: forbidden). |

The file had **15** forbidden rules at `34e7423f`. These findings keep enumerating spellings that prefix rules must list one by one. Inserted options such as `rm -r -i -f` remain possible in principle, and the header already says that the rules cover the documented forms, with the sandbox as the backstop.

### Codex review of `34e7423f`: one P1 and three P2, fixed in `8770ed66`

| Thread | Fix |
|---|---|
| P1 Forbid explicit infrastructure destruction | `["terraform", ["apply", "destroy"]]` and `["kubectl", ["apply", "delete"]]` replace the combined apply rule. `terraform plan`, `kubectl get` and `kubectl diff` stay unmatched (checked). |
| P2 Forbid the implicit apply in `chezmoi update` | `["chezmoi", "update"]` is forbidden; `chezmoi status` stays unmatched. |
| P2 Forbid `chezmoi edit --apply` | `["chezmoi", "edit", ["--apply", "--apply=true", "-a", "-a=true"]]`; a plain `chezmoi edit` stays unmatched. |
| P2 Cover true-valued `init` apply aliases | `-a=true` and `--one-shot=true` join the `chezmoi init` alternatives. |

The file now has **18** forbidden rules and **0** allow rules.

**Non-convergence, flagged for the orchestrator.** Each Codex review so far (a0b05905, 04d6e1f3, e16012eb, eb67299c, 34e7423f) has found further spellings or neighbouring commands in classes the file already covers. Prefix rules have to enumerate every spelling, so this is open-ended; for example, `rm -r -i -f` and `chezmoi edit <target> --apply` remain possible. I fixed every finding raised so far. If Codex finds more on `8770ed66`, I propose a stop rule rather than another round: the rules cover the documented forms, and the sandbox is the backstop, as already stated in the header and README under PONG decision 1.

## Revise round 2 (task_rev `7f7a1751…`), commit `c58e4835`

- **Audit on `8770ed66`:**
  - `chezmoi edit --watch <target>` applies on save and was unmatched.
  - pflag also accepts `1`, `t`, `T`, `TRUE` and `True` as boolean true, so `chezmoi init -a=1`, `--one-shot=1` and `edit --apply=1` were unmatched.
- **Decision:** stop enumerating chezmoi flag spellings. The alias rules are replaced by `["chezmoi", "init"]` (operator bootstrap) and `["chezmoi", "edit"]` (it opens an editor; agents edit source files directly). `chezmoi apply` and `chezmoi update` stay forbidden.
- **Checked with `codex execpolicy check`:**
  - **Forbidden:** `chezmoi init`, `init -a=1`, `init --one-shot=1`, `init --apply`, `edit`, `edit --watch`, `edit --apply=1`, `apply` and `update`.
  - **Unmatched:** `chezmoi diff`, `status`, `managed`, `execute-template`, `data` and `cat`.
- **Test and README:** `REQUIRED_PREFIXES` drops the alias tuples and adds `("chezmoi","init")` and `("chezmoi","edit")`. The README list now says "all of `chezmoi init` and `chezmoi edit`".
- **Header:** it did not name the init/edit alias forms, so it needed no change; its coverage statement already applies.
- **Rule count:** 18 forbidden rules (the same rules, with two of them generalised) and 0 allow rules.

If the Bot enumerates more spellings of a class that is already covered, the proposed `not-applicable` reason is the header coverage statement: prefix rules cover the documented invocation forms, and the sandbox is the backstop.

### Codex review of `c58e4835`: three P2 findings (two fixed in `7e83ed9c` and `ddb7bf16`, one proposed not-applicable)

| Thread | Disposition |
|---|---|
| P2 Block direct setup script invocations (`./setup.sh`) | **fixed in `7e83ed9c`.** This is a distinct entry point, not a spelling. It is the script that the already-forbidden `make setup` wraps, and it reaches `chezmoi apply` the same way. New rule: `[["./setup.sh", "setup.sh"]]`. Also added: `REQUIRED_PREFIXES` gains `("./setup.sh",)`, and the README clause "and `./setup.sh`, which `make setup` wraps". `codex execpolicy check` results: `./setup.sh` and `setup.sh --help` are forbidden. An absolute path (`<repo>/setup.sh`), `bash -lc ./setup.sh` (the CLI check does not unwrap shells), and `shellcheck setup.sh` are no-match. I did not enumerate the interpreter and absolute-path spellings; they fall under the header coverage statement. |
| P2 Forbid the clean make target (`make clean` runs `rm -rf docs/reference site`, `Makefile:209`) | **fixed in `ddb7bf16`.** I missed this third thread when I wrote `7e83ed9c` and found it in the unresolved-thread sweep afterwards. `clean` is added to the make union. In the same commit I also added `deploy` **on my own initiative, not flagged by the bot**: `make deploy` runs `mkdocs gh-deploy --force --ignore-version`, which force-pushes the docs site and so belongs to the publish class (`gh release`, `npm publish`). Drop it if you do not want it. `make docs`, `make serve` and `make unit-test` stay unmatched. Also updated: `REQUIRED_PREFIXES`, the README and the rule examples. |
| P2 Cover grouped force and verbose rm flags (`rm -r -fv build`, `-vf`, `-R` and reordered forms) | **proposed not-applicable, no commit (round-2 rule).** These are further spellings of the recursive-force `rm` class, which the file already covers in its combined, split and separated `-v` orderings. Header coverage statement, verbatim: "Rules match the argument list Codex is asked to run, prefix token by token, so they cover the documented invocation forms only." The header names `rm build -rf` as an uncovered example and states "the sandbox (read-only, or workspace-write with its writable roots) is the backstop for them". |

- **Load-time example validation:** Codex validated a `not_match` example of `./scripts/setup.sh` against the bare `setup.sh` alternative through `resolved_program` and rejected the file. The CLI `check` of the same argv is no-match. I replaced that example with `setup-gh`.
- **Final head:** `ddb7bf16`. CI, branch status and the Codex review are recorded in the validation file.
- **Intermediate head `7e83ed9c`:** CI green (13 pass including CodeRabbit, `nix` skipped); Codex left a 👍 at 11:46:05Z with no inline thread.
- **Final head `ddb7bf16`:**
  - **CI:** green; 13 pass including CodeRabbit, and `nix` is skipped.
  - **Branch:** up to date with `main` 910ba6f5 (behind_by=0).
  - **Codex:** 👍 at 12:12:29Z, with no inline thread.
  - **`mergeStateStatus`:** BLOCKED only by three unresolved threads, which are left for the orchestrator:
    - 4172944446 (fixed in `7e83ed9c`)
    - 4172944463 (fixed in `ddb7bf16`)
    - 4172944456 (proposed not-applicable)
  - **Round-2 commits:** three (`c58e4835`, `7e83ed9c`, `ddb7bf16`), not one, because the review of the round-2 head opened new findings that had to be fixed in the same round.
  - **Rule count at `ddb7bf16`:** 19 forbidden rules and 0 allow rules (`grep -c "prefix_rule(" home/dot_codex/rules/default.rules` = 19). The rule list at line 10 describes the first commit `a0b05905`.
