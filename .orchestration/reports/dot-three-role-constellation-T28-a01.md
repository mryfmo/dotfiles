# T28 report — dot-three-role-constellation-T28-a01

- worker: `claude-standard-dot-a005` (Claude Code, acting as worker per dispatch note)
- orchestrator: `claude-remediation-dot`
- worktree: `~/Workspace/dotfiles/.claude/worktrees/worker-c`
- branch: `feat/three-role-constellation` (base `origin/main` = `eb3cd4b`)
- task_rev: sha256 `df1c6d1a4d7a283e7e2e4fcb350a8b08aee2ade997761421198b0e0c3757e7c2`
  verified against the task file at `eb3cd4b` (see validation file)
- PR: https://github.com/mryfmo/dotfiles/pull/190, head `290e9bc2a7265108fc30518be78907aa63fc083c`
- status: ready_for_review; CI green on head 290e9bc (all checks pass, nix skipping; verbatim in validation file)

## Changes

1. `home/dot_agents/agent-config.yaml`
   - `deep.claude` → `{ model: claude-fable-5-1, effort: high, advisor: fable }`.
   - New `audit` profile after `security`, as specified. The one difference from
     the task snippet: `notify` uses the file's existing single-quoted flow-list
     style. The value is identical.
   - worker_kind, worker_profile, interactive_profile and the
     express/standard/review/security/adh values are untouched.
2. `scripts/generate-agent-configs.py`
   - New `CODEX_SANDBOX_MODES = ("read-only", "workspace-write", "danger-full-access")`.
     These values come from `codex --help` `-s/--sandbox` possible values.
   - `model_profiles()` fails when `codex.sandbox_mode` is set to any other value.
     The message is `model profile <name>.codex.sandbox_mode must be one of ...`.
   - `render_codex_profile()` emits `sandbox_mode = "<mode>"` only when the
     profile sets it. The profile file is a `--profile` layer over the base
     config, so every other profile inherits the global `workspace-write`. The
     base `codex-config-managed.toml` is unchanged; no template change was needed.
3. `scripts/validate-agent-assets.py`
   - `audit` joins the required base profile set. The message now reads "six
     base profiles and only the optional adh profile".
   - An operator-pin loop checks `codex.model == gpt-6-astra`,
     `model_reasoning_effort == high` and `sandbox_mode == read-only`. Each
     failure message names the key, the expected value and the actual value.
   - `validate_codex_profile_modify_scripts` now requires each rendered profile's
     `sandbox_mode` to equal the manifest's value, including absence. This is the
     schema acceptance for the optional per-profile key; no other schema check
     rejected extra keys.
4. `AGENTS.md`: new `## Audit` section (20 lines). It has the coverage list, the
   P0–P3/confidence/file:line/verdict format, the rule that a finding-free audit
   still records an approval, the untrusted-content rule, and the statement that
   acceptance is orchestrator-only.
5. Rules and skill:
   - `model-selection.md`: the constellation sentence is added to the manifest
     bullet. The review bullet is reconciled so the `review` profile covers plan
     and document reviews and code-changeset audit is the `audit` lane, with no
     overlap.
   - `agmsg-orchestration.md`: one audit bullet after the adversarial-review
     bullet.
   - `agmsg-orchestration/SKILL.md`: one carve-out clause for
     orchestrator-invoked read-only `codex --profile audit review`.
6. `README.md`: one paragraph after the model_profiles paragraph. It names the
   three roles, their profiles and models, and where the boundaries are
   documented.
7. Generated output. `--check` is clean, and only the expected files changed:
   - `home/.chezmoitemplates/claude-settings-managed.json`: `"model"` changed
     from `claude-fable-5` to `claude-fable-5-1`. `effortLevel` stays high and
     `advisorModel` stays `fable`.
   - `home/dot_agents/model-profiles.env`: new
     `MODEL_PROFILE_AUDIT_CLAUDE_ARGS="--model claude-fable-5-1 --effort high"`
     and `MODEL_PROFILE_AUDIT_CODEX_ARGS="--profile audit"`. `DEEP_CLAUDE_ARGS`
     is now `--model claude-fable-5-1 --effort high --advisor fable`.
   - New render target `home/dot_codex/modify_private_audit.config.toml`
     (executable, 0775). It renders `~/.codex/audit.config.toml` with
     `sandbox_mode = "read-only"`.
   - `codex-config-managed.toml` is unchanged, because `deep.codex` did not change.
8. Tests:
   - `test_generate_agent_configs.py`:
     - `test_audit_profile_renders_read_only_sandbox_override` checks that
       audit renders read-only, that standard has no `sandbox_mode`, that the
       base config keeps `workspace-write`, and that the audit env line exists.
     - `test_model_profiles_reject_invalid_sandbox_mode` covers an invalid
       sandbox value.
     - Adds the `tomllib` import.
   - `test_validate_agent_assets.py`:
     - The fixture gains a pinned `audit` profile.
     - `test_agent_manifest_rejects_missing_audit_profile` covers a missing
       audit profile.
     - `test_agent_manifest_pins_the_audit_codex_profile` has 4 subtests:
       wrong model, wrong effort, wrong sandbox, and sandbox missing.

## Auditor invocation (verified)

`codex --profile audit review --commit <head-sha>` works. `--profile` is a
global flag and must come before `review`; `codex review --help` has no
`--profile`. codex-cli 0.157.1 **silently ignores unknown profiles**, so I
verified the layering with the existing `security` profile. The session header
switched the model and effort, and `-c sandbox_mode="read-only"` showed
`sandbox: read-only`. No `-c` fallback is needed. `~/.codex/audit.config.toml`
does not exist on this host until the orchestrator's next apply. For the first
live audit, check that the header shows `model: gpt-6-astra`,
`sandbox: read-only` and `reasoning effort: high`.

## Evidence summary (verbatim outputs in the validation file)

- Mutation baseline: against the unmodified scripts restored from origin/main,
  the generator tests give FAILED (failures=1, errors=1). The validator tests
  give FAILED (failures=5, errors=1).
- The same tests against the modified scripts pass: 5 tests OK.
- `generate-agent-configs.py --check`: up to date.
- `make validate-agent-assets`: ok.
- `make unit-test`: 462 tests OK (skipped=1).
- `gh pr checks 190`: all pass (nix skipping), exit 0.
- No local bats was run (repo policy).

## Deviations / notes

- The Understand-Anything PostToolUse hook asked for a `.ua/` graph update after
  the commit. I did not do it because `.ua/` is outside allowed_files.
- The auditor claude sub-profile is `claude-fable-5-1` high, per the task. It is
  only used if someone launches the Claude side of `audit`.

## Durable facts

[memory:decision] T28: three-role constellation — deep=claude-fable-5-1 high (orchestrator), standard=claude-opus-5-5 high (worker), new audit profile codex gpt-6-astra high read-only sandbox (auditor via `codex --profile audit review --commit`); acceptance stays orchestrator-only (operator 2026-09-27).

[memory:failure] codex-cli 0.157.1 silently ignores an unknown `--profile` name; verify profile layering by reading the session header with an existing profile.

CompactionDB (main checkout), decision id `e6bb0903-a81e-41db-84a7-f566aa3064ac`:

```
python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T28: three-role constellation — deep=claude-fable-5-1 high (orchestrator), standard=claude-opus-5-5 high (worker), new audit profile codex gpt-6-astra high read-only sandbox (auditor via codex review --commit); acceptance stays orchestrator-only (operator 2026-09-27)"
```

cost: n/a
