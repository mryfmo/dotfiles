# Acceptance: dotfiles-T98-evidence-home-path-masking-a01

- **Decision:** ACCEPTED. PR #276 squash-merged to `main` as `ee0fd641`; final head `aa556845` (round 2). Gate passed at the head in the orchestrator-review worktree with the PR-feedback, audit (`incorrect`, two evidence-only dispositions below) and crit evidence (`BASE=origin/main … AUDIT_DISPOSITIONS=… make require-crit-review` rc=0, 2026-10-05 08:46Z). Three replays of the re-mask (aceb1b14, 6ce4e3b3, aa556845) reproduced the 749 files byte for byte. After the merge the orchestrator ran the new masker over every pending `.orchestration` file in the main checkout (18 files rewritten) and `make validate-agent-assets` passes (rc=0).
- **Worker:** `claude-standard-dot-a005` (worker-c, wT:p2). task_rev `29846e3f…` matched at dispatch (04:26Z).
- **Exemption declared:** acceptance and final integration (thread replies/resolutions, sweep, audit, gate, merge).
- **Plan reference:** added task (Codex Bot finding on boundary PR #273: local home paths in committed evidence); items 1–5 incl. the T83 follow-up (validator skips gitignored local state).

## What is under acceptance (PR #276; round-0 diff head `7aa565a7` / update-branch head `aceb1b14`; round-1 heads `3363ed7a` / `6ce4e3b3`; round-2 final head `aa556845` (diff and final; main unmoved at 94409ec4); 16 commits; product diff 4 files, plus 749 re-masked `.orchestration` files)

1. **Masker and scan** (`scripts/validate-agent-assets.py`): `mask_secret_matches` ends with `mask_home_paths` (shared with the gate's masked feedback comparison); the machine-independent pattern covers `/home/<user>` and `/Users/<user>` (accounts may start with `_`), root homes `~`, `~`, `~` bare or `<home>/.<dir>`, paths right after a namespace root `/proc/<pid|self>~`, and the running user's `$HOME` anywhere when multi-segment; a segment naming a top-level entry of the repository's `home/` tree is excluded (repository path, not a user). `validate_no_obvious_secrets` fails on a home path in `.orchestration/**` (raw text and decoded JSON strings) with the masking command in the message. `SECRET_PATTERN` unchanged.
2. **`herdr-agents --audit`:** no launcher change; `test_audit_task_normalises_home_paths_with_the_repository_masker` runs a task-level audit with the real validator and checks `~` in both transcript files.
3. **Re-mask:** 749 tracked `.orchestration` files, 35,162 prefixes, no `-pr-feedback.json` changed; the masker is byte-preserving (`\r` in pasted terminal output kept; the first, non-preserving re-mask was discarded).
4. **SKILL:** the Stop checklist masks every `.orchestration` file a boundary commit adds or changes with `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`; the boundary bullet runs it before `make validate-agent-assets`. The rule is unedited (429/450 words; the task's "one sentence each" was optional).
6. **Round 1 (d6b93ea9, 3363ed7a):** the `.orchestration` scan uses the masker's own pattern, so masked evidence always passes it, and gains the running user's multi-segment `$HOME` as a machine-dependent backstop (flags only on the workstation that writes the evidence; CI keeps the machine-independent forms). `~` and `~` match any child; plain `~` keeps the bare-or-`.<dir>` restriction and a `$HOME` of `~` adds no alternative, so committed Codex sub-agent ids (`/root/t97_evidence_review`) survive. Account components are any Unicode word character; `/var/home/<user>` and `/export/home/<user>` are machine-independent roots. The report now separates the eight fixed round-0 Bot findings from the `home/`-entry design limit; the narrated grep count was replaced by verbatim output re-run on the discarded first re-mask commit f3181a63. Re-mask after both commits: 0 changes (orchestrator replay at 6ce4e3b3: 749 files reproduced byte for byte).
7. **Round 2 (aa556845):** `mask_secrets` decides JSON handling by parse success (the scan's `json_strings` criterion), independent of the file suffix, catching `ValueError` and `RecursionError`; test: a `.md` whose whole content is JSON with escaped slashes is masked and then passes the scan, while prose is still masked line-wise. Sandbox record now lists the round-1 scratch worktree (removed with `git worktree remove`, no prune). Re-mask: 0 changes (orchestrator replay at aa556845 byte-identical).
5. **Validator scope:** the two repository-wide `rglob` scans skip every gitignored path (one cached `git ls-files -z --others --ignored --exclude-standard --directory`, `os.fsdecode`), so a worktree's CompactionDB ledger no longer fails `make validate-agent-assets` locally (T83 incident).

## Orchestrator re-derivation

- **Replay of the re-mask:** in the orchestrator-review worktree at aceb1b14, `git checkout origin/main -- .orchestration` (749 files), then the PR's own `scripts/validate-agent-assets.py --mask-secrets` over them: 749 files rewritten, `git diff HEAD -- .orchestration` empty. A first replay from a scratch copy of the validator diverged in 11 files because the validator derives its repository root from its own location (no `home/` entries → repository paths such as `${REPO_ROOT}/home/dot_config/…` in the T75 audit transcript were rewritten); that is evidence that the `home/`-entry exclusion is load-bearing.
- Product diff read in full; the final pattern code shows each of the eight Bot fixes.
- Design limits accepted: `/root/<name>` without a leading dot stays (Codex sub-agent ids in transcripts; `ponytail:` comment); an account named exactly like a top-level `home/` entry (`dot_config`, …) is not flagged (no such account on any host here; the exclusion protects quoted repository paths); `~` erases whose home a path was (cost noted by the worker).
- CI 13/13 on aceb1b14 (e515beb1 failed on macOS only: APFS refuses the non-UTF-8 fixture name; fixed in beb6c763).

## Bot threads (orchestrator replies and resolutions)

| thread | finding | disposition |
|---|---|---|
| 4180839344 (P1) | `/proc/self/root~/.ssh/id` escaped scan and masker | `fixed:2ae3e52c` |
| 4180886133 (P1) | root's own `~/.ssh/…` not matched | `fixed:dae71adc` |
| 4180975485 (P1) | escaped-slash JSON `\/home\/alice` passed the scan | `fixed:81812b72` |
| 4180975492 (P1) | macOS `~` not recognised | `fixed:81812b72` |
| 4181032750 (P1) | `_`-prefixed accounts not matched | `fixed:e515beb1` |
| 4181032757 (P1) | `~` not recognised | `fixed:e515beb1` |
| 4181032760 (P2) | strict decode of `git ls-files -z` on non-UTF-8 names | `fixed:e515beb1` |
| 4181164076 (P1) | root homes beneath namespace roots | `fixed:7aa565a7` |
| 4181459798 (P1, on aceb1b14) | accounts named like a top-level `home/` entry not flagged | `not-applicable` (design limit above; the exclusion keeps `${REPO_ROOT}/home/dot_config/…` intact) |
| 4181656337 (P1, on d6b93ea9) | non-ASCII account names not matched | `fixed:3363ed7a` |
| 4181656357 (P1, on d6b93ea9) | `$HOME=~` bypassed the restricted plain-`~` form | `fixed:3363ed7a` |
| 4181656346 (P1, on d6b93ea9) | custom home roots outside `/home` and `/Users` detected only on their own machine | `not-applicable` (design limit: arbitrary roots are unknowable to CI; `/var/home` and `/export/home` added in 3363ed7a; the writing workstation masks with its own `$HOME` before every boundary commit) |

| review 5411302667 body (P2, on d6b93ea9) | masker decoded JSON only for `.json` files while the scan decodes any parsing file | `fixed:aa556845` (a review-body finding without an inline thread; missed by the worker's Bot step and by the orchestrator's round-1 sweep, which treated every review item as a container; both corrected in round 2) |

**Bot coverage caveat:** three GitHub comments on the PR (07:39Z, 08:04Z, 08:24Z) report that Codex code-review usage limits were reached; the Bot therefore reviewed none of 3363ed7a, 6ce4e3b3 and aa556845, so `bot: none` on those heads is quota exhaustion, not a clean review. The task-level audit of 6ce4e3b3 is the independent review of the final head. PONG decision 1 (cap the pattern: form-only findings are proposed not-applicable with the grep showing the form absent) was dispatched 07:51Z and not yet read when the round-1 RESULT was sent; the RESULT's own disposition of 4181656346 matches it.

## Incidents and follow-ups

- Bot reviewed the update-branch head again (as in T83) seven minutes after the diff-head wait; caught by the sweep/thread query.
- Worker cost: 58 turns against max_turns 30 (five Bot rounds); the worker proposed capping the pattern, which the orchestrator accepted for the ninth thread.
- Orchestrator follow-up before the next boundary commit: run the new masker over every pending untracked/modified `.orchestration` file (T83-era artifacts hold home paths; the new scan would fail `make validate-agent-assets`). task_rev hazard: masking changes a task file's sha256; author task files with `~` or re-issue task_rev after masking.

## Audit / sweep / gate

| scope | verdict |
|---|---|
| task-level, aceb1b14 (round-0 head) | incorrect (5) → P2 scan ignores a non-standard running `$HOME` (fix: machine-dependent backstop form); P2 `/home/dot_config/.ssh/…` passes (orchestrator keeps the design-limit disposition: the `home/`-entry exclusion protects quoted repository paths, proven by the replay); P2 macOS root homes only for hidden children (fix: `~` and `~` match any child, plain `~` keeps the sub-agent-id restriction); P2 report says "fixed every finding" (fix: distinguish the ninth thread's limit); P3 narrated count instead of verbatim output (fix: restore) → revise round 1 |
| task-level, 6ce4e3b3 (round-1 head) | incorrect (3) → P2 masker decodes JSON strings only for `.json` files while the scan decodes any file that parses (fix: round 2); P2 the Bot review 5411302667 carried that finding in its body and the orchestrator's sweep dispositioned every `review` item as a container (orchestrator error: review bodies must be read for findings; round 2 dispositions it `fixed:<sha>`); P3 sandbox record says no scratch worktrees though round 1 made one (fix: round 2) → revise round 2 |
| task-level, final head aa556845 (round 2) | incorrect (2, both P3 evidence-reality on artifacts outside the PR diff) → dispositions below; no implementation defect within the accepted design limits; the auditor re-verified the 749 mechanical rewrites (747 byte-exact, 2 JSON-equivalent) and unchanged credential detection |

audit-finding: 1 the report's final status says unresolved threads block merging while the final-head sweep shows all 12 Bot threads resolved and the PR `clean` → not-applicable:the sentence was written before the orchestrator resolved the threads after the round-2 RESULT; the report is a main-checkout artifact outside the PR diff, so the head does not move; the worker corrected the final status to clean, all threads resolved by the orchestrator, head aa556845 (PONG decision 2, confirmed by its corrected PONG) and the orchestrator re-read the corrected line
audit-finding: 2 the learning note claims masking guarantees a portable scan pass despite the accepted `$HOME` dependency (a glued `F/home/runner/.ssh/id` masked under another `$HOME` survives locally but is flagged on a runner whose home it is) → not-applicable:this is the documented design limitation accepted in round 1 (the machine-dependent `$HOME` backstop flags only on the writing machine; CI keeps the machine-independent forms) and the worker's own round-1 residual-risk note; the learning file is a main-checkout artifact outside the PR diff and was corrected to state the limitation instead of a guarantee (PONG decision 2, confirmed by its corrected PONG); no tracked evidence holds such a glued runner-home path (full validator passes, re-mask unchanged)

- Sweep (final head aa556845): `.orchestration/validation/dotfiles-T98-evidence-home-path-masking-a01-pr-feedback.json`, 51 items: 11 × `fixed:` (2ae3e52c, dae71adc, 81812b72 ×2, e515beb1 ×3, 7aa565a7, 3363ed7a ×2, aa556845 for the review-body finding), 40 × `not-applicable` (2 design-limit threads, orchestrator reply comments, 18 Codex review containers without body findings, 3 Codex quota notices, CodeRabbit summary and status, 3 macOS capacity notices).
- Crit evidence `…-crit.json` (one resolved review-scope record) and receipt `…-review-receipt.md`.

## CompactionDB

- Worker decision `12c98f76` (main checkout, by a005). Orchestrator consolidation `c83687f0-6144-41f6-8c48-d5fa034da993`.
