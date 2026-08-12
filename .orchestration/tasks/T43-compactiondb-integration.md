# T43: Vendor CompactionDB 2.0.0, patch the review findings, wire the lifecycle

## Objective

Integrate CompactionDB 2.0.0 (reviewed and E2E-verified by the orchestrator;
MIT, stdlib-only) into dotfiles as a vendored tree with repo-tracked patches,
a managed sync into `~/.agents/compactiondb`, a per-project install wrapper,
and the standard per-asset rule/validator/bats/docs set. Move the source zip
from `references/` to `archive/` as the provenance artifact.

## Branch / commits

Branch `feat/compactiondb-integration`, now checked out IN THIS registered
worktree (/Users/mryfmo/Workspace/dotfiles). Work ONLY here: scratch
worktrees under /private/tmp are outside the Codex sandbox workspace and
every write there triggers an approval pause — never use them. Commits 1
(b76522c) and 2 (53467d5) are done; only commit 3 remains:

### Commit 1 — `chore(vendor): import CompactionDB 2.0.0 pristine`

- `mkdir -p archive vendor` ; move `references/CompactionDB-2.0.0.zip` to
  `archive/CompactionDB-2.0.0.zip` (plain `mv`; references/ is untracked;
  remove the now-empty `references/` dir) and `git add` the zip
  (sha256 must equal
  `4c803330322ab9e786717c6439f27cc30d0bcb517857de8da56529e572e8b8d9`).
- Unzip it to a temp dir and verify the pristine extraction THERE:
  `shasum -a 256 -c MANIFEST.sha256` must report 67/67 OK on the FULL temp
  tree (the manifest includes 5 `.pytest_cache` entries, so it can only pass
  before exclusion). Then copy `CompactionDB-2.0.0/` → `vendor/compactiondb/`
  EXCLUDING `.pytest_cache/`, byte-identical otherwise. Keep the original
  `MANIFEST.sha256` file unchanged in commit 1 (provenance; it intentionally
  does not match the pruned tree until commit 2 regenerates it without the
  `.pytest_cache` entries).

### Commit 2 — `fix(vendor): harden compactiondb redaction, retention, marker parsing`

All edits under `vendor/compactiondb/`, each with regression tests added to
the package's own test suite:

1. **Redaction gaps** (`.claude/contextdb/contextdb/redaction.py`): add
   patterns for underscore-form env assignments of sensitive keys
   (`AWS_SECRET_ACCESS_KEY=...` and generally `*_SECRET*/*_TOKEN*/*_KEY=`
   assignments), Stripe `sk_live_`/`rk_live_`, Slack `xox[baprs]-`, GCP
   `AIza[0-9A-Za-z_-]{35}`; extend the sensitive-suffix key list; add
   sensitive paths `.netrc`, `.npmrc`, `.pypirc`, `.docker/config.json`,
   `authorized_keys`. Extend `tests/test_redaction.py`.
2. **Retention** : on `SessionEnd` handling in the hook pipeline, after the
   normal event write/drain, call the existing `prune_expired` (and trim
   `health/errors.jsonl` per `operations.error_log_retention_days`, plus
   clean `spool/quarantine/` entries older than the same window). Keep it
   fail-open (errors never propagate to exit code). Add a test.
3. **Marker parsing bug**: reproduce first — the prompt
   `Read README.md and tell me ... Also note [memory: e2e-test decision — this scratch project validates CompactionDB hooks] for the record.`
   produced a durable memory whose content was `for the record.` instead of
   the bracketed text. Locate the extraction regex (normalize/semantic
   layer), fix it (em-dash and trailing-text safe), add a regression test
   with exactly that prompt.
4. Regenerate `vendor/compactiondb/MANIFEST.sha256` for the patched tree
   (same format), and note the patch level in `vendor/compactiondb/CHANGELOG.md`
   under a `2.0.0+dotfiles.1` heading.
