# U353c round 3 of U353: `router-gh` reads the active host's token alone and holds every component of the credential root, and the handout table carries standing order 5's columns

GOAL
The round-2 audit of PR 724 (verdicts/U353b-9c504ad9.md, class credential-boundary) found two P1s and one P2, each reproduced by the auditor against synthetic files. (1) router-gh:127: the `oauth_token` match inside the `github.com:` block is indentation-blind, so the file gh writes today for one login, which carries the active host's `oauth_token:` row at the block's own depth and the same account's row again under `users: <account>:`, counts as two rows and is refused with exit 2; the documented setup (one `gh auth login --insecure-storage` inside the root) cannot work. (2) router-gh:106: only the root (:99) and the `hosts.yml` leaf (:106) are held against links, so `<root>/gh` as a symbolic link to an outside same-user gh configuration directory passes and its login reaches gh as `GH_TOKEN`: the Router uses a credential outside its promised root. (3) docs/engagement-handout.md:55: the handout table the round added lacks the source and dry-run columns standing order 5 requires (an execution receipt from a scratch HOME, or the operator-only reason for the step). This round is the third audit row of U353 since the start (rounds-check.py, order 36): a fourth round needs a mechanism-change row, so this head closes every finding in full.

SCOPE
The same branch `feat/m26-stage-b-router-settings-and-credential-root` and PR 724; the tree is `/tmp/dotfiles-wt/U353` at 9c504ad9 (clean). May write: `scripts/orchestrator/router-gh` and its copy `home/dot_local/bin/common/executable_router-gh` (the token reader and the component hold), `tests/unit/test_router_settings_apply.py` (the wrapper's tests live there), `docs/engagement-handout.md` (the table's columns), the pins in `home/dot_agents/agent-config.yaml` through `scripts/generate-agent-configs.py` (never by hand) and whatever it regenerates, and the PR body `/tmp/dotfiles-wt/U353-pr-body.md`. Non-goals: hcom-seat, router-settings-apply and their tests stay as 9c504ad9 left them; no second credential source, no Keychain path, no YAML library.

CONTEXT
`router-gh` at 9c504ad9 (:96-146: the root hold, the leaf hold, the shell-only reader loop, the `GH_TOKEN` exec); the file `gh auth login --insecure-storage` writes in gh 2.40 and later (`github.com:` then, two spaces in, `git_protocol:`, `user:`, `oauth_token:`, and `users:` holding each account's `oauth_token:` deeper; the active account's row is the one at the block's own depth); the kit's precedent for a component hold, `seat-login-preflight`'s `claude_config_validate` (every component from the seats root to the shared directory is held absent or a real directory of this user, no link, each judged by its own test); `preferences.md` standing order 5 (the handout columns) and 21 (every producer's status read); `docs/engagement-handout.md` as written at 9c504ad9; the round-2 brief (briefs/U353b-...-round2.md) and the two verdicts.

