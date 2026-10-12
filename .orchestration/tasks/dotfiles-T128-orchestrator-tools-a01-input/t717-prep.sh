#!/usr/bin/env bash
# t717-prep.sh: prepare (never commit) the operator's T717 manifest patch in a detached scratch worktree.
set -euo pipefail
MAIN=~/Workspace/dotfiles
S=/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad
WT="$S/t717-prep"
cd "$MAIN"; git fetch -q origin main
[ -d "$WT" ] || git worktree add --detach "$WT" origin/main > /dev/null
cd "$WT"; git checkout -q --detach origin/main; git reset -q --hard
uv run --no-project python - <<'PY'
import pathlib
p = pathlib.Path("home/dot_agents/agent-config.yaml"); s = p.read_text()
def rep(old, new):
    global s
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)
rep("  standard:\n    claude: { model: claude-opus-5-5, effort: xhigh, advisor: fable }\n    codex:\n      model: gpt-6.1-sol\n      model_reasoning_effort: high\n",
    "  standard:\n    claude: { model: claude-opus-5-5, effort: xhigh, advisor: fable }\n    codex:\n      model: gpt-6.1-sol\n      model_reasoning_effort: xhigh\n")
rep("  review:\n    # One capability tier above the worker at full effort (operator decision 2026-10-07).\n    claude: { model: claude-fable-5-1, effort: high }\n    codex: { model: gpt-5.6-sol, model_reasoning_effort: low }\n",
    "  review:\n    # Claude: one capability tier above the worker at full effort (operator decision 2026-10-07).\n    # Codex: the worker's model at xhigh; review independence rests on the fresh context (operator decision 2026-10-12).\n    claude: { model: claude-fable-5-1, effort: high }\n    codex: { model: gpt-6.1-sol, model_reasoning_effort: xhigh }\n")
rep("  deep:\n    claude: { model: claude-fable-5-1, effort: high, advisor: fable }\n    codex:\n      model: gpt-5.6-sol\n      model_reasoning_effort: high\n",
    "  deep:\n    claude: { model: claude-fable-5-1, effort: high, advisor: fable }\n    codex:\n      # Also the profile-less base of ~/.codex/config.toml through interactive_profile (operator decision 2026-10-12).\n      model: gpt-6.1-sol\n      model_reasoning_effort: xhigh\n")
p.write_text(s); print("manifest edited (scratch worktree)")
PY
uv run --with pyyaml scripts/generate-agent-configs.py
make render-check
git diff --stat | cat
git diff > "$S/t717.patch"
echo "patch lines: $(wc -l < "$S/t717.patch")"
echo "claude-named files in diff: $(git diff --name-only | grep -c -i claude || true)"
git diff -U0 | grep -E '^[-+](model|model_reasoning_effort|MODEL_PROFILE)' | head -20
