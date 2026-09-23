# refkit-P2-C sandbox

No OpenSandbox used. Real subprocess/browser execution ran directly on this machine
(same pattern as refkit-P1/P2-B): `run_examples.py --mutation` via the
`examples/flowapprove_core/.venv` interpreter (already present from refkit-P1, left
untouched), and `render_mermaid.py` via the same venv's `playwright` + the previously
downloaded Chromium build (`~/.cache/ms-playwright/chromium-1243`) against
`references/.mermaid/{11,12}/node_modules/mermaid` (npm packages already present from
refkit-P1). No new installs were needed. All scratch/verification work (the isolated
clean-baseline copy, `/tmp/refkit-p2c/` outputs) stayed under `/tmp`, never touching the
real `evidence/` directory except transiently (each transient write was reverted via
`git checkout --` before this task's own commit).
