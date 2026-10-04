# Sandbox: dotfiles-T72-bootstrap-ci-pins-a01

- **Sandboxed:** edits, tests, `make render-check`, `make validate-agent-assets` and the commit.
- **Unsandboxed:** both pushes, `gh pr create`, `gh pr edit`, `gh pr update-branch`, `gh api` and `gh run view`, the reading of the task file from the boundary ref, CompactionDB `memory add` from the main checkout, and these artifact writes.
- **Phantom `.git/config.lock`:** it made `git switch -c` and `push -u` fail to write the upstream config. I finished with `git symbolic-ref` plus `git reset --hard origin/main`, and `git ls-remote` confirmed both pushes.
- **Main checkout:** nothing in it was modified except these five T72 artifacts. The T95 lesson applied.
- **Not done:** no merge, force push, push to main, thread resolution, local bats, docs.yml dispatch, Docker build, or `make update`/`apply`/`upgrade`.
