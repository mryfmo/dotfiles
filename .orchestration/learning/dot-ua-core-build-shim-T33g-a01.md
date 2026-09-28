# T33g learning triage

## Candidates

1. A mise shim on PATH does not mean the tool is installed. A shim can exist
   for a pinned tool whose version has not been installed yet ("No version
   is set for shim"). When mise is available, invoke pinned tools through
   `mise exec <tool> -- <cmd>`, which installs on demand, rather than
   probing `command -v`. My T33f ordering (PATH first, then mise exec) was
   wrong for exactly this reason.
2. `tests/install/common/lifecycle.bats` copies the real Makefile and pins
   the exact `make update` call sequence. Any change to an `update` recipe
   command line needs that bats expectation updated in the same change, and
   task specs should list the bats file in the allowed files up front.

## Promotion

None. These are candidates only.
