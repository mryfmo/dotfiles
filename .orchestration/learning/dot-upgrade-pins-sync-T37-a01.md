# T37 learning triage

## Candidates

1. **Prove the carry base first.** Before `git diff origin/main | git apply
   --index` from the canonical clone, compare the clone's `origin/main`
   blobs with the target base for each carried file (`git rev-parse
   <ref>:<file>` on both sides). If they are identical, the carried diff
   cannot silently revert commits that landed after the clone's last fetch.
   Cheap, and it makes the blob-identity proof meaningful.
2. **The render check needs PyYAML.**
   `scripts/generate-agent-configs.py --check` fails under a bare `python3`
   with "PyYAML is required". Task files should spell it
   `uv run --with pyyaml scripts/generate-agent-configs.py --check`, as the
   Makefile does for validate-agent-assets.
3. **zsh does not word-split.** A plain `$FILES` variable expands as one
   word in zsh, so pathspec loops silently operate on a single bogus path.
   Use an array (`FILES=(…)`) in worker shell snippets.

## Promotion

None. These are candidates only.
