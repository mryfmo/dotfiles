#!/bin/bash

# @file home/dot_claude/hooks/executable_project-map-reload.sh
# @brief Reload the visible project map after a Claude file edit.
# @description
#   Pass CDP on both calls to avoid terminal-browser issue 60.
#   Pin tab selection and guard reloads against navigation away from a project map.
#   Match the event file path before choosing an existing map tab.
#   Open a separate right split using half the width when the parsed listing yields no map tab.
#   shortcut: rejected map metadata or racing writes can open another pane; tighten selection in the hook follow-up.
# @exitcode 0 Always, including unavailable tools or browsers.

file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null) || exit 0
[[ "$file_path" == */.project-map/index.html ]] || exit 0

listing=$(terminal-browser ls --all --json 2>/dev/null) || exit 0
selection=$(jq -r --arg file_path "$file_path" --arg cwd "$PWD" '
    ($file_path | if startswith("/") then . else $cwd + "/" + . end
     | split("/") | reduce .[] as $part ([];
         if $part == ".." then .[:-1]
         elif $part == "." or $part == "" then . else . + [$part] end)
     | "/" + (map(@uri) | join("/"))) as $event_path
    |
    [.browsers[]? | .cdpPort as $port
     | select($port | type == "number")
     | select($port >= 1 and $port <= 65535 and $port == ($port | floor))
     | .tabs[]?
     | select(.url | strings | startswith("file://"))
     | select((.url | ltrimstr("file://")
               | gsub("(?<char>[^A-Za-z0-9/%._~?#-])"; .char | @uri)
               | gsub("%7[eE]"; "~")) == $event_path)
     | select(.targetId | strings | test("^[A-Fa-f0-9]{32}\\z"))
     | [$port, .targetId]] | .[0] // empty | @tsv
' <<< "$listing" 2>/dev/null) || exit 0
if [[ -z "$selection" ]]; then
    terminal-browser open "$file_path" --split right --size 0.5 --no-merge >/dev/null 2>&1
    exit 0
fi
IFS=$'\t' read -r port target_id <<< "$selection"

agent="${TERMINAL_BROWSER_AGENT:-$HOME/.local/share/terminal-browser/app/agent-browser/bin/agent-browser}"
"$agent" --cdp "$port" --session project-map-reload --pin-tab tab "$target_id" >/dev/null 2>&1 || exit 0
"$agent" --cdp "$port" --session project-map-reload --pin-tab eval 'if (location.pathname.endsWith("/.project-map/index.html")) location.reload()' >/dev/null 2>&1
exit 0
