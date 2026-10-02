# AGMSG-TASK dot-ua-refresh-policy-T52-a01

Drafted 2026-10-02 from the T51 blocked investigation (operator decision:
defer and codify). Worker-c (`claude-standard-dot-a005`), branch
`chore/ua-refresh-policy` from `origin/main` (ef9e5be or later). Verify the
dispatched task_rev sha256 against this file; else stop and PONG blocked.

## Objective

Under Understand-Anything 2.9.7 an incremental graph update that re-analyzes
a file without a deterministic parser — here the extension-less shell
scripts `home/dot_local/bin/common/executable_herdr-agents` and
`executable_agmsg-dispatch`, and the Python chezmoi script
`home/dot_claude/modify_private_settings.json` — always blocks publication
(`validate-incremental-symbols.mjs` marks every unowned callable `unknown`;
no per-path language override; T51 report and validation). `herdr-agents`
changes in nearly every task, so the incremental path never succeeds here,
and every `.ua` commit since b277a51 was a full rebuild. The operator decided
(2026-10-02): the graph stays stale between operator-requested **full
rebuilds** at regime boundaries, and the per-commit auto-update prompting
stops.

Codify that in the repository:

1. `.ua/config.json`: `"autoUpdate": false` (reverses the T40-UA setting; the
   SessionStart/PostToolUse "graph is stale, you MUST update it" prompts
   stop). Verify with the plugin hook source or `--help` which flag the hooks
   read, and paste the check; if `autoUpdate: false` does not silence the
   SessionStart staleness line, say so and leave that line (it is harmless).
2. `home/dot_config/claude/rules/understand-anything.md`: replace "Re-runs
   are incremental and cheap" with the truth for this repository: incremental
   updates block on parser-less files (name them and the plugin limitation);
   a refresh is `/understand --full` run by a worker task **only when the
   operator asks for it** at a regime boundary; between refreshes the graph
   is stale by design and the search-first bullet's freshness check already
   routes to grep. Keep the acceptance gate bullet (`ua-symbol-coverage`
   table; for a full rebuild `--old-ref` is the previous `meta.gitCommitHash`).
3. `home/dot_config/codex/AGENTS.md` Understand-Anything section: the same
   change in Japanese, same facts.
4. `README.md` Understand-Anything paragraph(s): the same facts; keep the
   `.ua/` commit/ignore guidance.
5. `home/dot_agents/skills/agmsg-orchestration/SKILL.md` and
   `home/dot_agents/agent-config.yaml` (express-explorer prompt text,
   rendered by `scripts/generate-agent-configs.py`): touch only if they
   state that re-runs are incremental or that the hook's update instruction
   must be executed; the freshness-check wording stays. Run the generator
   and `make render-check` after any manifest change.
6. `[memory:decision]` T52: this repository refreshes `.ua/` only by
   operator-requested full rebuild at a regime boundary; incremental UA
   updates block on parser-less shell/chezmoi scripts; `autoUpdate` is off
   (operator 2026-10-02).

## Allowed files

- `.ua/config.json`
- `home/dot_config/claude/rules/understand-anything.md`, `home/dot_config/codex/AGENTS.md`, `README.md`
- Only if they carry the wording: `home/dot_agents/skills/agmsg-orchestration/SKILL.md`,
  `home/dot_agents/agent-config.yaml`, and the files `scripts/generate-agent-configs.py`
  renders from it (list them in the report).
- `.orchestration/{reports,validation,sandboxes,learning,autoskill/runs}/dot-ua-refresh-policy-T52-a01.md`
- `.agents/worklog/**` waived.

## Forbidden actions

Any graph analysis (`/understand`, incremental or full); editing
`.ua/knowledge-graph.json`, `fingerprints.json`, `meta.json`; editing the
plugin cache; source/test changes outside the files above; the T51 branch;
`.orchestration/acceptance/**`; merge; force-push; `--delete-branch`; local
`bats`; `make update`/`upgrade`.

## Validation (verbatim output)

The hook-flag check from item 1, `make render-check`, `make unit-test`,
`make validate-agent-assets`, `git diff --stat origin/main`, `gh pr view <n>
--json url,headRefOid,mergeStateStatus`, `gh pr checks <n>`, and the
CompactionDB `memory add --kind decision --scope project` command.

## Completion

English PR to `main`, CI green on Linux and macOS, artifacts at the expected
paths, `AGMSG-RESULT v1` with `cost:` in the report. max_turns=30.
