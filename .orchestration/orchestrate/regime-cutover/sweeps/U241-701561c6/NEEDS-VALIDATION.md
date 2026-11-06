# Needs validation: dotfiles @ 701561c6

Prioritized leads, without severity. Each is source-grounded and blocked on a fact outside source or on local execution this run was not allowed to perform. None is a confirmed vulnerability. The plans below are bounded local fixtures or owner-observed checks; none sends traffic to a deployment. All seven are carried from run-52 and re-verified at this head; U241 adds none. The two dsh leads are latent here (no thak turn reaches a model without U227's agent-default-model row) and stand in source for the head that carries U227.

## 1. The seat's per-base write-deny list omits the project-scope Claude Code instructions and commands of the checkout

- Fingerprint: `hcom-seat:srt-deny-write-misses-claude-project-instructions`
- Affected boundary: orchestrator seat srt sandbox -> coordinator's Claude Code (project instructions)
- First source location: `scripts/orchestrator/hcom-seat:1151`

Since U190 the user-scope Claude Code files that sessions outside the seat load are out of every seat's write roots (~/.claude and ~/.claude.json are no root, scripts/orchestrator/hcom-seat:1373-1374). The project scope is still written: the per-base loop for the seat directory and the checkout denies only settings, hooks and, since U189, the contextdb package (:1719-1721). For the orchestrator seat the seat directory is the main checkout (:1151), so a yolo seat (home/dot_agents/omp/policies/orchestrator.yml:10) that reads worker pull requests and bus text can rewrite CLAUDE.md, which imports AGENTS.md (CLAUDE.md:1), and create .claude/commands, .claude/agents, .claude/skills or .claude/rules, none tracked today, which a Claude Code session the coordinator opens in the checkout loads as memory, commands, subagents and skills. The result is instructions, and possibly frontmatter hooks, persisting from the seat into the coordinator's unsandboxed session. Fix if validated: deny the same names per base as at user scope (${base}/CLAUDE.md, ${base}/AGENTS.md, ${base}/.claude/commands, ${base}/.claude/agents, ${base}/.claude/skills, ${base}/.claude/rules), creating the directories first so srt on Linux binds them, with a test beside the U189 asserts.

Claimed root cause: The per-base deny loop enumerates the project's hook code and settings but not the project-scope instruction and command files (CLAUDE.md, .claude/commands, agents, skills, rules) that a Claude Code session opened in the checkout loads.

Source trace:

1. `scripts/orchestrator/hcom-seat:1151` (entrypoint, seat directory): The orchestrator seat's directory, its first write root, is the main checkout.
2. `scripts/orchestrator/hcom-seat:1719` (propagation, seat_sandbox_write deny loop): The per-base deny loop runs for the seat directory and the checkout.
3. `scripts/orchestrator/hcom-seat:1721` (sink, seat_sandbox_write deny loop): Per base only settings, hooks, contextdb, .omp, .codex, .envrc and .mcp.json are denied.

Verified evidence:

- `scripts/orchestrator/hcom-seat:1373`: Since U190 the user scope is no write root: seat_write_roots lists no ~/.claude, ~/.claude.json or CLAUDE_CONFIG_DIR (lines 1371-1372), so only the project scope stays writable.
- `CLAUDE.md:1`: The checkout's CLAUDE.md imports AGENTS.md.
- `home/dot_agents/omp/policies/orchestrator.yml:10`: The orchestrator seat runs approvalMode yolo.
- `scripts/orchestrator/hcom-seat:1373`: seat_write_roots starts with the seat directory itself.

Blockers:

- Whether the installed Claude Code loads a project's CLAUDE.md imports and .claude/commands, agents, skills and rules into a session without a prompt, and whether a skill's or subagent's frontmatter hooks run outside the Bash sandbox, is product behaviour not visible in this repository.
- Whether srt lets a seat create new entries below an allowed write root for names absent from denyWrite needs a sandboxed run, which this run may not perform.

Bounded local plan:

In a scratch copy of the repository launched as a scratch orchestrator seat, inside srt with the rendered settings, append one harmless marker sentence to CLAUDE.md and add .claude/skills/probe/SKILL.md whose frontmatter hook writes a marker file into scratch; then open Claude Code in the scratch copy outside srt and check whether the sentence is in its memory and whether the marker file appears when the skill loads. Stop there.

Owner-observed check:

The owner confirms whether the coordinator opens Claude Code in the main checkout and compares its CLAUDE.md, AGENTS.md and .claude/ with origin/main after orchestrator seat sessions.

## 2. The Claude Code sandbox still lets a contained command write the seat-launch inputs of the per-slug hcom stores and seat sandboxes on Linux, and of a renamed store or seat directory on macOS

- Fingerprint: `claude-sandbox:allow-write-covers-seat-launch-inputs`
- Affected boundary: Claude Code Bash sandbox (linux per-slug stores, darwin rename) -> unsandboxed seat launch
- First source location: `home/.chezmoitemplates/claude-settings-managed.json:670`

The managed Claude Code settings grant every session on the host sandboxed write access to ~/.local/state/hcom-regime, ~/.local/state/hcom and ~/.local/state/omp-seats with autoAllowBashIfSandboxed (home/.chezmoitemplates/claude-settings-managed.json:568, :575-581; linux :670, :677-682). U195 and U195b take the seat-launch inputs back with filesystem.denyWrite, rendered per OS from one derivation (scripts/generate-agent-configs.py:876-918). On linux the Linux sandbox discards every entry holding an interior `*`, so only the static store hcom-regime is denied (:689-698): every per-slug store under ~/.local/state/hcom (config.toml, env, config.env, .tmp/launch, scripts, integrations, shell_env.json) and every seat's .sandbox (its srt settings and omp shim) stay writable from a contained Bash command, including one a session runs on untrusted repository content. On darwin every path is denied as written (:590-605) but no directory above a denied path is pinned, so a contained command can rename a slug, program or `.tmp` directory within its root, write the control files there unmatched and move it back. The next seat launch reads those files outside any sandbox (hcom-seat denies its seats the same names, scripts/orchestrator/hcom-seat:1740). The README and the orchestrator threat row record both as same-user residuals owned by gate G17 (README.md:606-621; scripts/orchestrator/README.md:260). Fix if validated: move the check to the unsandboxed consumer, hcom-seat refusing a launch whose store control files or seat sandbox are not the ones it last wrote (owner, mode and content recorded at its last write), or keep ~/.local/state/hcom and ~/.local/state/omp-seats out of the Claude Code sandbox's allowWrite on linux.

Claimed root cause: The sandbox grants the hcom parent and the seats root whole, and neither OS's denyWrite can name their per-slug and per-program children durably: linux drops interior globs and darwin has no pin against a parent rename.

Source trace:

1. `home/.chezmoitemplates/claude-settings-managed.json:670` (entrypoint, linux sandbox): autoAllowBashIfSandboxed: a contained Bash command runs without a prompt.
2. `home/.chezmoitemplates/claude-settings-managed.json:677` (propagation, linux sandbox.filesystem.allowWrite): The hcom parent and the seats root are write roots on linux.
3. `scripts/generate-agent-configs.py:916` (propagation, render_claude_deny_write): On linux no entry holding `*` renders, so no per-slug store or seat sandbox is denied.
4. `home/.chezmoitemplates/claude-settings-managed.json:689` (sink, linux sandbox.filesystem.denyWrite): The linux list names the static store hcom-regime alone.

Verified evidence:

- `scripts/generate-agent-configs.py:914`: On darwin no pin renders above a denied path, leaving the rename route.
- `home/.chezmoitemplates/claude-settings-managed.json:601`: On darwin each slug's env is denied as written.
- `README.md:612`: A sandboxed command can rename such a directory, write its control files unmatched and move it back.
- `README.md:617`: On linux the per-slug stores and the seat sandboxes stay writable to a sandboxed command.
- `scripts/orchestrator/README.md:260`: The threat row records both as residual for gate G17.
- `scripts/orchestrator/hcom-seat:1740`: Seats are denied the same seven names, the sibling control.
- `scripts/validate-agent-assets.py:719`: The validator refuses an interior glob on linux, so the gap cannot be papered over.

Blockers:

- Whether Claude Code's linux sandbox grants writes below an allowWrite root to names no honoured denyWrite covers, and whether darwin's Seatbelt lets a contained command rename a directory above a denied path, is product behaviour; the README records the linux forms as unmeasured and this run may not execute agent code.
- hcom's consumption of config.toml, env, config.env, scripts, integrations, .tmp/launch and shell_env.json at seat launch happens in the external hcom binary; the repository only asserts it (scripts/orchestrator/README.md:260).

Bounded local plan:

Under a scratch HOME with a dummy hcom store at ~/.local/state/hcom/<slug> and the rendered settings, on linux run one sandboxed Claude Code Bash command that appends MARKER=1 to <slug>/env; on darwin run one that moves <slug> to <slug>.x, appends MARKER=1 to <slug>.x/env and moves it back; observe whether each succeeds. Stop there.

Owner-observed check:

The owner states which hosts run Claude Code sessions beside hcom stores seats launch from, and which store files the installed hcom reads at launch.

## 3. The kit's only DeepSeek harness profile turns the harness's command sandbox off, and nothing makes a dsh run happen inside an srt seat

- Fingerprint: `dsh-profile:thak-runs-without-command-sandbox` (latent at this head: reached once U227 lands)
- Affected boundary: model-driven dsh session -> operator host shell (no sandbox, no kit hook gate)
- First source location: `scripts/update-agent-assets.sh:2191`

The rendered thak profile disables the harness's own command-isolation row, bash-sandbox (home/dot_dsh/profiles/thak/cordis.patch.yml:9-10), and the asset's note gives the reason: 'the seat boundary is srt or nothing' (home/dot_agents/agent-config.yaml:1383). No code of this head provides that seat: scripts/orchestrator/hcom-seat starts only omp seats (:3-11), no lever starts dsh, and the wrapper update_deepseek_harness installs at ~/.dsh/bin/dsh execs the harness directly under mise's node with no seat check (scripts/update-agent-assets.sh:2191). Every run of the installed harness is therefore 'nothing': a session driven by a cloud model over ollama.com (cordis.patch.yml:14-18), reading repository and tool content that may carry injected instructions, runs its shell tool on the operator's account with the operator's credentials and no isolation, which is the outcome the repository refuses for Claude Code (agent-config.yaml:916-921, failIfUnavailable). Whether a command runs without an approval prompt under the headless bundle decides how much of this is reachable. The Claude hooks plugin the profile mounts over ~/.claude/settings.json (cordis.patch.yml:22-26) is no second gate at this pin: the table U179 computes from upstream source at dsh-v0.2.1-rc.5 (tests/unit/test_dsh_hook_coverage.py:126-132) puts the kit's permission gate, permgate (home/.chezmoitemplates/claude-settings-managed.json:813-819), on PermissionRequest, an event the bridge never reads, and its PreToolUse group on the matcher Bash, a name no DSH tool carries (the shell tool is bash), so neither runs on the harness's shell tool. Fix if validated: keep bash-sandbox enabled in the kit profile and disable it only in a seat overlay, or make ~/.dsh/bin/dsh refuse to start outside an srt seat (for example when HCOM_SEAT_SANDBOX is unset), the way hcom-seat refuses to launch without srt. At c43b31de the profile has no agent-default-model row (U227, PR 675, is not merged): the base bundle's default names deepseek-official, whose adapters the kit disables, so a thak turn ends with NO_ADAPTER (M-21) before the shell tool can run; with U227 every turn reaches a model and this path (run-51's reading of 785658d1).

Claimed root cause: The profile disables the harness's command sandbox on the premise of an srt seat boundary that no launch path of this head applies.

Source trace:

1. `scripts/update-agent-assets.sh:2191` (entrypoint, update_deepseek_harness): The installed wrapper starts the harness directly under mise's node; it checks for no seat.
2. `home/dot_dsh/profiles/thak/package.json:9` (propagation, dsh.profile.bundles): The profile composes the headless bundle.
3. `home/dot_dsh/profiles/thak/cordis.patch.yml:9` (sink, bash-sandbox): The harness's own command-isolation row is disabled in every run of the profile.

Verified evidence:

- `home/dot_agents/agent-config.yaml:1383`: The asset's note: its own command sandbox is off since the seat boundary is srt or nothing.
- `scripts/orchestrator/hcom-seat:3`: The seat launcher starts omp seats through hcom omp, nothing else.
- `home/dot_dsh/profiles/thak/cordis.patch.yml:17`: The model behind the session is served from ollama.com.
- `home/dot_agents/agent-config.yaml:921`: Claude Code is configured to refuse to start rather than run commands unsandboxed.
- `tests/unit/test_dsh_profile.py:118`: The test asserts the sandbox row disabled by id.
- `home/.chezmoitemplates/claude-settings-managed.json:813`: The kit's permission gate is a PermissionRequest hook that runs permgate.
- `tests/unit/test_dsh_hook_coverage.py:131`: The table pins the kit's PermissionRequest group as uncovered: the bridge's event tuple (:33-35) has no PermissionRequest.
- `tests/unit/test_dsh_hook_coverage.py:127`: The PreToolUse group's matcher Bash is pinned uncovered: the bridge compares tool names exactly and DSH names its shell tool bash.

Blockers:

- Whether the dsh headless bundle asks for approval before its shell tool runs a command, or runs it, is behaviour of the upstream harness at dsh-v0.2.1-rc.5.
- That the installed @deepseek-ai/dsh-hooks-claude-code runs neither the kit's PreToolUse Bash group nor its PermissionRequest group (permgate) on the harness's shell tool is the coordinator's reading of upstream source at dsh-v0.2.1-rc.5, held as constants in tests/unit/test_dsh_hook_coverage.py:126-132, not an observed run of the plugin.
- At this head no turn reaches a model unless a settings layer outside the kit overrides the base bundle's deepseek-official default; the path opens on every turn when U227 lands.

Bounded local plan:

On a scratch account with no credentials and a scratch HOME, install the pinned harness with DSH_HOME=~/.dsh and point a scratch copy of the patch's ollama-cloud baseURL at a local stub that answers one tool call running `touch "$HOME/dsh-probe"`; start ~/.dsh/bin/dsh with the thak profile and observe whether it prompts, refuses or runs the command, and whether a PreToolUse hook (matchers Bash and bash) or the PermissionRequest hook in the scratch ~/.claude/settings.json is called. Stop at the probe file.

Owner-observed check:

The owner states whether dsh is to run only inside an srt seat; if so, the wrapper or a launcher enforces it, or the kit profile keeps bash-sandbox on outside seats.

## 4. The thak profile leaves the base bundle's DeepSeek web-search provider mounted, so once a turn reaches a model a model-chosen search goes to the official DeepSeek API whenever DEEPSEEK_API_KEY is in the launch environment

- Fingerprint: `dsh-profile:web-search-routes-to-the-official-api` (latent at this head: reached once U227 lands)
- Affected boundary: model-driven dsh session -> official DeepSeek API (web search under the operator's key)
- First source location: `scripts/update-agent-assets.sh:2191`

The kit's route decision keeps the official DeepSeek API off by default, opt-in per engagement (scripts/generate-agent-configs.py:162-164). The thak patch carries it out by disabling the two official LLM adapters (home/dot_dsh/profiles/thak/cordis.patch.yml:5-8), and its test checks the patch text alone for api.deepseek.com and deepseek-official (tests/unit/test_dsh_profile.py:90-94). The profile composes @deepseek-ai/dsh-base (home/dot_dsh/profiles/thak/package.json:8), whose single insert block (upstream packages/bundle/base/cordis.patch.yml:15 at dsh-v0.2.1-rc.5) also mounts the web seam with searchProvider deepseek-official (:467-471), the web-search-deepseek and web-deepseek-api providers on DEEPSEEK_API_KEY (:473-481) and the model-facing tool-web (:486-490; web_search registers by default, packages/web/tool-web/src/index.ts:55, :91-93). The headless bundle disables only hmr, credentials, authorization and deepseek-account, and no file of this repository names a web row. With the credentials row off, the provider reads DEEPSEEK_API_KEY from the launch environment (packages/web/web-search-deepseek/src/index.ts:115-121) and POSTs 'Perform a web search for the query: <model-written query>' with that key to https://api.deepseek.com/anthropic/v1/messages (provider.ts:34, :220-253; DEEPSEEK_SEARCH_BASE_URL may redirect it); without a key it throws WEB_PROVIDER_CREDENTIAL_MISSING before anything is sent (provider.ts:330-341). At c43b31de no thak turn reaches a model: the profile has no agent-default-model row, so the base bundle's deepseek-official default (packages/bundle/base/cordis.patch.yml:90-94) resolves no adapter, and the headless runner selects nothing else (packages/bundle/headless/src/index.ts:334-335). U227 (PR 675) adds that row, and run-51 read this lead at its head; from then on a session whose context holds repository content, or content injected through a file it read, can choose a web_search whose query carries that content to the official API under the operator's key, on a host where the key is exported for another tool or engagement. Smallest fix if validated: render `- id: web-search-deepseek` / `  disabled: true` and `- id: web-deepseek-api` / `  disabled: true` in render_dsh_profile_patch (the web seam's configured deepseek-official id then resolves no provider and a search fails closed, packages/web/web/src/index.ts:178-182), or point the web row's searchProvider at a provider on the kit's route, and extend test_the_official_deepseek_api_rows_are_disabled_and_no_official_route_is_named to those rows.

Claimed root cause: The kit enforces its no-official-API route decision row by row on the LLM adapters only; the base bundle's web-search provider for the same official API, keyed by the same DEEPSEEK_API_KEY, stays mounted.

Source trace:

1. `scripts/update-agent-assets.sh:2191` (entrypoint, update_deepseek_harness): The installed wrapper starts the harness, and a thak session's tools run with what its bundles mount.
2. `home/dot_dsh/profiles/thak/package.json:8` (propagation, dsh.profile.bundles): The profile composes dsh-base, which mounts the web seam, web-search-deepseek and tool-web.
3. `home/dot_dsh/profiles/thak/cordis.patch.yml:5` (sink, llm-deepseek): Only the official LLM adapters are disabled; no row disables web-search-deepseek or web-deepseek-api.

Verified evidence:

- `scripts/generate-agent-configs.py:163`: The route decision: the official API is opt-in per engagement, so no official route stands.
- `scripts/generate-agent-configs.py:2262`: The renderer disables llm-deepseek and llm-deepseek-account and no web row.
- `tests/unit/test_dsh_profile.py:91`: The test checks the rendered patch text, not the composed tree, for the official endpoint.
- `home/dot_agents/agent-config.yaml:1373`: The bump review re-verifies the composed tree for the session-log upload and the route, not for the web-search provider.

Blockers:

- Whether a kit host launches dsh with DEEPSEEK_API_KEY (or DEEPSEEK_SEARCH_BASE_URL) in its environment is host state; no file of this repository sets or names either.
- That the composed thak tree registers web_search over the deepseek-official provider in a headless run is read from upstream source at dsh-v0.2.1-rc.5, not from an observed run.
- At this head no turn reaches a model (no agent-default-model row; U227 is not merged), so the search can run only after U227 lands or a settings layer outside the kit selects a registered route.

Bounded local plan:

On a scratch account with a scratch HOME and DSH_HOME and only loopback networking, install the pinned harness, print the thak profile's composed tree and look for the web, web-search-deepseek and tool-web rows; then run one turn against a loopback stub of the ollama-cloud baseURL that answers with one web_search call, with DEEPSEEK_API_KEY=dummy and DEEPSEEK_SEARCH_BASE_URL at a second loopback stub, and observe whether that stub receives the query and the dummy key. Stop at the first request.

Owner-observed check:

The owner states whether any host exports DEEPSEEK_API_KEY where dsh runs; if the route decision covers search too, the kit profile disables the official search providers by id.

## 5. disk-gc's worktree-root proof reads git metadata a seat can forge, so the daily sweep can remove a directory holding seat-denied files

- Fingerprint: `disk-gc:forged-worktree-root-removes-seat-denied-tree`
- Affected boundary: seat-written git metadata -> unsandboxed daily disk-gc removal
- First source location: `home/dot_config/systemd/user/disk-gc.service.tmpl:6`

U188's worktree_root accepts a candidate when git, run in it, reports it as its own toplevel and names the repository's common directory (round 3 refuses a common-directory name ending in a newline, which a forged entry need not use) (home/dot_local/bin/common/executable_disk-gc:207-242); the later checks read HEAD, the index and the default branch, which prefers refs/remotes/origin/HEAD (:154-166, :283-307); and the tree then goes to `git worktree remove --force --force` (:332) under the unsandboxed daily timer. Every one of those facts lives in files a seat can write: the repository's common directory is a seat write root (scripts/orchestrator/hcom-seat:1373), where on Linux a new worktrees/<id> admin entry and a ref are not denied (:1729), and the orchestrator seat writes the main checkout (:1151), where `.claude/` itself is not denied, only its settings, hooks and, since U189, the contextdb package (:1753-1758). A `.claude/.git` file naming a hand-made admin entry, an index of a commit whose tree is `.claude`'s files and an origin/HEAD naming that commit would present `.claude` as a merged, clean, idle, unlocked worktree root, and git would delete it with the seat-denied hooks and settings inside; on Linux srt binds only existing deny paths, so a later launch could leave them writable. Fix if validated: keep a candidate that lies inside the main worktree (walk its parents by -ef against the main worktree), and read the default branch from origin/main or origin/master before origin/HEAD, with a fixture test of a forged root under the checkout.

Claimed root cause: The root proof and the removal criteria are all answers git derives from metadata at the candidate and from refs, both writable by a seat, and nothing confines a candidate to lie outside the main worktree.

Source trace:

1. `home/dot_config/systemd/user/disk-gc.service.tmpl:6` (entrypoint, ExecStart): The daily unsandboxed sweep.
2. `home/dot_local/bin/common/executable_disk-gc:218` (propagation, worktree_root): The toplevel answer comes from git at the candidate, so a .git file there decides it.
3. `home/dot_local/bin/common/executable_disk-gc:226` (propagation, worktree_root): The common directory answer comes from the candidate's own .git file and admin entry.
4. `home/dot_local/bin/common/executable_disk-gc:156` (propagation, default_branch): The default branch prefers the refs/remotes/origin/HEAD symbolic ref.
5. `home/dot_local/bin/common/executable_disk-gc:332` (sink, worktree_gc): git worktree remove --force --force deletes the candidate recursively.

Verified evidence:

- `scripts/orchestrator/hcom-seat:1373`: The repository's common directory is a seat write root.
- `scripts/orchestrator/hcom-seat:1151`: The orchestrator seat's directory is the main checkout.
- `scripts/orchestrator/hcom-seat:1719`: Per base only named children of .claude are denied (settings, hooks, contextdb), not .claude itself.
- `scripts/orchestrator/hcom-seat:1729`: On Linux a worktree admin entry created after launch is not denied.
- `tests/unit/test_disk_gc.py:346`: The tests keep a listed subdirectory with no .git of its own, not a forged root.

Blockers:

- Whether `git worktree remove --force --force` removes a directory through a hand-made worktrees/<id> entry and a matching <dir>/.git file, and whether a crafted index and an origin/HEAD set in the common directory meet disk-gc's merge, status and recency checks, is git behaviour that needs a fixture run, which this run may not perform.
- Whether an orchestrator seat runs on an Ubuntu host that also runs the disk-gc timer, and whether srt on Linux then leaves the removed deny paths writable at the next launch, are deployment and srt facts.

Bounded local plan:

In a scratch HOME with a fixture repository under a scratch DISK_GC_WORKSPACE, create a directory inside its main worktree holding two old files, a .git file naming a new worktrees/<id> entry, an index and HEAD of a commit whose tree is those files, and set refs/remotes/origin/HEAD to that commit; run `disk-gc` (report mode) and then `disk-gc --apply` with DISK_GC_REPOS set to the fixture; observe whether the directory is reported and removed. Stop at that result.

Owner-observed check:

The owner states whether seats run on the Ubuntu host the disk-gc timer runs on, and inspects the checkout's .git/worktrees for entries no git worktree add made.

## 6. Bus sender identity is caller-asserted while the seats treat a row's from as identity

- Fingerprint: `hcom-bus:sender-identity-caller-asserted`
- Affected boundary: worker seat -> another seat's view of sender identity
- First source location: `scripts/orchestrator/hcom-seat:1373`

The bus trust boundary (README:177) states that identities are hcom participant names, the from and delivered_to of a row, and that no seat writes under $HCOM_DIR except through hcom. hcom-dispatch sets from from its own argument (`--from <from>` is the external sender identity), and every seat's srt settings grant write access to the whole hcom store with only its launch inputs denied, so hcom.db is seat-writable and `hcom send --from` is reachable. A worker seat can plausibly post a row whose from names the coordinator or another seat; the omp stop gate already decides a seat's task state by from. The effect on a recipient is bounded by the rule that bus text never authorises a command, but the orchestrator seat writes the main checkout and acts on TASK and RESULT lines by sender. Fix if validated: deny seats direct write to hcom.db (only hcom, binding the sender to the launched participant, should write it) or have recipients and the stop gate verify from against hcom's process binding rather than the row value.

Claimed root cause: The bus identity seats rely on is supplied by the sender (hcom send --from, or a direct row write to the seat-writable hcom.db) instead of being bound by hcom to the launched seat.

Source trace:

1. `scripts/orchestrator/hcom-seat:1373` (entrypoint, seat_write_roots): HCOM_DIR, the program's store, is a write root of every seat.
2. `scripts/orchestrator/hcom-seat:1740` (propagation, seat_sandbox_write): Only the store's launch inputs are denied; hcom.db stays writable.
3. `scripts/orchestrator/hcom-dispatch:136` (propagation, send): hcom send ... --from "${from}" with a caller-chosen from.
4. `home/dot_agents/omp/hooks/stop-gate.ts:81` (sink, task tracking): The stop gate decides a task's open or closed move by comparing the row's from with the seat name.

Verified evidence:

- `scripts/orchestrator/README.md:177`: Bus trust boundary: identities are the row's from and delivered_to, and no seat writes under $HCOM_DIR except through hcom.
- `scripts/orchestrator/hcom-dispatch:16`: Documents --from <from> as the external sender identity that becomes the row's from.
- `scripts/orchestrator/hcom-seat:1758`: The store is also in every seat's allowRead.
- `home/dot_agents/omp/policies/orchestrator.yml:10`: The orchestrator seat runs approvalMode yolo.

Blockers:

- Whether hcom accepts --from naming another participant from inside a launched seat, and whether a row written directly into hcom.db is delivered with that from, is behavior of the external hcom binary.
- How the orchestrator and worker seats weigh from when acting on a line is runtime model behavior, observable only in a seat run.

Bounded local plan:

With two dummy seats on a scratch HCOM_DIR, from seat B run `hcom send @seatA --from coordinator -- PING test` and, separately inside B's srt sandbox, insert a message row with from=coordinator into the scratch hcom.db with sqlite3; check what sender seat A's delivery and bus-history.sh show. Stop at the delivered row.

Owner-observed check:

Owner checks in the installed hcom version whether send honors --from for a launched participant and whether it binds the sender to HCOM_PROCESS_ID.

## 7. The DeepSeek harness installer resolves the thak profile's plugins from the npm registry with no lockfile, outside the reviewed digest

- Fingerprint: `dsh-installer:profile-plugins-resolve-outside-the-digest`
- Affected boundary: unreviewed npm registry closure -> opted-in host (profile plugin install)
- First source location: `scripts/update-agent-assets.sh:2743`

update_deepseek_harness verifies GitHub's tag archive of the harness against a reviewed sha256 and builds it from its own lockfile, but then runs `mise exec -- pnpm install` in the deployed thak profile directory (scripts/update-agent-assets.sh:2170) with no lockfile and no --frozen-lockfile. The profile's only dependency, @deepseek-ai/dsh-hooks-claude-code at 0.2.1-rc.5 (home/dot_dsh/profiles/thak/package.json:14), therefore comes from the npm registry, not from the verified archive, and its own dependencies resolve to whatever versions their ranges admit at install time; the kit renders no lockfile for the profile (scripts/generate-agent-configs.py:2643-2644). That code is loaded into the harness and runs as the operator whenever dsh starts (and at install if pnpm runs its dependencies' lifecycle scripts). The repository's npm cooldown, min-release-age=3 (home/dot_npmrc:1), is npm's key; pnpm 12.8.1 from mise performs this install. A malicious or hijacked release of any package in that closure, inside its range and younger than any cooldown pnpm applies, would run on every opted-in host at its next harness install. Fix if validated: commit a generated pnpm-lock.yaml for the profile (or install the hooks plugin from the verified archive's own workspace) and run `pnpm install --frozen-lockfile` there, and set pnpm's own minimum-release-age for the profile install.

Claimed root cause: The profile's plugin install resolves its dependency closure fresh at install time, outside the archive digest and the archive's lockfile that bind the harness itself.

Source trace:

1. `scripts/update-agent-assets.sh:2743` (entrypoint, main): make update runs update_deepseek_harness on every host; it proceeds only where DSH_HOME is exported and names ~/.dsh.
2. `scripts/update-agent-assets.sh:2137` (propagation, update_deepseek_harness): The reviewed sha256 binds the downloaded harness archive only.
3. `scripts/update-agent-assets.sh:2161` (propagation, update_deepseek_harness): The harness builds from its digest-bound lockfile with --frozen-lockfile.
4. `scripts/update-agent-assets.sh:2170` (sink, update_deepseek_harness): The profile's plugins install with `mise exec -- pnpm install`, no lockfile and no --frozen-lockfile.

Verified evidence:

- `home/dot_dsh/profiles/thak/package.json:14`: The one dependency, the Claude hooks plugin, an exact prerelease version from the npm registry.
- `scripts/generate-agent-configs.py:2643`: The rendered profile scope names package.json and cordis.patch.yml only; no lockfile is rendered.
- `tests/unit/test_check_agent_runtime.py:456`: The lockfile pnpm writes in the deployed profile is an unmanaged byproduct the doctor is told to ignore.
- `home/dot_npmrc:1`: The repository's npm cooldown is npm's own key, min-release-age.
- `home/dot_mise/config.toml:42`: pnpm comes from mise as npm:pnpm 12.8.1.
- `scripts/update-agent-assets.sh:1362`: The Understand-Anything build in the same file tries pnpm install --frozen-lockfile first.

Blockers:

- Whether pnpm 12.8.1 applies ~/.npmrc's min-release-age (npm's key) or only its own minimum-release-age setting is pnpm behaviour, not visible in this repository.
- The dependency ranges of @deepseek-ai/dsh-hooks-claude-code@0.2.1-rc.5, whether pnpm runs their lifecycle scripts, and whether the harness loads the plugin from the profile's node_modules or from its own verified workspace are facts of the registry and the upstream harness.

Bounded local plan:

In a scratch HOME with an empty pnpm store, copy home/dot_dsh/profiles/thak/package.json into an empty directory and run `mise exec npm:pnpm@12.8.1 -- pnpm install --lockfile-only --ignore-scripts`; read the written pnpm-lock.yaml for packages resolved through ranges and for versions published less than three days before, and `pnpm config get minimum-release-age`. Stop at the lockfile; build and run nothing.

Owner-observed check:

The owner reads the published manifest of @deepseek-ai/dsh-hooks-claude-code@0.2.1-rc.5 and the harness's plugin resolution, and decides whether the profile gets a committed lockfile.
