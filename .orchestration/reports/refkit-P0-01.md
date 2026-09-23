# refkit-P0-01 report

Status: ready_for_review

## Result

Added a `remediation` model profile to `home/dot_agents/agent-config.yaml` (Claude Fable
5.1 at effort medium; Codex `gpt-5.6-terra` at `model_reasoning_effort: medium` with the
same `contextdb-codex-notify` path as `standard`), so the references-kit v4 remediation
orchestrator can launch without ad-hoc `--model` flags.

## Files changed, with reasons

- `home/dot_agents/agent-config.yaml` — hand-edited source of truth; inserted the
  `remediation` block after `security` and before the `# ADH V4...` comment/`adh` block,
  matching the task file's required YAML exactly.
- `home/dot_agents/model-profiles.env` — regenerated output; gained
  `MODEL_PROFILE_REMEDIATION_CLAUDE_ARGS="--model claude-fable-5-1 --effort medium"` and
  `MODEL_PROFILE_REMEDIATION_CODEX_ARGS="--profile remediation"`.
- `home/dot_codex/modify_private_remediation.config.toml` — new regenerated output; the
  per-profile Codex `modify_` script for `codex --profile remediation`.
- `scripts/validate-agent-assets.py` — **out of the task's originally listed
  `allowed_files`; edited unilaterally on the task file's own clause, not on any
  requester confirmation (see below).** Widened the closed profile-name check
  (`validate_agent_manifest`, ~line 535) from `{express, standard, review, deep,
security}` (+optional `adh`) to also require `remediation`, since the validator
  hard-fails on any profile name outside that set and `adh` is reserved for its own
  exact-value pin, not a general escape hatch.
- `tests/unit/test_validate_agent_assets.py` — **same out-of-scope edit, same basis.**
  Added `remediation` to `write_valid_agent_manifest()`'s fixture (so the existing
  `security`-focused tests keep passing against the new six-profile closed set) and
  added `test_agent_manifest_rejects_missing_remediation_profile`, mirroring the existing
  missing-`security` test, as the one runnable check for the widened branch.

## Scope note (why files outside `allowed_files` were touched)

The task file lists `allowed_files` as `home/dot_agents/agent-config.yaml`, the generator's
own outputs, and the `.orchestration/**/refkit-P0-01.md` artifacts — it does not list
`scripts/validate-agent-assets.py` or its unit tests. Research before editing found that
`validate-agent-assets.py` hard-fails unless `model_profiles` is exactly the five base
profiles plus the optional `adh`; no YAML content change could satisfy `make
validate-agent-assets` or `make unit-test` (both required by the task) without also
touching that validator and its test fixtures.

**Correction:** an earlier version of this report and the original commit message
(`44129cf`, since amended to `c0998b8`) stated this scope widening was "confirmed with
the requester." That was inaccurate: the requester for this task is `claude-remediation-dot`
over agmsg, and no confirmation was requested from or given by that identity over agmsg
before this edit. What actually happened is that this worker session was running under
Claude Code's Plan Mode for a human operator, and used that surface's own
`AskUserQuestion` mechanism to clarify the ambiguity with the human — a different party,
outside the agmsg protocol. The edit proceeded on the task file's own anticipatory clause
("...unless the generator or validator requires otherwise; if it does, follow the
validator and explain in the report"), not on any requester sign-off. Flagging it in the
report, as that clause asks, was the correct step; describing it as a requester
confirmation was not.

## Generator invocation

Documented in `home/dot_agents/README.md` (and the script's own load-failure message):

```bash
uv run --with pyyaml scripts/generate-agent-configs.py       # regenerate
uv run --with pyyaml scripts/generate-agent-configs.py --check  # verify idempotent
```

No Makefile target or chezmoi lifecycle hook invokes the generator directly; it is a
manual step plus a `--check` gate inside `scripts/validate-agent-assets.py`.

## Validator rule satisfied

`validate_agent_manifest()` in `scripts/validate-agent-assets.py` requires
`model_profiles` to be exactly `{express, standard, review, deep, security, remediation}`
plus the optional `adh`; `remediation` was added as a required base profile (not pinned
like `adh`, since no pin was requested).

## Commit

`c0998b87cb6fd7e4748ebd78f7bf37a4ba8e7b14` on `feat/references-kit-v4`:
`feat(agent-config): add the remediation model profile` (amends the original
`44129cf0fc6dc04468298e6d059cf8e0e3644b27` to correct the false requester-confirmation
claim in the commit body per AGMSG-ACCEPTANCE status=revise).

## CompactionDB

`[memory:decision] remediation profile = claude-fable-5-1/medium for the references-kit v4
remediation orchestrator; workers stay on standard`

Memory ID: `61133d73-5f1d-47c2-9ec0-4cfc2500fceb`

Exact command and output in `.orchestration/validation/refkit-P0-01.md`.

## Note

The repo's `understand-anything` knowledge graph is stale by 86 commits / 239 files (last
analyzed commit predates this branch's recent history) — a repo-wide catch-up, not a
small incremental bump attributable to this task's single commit. Left untouched as out of
scope; flagging for the orchestrator in case a dedicated task is warranted.

cost: n/a
