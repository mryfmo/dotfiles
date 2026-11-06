# Architecture: dotfiles at 179de4db (scoped to unit U234b)

## Product, principals and resources

This is a personal dotfiles repository. `scripts/validate-agent-assets.py` is its committed-secret scanner and masker. It runs:
- in CI on every pull request (`.github/workflows/agent-assets.yml:69-70`), over text a pull-request author controls;
- inside the records lever (`--mask-secrets`, `--scan-identifiers`), over the program store's copies.

Its availability matters at both sites: a superlinear scan over pull-request text would stall a required check, and over store copies it would stall the records publish.

## The change

Commit 179de4db on origin/main d2389a05 changes one file, `tests/unit/test_validate_agent_assets.py` (+115/−52). The scanner under test (`scripts/`) is unchanged. The change adds `LinearGrowth` (`:147-168`) and `linear_growth` (`:171-205`), and the two linear-time tests use them:
- the padded-line test (`:2835-2926`);
- the one-finding-per-line test (`:2985-3050`).

Instead of bounding the raw ratio of two wall times at 24 over an 8x step, each test now divides the scan's growth by a reference's growth and bounds the result at 3. The reference is `re.findall` of one character over the same texts, repeated a calibrated number of rounds and timed interleaved with the scan. The 20 s hang cap and every correctness assertion stay. The 2,000-character size of the padded-line test is no longer timed.

## Entry surfaces and boundaries

- **The guard itself.** It is not a runtime boundary. It is the regression test that keeps the scan linear, so the question is whether it still fails a quadratic regression (RESOURCE-EXHAUSTION companion, superlinear matching).
- **Fixtures.** Dummy tokens built by concatenation (`:3021`), written under a `mkdtemp` root that `module.ROOT` points at during the test (`:209-220`, `:529-533`).

## Prior coverage

This seat's run-4 (records sync 45 at 2f1f2c67) is carried. Its store units are out of scope here, because the records sync commits are not on this branch. Its candidate (the account-identity row) is absent at this head and on origin/main, so it stays open on the `records/sync-*` branches only. No earlier sweep of this seat covered this test module.

## Companion selection

`RESOURCE-EXHAUSTION-AND-AVAILABILITY.md` (superlinear parsing or matching), because the module guards the scanner's complexity. Each unit records its exclusions.

## Execution and independence limits

By task rule, no target code ran; the tests were read, not run. The delegation tool and eval kernel are denied by policy on this seat, so every phase ran in the parent.
