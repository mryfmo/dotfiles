#!/bin/bash

# @file home/dot_claude/hooks/executable_project-map-reload.sh
# @brief Reload the visible project map after a Claude file edit.
# @description
#   Pass CDP on both calls to avoid terminal-browser issue 60.
#   Pin tab selection and guard reloads against navigation away from a project map.
#   Match the event file path before choosing an existing map tab.
#   Canonicalize event paths and file URLs with the installed isolated Python stdlib.
#   Bind the reload guard to the canonical-matched URL, encoded as a JSON string.
#   Open a separate right split using half the width when the parsed listing yields no map tab.
#   shortcut: rejected map metadata or racing writes can open another pane; tighten selection in the hook follow-up.
# @exitcode 0 Always, including unavailable tools or browsers.

# @description Return the physical absolute path of a local path or file URL.
# @arg $1 path Event path or file URL, including home and relative forms.
# @stdout Canonical path.
canonical_path() {
    python3 -I -S -c '
import os
import sys
from urllib.parse import unquote, urlsplit

path = sys.argv[1]
if path.startswith("file://"):
    url = urlsplit(path)
    if url.netloc not in ("", "localhost"):
        sys.exit(1)
    path = unquote(url.path, errors="strict")
if path == "~" or path.startswith("~/"):
    path = os.path.expanduser("~") + path[1:]
print(os.path.realpath(path))
' "$1" 2>/dev/null
}

file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
[[ -n "$file_path" ]] || exit 0
event_path=$(canonical_path "$file_path") || exit 0
[[ "$event_path" == */.project-map/index.html ]] || exit 0

listing=$(terminal-browser ls --all --json 2>/dev/null) || exit 0
candidates=$(jq -c '
    [.browsers[]? | .cdpPort as $port
     | select($port | type == "number")
     | select($port >= 1 and $port <= 65535 and $port == ($port | floor))
     | .tabs[]?
     | select(.url | strings | startswith("file://"))
     | select(.targetId | strings | test("^[A-Fa-f0-9]{32}\\z"))
     | [$port, .targetId, .url]][]
' <<< "$listing" 2>/dev/null) || exit 0
selection=""
while IFS= read -r candidate; do
    [[ -n "$candidate" ]] || continue
    tab_path=$(canonical_path "$(jq -r '.[2]' <<< "$candidate")") || continue
    [[ "$tab_path" == "$event_path" ]] || continue
    selection=$(jq -r '.[0:2] | @tsv' <<< "$candidate")
    selected_url=$(jq -c '.[2]' <<< "$candidate")
    break
done <<< "$candidates"
if [[ -z "$selection" ]]; then
    terminal-browser open "$file_path" --split right --size 0.5 --no-merge >/dev/null 2>&1
    exit 0
fi
IFS=$'\t' read -r port target_id <<< "$selection"

agent="${TERMINAL_BROWSER_AGENT:-$HOME/.local/share/terminal-browser/app/agent-browser/bin/agent-browser}"
"$agent" --cdp "$port" --session project-map-reload --pin-tab tab "$target_id" >/dev/null 2>&1 || exit 0
"$agent" --cdp "$port" --session project-map-reload --pin-tab eval "if (location.href === new URL($selected_url).href) location.reload()" >/dev/null 2>&1
exit 0
