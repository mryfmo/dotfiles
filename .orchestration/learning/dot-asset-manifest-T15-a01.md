# Learning
- Candidate (not promoted): in zsh, `$VAR:word` applies a history modifier (`:s`, `:h`, `:t`, …), so `git show $B:path` silently breaks. Write `${B}:path` in commands built for zsh.
- Candidate (not promoted): rendering a pin by rewriting the existing `NAME="..."` assignment (exactly one match, plain value) keeps chezmoi `include`d installers self-contained and gives byte-identity for free. A shared sourced fragment does not work for inlined scripts.
- Candidate (not promoted): split a refactor into commits that each pass the generator `--check` and the validator by staging an intermediate file state from a scratch backup, and verify at each step.
- Carry-over: `test_permgate.test_bench_runs_five_layer_two_fixtures` is load-flaky in full local runs; gate commits on the required suites plus a diagnosis, not on a blind full-suite pass.
No rule or skill promotion.

## Revision round 1
- Candidate (not promoted): a text-level manifest editor (one line per NAME.FIELD, parse and verify before writing) lets shell lifecycle scripts update a commented YAML manifest without a YAML round-trip that would drop comments.
- Candidate (not promoted): unit tests here run without PyYAML, so YAML-dependent flows are tested through pure functions plus a patched parser, and the shell-side contract is asserted through the fake-uv command log.

## Revision round 2
- Candidate (not promoted): an `except module.Error` clause is evaluated only when an exception propagates, so if the optional module can be None, bind the handler target first (`() if module is None`). Otherwise the handler raises AttributeError and masks the real error.
