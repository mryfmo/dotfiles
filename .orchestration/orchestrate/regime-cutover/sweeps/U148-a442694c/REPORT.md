# Security audit report: dotfiles @ a442694c

## 1. Run

- Source ref: `a442694c439b035e5d27c1213fc4bc2801e24998` (U148 round-3 head, PR 646, branch `feat/kwp-skills-subset`; detached, clean worktree). It is an empty commit on the round-2 head c44a7c6c: both commits have tree d711989c and no path differs (the commit exists so the audit reads the corrected pull request body).
- Profile: `standard`; scope: the whole repository at this head; no budget set.
- Execution: sandboxed-source-and-local-only. Nothing from the target was built, tested or executed (brief U162), so every candidate that needs execution for proof is `needs_validation`.
- Prior runs: run-7 (U148 round-2 head c44a7c6c, the parent of this head) was read whole and carried; run-1 and run-2 are reached through it, and run-3 to run-6 and run-8 to run-10 (U147 and U150 heads) are other branches, read and not carried. With an identical tree every unit is `prior_covered_same_source` (or carried deferred or not applicable as it was) and its five `needs_validation` records hold unchanged (every cited line re-read). No candidate is new; see section 2.
- Agent independence (read this first): the seat exposes no delegation tool (`task` and `eval` are blocked by user policy), so one agent ran every role in sequence (reconnaissance, hunters, critics, candidate verifiers, record verifiers). The per-role agent IDs in the ledger (`h11-*`, `v11-*`, `r11-*`, `critic11-*`) are separate passes with separate `agents/<id>/` directories, not independent agents. The independence the skill asks of verifiers is therefore procedural only, which is one more reason no record is `confirmed`.
- Coverage: partial. 20 units covered, 5 candidate, 8 deferred, 5 not applicable (of 38). The post-wave critic queued the deferred units; the final-clean critic did not pass clean because they remain, so no complete-coverage claim is made.
- Status: advisory. These records are input to the coordinator's ledger, never a verdict.

## 2. Posture

