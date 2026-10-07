# Report: dotfiles-T111-project-map-subagent-a01

- **PR:** https://github.com/mryfmo/dotfiles/pull/299, branch `feat/project-map-subagent` from `origin/main` `8e9bd072`, final head `0c1d280bc62c02e5dd866994df3fd3a62cdfcee3`. Two commits: `8c9e85e7` (the change) and `0c1d280b` (ruff format fix, see objective 2).
- **Status:** ready_for_review. CI: all 13 checks pass on `0c1d280b` (output in the validation file). On `8c9e85e7`, the four `test` jobs failed only at "Check Python and Markdown formatting", because of ruff format. Bot: `bot: none`. The 15-minute wait on `0c1d280b` after green CI found no Bot review and no Bot inline comment (31 iterations, all `rc=0`, empty). On `8c9e85e7` the Codex code review reported "usage limits have been reached", and the Codex security review (trigger "PR opened") completed on `8c9e85e` without a comment or thread. Its summary comment `6027027953` (updated 2026-10-06T23:09:55Z, re-read after the final push) still names only `8c9e85e`, so no Codex review ran on `0c1d280b`. CodeRabbit skipped because auto reviews are disabled. No review, inline comment or thread exists on the PR.

## What changed (task objectives 1–7)

1. `home/dot_agents/agent-config.yaml`: `model_profiles.review.claude` is `{ model: claude-fable-5-1, effort: high }` and its comment reads `One capability tier above the worker at full effort (operator decision 2026-10-07).` `review.codex` and every other profile are untouched.
2. `scripts/generate-agent-configs.py`: `render_claude_project_map_agent(manifest)` sits directly after `render_claude_express_agent`, and `expected_outputs()` registers `home/dot_claude/agents/project-map.md` on the line after express-explorer. No new required profile, manifest key or body file. It matches the task text except for one deviation that CI forced. In commit `0c1d280b`, `ruff format` (CI's "Check Python and Markdown formatting" step, `ruff format --config ruff.toml --check`) rewrote the `description:` literal from a double-quoted string with `\"` escapes to a single-quoted string with plain `"`. The string value, and therefore the rendered `project-map.md`, is byte-identical: `make render-check` stays up to date across the commit.
3. `home/dot_agents/skills/project-map/SKILL.md` and `agents/openai.yaml`, verbatim from the task file.
4. `home/dot_config/claude/rules/project-map.md`, verbatim, and `home/dot_claude/rules/symlink_project-map.md.tmpl`, one line with a trailing newline, byte-for-byte the form of `symlink_ponytail.md.tmpl`.
5. `home/dot_agents/README.md`: `- \`home/dot_claude/agents/project-map.md\`` directly after the express-explorer line.
6. `.gitignore`: the comment and `.project-map/` after `.crit/`. I added a blank line before and after them, because the `.claude/contextdb/...` lines follow `.crit/` with no separator and would otherwise read as part of the project-map block. That makes 4 added lines, not 2: the two content lines plus two blank separators.
7. `tests/unit/test_generate_agent_configs.py`: next to the express-explorer assertions, `model: sonnet`, `effort: high` (the sample manifest's `standard.claude`) and `  - project-map\n` are asserted on `home/dot_claude/agents/project-map.md`. No other test needed a change for the `review` value; both unit modules and `make unit-test` pass.

## Generated outputs (from `uv run --no-project --with pyyaml scripts/generate-agent-configs.py`, none hand-edited)

- `home/dot_claude/agents/project-map.md`. It renders `model: claude-opus-5-5`, `effort: high` from the live `standard` profile.
- `home/dot_claude/skills/project-map/symlink_SKILL.md.tmpl`.
- `home/dot_agents/model-profiles.env`: only `MODEL_PROFILE_REVIEW_CLAUDE_ARGS="--model claude-fable-5-1 --effort high"` changed.
- **Outside the listed allowed files:** `home/dot_claude/skills/project-map/agents/symlink_openai.yaml.tmpl`. `claude_skill_symlink_outputs()` (`scripts/generate-agent-configs.py:557`) mirrors every file of a shared skill, so the allowed `agents/openai.yaml` necessarily generates this symlink, and `make render-check` fails without it. It is the generator's own output of an allowed file, not a hand edit. I committed it rather than leave render-check red; please confirm or re-task.

## User-visible impact (AGENTS.md "Dotfiles safety")

- After `chezmoi apply`, Claude Code gains a `project-map` subagent (tools Read, Glob, Grep, Bash, Write, Edit; user-scope memory) and a global rule. The rule tells the main session to launch the subagent in the background before long solo runs.
- Claude sessions on the `review` profile run `claude-fable-5-1` at `high` effort instead of `claude-fable-5` at `medium`.
- No shell startup, PATH, auth helper, hook or permission default changed.

- `chezmoi apply` replaces the unmanaged prototype `~/.claude/agents/project-map.md` (4.7 KiB, 2026-10-07 08:14). The prototype has `effort: medium`, a `NEED_STYLE` reply, preloads `frontend-design:frontend-design`, and saves its style in `style.md`. Its memory, `~/.claude/agent-memory/project-map/MEMORY.md`, only points to `style.md` (light, `#14b8a6`); it does not hold the `style:`/`accent:` keys the new skill reads, so the first run after apply may ask `STYLE-NEEDED` once. I verified this read-only, left `~/.claude/**` untouched (forbidden), and added it to the PR body's user-visible impact. Migrating the memory is up to the operator.

## Worker review (Worker Playbook step 5; `crit status --json` had no review file)

- An independent read-only subagent reviewed `8e9bd072..0c1d280b`: 3 P3, overall approve. Evidence: `.orchestration/validation/dotfiles-T111-project-map-subagent-a01-worker-crit.json` and `-worker-review-receipt.md` (`review_outcome: addressed`).
- **Design note for the orchestrator (P3, not applicable within this task):** the rule is global, and the skill appends `.project-map/` to a tracked `.gitignore` when the line is missing. A background run in another repository, including one under the agmsg regime, therefore edits a tracked file. The text is the operator's verbatim design, so I did not change it.

## CompactionDB (main checkout, through the permission gate)

```
cd ~/Workspace/dotfiles && uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T111 (operator 2026-10-07): the project-map subagent is built only from existing mechanisms: a shared skill `home/dot_agents/skills/project-map/`, a generator-rendered `home/dot_claude/agents/project-map.md` that borrows `model_profiles.standard` (no new profile), a rule `home/dot_config/claude/rules/project-map.md` with its symlink template, and a `.project-map/` gitignore line.'
uv run --no-project .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T111 (operator 2026-10-07): `model_profiles.review.claude` is `claude-fable-5-1 / high`; the three roles (deep, standard, audit) are unchanged.'
```

IDs `133c2f01-1b73-4238-8cd6-78640b67843e` and `7727698a-48d8-406d-84c4-29833f1f5364` (output in the validation file).

[memory:decision] dotfiles-T111 (operator 2026-10-07): the project-map subagent is built only from existing mechanisms: a shared skill, a generator-rendered agent that borrows `model_profiles.standard`, a rule with its symlink template, and a `.project-map/` gitignore line.
[memory:decision] dotfiles-T111 (operator 2026-10-07): `model_profiles.review.claude` is `claude-fable-5-1 / high`.

## Other

- Understand-Anything hook: did not fire in this task.
- Plan Mode not used; no Crit server started.
- Unresolved threads: none (the PR has no review threads; the only Bot output is three issue comments, listed in the validation file).
- cost: n/a

## Revise round 1 (final head `32e7742a8a1fe2ebdae0430853331a01fb11f04f`)

- **Item 3 (P2, write boundary vs. style memory):** commit `32e7742a` adds two things to `home/dot_agents/skills/project-map/SKILL.md`, verbatim from the task file. A new "Writes" bullet after the `.gitignore` exception names the agent's own memory as the other permitted write. The artifact-design precedence sentence goes at the end of the first "The map: index.html" bullet. No other text changed; the validation file pastes the `git diff` of SKILL.md.
- **Item 4 (P3, evidence):** the validation file's "Revise round 1" section pastes the four commands from the task file verbatim. It adds two read-only probes that back the remaining claims: `grep -n -E "NEED_STYLE|style\.md"` on the prototype (lines 27 and 32), and `ls -la` of its memory directory (`MEMORY.md` 88 B, `style.md` 532 B). `~/.claude/**` was not edited.
- **Items 1 and 2:** the orchestrator dispositioned them; no action taken.
- **Regenerated:** `generate-agent-configs.py` rc=0, and only SKILL.md changed. Its symlink template is unchanged. render-check, the validator, both unit modules (168), ruff format (44 files), prettier and `make unit-test` (921, skipped=1) all pass.
- **CI:** all 13 checks pass on `32e7742a`, and the check runs carry that head_sha. Bot: `bot: none` (15-minute wait on `32e7742a` after green CI: 31 iterations, all `rc=0`, empty; no review, inline comment or thread on the PR).
- **Unresolved threads:** none.
- cost: n/a

## Revise round 2 (final head `2e15d4aa1a1696adfe0f05b1ec8f076cfc0cb9a9`)

- **Item 1 (P2, agent body vs. skill write boundary):** commit `2e15d4aa` replaces the last three body lines of `render_claude_project_map_agent()` with the task file's five lines, verbatim. The regenerated `home/dot_claude/agents/project-map.md` carries the same text. The agent body and the skill now name the same three permitted writes: `.project-map/`, the one `.gitignore` line, and the agent's own memory. The validation file pastes the `git diff` and the rendered body.
- **Validation:** generator rc=0; only the generator and the agent file changed. render-check, the validator, both unit modules (168), ruff format (44 files), prettier and `make unit-test` (921, skipped=1) pass. The existing test assertions still hold.
- **CI:** all 13 checks pass on `2e15d4aa`, and every check run carries that head_sha. Bot: `bot: none` (15-minute wait on `2e15d4aa` after green CI: 31 iterations, all `rc=0`, empty; no review, inline comment or thread on the PR).
- **Unresolved threads:** none.
- cost: n/a
