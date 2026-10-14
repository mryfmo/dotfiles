#!/bin/bash

# @file home/dot_claude/hooks/executable_project-map-reload.sh
# @brief Reload the visible project map after a Claude file edit.
# @description Pass CDP on both calls to avoid terminal-browser issue 60.
# @exitcode 0 Always, including unavailable tools or browsers.

file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
[[ "$file_path" == */.project-map/index.html ]] || exit 0

listing=$(terminal-browser ls --all --json 2>/dev/null) || exit 0
selection=$(jq -r '
    [.browsers[]? | .cdpPort as $port
     | select($port | type == "number")
     | select($port >= 1 and $port <= 65535 and $port == ($port | floor))
     | .tabs[]?
     | select(.url | strings | endswith("/.project-map/index.html"))
     | select(.targetId | strings | test("^[A-Za-z0-9][A-Za-z0-9_-]*$"))
     | [$port, .targetId]] | .[0] // empty | @tsv
' <<< "$listing" 2>/dev/null) || exit 0
[[ -n "$selection" ]] || exit 0
IFS=$'\t' read -r port target_id <<< "$selection"

agent="${TERMINAL_BROWSER_AGENT:-$HOME/.local/share/terminal-browser/app/agent-browser/bin/agent-browser}"
"$agent" --cdp "$port" --session project-map-reload tab "$target_id" >/dev/null 2>&1 || exit 0
"$agent" --cdp "$port" --session project-map-reload eval 'location.reload()' >/dev/null 2>&1
exit 0
