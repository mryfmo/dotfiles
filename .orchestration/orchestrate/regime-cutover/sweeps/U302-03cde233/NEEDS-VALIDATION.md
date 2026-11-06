# Needs validation: dotfiles at 03cde233ff84847ca9177a795cbf0e232e84eea1

No `needs_validation` record is in this run's `findings.json`. Two leads would be `needs_validation` once independently verified. Both are held as unvalidated candidates in the ledger.

## `dsh-profile:thak-fs-tool-writes-workspace-git-unguarded` (carried from run-14)

**Trace.**
- The kit patch disables `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:9-10`), so `hooks-claude-code` and `permission-presets` are pending: upstream injection facts; U298's test, which records them, is not merged into this base.
- `tool-fs` stays active, and its writes are fenced only by `fs-sandbox`'s `workspace-write` under the working directory, with no `.git` exception. These are pinned upstream facts: `fs/tool-fs/src/index.ts:23`, `fs/tool-fs/src/write.ts:1-4` and `:113-131`, `bundle/base/cordis.patch.yml:243-247` and `:516-519`, `fs/fs-sandbox/src/index.ts:20-24` and `:113-143`.
- Nothing on main launches dsh under srt.

**Blockers.**
- Upstream runtime behaviour, read but not observed: `tool-fs` registering under the composed tree, and a `.git` write succeeding.
- Deployment: whether dsh is run in a git checkout.

**Local plan, in the required sandbox.**
1. With a scratch HOME and DSH_HOME, the pinned harness and loopback only, make a scratch git repository the working directory.
2. Have a stub model answer one write call to `.git/hooks/post-checkout` with a harmless marker.
3. Run one headless turn and check for the file. Stop without running git.

**Owner-observed.** Where dsh is run, and whether `tool-fs` should stay on while `bash-sandbox` is off.

## `dsh-profile:web-search-routes-to-the-official-api` (carried)

**Trace.** At this base the base bundle's `web-search-deepseek` and `web-deepseek-api` rows are mounted, because U227f is unmerged (upstream `bundle/base/cordis.patch.yml:467-481`).

**Blocker.** Whether a host launches dsh with `DEEPSEEK_API_KEY` set.

**Local plan.** The store record's own: a loopback stub for the search base URL, with a dummy key. Expect a request here, since the fix is not on this base.

**Owner-observed.** Whether any host exports `DEEPSEEK_API_KEY` where dsh runs, and when U227f merges.
