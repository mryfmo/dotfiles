# refkit-P0-06 sandbox

No OpenSandbox used. This task edits a local hook script and a unit test only; all
formatter subprocess calls in the new test are mocked (no real `ruff`/`prettier`/`ty`
execution), and the one live network-touching step (`uvx ruff format --help`,
`uv run ...`, and the manual demo's real `npx prettier@2 --write`/`uvx ruff`
invocations) ran directly on this machine, matching the pattern already used by every
prior task this session (refkit-P0-01/P1/P2-A/P2-B).
