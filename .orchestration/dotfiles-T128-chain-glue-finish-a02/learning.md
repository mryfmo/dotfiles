# Learning triage: dotfiles-T128-chain-glue-finish-a02

These are candidates only; nothing is promoted.

1. [memory:decision] To normalise a "not a shim" test, resolve the binary's directory, not the binary. A mise shim is a symlink to the mise binary outside `shims/`, so `realpath` of the file would let every shim through.
2. [memory:failure] A selector in a threat table must name an existing class. `ChainGlueTest` does not exist in `tests/unit/test_chain_glue.py` (its class is `ChainIntegrateTest`). A task text's selectors should be checked against `grep '^class '` before dispatch.
