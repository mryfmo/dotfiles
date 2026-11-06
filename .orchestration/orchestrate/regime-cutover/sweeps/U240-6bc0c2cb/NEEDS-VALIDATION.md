# Needs validation: dotfiles at 6bc0c2cbd44a76901c33acc36458518a300cb2ab

No unresolved record exists in this run, and the carried U240-2256b56c sweep holds none.

Each of the brief's questions was settled from source:
- the child's command and environment rows;
- the JSON-line parser;
- the abort and exit paths;
- what the proof runner writes and where, including round 4's per-case files;
- whether user content can forge or escape the `<dsh-system>` block.

The three new notes are operator-own test and proof behaviour, recorded as hardening in `REPORT.md` section 6, not leads:
- the test's resolution of DSH's installed llm package;
- the proof's second provider route;
- the U250 scratch directory left in tmpdir.

The carried error-text note becomes a lead only once a profile that uploads session logs loads the plugin. At this head no profile in the repository loads it. U250 item d3 (`home/dot_dsh/plugins/omp-gateway/test/use-cases.test.mjs:437-444`) now confirms, against a dummy scripted child, that the stderr tail reaches the `LlmError` message. One question stays open:
- **Owner-observed:** does `omp auth-gateway stdio` write credential text to stderr on any of its failure paths?
