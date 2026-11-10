# U311 the AWS CLI installer installs the release version.txt names from its versioned archive and signature

GOAL
The operator's Ubuntu `make update` (2026-11-07 JST morning, aarch64) stopped in `.chezmoiscripts/ubuntu/04-install-aws-cli.sh` with `gpgv: BAD signature from "AWS CLI Team <aws-cli@amazon.com>"`, and passed on the re-run. Cause, measured by the coordinator on 2026-11-06T2xZ: `install/common/aws_cli.sh` downloads AWS's mutable `awscli-exe-linux-<arch>.zip` and its mutable `.sig` as two requests (lines 136-139). AWS writes the two objects minutes apart (aarch64 archive Last-Modified 2026-11-06 20:20:13 UTC, its `.sig` 20:21:03 UTC), so a run in that window, or behind an edge that still caches the old `.sig`, pairs the 2.39.6 archive with the 2.39.5 signature. The log's "Signature made 2026-11-06 04:17:52 JST" equals the creation time of `awscli-exe-linux-aarch64-2.39.5.zip.sig`, and that signature against the 2.39.6 archive gives the same `BAD signature`, exit 1, in ubuntu:24.04 arm64 with the real key and the real objects (`/private/tmp/aws-cli-fix/repro.sh`). The same installer runs on macOS through `v2/install.sh`, which reads version.txt a second time when it gets no `--version`. The installer is part of the kit's unattended `make update` on both hosts (goal clause 「両ホスト」; handoff/08 §4 row 1).

SCOPE
Branch `fix/aws-cli-versioned-release` from `origin/main`; the tree is `/tmp/dotfiles-wt/fix-aws-cli` (created by the coordinator before this brief). May write: `install/common/aws_cli.sh`, `tests/unit/test_aws_cli_acquisition.py`, `tests/unit/test_network_bounds.py` (the one exemption that names a deleted line), `home/.chezmoiremove`, and the body `../U311-pr-body.md`. Not: `home/dot_agents/agent-config.yaml` (`release: latest` stays accurate: the release version.txt names), the chezmoi script templates, any other installer, lines 15-16 of the installer (rendered constants).

CONTEXT
Read the installer whole and the whole test module before editing. Read `/private/tmp/aws-cli-fix/sketch.md` (the design with its evidence and the rejected alternative) and the facts verified against AWS on 2026-11-06: `https://awscli.amazonaws.com/v2/version.txt` prints `2.39.6`; `awscli-exe-linux-<arch>-<version>.zip` and `.zip.sig` exist for 2.39.5 and 2.39.6 and are written once; the versioned 2.39.6 `.sig` is byte-identical to the current `latest` `.sig`; `v2/install.sh` accepts `--version X.Y.Z`, validates it with `^[0-9]+\.[0-9]+\.[0-9]+$`, and then downloads `AWSCLIV2-<version>.pkg` without reading version.txt. The network-bounds test exempts curl lines by exact text (`tests/unit/test_network_bounds.py:289-295`); the comparison lint baselines the three `aws-cli/...` string comparisons of the installer (`scripts/lint-comparisons-baseline.tsv:18-20`).

DATA SHAPE
One `version` string per run (for example `2.39.6`), read once from version.txt in `main`, is the release identity; every URL derives from `(kernel, architecture, version)`; the installed identity is what `aws --version` prints, `aws-cli/<version>`, which `verify_aws_cli_install` already compares. No state file.

