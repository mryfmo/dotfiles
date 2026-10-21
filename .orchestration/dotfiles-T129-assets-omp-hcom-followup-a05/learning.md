# Learning triage: dotfiles-T129-assets-omp-hcom-followup-a05

These are candidates only; nothing is promoted.

1. [memory:failure] A claim made from a reviewer's run is not evidence until the run is in the worker's own record. The a04 report cited the pre-push reviewer's GNU-shim run, but validation.md never held it, so the audit raised `audit:4e743a1:2`.
   - Re-run the reviewer's experiment and record its command, its inputs (here the shim's source and hash) and its output, or state the conclusion as an inference.
2. [memory:decision] When the real tool is missing, a shim that reproduces its documented behaviour can carry a cross-platform claim, provided three things are recorded:
   - the absence of the real tool (§4a);
   - the shim's source and hash;
   - a probe showing the shim behaves as documented while the system tool does not.

   The record must also say where the claim stops: real coreutils was not run.
3. [memory:failure] Under `uv run python -I`, a one-liner cannot import `tests.*` from the working directory, because `-I` drops it from `sys.path`. Use a small script that inserts the worktree path.
