# Problem statement for the remediation research (measured 2026-10-28, JST)

Program: `regime-cutover` in `~/Workspace/dotfiles` (store `.orchestration/orchestrate/regime-cutover/`, handoff set under `handoff/`). Every fact below was measured in the coordinator session unless labelled inferred.

Local tool versions (measured): git 2.56.0, shfmt v3.14.1, ShellCheck 0.11.0, codex-cli 0.164.0, sandbox-runtime (srt) 0.0.81, Bats 1.14.0, npm 11.20.0, node v26.12.1, gh 2.103.2, mise 2026.10.19, bun present.

## Phenomena (implementation phase)

P1. Treadmill rounds. 13 `treadmill` or `premise` rows in `decisions.tsv`. Each: an open-ended input (shell text, process tree, git configuration or state, worktree or file-system shape, path name) judged by a hand-written parser, supervisor or heuristic; a fresh-context auditor found one more way past it per round; the run ended only when the mechanism changed (shfmt `--to-json` AST walk, one strict parser module, an exact-form allowlist, or removing the feature). Rounds per unit: U85 30, U73 29, U71b 23, U95 19, U101 13, U92 12, U71 11, U81 11, U75 10, U91 10, U96 10. The change of approach always came after 3 or more rounds, never at brief time.

P2. Fail-closed violations ("a failed read treated as an absence"), standing order 21: U25 F1 (jq inspection error read as "no hooks"), U25d F4, Codex finding 4379614437 (`git config --get` exit 3 read as unset), U101 round 11 (`git ls-files` warns and exits 0 on an unreadable directory, so missing files became deletions; origin URL read likewise).

P3. Git configuration channels reaching an automation (U101 rounds 2 to 12): `url.<base>.insteadOf` and `pushInsteadOf` (user config), `includeIf "gitdir:**/worktrees/**"`, `author.*`/`committer.*` config outranking `-c user.*`, hooks (post-checkout, pre-commit, reference-transaction), clean filters via `.gitattributes`, and `core.fsmonitor` running inside `git ls-files`. Final design: a `git init --bare --template=` scratch repository, every command under `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1`, inherited `GIT_*` removed, `-c core.fsmonitor=false -c core.hooksPath=/dev/null` on the one index read left in the checkout, identity via `GIT_AUTHOR_*`/`GIT_COMMITTER_*` on `commit-tree`, push over https with `credential.helper=!gh auth git-credential`.

P4. Process supervision (U71b 18 rounds on bash+perl supervisor; U99): setpgrp unchecked, fork-to-pid windows, readiness pipe failures; ended in one Python supervisor (`subprocess.Popen(start_new_session=True)`, `killpg`), and in U99 by removing descendant cleanup and relying on CI `timeout-minutes`.

P5. Secret-scan false positives: the repository's `validate-agent-assets.py` SECRET_PATTERN has a generic rule for `token`, `secret`, `password`, `api_key` followed by `=` or `:` and a quoted string, which matched test fixture variable assignments twice (U101 rounds 10 and 13); the scan stops at the first hit, so the second file was hidden until the first was fixed.

## Phenomena (verification phase)

V1. Audit route changes: hcom audit seat (omp, openai-siwc) hit a usage limit 2026-10-24 (gates.md G9); audits moved to `codex exec` read-only with scratch CODEX_HOME, then to the U71b lever `pr-audit.sh` (Codex permission profile `audit`: read-only, no network, credential stores denied, scratch HOME, prompt holds the `## Audit` section of `main:AGENTS.md`, the PR body `## Contract` section as untrusted data, and the diff range). Each run 6 to 8 minutes (478 s, 448 s, 359 s, 408 s measured).

V2. Per-head verdict rule: every head (fix round, merge of main, formatting commit) gets a fresh audit; `pr-merge.sh` merges only with a `correct` ledger row for the full 40-hex head sha and all checks pass. Rounds spent on "merge of main" heads bought no finding (U75 round 10, U72 round 7).

V3. The treadmill rule (3 consecutive rounds of one class) and standing order 33 (prefer removal over hardening) fire only after the fact.

V4. CI flakes fixed during the program: macos-14 brownouts and retirement (U64, U64b; ruleset swapped to macos-15 contexts), azure.archive.ubuntu.com apt mirror stalls (U15, U102; actions/runner-images#14823, #15040), chezmoi external download EOF (U96), unpinned ShellCheck/shfmt versions across hosts and CI (U97), reverse-DNS stall in HTTPServer bind on macos-15 (U98), unbounded bats tests and installer downloads (U99), git 2.55 background maintenance racing test cleanup (U100), npm `min-release-age` cooldown vs rebuild (U89), mise.bats hitting the GitHub API unauthenticated (U93), ccusage 20.0.38 published without its linux-x64 binary (U42).

V5. `pr-audit.sh` refuses a PR body without a `## Contract` section, so records-sync PRs (whose body the lever writes) get an orchestrator verdict instead (R3 proposal).

V6. Bot reviews (Codex connector, CodeRabbit) answered by `pr-thread-reply.sh` with `fixed: <sha>` / `refuted:` / `residual:` first lines; GitHub ruleset does not require thread resolution; `gh api graphql` and GitHub REST POST are blocked by the agent tool policy, so levers do those writes.

## Root causes already named in the store

RC1. Hand-written judgement of open-ended inputs, with no brief-time requirement to name the closing mechanism (AST, strict parser module, allowlist, removal).
RC2. Producer status not read (guards without the exit status of the read they depend on).
RC3. The rules that stop a treadmill are reactive (3 strikes) and text-only.
RC4. Audit capacity and the per-head rule multiply the cost of RC1.

## Proposals already drafted (handoff/03-remediation-spec.md)

R1 brief-time closure check script; R2 two-strike treadmill rule; R3 `## Contract` in the sync body; R4 store maintenance; R5 checkout residue.

## What the research must decide

For each root cause: what the official documentation and current primary sources (2025 to 2026) say is the correct mechanism, whether the program's final designs match it, what they still miss, and what the remediation units should specify. Cite the URL and the accessed date for every external claim. Prefer vendor documentation (git-scm.com, shellcheck.net wiki, mvdan/sh, GitHub Docs, docs.github.com changelog, actions/runner-images, OpenAI Codex docs, Anthropic docs, bats-core docs, npm docs, chezmoi docs) and primary issue trackers. Mark anything inferred.
