# refkit-P0-07 sandbox

No OpenSandbox used. This task only edits a validator script and its unit tests; the
new tests run real `git init`/`git ls-files` inside `tempfile.mkdtemp()` directories
(no network, no writes outside the temp dir), matching the pattern already used by
every prior task this session.
