# Report: dotfiles-T98-evidence-home-path-masking-a01

- **Worker and branch:** `claude-standard-dot-a005` in worker-c, branch `chore/evidence-home-path-masking` from `origin/main` 61806f56 with `--no-track`. Earlier branches are untouched.
- **task_rev:** `sha256:29846e3f…8a7136a`, matched in the main checkout.
- **PR:** #276, https://github.com/mryfmo/dotfiles/pull/276.
- **Commits:**
  - `397b0215`: masker, scan, ignore-skip, tests and SKILL sentences.
  - `2b7e3797`: byte-preserving masker.
  - `97525e13`: `$HOME` anywhere, and a machine-independent scan.
  - `4fd1b43f`: the mechanical re-mask.
  - `2ae3e52c`: the first Codex P1 fix.
  - `dae71adc`: the second Codex P1 fix.
  - `811eea63`: the mechanical re-mask for it.
  - `81812b72`: the third Bot round.
  - `e515beb1`: the fourth Bot round.
  - `beb6c763`: macOS CI fix.
  - `7aa565a7`: the fifth Bot round; this is the diff head (`bot: none`, 06:41:10Z–06:56:12Z).
  - `aceb1b14`: the final head, the `gh pr update-branch` merge of main `64167825` (#277) on top of `794a80db` (#275). CI is green, and `mergeable_state` is `blocked` only by the unresolved Bot threads.
- **CI and bot:** the CI result, mergeable state and bot wait are in the validation file.
- **Main moved twice** while the PR was open (#275, then #277); neither touches the validator or `.orchestration`, and both merges were clean.
- **Status:** ready_for_review.

## 1. What changed (items 1–5)

Example paths below are spelt with `∕` (U+2215) where a literal path would be masked or flagged by the scan this task adds.

1. **Masker and scan** (`scripts/validate-agent-assets.py`):
   - `mask_secret_matches` now ends with `mask_home_paths`, which rewrites a home-directory prefix to `~`. The `--mask-secrets` mode and the integration gate's masked comparison of feedback bodies (`require-crit-review.py` `feedback_key(masked=True)`) both call it, so they stay in step. `SECRET_PATTERN` is unchanged.
   - `validate_no_obvious_secrets` fails on a home path in `.orchestration/**` (`… names a home directory; normalise it with uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`).
   - Tests:
     - normalisation cases, including repository paths, placeholders and a glued temporary home;
     - the scan rejecting home paths in `.orchestration` only, and passing after masking;
     - `--mask-secrets` on text and JSON evidence;
     - a byte-preservation test.
2. **`herdr-agents --audit`:** no launcher change was needed. Its existing call (`python3 <DIR>/scripts/validate-agent-assets.py --mask-secrets <out> <out>.last.md`) now normalises home paths. `test_audit_task_normalises_home_paths_with_the_repository_masker` commits the real validator in the fixture DIR and runs a task-level audit (`--task T1`) whose transcript and `.last.md` hold the fixture `$HOME`, `∕Users∕alice` and `∕home∕alice`. Both files come out with `~` and `Audit verdict: correct`.
3. **One-time re-mask** (`4fd1b43f`):
   - Every tracked `.orchestration` file went through the masker: 35,162 prefixes in 749 files (the masker's own output is in the validation file).
   - A verification script compared each changed file with the home-path rewrite of its previous content: 747 are byte-identical, and the two `crit-comments.json` files parse to the same document (the masker re-dumps JSON, so `<` becomes `<`). Nothing is unexplained.
   - **No `-pr-feedback.json` changed.**
   - The task's grep `grep -rl "/home/[a-z]*/" .orchestration | wc -l` is 0. Before the `$HOME`-anywhere fix it was 11: `file:///home/…`, `/proc/self/root/home/…`, and pytest output glued to a path (`..F/home/…`).
4. **SKILL:**
   - The Stop checklist masks every `.orchestration` file a boundary commit adds or changes, using `uv run --no-project --with pyyaml scripts/validate-agent-assets.py --mask-secrets <files>`.
   - The boundary-commit bullet runs that masker before `make validate-agent-assets`.
   - **The rule is not edited:** it is at 429 words, and T83's docs test caps it at 450, so one more sentence would fail that test. The task allowed "one sentence each", which I read as optional.
5. **Validator scope:** the two repository-wide `rglob` scans (`validate_no_removed_claude_skill`, `validate_no_obvious_secrets`) skip every path git ignores. They use one cached `git ls-files -z --others --ignored --exclude-standard --directory`; outside a work tree the set is empty and everything is scanned as before. `test_recursive_scans_skip_gitignored_local_state` builds a git fixture whose ignored `.claude/contextdb/state/context.db` holds the removed-skill token, a token-shaped secret and a home path. Both scans pass, and the same text in a non-ignored file fails both. `make validate-agent-assets` now passes in this worktree, where T83's ledger failure came from.

## 2. Decisions and their costs

- **Scope widened from "the running user's home" to any `/home/<user>` or `/Users/<user>`** (plus `$HOME` anywhere in the masker).
  - A running-user scan cannot be machine-independent: CI runs as `runner`, and committed evidence quotes `∕home∕runner` 266 times and `∕Users∕runner` 141 times from Actions logs. A running-user-only scan would also fail CI on any workstation's unmasked evidence.
  - The task's own validation grep expects 0 files, which a running-user-only masker cannot reach.
  - **The scan pattern does not depend on `$HOME`**, so CI and workstations flag the same text. The masker covers that pattern plus `$HOME` anywhere, so masked evidence always passes.
  - **Cost:** `~` erases whose home it was, and can read as portable when the original point was the opposite. For example, `T56b-crit-comments.json` now says "four hard-coded ~ paths in home/Library/LaunchAgents/com.mryfmo.dotfiles.usage-snapshot.plist", where the finding was about absolute paths. Transcripts quoting fixture users (`∕Users∕alice`, `∕home∕dotmktcheck`) also become `~`.
- **Repository paths are protected:** a segment that names a top-level entry of the repository's `home/` tree (`dot_config`, `.chezmoiscripts`, `private_*`, …) is never a user, and a generic match must not be glued to a word character (`dotfiles/home/x`, a test's temporary `…∕home∕worker`).
- **Unrequested change: byte-preserving masker** (`2b7e3797`). The first re-mask showed 32,599 insertions against 32,587 deletions (+12 lines). The masker read files with universal newlines, so a `\r` in pasted terminal output (10 in `dot-codex-worktree-git-writable-T50-a01.md`) became a newline. It now decodes and writes bytes; a test pins a CR-bearing file. After the fix the re-mask is +32,511/−32,511. The first re-mask was discarded, not committed.
- **Forward implication for PR feedback:** Bot bodies on PRs (including this one) can quote diff lines that hold home paths. When the orchestrator sweeps such a PR, the scan rejects the unmasked `-pr-feedback.json` once it is in `.orchestration/`. After masking, the gate still accepts it, because `feedback_key(masked=True)` routes through the same `mask_secret_matches`.
- **task_rev hazard (for the orchestrator):** the re-mask changed 182 tracked task files (none in flight: T81b, T87, T90b and T98 have no home paths). Their recorded `task_rev` values in acceptance records and agmsg history describe pre-mask content. The new boundary rule masks every added or changed `.orchestration` file, including `tasks/*.md`, so masking an in-flight task file changes its sha256 and breaks the next task_rev check. Recommendation: author task files with `~`, or re-issue task_rev after masking.
- **Main checkout after merge:** untracked T83-era artifacts written after #273 still hold home paths. `make validate-agent-assets` in the main checkout fails on them until the Stop-checklist masking runs over them. My own five T98 artifacts were masked after writing (validation file).

## 3. Codex Bot review of 4fd1b43f (one review, one comment; wait ended 04:59:58Z)

| Thread | Finding | Disposition |
| --- | --- | --- |
| 4180839344 (P1, `validate-agent-assets.py`) | `∕proc∕self∕root∕home∕alice∕.ssh∕id` escaped both the scan and the masker, because the generic rule refused a match glued to `root`. On a root runner, `$HOME=∕root` matching anywhere rewrote `∕proc∕self∕root` itself to `∕proc∕self~`, leaving `home∕alice` exposed. | `fixed:2ae3e52c`. Both patterns accept a home path right after `∕root` (namespace roots `∕proc∕<pid\|self>∕root`). A one-segment `$HOME` keeps the scan's boundary instead of matching anywhere. Tests: `∕proc∕self∕root∕home∕alice∕.ssh∕id` and `∕proc∕42∕root∕Users∕bob∕x` become `…∕root~∕…`; with `HOME=∕root`, `cd ∕root∕x` becomes `cd ~/x`, while `/proc/self/root/etc` stays and is not flagged. The re-masked evidence still passes the validator (no `/proc/*/root/(home\|Users)/` path remains), so no re-mask was needed. |

Codex Bot review of 2ae3e52c (one review, one comment; wait ended 05:11:58Z):

| Thread | Finding | Disposition |
| --- | --- | --- |
| 4180886133 (P1, `validate-agent-assets.py`) | Root's own home (`∕root∕.ssh∕id_ed25519`) matched neither the machine-independent scan nor, for a non-root masker, the masker. | `fixed:dae71adc`. Both patterns treat root's home as a bare `∕root` or a `∕root∕.<dir>` path, with the generic boundary, so `/proc/self/root` stays intact. **Deliberate limit:** a `/root/<name>` without a leading dot stays, because committed Codex transcripts name sub-agents that way (`/root/t97_evidence_review`, 40+ occurrences). The limit is marked with a `ponytail:` comment in the code; widen it when evidence quotes other `/root/<dir>` paths. Re-mask `811eea63` rewrote 2 `…:∕root∕.config∕gcloud` docker mounts (now `…:~/.config/gcloud`) in one audit transcript, byte-identical to the rewrite. Sentence-final `/root.` (4 files) is neither flagged nor masked, consistently. |

Codex Bot review of 811eea63 (one review, two comments; wait ended 05:30:13Z), both fixed in `81812b72`:

| Thread | Finding | Disposition |
| --- | --- | --- |
| 4180975485 (P1) | The `.orchestration` home-path scan searched raw JSON text, so an escaped `\/home\/alice\/.ssh\/id` passed. | `fixed:81812b72`. The scan now checks the raw text and every decoded JSON string (`json_strings`), as the secret scan does. A test with an escaped-slash JSON file fails the scan. |
| 4180975492 (P1) | macOS root's home `∕var∕root` was not recognised. | `fixed:81812b72`. The root-home form is `(?:∕var)?∕root`, bare or `<home>∕.<dir>`, with the same boundary; a test covers `∕var∕root∕.ssh∕id_ed25519` becoming `~/.ssh/id_ed25519`. The tracked evidence has no such path and still validates, so no re-mask. |

Codex Bot review of 81812b72 (one review, three comments; wait ended 05:44:16Z), all fixed in `e515beb1`:

| Thread | Finding | Disposition |
| --- | --- | --- |
| 4181032750 (P1) | Account names starting with `_` (`∕home∕_build∕.ssh∕id`) were not matched. | `fixed:e515beb1`. The first account character may be `_`; the placeholder and repository-entry exclusions are unchanged. |
| 4181032757 (P1) | macOS's physical `∕private∕var∕root` was not a root home. | `fixed:e515beb1`. The root-home form is `(?:(?:∕private)?∕var)?∕root`, and the full prefix becomes `~`. |
| 4181032760 (P2) | A non-UTF-8 ignored file name made the strict `.decode()` of `git ls-files -z` raise, aborting both scans. | `fixed:e515beb1`. Names are decoded with `os.fsdecode`, as `Path` does; the ignore test adds a raw `\xff` file name under the ignored ledger directory. |

**CI on e515beb1 failed on macOS only:** `test (macos-14, client)` errored in `test_recursive_scans_skip_gitignored_local_state`, because APFS refuses a non-UTF-8 file name (`OSError: [Errno 92] Illegal byte sequence`). The three Ubuntu `test` jobs were cancelled by the matrix's fail-fast. `beb6c763` creates that fixture file under `contextlib.suppress(OSError)`, since git cannot emit such a name on a filesystem that refuses it. The run log excerpt is in the validation file.

Bot wait on e515beb1: `bot: none` (05:55:25Z–06:10:26Z). Codex Bot review of beb6c763 (one review, one comment; wait ended 06:14:23Z):

| Thread | Finding | Disposition |
| --- | --- | --- |
| 4181164076 (P1) | Root-home forms lacked the namespace-root exception, so `∕proc∕1∕root∕root∕.ssh∕id_ed25519` (or its `∕var∕root` equivalent) passed. | `fixed:7aa565a7`. The root-home forms use the same boundary as `/home/<user>`; a test covers `∕proc∕1∕root∕root∕.ssh∕id` and `∕proc∕1∕root∕var∕root∕.ssh∕id`, while `/proc/self/root/etc` stays untouched. |

Five Bot rounds have each found narrower home-path forms. Eight Bot findings were fixed (4180839344, 4180886133, 4180975485, 4180975492, 4181032750, 4181032757, 4181032760, 4181164076). Thread 4181459798 on aceb1b14 (accounts named like a top-level `home/` entry) is not a fix but a design limit, dispositioned `not-applicable` by the orchestrator (section 6). If the Bot keeps finding more after this round, I propose capping the pattern: it covers the forms committed evidence actually contains, and the scan is a backstop to the masking step, not a proof.

cost: eleven commits, seven CI rounds; about 58 turns (max_turns 30 exceeded by five Bot rounds).

[memory:decision] dotfiles-T98 (orchestrator 2026-10-05): committed `.orchestration` evidence has home paths normalised to `~` by the repository masker, which the boundary procedure runs before every boundary commit and the secret scan enforces.

## 6. Revise round 1 (task_rev `sha256:9976cb2a…a32061d9`): fix commit `d6b93ea9`

The task-level audit of aceb1b14 returned `incorrect` with 5 findings. The orchestrator dispositioned finding 2 (`∕home∕dot_config∕.ssh∕…` passes) as a design limit, out of my scope; the other four are fixed here.

1. **Running user's `$HOME` in the scan (P2): fixed.**
   - `home_path_pattern()` is now the masker's pattern too. It contains the machine-independent forms plus the running user's `$HOME`: a multi-segment home anywhere, a one-segment home with the boundary. `mask_home_paths()` applies exactly that pattern, so masked evidence always passes the scan.
   - The docstring states that the `$HOME` part flags only on the workstation whose home it is, while CI keeps the machine-independent forms.
   - `test_secret_scan_flags_the_running_users_home_as_a_backstop`: `∕srv∕operator∕.ssh∕id_ed25519` in `.orchestration` passes under the real `$HOME` and fails with `HOME=∕srv∕operator`.
   - **Residual risk:** CI's own `$HOME` (`∕home∕runner`) is also flagged anywhere in CI. A runner path glued to a word in evidence masked on a workstation (where the masker matches only the boundary form of other users) would pass locally and fail CI. No tracked evidence has such a path today (the full validator passes and the re-mask changes nothing).
2. **macOS root homes (P2): fixed.** `∕var∕root` and `∕private∕var∕root` match any child, and only plain `∕root` keeps the bare-or-`.<dir>` restriction (the `ponytail:` comment is narrowed to plain `∕root`). The tests cover:
   - `∕var∕root∕Library∕Keychains∕login.keychain-db` becoming `~/Library/Keychains/login.keychain-db`;
   - `∕private∕var∕root∕Library∕x` becoming `~/Library/x`;
   - `∕proc∕1∕root∕var∕root∕Library∕x` becoming `∕proc∕1∕root~/Library/x`.
3. **Re-mask: run, nothing changed.** The masker printed `masked 0 match(es)` for all 2,432 tracked files (validation file, verbatim), so there is no re-mask commit.
4. **Report wording (P2):** section 3 now separates the eight fixed Bot findings from thread 4181459798. **Design limit, not a fix:** an account named exactly like a top-level entry of the repository's `home/` tree (`dot_config`, `dot_agents`, …) is not matched. The exclusion keeps quoted repository paths such as `${REPO_ROOT}∕home∕dot_config∕…` (T75 audit transcript) intact, and no host of this distribution has such an account. The orchestrator dispositioned the thread `not-applicable` on that basis.
5. **Validation (P3):** the narrated "11" is replaced by verbatim output. I re-ran the task's grep in a scratch worktree at the discarded first re-mask commit `f3181a63` (removed afterwards with `git worktree remove`, no prune). It prints `11` and lists the 11 files (validation file, "Revise round 1").

After d6b93ea9: 92 validator tests, 322 validator+launcher tests and the full `make unit-test` (873) pass, `make validate-agent-assets` passes, and the grep prints 0 (validation file). CI and the Bot wait on d6b93ea9 are in the validation file.

### Codex Bot review of d6b93ea9 (one review, three comments; wait ended 07:36:15Z)

| Thread | Finding | Disposition |
| --- | --- | --- |
| 4181656337 (P1) | Non-ASCII account names (`∕home∕éclair∕.ssh∕id`, `∕Users∕<non-ASCII>∕…`) were not matched. | `fixed:3363ed7a`. The account component is any Unicode word character followed by `[\w.-]*`; the trailing and repository-entry lookaheads use the same class. Tested. |
| 4181656357 (P1) | Under `HOME=∕root`, the `$HOME` alternative bypassed the restricted plain-`∕root` form, so the scan would reject the committed Codex sub-agent ids (`∕root∕t97_evidence_review` in `dotfiles-T86-…-worker-crit.json`), and masking would rewrite them. | `fixed:3363ed7a`. A `$HOME` of `∕root` adds no alternative of its own. The earlier one-segment test now uses `∕root∕.cache`, and a new test keeps `∕root∕t97_evidence_review` under `HOME=∕root`. The full secret scan under `HOME=∕root` passes (validation file). |
| 4181656346 (P1) | A custom home outside `∕home` and `∕Users` (`∕srv∕operator`) is detected only on the machine whose `$HOME` it is, so CI cannot reject it if local masking is skipped. | **In part** `fixed:3363ed7a`: the two common portable relocations `∕var∕home∕<user>` (Fedora Atomic) and `∕export∕home∕<user>` (Solaris/illumos) are machine-independent forms now. Proposed `not-applicable:` for arbitrary locations, because CI cannot know where another machine keeps its homes. The workstation that writes the evidence masks and scans it with its own `$HOME` (finding 1 of this round), and the boundary procedure runs that masker before every boundary commit. |

The re-mask after 3363ed7a changes nothing. Bot wait on the diff head 3363ed7a: `bot: none` (07:49:05Z–08:04:06Z; a transient empty `gh api` poll ended the first loop early, and the wait was resumed in the same log to the original deadline). Main moved again (#278, docs only), so the final head is `6ce4e3b3`, the `gh pr update-branch` merge of `94409ec4`. CI there is green, and `mergeable_state` is `blocked` only by the unresolved threads.

cost (round 1): two commits, two CI rounds; about 20 turns.

## 7. Revise round 2 (task_rev `sha256:7e36cf7a…7cbf7c8`): fix commit `aa556845`

The task-level audit of 6ce4e3b3 returned `incorrect` with 3 findings.

1. **Masker/scan JSON asymmetry (P2): `fixed:aa556845`.** `--mask-secrets` now parses every file as JSON, catching the same errors as `json_strings()` (`ValueError`, `RecursionError`), instead of only files ending in `.json`. A parsed document is masked per key and string value and rewritten in the pr-feedback layout whatever its suffix.
   - `test_masks_json_content_whatever_the_suffix`: a `.md` file holding `{"path":"\/home\/alice\/.ssh\/id"}` masks to `~/.ssh/id` and passes the scan's decoded check, while a `.md` prose file is still masked line by line.
   - **This is also the finding the Codex Bot placed in the body of review 5411302667 on d6b93ea9** ("Parse JSON evidence independently of filename"), not as an inline thread. My round-1 report missed it: the wait loop counted that review, but I read only the inline comments. Disposition: `fixed:aa556845`.
2. **Sandbox record (P3): fixed.** The sandbox file now records the round-1 scratch worktree (created under the scratchpad, removed with `git worktree remove --force`, no prune) instead of "No scratch worktrees".
3. **Re-mask:** run over all 2,432 tracked files, `masked 0 match(es)` each; no re-mask commit.

After aa556845: 94 validator tests, 324 validator+launcher tests and `make unit-test` (875) pass, `make validate-agent-assets` passes, and the grep prints 0. The Bot wait now also ends on a "Codex usage limits have been reached" notice, per the task. PONG decision 1 (pattern capped) stands. CI and the Bot wait on aa556845 are in the validation file.

- **Bot wait on aa556845:** it ended at its first poll (08:33:25Z) on the quota notice "Codex usage limits have been reached for code reviews" (issue comment 5990820625, 08:24:31Z, right after the push), as the task instructs. CI is green. **Final status (checked 2026-10-05 after the round-2 RESULT):** head `aa556845`, `mergeable_state=clean`; the orchestrator resolved all 12 review threads (GraphQL `reviewThreads`: 12 total, 12 resolved).
- **Correction to my round-1 PONG:** it said no Bot review or comment had appeared since 08:04Z. I had checked only reviews and inline comments. An issue-comment quota notice (5990519795, 08:04:34Z, after the round-1 update-branch) existed; it is a notice, not a review.

cost (round 2): one commit, one CI round; about 10 turns.
