# Learning triage: dotfiles-T133-regime-ci-fixture-grammar-a01

These are candidates only; nothing is promoted.

1. [memory:failure] An `env -i` command written outside the sandbox fails inside it in three separate ways. A Check command that strips the environment must keep each of these on purpose, and be measured on the unmodified tree before dispatch:
   - **tools on `PATH`:** here `uv`;
   - **`TMPDIR`:** without it, `tempfile` falls back to the working directory, because the sandbox does not allow `/tmp`;
   - **the proxy variables:** without them, network-dependent steps fail with DNS errors, and only when a cache needs revalidation.
2. [memory:decision] Before editing, measure a line cap against the formatter. Ruff splits any line over 120 columns, so an inline sentence on a 108-column line costs three extra lines. One shared constant keeps every row on its own line. Measure the variants on a scratch copy with `ruff format`, then `git diff --no-index --numstat`.
3. [memory:failure] A cache-dependent pass is not a stable pass. The amended command passed or failed with `uv`'s index-cache freshness. Record a run with the stable environment beside the prescribed one.