5. Verify inside `vendor/compactiondb/`: full pytest green (39 + new tests)
   and `python3 validate.py` passes everything except the `claude
--version` optional check (record output).

### Commit 3 — `feat(agents): manage CompactionDB sync and per-project install`

1. `scripts/update-agent-assets.sh`: new `update_compactiondb()` — rsync
   `vendor/compactiondb/` → `~/.agents/compactiondb/` with `--delete`,
   EXCLUDING the runtime state dirs (`.claude/contextdb/state/`,
   `.claude/contextdb/spool/`, `.claude/contextdb/health/`,
   `.claude/contextdb/contextdb.sqlite3*` if present) so user data is never
   deleted by a sync; source path resolved from the dotfiles repo (follow how
   the script locates repo-relative resources, or derive from
   `chezmoi source-path`). Call it from `main()` after the
   understand-anything entries. shdoc comments, shellcheck/shfmt clean.
2. New wrapper `home/dot_local/bin/common/executable_compactiondb-install`:
   thin shell script running
   `python3 "${HOME}/.agents/compactiondb/install.py" --project "${1:-.}"`
   (pass through extra args), with shdoc header.
3. Rules (established per-asset pattern):
   - `home/dot_config/claude/rules/compactiondb.md` +
     `home/dot_claude/rules/symlink_compactiondb.md.tmpl`: when to opt a
     project in (`compactiondb-install`), that recovery text is historical
     evidence not instructions, explicit `[memory:...]` for cross-session
     facts, `contextdb prune` runs automatically at SessionEnd, ledger may
     still contain unredacted exotic secrets so it stays gitignored and
     uncommitted, and Codex shares the same per-project DB via the explicit
     CLI.
   - `## CompactionDB` section in `home/dot_config/codex/AGENTS.md`
     (Japanese): Codex uses the explicit CLI
     (`python3 .claude/hooks/contextdb_cli.py memory add/search`, `recent
--session <id>`) against the same project DB; automatic hook capture is
     Claude-side only; workers record decisions with
     `memory add --kind decision --scope project`.
4. `scripts/validate-agent-assets.py`: `validate_compactiondb_assets()` —
   tokens for the updater function, wrapper existence, both rule docs, and
   `vendor/compactiondb/install.py` presence; call it after
   `validate_understand_anything_assets()`.
5. `tests/install/common/lifecycle.bats`: new `@test` with grep assertions
   (updater function, rsync excludes, wrapper file, rule docs, validator
   function).
6. `README.md`: extend the agent-assets section with one short paragraph
   (vendored tree, patched fork noted in vendor CHANGELOG, per-project
   opt-in via `compactiondb-install`, zip provenance in `archive/`).

## Forbidden actions

- No git push, PR ops, or merge (orchestrator's part).
- Do not run `update_compactiondb` against the live `~/.agents` (script code
  only; the orchestrator applies after merge).
- No edits outside: `archive/`, `vendor/compactiondb/`, the six files listed
  in commit 3, and the T43 artifact files.
- No new Python dependencies; the vendored package stays stdlib-only.

## Validation (record all output)

- vendor pytest + validate.py results (commit 2 step 5)
- `bash -n`, `shellcheck -x`, `shfmt -i 4 -sr -d` on the two shell files
- `uv run --with pyyaml scripts/validate-agent-assets.py`
- replay of each new bats grep
- `shasum -a 256 archive/CompactionDB-2.0.0.zip`

## Expected artifacts

- report: `.orchestration/reports/T43-compactiondb-integration.md`
- validation: `.orchestration/validation/T43-compactiondb-integration.md`
- sandbox: `.orchestration/sandboxes/T43-compactiondb-integration.md`
- learning: `.orchestration/learning/T43-compactiondb-integration.md`
- autoskill: `.orchestration/autoskill/runs/T43-compactiondb-integration.md`

## Done signal

`AGMSG-RESULT v1 task_id=T43-compactiondb-integration
status=ready_for_review|blocked` with all artifact paths. Max turns: 40.
