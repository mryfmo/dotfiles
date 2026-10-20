[P1] high orchestration `.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01.md:109` — Amendment 2 excludes the pre-RESULT fix round from INV-6, contrary to C-61; Amendment 3 continues after the recorded `S2: amendments 2 >= 2`. Scope reduction by the same author does not satisfy the required independent redesign/reset.

[P2] high implementation `home/dot_local/bin/common/executable_herdr-agents:1832` — The lock assumes `.git` is a directory. A checkout using `git init --separate-git-dir` passes `is_main_checkout` but fails this redirection with “Not a directory,” preventing worker additions. Existing finding 4305808095 remains applicable.

[P2] high orchestration `.orchestration/acceptance/dotfiles-T133-worker-cap-hookspath-a01.md:62` — The disposition misidentifies that regression as an `is_main_checkout` defect. Its owner task, line 45, prescribes comparing git-dir with common-dir, which the function already does; that prescribed fix leaves the failing lock path unchanged.

[P2] high evidence `.orchestration/dotfiles-T133-worker-cap-hookspath-a01/pr-body.md:1` — The [live PR description](https://github.com/mryfmo/dotfiles/pull/408) still claims worktree hooks configuration, extension writes and corresponding tests. Those were removed at `c96697ae`; it also retains the superseded security-stop status and task hash, misrepresenting the final change.

CI verification: the [macOS unit job](https://github.com/mryfmo/dotfiles/actions/runs/39102367787/job/117601076904) passed all four added tests. Task-copy bytes match the dispatched hash; source/test changes meet the stated caps.

INV-6: violated `.orchestration/tasks/dotfiles-T133-worker-cap-hookspath-a01.md:109`

Orchestration findings: 2

📝 まとめ: Read-only audit completed; nothing modified. Local tests and live Herdr were not rerun; the functional regression and record defects above remain.
Verdict: incorrect