#!/usr/bin/env bash
# ff-main.sh: fast-forward the main checkout to origin/main after a records-only squash merge.
# Local .orchestration files identical to origin/main's version are removed (git recreates them);
# differing or extra local files are moved aside and restored after the fast-forward.
set -euo pipefail
cd ~/Workspace/dotfiles
git fetch -q origin main
side="$(mktemp -d "${TMPDIR:-/tmp}/ff-side.XXXXXX")"
kept=0 moved=0
while IFS= read -r path; do
  [ -f "$path" ] || continue
  if git cat-file -e "origin/main:$path" 2>/dev/null; then
    if [ "$(git hash-object "$path")" = "$(git rev-parse "origin/main:$path")" ]; then
      rm -f "$path"; kept=$((kept+1)); continue
    fi
  fi
  mkdir -p "$side/$(dirname "$path")"; mv "$path" "$side/$path"; moved=$((moved+1))
done < <(git status --porcelain --untracked-files=all -- .orchestration | awk '{print $2}')
git merge -q --ff-only origin/main
if [ "$moved" -gt 0 ]; then (cd "$side" && find . -type f) | sed 's#^\./##' | while IFS= read -r p; do mkdir -p "$(dirname "$p")"; mv "$side/$p" "$p"; done; fi
echo "fast-forwarded to $(git rev-parse --short HEAD); identical files recreated: $kept; local-newer files restored: $moved; side dir $side"
git status --porcelain -- .orchestration | wc -l
