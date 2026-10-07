# Learning: dotfiles-T111-project-map-subagent-a01

- **A new shared skill file always brings a generated Claude symlink of its own.** `claude_skill_symlink_outputs()` (`scripts/generate-agent-configs.py:557`) mirrors every non-dot file under `home/dot_agents/skills/`, so `agents/openai.yaml` also generated `home/dot_claude/skills/project-map/agents/symlink_openai.yaml.tmpl`, and `make render-check` fails without it. A task that adds skill files should list the full mirrored set in `allowed_files`. [memory:failure] A skill task's allowed_files that names only `symlink_SKILL.md.tmpl` misses the generator's `agents/symlink_openai.yaml.tmpl` output.
- **`agmsg-dispatch` still ran inside the sandbox on the first try in this seat** (as in T110), despite the SKILL saying `excludedCommands` takes it out. Sending it with `dangerouslyDisableSandbox` from the start avoids a failed first send.
- **Run the CI ruff check locally before the first push of any Python edit.** CI's "Check Python and Markdown formatting" runs `git ls-files -z '*.py' | xargs -0 ruff format --config ruff.toml --check` (the `make format` line), which the task's validation list does not include. ruff format prefers single quotes for a literal that contains `"`, so a verbatim task snippet with `\"` escapes fails CI. [memory:failure] A Python snippet with `\"` escapes copied verbatim from a task file fails CI's ruff format check; run `mise x ruff -- ruff format --config ruff.toml --check` before pushing.
- **Sandboxed and unsandboxed Bash see different `$TMPDIR` values** (`/tmp/claude-1000` versus `/tmp`), so a file one writes under `$TMPDIR` is not where the other looks. Use an absolute scratchpad path for files shared between them.
- No rule candidate is promoted; the first point is for the orchestrator's task authoring (Orchestrator Playbook step 3, grounding `allowed_files`).

## Revise round 1

- **Check a new skill's "Writes" fence against every other section that asks for a write.** Here the fence forbade all writes outside `.project-map/`, while the "Style" section required a memory save. An exclusive "only X" sentence needs every permitted exception listed beside it.
- **Paste the read that backs every claim about host state, even a read-only one,** in the validation file at the time of the claim. A report sentence about `~/.claude/...` without its `stat`/`sed`/`grep` output counts as unexecuted.
- **After a short lead-in, `gh pr checks --watch` can return on the previous head's runs.** Confirm with `gh api repos/{owner}/{repo}/commits/<sha>/check-runs` that every run carries the new `head_sha`.

## Revise round 2

- **A boundary stated in a skill is often restated in the agent body or rule that loads it.** When a fix widens a skill's permitted writes, grep every rendered restatement too (`grep -rn "write only" home/ scripts/`) and change them in the same commit.
