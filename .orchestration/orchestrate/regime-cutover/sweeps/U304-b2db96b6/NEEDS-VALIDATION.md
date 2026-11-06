# Needs validation: dotfiles at b2db96b627802c287c4e855bf252309a0d0a298d

No `needs_validation` record is in this run's `findings.json`. One lead would be `needs_validation` once independently verified: `dsh-profile:thak-fs-tool-writes-workspace-git-unguarded`, held as an unvalidated candidate (`REPORT.md` section 5a).

**Trace.**
- The kit patch disables `bash-sandbox` (`home/dot_dsh/profiles/thak/cordis.patch.yml:13-14`), so no kit hook and no permission preset activates. U298's test pins this on main (`tests/unit/test_dsh_hook_coverage.py:260`).
- `tool-fs` stays active, fenced only by `fs-sandbox`'s `workspace-write` under the working directory, with no `.git` exception. These are pinned upstream facts: `fs/tool-fs/src/index.ts:23`, `fs/tool-fs/src/write.ts:113-131`, `bundle/base/cordis.patch.yml:243-247` and `:516-519`, `fs/fs-sandbox/src/index.ts:20-24` and `:113-143`.

**Blockers.**
- Upstream runtime behaviour, read but not observed.
- Deployment: whether dsh is run in a git checkout.

**Local plan, in the required sandbox.**
1. With a scratch HOME and DSH_HOME, loopback only, make a scratch git repository the working directory.
2. Have a stub model answer one write to `.git/hooks/post-checkout`.
3. Check for the file. Stop without running git.

**Owner-observed.** Where dsh is run, and whether `tool-fs` should stay on while `bash-sandbox` is off.

The web-search lead from `sweeps/U227-785658d1` is refuted at this head, with proposed verdict rejected (section 5b). Its own store record's local plan would confirm that refutation.
