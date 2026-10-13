[P2] high orchestration .orchestration/tasks/dotfiles-T128-gate-evidence-a04.md:93 The contract requires every `audit_findings` field to be a non-empty string, but the passing fixture uses integer `"n": 1` at `tests/fixtures/gate-evidence/acceptance-finding-quotes-grammar.md:12`, matching PR #329’s integer-only validator; specify a positive integer for `n` and strings for `reason` and `evidence` so contract-compliant records are accepted.

[P2] high conformance .orchestration/sandboxes/dotfiles-T128-gate-evidence-a04.md:30 Call 7 created the fixture branch, checked out files, and committed `27e8a0ea` outside the sandbox; Worker Playbook steps 2 and 4 require these mutations inside it, and the fetch exception does not cover commands chained after the fetch.

Verification: all 13 files inspected; 164 lines confirmed; malformed cases are intentional; historical dispositions match; fixtures equal the recorded combined-test head. Premises 1–3 hold. Live Actions runs passed for [PR #340](https://github.com/mryfmo/dotfiles/pull/340). Unit tests were not rerun during this read-only audit.

📝 まとめ: Completed the read-only audit with two findings; modified nothing.

INV-6: holds tests/fixtures/gate-evidence/acceptance-s6-missing.md:7 and tests/fixtures/gate-evidence/pr-feedback-wrong.json:2 — within this fixture-only scope, the S6 and missing-evidence cases are preserved.

Orchestration findings: 1

Verdict: incorrect