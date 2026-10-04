# Report: dotfiles-T92-stop-gate-sandbox-placeholders-a01

- Worker: `claude-standard-dot-a007` (worktree `.claude/worktrees/worker-e`). `task_rev` `sha256:32a78d26…c9c2befc` was verified before work started.
- PR: https://github.com/mryfmo/dotfiles/pull/248 (`fix/stop-gate-sandbox-placeholders` → `main`). Final head **`bbd3d3fbe547bde807e169c923d6659857c984b7`**, current with `main` `f32f33a0`; CI is all green.
- The Codex Bot posted "Didn't find any major issues" with "Reviewed commit: bbd3d3fbe5" at 06:40:04Z.
- Status: ready_for_review. `plan-mode-used=none`.

## Cause (reproduced)

Inside the Claude Code sandbox, a worker worktree carries the same 19 untracked placeholders that the orchestrator reported (`.zshrc`, `.claude/agents`, …).
- `ls` shows each as a 0-byte, mode 0444 file, and `mountpoint .zshrc` reports a mount point.
- In `/proc/self/mountinfo` each is a bind mount of the path onto itself with `ro` options: 26 of 26 mounts under the worktree.
- `git status` lists all 19 as `??`. The Stop hook runs in that mount namespace, so the merged gate counted them as dirty.

## Fix

The orchestrator seat's dirty-tree loop skips an untracked entry when **all** of these hold:
- the path is listed, exactly, as a mount point in field 5 of `/proc/self/mountinfo`;
- that mount's options (field 6) start with `ro`;
- the path is a character device (a `/dev/null` mask) **or** an empty regular file.

`sandbox placeholders ignored: <n>` is printed only when the gate blocks for another reason, so a clean stop stays silent. The header `@description` explains the skip.

Live in the sandbox, 19 of 19 untracked entries match the final predicate, and a freshly created file does not.

## Deviations from the task text (each forced by a Codex P1; evidence in validation)

1. **`mountpoint(1)` is not used**, so no fallback is needed:
   - **One `mountpoint` process per untracked path (P1 4176318316):** with many untracked files this could outlive the 5 s hook timeout. The mount table is now read once (one `awk`): 600 untracked files take 0.96 s with per-path `mountpoint` and 0.09 s now.
   - **`mountpoint` follows symlinks (P1 4176318319):** an untracked symlink to `/` was skipped. Exact path matching against mountinfo never follows a symlink.
2. **The test override is an argument, not an environment variable.** An inherited `AGENT_STOP_GATE_MOUNTINFO` could have pointed the gate at a fabricated mount table (P1 4176428485). Tests now use `--mountinfo <file>`, documented as test-only in `@option`. The Stop hook in `settings.json` passes no arguments, so a launcher's environment cannot redirect `/proc/self/mountinfo`.
3. **The placeholder must look like Claude's**, as an empty regular file or a char device on a read-only mount:
   - **A user's own bind mount of a real file is not skipped (P2 4176359774).**
   - **Read-only comes from the mount options, not `-w`:** `-w` would mis-classify every placeholder when the hook runs as root (P1 4176394555).
   - **Character-device masks are accepted too (P1 4176428492).** In this Claude Code version the masks are 0-byte regular files bound onto themselves.
4. **Tests.** The fake-`mountpoint` test was replaced by fixture tests through `--mountinfo`. Fixtures are written as the kernel would: resolved directories, octal escapes. macOS CI failed before this because `/var` is a symlink there. The tests:
   - placeholders skipped while a real file still blocks, with the note;
   - a symlink to `/` is reported;
   - a nonempty user bind mount is reported;
   - an `rw` mount is reported;
   - a character-device mask is skipped;
   - the environment cannot redirect the mount table.

   Every test fails on the script before its fix (pasted). The char-device test also fails on the final script with the `-c` clause removed.

## Review threads (every unresolved thread on PR #248; replied inline on the fixed ones, none resolved)

