---
format: 2
task_id: dotfiles-T128-chain-review-scripts-followup-a08
reset_of: [dotfiles-T128-chain-review-scripts-followup-a07]
kind: code
security: true
allowed_files:
  - scripts/orchestrator/local-advisory.sh
  - scripts/orchestrator/local-review.sh
  - tests/unit/test_chain_review_scripts.py
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**
  - scripts/orchestrator/chain-integrate.sh
  - tests/unit/test_chain_glue.py
after: []
retained_predecessor_directories:
  - .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/
threat_table:
  - {control: "scripts/orchestrator/local-advisory.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success"}
  - {control: "scripts/orchestrator/local-review.sh", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects"}
  - {control: "tests/unit/test_chain_review_scripts.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; temporary fixtures assert consumed content, refusals and descendant bindings; audit checks sensitivity and retained behavioral regressions."}
  - {control: ".orchestration/dotfiles-T128-chain-review-scripts-followup-a08/**", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; records are untrusted evidence compared with dispatched bytes, diff and final-head CI; no runtime helpers."}
  - {control: "scripts/orchestrator/chain-integrate.sh", disposition: "closed: tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1"}
  - {control: "tests/unit/test_chain_glue.py", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fixtures exercise the actual caller and consumer; audit compares assertions with execution and stop behavior."}
  - {control: "task copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; compare whole-file bytes and dispatch SHA-256 at acceptance."}
  - {control: "predecessor copy: .orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; preserve SHA-256 b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36 and compare at acceptance."}
  - {control: "evidence records under .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; report, validation, sandbox, learning and autoskill records identify producers, commands, statuses, provenance and every refusal."}
  - {control: "review-cache identity and shared-artifact rejection", disposition: "closed: tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache"}
  - {control: "review-cache producer authenticity", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a09; head/base/tree are public identifiers, not producer authentication; a09 owns authenticated audit-reuse provenance and protected audit worktree inputs; its completion is a release prerequisite for the chain's trust claims, alongside deployed write protection."}
  - {control: "task metadata: kind, security, allowed_files, reset_of, retained_predecessor_directories, threat_table and premises", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; consistency checks before dispatch/acceptance and whole-file comparison detect changed metadata."}
  - {control: "metadata separators: task-copy and evidence front matter", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; parse front matter as data and compare complete bytes; evidence confers no execution authority."}
  - {control: "in-process effects", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; private repositories and bound reviewers run under verified host prerequisites; fixtures never fetch live GitHub content."}
  - {control: "workflow and interpreter or environment inputs", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; this task binds the actual chain review call sites; complete host executable/input provisioning remains separately deployed."}
  - {control: "new or renamed scripts", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none authorized; audit rejects undeclared helpers, wrappers or renames."}
  - {control: "design 5.14 item 0: 脅威モデル（D-024-21）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; shared credentials and unrestricted same-UID processes remain outside prevention; missing acceptance is detected at the next records PR."}
  - {control: "design 5.14 item 1: 書き込み境界（前提 6、ランタイム別に正直に）", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice2-a01; protected storage requires deployed Bash and file-tool boundaries for every active worker kind; mode 0700 alone proves none."}
  - {control: "design 5.14 item 2: 無害化した環境を最初に", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed caller establishes child entry boundaries; orchestrator must supply the clean outer parent before chain shell/loader startup."}
  - {control: "design 5.14 item 3: 信頼パスの境界検査", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; reject shared scratch, worker roots and aliases for production objects/artifacts; live boundary evidence remains mandatory."}
  - {control: "design 5.14 item 4: 検証したものを実行し、検証した内容を渡す", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; use the same verified bindings/content without rediscovery; unrestricted same-UID replacement remains possible."}
  - {control: "design 5.14 item 5: 出力と予約の同一性", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; fresh lookup/fetch precede full head/base/tree cache comparison; unique invocation roots introduce no reservation."}
  - {control: "design 5.14 item 6: 正直な残余", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; functional cache tests do not authenticate producers or prove live deployment, credentials, executable protection or reservations."}
  - {control: "design 5.14 item 7: 検証", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; security-assertion red/green evidence covers source, cache, consumer and entry behavior, not the whole host contract."}
  - {control: "design 5.14 item 8: 承認はコミット済み台帳から読む", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a09; a08 preserves ledger behavior without proving its source; a09 must authenticate committed-ledger reads and test their source; its completion is a release prerequisite for the chain's trust claims."}
  - {control: "design 5.14 item 9: 私設キャッシュ", disposition: "residual: owner dotfiles-T133-trusted-entrypoint-binding-a01; fresh protected object stores and protected artifacts avoid shared caches; host executable/input provenance remains a deployment residual."}
  - {control: "design 5.14 item 10: worker は sandbox 外でコマンドを実行しない（D-024-17 の改訂）", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; every Codex worker command remains sandboxed; denial produces blocked evidence without escalation."}
  - {control: "orchestrator effect trusted-parent launch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; invoke the anchored chain under design 5.14 item 2 before its first executable; no direct inherited-environment launch or self-reexec."}
  - {control: "orchestrator effect production release", disposition: "residual: owner dotfiles-T133-worker-write-boundary-slice5-a01; verify installed protection and activation before dispatch/live use; merge, after: [] and fixture success do not release dependents."}
  - {control: "orchestrator effect cache commissioning", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; after verified deployment, commission empty protected storage and quarantine prior artifacts; only reviews produced after commissioning may authorize reuse."}
  - {control: "orchestrator effect merge", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; only gh pr merge --squash --match-head-commit <audited head> after Playbook step 10; worker never merges or pushes main."}
  - {control: "orchestrator effect update-branch", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; changed head invalidates earlier CI, sweep, audit and security evidence; repeat before the gate."}
  - {control: "orchestrator effect forced worker removal", disposition: "residual: owner dotfiles-T128-chain-review-scripts-followup-a08; none planned; explicit force and acceptance recording of discarded state are required for dirty removal."}
premises:
  - {claim: "worker (Codex seat, review-profile authoring context): local continuation identity only; this does not authenticate content.", command: "git rev-parse --verify 'a644a7d9^{commit}'", output: "a644a7d965399b9463e9b32721287440a7efa233"}
  - {claim: "worker (Codex seat, review-profile authoring context): predecessor copy matches dispatched a07 bytes.", command: "git show a644a7d9:.orchestration/dotfiles-T128-chain-review-scripts-followup-a07/task.md | shasum -a 256", output: "b91cc496e71acaec4d3f8aed6680c59027aa75d2a6eac9d103be442de23e2e36  -"}
---

# AGMSG-TASK dotfiles-T128-chain-review-scripts-followup-a08 — private review content

Independent-context reset after INV-6 S2 (two amendments including the erroneous resend; D-024-41); preserve a07 history in `.orchestration/acceptance/dotfiles-T128-chain-review-scripts-followup-a07.md`. Continue PR #439, branch `tools/chain-review-scripts-followup-a07`, from `a644a7d965399b9463e9b32721287440a7efa233` with worker a013 (Codex, worker-h); create no branch or PR.
Retain inherited code head `f5aaaf7e` except the corrections below; the two additional allowed paths authorize only C-80's actual caller/consumer binding and its regression, never a09's CI-wait or stale-comment rows.
Design 5.14 in `$HOME/Workspace/dotfiles/.orchestration/plans/024-design-quality.md` is frozen (D-024-29), applies by reference (D-024-30), and its items 0–10 have individual threat rows; do not restate its contract.
[memory:decision] D-024-52 re-plans `integration-trust-chain`: narrow a08's claims and require a09 completion before release of the chain's trust claims; retain deployed-protection prerequisites.
Read the whole a07 task, its acceptance, `.orchestration/validation/dotfiles-T128-chain-review-scripts-followup-a07-audit-a644a7d.md.last.md`, the a08 acceptance's re-plan and `.agents/worklog/orchestrator-glue/BRIEF-TEMPLATE-NOTES.md`; premises above are inherited authoring observations, not rerun by this context or a013.
Before dispatch, the orchestrator records deployed design 5.14 items 1–4/9 protection for every active worker kind, installed bindings and the clean outer chain launch; otherwise keep this task and PR held.
P1-15's slice2 startup/administrative outputs and slice5 activation require actual deployment evidence; neither merge nor `after: []` establishes readiness. No worker deploys settings or invents an enforcement sentinel.
After protection is verified, the trusted orchestrator commissions empty protected review storage, quarantines pre-existing artifacts and records that boundary/creation order; pre-deployment artifacts cannot become trusted by matching public identifiers.

## Item 1

The a06 record's `## Owned by dotfiles-T128-chain-review-scripts-followup-a07` still has no rows; import none from a09.
C-80 requires `local-advisory.sh` to consume the exact protected artifact produced by Item 3, with full head/base/tree identity, rather than the legacy shared `.orchestration/validation/<task>-local-review-<sha7>.md`.
Have `chain-integrate.sh` hand that completed invocation's exact protected path and identities to the advisory consumer; validate containment, metadata and finding/count consistency before using it, and refuse missing, malformed or mismatched evidence with exit 2.
Never default a missing count to zero or fall back to shared artifacts; retain P0/P1 exit 3, chain exit 11 and existing P2/P3 ownership/repeat semantics, reading prior review content only from protected full-head artifacts.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_advisory_uses_private_review_despite_planted_legacy_success`: a private P1 plus planted legacy zero must stop; missing/mismatched private evidence must refuse; retain positive advisory cases.

## Item 2

On every `local-review.sh` invocation, before any cache read, use the bound gh for `gh api repos/mryfmo/dotfiles/git/ref/heads/main --hostname github.com --jq .object.sha`; require successful exit and exactly 40 ASCII hexadecimal characters, otherwise a named exit-2 refusal.
Neither local `main` nor `origin/main` selects the base; pass that exact SHA to `codex review --base`, with commit checks in Item 3's private store.
Keep `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null` exported and passed through `-c 'shell_environment_policy.set.GIT_NO_REPLACE_OBJECTS="1"'` and `-c 'shell_environment_policy.set.GIT_GRAFT_FILE="/dev/null"'`.
Preserve failed-review refusal, full-head equality, finding/output behavior and inherited red/green provenance; revise unsafe executable-resolution expectations and cache trust/location as required below, without undoing implemented fixes to reproduce old reds.

## Item 3

Close `audit:a644a7d:1`: review content never comes from worker-writable shared objects; existence/type checks and replacement/graft suppression do not authenticate overwritten objects.
Use `<anchored-checkout>/.agents/worklog/local-review/` as the protected production storage parent; create each invocation's fresh mode-0700 object/worktree directory there, never under `${TMPDIR:-/tmp}` or other shared scratch.
Apply design 5.14 items 1/3 to the actual resolved parent, object store, worktree and artifact paths; reject worker-writable roots and symlink/case aliases. Mode 0700 is hygiene, not a same-UID write boundary.
Before production use, the orchestrator supplies installed-policy and actual denied-write evidence for Bash and file tools of each active worker kind against this parent; absent protection keeps review/reuse/integration held, not silently downgraded.
Create a fresh bare repository with `git init --bare <dir>`, then `git --git-dir=<dir> fetch https://github.com/mryfmo/dotfiles.git <head40> <base40>` on every invocation before any cache read.
Use only that explicit HTTPS source; prohibit remote-name/URL rewriting, local transport, alternates, `--reference`, `--shared`, copied objects and the shared `.git` as object sources; apply design 5.14 items 2/4/9 to all Git children.
Bind Git, gh, reviewer and required interpreters before checkout under design 5.14 items 2/3/4/9; execute those bindings and apply the same isolation and verified Git-only resolution to reviewer descendants, retaining Item 2's overrides.
Use fresh protected `GH_CONFIG_DIR` and read the token once with the bound gh's `auth token --hostname github.com` as in `.orchestration/tasks/dotfiles-T133-python-pin-a02.md` Commands (e)/(e'); isolate the fixed-host canonical-main request. Never print/persist the token or pass it to Codex; canonical-main lookup and private fetch cannot be skipped by cached success.
Verify both exact full SHAs have type `commit` in the private repository, check out that exact head into its own worktree and verify HEAD; recompute head, canonical-main base and `git --git-dir=<dir> rev-parse <head40>^{tree}` there.
Store the artifact only at `<anchored-checkout>/.agents/worklog/local-review/<task>-local-review-<head40>.md`; shared/legacy artifacts, including ones with matching public head/base/tree, are never authoritative.
After fresh lookup/fetch/verification, a structurally valid protected artifact may skip only the model call when its single full `head:`, `base:` and `tree:` fields equal all three recomputed values and findings/counts agree.
Absent, legacy, malformed, duplicate-field, untrusted-location or mismatched artifacts require review in that private worktree and atomic replacement of the protected artifact after successful review; identifiers alone do not authenticate its producer.
On fetch failure emit `local-review: private fetch failed`; on missing/non-commit/mismatched head or base emit `local-review: private commit check failed`; exit 2, call no reviewer, create/rewrite no artifact and never fall back.
Remove only this invocation's private repository/worktree on completion/refusal; preserve failed-review transcripts and inherited exit-4 behavior without retaining reusable success for the failed invocation.
Change `chain-integrate.sh`'s actual review/advisory exec sites to establish design 5.14 item 2 before either child's shell/loader starts, using anchored script bindings; satisfy its own entry requirements under the orchestrator-controlled outer parent, with no self-reexec repair.
Add `tests/unit/test_chain_glue.py::ChainIntegrateTest::test_chain_binds_review_children_before_exec_and_stops_on_private_p1`: execute the actual changed caller/consumer path from the trusted fixture parent with hostile inherited startup/loader inputs; assert no payload/decoy execution, exact private handoff, exit 11 on private P1 despite legacy zero and no downstream sweep/audit.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_reads_private_clone_content_despite_overwritten_shared_objects`: stub gh/git, plant forged shared-object content, serve different canonical content through explicit-URL private fetch, and make the reviewer read its actual cwd; assert consumed canonical content, isolated inputs and object provenance.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_refuses_a_failed_private_fetch_or_commit_check`: cover fetch failure and each missing/non-commit/mismatched head/base, with a matching private cache planted; assert named refusal, no reviewer, no artifact creation/rewrite and no fallback.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_ignores_shared_cache_and_revalidates_private_cache`: plant matching shared head/findings-zero artifacts, also matching base/tree; assert fresh lookup/fetch, canonical-cwd review and protected rewrite.
That cache test proves lookup/fetch precede any cache read, valid protected head/base/tree skips only the model, changed/missing/duplicate metadata or inconsistent counts reruns it, and failed lookup/fetch cannot return cached success; it proves identity/rejection, not producer authenticity.
Add `tests/unit/test_chain_review_scripts.py::ChainReviewScriptsTest::test_local_review_rejects_shared_scratch_and_worker_private_roots` for shared TMPDIR, worker roots and aliases; fixtures prove path refusals only, never live worker write isolation.
Revise inherited tests that demand PATH-selected `mise which`, `command -v`/interpreter fallback or exactly two Codex overrides: assert design 5.14 items 4/9 bindings and an actually spawned Git's resolved executable/environment after Codex-policy filtering, including a shim/decoy attack.
Record each new regression red against `a644a7d9` on its security assertion, then green; separately disclose bootstrap-only fixture adaptations. Retain traversal, literal-path, shebang-argument/refusal, owner/repeat, output and failure regressions with safe fixtures.

## Out of scope

Under D-024-52, `chain-integrate.sh`'s audit-reuse decision and the shared review worktree handed to `orch-audit.sh` are unchanged by a08 and remain residual under `dotfiles-T128-chain-review-scripts-followup-a09`; that task owns their authenticated-source/protected-worktree obligation. Committed-ledger source authentication, including advisory ownership/repeat decisions (design 5.14 item 8), is also residual under a09; its text carries both obligations. a09 completion is a release prerequisite for the chain's trust claims, in addition to deployed protection; a08 tests or merge do not release them.

## Check and Completion

Host facts: mise at `$HOME/.local/bin/mise`; `env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv` -> `$HOME/.local/share/mise/installs/uv/<version>/uv-<target>/uv` (no `bin` subdirectory, no pin file); python 3.15.0 at `$HOME/.local/share/mise/installs/python/3.15.0/bin/python3`. Run that uv resolve command as a host observation and paste actual output; bind validation operands under design 5.14 items 2/4/9, record interpreter realpath/version, and never guess an uv path or use the observation as production runtime discovery.
Run the bound uv/Python equivalents of `uv run python -m unittest tests/unit/test_chain_review_scripts.py -v` and `uv run python -m unittest tests/unit/test_chain_glue.py -v` under design 5.14 items 2/9; record complete actual argv/output/status.
Run `bash -n` on all three changed shell scripts, `shellcheck scripts/orchestrator/local-review.sh scripts/orchestrator/local-advisory.sh scripts/orchestrator/chain-integrate.sh` and applicable repository lint; comments use English shdoc; never run Bats locally.
The whole PR has at most 120 changed lines outside `tests/` and `.orchestration/`, and 400 under `tests/`, counting additions plus deletions; attribute inherited 33 outside-test lines and 102 test lines (measured in Checks) separately from this reset's corrections, including caller edits.
Run `git --git-dir=<private-bare> diff --numstat <base40>...<head40>` in the authenticated private repository using resolved full SHAs and record complete output before cleanup.
The orchestrator pastes the resolved measurement base into Checks before anchor review; attribute inherited/new changes against that base and final head, including a branch-head base for any records-only round after update-branch; an overrun blocks, never raises caps.
Keep the complete dispatched text at or under 140 lines, reserving seven for Checks; no workflow, permission, dependency, launcher, knowledge-graph, predecessor-artifact or a09-owned changes are authorized.
Worker Playbook step 4 applies: every a013 command, including gh, Git and agmsg delivery, stays sandboxed; push without `-u` over HTTPS with `git push https://github.com/mryfmo/dotfiles.git tools/chain-review-scripts-followup-a07`; every denial records command/status/boundary and sends blocked PONG without escalation/substitution.
Do not probe the herdr socket; placement/delivery verification and host-deployment evidence belong to the orchestrator. Keep plan/todo/learn uncommitted and at most one active todo per owner.
Copy these complete dispatched bytes to `.orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md`; keep the retained a07 task copy/evidence unchanged; no executable helper may be hidden in the artifact wildcard.
Write `report.md`, `validation.md`, `sandbox.md`, `learning.md`, `autoskill.md` and `-worker-` crit-data/receipt evidence under the a08 directory; follow repository review gates without browser/human review, record provenance and `cost:`.
Each evidence item names `worker (Codex seat, a013)` or `orchestrator (Claude seat, sandboxed Bash)`; identify separate authoring/inherited producers honestly and include exact commands, operands, statuses, complete outputs and refusals without secrets.
Keep evidence untracked at the same relative paths in worker-h when main-checkout paths are inaccessible; RESULT identifies their location for orchestrator transfer. D-024-52 authorizes one C-80 round under `re-plan: integration-trust-chain`, retaining design 2's completed two-round history; no private extra round. Keep INV-6/a07 counters and the one worker Bot fix-round limit; surviving P0/P1 goes to the operator.
After final push verify GitHub Actions and wait for final-head Bot feedback under the Worker Playbook; the worker proposes dispositions and resolves no threads.
RESULT names PR, full head/base, branch, changed files, selectors, red/green commits, caps/attribution, artifact paths and `task_copy=<sha256 of .orchestration/dotfiles-T128-chain-review-scripts-followup-a08/task.md>`.
The orchestrator records counters before acceptance, carries a07 history, then performs final-head sweep, task audit, security review, acceptance and gate in Playbook step 10 order; changed heads repeat required evidence; advisory ownership remains `dotfiles-T128-chain-review-scripts-followup-a09`.
Complete Checks, including the resolved measurement base, before anchor review; record the independent anchor review in acceptance, then dispatch the anchored whole-file bytes unchanged, with no subsequent paste.

## Checks (orchestrator evidence completed before anchor review)

```text
measurement_base=b8213131f3818de6d14aae1ccb4b79a7ce7a99ba = git merge-base a644a7d9 origin/main; origin/main=a811f1334ad2e2a78d86fb63c65a69dba8e27b2e; observed 2026-10-21T05:28Z by the orchestrator (Claude seat, sandboxed Bash)
git diff --numstat b8213131 a644a7d9 -- scripts tests: 27 6 scripts/orchestrator/local-review.sh; 94 8 tests/unit/test_chain_review_scripts.py (inherited: 33 lines outside tests/ and .orchestration/, 102 under tests/, additions plus deletions)
env -i PATH=/usr/bin:/bin HOME="$HOME" "$HOME/.local/bin/mise" which uv -> $HOME/.local/share/mise/installs/uv/latest/uv-aarch64-apple-darwin/uv; $HOME/.local/share/mise/installs/python/3.15.0/bin/python3 exists
```
