# T8: Fix check-agent-runtime.py false positives (executable\_ prefix, runtime state)

task_id: T8
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-gpt55-high

## Background (why)

`uv run scripts/check-agent-runtime.py` exits 1 with three error classes.
Audit attribution: none involve T5/T6/T7 files; they are pre-existing drift:

1. "shared skill directory is missing files: agmsg/scripts/executable*\*.sh ..."
   — the agmsg skill sources were renamed to chezmoi `executable*`prefix
(2026-07-05, RR-9 executable-bit fix) but the checker's shared-skill
comparison compares RAW source filenames against deployed names; chezmoi
strips the`executable\_` prefix on apply, so every such file is reported
   both as "missing" (prefixed name) and "unexpected" (deployed name).
2. "unexpected files: agmsg/.agmsg, agmsg/db/messages.db*, agmsg/run/.lastcheck-*,
   agmsg/db/config.yaml" — agmsg RUNTIME state living inside the deployed
   skill dir is flagged as drift. Also `db/.keep` / `run/.keep` are reported
   missing because the deployed dirs contain real state instead.
3. hermes-agent-orchestration leftovers in `~/.claude/skills` — already
   cleaned by the orchestrator (moved out); NOT your concern.

## Goal

Fix the checker so it models chezmoi/runtime reality:

1. In the shared-skill comparison (and any other source-vs-deployed name
   comparison in `scripts/check-agent-runtime.py`), normalize chezmoi source
   attributes: strip the `executable_` filename prefix (and `private_` if the
   comparison can encounter it) before comparing source names to deployed
   names. For prefixed sources, additionally verify the deployed file has the
   executable bit and report a clear error when it does not.
2. Add a runtime-state ignore mechanism for deployed skill dirs: paths under
   `agmsg/db/`, `agmsg/run/`, and the `agmsg/.agmsg` marker are ignored on
   BOTH sides (so `db/.keep` / `run/.keep` in the source are not demanded of
   the deployed tree, and runtime files are not "unexpected"). Implement as a
   small module-level constant (e.g. tuple of ignore prefixes), not a config
   file.
3. Keep the rest of the checker behavior unchanged (it correctly caught a
   real hermes leftover — do not weaken unexpected-file detection beyond the
   runtime ignore list).
4. Unit test: follow the existing test conventions (check tests/unit for a
   checker test module; if none exists, add a minimal
   tests/unit/test*check_agent_runtime.py exercising the pure comparison
   logic with temp dirs: executable* prefix normalization, exec-bit failure
   reporting, runtime-path ignoring). Refactor the comparison into testable
   function(s) if needed, keeping the diff minimal.

## Allowed files (edit boundary)

- scripts/check-agent-runtime.py
- tests/unit/test_check_agent_runtime.py (new) or the suitable existing test module
- plus your artifact paths under .orchestration/

## Forbidden actions

git commit; git push; chezmoi apply; make update/upgrade; make require-crit-review; editing deployed files under ~/; local bats; herdr operations; deleting anything outside the repo.

## Validation (record outputs in the validation artifact)

1. `uv run scripts/check-agent-runtime.py; echo exit=$?` → exit=0 with NO errors (hermes leftover already cleaned by orchestrator; if any OTHER unexpected real drift surfaces, report it as blocked instead of silencing it)
2. `uv run python -m unittest discover -s tests/unit -v` → green including new tests
3. `python3 -m py_compile scripts/check-agent-runtime.py` → ok
4. `git status --porcelain` → only expected changes

## Expected artifacts

- report: .orchestration/reports/T8.md
- validation: .orchestration/validation/T8.txt
- sandbox: .orchestration/sandboxes/T8.md
- learning: .orchestration/learning/T8.md
- autoskill: .orchestration/autoskill/runs/T8.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT v1 task_id=T8 status=ready_for_review report=.orchestration/reports/T8.md validation=.orchestration/validation/T8.txt sandbox=.orchestration/sandboxes/T8.md learning=.orchestration/learning/T8.md autoskill=.orchestration/autoskill/runs/T8.md"
```

max_turns: 25