| Thread | Finding | Disposition |
|---|---|---|
| 4176318316 (P1) | `mountpoint` per untracked path | `fixed:776cbfecf19c1e2224504b150dd6347cf2911bb9` |
| 4176318319 (P1) | `mountpoint` follows symlinks | `fixed:776cbfecf19c1e2224504b150dd6347cf2911bb9` |
| 4176359774 (P2) | every untracked mount treated as a placeholder | `fixed:5d4928fbecde430420e81a769a6bc4fdc0179d64` |
| 4176394555 (P1) | `-w` is wrong for root | `fixed:68d8e142b9594d8ae5d223dc048b4ad444be7f29` |
| 4176428485 (P1) | env override could bypass the gate | `fixed:bbd3d3fbe547bde807e169c923d6659857c984b7` |
| 4176428492 (P1) | character-device placeholders | `fixed:bbd3d3fbe547bde807e169c923d6659857c984b7` |
| 4176428488 (P2) | an empty read-only user bind mount is indistinguishable | proposed `not-applicable:` such a file is empty, so a skip loses no content; it is mounted read-only in the orchestrator checkout, so no edit can be pending on it; and its mountinfo shape (an `ro` self-bind of an empty file) is exactly the sandbox placeholder's, so no further test separates them without the sandbox's private configuration. |

## CompactionDB

```
cd /home/moriya/Workspace/dotfiles && python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content 'dotfiles-T92 (orchestrator 2026-10-04): the agent stop gate ignores untracked paths that are mount points in its own namespace, because the Claude Code sandbox bind-mounts 0-byte placeholders for protected paths into the repository root and the Stop hook runs inside that namespace.'
```

Output: `74bc8922-86c4-48f7-bdf1-a9e72198761e`.

[memory:decision] dotfiles-T92: a sandbox placeholder is recognized from `/proc/self/mountinfo` read once: an exact path match with `ro` mount options, on an empty regular file or a character device. The table cannot be redirected through the environment; tests pass `--mountinfo <file>`.

## Notes

- CI on intermediate heads:
  - `cbbd26cd`: the macOS test failed because fixture paths were unresolved (`/var` → `/private/var`), and the Linux jobs were cancelled by fail-fast.
  - Later heads: green.
- `main` moved twice; the branch was updated (`164cc220`, `77798622`). The last code commits sit on `f32f33a0`, which is still current.
- The Understand-Anything hook did not fire.

cost: n/a (Claude Code does not expose session token or cost figures to the worker)

## Revise round 1

`task_rev` `30580db0…` was verified. Status: ready_for_review.

- **Item 1, P2: a read-only bind of *another* empty file was skipped.** Fixed in **`adca1e6b1f8cac91bd7f18a25f48728dd297b0c1`**. The mount table is read once, now with mountinfo fields 4-6, and tagged:
  - `S<path>`: an `ro` self-bind, where root (field 4) equals the mount point;
  - `N<path>`: an `ro` bind whose root is `/null`.

  An empty regular file needs an `S` entry; a character device needs an `N` entry. Anything else is reported, including an empty `ro` bind from elsewhere. The `/dev/null` branch keeps the earlier char-device fix (4176428492) working: such a mask's root is `/null`, never its own path. Test: `test_read_only_bind_of_another_empty_file_is_not_a_placeholder`, with fixture root `/srv/empty.env`. Live: all 26 mounts under the worktree are `ro` self-binds.
  - This supersedes the proposed not-applicable on Bot thread 4176428488, which is now `fixed:adca1e6b1f8cac91bd7f18a25f48728dd297b0c1`. The orchestrator re-replies.
- **Item 2, evidence as summaries.** The validation file now has executable commands with raw output:
  - a mutation harness (source pasted) that removes each property of the predicate from the final script in turn and runs the test guarding it;
  - the live predicate loop, with its copy of the gate's predicate checked identical by `diff`;
  - the 600-file timing script (source pasted).

  The mutation run **found a weak test**. The symlink test pointed at `/`, a directory, so the file-type check rejected it before any mount matching, and a "follow the symlink" mutation survived. Commit **`153a647d50d9f4af09809e9ac012a2e0ecdefa53`** points the link at an empty read-only file that is itself a listed self-bind. All 7 mutations now fail their guarding test, and the unmutated script passes.
  - Live result: 19 of 19 untracked entries are placeholders, and a freshly created file is `REPORTED`.
  - Timing: 600 untracked files take 0.85 s on `cbbd26cd` and 0.13 s on the final script, both rc=2 with 600 reasons.
