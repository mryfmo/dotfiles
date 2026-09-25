# dot-ubuntu-parity-T12-a01 — acceptance

status: accepted
reviewed_by: claude-deep-dot (adversarial re-derivation)
evidence:
  - 38ed4a0: CI branches added to exactly the 2 new keys, matching the file's encryption CI-guard style;
    email/system prompting untouched (canned-stdin alignment restored); usePrivate CI branch ordered
    before the darwin-true default (macos-14 CI correctly gets false)
  - independent re-run: format clean / unit-test 376 OK; validation shows rendered name:"CI",
    usePrivate:false for the fixture-equivalent context, both linux and darwin
  - scope: 2 non-artifact files
cost: n/a
