# AGMSG-TASK dotfiles-T111-project-map-subagent-a01

Drafted 2026-10-07 by the orchestrator seat (`claude-remediation-dot`, w1A:p1) from the operator's approved design (chat, 2026-10-07). The operator wants a `project-map` subagent that draws one double-click HTML project map, built strictly with the mechanisms this repository already has: a shared skill under `home/dot_agents/skills/`, a Claude subagent rendered by `scripts/generate-agent-configs.py` exactly like `express-explorer`, a global rule in `home/dot_config/claude/rules/` with its `home/dot_claude/rules/symlink_*.tmpl`, and a `.gitignore` line. No new directory, no new manifest key, no new generator mechanism. The operator also decided that the `review` model profile's Claude side becomes `claude-fable-5-1 / high`. Kind: shared skill prose, a Claude subagent render function, a model profile value, a rule, tests; this touches no `claude.permissions`, `claude.sandbox`, `claude.hooks` block and no settings template, so a Claude seat is allowed. Dispatched to `claude-standard-dot-a005` (worker-c, w1A:p2). If the auto-mode classifier denies any edit as Self-Modification, stop without a diff and send `AGMSG-PONG v1 task_id=dotfiles-T111 status=blocked note=<classifier reason>`; the orchestrator re-routes to a Codex seat.

## Objective

1. **`home/dot_agents/agent-config.yaml`**, `model_profiles.review.claude` only: `{ model: claude-fable-5-1, effort: high }`. Replace the comment `One capability tier above the worker at reduced effort.` with `One capability tier above the worker at full effort (operator decision 2026-10-07).` Leave `review.codex` and every other profile untouched.

2. **`scripts/generate-agent-configs.py`**: add `render_claude_project_map_agent(manifest)` next to `render_claude_express_agent`, and register `outputs[ROOT / "home/dot_claude/agents/project-map.md"] = render_claude_project_map_agent(manifest)` in `expected_outputs()` right after the express-explorer line. The function reads `model_profiles(manifest)["standard"]["claude"]` and returns exactly:

   ```python
   def render_claude_project_map_agent(manifest: dict[str, Any]) -> str:
       standard = model_profiles(manifest)["standard"]["claude"]
       return (
           "---\n"
           "name: project-map\n"
           "description: Draws the project map, one double-click HTML file under .project-map/, with part status, milestones, items left to the next milestone, the suggested next step, and what changed since the last update. Use before a long solo run, after each milestone, and to answer \"どこまで進んだ？\".\n"
           "tools: Read, Glob, Grep, Bash, Write, Edit\n"
           f"model: {standard['model']}\n"
           f"effort: {standard['effort']}\n"
           "memory: user\n"
           "skills:\n"
           "  - project-map\n"
           "  - dataviz\n"
           "  - artifact-design\n"
           "color: cyan\n"
           "---\n"
           "\n"
           f"<!-- {GENERATED_HEADER} -->\n"
           "\n"
           "You draw the project map and nothing else. Follow the preloaded\n"
           "project-map skill exactly: ask for the style once through\n"
           "`STYLE-NEEDED`, write only under `.project-map/` plus the one\n"
           "`.gitignore` line, and end with the short report it specifies.\n"
       )
   ```

   Do not add a required profile, a manifest key, or a body file. Regenerate with `uv run --no-project --with pyyaml scripts/generate-agent-configs.py` so `home/dot_claude/agents/project-map.md`, `home/dot_claude/skills/project-map/symlink_SKILL.md.tmpl` and `home/dot_agents/model-profiles.env` (its `MODEL_PROFILE_REVIEW_CLAUDE_ARGS` line) are the generator's output, never hand-edited.

