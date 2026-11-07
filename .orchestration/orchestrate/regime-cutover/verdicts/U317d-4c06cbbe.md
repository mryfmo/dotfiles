## Findings

- P2 (high) [f1 s8] scripts/update-agent-assets.sh:2773: EXIT cleanup uses stdout retained from a failed mktemp and removes pre-existing settings paths; a scratch failure injection deleted both an existing directory printed by mktemp and an unrelated settings directory.
- P2 (high) [f1 s4] scripts/orchestrator/intake-observe.py:287: Appending to a valid decisions.tsv without a terminal newline concatenates two records; the lever reports success, but rounds-check then rejects the resulting 11-column row.
- P2 (high) [f3 s4] scripts/generate-agent-configs.py:2590: The carried P1 docs/deepseek-harness.md:141 is corrected there, but this generated guidance and the asset note still recommend hcom-seat dsh --profile router, whose binding-denied role cannot run the required listener.
- P2 (high) [f10 s3] tests/unit/test_update_agent_assets.py:6401: The fake srt always makes the new canary succeed; no DshSuperagent test injects a write-open response or failed probe, leaving this safety decision without the standing rules' required failure-injection coverage.
- P2 (high) [f10 s2] tests/unit/test_update_agent_assets.py:6953: The PR Threat table's closed updater row cites test_a_failed_build_inside_srt_removes_the_new_tree_and_records_nothing, which no longer exists; its evidence needs the renamed selector and current-head results.
- P3 (high) [f10 s1] docs/deepseek-harness.md:124: The documentation still describes one combined srt build invocation, while this head runs install and build separately; it also says the listener awaits U321 although that role is already in the base.

## Reproduced

- Git status, rev-parse and diff inspection confirmed a clean checkout at 4c06cbbe and the specified 18-path changeset.
- shellcheck -x scripts/update-agent-assets.sh passed.
- bash -n scripts/update-agent-assets.sh passed.
- shfmt -i 4 -sr -d scripts/update-agent-assets.sh passed.
- git diff --check 49f3c33c..4c06cbbe passed.
- cmp confirmed the intake-observe source and deployed copy are identical; indexed source hashes matched.
- Initial 50-test profile/intake/updater run encountered 17 failures and one error from blocked Perl/shasum and temporary-directory access; profile and intake tests passed.
- A scratch-only hashlib adapter allowed further updater checks, but 11 failures remained because the audit sandbox blocks Bash temporary files.
- A broader 203-test run encountered 79 failures and 57 errors involving unavailable PyYAML, blocked temporary files and the system Git shim; it did not establish a passing full suite.
- A focused 38-test run covering profiles, intake-observe and updater preflight checks passed.
- In-process validate_assets passed; profile, constant and lever outputs matched exactly, and the deployment index matched structurally. The alternative YAML reader reordered unrelated mappings, preventing a full bytewise render-check.
- The lever-pin and committed-output-index tests passed after correcting an initially mistyped test-class selector.
- Running the Threat table's obsolete failed-build selector produced AttributeError because that test no longer exists.
- A failing mktemp fixture printing an existing scratch directory caused EXIT cleanup to delete it and a pre-existing profile-settings directory.
- A decisions.tsv lacking its terminal newline passed rounds-check parsing before intake-observe; the lever exited 0, then rounds-check rejected the appended table as 11 columns instead of six.

## Notes

No P0 or P1 finding meets the rejection rule. The carried proxy, credential-deny and canonical launch-command blockers are addressed. Subthreshold findings are filed. The checkout remains unchanged; current CI, the upstream archive and real-srt containment were not independently verified offline.

Blocking: 0
Filed: 2
Verdict: correct
