# AGMSG-TASK dot-formatter-hook-root-fix-T61-a01

Drafted 2026-10-03 by the orchestrator seat; operator-approved ("後者で進めろ、T61 を起票しろ": format the repository once and keep it formatted in CI, rather than deleting the hook). Worker: `claude-standard-dot-a005` in `/home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c`.

## Objective

The Claude PostToolUse hook `home/dot_claude/hooks/executable_format-edited-files.py` runs `uvx ruff format`, `uvx ruff check --fix`, `uvx ty check` and `npx prettier@2 --write` on every edited `.py`/`.md` file. The repository is not formatted to those tools and nothing in CI checks it, so a worker's one-line edit turns into a reformat of the whole file (T57 README +21/−7, T59 test file +21/−7) and workers dodge the hook with scripts. The tools are also unpinned downloads at hook time. Measured by the orchestrator on 2026-10-03 (`uvx ruff 0.16.9`, `prettier 3.9.9`): 69 of 98 tracked `.py` files would change at ruff's default line length 88, 45 of 57 non-vendor files at line length 120; 21 of 56 non-record `.md` files would change under prettier 3, 15 of them under `vendor/`.

Make the hook idempotent on a formatted repository, pin its tools in the one pin source, and let CI keep it that way:

1. **Pins.** Add `ruff` and `npm:prettier` (prettier 3, current stable) to `home/dot_mise/config.toml` with matching `mise.lock` entries (`mise lock`/`mise install --locked` in the worktree). These are new tools, not version bumps of existing pins, so they travel in this task; do not change any existing pin.
2. **Configuration.** New root `ruff.toml`: `line-length = 120` (matches `vendor/compactiondb/pyproject.toml` and minimises churn), `target-version` = the lowest Python the CI matrix runs (state how you determined it), `extend-exclude = ["vendor", ".ua", ".orchestration", "reviews", ".claude", "references"]`. New root `.prettierignore` with `vendor/`, `.ua/`, `.orchestration/`, `reviews/`, `.agents/`, `.claude/`, `references/`. Vendored and record files stay byte-identical; records are written by agents and must not be reflowed (task files are hashed into `task_rev`).
3. **Hook.** `format-edited-files.py` runs exactly `ruff format <files>` and `prettier --write <files>`, resolved from `PATH` (mise shims provide the pinned versions; no `uvx`/`npx`, no version literal). Drop `ruff check --fix` (lint fixes change code beyond formatting and there is no lint policy or CI lint yet; 247 findings today) and `uvx ty check` (a type-check report has no place in a formatter hook). In `home/dot_agents/agent-config.yaml` remove the `python_post_edit` and `markdown_post_edit` command lists, which the hook never read (dead configuration, target-state appendix A), and change `scripts/generate-agent-configs.py` so the PostToolUse entry is rendered when `format_edited_files_hook` is set; update the generator tests accordingly and run `make render-check` so the rendered settings stay in sync.
4. **CI.** In `.github/workflows/test.yaml`, install `ruff` and `npm:prettier` in the existing exact-config step (`mise -C "${RUNNER_TEMP}/statusline-mise" install --locked …`, the directory that copies `home/dot_mise/config.toml` and `mise.lock`), and add one step next to the `shfmt` step that runs `mise -C <that dir> x ruff -- ruff format --check` over `git ls-files '*.py'` and `mise -C <that dir> x npm:prettier -- prettier --check` over `git ls-files '*.md'` (`.prettierignore` applies). No version literal in the workflow: the pin source is the mise config. Extend `make format` (Makefile:156, today `shfmt --diff`) with the same two checks so local and CI agree.
5. **One-time format, as its own commit.** A commit that contains only the output of `ruff format` and `prettier --write` on tracked files (the exclusions above), nothing else; verify by re-running both on the head (`git status --short` empty) and by `make unit-test`. Keep the tooling in a separate commit so each commit is auditable on its own.
6. **Codex Bot.** After the final push, run `python3 scripts/pr-feedback.py <pr> --json "$TMPDIR/sweep.json"` (read-only) and address every Codex inline finding with a fix commit, or state in the report why it does not apply. Do not resolve threads; the orchestrator does that at acceptance.