3. **`home/dot_agents/skills/project-map/SKILL.md`** (new), verbatim:

   ````markdown
   ---
   name: project-map
   description: Draw the project map, one double-click HTML file under .project-map/, showing the project's major parts with their status, milestones, items left to the next milestone, the suggested next step, and what changed since the last update. Use before a long solo run, after each milestone, and to answer "どこまで進んだ？".
   ---

   # Project Map

   You draw one thing: the project map. Nothing else.

   ## Style: ask once, then obey

   - Your MEMORY.md holds `style: dark|light` and `accent: <CSS color>`. If both exist, use them and never ask again.
   - If they are missing, look for a saved dashboard-builder style first: `~/.claude/agents/dashboard-builder.md` and the dashboard-builder memory directory next to yours. If it records a theme and an accent, copy them into your MEMORY.md and use them.
   - If neither exists, do not draw. Reply with exactly one line, `STYLE-NEEDED: dark or light? one accent color?`, and stop. The main session asks the human and re-runs you with `style=... accent=...`. Save those two values to MEMORY.md, then draw.

   ## Writes

   - Write only inside `<repo>/.project-map/`: `index.html` and `state.json`.
   - One exception: when `.gitignore` has no `.project-map/` line, append one.
   - Never touch any other file. Never run a git command that changes state (no add, commit, push, stash, checkout, reset).

   ## Reads

   - README first, then the code layout, then `git log` and `git diff --stat` from the `head` recorded in `state.json` to HEAD.
   - `gh issue list --state open --limit 50` when it works. When `gh` fails or the sandbox blocks it, skip issues and show "issues: unavailable" in the map instead of failing.
   - When `.ua/knowledge-graph.json` exists and `.ua/meta.json` `gitCommitHash` equals HEAD, read that graph for structure before grepping the tree.

   ## state.json

   Keep this file as the memory of the map. Shape:

   ```json
   {
     "updated": "2026-10-07T09:00:00+09:00",
     "head": "8e9bd072",
     "style": { "theme": "dark", "accent": "#5b8def" },
     "milestones": [{ "name": "...", "proposed": true, "parts": ["..."] }],
     "parts": [
       {
         "id": "...",
         "name": "...",
         "status": "done|in-progress|not-started|stuck",
         "waiting_on": "",
         "paths": ["..."],
         "changed": false
       }
     ],
     "decisions": [{ "question": "...", "default": "...", "answer": null }]
   }
   ```

   - Read the previous `state.json` before drawing. The human edits milestone names and decision answers there; never overwrite a human edit, only add to it.
   - `parts[].changed` is true when any of the part's paths changed between the previous `head` and HEAD.

   ## The map: index.html

   - One self-contained HTML file: inline CSS and JS, no external requests, no build step, opens by double-click from `file://`. Theme and accent from memory, both contrast-checked as dataviz describes.
   - Top strip: project name, HEAD short sha and date, **N items left to <next milestone>**, **Suggested next step** in one concrete sentence, and a "changed since <last update>" count.
   - Parts: split the project into 4 to 9 major parts, derived from the directory layout, README, and recent commits, never from a fixed list. Each part shows `done`, `in-progress`, `not-started`, or `stuck`. A stuck part states what it waits on: a person, a decision, an external service, or a failing check. Parts that changed since the last update carry an accent border and a "changed" tag.
   - Milestones: when the human has not named any, read README and the commit history and propose a first version of 3 to 6 milestones, each listing the parts it needs, labelled "proposed, edit me in .project-map/state.json".
   - Decisions panel, "needs your call": every open question with the default you will take when it stays unanswered.
   - Other panels: choose only what this project's evidence supports, such as CI health, open PRs, stuck tasks, or a recent-commit timeline. Drop any panel that would be empty. No templates.

   ## Report back

   End with three to eight lines: the map's path, items left to the next milestone, the suggested next step, the changed parts, and the pending decisions.
   ````

   **`home/dot_agents/skills/project-map/agents/openai.yaml`** (new), verbatim:

   ```yaml
   interface:
     display_name: "Project Map"
     short_description: "Draw the single-file project map under .project-map/"
     default_prompt: "Use $project-map to draw or refresh the project map and report items left to the next milestone and the suggested next step."
   ```

