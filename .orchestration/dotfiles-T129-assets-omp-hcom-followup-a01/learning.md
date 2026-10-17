# Learning triage: dotfiles-T129-assets-omp-hcom-followup-a01

These are candidates only; nothing is promoted.

1. [memory:decision] `uv tool install <local wheel>` records the wheel's path as the tool's source in its receipt, and `uv tool upgrade` re-reads it; an installer that deletes the downloaded wheel leaves a receipt that a later upgrade cannot resolve. Keep a verified local artifact at a managed path and list it in the asset manifest.
2. [memory:failure] In the Claude macOS sandbox, `mktemp` and `mktemp -d` without a template fail (they ignore TMPDIR and use the denied `/var/folders` default); tests that pin PATH to `/usr/bin:/bin` cannot be shimmed, so their failures there are environmental and the baseline run on the parent head is the evidence.