[memory:decision] T61 (operator 2026-10-03): the repository is formatted once with ruff (line length 120) and prettier 3, both pinned in the mise config; the Claude formatter hook runs only `ruff format` and `prettier --write` from the pinned tools, and CI checks formatting, so an agent's edit never produces unrelated diff lines. Vendored and record paths are excluded.

## Repo / branch

- Work ONLY in the worker-c worktree. `git fetch origin`; `git switch -c chore/formatter-root-fix origin/main` (f8e22ba3 or later, after #232 merges it may be newer). Verify the dispatched task_rev sha256 against this file; else stop and PONG blocked.
- Strict status checks apply: if `main` moves while the PR is open, `gh pr update-branch <pr>` and wait for CI again before RESULT.

## Allowed files

- `home/dot_mise/config.toml`, `home/dot_mise/mise.lock` (only adding `ruff` and `npm:prettier`)
- `ruff.toml`, `.prettierignore` (new)
- `home/dot_claude/hooks/executable_format-edited-files.py`
- `home/dot_agents/agent-config.yaml` (the `hooks` block only), `scripts/generate-agent-configs.py`, and the rendered outputs `make render-check` governs
- `.github/workflows/test.yaml`, `Makefile` (`format` target)
- `tests/**` that assert the hook, the generator, the manifest hooks block, the supply-chain pin policy, or the workflow (name each in the report)
- every tracked `*.py` and `*.md` outside the excluded paths, in the format-only commit
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-formatter-hook-root-fix-T61-a01.md` (main checkout)

## Forbidden actions

- Changing the version of any existing pin; any `ruff check --fix` or lint rule enforcement; semantic edits inside the format-only commit; touching `vendor/`, `.ua/`, `.orchestration/` (other than your artifacts), `reviews/`; a version literal for ruff or prettier anywhere but the mise config; local bats; `make update`/`make apply`; merging; force push; pushing `main`.

## Validation commands (paste verbatim output)

```
git log --oneline origin/main..HEAD                       # tooling commit(s) and exactly one format-only commit
git diff --stat origin/main..<tooling-commit>
git diff --stat <tooling-commit>..<format-commit> | tail -1
grep -n 'ruff\|prettier' home/dot_mise/config.toml; grep -c 'ruff\|prettier' home/dot_mise/mise.lock
grep -rn 'ruff@\|prettier@\|uvx\|npx' .github/workflows/test.yaml home/dot_claude/hooks/executable_format-edited-files.py Makefile; echo "exit=$?"   # expect no matches, exit=1
git ls-files '*.py' | xargs mise x ruff -- ruff format --check | tail -1
git ls-files '*.md' | xargs mise x npm:prettier -- prettier --check | tail -1
git ls-files '*.py' | xargs mise x ruff -- ruff format; git ls-files '*.md' | xargs mise x npm:prettier -- prettier --write; git status --short | wc -l   # expect 0 on the head
make format; make unit-test; make render-check; make validate-agent-assets
gh pr checks <pr-number>
gh api repos/mryfmo/dotfiles/pulls/<pr-number> --jq '.mergeable_state'
```

## Completion

1. PR to `main`, English title/description ending with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. CI green on the final head, branch up to date with `main`.
2. Artifacts at the exact expected paths; validation with verbatim outputs, PR number, head SHA and the per-commit SHAs; report lists the chosen versions, the target-version derivation, every test file touched, and the Bot threads with their fix commits.
3. CompactionDB `memory add --kind decision --scope project` with the `[memory:decision]` text from the main checkout; paste command and output.
4. `AGMSG-RESULT v1` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot wT:p1 "<single line>"` (outside the sandbox). `cost:` line. max_turns=40.

## Revise round 1 (2026-10-03, after RESULT on ae806f37)

Per-commit audits: 45d44292 `incorrect` (5 findings, 4 fixed later in the PR), bd9a7995 `correct`, e5648fa6 `incorrect` (plans corruption, fixed by b5084de5/57021632), ff37f41d `correct`, b5084de5 `correct`, 772ff3c6 `incorrect` (1 P3), 57021632 `correct`, ae806f37 `correct`. Orchestrator re-derivation: the format-only commit reproduces from `bd9a7995` with the pinned tools except one prettier non-idempotent line in plans/005 (later restored); the head is a fixpoint (re-running both tools changes nothing).

Live on the head, fix in this round (one push, then a new RESULT):

1. **Install the formatters on existing machines (Codex P1, audit P1 on 45d44292).** Allowed files extended to `Makefile` line 72 (`mise install --locked npm:ccstatusline npm:ccusage npm:pnpm`) and `install/common/mise.sh` line 108: add `ruff npm:prettier` to both install lines so `make update` and first setup provide what the hook calls. Nothing else in those files.
2. **`CLAUDE.md` is installer-managed.** prettier inserted blank lines inside the `<!-- compactiondb:begin -->…end -->` block; `vendor/compactiondb/install.py` (`append_instruction`) rewrites that block without them, so the CI check and the installer would ping-pong. Add `CLAUDE.md` to `.prettierignore` (comment: CompactionDB-managed block) and restore the file to its `origin/main` bytes (`git checkout origin/main -- CLAUDE.md`; verify with `git diff --quiet origin/main -- CLAUDE.md`).
3. **Hook (audit P3 on 772ff3c6):** `repository_root` uses `result.stdout.strip()`; use `rstrip("\n")` so a repository path with trailing spaces is not altered.

Keep the format-only commit untouched; put the three fixes in one commit; CI green; branch up to date; list every Codex thread with its fix commit in the report; do not resolve threads.

## Revise round 2 (2026-10-03, after RESULT on 3da4cfad)

The three Codex P2 threads opened on 0827371f/3da4cfad are valid and are fixed in this PR, not deferred: a Bot finding is fixed at its root once (operator rule), and "follow-up" is not a disposition. One commit with the three fixes:

1. **`should_test` filter (test.yaml `changes` job):** any changed `*.py` or `*.md` outside `.orchestration/` sets `should_test=true` (for example an alternation `(^|/)[^/]+\.(py|md)$` applied after excluding `^\.orchestration/`), so nested Markdown such as `.github/ISSUE_TEMPLATE/*.md` and Python in new directories cannot bypass the formatting check. Keep `.orchestration/`-only diffs skipping the matrix.
2. **`make format`:** call `ruff` and `prettier` from `PATH` (the mise shims of the pinned tools, which `make update` now installs) instead of `mise x`, so an untrusted repository `mise.toml` cannot make the target refuse; keep `--config ruff.toml`.
3. **Hook:** when `<repository root>/ruff.toml` exists, pass `--config <root>/ruff.toml` to `ruff format`, so the root exclusions govern even a file under a nested `pyproject.toml`; extend the existing hook test (fake `ruff` records its arguments) to assert the flag.

Then: push, wait for the Codex review of the new head to complete (the review-activity summary comment shows "Completed" for that commit, or the 👍 reaction), and fix any new inline finding in the same round before RESULT. Stop only when the head has no open finding, or the remaining ones are not applicable for a reason stated in the report. CI green, branch up to date (`gh pr update-branch` if `main` moved), do not resolve threads, list every thread with its fix commit.

## Revise round 3 (2026-10-03, after RESULT on 74ade52f)

Audits: 0827371f `correct`; 74ade52f `incorrect` with one P2, reproduced by the auditor: `git diff --name-only` quotes non-ASCII paths by default (`core.quotePath`), so a changed `.github/ISSUE_TEMPLATE/日本語.md` reaches the filter as `"\343\...md"` with a closing quote and matches neither alternative, giving `should_test=false`.

One commit: read the changed paths with `git -c core.quotePath=false diff --name-only "${diff_range}"` (keeps the here-string logic from 74ade52f; no pipe), and state in the report a reproduction with a non-ASCII `.md` path showing `should_test=true`. Then push, wait for the Codex review of the new head to complete, fix any new inline finding in the same round, CI green, branch up to date, new RESULT; do not resolve threads.
