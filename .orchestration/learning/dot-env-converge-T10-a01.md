# Learning
- Candidate (not promoted): transferring pending lifecycle output across a base gap (455455e → 3303fbc) with `git apply --3way` of a diff taken against the *old* base conflicts whenever intervening commits touched neighbouring lines, even when their content is already included. Generate the transfer diff against the *target* base (`git diff <target> -- <files>` of the source working files, e.g. via `git diff --no-index`), or take index stage 3 and prove identity with `hash-object`.
- Candidate (not promoted): after a 3-way conflict, `git rev-parse :3:<path>` equal to the source blob hash is a cheap proof that "theirs" is exactly the intended content.
- Revision 1 candidate (kept): `make upgrade` upgrades the whole user toolchain; tasks that run it need `effects=` and operator sign-off.
No rule or skill promotion.

## Revision 4
- Validated: diffing the source working files against the *target* base (`git -C <src> diff <target-sha> -- <files>`) gives a patch that `git apply --index` lands cleanly, and `hash-object` identity then holds for every file.
- Candidate (not promoted): `scripts/validate-agent-assets.py` needs PyYAML. Task files should name the repo invocation, `uv run --with pyyaml scripts/validate-agent-assets.py` (Makefile L165 / agent-assets.yml L35), not bare `python3`.
- Candidate (not promoted): the `public-bootstrap` matrix is fail-fast. One macOS chezmoi HTTP/2 `PROTOCOL_ERROR` cancels the Ubuntu legs too, so read job conclusions (`failure` vs `cancelled`) before calling a CI failure a real regression. `gh run rerun <id> --failed` is the minimal retry.
