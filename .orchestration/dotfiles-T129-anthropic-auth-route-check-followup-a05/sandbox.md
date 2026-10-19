# Sandbox evidence

Status: all a05 implementation and local tests stayed inside the authorized worker-g sandbox. Evidence is task-local; the main checkout is read-only. No escalation, live credential inspection, home apply or sibling-task mutation occurred. The predecessor a04 copy deletion is the dispatched sole scope exception.

The shared Git common config, hooks, HEAD and packed-refs remain read-only. The existing PR branch was free and checked out locally without changing shared config. Git's known packed-refs.lock maintenance warning does not establish operation success; commits, refs and remote equality will be checked directly. Commit signing is disabled only on each worker commit because the configured external SSH signing key is unavailable.

UV_CACHE_DIR=/private/tmp/uv-cache-a012 is used for uv commands; this avoids the unavailable default cache as confirmed by the orchestrator. GIT_CONFIG_GLOBAL=/dev/null is used in temporary Git-fixture tests to avoid inheriting global signing settings. Existing PyYAML is selected with uv --with pyyaml; no dependency is added. The Ruff baseline uses pristine 325f520b contents, original scripts/ and tests/unit/ relative filenames and original 100644 modes in a temporary snapshot with the repository Ruff configuration.

Local baseline/test/format/Ruff and applied-tree auth checks executed without evaluating applied scripts. Unit fixtures use temporary tracked repositories, skip symlinks and preserve the live home directory. Bats was not run. No new executable, script or interpreter configuration is introduced.

First push remains held for the orchestrator's PR420 merged-sha PING. The eventual authenticated HTTPS push will use command-scoped gh credential handling, no -u and no shared config write; no token is printed or copied. No PR is created or edited, no manual review request/comment is posted. CI and automatic-review status will be read only.

The knowledge graph is stale against the starting branch, so targeted rg was used and no .ua update was made; no update hook was acted on. The project-map output path is outside allowed_files and was not created. Worklogs are timestamped in this task directory because .agents is read-only, and remain uncommitted. Durable learning.md is a requested task report rather than a type: learn worklog and is committed under the orchestrator's specific four-evidence-file instruction.

