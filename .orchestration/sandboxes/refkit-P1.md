# refkit-P1 sandbox record

OpenSandbox was not used. This task ran entirely inside the assigned repo worktree
(`/home/moriya/Workspace/dotfiles-w1`) plus one declared, reversible effect outside it.

`effects=playwright-chromium`: `python -m playwright install chromium` wrote Chromium
build 1243 (`153.0.8010.12`), an FFmpeg build, and Chrome Headless Shell under
`~/.cache/ms-playwright/`. Reverse mapping (see `.orchestration/reports/refkit-P1.md`):

```
rm -rf ~/.cache/ms-playwright/chromium-1243 ~/.cache/ms-playwright/chromium_headless_shell-1243 ~/.cache/ms-playwright/ffmpeg-1011
```

No system `pip install` was used (all Python dependencies went through `uv run --with`,
`uv venv`, and `uv pip install --python <venv>`); no writes under `$HOME` other than the
declared Playwright browser cache; no `chezmoi apply`; no push/PR. `git status --short`
before committing showed only `references/**` and `.gitignore` as required by the task.
