# U311b round 2 of U311: the README asset table names the versioned AWS CLI archive

GOAL
Codex's review of PR 713 (comment 4498953617, P2, frequency 10 severity 2): `README.md:1230` still says the AWS CLI is acquired from the unversioned archive, while the U311 head installs the release `v2/version.txt` names from `awscli-exe-linux-<arch>-<version>.zip` and its `.sig` (macOS: `v2/install.sh --version <v>`). The asset table documents the opposite of the mechanism. A weight-20 finding is fixed in a new head.

SCOPE
The same branch `fix/aws-cli-versioned-release` and PR 713; the tree is `/tmp/dotfiles-wt/fix-aws-cli` at 0059848e. May write: `README.md` (the AWS CLI row of the asset table and any sentence near it that names the unversioned archive or the ETag) and the body `../U311b-pr-body.md` (the round-1 body `/tmp/dotfiles-wt/U311-pr-body.final.md` plus a Round 2 section). Not: any code or test.

CONTEXT
`grep -n -i 'aws' README.md` finds the row and the sentences; `home/dot_agents/agent-config.yaml` `assets.aws-cli` keeps `release: latest` with `verify: gpg`. The row should say: the release version.txt names, installed from its versioned archive and signature (Linux) or `install.sh --version` (macOS), verified against the pinned key; no ETag.

DATA SHAPE
One row and at most two sentences in the README, consistent with the installer's shdoc.

CHANGE
1. Edit the README row and sentences. 2. `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0; `uv run python -m unittest tests.unit.test_supply_chain_policy tests.unit.test_aws_cli_acquisition` OK (a test may pin README text). 3. Commit `docs(readme): the AWS CLI asset row names the versioned archive version.txt selects (regime-cutover U311b)` with the trailer. 4. The body: the round-1 body plus `## Round 2` quoting the Codex finding and the row's new text.

ACCEPTANCE
1. `grep -n -i 'unversioned' README.md` prints nothing about the AWS CLI (pasted). 2. prettier exit 0; the two test modules OK (counts pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section.

CLOSURE
remove

TRUST
TRUST: the unit trusts the installer's shdoc at this head as the description of the mechanism; it changes no code, reads no credential, runs no installer.

TIMEBOX
15 minutes.

FORBIDDEN
No code or test change; no local bats; no network; no push; no `gh` call; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u311b/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 62)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/fix-aws-cli`.
- Progress line at `../U311b-progress.txt`; final report to `../U311b-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the row's new text, the ACCEPTANCE lines. Under 6 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 44, 46); PR 713 comment 4498953617; `verdicts/U311-0059848e.md`.
