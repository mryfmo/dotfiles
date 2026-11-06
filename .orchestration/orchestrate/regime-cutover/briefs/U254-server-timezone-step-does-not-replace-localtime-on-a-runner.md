# U254 the server timezone step is idempotent and never replaces /etc/localtime on a GitHub runner

GOAL
Since 2026-11-06T00:52Z every `public-bootstrap (ubuntu-24.04, server)` job of `.github/workflows/remote.yaml` stalls after about 37 s of the bootstrap step and is cancelled at 35 minutes, on main and on every pull request, so no program pull request can merge. Six probes bisected it today (decisions rows of phase `ci`, 07:21Z to 08:1xZ): with the timezone step rendered empty the leg passes in 8 min (PR 681); with only `apt-get install -y tzdata` it passes (PR 685); with only `echo Asia/Tokyo | sudo tee /etc/timezone` it passes (PR 690); with `sudo ln -snf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime` kept it stalls (PRs 684, 689), and so does `timedatectl set-timezone` (PR 688, which also rewrites `/etc/localtime`). The kit diff between the last pass and the first stall is a comment-only bats edit, so the trigger is on the runner's side (inferred: the runner stops reading the step's output once `/etc/localtime` changes, which is why four dump probes never ended; the mechanism is not measured). The kit's intent stands for real servers: `install/ubuntu/server/setup_timezone.sh` sets `Asia/Tokyo`. This unit keeps that for hosts and makes the step do nothing where it cannot: when the zone is already set, and on a GitHub runner, whose clock is not the kit's to set.

SCOPE
A new branch `fix/server-timezone-step-on-a-runner` from `origin/main` b49be338 (your tree is `/tmp/dotfiles-wt/U254`). May write: `install/ubuntu/server/setup_timezone.sh`, its tests under `tests/install/ubuntu/server/` (find the bats file that covers the server scripts, or add `setup_timezone.bats` beside its siblings in the existing form), `home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl` only if the template must pass something new (it includes the script; prefer no change), and the body `../U254-pr-body.md`. Not: the workflow (the bound and the dump of the probes are not merged), the client scripts, `setup.sh`.

CONTEXT
`install/ubuntu/server/setup_timezone.sh` at b49be338: `main()` exports `TZ=Asia/Tokyo`, runs `sudo ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime`, `echo "${TZ}" | sudo tee /etc/timezone`, `sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata`; `set -Eeuo pipefail`; the `BASH_SOURCE` guard at the end. The chezmoi template `home/.chezmoiscripts/ubuntu/run_once_50-server-setup-timezone.sh.tmpl` includes it for `linux` + `debian`-like + `.system == "server"`. The repository's bats tests for install scripts live under `tests/install/ubuntu/` (read `tests/install/ubuntu/client/misc.bats` for the fixture style: a fake `sudo` first on PATH that records its argv, `run`, assertions on the recorded calls; AGENTS.md Test Policy: bats runs in CI only, never locally; your local gates are shellcheck, shfmt and a `bash -n`). GitHub sets `GITHUB_ACTIONS=true` in every step (documented default variable). `readlink -f /etc/localtime` prints the zone file the link resolves to (`/usr/share/zoneinfo/Asia/Tokyo` when set, `/usr/share/zoneinfo/Etc/UTC` on the runner image).

DATA SHAPE
One decision function and one effect. `wanted_zone` is `Asia/Tokyo`; `current_zone_file` is `readlink -f /etc/localtime` (empty when unreadable). The step has three outcomes, printed as one line each: `timezone: already ${TZ}` (the resolved file ends with `/${TZ}`), `timezone: unchanged on a GitHub runner (GITHUB_ACTIONS is set; replacing /etc/localtime stalls the runner, regime-cutover U254)`, or the change (ln, tee, and the tzdata install as today). `apt-get install -y tzdata` runs only on the change path (it is the package the zone files come from; the runner has it). No new flag, no new variable beyond the two reads.