4. **`home/dot_config/claude/rules/project-map.md`** (new), verbatim:

   ```markdown
   ## Project map

   - Before a long solo run (a chain of tasks, waiting on workers, or more than about 30 minutes of unattended work), launch the `project-map` subagent in the background to draw the current version. Update it after every milestone.
   - Run it in the foreground only the first time, when its memory holds no style. When it replies `STYLE-NEEDED`, ask the human with AskUserQuestion for dark or light and one accent color, then re-run it with `style=... accent=...`. Reuse a saved dashboard-builder style when one exists and do not ask again.
   - When the human asks "どこまで進んだ？" or how far the project has come, answer from `.project-map/state.json` and the map. Read them; do not redraw first.
   - Follow the map's suggested next step. Put anything that needs the human's judgement into the map's decisions panel with a default; when no answer arrives, proceed with that default and say so.
   - Existing dashboard rules (such as `/understand-dashboard` in understand-anything.md) stay as they are.
   ```

   **`home/dot_claude/rules/symlink_project-map.md.tmpl`** (new), one line, the same form as the sibling templates:

   ```
   {{ .chezmoi.sourceDir }}/dot_config/claude/rules/project-map.md
   ```

5. **`home/dot_agents/README.md`**: in the generated-outputs list, add `- \`home/dot_claude/agents/project-map.md\`` directly after the `express-explorer.md` line.

6. **`.gitignore`**: append, after the `.crit/` block:

   ```
   # project-map subagent output (one local HTML map and its state)
   .project-map/
   ```

7. **`tests/unit/test_generate_agent_configs.py`**: in the test that asserts the express-explorer output (`agent_path = ... express-explorer.md`), add the same two assertions for `home/dot_claude/agents/project-map.md` against the sample manifest's `standard` profile (`model:` and `effort:` lines), plus one assertion that the output contains `  - project-map\n`. The orchestrator's grep found no test pinning the `review` profile's old Claude value (`tests/unit/test_generate_agent_configs.py:591` pins the `security` fixture, not `review`); if a test still fails because of the manifest change, update only that assertion and say so in the report.

Forbidden: any other file; `make update`; `make upgrade`; editing `~/.claude/**` directly; thread resolution; a new `model_profiles` entry; a new manifest key; hand edits to generated files.

[memory:decision] dotfiles-T111 (operator 2026-10-07): the project-map subagent is built only from existing mechanisms: a shared skill `home/dot_agents/skills/project-map/`, a generator-rendered `home/dot_claude/agents/project-map.md` that borrows `model_profiles.standard` (no new profile), a rule `home/dot_config/claude/rules/project-map.md` with its symlink template, and a `.project-map/` gitignore line.
[memory:decision] dotfiles-T111 (operator 2026-10-07): `model_profiles.review.claude` is `claude-fable-5-1 / high`; the three roles (deep, standard, audit) are unchanged.

## Repo / branch

worker-c; `git fetch origin`; `git switch -c feat/project-map-subagent --no-track origin/main` (main at 8e9bd072 or later).

## Allowed files

`home/dot_agents/agent-config.yaml` (the `review.claude` line and its comment only), `scripts/generate-agent-configs.py`, `tests/unit/test_generate_agent_configs.py`, `home/dot_agents/skills/project-map/SKILL.md`, `home/dot_agents/skills/project-map/agents/openai.yaml`, `home/dot_config/claude/rules/project-map.md`, `home/dot_claude/rules/symlink_project-map.md.tmpl`, `home/dot_agents/README.md` (one line), `.gitignore` (two lines), and the generator's own outputs `home/dot_claude/agents/project-map.md`, `home/dot_claude/skills/project-map/symlink_SKILL.md.tmpl`, `home/dot_agents/model-profiles.env`. Artifacts at the standard seven `dotfiles-T111-project-map-subagent-a01` paths in the main checkout (Claude seat, through the permission gate), masked.

## Validation commands (paste verbatim output, whole)

```
uv run --no-project --with pyyaml scripts/generate-agent-configs.py; echo "rc=$?"
make render-check; echo "rc=$?"
uv run --no-project --with pyyaml scripts/validate-agent-assets.py; echo "rc=$?"
uv run --no-project python -m unittest tests.unit.test_generate_agent_configs tests.unit.test_validate_agent_assets 2>&1 | tail -3
make unit-test 2>&1 | tail -3
mise x node npm:prettier -- prettier --check home/dot_agents/README.md home/dot_agents/skills/project-map/SKILL.md home/dot_config/claude/rules/project-map.md home/dot_agents/skills/project-map/agents/openai.yaml 2>&1 | tail -2
git diff --stat origin/main
grep -n "REVIEW_CLAUDE_ARGS" home/dot_agents/model-profiles.env
gh pr checks <pr>
```

## Completion

