---
format: 1
task: test
head: HEAD
pr: 1
ledger: []
searches: []
audit_findings:
  - n: 1
    reason: "the finding quotes not-applicable: without evidence; this reason is a field, not a disposition"
    evidence: grep -n audit_findings scripts/require-crit-review.py
---

# Acceptance: test (an audit finding whose reason quotes the grammar, thread 4249544748)
