# refkit-P2-C learning

## Reusable

- **When two independent scripts must agree on "the same set of files" (a document
  scope, a scan boundary), don't let each script independently derive that set from a
  shared config file** — it drifts the moment one script's derivation logic changes and
  the other doesn't (this is exactly how E-06 happened: `render_mermaid.py` re-derived
  "all markdown files" via `rglob`, `check_mermaid` derived "the configured document
  set" via `kit.toml` globs, and nobody noticed the two definitions had quietly
  diverged). Factor the derivation into one function both call, even if it means a new,
  deliberately dependency-free shared module so neither script's install footprint
  grows. Verify parity with an actual equality assertion (path-list, not just count)
  before trusting it, not just "looks right."
- **A "no false positive" regression-guard mutation that asserts `overall status ==
passed` is only as strong as the baseline it runs against** — if the KIT's own
  fixture ever drifts (a hash goes stale, a config key changes), _every_ mutation using
  that assertion style silently starts reporting `MISSED`, and the _cause_ can be
  completely unrelated to what each mutation is actually testing. `selftest`'s own
  `baseline` field already surfaces this (comparing `base['status']` before folding it
  into overall `status`) — read that field first when several unrelated-looking
  mutations start failing at once; don't assume all of them broke independently.
- **`repr()` a suspect line before trusting a diff read-through for anything involving
  nested string-escaping** (a Python string that is itself JS source, or any two-layer
  quoting). A single missing backslash can look completely innocuous in a rendered diff
  (`\n` vs `\\n` differ by one character) but change behavior completely at runtime,
  and the failure surfaces far from the edit (a Playwright `Page.evaluate` SyntaxError
  deep in a browser, not a Python-level error at the write site). This is the same
  class of bug flagged earlier this session ("nested-quoting bugs in inline `python3
-c`" — [[compactiondb]] area), but this time it was self-inflicted by _my own_
  scratchpad-script-generates-target-file pattern, not an inline bash invocation —
  the mitigation (write a dedicated script file, verify with `assert`) doesn't fully
  protect against escaping arithmetic errors _within_ that script's own string
  literals; only actually running the generated code catches those.
- **`coverage.py`'s `percent_covered` is a _combined_ line+branch metric, not branch
  coverage**, even when `branch = true` is configured — the JSON's separate
  `percent_branches_covered`/`covered_branches`/`num_branches` fields (or the derived
  ratio) are what "true branch coverage" actually is. A field simply being present and
  plausible-looking (a percentage between 0 and 100) doesn't mean it measures what its
  variable name in _your own_ code claims.
- **A vendored/old-generation config key (here: mutmut 2.x's `paths_to_mutate`/
  `tests_dir`) can silently stop being honored by a tool without any error** — the tool
  just ignores keys it doesn't recognize, and everything still "works" (mutmut 3 still
  ran, still produced a score) because it fell back to auto-discovering the target
  module some other way, or because the hardcoded fallback in the calling script masked
  it. Absence of an error is not confirmation that a config key still does anything;
  check the current docs page's key list directly.

## Round 2 addition (from the acceptance revision)

- **A "no regression" selftest/property-test assertion must compare against a baseline
  computed in the *same* fixture instance, not assume that instance is otherwise
  clean.** I wrote `status = 'detected' if rep_['status'] == 'passed' else 'MISSED'`
  for four mutations, which is really asserting two different things at once ("the
  tree this fixture started from was already clean" AND "my mutation didn't add
  anything") without distinguishing them. The fix — capture
  `baseline = Lint(t).run()` before mutating, then check
  `codes(mutated) - codes(baseline) == set()` — isolates exactly the second claim,
  which is the one the mutation is actually supposed to test. This generalizes past
  this one linter: any "does X introduce a new problem" check should difference
  against a same-instance before/after baseline rather than asserting the after-state
  is globally clean.

## Not promoted (task-specific)

- The E153/E158 baseline-gap analysis is specific to this session's exact sequencing
  (P2-C landing before P7/P9); not a reusable rule beyond "editing a hashed input file
  makes its dependent evidence checks fail until regeneration — this is expected, not a
  bug, when regeneration itself is out of scope."
