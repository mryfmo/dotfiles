# T41: Remove Cognee entirely

## Objective

Understand-Anything is now the repo's knowledge layer; remove the unused
Cognee memory stack (MCP server config, installer, launcher, validation,
tests, docs, data gate) from the repository and retire the applied launcher.

## Steps

Branch `chore/remove-cognee` from current `main`; return to `main` when done;
do not push. Single commit: `chore(agents): remove the Cognee memory stack`.

1. `home/dot_agents/agent-config.yaml`: delete the `cognee_memory` entry
   under `mcp_servers` (and any other cognee references in the manifest).
2. Regenerate: `uv run --with pyyaml scripts/generate-agent-configs.py` —
   commits the regenerated `home/.chezmoitemplates/codex-config-managed.toml`
   and `home/dot_claude/private_mcp.json.tmpl` without cognee.
3. `scripts/validate-agent-assets.py`: remove
   `validate_cognee_install_assets` and its call site.
4. Delete files: `install/common/cognee.sh`,
   `home/.chezmoiscripts/common/run_once_after_05-install-cognee.sh.tmpl`,
   `home/dot_local/bin/common/executable_start-cognee-mcp`,
   `tests/install/common/cognee.bats`.
5. `home/.chezmoiremove`: add `.local/bin/common/start-cognee-mcp` (match the
   file's existing path style) so applied machines drop the launcher.
6. `home/.chezmoi.yaml.tmpl`: remove the `cognee:` data block (around line 32) including its `install` prompt/default.
7. `home/dot_agents/README.md`: remove the Shared Cognee memory section.
8b. `scripts/require-crit-review.py`: remove the
    `home/dot_local/bin/common/executable_start-cognee-mcp` entry from the
    lifecycle trigger path list (line ~43).
8c. `tests/unit/test_require_crit_review.py`: remove the matching list entry
    (line ~112). Run this test file locally (pytest via the repo's usual
    runner, e.g. `uv run --with pytest pytest tests/unit/test_require_crit_review.py`
    or `make unit-test`) and record the output in the validation file —
    Python unit tests are allowed locally; only bats stays CI-only.
8. `home/dot_local/bin/common/executable_agent-fanout`: check with
   case-insensitive grep and remove any cognee handling if present.
9. Sweep: `grep -rni cognee . --exclude-dir=.git --exclude-dir=.ua
--exclude-dir=.orchestration --exclude-dir=.agents` must return nothing
   except the intentional retirement entry in `home/.chezmoiremove`.
   (.orchestration history stays untouched.)
10. Validate: `uv run --with pyyaml scripts/validate-agent-assets.py`,
    `python3 -m py_compile scripts/validate-agent-assets.py scripts/generate-agent-configs.py`,
    generator idempotency (re-run produces no diff), and
    `bash -n` on any edited shell files.

## Forbidden actions

- No push, no PR ops, no merge.
- Do not touch `.orchestration/**` history, `.ua/**`, or unrelated files.
- No edits to live `$HOME` paths — repo source only (chezmoi apply handles
  target cleanup via `.chezmoiremove`).

## Expected artifacts

- report: `.orchestration/reports/T41-remove-cognee.md`
- validation: `.orchestration/validation/T41-remove-cognee.md`
- sandbox: `.orchestration/sandboxes/T41-remove-cognee.md`
- learning: `.orchestration/learning/T41-remove-cognee.md`
- autoskill: `.orchestration/autoskill/runs/T41-remove-cognee.md`

## Done signal

`AGMSG-RESULT v1 task_id=T41-remove-cognee status=ready_for_review|blocked`
with all artifact paths. Max turns: 25.