PR to `main` (English title and body, attribution footer), CI green, Bot wait per the SKILL, artifacts, the CompactionDB `memory add` of both decision lines, then `AGMSG-RESULT v1 task_id=dotfiles-T111` via `agmsg-dispatch dotfiles claude-standard-dot-a005 claude-remediation-dot w1A:p1 "<single line>"`. max_turns=12.

## Revise round 1 (orchestrator, 2026-10-06 23:47Z) — audit of 0c1d280b: `incorrect` (3 P2, 1 P3; two are dispositioned by the orchestrator, no action for you)

1. (Orchestrator's, no action for you.) **Allowed-files boundary (P2, `home/dot_claude/skills/project-map/agents/symlink_openai.yaml.tmpl:1`).** The generator mirrors every file of a shared skill, so this template is the generator's output of the allowed `agents/openai.yaml`. **Allowed files amendment:** `home/dot_claude/skills/project-map/agents/symlink_openai.yaml.tmpl` is an allowed generator output of this task. Dispositioned `not-applicable` in the acceptance record.
2. (Orchestrator's, no action for you.) **Preloaded skills (P2, `home/dot_claude/agents/project-map.md:10`).** `dataviz` and `artifact-design` are Claude Code bundled skills, not repository files. The orchestrator ran the installed `project-map` agent in a diagnostic turn (2026-10-07 08:5xZ JST): both skills were present in its context, loaded from `/tmp/claude-1000/bundled-skills/2.1.292/…/dataviz` and the bundled `artifact-design`. Dispositioned `not-applicable` with that evidence.
3. **Write boundary vs. style memory (P2, `home/dot_agents/skills/project-map/SKILL.md:17`).** The "Writes" section forbids every write outside `.project-map/`, while "Style" requires saving `style`/`accent` to MEMORY.md. Add one bullet to "Writes", after the `.gitignore` exception: `- Your own agent memory (MEMORY.md and the files beside it, outside the repository) is the other permitted write; nothing else.` Also add, at the end of the "The map: index.html" first bullet, the sentence: `The map is a local file, not a published Artifact: where artifact-design's page contract (CDN libraries, Google Fonts, no html/head/body tags) conflicts with this skill, this skill wins.` (The diagnostic run above showed artifact-design's contract contradicting the offline single-file requirement.) No other text changes.
4. **Evidence (P3, report `:29`).** The report's claims about the host prototype (`~/.claude/agents/project-map.md` size and date, its `effort: medium`, `NEED_STYLE`, `frontend-design` preload, `style.md` memory shape) and the PR-body disclosure have no pasted output. Append to the validation file the verbatim output of: `stat -c '%s %y' ~/.claude/agents/project-map.md`; `sed -n '1,12p' ~/.claude/agents/project-map.md`; `cat ~/.claude/agent-memory/project-map/MEMORY.md`; `gh pr view 299 --json body --jq .body | grep -n -i prototype`. Read-only; `~/.claude/**` stays unedited.

Then regenerate (`uv run --no-project --with pyyaml scripts/generate-agent-configs.py`; the symlink template content does not change), rerun the validation commands, push, CI, Bot wait on the final head, `AGMSG-RESULT v1 … round=1`. No `make update`.

## Revise round 2 (orchestrator, 2026-10-07 00:23Z) — audit of 32e7742a: `incorrect` (1 P2)

1. **Agent body vs. skill write boundary (P2, `scripts/generate-agent-configs.py:1322`).** The rendered agent body still says `write only under .project-map/ plus the one .gitignore line`, which contradicts the skill's new memory-write bullet. In `render_claude_project_map_agent()` replace the last three body lines so the body reads exactly:

   ```
   You draw the project map and nothing else. Follow the preloaded
   project-map skill exactly: ask for the style once through
   `STYLE-NEEDED`, write only under `.project-map/`, the one
   `.gitignore` line and your own agent memory, and end with the
   short report it specifies.
   ```

   Regenerate so `home/dot_claude/agents/project-map.md` carries the same text; the test's existing assertions still hold. **Boundary:** with this, the agent body and the skill name the same three permitted writes; no further decomposition is requested.

Then rerun the validation commands (ruff format check included), push, CI, Bot wait on the final head, `AGMSG-RESULT v1 … round=2`. No `make update`.
