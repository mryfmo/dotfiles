# Review receipt: dotfiles-T128-aws-cli-macos-review-a01 (round 3)

- reviewer: claude-review-dot-a001 (review seat half; the Codex half runs in parallel)
- previous_receipt: round 2 sha256 `b547826bd1c769c1161554bd82accabfd448ea5d2589f4a823af587060716945` (revise on `adb581da`, one P2 and two P3; overwritten by this file)
- brief: `.orchestration/tasks/dotfiles-T128-aws-cli-macos-review-a01.md` sha256 `13143f6ddf307653881f0081e05e72e62555957f824bf61a995fc79dc6a94788` (round 2 brief plus a "Round 3" section; `diff` against the round-2 copy shows nothing else)
- reviewed file: `.orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md` sha256 `b51b8bfba2d259b710917f5ea0cb333b83768c129da66c38bc3cdddbfd48a585` (copied from the main checkout and hashed before reading)
- origin/main at review: `04590ae9` (unchanged since round 1)

## What changed since round 2 (`diff` of the two copies: lines 40, 82, 85)

- Seat P2 applied: item 1 says `main` returns 3, the download status, when no working `aws` exists, names the Linux test's "download fails, no CLI" case as pinning it, and names the ETag-probe path as the one returning 1; item 4's download test expects 3 "as the Linux case pins".
- Seat P3s applied: row 40 drops `head` and `printf` and notes that `printf` and `read` are builtins and `--head` is curl's flag; item 1 trims the version.txt value and notes the missing trailing newline.
- Codex P2 applied: item 1 classifies a key read or dearmor failure (fail closed before any `gpgv`, the form of `test_key_metadata_failures_stop_before_dearmor_and_gpgv`) and a non-zero install.sh exit (the status returned, no ETag recorded, fail closed).
- Nothing else changed; the front matter is otherwise the round-2 one.

## Checks (stop condition 1 to 4)

1. The new sentences match the sources: `main` returns the status after the status-3 branch (aws_cli.sh:183), the Linux case pins 3 (test_aws_cli_acquisition.py:536), the ETag-probe path returns 1 (aws_cli.sh:162-167); the key path returns on `mkdir`, `gpg --import`, the metadata check and `gpg --dearmor` before `gpgv` (aws_cli.sh:111-123); install.sh exits only with 1 or 2 (29 `error 1` and 9 `error 2` calls in the current script), so its non-zero exit never collides with the download status 3 that `main` treats as fail open. Items 1 to 4 keep the reviewed content; every failure path is now classified.
2. Rows as in round 1 (one per path, two non-path rows, the seven generic rows byte-identical to the template, the new-scripts row naming the one new template); the closed row's test name is verbatim in item 4. 16 controls, 4 claims.
3. Premises 1 and 2 unchanged in text and output from the rounds this seat replayed them (1 with the user's PATH in round 1, 2 from the sandbox in rounds 1 and 2); 3 and 4 replayed from the main checkout after `git fetch` (`17:    awscli`, `21:    gpg`; `16`), equal. Completion clause, cap sentence and disjointness unchanged.
4. `task-consistency-check.py` (origin/main copy, sha256 prefix `ba27c4da`, `--root` the main checkout): `dotfiles-T128-aws-cli-macos-a01.md: OK`; `validate-agent-assets.py --mask-secrets` on a second copy: `masked 0 match(es)`, `cmp` equal.

## Findings

1. P3 (confidence high, no change required) `dotfiles-T128-aws-cli-macos-a01.md:82`: the fail-open classification of status 3 rests on install.sh never exiting 3; today it exits 1 or 2 only. A future install.sh exit 3 would be read by `main` as a download failure and keep a working `aws`; the postcondition would still catch a half-installed release at the next apply. Informational.

Task-file verdict: dotfiles-T128-aws-cli-macos-a01: confirm
