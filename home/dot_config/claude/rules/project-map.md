## Project map

- Before a long solo run (a chain of tasks, waiting on workers, or more than about 30 minutes of unattended work), launch the `project-map` subagent in the background to draw the current version. Update it after every milestone. The `project-map-reload` PostToolUse hook opens its own pane in a right split using half the width at the first map write when absent, never merging it into a neighbouring terminal-browser, and reloads it at every later write; no seat and no human opens or refreshes it.
- Run it in the foreground only the first time, when its memory holds no style. When it replies `STYLE-NEEDED`, ask the human with AskUserQuestion for dark or light and one accent color, then re-run it with `style=... accent=...`.
- When the human asks "どこまで進んだ？" or how far the project has come, answer from `.project-map/state.json` and the map. Read them; do not redraw first.
- Follow the map's suggested next step. Put anything that needs the human's judgement into the map's decisions panel with a default; when no answer arrives, proceed with that default and say so.
- Existing dashboard rules (such as `/understand-dashboard` in understand-anything.md) stay as they are.
