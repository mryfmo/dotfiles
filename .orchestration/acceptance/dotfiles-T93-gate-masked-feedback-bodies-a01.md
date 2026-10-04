# Acceptance: dotfiles-T93-gate-masked-feedback-bodies-a01

- **Decision:** ACCEPTED after two revise rounds. PR #251 squash-merged to `main` as `2e2e1e09`; final head `254d9ebf86e7d986b418aa74098ae546b4bdd843` (substantive commits 7d7a9777, 935399c0, 4db6083a, 63e8fd90, dd155f2b, 56546541, 62cf4aa9, 09784303, 254d9ebf; update-branch merges 10c03df2, c70878d4, ba920163, aa5b061e onto main c6b348ba). Merged without `--delete-branch`; worker-c holds `fix/gate-masked-feedback-bodies`.
- **Worker:** `claude-standard-dot-a005` (worker-c). task_rev chain matched. Dispatched after T71 merged; T95 ran on the same seat between rounds.
- **Exemption declared:** acceptance and final integration; evidence masking of the orchestrator's own sweep JSON with the PR head's `--mask-secrets`.
- **Plan reference:** T68/T91 follow-up (gate and secret scan agree on masked evidence), outside the numbered phases.

## What was accepted (`scripts/require-crit-review.py`, `scripts/validate-agent-assets.py`, tests, the pr-integration bullet and its Codex mirror)

- The gate accepts a saved feedback item when it equals the collected one verbatim or when its `body` and `path` equal their `mask_secret_matches` form; `source`, `url`, `level` and `line` stay byte-exact. `--mask-secrets` masks a parseable JSON file per key and string value (duplicate members masked as parsed; two distinct keys that would mask to one name make the run fail instead of merging) and rewrites it in the pr-feedback layout.
- The repository secret scan reads a JSON document per key and string value, so a match never spans JSON syntax; non-JSON text keeps the whole-text scan. For `.orchestration` evidence a NUL byte fails with its offset and a UTF-16 encoding is refused, both before any decode.
- The rule bullet and its Codex mirror say the JSON may be masked and name the six-field identity. 783 tests.

## Decisions taken during the rounds

- Round 1 (audit of dd155f2b): mask only body and path; JSON-aware scan (closing the thread first deferred as a follow-up); mask object keys; NUL evidence pasted. Round 2 (audit of aa5b061e): NUL check before the UTF-16 branch and UTF-16 refused for evidence; masked-key collision rejected; report corrected.
- Bot threads: eight, seven fixed in-PR, one not-applicable (masked urls: the url is the byte-exact identity and would fail closed; none exists).

## Orchestrator re-derivation

- Read every diff hunk across the rounds; re-ran the PR head's validator against the saved T93 sweep JSON (3 strings masked, 0 flagged afterwards) and confirmed `missing_feedback` accepts that masked file (this PR's own gate run below).

## Audit / Bot / sweep / gate

| scope | verdict |
|---|---|
| task-level, final head 254d9ebf | incorrect (3, P3 evidence only) → dispositions below |
| task-level, aa5b061e | incorrect (3) → fixed in 254d9ebf and the artifacts |
| task-level, dd155f2b | incorrect (5) → fixed in 56546541, 62cf4aa9, 09784303 and the artifacts |

audit-finding: 1 the report claims 15 Ruff findings are unchanged without pasted lint output → not-applicable:evidence-only finding with no code defect; the CI ruff job passes on 254d9ebf per the sweep JSON and the worker pastes the lint output as an artifact correction that does not move the head
audit-finding: 2 the validation's UTF-16 scan command contains an ellipsis → not-applicable:evidence-only finding; the worker records the exact command as an artifact correction; the orchestrator's own scan of .orchestration found no UTF-16 or NUL file
audit-finding: 3 the PR description still describes the round-0 behaviour → not-applicable:a PR body is not part of the audited changeset and does not move the head; the worker updates the description to the final behaviour (body and path masked, JSON-aware scan, UTF-16 and collision rejection) before the merge is recorded

- Sweep (head 254d9ebf): 37 items, 0 failure/warning, all dispositioned; the JSON is masked with the PR head's `--mask-secrets`. Gate at 254d9ebf with `AUDIT_EVIDENCE` and `AUDIT_DISPOSITIONS=<this record>`: exit 0 (the masked JSON accepted by this PR's own gate), evidence copies removed.

## Follow-ups

- After this merge, re-mask every saved `-pr-feedback.json` under `.orchestration/validation/` with the merged validator before the boundary commit.

## CompactionDB

- Worker decision `2c104580-db1d-4867-9777-cb115fb37676`; cited.
