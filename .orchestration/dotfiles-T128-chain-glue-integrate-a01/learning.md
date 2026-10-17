# Learning triage: dotfiles-T128-chain-glue-integrate-a01

These are candidates only; nothing is promoted.

1. [memory:decision] A mutant script must prove that each mutant changed the file before its test result counts. This run's first pass printed its diff through a filter that matched only indented lines (`^[-+] `), so the mutants of top-level lines looked unapplied while their tests failed; the second pass prints the whole hunk and ends with a baseline run of the unmutated suite, so a test that fails on clean code cannot pass for a caught mutant.
2. [memory:decision] Paginated `gh api` writes one JSON array per page back to back; a reader that needs one array takes `--paginate --jq '.[]'` (one compact object per line) and joins the lines, or the second page ends the JSON.
