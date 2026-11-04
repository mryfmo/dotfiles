# Security audit report: dotfiles @ 78eea03c

## 1. Run

- Source ref: `78eea03c20b92a47e4d82b90f139ead57fcf8fdb` (U166 head, PR 650, branch `fix/worker-root-probe-names-the-reader`; detached, clean worktree). It is one commit on main 30e94d9b changing two test files: the worker-root probe of `tests/unit/trusted_exec_contract.py` gains `WorkerRoot._holders`, a /proc reader that names the processes holding its FIFO sentinel open in the recorded-read message, and `tests/unit/test_trusted_exec_contract.py` its test.
- Profile: `standard`; scope: the whole repository at this head, hunting effort on the /proc reader as the trust-boundary change (what it opens, whose data it reads, where that data goes); no budget set.
- Execution: sandboxed-source-and-local-only. Nothing from the target was built, tested or executed (brief U168), so every candidate that needs execution for proof is `needs_validation`.
- Prior runs: run-15's five records were re-verified as the brief asks; they are run-14's records, cited at main's lines (claude-sandbox at agent-config.yaml:930 and :938, without U148's audience lines). The ledger is run-14's main-line ledger: this head holds main and U166 but not U165, so run-14's flake-signature unit is not carried and the tracked-file scan and the tests disposition are re-stated for U166. Run-9's sweep-row gate unit holds byte-for-byte. One new unit covers the /proc reader; the eight deferred units are deferred again.
- Agent independence (read this first): the seat exposes no delegation tool (`task` and `eval` are blocked by user policy), so one agent ran every role in sequence (reconnaissance, hunters, critics, candidate verifiers, record verifiers). The per-role agent IDs in the ledger (`h16-*`, `v16-*`, `r16-*`, `critic16-*`) are separate passes with separate `agents/<id>/` directories, not independent agents. The independence the skill asks of verifiers is therefore procedural only, which is one more reason no record is `confirmed`.
- Coverage: partial. 19 units covered, 5 candidate, 8 deferred, 5 not applicable (of 37). The post-wave critic queued the deferred units; the final-clean critic did not pass clean because they remain, so no complete-coverage claim is made.
- Status: advisory. These records are input to the coordinator's ledger, never a verdict.

## 2. Posture