DATA SHAPE
One active-host token row, read at one depth (the `github.com:` block's own indent, measured from the first row inside the block); one component chain `<root>`, `<root>/gh`, `<root>/gh/hosts.yml`, each held by its own tests before anything is read; one handout table with the columns standing order 5 names.

CHANGE
1. Tests first, red at 9c504ad9, in `tests/unit/test_router_settings_apply.py`: (a) a `hosts.yml` in today's gh form for one account (the host-level `oauth_token:` row and the same account's row under `users:`) makes the wrapper run the fake gh once with `GH_TOKEN` equal to the host-level value; a file whose `github.com:` block holds `users:` rows alone (no active host row) is refused naming no active login, fake gh never runs; a file with two host-level `oauth_token:` rows is refused as today; (b) `<root>/gh` as a symbolic link to an outside same-user directory holding a valid `hosts.yml` is refused naming `<root>/gh`, fake gh never runs; `<root>/gh` as a regular file is refused; a `<root>/gh` directory not of this user is refused (skip with a reason when the harness cannot make one); (c) the handout table carries the source and dry-run columns of standing order 5, each row filled (an execution receipt from a scratch HOME where the step can run there, else the operator-only reason), checked by the docs test the repository uses for handouts if one exists, else by a grep assertion in the module's test for the handout line. 2. `router-gh`: the reader measures the block's depth from the first indented row after `github.com:` and takes `oauth_token:` rows at that depth alone (deeper rows are the `users:` entries and are never read); the hold walks `<root>`, `<root>/gh`, `<root>/gh/hosts.yml` in order, each no link (`-L` first), the first two directories of this user, the last a regular file of this user with mode `?00`, and the physical path of `<root>/gh` (`cd ... && pwd -P`) equal to `<root_phys>/gh`, every producer's status read; the copy identical; the pin regenerated. 3. `docs/engagement-handout.md`: the columns added to the table, the prose beside it adjusted if it names the columns. 4. Green: `uv run --offline --with pyyaml python -m unittest tests.unit.test_router_settings_apply tests.unit.test_hcom_seat tests.unit.test_hcom_seat_dsh tests.unit.test_dsh_profile tests.unit.test_generate_agent_configs tests.unit.test_lint_comparisons tests.unit.test_scratch_git -v` to `/tmp/u353c/full.txt`. 5. Lints as round 2 (shellcheck, shfmt, ruff format --check, prettier, lint-comparisons over the changed paths, render-check, validate-agent-assets); `cmp` of the source and the copy; the pin equal to `shasum -a 256` of the source. 6. One commit on 9c504ad9; the body gains `## Round 3 (U353c)` (what the two P1s and the P2 were, what changed, in the body's own words) and, under the existing `## Verification` heading, a `### Round 3, U353c, head <sha>` subsection with ACCEPTANCE pasted; the `## Verification` line itself stays (the body lever refuses a body that drops it); the Threat table gains a row per path changed.

ACCEPTANCE
1. Tests (a), (b), (c) named with their red lines at 9c504ad9 (`/tmp/u353c/red.txt`) and green lines at the head. 2. The seven modules OK with counts. 3. Every lint 0; cmp 0; the pin equals `shasum -a 256` of the source. 4. `git diff --stat 9c504ad9 HEAD` pasted. 5. The body's `## Verification` heading present once and `Program-Unit: regime-cutover/U353` present once (`grep -c` of each pasted).

VERIFY
ACCEPTANCE pasted into the body's Verification section and the report; the coordinator pushes to PR 724's branch, and the one audit, the sweep and CI follow.

CLOSURE
remove

TRUST
TRUST: the unit trusts gh's own `hosts.yml` layout (the active account's `oauth_token:` row at the host block's depth, every account's row under `users:`) as read from gh's documentation and a file gh 2.40 or later writes, the kit's `claude_config_validate` as the shape of a component hold, and the fake gh on PATH as the proof that no gh ran on a refusal.

TIMEBOX
45 minutes.

FORBIDDEN
No read grant of the credential root to any role but router; no token in any file of the repository or the store; no `gh` call against GitHub; no network; no push; no pin edited by hand; no rebase; no change to hcom-seat or router-settings-apply; no pipe `|` in any bash command (standing order 46: output to a file under `/tmp/u353c/`, then read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46, 49; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 56)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U353`. The worktree is yours alone; your final line is the Task return.
- Progress line at `../U353c-progress.txt`; final report to `../U353c-report.txt`.
- Commit unsigned: `git -c commit.gpgsign=false commit`. The commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

REPORT
Status, head sha (40 hex), the three tests with red and green lines, the ACCEPTANCE lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 5, 21, 24, 27, 29, 34, 36, 44, 46, 49); `verdicts/U353b-9c504ad9.md`; `verdicts/U353-8791100f.md`; the U353 and U353b briefs; `handouts/m25-agent-github-account.md`.
