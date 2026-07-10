# T10 Herdr Files Pane Learning Triage

## Existing learn entries used

- `.agents/worklog/codex/learn/20260708_122200_learn.md`: `herdr pane split` takes a positional pane id while `pane swap` uses `--pane`.
- `.agents/worklog/codex/learn/20260705_135421_learn.md`: Herdr workspace and root pane ids are under `result.*`.

## Reusable candidate

- Live verification supplied by the orchestrator established that `herdr pane split --ratio R` retains fraction `R` for the original pane; the new pane receives `1 - R`.
- For the 40/40/20 fresh layout, split the Claude root at `0.8` before starting Codex so Codex lands between Claude and files.

This candidate was recorded for orchestrator triage only. It was not promoted to the project learn registry because that path is outside this task's allowed files.

