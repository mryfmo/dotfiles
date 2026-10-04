# Learning triage: dotfiles-T89-add-worker-same-workspace-a01

Candidates only; nothing is promoted.

1. **`herdr workspace create --env` sets the environment of the workspace's root pane only.** A `spawn.sh --window` tab that is opened later does not inherit it. This was checked through `/proc/<pid>/environ` of live seats. Env meant for a spawn-seated agent has to travel through the spawn path itself.
2. **Self-named pair workspaces.** A pair brought up through attach keeps the workspace's own label (live wT is `dotfiles`), so "find the pair by `<repo> agents`" misses it. Find it through the self-named orchestrator pane (`single_managed_workspace` after `load_seat_labels`) or through a pane whose cwd is the main checkout.
3. **Tab filtering protects only some pair-mode logic.** It protects attach, restart and the layout repairs. Helpers that scan the whole workspace (`has_claude_pane`, `empty_pane_id`) still see every tab, so "add a tab" is not automatically "zero pair-logic impact".
4. **Prove each new test against the code it guards.** Swap in the previous file, run only the new tests, and restore. This shows the test fails without the change.
5. **Sandboxed vs unsandboxed TMPDIR.** The Claude sandbox's `$TMPDIR` (`/tmp/claude-1000`) differs from an unsandboxed command's (`/tmp`). Pass explicit paths between the two.
