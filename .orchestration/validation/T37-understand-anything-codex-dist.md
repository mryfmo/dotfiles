# T37 validation

All required commands passed:

```text
$ bash -n scripts/update-agent-assets.sh
exit 0

$ shellcheck -x scripts/update-agent-assets.sh
exit 0

$ shfmt -i 4 -sr -d scripts/update-agent-assets.sh
exit 0

$ uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
```

Direct replays of the six new lifecycle grep assertions all passed:

```text
function provision_codex_understand_anything_runtime()
packages/core/dist
packages/core/node_modules
Understand-Anything Codex runtime not provisioned: no matching Claude plugin release artifact
```

The revision checks for a source directory before `rm -rf` and falls back on non-numeric release-directory names; their direct grep replays also passed.

Crit-data review passed. Receipt: `.orchestration/validation/T37-understand-anything-codex-dist-review-receipt.md`.
