# T80 validation

## Clause inventory and mapping

Source: pre-edit `home/dot_config/codex/AGENTS.md` at `HEAD`. Compound bullets
are split into independently actionable clauses. `kept` means the clause
remains in the always-on file; `moved` means its complete substance is in the
named on-demand section; `duplicate-of` names the canonical clause/location.

| ID | Pre-edit clause | Disposition |
|---|---|---|
| C001 | Ask questions needed to propose the best solution from user input. | kept — `AGENTS.md` § ユーザーへの質問 |
| C002 | Read `learn_index.md` before starting work. | kept — `AGENTS.md` § セッション開始時の learn 確認 |
| C003 | Read relevant learn files before work. | kept — same section |
| C004 | Apply prior error/failure lessons during work. | kept — same section |
| C005 | At a natural stopping point with no immediate next action, emit a one-line summary. | kept — `AGENTS.md` § セッション終了時のまとめ |
| C006 | Use the exact `📝 まとめ:` content contract. | kept — same section |
| C007 | Project structure varies by programming language. | moved — `agmsg-orchestration` § Codex worker worklogs, opening sentence |
| C008 | Create the worklog structure only when absent. | moved — same section, opening sentence |
| C009 | Keep plan and todo current throughout work. | kept — `AGENTS.md` § プロジェクトの構成について |
| C010 | Do not commit plan/todo/learn files. | kept — same section |
| C011 | Store plans under `.agents/worklog/codex/plan/`. | moved — skill § Codex worker worklogs, plan bullet |
| C012 | Name plans `<YYYYMMDD_HHMMSS>_plan.md`. | moved — same bullet plus opening timestamp rule |
| C013 | Write the plan before implementation. | moved — same bullet |
| C014 | Ask the user questions when needed. | moved — same bullet |
| C015 | Update the plan after those questions. | moved — same bullet |
| C016 | Store todos under `.agents/worklog/codex/todo/`. | moved — skill § Codex worker worklogs, todo bullet |
| C017 | Name todos `<YYYYMMDD_HHMMSS>_todo.md`. | moved — same bullet plus opening timestamp rule |
| C018 | Derive todo tasks from the plan. | moved — same bullet |
| C019 | Move completed tasks to Done. | moved — same bullet |
| C020 | Rename an all-done todo to `<timestamp>_done.md`. | moved — same bullet |
| C021 | Update the plan when task completion changes it. | moved — skill § Codex worker worklogs, plan bullet |
| C022 | Store learns under `.agents/worklog/codex/learn/`. | moved — skill § Codex worker worklogs, learn bullet |
| C023 | Name learns `<YYYYMMDD_HHMMSS>_learn.md`. | moved — same bullet plus opening timestamp rule |
| C024 | Record knowledge or techniques needed for implementation. | moved — same bullet (`reusable, validated knowledge`) |
| C025 | Reflect learned material in the plan when needed. | moved — same bullet |
| C026 | Update learn only for information that speeds future decisions. | moved — same bullet |
| C027 | A learn states what was learned. | moved — same bullet |
| C028 | A learn states where it applies. | moved — same bullet |
| C029 | Update plan Assumptions/Design/Tests when a learn warrants it. | moved — same bullet |
| C030 | Maintain `.agents/worklog/codex/learn/learn_index.md`. | moved — same bullet |
| C031 | Update the index whenever a learn file changes. | moved — same bullet |
| C032 | Use one `- [title](filename) — summary` line of at most 150 characters per index entry. | moved — same bullet |
| C033 | Worklog files require their type-specific minimum headings. | moved — skill § Codex worker worklogs, three file bullets |
| C034 | Plan headings are Goal, Scope, Assumptions, Design, Tests, Open Questions. | moved — plan bullet |
| C035 | Todo headings are TODO and Done. | moved — todo bullet |
| C036 | Learn headings are Date, Learnings, Plan Updates. | moved — learn bullet |
| C037 | Every plan/todo/learn starts with YAML frontmatter. | moved — skill § Codex worker worklogs, frontmatter paragraph |
| C038 | The active constraint applies per owner, not repository-wide. | kept — `AGENTS.md` § プロジェクトの構成について |
| C039 | Common `type` is plan, todo, or learn. | moved — skill § Codex worker worklogs, frontmatter paragraph |
| C040 | Common `id` is `YYYYMMDD_HHMMSS`. | moved — same paragraph |
| C041 | Common `owner` is required. | moved — same paragraph |
| C042 | Common `created_at` is ISO8601. | moved — same paragraph |
| C043 | Common `updated_at` is ISO8601. | moved — same paragraph |
| C044 | Todo requires status, workstream, and related_plan. | moved — skill § Codex worker worklogs, todo frontmatter bullet |
| C045 | Plan requires status. | moved — plan frontmatter bullet |
| C046 | Learn requires validated and apply_to. | moved — learn frontmatter bullet |
| C047 | Todo statuses are active, blocked, done, superseded. | moved — todo frontmatter bullet |
| C048 | Plan statuses are draft, active, done, superseded. | moved — plan frontmatter bullet |
| C049 | Learn validated is true or false. | moved — learn frontmatter bullet |
| C050 | Optional depends_on is an array of todo IDs. | moved — skill § Codex worker worklogs, optional frontmatter paragraph |
| C051 | Optional blocked_reason explains blocked status. | moved — same paragraph |
| C052 | Optional evidence is an array of paths. | moved — same paragraph |
| C053 | Optional tags carries arbitrary tags. | moved — same paragraph |
| C054 | A new todo must set owner. | duplicate-of C041 — canonical skill frontmatter paragraph |
| C055 | Each owner may have at most one active todo. | duplicate-of C038 — canonical always-on core |
| C056 | When TODO is empty, set status to done. | moved — skill § Codex worker worklogs, todo bullet |
| C057 | When TODO is empty, rename the file to `*_done.md`. | moved — same bullet |
| C058 | Create learns only when reusable. | moved — skill § Codex worker worklogs, learn frontmatter bullet |
| C059 | Create learns only when validated true. | moved — same bullet |
| C060 | Learn apply_to identifies plan/tests reflection targets. | moved — same bullet |
| C061 | Do not fear errors during initial coding. | kept — `AGENTS.md` § コーディング全般について |
| C062 | Initial code need not prioritize exception handling. | kept — same section |
| C063 | Final deliverables need not add exception handling. | kept — same section |
| C064 | R&D work need not preserve backward compatibility. | kept — same section |
| C065 | Write tests before implementation. | kept — same section |
| C066 | Refactor after tests pass when needed. | kept — same section |
| C067 | Prefer Codex native review surfaces or retrieved Crit data for review work. | kept — `AGENTS.md` § Crit レビュー運用 |
| C068 | Use browser Crit only when explicitly requested or Crit data is unavailable. | kept — same section |
| C069 | Respect a triggered Crit Plan Mode Stop hook. | kept — same section |
| C070 | Do not bypass that hook unless `CRIT_PLAN_REVIEW=off` is explicit. | kept — same section |
| C071 | Run `make require-crit-review` before completion when a git diff exists. | kept — same section |
| C072 | Require review only for meaningful lifecycle/hooks/plugins/permissions/scripts/broad changes. | kept — same section |
| C073 | When the gate requires review, do not open browser Crit by default. | kept — same section |
| C074 | Locate the review with `crit status --json`. | kept — same section |
| C075 | Save `crit comments --all --json` under repo-local worklog. | kept — same section |
| C076 | Read and judge the retrieved Crit findings. | kept — same section |
| C077 | Agent evidence needs at least one resolved record. | kept — same section |
| C078 | For a finding-free review, add and resolve a review-scope approval. | kept — same section |
| C079 | Local Crit evidence is process evidence. | kept — same section |
| C080 | Local Crit evidence does not authenticate the reviewer. | kept — same section |
| C081 | Receipt includes review_surface, reviewer, review_source, review_outcome. | kept — same section |
| C082 | Rerun with `AGENT_REVIEWED=1 REVIEW_EVIDENCE=<receipt>`. | kept — same section |
| C083 | Bare `AGENT_REVIEWED=1` without retrieved JSON is forbidden. | kept — same section |
| C084 | Browser Crit is permitted only on explicit request or unavailable Crit data. | duplicate-of C068 — canonical same section |
| C085 | For browser review, show the localhost URL to the user. | kept — same section |
| C086 | Tell the user to click Finish Review. | kept — same section |
| C087 | After browser completion, write a receipt. | kept — same section |
| C088 | Rerun with `CRIT_REVIEWED=1 REVIEW_EVIDENCE=<receipt>`. | kept — same section |
| C089 | Use `CRIT_REVIEW=off` only when the user explicitly disables review. | kept — same section |
| C090 | `agent-config.yaml` model_profiles is the source of truth. | kept — `AGENTS.md` § モデル選択 |
| C091 | Profiles generate Codex config and model-profiles.env. | kept — same section |
| C092 | Change interactive models in the manifest, not launchers/rules. | kept — same section |
| C093 | Only the permgate classifier model is separately fixed by security policy. | kept — same section |
| C094 | Use standard for ordinary implementation/debugging. | kept — same section |
| C095 | Use express for read/search/extraction-only work. | kept — same section |
| C096 | Use review for independent review. | kept — same section |
| C097 | Use security for security-review/permgate/redaction/secrets/trust-boundary audits. | kept — same section |
| C098 | Use deep only for cross-cutting design or unknown non-audit failures. | kept — same section |
| C099 | Return to standard after the difficult portion. | kept — same section |
| C100 | Do not switch models during a session. | kept — same section |
| C101 | Evaluate PermissionRequest deterministic-first. | kept — same section |
| C102 | Fail closed to Codex native confirmation on unknown/failure. | kept — same section |
| C103 | Claude and Codex use their official CLIs and existing auth. | kept — same section |
| C104 | Send only normalized action metadata to classifiers. | kept — same section |
| C105 | Keep both providers in shadow mode. | kept — same section |
| C106 | Enable only a provider meeting success, p50/p95, and human-evaluation thresholds. | kept — same section |
| C107 | Use Ponytail when available for coding. | kept — `AGENTS.md` § Ponytail |
| C108 | Prefer YAGNI. | kept — same section |
| C109 | Prefer stdlib/native platform first. | kept — same section |
| C110 | Prefer existing implementation reuse. | kept — same section |
| C111 | Prefer the smallest correct diff. | kept — same section |
| C112 | Ponytail does not mean merely shorter. | kept — same section |
| C113 | Do not simplify trust-boundary input validation. | kept — same section |
| C114 | Do not simplify data-loss prevention. | kept — same section |
| C115 | Do not simplify security. | kept — same section |
| C116 | Do not simplify accessibility. | kept — same section |
| C117 | Do not simplify explicit requirements. | kept — same section |
| C118 | After first Codex install/update, open `/hooks`. | kept — same section |
| C119 | Review and trust Ponytail lifecycle hooks. | kept — same section |
| C120 | Start a new thread after that trust step. | kept — same section |
| C121 | Use upstream default Ponytail mode `full`. | kept — same section |
| C122 | Override mode only when needed via env or Ponytail command. | kept — same section |
| C123 | Use Understand-Anything for repository graph generation/reference when available. | kept — `AGENTS.md` § Understand-Anything |
| C124 | Invoke it in Codex as `$understand`, not `/understand`. | kept — same section |
| C125 | Initial full analysis is token-heavy. | kept — same section |
| C126 | Incremental analysis is lightweight. | kept — same section |
| C127 | Understand-Anything outputs under `.ua/`. | kept — same section |
| C128 | Do not commit `.ua/intermediate/`. | kept — same section |
| C129 | Do not commit `.ua/diff-overlay.json`. | kept — same section |
| C130 | Add those exclusions to `.gitignore`. | kept — same section |
| C131 | Commit the remaining `.ua/` output. | kept — same section |
| C132 | Before whole-repo exploration/symbol search, consult graph summaries/filePath when present. | kept — same section |
| C133 | Compare graph meta gitCommitHash with HEAD. | kept — same section |
| C134 | Fall back to grep when the graph is stale or absent. | kept — same section |
| C135 | The installer symlinks skills into `~/.agents/skills`. | kept — same section |
| C136 | Restart the CLI after installation/update. | kept — same section |
| C137 | Standard/deep turns auto-record to project CompactionDB when installed. | kept — `AGENTS.md` § CompactionDB |
| C138 | Explicitly record durable decisions with `memory add`. | kept — same section |
| C139 | Use Crit only for the agent's own review. | kept — final Crit policy bullets |
| C140 | Use Crit CLI to create/reply/resolve comments. | kept — same bullets |
| C141 | Save Crit JSON evidence under `.orchestration/` or `.agents/worklog/`. | kept — same bullets |
| C142 | Do not open browser Crit to request human review. | kept — same bullets |
| C143 | The browser/human-review prohibition is the 2026-07-18 operator directive. | kept — same bullets |

