## Project map

- Before a long solo run (a chain of tasks, waiting on workers, or more than about 30 minutes of unattended work), launch the `project-map` subagent in the background to draw the current version. Update it after every milestone.
- Run it in the foreground only the first time, when its memory holds no style. When it replies `STYLE-NEEDED`, ask the human with AskUserQuestion for dark or light and one accent color, then re-run it with `style=... accent=...`. Reuse a saved dashboard-builder style when one exists and do not ask again.
- When the human asks "どこまで進んだ？" or how far the project has come, answer from `.project-map/state.json` and the map. Read them; do not redraw first.
- Follow the map's suggested next step. Put anything that needs the human's judgement into the map's decisions panel with a default; when no answer arrives, proceed with that default and say so.
- Existing dashboard rules (such as `/understand-dashboard` in understand-anything.md) stay as they are.