This head changes no file, so it adds no candidate: the kwp skill copies, their drift test, symlinks and audience lines are byte-identical to run-7's review. Run-2's hardening note stands unchanged: the port turns the upstream connector gates into 'any tool of that kind in this session', and the incident-response and change-request skills name outward actions (paging, posting to channels) while their audience includes the unattended omp seats (section 6). The five carried leads are unchanged from run-1: write roots granted to one sandbox (Claude Code, or a seat's srt) include files that a later, unsandboxed process executes or trusts, plus one destructive timer job that parses paths unsafely. The rest of the repository keeps the posture run-1 recorded: verified downloads, CI that never runs PR code with write tokens or fork-reachable secrets, a full-match approval hook, and generated, probed seat containment.

## 3. Confirmed findings

None. No record reached `confirmed`: confirmation needs a bounded local observed result, and this run could not execute anything.

## 4. Confirmed finding details

None (see section 3).

## 5. NEEDS VALIDATION

| # | Lead | Repository trace | Exact blocker | Bounded local next step | Owner-observed check |
|---|---|---|---|---|---|
| 1 | Claude Code sandbox write roots expose hcom launch inputs and seat sandbox files that later run unsandboxed (`claude-sandbox:allow-write-covers-seat-launch-inputs`) | `home/.chezmoitemplates/claude-settings-managed.json:568` -> `home/.chezmoitemplates/claude-settings-managed.json:575` -> `home/dot_claude/modify_private_settings.json:272` -> `scripts/orchestrator/README.md:259` | hcom's consumption of config.toml, env, config.env, scripts, integrations, .tmp/launch and shell_env.json at seat launch happens in the external hcom binary; the repository only asserts it (README:259). | Under a scratch HOME with a dummy hcom store and the rendered settings, run one sandboxed Claude Code Bash command that appends a benign marker assignment (MARKER=1) to <scratch>/.local/state/hcom/<slug>/env; then launch a dummy seat against a fake omp that prints its environment and check whether MARKER=1 reaches the unsandboxed launch. Stop at the marker. | Owner confirms from the installed hcom version which store files `hcom omp` reads or executes at launch, and checks that ~/.claude/settings.json sandbox.filesystem carries no denyWrite for them. |
| 2 | Seat srt sandbox can write the operator's Claude Code config (~/.claude.json, ~/.claude/rules) that unsandboxed Claude Code sessions load (`hcom-seat:srt-write-roots-share-operator-claude-config`) | `scripts/orchestrator/hcom-seat:1369` -> `scripts/orchestrator/hcom-seat:1680` -> `scripts/orchestrator/hcom-seat:1706` -> `scripts/orchestrator/README.md:173` | Whether Claude Code starts user-scope mcpServers from ~/.claude.json without a prompt and outside its Bash sandbox, and loads every ~/.claude/rules/*.md into sessions, is product behavior not visible in this repository. | In a scratch HOME, render a seat's srt settings with hcom-seat's seat_sandbox_write; inside `srt --settings <file>` add a dummy user-scope MCP server whose command writes a marker file into scratch, and drop a rules file with a harmless marker sentence into <scratch>/.claude/rules/; then start Claude Code with that HOME outside srt and check `claude mcp list`, the marker file, and whether the sentence appears in the loaded memory. Stop there. | Owner inspects ~/.claude.json mcpServers and ~/.claude/rules on a seat host after seat sessions for entries no operator added, and confirms the installed Claude Code version's startup behavior for user-scope MCP servers. |
| 3 | Orchestrator seat can rewrite the Python package that the checkout's Claude Code project hooks import (`hcom-seat:srt-deny-write-misses-claude-hook-package`) | `scripts/orchestrator/hcom-seat:1151` -> `scripts/orchestrator/hcom-seat:1682` -> `.claude/settings.json:9` -> `.claude/hooks/contextdb_hook.py:8` -> `.claude/contextdb/contextdb/hook.py:91` | Whether the operator or coordinator runs Claude Code with this project's hooks enabled in the main checkout (or in a worker worktree) is a deployment fact. | In a scratch copy of the repository launched as a scratch orchestrator seat, inside srt with the rendered settings, append an import-time line that writes a marker file into scratch to .claude/contextdb/contextdb/hook.py and confirm the same write to .claude/hooks/contextdb_hook.py is denied; then start Claude Code in the scratch copy outside srt and check for the marker after SessionStart. Stop there. | Owner confirms whether Claude Code sessions are opened in the main checkout with the project's .claude/settings.json hooks trusted, and compares .claude/contextdb in the checkout with origin/main after orchestrator seat sessions. |
| 4 | disk-gc splits worktree paths on whitespace and can rm -rf a different directory (`disk-gc:worktree-porcelain-path-field-split`) | `home/dot_config/systemd/user/disk-gc.service.tmpl:6` -> `home/dot_local/bin/common/executable_disk-gc:184` -> `home/dot_local/bin/common/executable_disk-gc:186` -> `home/dot_local/bin/common/executable_disk-gc:188` -> `home/dot_local/bin/common/executable_disk-gc:221` -> `home/dot_local/bin/common/executable_disk-gc:223` | Proof needs git and disk-gc to run against a fixture repository; this run may not execute target code and used no OS sandbox. | In a scratch HOME on Linux with DISK_GC_WORKSPACE set to a scratch directory: create repository A with an origin/main, a tracked directory keep/ whose files are older than four days, and a worktree admin entry whose gitdir names <A>/keep x/.git; run disk-gc without --apply and confirm it logs `remove keep`, then run with --apply inside the sandbox and confirm keep/ is removed. Stop there. | Owner runs disk-gc in report mode (no --apply) on the Ubuntu host and checks for any remove line naming a path that `git worktree list --porcelain -z` does not list. |
| 5 | Bus sender identity is caller-asserted while the seats treat a row's from as identity (`hcom-bus:sender-identity-caller-asserted`) | `scripts/orchestrator/hcom-seat:1369` -> `scripts/orchestrator/hcom-seat:1703` -> `scripts/orchestrator/hcom-dispatch:136` -> `home/dot_agents/omp/hooks/stop-gate.ts:81` | Whether hcom accepts --from naming another participant from inside a launched seat, and whether a row written directly into hcom.db is delivered with that from, is behavior of the external hcom binary. | With two dummy seats on a scratch HCOM_DIR, from seat B run `hcom send @seatA --from coordinator -- PING test` and, separately inside B's srt sandbox, insert a message row with from=coordinator into the scratch hcom.db with sqlite3; check what sender seat A's delivery and bus-history.sh show. Stop at the delivered row. | Owner checks in the installed hcom version whether send honors --from for a launched participant and whether it binds the sender to HCOM_PROCESS_ID. |

Full traces, evidence and the fix each lead implies if validated: NEEDS-VALIDATION.md and the `description` of each record in findings.json.

## 6. Hardening notes and positive patterns

Hardening notes (no boundary violation shown; retained from hunter results):

- (.github/workflows) Same-repository pull_request runs of macos.yaml and ubuntu.yaml load PRIVATE_DOTFILES_PRIVATE_DEPLOY_KEY into ssh-agent before running the branch's setup.sh (macos.yaml:93-121); acceptable while only the coordinator pushes branches, but any future branch-push grant to a lower-trust actor would expose the deploy key.
- (.github/workflows) regime-ci passes a records-only pull request (every path under .orchestration/) from any author, including outside forks (regime-ci.py:76-79); by design while regime is not a required context, but if it becomes required the records-only branch should also check author_association.
- (.github/workflows) rounds-check --all reads ledger.tsv and decisions.tsv from the pull request head (regime.yml:57-66), so the head can present its own round history; the coordinator's store remains the authority (pr-audit.sh runs rounds-check over the store).
- (home/Library) The job executes the chezmoi working tree's Makefile and scripts outside any sandbox on a timer; a Claude Code session whose cwd is that tree can change them within its sandbox and have them run unsandboxed later without operator action.
- (home/dot_agents/skills) The port rewrites each upstream connector gate 'If **~~<kind>** is connected:' (a connector the operator configured for that placeholder) to 'If <kind> tools are available in this session:' and adds 'use the ones available in this session' (drift test PLACEHOLDER_REPLACEMENT and CONNECTORS_REPLACEMENT, test_kwp_skills_drift.py:87-91). The incident-response, change-request and status-report skills then direct 'Page on-call responders', 'Post status updates to incident channel' and 'Post change updates to the relevant team channels' (kwp-incident-response/SKILL.md:150-156, kwp-change-request/SKILL.md:117-119) through whatever tool of that kind a session has; in an omp seat the hcom bus is such a tool, and the audience includes the yolo seats. Consider keeping those lines as offers, as status-report already does ('Offer to post', kwp-status-report/SKILL.md:72), or leaving the three skills out of the omp-worker and omp-orchestrator audiences.
- (home/dot_claude) project-map-reload opens any agent-written */.project-map/index.html in terminal-browser outside the sandbox (project-map-reload.sh); the page runs with a file:// origin in that browser profile.
- (home/Library) The opener uses the single-threaded http.server.HTTPServer with no socket timeout, so one connection that sends nothing stalls it until it closes; any process on the laptop or the forwarded seat host can do that.
- (install) install/ubuntu/common/apparmor/bwrap-userns grants any caller of /usr/bin/bwrap unprivileged user namespaces (flags=(unconfined), userns), reopening the kernel attack surface Ubuntu restricts; the file documents this ceiling.
- (.) home/.key.txt.age publishes the passphrase-encrypted age identity in a public repository; its strength rests entirely on the passphrase (standard chezmoi pattern).
- (.) Seats read the machine's single gh login from ~/.config/gh/hosts.yml (not in the seat denyRead list); documented as out of scope (README:299, U29).
- (install) Docker and Tailscale apt signing keys are fetched over HTTPS and installed without a fingerprint check (install/ubuntu/client/docker.sh:74-75, install/ubuntu/client/tailscale.sh:34-35), unlike the pinned-fingerprint handling for AWS CLI and mise; TLS to the vendor is the only check.

Positive source patterns:

- Downloads verified before execution: release attestation or reviewed sha256 for chezmoi, zed and starship; pinned key fingerprints for AWS CLI and mise; commit-and-hash pin for the Homebrew installer; sha256 required for every chezmoi external.
- `regime.yml` runs `pull_request_target` from the base checkout only, with `persist-credentials: false` and `contents: read`, and reads the pull request body as data.
- No `${{ }}` expression is interpolated into any workflow `run:` script; event fields go through `env:`.
- `permgate` auto-approves only full-match read-only commands with no shell control, expansion or unsafe option, and never a sandbox-excluded command.
- Seat levers verify their own sha256 against the deployed manifest before running; seat srt settings deny git config and hooks, hcom launch inputs, and Claude Code settings and hooks, and the shim refuses to start omp unless a canary proves the sandbox holds.
- The SIWC OAuth flow uses PKCE S256 and a state check on a 127.0.0.1 listener; the url-opener requires a custom header and an https host allow-list.
- contextdb stores transcripts 0700/0600 with no-follow opens and promotes project-scope memory only from explicit user markers.

## 7. Coverage

Ledger: 38 units: covered 20, candidate 5, blocked 0, deferred 8, not applicable 5.

Top-level directories:

| Directory | Ledger units by status |
|---|---|
| `.claude/` | candidate 1, covered 2 |
| `.github/` | covered 3 |
| `.orchestration/` | covered 1, not_applicable 1 |
| `.ua/` | covered 1, not_applicable 1 |
| `docs/` | covered 1, not_applicable 1 |
| `home/` | candidate 3, covered 15, deferred 4 |
| `install/` | covered 3 |
| `plans/` | covered 1, not_applicable 1 |
| `scripts/` | candidate 4, covered 6, deferred 5 |
| `tests/` | covered 2, not_applicable 1 |
| `vendor/` | covered 3 |

Deferred units (prior_deferred from run-1; not reached by this single-agent unit sweep):

- `home/.chezmoiscripts#run scripts` / `home/.chezmoi.yaml.tmpl#template data` (home/.chezmoiscripts, home/.chezmoi.yaml.tmpl, home/.chezmoiexternal.yaml.tmpl, home/.chezmoitemplates/chezmoiexternal.d)
- `home/dot_agents/omp/hooks/stop-gate.ts#session_start` / `omp extension loading` (home/dot_agents/omp/hooks/stop-gate.ts, home/dot_agents/assets/pi-claude-bridge)
- `home/dot_local/bin/common#operator tools` / `same-user CLI helpers` (home/dot_local/bin/common/executable_remove-agent-asset, home/dot_local/bin/common/executable_provision-machine-key, home/dot_local/bin/common/executable_setup-gh, home/dot_local/bin/common/executable_setup-gpg, home/dot_local/bin/common/executable_ua-symbol-coverage, home/dot_local/bin/server)
- `scripts/ci#CI helper scripts` / `.github/workflows#run steps` (scripts/ci, Makefile)
- `scripts/generate-agent-configs.py#render` / `scripts/validate-agent-assets.py#invariants` (scripts/generate-agent-configs.py, scripts/validate-agent-assets.py, scripts/pin_records.py)
- `scripts/orchestrator/pr-audit.sh#codex exec` / `home/dot_agents/codex-audit/config.toml#default_permissions` (scripts/orchestrator/pr-audit.sh, home/dot_agents/codex-audit/config.toml)
- `scripts/orchestrator/regime-start#--supervise` / `home/Library/LaunchAgents/com.mryfmo.dotfiles.regime-supervisor.plist.tmpl` (scripts/orchestrator/regime-start, scripts/orchestrator/regime-stop, scripts/orchestrator/regime-init, scripts/orchestrator/seat-login-preflight)
- `scripts/orchestrator/worker-worktree.sh#push path` / `scripts/orchestrator/checkout-guard.sh#pre-commit` (scripts/orchestrator/worker-worktree.sh, scripts/orchestrator/checkout-guard.sh, scripts/orchestrator/git-isolated.sh, scripts/orchestrator/worktree-gc.sh)

Not applicable:

- `.orchestration/`: Coordinator records, briefs and verdicts (data). The one script, .orchestration/validation/025-pilot-s0-siwc-probe.py, is a pilot artifact no workflow, hook, installer or lever references (grep). Covered only by the tracked-file secret scan.
- `.ua/`: Generated knowledge-graph data for a local code-map tool; no host, hook, or CI path executes it.
- `docs/`: Prose documentation and one stylesheet; no executable path or configuration consumed by a host or CI step (docs.yml only renders it).
- `plans/`: Prose planning documents; nothing executes or loads them.
- `tests/`: Unit and install tests with fixtures; run only in CI with contents: read and never deployed to hosts. Covered only by the tracked-file secret scan (dummy values). At 4e83aba7 it also holds tests/fixtures/kwp-upstream (the pinned upstream copies of the nine kwp skills and their LICENSE) and tests/unit/test_kwp_skills_drift.py, test data and a test that run only in CI; reviewed under the kwp units. Changed at c44a7c6c: tests/unit/test_kwp_skills_drift.py (the U148 round-2 drift test), still a test only.

Final critic result: not clean. The deferred units above remain open coverage, unchanged by the U148 change; the next full sweep should start with them, highest first: `pr-audit.sh` (PR content into a Codex auditor), the worker push and commit guards, the regime supervisor, then the omp extensions and remaining operator tools.