CHANGE
1. `setup_timezone.sh`: `main()` per DATA SHAPE; the shdoc header's `@description` says what the step does and the two cases where it does nothing and why (one sentence each, the runner case citing this unit); every producer's exit status read (`readlink` failing reads as "unknown zone", which takes the change path on a host and the skip path on a runner).
2. Tests (bats, CI-run): with a fake `sudo` and a fake `readlink` (or a scratch `/etc/localtime` is not writable, so stub the read through a function the test can override, in the form the sibling tests use): (a) on a host whose link already resolves to Asia/Tokyo, no `sudo` call is recorded and the `already` line prints; (b) with `GITHUB_ACTIONS=true` and a UTC link, no `sudo` call is recorded and the runner line prints; (c) on a host with a UTC link and `GITHUB_ACTIONS` unset, the three `sudo` calls are recorded in order (`ln -snf ... /etc/localtime`, `tee /etc/timezone`, `apt-get install -y tzdata` with `DEBIAN_FRONTEND=noninteractive`); (d) a `readlink` failure on a host takes the change path.
3. The body `../U254-pr-body.md`: Summary (the stall, the six probes with their PR numbers and results, the inference about the runner labelled as such), Contract (guarantee: the server bootstrap on a GitHub runner never replaces `/etc/localtime`; on a host the zone is set once and the step is idempotent; leaves out: the runner-side mechanism, which is not measured, and the probe workflow changes, which are not merged), Threat table (the script, the test, the template if touched; the `GITHUB_ACTIONS` read as the only environment-dependent branch), Verification (ACCEPTANCE pasted), and one sentence that this PR's own server leg is the proof (it must pass where every other leg stalls).

ACCEPTANCE
1. `bash -n install/ubuntu/server/setup_timezone.sh` exit 0; `make shellcheck` exit 0.
2. `scripts/ci/run-on-lint-files.sh shell shfmt -i 4 -sr -d` exit 0, `scripts/ci/run-on-lint-files.sh python ruff format --config ruff.toml --check` exit 0, `scripts/ci/run-on-lint-files.sh markdown prettier --check` exit 0.
3. `GITHUB_ACTIONS=true bash -c 'source install/ubuntu/server/setup_timezone.sh; main'` on this macOS host prints the runner line and calls no sudo (paste it; the script's `readlink -f` form must work on macOS or the test stubs it, say which).
4. `uv run python -m unittest tests.unit.test_scratch_git` OK; `uv run --no-project --with pyyaml scripts/lint-comparisons.py --changed` exit 0.
5. `grep -c 'GITHUB_ACTIONS' install/ubuntu/server/setup_timezone.sh` prints 1 or 2 (the read and the message).

VERIFY
ACCEPTANCE pasted into the body's Verification section. CI's `public-bootstrap (ubuntu-24.04, server)` on the PR is the proof of the unit; the coordinator reads it.

CLOSURE
allowlist

TRUST
TRUST: the unit trusts the six probes' results as the bisect (the PR numbers in GOAL) and GitHub's documented `GITHUB_ACTIONS` variable as the runner mark; it reads no network, changes no workflow and does not explain the runner's mechanism.

TIMEBOX
40 minutes.

FORBIDDEN
No change to `.github/workflows/`, `setup.sh` or any client script; no local bats run (AGENTS.md Test Policy); no `sudo` on this host; no network; no push; no `gh` call; no pipe `|` in any bash command you run (standing order 46: write output to a file under `/tmp/u254/` and read it).

WORKER RULES (standing orders 21, 27, 29, 31, 34, 44, 46; read `~/Workspace/dotfiles/.orchestration/orchestrate/regime-cutover/preferences.md` lines 23 to 58)
- Never run git or edit files in `~/Workspace/dotfiles`, never push, never open or edit a PR, never edit the live store; you stop at a committed head in `/tmp/dotfiles-wt/U254` and the coordinator fetches it by path.
- Progress line beside your tree (`../U254-progress.txt`) every ten minutes at most; first edit within ten minutes.
- Commit unsigned: `git -c commit.gpgsign=false commit`. Every commit message ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Comments explain a non-obvious why only, no phase narration. Shell comments are English shdoc.
- Follow `~/.agents/pstack/skills/poteto-mode/SKILL.md` (Fix Root Causes: the guard is a fix because a runner whose clock is not ours is a legitimate state; Make Operations Idempotent).

REPORT
Status, head sha (40 hex), files changed (`git diff --stat origin/main`), the ACCEPTANCE result lines, deviations. Under 12 lines, ending with `head=<40 hex>`.

STANDING
`preferences.md` (standing orders 21, 27, 29, 34, 35, 37, 41, 44, 45, 46); `AGENTS.md` (Test Policy, threat table); the `decisions.tsv` rows of phase `ci` on 2026-11-06 (the probes).
