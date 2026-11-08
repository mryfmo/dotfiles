# Handout: move the regime-cutover live store out of the main checkout (one time, the operator's hand)

Written 2026-11-08T15:0xZ after PR 739 (U393) merged and `make deploy-kit` installed `regime-store-move` at 62e682f3. The lever is read-only: it judges and prints, you run the lines. Standing order 40: the coordinator never writes the live main checkout; this procedure is that one write, by you, once.

## Before you start

- Close this coordinator session (the Claude Code window that ran the regime today) and any other terminal that runs a kit lever against `~/Workspace/dotfiles`. Line 1 below stops the seats; a coordinator process that keeps writing the live store after line 2 would lose those writes at line 4.
- Expected state before line 1: `hcom list -v` from `~/Workspace/dotfiles` with `HCOM_DIR=$HOME/.local/state/hcom-regime HCOM_TEAM=regime` shows two listening seats (sweep-2-gume, sweep-3-dima; the idle seat sweep-4-zilu that made the store root was stopped at 15:05Z). The store root `~/.local/state/regime-store/dotfiles` exists (mode 0700) and holds no `regime-cutover` directory yet. The coordinator kept writing records after the handout was first written (the operator's `continue` at 15:03Z); step 0 reprints the count of the moment, so nothing on this page needs updating.

## Step 0: print the current procedure (read-only, safe to repeat)

```sh
cd ~/Workspace/dotfiles && ~/.local/bin/common/regime-store-move regime-cutover
```

Expected: the first line `ready: <n> live files; the derived store is absent` (at 15:01Z `<n>` was 1825; every record the coordinator wrote after that raises it, so trust the number this run prints, not this page), then seven numbered lines identical to the ones below except for that count in line 3's comment. If it prints `refused:` instead, stop and paste the message to the coordinator's next session; nothing has changed.

## Steps 1 to 7: run the printed lines in order, each only after the previous one succeeded

```text
1. Stop every seat and end every coordinator process: run regime-stop --all in ~/Workspace/dotfiles (the stop of the kit, regime-start --stop --all), confirm with hcom list -v that no seat of this checkout is alive, and close every session that runs a lever of the kit against it.
2. cp -a ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover ~/.local/state/regime-store/dotfiles/regime-cutover && chmod -R go-rwx ~/.local/state/regime-store/dotfiles/regime-cutover
3. diff -r ~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover ~/.local/state/regime-store/dotfiles/regime-cutover && find ~/.local/state/regime-store/dotfiles/regime-cutover -type f | wc -l   # expect no line from diff and the count <n>
4. git -C ~/Workspace/dotfiles checkout -- .orchestration/orchestrate/regime-cutover
5. git -C ~/Workspace/dotfiles clean -fd -- .orchestration/orchestrate/regime-cutover
6. git -C ~/Workspace/dotfiles pull --ff-only
7. regime-store-move regime-cutover
```

What each line should show:

| line | expected | if not |
| --- | --- | --- |
| 1 | `regime-stop --all` exits 0; `hcom list -v` lists no seat as listening or active | stop the remaining seat by name (`hcom kill <name> --go`) before line 2 |
| 2 | no output, exit 0 | do not continue; the destination is removed with `rm -rf ~/.local/state/regime-store/dotfiles/regime-cutover` and the live store is untouched |
| 3 | no diff line; the count equals `<n>` from step 0 | the copy is incomplete: remove the destination as above and rerun line 2 |
| 4 | no output; `git -C ~/Workspace/dotfiles status --porcelain -- .orchestration/orchestrate/regime-cutover` shows only `??` lines | a modified tracked file left means line 4 failed; rerun it |
| 5 | one `Removing ...` line per untracked record; the status above is then empty | rerun line 5 |
| 6 | `Updating ba051b0d..62e682f3` (or a later main) and `Fast-forward`; 58 or more commits | a refusal names local changes; paste it to the next session, nothing is lost (the derived store holds every record) |
| 7 | `moved: the derived store holds <n> files; the checkout store is clean against HEAD` | paste the message to the next session |

## After line 7 (the coordinator's next session does these; nothing for you)

- Every lever resolves the derived store from now on (`store: derived ~/.local/state/regime-store/dotfiles/regime-cutover` on stderr).
- Records sync 53 lists the derived store (U220) and publishes the rows written after sync 52's listing (the sync 52 verdict, sweep and merge rows; U392 to U394; this handout; the evening state note).
- The seats are relaunched when the next unit needs them (`hcom-seat worker --name sweep-2` and so on).
- The scratch copy of the ignored `.claude/.cc-writes` drafts at `/tmp/regime-cutover-store-dotdirs-2026-11-08T131752Z` can be deleted.
