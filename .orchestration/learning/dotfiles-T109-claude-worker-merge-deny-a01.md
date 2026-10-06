# Learning triage

Validated: appending the difference of a required list and an existing deny list with jq preserves existing deny order and unrelated permissions; fixture tests verify file-byte idempotence on repeated seat preparation. Applies to worker settings merges.

Official references: https://code.claude.com/docs/en/permissions (deny precedence and nested subcommands); https://code.claude.com/docs/en/permission-modes (denials apply in every mode). Prefix matching remains limited by method-flag placement.

Plan update: the shared prepare_worker_seat call covers pair starts and restarts; separate calls cover add-worker and bootstrap. No rule or learning promotion performed.
