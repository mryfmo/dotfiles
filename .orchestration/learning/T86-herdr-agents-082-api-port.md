# T86 Learning Triage

## Candidate reusable lessons

- Pane creation success does not prove interactive readiness. For herdr 0.8.2 automation, require both a shell foreground process and a visible prompt before `agent start`; otherwise bracketed-paste bytes can be injected into a still-initializing zsh.
- Canonicalize workdir identity with `pwd -P` before matching workspaces. On macOS, `/tmp` and `/private/tmp` otherwise describe the same directory with different strings and can create duplicate workspaces.
- A daemon-created interactive zsh can stop at `compinit` when inherited `FPATH` includes insecure directories. Propagating a caller-vetted `FPATH` makes readiness deterministic without weakening zsh security checks.
- Zsh configuration tests should isolate HOME as well as PATH; otherwise a developer's mise activation can replace fake binaries and accidentally execute the real CLI.

## Promotion

The two required architectural decisions were promoted to CompactionDB. The operational lessons above remain task-local pending reuse in another herdr lifecycle change; no new skill was warranted.