Inventory result: **143 clauses; 91 kept, 49 moved, 3 duplicate-of, 0
unmapped, 0 deleted.** The three duplicates retain one canonical copy each.

## Token measurement

T77 method: count every non-ASCII character as Japanese at 1.7 chars/token,
every ASCII character at 4 chars/token, and sum the two estimates. This is a
comparative estimate with the same approximately ±20% caveat as T77.

| State | Characters | Non-ASCII | ASCII | Estimated tokens |
|---|---:|---:|---:|---:|
| before (`HEAD`) | 7,180 | 2,893 | 4,287 | 2,773.51 |
| after | 4,726 | 1,985 | 2,741 | 1,852.90 |

Reduction: **920.62 estimated tokens (33.19%)** from the always-injected file.

## Plan-quality gate

- Manual checklist: passed.
- Validator / Make target: unavailable.
- Hook: unavailable.
- Subagent definition: unavailable.
- CI entrypoint: unavailable.
- Required command could not be run because
  `scripts/validate_plan_quality.py` is absent:
  `uv run python scripts/validate_plan_quality.py .agents/worklog/codex/plan/20260817_165353_plan.md`.

## Command validation

| Command | Result |
|---|---|
| `make format` | PASS — `shfmt --indent 4 --space-redirects --diff .` produced no diff |
| `env UV_CACHE_DIR=/private/tmp/t80-uv-cache uv run python -m unittest discover -s tests/unit -p 'test_*.py' -q` | PASS — 336 tests in 29.316s |
| `git diff --check` | PASS |
| clause-map continuity/count assertions | PASS — rows=143, unmapped=0 |
| T77 token assertion | PASS — before=2773.51, after=1852.90 |
| `env UV_CACHE_DIR=/private/tmp/t80-uv-cache make validate-agent-assets` | Initial sandbox attempt could not resolve `pypi.org` while fetching PyYAML; no source failure |
| `env UV_CACHE_DIR=/private/tmp/t80-uv-cache uv run --with pyyaml scripts/validate-agent-assets.py` | PASS after approved network retry — `agent asset validation ok` |
| `make require-crit-review` | Expected initial block — meaningful shared skill/broad diff requires evidence |
| `env AGENT_REVIEWED=1 REVIEW_EVIDENCE=.agents/worklog/codex/review/T80-receipt.md make require-crit-review` | PASS — repo-local resolved Crit record `r_65f934` |

The unit output includes four deliberate `ERROR:` lines emitted by negative
model-profile fixtures; the unittest process completed `OK` with exit 0.
