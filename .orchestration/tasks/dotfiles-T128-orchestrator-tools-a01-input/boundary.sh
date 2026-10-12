#!/usr/bin/env bash
# boundary-7.sh [--dry-run]: boundary PR -5 with every local-newer .orchestration file of the main checkout.
set -euo pipefail
MAIN=~/Workspace/dotfiles
S=/private/tmp/claude-501/-Users-a0004262-Workspace-dotfiles/7ae255cc-f146-44c4-b7ae-b25b7fc7311b/scratchpad
BR=orchestration/boundary-2026-10-12-5
WT="$S/boundary-2026-10-12-5"
cd "$MAIN"
git fetch -q origin main
git status --short --untracked-files=all -- .orchestration | awk '{print $2}' | sort -u > "$S/boundary-7-files.txt"
echo "files: $(wc -l < "$S/boundary-7-files.txt")"
if [ "${1:-}" = "--dry-run" ]; then cat "$S/boundary-7-files.txt"; exit 0; fi
[ -d "$WT" ] || git worktree add --no-track -b "$BR" "$WT" origin/main
while IFS= read -r f; do mkdir -p "$WT/$(dirname "$f")"; cp "$f" "$WT/$f"; done < "$S/boundary-7-files.txt"
cd "$WT"
tr '\n' '\0' < "$S/boundary-7-files.txt" | xargs -0 uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets
make validate-agent-assets
git add -A .orchestration
git -c commit.gpgsign=false commit -q -F - <<'MSG'
chore(orchestration): boundary commit 2026-10-12 (5): design v20 (plan 006 B0), review rounds 20 to 23, Phase 1 task files and their review, M/C records

Records only: the regime-v3 design at v20 (INV-12 narrowed, INV-2's dead clause, INV-6's gate clause, two map entries; receipt pointer at round 22), the design-review task file rounds 20 to 22, the receipts of rounds 20 to 23 (Claude and Codex), the Phase 1 task files (gate-evidence, playbook-rules, aws-cli-macos) after their one paired review round with both receipts and the acceptance record, plan 006 B0 done, plan 007 status and Phase 5 rows, mistake records M-20261012-12 and -13 with corrections C-14 and C-15, and the index.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
MSG
echo "commit $(git rev-parse --short HEAD)"
