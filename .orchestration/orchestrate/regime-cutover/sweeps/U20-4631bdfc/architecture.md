# Architecture: dotfiles at 4631bdfc (scoped to unit U20, records sync 43)

## Product, principals and resources

This is a personal dotfiles repository whose program store, `.orchestration/orchestrate/regime-cutover/`, holds the orchestration records: briefs, ledger and unit rows, decisions, verdicts, sweeps, tests, handoff and handouts.

The coordinator writes the store in the main checkout. The lever `scripts/orchestrator/records-sync.sh` (installed as `~/.local/bin/common/records-sync.sh`) publishes it as `records/sync-<n>` pull requests on the origin remote.

The principals are:
- the operator and the coordinator, who write the store;
- the lever;
- CI;
- anyone who can read the origin repository and its branches.

The protected resources:
- credentials;
- the operator's identity and account identifiers, which the private `redact-words.txt` exists to keep out of the copies;
- home and host paths;
- the integrity of the published records.

## The change

Commit 4631bdfc on origin/main cf68daf6 changes 214 paths, all under the store directory: 204 added and 10 modified. All are mode 100644 UTF-8 text, and none is a symlink or binary.

The added files are 44 briefs, 135 sweep files, 25 verdicts, a handoff page, two handouts and a test table. The row files changed are `decisions.tsv`, `ledger.tsv`, `units.tsv` and `dispositions.tsv`, plus `gates.md` and `preferences.md`. `redact-words.txt` is not in the tree.

## Controls on the publish boundary, with lines at this head

1. **Copy set.** Store paths only; no `..`, no control characters, no symlink components (`records-sync.sh:188-230`). The list is never copied (`:15-16`, `:283-292`). The change set must equal the copy set (`:435-472`).
2. **Masking and scanning.** Each copy is masked with `validate-agent-assets.py --mask-secrets`, then `--scan-identifiers` refuses on a secret pattern, a home path or a literal redact word (`records-sync.sh:408-433`; `validate-agent-assets.py:2494-2525`). There is no email or account-identity rule.
3. **CI.** `agent-assets.yml` runs the committed-secret scan on every pull request (`:3-5`, `:69-70`). `regime.yml` passes records-only diffs (`:3-8`). `test.yaml` skips the unit tests for them (`:97-146`).
4. **Review rule.** `AGENTS.md:86`: review `.orchestration` for secrets and home paths.
5. **Contract.** The sync's contract excludes content review beyond the identifier scan (`records-sync.sh:511-515`).

The store's own `decisions.tsv:521` records a hand redaction pass before this sync. It mapped home paths to `~`, the host name to `<host>`, and the five literal redact words to `<redacted>`, so the scan would pass.

## Prior coverage

The brief's carry set, `sweeps/U20-2256b56c`, does not exist. This seat's run-1 (U240 at 6bc0c2cb, 35 units, 0 findings) is carried instead:
- its U240 units carry as out of scope, because the plugin is absent at this head;
- its other units carry as out of scope, with `.orchestration#unchanged-paths` kept for the records this sync does not touch.

No earlier sweep covered a records sync.

## Companion selection

- `SUPPLY-CHAIN-AND-RELEASE.md#Build-context inclusion`: the sync turns private local files into published repository content.
- `AI-AND-LLM.md#Indirect injection through retrieved or ingested content`: briefs and rows are agent-read text.

Each unit records its exclusions. The brief's U240 hunt questions have no surface at this head.

## Execution and independence limits

No target code ran. The parent's scans read git blobs and print counts and locations only. The delegation tool and eval kernel are denied by policy on this seat, so every phase ran in the parent, and the one candidate could not be independently verified.