The U166 change adds no candidate. `WorkerRoot._holders` runs inside the test interpreter and opens no FIFO: it lists /proc, stats each /proc/<pid>/fd link (which follows the link without opening the file) and reads status, comm and cmdline, procfs files, only for a pid holding the sentinel, skipping the probe's own writer. It reaches only processes of the user the tests run as (another user's fd table is counted as unreadable), and the processes it names hold the test's own temporary FIFO, normally the consumer under test, so no principal above the tests' own is read. One hardening note: the holder's comm and first 200 characters of its argv reach the failure message, and so the terminal or the CI log, unescaped, so a newline, a `::` workflow command or an argv-borne token of such a process would be printed as written (section 6). Run-9's notes on the gate stand. The five carried leads are unchanged from run-1: write roots granted to one sandbox (Claude Code, or a seat's srt) include files that a later, unsandboxed process executes or trusts, plus one destructive timer job that parses paths unsafely. The rest of the repository keeps the posture run-1 recorded: verified downloads, CI that never runs PR code with write tokens or fork-reachable secrets, a full-match approval hook, and generated, probed seat containment.

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
- (home/dot_claude) project-map-reload opens any agent-written */.project-map/index.html in terminal-browser outside the sandbox (project-map-reload.sh); the page runs with a file:// origin in that browser profile.
- (home/Library) The opener uses the single-threaded http.server.HTTPServer with no socket timeout, so one connection that sends nothing stalls it until it closes; any process on the laptop or the forwarded seat host can do that.
- (install) install/ubuntu/common/apparmor/bwrap-userns grants any caller of /usr/bin/bwrap unprivileged user namespaces (flags=(unconfined), userns), reopening the kernel attack surface Ubuntu restricts; the file documents this ceiling.
- (.) home/.key.txt.age publishes the passphrase-encrypted age identity in a public repository; its strength rests entirely on the passphrase (standard chezmoi pattern).
- (.) Seats read the machine's single gh login from ~/.config/gh/hosts.yml (not in the seat denyRead list); documented as out of scope (README:299, U29).
- (scripts/orchestrator) trust_probe still runs the checkout copy scripts/orchestrator/brief-check.py (pr-merge.sh:869, :728), and the comment at pr-merge.sh:253 still says its import-time pin self-check means 'a rewritten checker reads no brief'; outside ~/.local/bin/common that self-check compares the file with the checkout's own home/dot_agents/agent-config.yaml (brief-check.py:75-91), and a rewrite can drop the check itself; the same holds for the unpinned checkout ledger.py. Round 4 already reads the skill pin from LEVER_MANIFEST; reading the pinned installed ~/.local/bin/common/brief-check.py the same way would make the comment true.
- (scripts/orchestrator) The findings-file check refuses a symlink only at the last component (`! -L ${findings_file}`, pr-merge.sh:798) after checking sweeps/ itself; a symlinked subdirectory below sweeps/ (sweeps/<link>/x.json) passes -f and -O through the link, so the file need not be under the store. The lever never opens it and the store is the orchestrator's own, so this weakens only the stated 'under the store' property; a physical-path check (cd -P and a prefix compare) would close it.
- (scripts/orchestrator) RESOLVED since run-3: newest_sweep accepted any row starting with the word sweep whatever its pr and verifier; round 4 requires pr '-', the 'security-audit-skill <pin>' verifier with the pin checked against the deployed manifest, and a findings file under sweeps/ (ledger.py:129-150, pr-merge.sh:771-799).
- (install) Docker and Tailscale apt signing keys are fetched over HTTPS and installed without a fingerprint check (install/ubuntu/client/docker.sh:74-75, install/ubuntu/client/tailscale.sh:34-35), unlike the pinned-fingerprint handling for AWS CLI and mise; TLS to the vendor is the only check.
- (tests/unit) WorkerRoot._holders puts a holder's comm and the first 200 characters of its cmdline into the failure message unescaped (tests/unit/trusted_exec_contract.py:259-260, raised at :344), so a control character, a newline followed by a `::` workflow command, or an argv-borne token of a process that opened the sentinel reaches the terminal or the CI log as written. The reader is the tests' own user and the named process holds the test's own FIFO, so no boundary is crossed; formatting the fields with repr() (or escaping everything outside printable ASCII) and printing argv[0] with the argument count instead of the arguments would keep the record useful without carrying another process's arguments into a log.

Positive source patterns:

- Downloads verified before execution: release attestation or reviewed sha256 for chezmoi, zed and starship; pinned key fingerprints for AWS CLI and mise; commit-and-hash pin for the Homebrew installer; sha256 required for every chezmoi external.
- `regime.yml` runs `pull_request_target` from the base checkout only, with `persist-credentials: false` and `contents: read`, and reads the pull request body as data.
- No `${{ }}` expression is interpolated into any workflow `run:` script; event fields go through `env:`.
- `permgate` auto-approves only full-match read-only commands with no shell control, expansion or unsafe option, and never a sandbox-excluded command.
- Seat levers verify their own sha256 against the deployed manifest before running; seat srt settings deny git config and hooks, hcom launch inputs, and Claude Code settings and hooks, and the shim refuses to start omp unless a canary proves the sandbox holds.
- The SIWC OAuth flow uses PKCE S256 and a state check on a 127.0.0.1 listener; the url-opener requires a custom header and an https host allow-list.
- contextdb stores transcripts 0700/0600 with no-follow opens and promotes project-scope memory only from explicit user markers.

## 7. Coverage

Ledger: 37 units: covered 19, candidate 5, blocked 0, deferred 8, not applicable 5.

Top-level directories:

| Directory | Ledger units by status |
|---|---|
| `.claude/` | candidate 1, covered 2 |
| `.github/` | covered 3 |
| `.orchestration/` | covered 1, not_applicable 1 |
| `.ua/` | covered 1, not_applicable 1 |
| `docs/` | covered 1, not_applicable 1 |
| `home/` | candidate 3, covered 12, deferred 4 |
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

- `.orchestration/`: Coordinator records, briefs and verdicts (data). The one script, .orchestration/validation/025-pilot-s0-siwc-probe.py, is a pilot artifact no workflow, hook, installer or lever references (grep). Covered only by the tracked-file secret scan. Main 30e94d9b holds the eight coordinator records run-13 read (the U145, U146 and U147 briefs, the U145 and U20 verdicts, decisions.tsv, ledger.tsv, units.tsv), unchanged by 78eea03c; still records only.
- `.ua/`: Generated knowledge-graph data for a local code-map tool; no host, hook, or CI path executes it.
- `docs/`: Prose documentation and one stylesheet; no executable path or configuration consumed by a host or CI step (docs.yml only renders it). Main 30e94d9b holds docs/engagement-handout.md (U149), read whole in run-12 and unchanged by 78eea03c; still documentation, no runtime trust boundary.
- `plans/`: Prose planning documents; nothing executes or loads them.
- `tests/`: Unit and install tests with fixtures; run only in CI with contents: read and never deployed to hosts. Covered only by the tracked-file secret scan (dummy values). Changed at 78eea03c: tests/unit/trusted_exec_contract.py and tests/unit/test_trusted_exec_contract.py (a /proc holder scan in the worker-root probe and its test), still tests only; read under the holder-scan unit. U165's test changes are on another branch and absent here.

Final critic result: not clean. The deferred units above remain open coverage, unchanged by the U166 change; the next full sweep should start with them, highest first: `pr-audit.sh` (PR content into a Codex auditor), the worker push and commit guards, the regime supervisor, then the omp extensions and remaining operator tools.