CHANGE
1. Commit 1 (the failing test first): one test asserting that a Linux run requests `v2/version.txt`, then `awscli-exe-linux-x86_64-2.39.6.zip` and its `.sig`, and never the unversioned archive. It fails on `origin/main`. Commit it alone.
2. Commit 2 (the fix): `aws_cli_release_version` (one bounded curl of version.txt, whitespace stripped, `X.Y.Z` required, else one stderr line and return 1); `aws_cli_url <version>` (Linux the versioned archive, Darwin `v2/install.sh`); `install_aws_cli <version>` (signature `${archive_url}.sig`; macOS runs `bash install.sh --version "$1"`; Linux requires the staged `aws/dist/aws` to report `aws-cli/$1`, then the same-version-directory repair, `aws/install --update` and `verify_aws_cli_install "$1"` unchanged); `main` reads the version once, takes the existing unreachable branch when the read fails, skips with `verify_aws_cli_install "${version}" > /dev/null 2>&1`, keeps the exit-3 handling; `AWS_CLI_ETAG_FILE`, `aws_cli_archive_etag` and the ETag write are deleted; shdoc rewritten for the version flow; `.local/state/dotfiles/aws-cli-archive.etag` added to `home/.chezmoiremove`. The ETag tests become version tests (the stub serves version.txt text; assertions move to whether the installer ran and to the URL list), plus: a 404 on the versioned archive with a working CLI returns 0 with the download warning; a version.txt that is not `X.Y.Z` downloads nothing after it (warning with a working CLI, failure without); the macOS installer receives `--version <v>`. The stale exemption in `test_network_bounds.py` goes.
3. The body: Summary (the operator's log quoted), Contract (the archive and the signature are the same release's write-once objects named by one version.txt read; a bad signature or a failed postcondition still fails loudly and never replaces a working CLI; a failed download keeps a working CLI; Left out: downgrade refusal, retry loops, the orphaned ETag file's removal beyond `.chezmoiremove`; the TRUST sentence below), Verification (ACCEPTANCE pasted).

ACCEPTANCE
1. `uv run python -m unittest tests.unit.test_aws_cli_acquisition tests.unit.test_network_bounds tests.unit.test_lint_comparisons tests.unit.test_supply_chain_policy tests.unit.test_validate_agent_assets tests.unit.test_scratch_git -v` OK (counts pasted); the commit-1 test named, with its failing run at commit 1 pasted.
2. `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0; `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0; `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `make shellcheck` exit 0; `make render-check` exit 0.
3. `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
4. `/private/tmp/aws-cli-fix/repro.sh /tmp/dotfiles-wt/fix-aws-cli` exit 0: the request log names `v2/version.txt`, the versioned zip and its `.sig`, never the unversioned pair, and the last line prints `aws-cli/2.39.6` (the coordinator's measurement on the real surface; the worker runs it too when docker is reachable).

VERIFY
ACCEPTANCE pasted into the body's Verification section. The coordinator re-runs item 4 on the pushed head and, after the merge and `make update` on the macOS laptop, the installer's skip path (`aws --version` equals version.txt, exit 0, no download).

CLOSURE
remove

TRUST
TRUST: the unit trusts AWS's published signing key at the pinned fingerprint and the write-once versioned objects that key signs; it reads version.txt as data and accepts only `X.Y.Z`; it trusts nothing else from the network, reads no credential, and writes under `$HOME` only through the installer's own paths inside the test fixtures.

TIMEBOX
45 minutes.

FORBIDDEN
No change to `home/dot_agents/agent-config.yaml`; no retry loop; no downgrade guard; no local bats; no push; no `gh` call; no write under `~/.omp`, `~/.dsh`, `~/.agents`, `~/.local`, `~/Workspace`; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u311/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/fix-aws-cli` and the coordinator fetches it by path.
- Progress line at `/tmp/dotfiles-wt/U311-progress.txt` after every step; final report to `/tmp/dotfiles-wt/U311-report.txt` before you end; deliverables beside the worktree under `/tmp/dotfiles-wt/`, never in the store.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes: the two mutable reads go, not a retry; Laziness Protocol: the state file is deleted, not migrated).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat` against the merge base, no fetch), the ACCEPTANCE result lines, deviations. Under 10 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 41, 42, 44, 46, 47); `handoff/08-purpose-and-goal.md` §1 「両ホスト」 and §4 row 1; `decisions.tsv` 2026-11-06T22:3xZ (goal-check); `/private/tmp/aws-cli-fix/sketch.md`.
