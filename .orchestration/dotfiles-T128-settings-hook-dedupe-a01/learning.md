# T15 amendment5 learning

[memory:failure] Interpreter basename recognition admits a compound first token ending in /usr/bin/python3 and can consume a user's preceding chained command. Exact script-path equality alone did not close it; peer caught this before amendment4 commit.

[memory:decision] The managed template emits only a bare script path, so recognize exactly one token equal to tilde/current-home absolute managed paths and preserve all multi-token commands. Four interpreter forms and the compound chain fail before clause removal, then all20 tests pass. Reuse home_dir() and current merge logic; no shell-pattern ownership heuristics. This stays in the same operator-authorized fix round.
