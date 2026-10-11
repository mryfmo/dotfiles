"""The regime's contract decorator (T128 INV-12).

A design-tier code wave first lands its contract tests in a `<task>-contract-a01`
PR. They carry `@contract`, so they skip in ordinary CI and the PR merges before
the implementation exists. `scripts/main-tests.sh` runs main's copy of them with
`REGIME_CONTRACT=1` against the implementation PR, which removes the decorator
from the contracts it satisfies: they become ordinary tests in its tree, and
nothing stays dormant after the wave lands.
"""

import os
import unittest

contract = unittest.skipUnless(os.environ.get("REGIME_CONTRACT") == "1", "dormant contract")
