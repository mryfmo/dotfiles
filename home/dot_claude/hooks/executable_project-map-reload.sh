#!/bin/bash

# @file home/dot_claude/hooks/executable_project-map-reload.sh
# @brief Reload the visible project map after a Claude file edit.
# @exitcode 0 Always, including unavailable tools or browsers.

file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)
if [[ "$file_path" == */.project-map/index.html ]]; then
    terminal-browser action -- eval 'location.pathname.endsWith("/.project-map/index.html") && location.reload()' >/dev/null 2>&1
fi
exit 0
