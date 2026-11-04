# Security audit report: dotfiles @ 3da428db

## 1. Run

- Source ref: `3da428db12f9d56293238122e7db5c6aed1bfd2a` (U150 round-8 head, PR 647, branch `feat/graphify-pinned-asset`; detached, clean worktree). It merges main dab64ca1 (main 30e94d9b plus the merged U148: nine kwp skills, their symlinks, drift test and audience lines) into the U150 head ac4af099; against main it adds only the U150 files, unchanged since ac4af099 apart from the manifest's line numbers (the Graphify entry now at agent-config.yaml:1325-1359).
- Profile: `standard`; scope: the whole repository at this head, hunting effort on what the merged main brings and where it meets the U150 entry; no budget set.
- Execution: sandboxed-source-and-local-only. Nothing from the target was built, tested or executed (brief U169), so every candidate that needs execution for proof is `needs_validation`.
- Prior runs: dab64ca1's tree equals run-13's head 406fb9dd (main plus U148), so run-13 was read whole and carried; this head differs from it by U150's three files only. Run-12 (U150 at ac4af099) contributes the three U150 units and the rejected Graphify record, whose manifest lines move 10 lower in the file (each shifted line compared with its text at ac4af099). The five `needs_validation` records are run-14's fingerprints, cited as at 406fb9dd (claude-sandbox at agent-config.yaml:940 and :948, under U148's lines); every cited line was re-read. The eight deferred units are deferred again.
- Agent independence (read this first): the seat exposes no delegation tool (`task` and `eval` are blocked by user policy), so one agent ran every role in sequence (reconnaissance, hunters, critics, candidate verifiers, record verifiers). The per-role agent IDs in the ledger (`h15-*`, `v15-*`, `r15-*`, `critic15-*`) are separate passes with separate `agents/<id>/` directories, not independent agents. The independence the skill asks of verifiers is therefore procedural only, which is one more reason no record is `confirmed`.
- Coverage: partial. 23 units covered, 6 candidate, 8 deferred, 5 not applicable (of 42). The post-wave critic queued the deferred units; the final-clean critic did not pass clean because they remain, so no complete-coverage claim is made.
- Status: advisory. These records are input to the coordinator's ledger, never a verdict.

## 2. Posture

The merge adds no lead. The U150 entry, its installer and both tests are byte-equal to ac4af099, and the merged main brings the U148 port: nine kwp skills, their Claude Code symlinks, the drift test and ten audience lines, byte-equal to what run-13 reviewed at 406fb9dd. The two meet only in the manifest: the U148 lines sit under `skills.audience` (agent-config.yaml:114-123) and the U150 entry under `assets:` (:1325-1359), so neither reads the other, and the sweep gate's `sweep_pin_probe` still yields the one skill pin (:1305): `graphifyy:` closes the skill's block at the asset indent and its `pin: 0.9.99` is not 40 hex. Run-4's Graphify lead stays rejected on the unchanged installer (now :1352-1359). Run-2's hardening note on the kwp connector gates and outward actions, run-6's notes on the trial install and run-9's notes on the gate stand. The five carried leads are unchanged from run-1: write roots granted to one sandbox (Claude Code, or a seat's srt) include files that a later, unsandboxed process executes or trusts, plus one destructive timer job that parses paths unsafely. The rest of the repository keeps the posture run-1 recorded.

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
- (home/dot_agents) The verified wheel is installed with `uv tool install --force <wheel>`, which resolves graphifyy's dependency closure from PyPI by version, without hashes, at install time (agent-config.yaml:1358; gated by the host's 7-day exclude-newer, :1342-1344). Round 4 keeps make update from re-resolving it later (upgrade-tools.sh:552-555 skips the tool), so the residual is the one trial install, the same as the hcom install carries (update-agent-assets.sh:1699); a hashed constraints file for the closure would close it for both.
- (home/dot_agents) The installer's `|| exit 1` (agent-config.yaml:1356) ends the operator's interactive shell on a failed digest read, and the chain's left-to-right && / || grouping also sends a failed mktemp or curl there; it fails closed, but a subshell `( ... )` around the line would keep the terminal. The mktemp directory and the wheel are still left behind (:1353-1358).
- (home/dot_agents/skills) The port rewrites each upstream connector gate 'If **~~<kind>** is connected:' (a connector the operator configured for that placeholder) to 'If <kind> tools are available in this session:' and adds 'use the ones available in this session' (drift test PLACEHOLDER_REPLACEMENT and CONNECTORS_REPLACEMENT, test_kwp_skills_drift.py:87-91). The incident-response, change-request and status-report skills then direct 'Page on-call responders', 'Post status updates to incident channel' and 'Post change updates to the relevant team channels' (kwp-incident-response/SKILL.md:150-156, kwp-change-request/SKILL.md:117-119) through whatever tool of that kind a session has; in an omp seat the hcom bus is such a tool, and the audience includes the yolo seats. Consider keeping those lines as offers, as status-report already does ('Offer to post', kwp-status-report/SKILL.md:72), or leaving the three skills out of the omp-worker and omp-orchestrator audiences.
- (home/dot_claude) project-map-reload opens any agent-written */.project-map/index.html in terminal-browser outside the sandbox (project-map-reload.sh); the page runs with a file:// origin in that browser profile.
- (home/Library) The opener uses the single-threaded http.server.HTTPServer with no socket timeout, so one connection that sends nothing stalls it until it closes; any process on the laptop or the forwarded seat host can do that.
- (install) install/ubuntu/common/apparmor/bwrap-userns grants any caller of /usr/bin/bwrap unprivileged user namespaces (flags=(unconfined), userns), reopening the kernel attack surface Ubuntu restricts; the file documents this ceiling.
- (.) home/.key.txt.age publishes the passphrase-encrypted age identity in a public repository; its strength rests entirely on the passphrase (standard chezmoi pattern).
- (.) Seats read the machine's single gh login from ~/.config/gh/hosts.yml (not in the seat denyRead list); documented as out of scope (README:299, U29).
- (scripts/orchestrator) trust_probe still runs the checkout copy scripts/orchestrator/brief-check.py (pr-merge.sh:869, :728), and the comment at pr-merge.sh:253 still says its import-time pin self-check means 'a rewritten checker reads no brief'; outside ~/.local/bin/common that self-check compares the file with the checkout's own home/dot_agents/agent-config.yaml (brief-check.py:75-91), and a rewrite can drop the check itself; the same holds for the unpinned checkout ledger.py. Round 4 already reads the skill pin from LEVER_MANIFEST; reading the pinned installed ~/.local/bin/common/brief-check.py the same way would make the comment true.
- (scripts/orchestrator) The findings-file check refuses a symlink only at the last component (`! -L ${findings_file}`, pr-merge.sh:798) after checking sweeps/ itself; a symlinked subdirectory below sweeps/ (sweeps/<link>/x.json) passes -f and -O through the link, so the file need not be under the store. The lever never opens it and the store is the orchestrator's own, so this weakens only the stated 'under the store' property; a physical-path check (cd -P and a prefix compare) would close it.
- (scripts/orchestrator) RESOLVED since run-3: newest_sweep accepted any row starting with the word sweep whatever its pr and verifier; round 4 requires pr '-', the 'security-audit-skill <pin>' verifier with the pin checked against the deployed manifest, and a findings file under sweeps/ (ledger.py:129-150, pr-merge.sh:771-799).
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

Ledger: 42 units: covered 23, candidate 6, blocked 0, deferred 8, not applicable 5.

Top-level directories:

| Directory | Ledger units by status |
|---|---|
| `.claude/` | candidate 1, covered 2 |
| `.github/` | covered 3 |
| `.orchestration/` | covered 1, not_applicable 1 |
| `.ua/` | covered 1, not_applicable 1 |
| `docs/` | covered 1, not_applicable 1 |
| `home/` | candidate 4, covered 17, deferred 4 |
| `install/` | covered 3 |
| `plans/` | covered 1, not_applicable 1 |
| `scripts/` | candidate 5, covered 9, deferred 5 |
| `tests/` | candidate 1, covered 4, not_applicable 1 |
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

- `.orchestration/`: Coordinator records, briefs and verdicts (data). The one script, .orchestration/validation/025-pilot-s0-siwc-probe.py, is a pilot artifact no workflow, hook, installer or lever references (grep). Covered only by the tracked-file secret scan. Changed at 406fb9dd (the merge of main 30e94d9b): eight coordinator records (the U145, U146 and U147 briefs, the U145 and U20 verdicts, decisions.tsv, ledger.tsv, units.tsv), still records only.
- `.ua/`: Generated knowledge-graph data for a local code-map tool; no host, hook, or CI path executes it.
- `docs/`: Prose documentation and one stylesheet; no executable path or configuration consumed by a host or CI step (docs.yml only renders it). Changed at 406fb9dd (the merge of main 30e94d9b): docs/engagement-handout.md (U149), read whole: an operator page of commands and read-only checks with hosts named by kind and no credential; still documentation, no runtime trust boundary.
- `plans/`: Prose planning documents; nothing executes or loads them.
- `tests/`: Unit and install tests with fixtures; run only in CI with contents: read and never deployed to hosts. Covered only by the tracked-file secret scan (dummy values). At 4e83aba7 it also holds tests/fixtures/kwp-upstream (the pinned upstream copies of the nine kwp skills and their LICENSE) and tests/unit/test_kwp_skills_drift.py, test data and a test that run only in CI; reviewed under the kwp units. Changed at c44a7c6c: tests/unit/test_kwp_skills_drift.py (the U148 round-2 drift test), still a test only. Changed at 406fb9dd (the merge of main 30e94d9b): tests/unit/test_ledger.py, tests/unit/test_pr_merge.py, tests/unit/test_pr_levers.py (the U147 gate's tests, byte-equal to 84b4e984), still tests only. At 3da428db (the merge of main into the U150 head) it also holds tests/unit/test_graphify_asset.py and the Graphify cases of tests/unit/test_validate_agent_assets.py, byte-equal to ac4af099 and read under the Graphify units; still tests only.

Final critic result: not clean. The deferred units above remain open coverage, unchanged by this merge; the next full sweep should start with them, highest first: `pr-audit.sh` (PR content into a Codex auditor), the worker push and commit guards, the regime supervisor, then the omp extensions and remaining operator tools.

Rejected records (not findings): `assets.graphify:installer-skips-pinned-sha256`
