# fix-chezmoi-pycache-modify-exec: Repair `make update` chezmoi exec format error

task_id: fix-chezmoi-pycache-modify-exec
repo: /Users/mryfmo/Workspace/dotfiles
team: dotfiles-conformance
worker: codex-gpt55-high

## Background (root cause, already confirmed — do not re-investigate from scratch)

`make update` → `chezmoi apply --verbose --exclude=scripts` fails:

```
chezmoi: .codex/__pycache__/config.cpython-311.pyc: fork/exec /var/folders/.../2065149409.config.cpython-311.pyc: exec format error
```

- Stray file `home/dot_codex/__pycache__/modify_private_config.cpython-311.pyc` sits in the chezmoi source tree (git-ignored, but chezmoi walks the disk).
- chezmoi parses the `modify_` + `private_` filename prefixes as source-state attributes and treats the `.pyc` as a **modify script** for target `.codex/__pycache__/config.cpython-311.pyc`; exec of a `.pyc` → `exec format error`.
- `--exclude=scripts` only excludes `run_` scripts (type=scripts), not `modify_` entries (type=modifies).
- Proof: `chezmoi source-path ~/.codex/__pycache__/config.cpython-311.pyc` → that .pyc.
- No `__pycache__`/`*.pyc` patterns exist in `home/.chezmoitemplates/chezmoiignore.d/*`.
- The failed apply already created an empty `~/.codex/__pycache__/` in the target.
- Cache origin is not pinned down (mtime 2026-07-08 09:33, during a WP-I/J/K worker run). `tests/unit/test_codex_config_merge.py` runs the script via subprocess (no cache); the spec_from_file_location loaders in `tests/unit/test_generate_agent_configs.py` / `tests/unit/test_validate_agent_assets.py` byte-compile in-tree modules under `scripts/`. Something similar likely imported `home/dot_codex/modify_private_config.toml` as a module.

## Goal

1. **Immediate fix**: delete the stray caches
   - `rm -rf home/dot_codex/__pycache__`
   - `rmdir ~/.codex/__pycache__` (empty dir created by the failed apply; use rmdir, NOT rm -rf, so it fails loudly if unexpectedly non-empty)
2. **Durable fix (a)**: add bytecode ignore patterns to `home/.chezmoitemplates/chezmoiignore.d/common`:
   - `**/__pycache__` and `**/*.pyc` (chezmoiignore matches TARGET paths; verify pattern syntax against chezmoi docs/behavior with the dummy test below)
3. **Durable fix (b)**: stop in-tree bytecode generation
   - Set `sys.dont_write_bytecode = True` before `exec_module` in the module loaders of `tests/unit/test_generate_agent_configs.py` and `tests/unit/test_validate_agent_assets.py` (or a cleaner equivalent, e.g. at module import top). Grep `spec_from_file_location` / `exec_module` across scripts/ and tests/ to make sure you cover every in-tree loader.
   - Do NOT modify `home/dot_codex/modify_private_config.toml` itself.

## Allowed files (edit boundary)

- delete: `home/dot_codex/__pycache__/` (and dummy files you create there during validation), `~/.codex/__pycache__/` (empty dir only)
- edit: `home/.chezmoitemplates/chezmoiignore.d/common`, `tests/unit/test_generate_agent_configs.py`, `tests/unit/test_validate_agent_assets.py`, plus any other in-tree spec_from_file_location loader your grep finds under scripts/ or tests/
- write: your artifact paths under `.orchestration/`

## Forbidden actions

git commit; git push; dependency changes; editing `home/.chezmoi.yaml.tmpl` or `~/.config/chezmoi/chezmoi.yaml`; editing `home/dot_codex/modify_private_config.toml`; editing the Makefile `--exclude` flags (workaround, not a fix); running bats; LLM calls.

Exception to the usual no-apply rule: you MAY run `make update` / `chezmoi apply` here — restoring that exact command is the point of this task and the orchestrator will re-run it independently afterwards.

## Validation (save all command outputs to the validation artifact)

1. `ls home/dot_codex/` → no `__pycache__`
2. `make update` → exit 0, no exec format error (run from repo root)
3. `chezmoi status | grep -i pycache` → empty
4. Recurrence guard: create dummy `home/dot_codex/__pycache__/modify_private_config.cpython-311.pyc` (any bytes), confirm `chezmoi status` ignores it (no pycache entries), then delete the dummy
5. `uv run pytest tests/unit/` → all pass, and afterwards `find . -path ./\.git -prune -o -name '__pycache__' -print` shows no in-tree `__pycache__` under `home/` (pytest's own caches under tests/ are acceptable only if they predate your change; prefer none under home/)
6. `git status --porcelain` → only expected changes

## Expected artifacts

- report: .orchestration/reports/fix-chezmoi-pycache-modify-exec.md
- validation: .orchestration/validation/fix-chezmoi-pycache-modify-exec.txt
- sandbox: .orchestration/sandboxes/fix-chezmoi-pycache-modify-exec.md
- learning: .orchestration/learning/fix-chezmoi-pycache-modify-exec.md
- autoskill: .orchestration/autoskill/runs/fix-chezmoi-pycache-modify-exec.md (record "not-used")

## Done signal

```
bash ~/.agents/skills/agmsg/scripts/send.sh dotfiles-conformance codex-gpt55-high orchestrator-fable5 "AGMSG-RESULT v1 task_id=fix-chezmoi-pycache-modify-exec status=ready_for_review report=.orchestration/reports/fix-chezmoi-pycache-modify-exec.md validation=.orchestration/validation/fix-chezmoi-pycache-modify-exec.txt sandbox=.orchestration/sandboxes/fix-chezmoi-pycache-modify-exec.md learning=.orchestration/learning/fix-chezmoi-pycache-modify-exec.md autoskill=.orchestration/autoskill/runs/fix-chezmoi-pycache-modify-exec.md"
```

max_turns: 15