- **Item 3, a mislabelled command.** The validation entry is corrected to the command that actually ran (`--jq '.head.sha, .mergeable_state'`). The new section records `.head.sha` and `.mergeable_state` as two separate commands.
- **Final head `153a647d50d9f4af09809e9ac012a2e0ecdefa53`:** CI is all green, and the branch is current with `main` `0ea5948b` (merge `8d54bd3f`). `mergeable_state` is `clean`.
  - The Codex Bot reported "Didn't find any major issues" on `8d54bd3fb4` (07:20:07Z) and on `153a647d50` (07:23:00Z).
  - All 7 review threads are resolved (GraphQL `isResolved == true`), and no new thread was opened.
- **Local:** 42 gate tests pass, `make unit-test` 758 OK, `make validate-agent-assets` ok, and ShellCheck/shfmt are clean.
- **Commits this round:** two (code plus test, then a test-only hardening found by the requested evidence work). Both are on the PR.

cost: n/a

## Revise round 2

`task_rev` `780ac8ee…` was verified. Status: ready_for_review.

- **The instructed fix, commit `8535b3f34628434c81fcb88bba1c1a45d5f241ad`:** a self-bind became a mount point that *ends with* its root, so `/home` as its own filesystem works. Tests: a separate-filesystem fixture and a whole-filesystem bind (root `/`). Root `/` turned out to be excluded by construction, because no mount point ends in `/`; the mutation run showed the guard was redundant, so it was dropped.
- **The Bot review of `8535b3f3`** then found the suffix rule too loose (P2s):
  - **4176646780:** a same-named file bound from elsewhere, such as `/foo` over `<repo>/any/foo`, was accepted.
  - **4176646783:** a `null` device of another filesystem passed as a `/dev/null` mask.

  Both are fixed in **`a8a87bd985cfabdc40698cd0757a7fc8cc2ff2d1`**. Each mount's root is joined onto the mount point of its source filesystem's own root mount (same device in field 3 with root `/`, from a first pass over the same table, still one `awk`):
  - **Self-bind:** an empty file whose joined path is its own mount point. This covers both the same-filesystem and the separate-`/home` layout.
  - **`/dev/null` mask:** a character device whose joined path is `/dev/null`.

  Live, the root filesystem `259:2` has its root mount at `/`, and `/dev/null` is `udev` root `/null` with `udev` mounted at `/dev`. Tests: `test_same_named_file_bound_from_elsewhere_is_not_a_placeholder` and `test_null_device_of_another_filesystem_is_not_a_placeholder`. The fixtures now carry filesystem-root lines for `/`, a separate first-component filesystem, `/dev` and `/other-dev`.
- **Evidence (verbatim in validation):**
  - **Mutation harness:** 11 mutations, including the round-1 equality rule and the round-2 suffix rule as mutations. Each fails its guarding test, and the unmutated script passes.
  - **Live predicate in the sandbox:** 19 of 19 untracked entries are placeholders, and a fresh file is `REPORTED`.
  - **Validation:** 46 gate tests pass, `make unit-test` 762 OK, `make validate-agent-assets` ok.
- **Final head:** `3371cc818276df49ceeae78c17f3f16d7661375e`, a merge of `main` `65915b93` that touches no PR file.
  - **CI:** all 13 checks are `SUCCESS`. One earlier run on `a8a87bd9` failed in `public-bootstrap (macos-14)`, and the other bootstrap job was cancelled by fail-fast. Job log excerpt (`gh run view --job 111393109184 --log`, pasted in full in validation "Corrected command evidence"): `✘ Failed to add marketplace: Fetching the marketplace from GitHub failed on both attempts. HTTPS (https://github.com/tomasz-tomczyk/crit.git): Failed to clone marketplace repository: Network error or timeout while cloning repository.` followed by `##[error]Process completed with exit code 1.` The merge-head run is green.
  - **Codex Bot:** "Didn't find any major issues" on `a8a87bd985` (08:06:51Z) and on `3371cc8182` (08:24:43Z), with no new threads.
- **Unresolved threads:**
  - 4176646780 → `fixed:a8a87bd985cfabdc40698cd0757a7fc8cc2ff2d1`
  - 4176646783 → `fixed:a8a87bd985cfabdc40698cd0757a7fc8cc2ff2d1`

  Both have inline replies; neither is resolved. The other seven are resolved.
- **Commits this round:** two. The instructed fix, then the Bot's P2s on that head under the "fix and repeat" rule.

cost: n/a
