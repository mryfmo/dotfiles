# T11 learning triage

## Validated observations

- Cross-team identity uniqueness must be checked before `mkdir` or config creation so a rejected join has no partial registry write.
- Removing one opt-in flag from argv before restoring positional arguments preserves existing callers while allowing the flag at any position.
- Querying `json_each(...agents)` by exact key avoids treating punctuation in an agent ID as JSON-path syntax during the new registry scan.

## Promotion decision

Keep this as task evidence. Do not create a project learn entry until pytest runs in the orchestrator or CI environment and confirms the test file through the required runner.

