# Report: dotfiles-T84-orchestrator-kind-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `feat/orchestrator-kind` from `origin/main` 2e65742c with `--no-track`. Earlier branches are untouched.
- **task_rev:** `sha256:a02bd26f…bfab9d`, matched in the main checkout.
- **PR:** #272, https://github.com/mryfmo/dotfiles/pull/272.
- **Commits:** `25f5079f` (the change, and the bot-wait diff head); `55f4d43f` (`gh pr update-branch` merge of main `ddf14036`, T86 #271, which landed during the wait).
- **Final head:** `55f4d43f`. CI is green on both heads and `mergeable_state` is `clean`. Bot wait on 25f5079f: `bot: none` after 15 min. Re-validation on the merged head: 853 unit tests OK, plus the 38 `test_codex_orchestrate` tests.
- **Final head (revise round 1):** `26e748e2`.
- **Status:** ready_for_review.

## 1. What changed

1. **Manifest** (`home/dot_agents/agent-config.yaml`): `orchestrator_kind: claude` follows `worker_kind`. Its comment mirrors `worker_kind`'s: the allowed values are `claude` and `codex`, `codex` means the pair is driven by `codex-orchestrate` (T86), the value renders as `HERDR_AGENTS_ORCHESTRATOR_KIND`, and an explicit export still overrides it.
2. **Generator** (`scripts/generate-agent-configs.py`):
   - `orchestrator_kind(manifest)` defaults to `claude` and fails on any value outside the existing `WORKER_KINDS` tuple (no second identical tuple).
   - `render_model_profiles_env` emits `HERDR_AGENTS_ORCHESTRATOR_KIND="<kind>"` right after `HERDR_AGENTS_WORKER_KIND`.
   - `home/dot_agents/model-profiles.env` is regenerated: one added line, `HERDR_AGENTS_ORCHESTRATOR_KIND="claude"`.
3. **Validator** (`scripts/validate-agent-assets.py`):
   - `orchestrator_kind` must be `claude` or `codex`.
   - The rendered env must define `HERDR_AGENTS_ORCHESTRATOR_KIND`; that token joins the existing env token list.
   - The README must contain ``` `orchestrator_kind` in `home/dot_agents/agent-config.yaml` (currently `<kind>`; ```, compared after whitespace normalisation so line wrapping does not matter.
   - Anchoring on the key name is deliberate: `worker_kind` is also `claude`, so a bare ``(currently `claude`;`` would already be satisfied by the existing worker_kind sentence and would test nothing.
4. **README:** one sentence directly after the `worker_kind` sentence: ``(currently `claude`; `claude` when the key is absent, `codex` hands the pair to `codex-orchestrate`)``, rendered as `HERDR_AGENTS_ORCHESTRATOR_KIND`.
5. **`herdr-agents`:** untouched. T85 already reads the variable from `model-profiles.env`.

## 2. Decisions (decide, record, continue)

- **A missing key is rejected by the validator but defaulted by the generator.** This is the same split as `worker_kind`: the generator defaults to `claude`; the validator, like its `worker_kind` check, rejects `None`. The shipped manifest carries the key, and the test fixture manifest gained `"orchestrator_kind": "claude"`.
- **The env check is presence-only** (the token list). `make render-check` already enforces that the env file byte-matches the manifest, so a value check there would duplicate it.

## 3. Tests

- **`tests/unit/test_generate_agent_configs.py`:**
  - `test_orchestrator_kind_defaults_to_claude`;
  - `test_model_profiles_env_renders_orchestrator_kind` (explicit `codex`: the env line and the accessor);
  - `test_unknown_orchestrator_kind_fails` (exit, plus the message on stderr).
- **`tests/unit/test_validate_agent_assets.py`:**
  - `test_agent_manifest_rejects_invalid_or_missing_orchestrator_kind` (`banana`, `None`);
  - `test_agent_manifest_requires_readme_to_state_the_orchestrator_kind` (manifest `codex` against a README stating `claude`).
  - The fixture README in `write_valid_agent_manifest` and in `test_agent_manifest_requires_readme_to_document_restart_worker` (which overwrites the README) carries the orchestrator sentence, wrapped across two lines to exercise the normalisation.
  - The first `make unit-test` run failed in that restart-worker test, because its README lacked the sentence. The fixture fix is in the same commit.

## 4. Validation summary (full output in the validation file)

| Check | Result |
| --- | --- |
| `make render-check` | up to date (exit 0) |
| `make validate-agent-assets` | ok (exit 0) |
| `grep` on the env | line 5 |
| `make unit-test` | 815 tests OK, 1 skipped |
| `ruff format --check` | 42 files already formatted (exit 0) |
| `prettier --check README.md` | clean (extra check) |
| `gh pr checks 272` | all pass (both heads) |
| `mergeable_state` | `clean` (55f4d43f) |
| Bot wait | `bot: none` (01:13:05Z–01:27:59Z) |

- **Deviation (tool invocation only):** the task's ruff command uses `mise x ruff`. Under the pinned scratch mise directory (`mise -C /tmp/claude-1000/t61-mise`), relative paths resolve in that directory, and absolute worktree paths under `.claude/` are skipped by ruff ("No Python files found"). The check therefore ran the same pinned binary (`mise -C … which ruff`, ruff 0.16.10) from the repository root with the task's exact arguments. All three attempts are in the validation file.
- **Not in scope:** a `ruff check` on the four touched Python files reports 22 lints, all on lines that already exist on origin/main and none on added lines. The task's command is `ruff format --check` only.

## 5. Revise round 1 (task_rev `sha256:8038b349…a89eea`)

The task-level audit of 55f4d43f returned `incorrect` with two findings.

1. **P2, worker-kind README check regression: fixed in `26e748e2`.**
   - **Cause:** the pre-existing worker check looked only for ``(currently `<kind>`;``. The new orchestrator sentence also contains ``(currently `claude`;``, so a README stating the wrong worker kind passed whenever the orchestrator kind equalled the manifest's worker kind. This change introduced the regression; it was not pre-existing.
   - **Fix:** the worker check is now anchored on its key, the same way as the orchestrator check: ``` `worker_kind` in `home/dot_agents/agent-config.yaml` (currently `<kind>`; ```, matched against the same whitespace-normalised README text (`readme_words`, now shared by both checks). The two fixture READMEs carry the anchored worker sentence.
   - **Test:** the new regression test `test_agent_manifest_worker_kind_check_ignores_the_orchestrator_sentence` uses manifest worker `claude`, a README worker sentence `codex` and an orchestrator sentence `claude`, and expects a failure. It fails against the 55f4d43f validator ("SystemExit not raised") and passes with the fix; both runs are verbatim in the validation file.
   - The real README passes both checks (`make validate-agent-assets` ok).
2. **P3, CompactionDB evidence: fixed in the validation file.** The first paste's header line was an `echo` of a placeholder. The validation file now has the command exactly as executed and a `memory search T84` readback showing record `14be3cdb-183b-423a-8811-659797221a0b` with the full decision text.

After the fix: `make unit-test` passes 854 tests (1 skipped), `ruff format --check` reports 43 files formatted, and render-check and validate both pass. One commit; CI is green on `26e748e2`, the bot wait (01:57:16Z–02:12:12Z) found `bot: none`, `mergeable_state` is `clean`, and main did not move. Full output is in the validation file.

cost: two content commits (change plus round-1 fix), one update-branch merge, three CI rounds, one revise round; about 18 turns.

[memory:decision] dotfiles-T84 (operator 2026-10-03): the manifest's `orchestrator_kind` (claude or codex, default claude) renders to `HERDR_AGENTS_ORCHESTRATOR_KIND` in `model-profiles.env`; the launcher (T85) and `codex-orchestrate` (T86) read it there and never from ad-hoc exports.
