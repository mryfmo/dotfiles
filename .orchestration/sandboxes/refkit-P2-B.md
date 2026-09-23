# refkit-P2-B sandbox record

OpenSandbox was not used. All edits and validation runs happened inside the assigned repo
worktree (`/home/moriya/Workspace/dotfiles-w1`). `portability_test.py` itself creates and
tears down its own throw-away project under `tempfile.TemporaryDirectory()` (outside the
repo, auto-cleaned) for each run — this is the script's own designed behavior, unchanged
from before this task, not a new sandboxing mechanism added here. No `pip install` into a
system interpreter; the "with playwright" verification run used the existing
`references/examples/flowapprove_core/.venv` (created in refkit-P1) rather than installing
anything new. No writes under `$HOME`, no `chezmoi apply`, no push/PR.
