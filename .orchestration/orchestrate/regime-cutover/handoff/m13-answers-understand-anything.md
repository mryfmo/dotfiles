# M-13 Understand-Anything answers (corpus 182fbaa2, plugin 2.9.7, graph refreshed in the scratch clone)

Route: `/understand --full` then `/understand-chat <question>` through `claude --model claude-haiku-5-5 -p` in a second clean scratch clone (`corpus-ua`, no graphify project install, so graphify's PreToolUse hooks and CLAUDE.md block could not steer this session). Refresh ran 2026-11-04T00:23:50Z to 00:54:51Z (31 min); `.ua/meta.json` after it: gitCommitHash 182fbaa2d34048f56abfc2935d272c2522ed34b1, analyzedFiles 630, lastAnalyzedAt 2026-11-04T00:54:40Z; graph 1846 nodes (file 496, function 1023, class 200, config 61, document 53, pipeline 11, service 2), 2102 edges, 1.4 MB. Each answer below is the verbatim stdout of one headless call (exit code and wall time after it). The appended system prompt said: follow the understand-chat skill, answer from the graph, cite the file path and line range when a node has them, answer in English, modify nothing. Where an answer says it read the source instead of the graph, that is marked in the judgement.

## Q1 Which function installs the security-audit skill, and into which directory?

```text
The function is `update_security_audit_skill`, and it installs into `~/.agents/skills/security-audit`.

**Source:** `scripts/update-agent-assets.sh:1830`. It is a subshell function. It takes the archive from `SECURITY_AUDIT_SKILL_ARCHIVE_URL` (`codeload.github.com/cloudflare/security-audit-skill`, pinned to `SECURITY_AUDIT_SKILL_COMMIT`, line 90–94) and checks its SHA-256. It then extracts only `skills/security-audit` into a staging directory, requires `SKILL.md` there, and moves the tree to the install path. It fails closed on a checksum mismatch or a missing `SKILL.md`. It records the install in the installed manifest (line 1872). The function is also dispatched as a single step at line 2330.

**Graph:** The graph does not have a node for this function. `.ua/knowledge-graph.json` lists the other functions in `scripts/update-agent-assets.sh` (around line 13563), but not this one. The graph does link the related test class `SecurityAuditSkillTest` (`tests/unit/test_update_agent_assets.py:463-664`), which covers the pinned install step. I took the function's location and behaviour from the source file, not from the graph.

**Freshness:** The graph's `gitCommitHash` (`182fbaa2`) matches `HEAD`. The only uncommitted changes are under `.ua/`, which are ignored, so the graph is current. Its gap is a missing node, not drift.

I did not modify any files, and I did not run any git commit or push.

exit=0 seconds=21
```

## Q2 Which validator constant lists the asset sources that must carry a reason when pinned, and where is that check applied?

```text
The graph does not name the constant, so I can't give you its name from the graph. The nearest match is the validator's asset-pin check.

**Graph freshness:** `.ua/meta.json` `gitCommitHash` (182fbaa2) matches HEAD, and the project diff is empty, so the graph is current.

**What the graph shows:**

- **Validator file:** `scripts/validate-agent-assets.py`. Its file node says it validates the Codex, Claude Code, MCP, plugin, skill, omp policy and git-config assets, and scans for secrets and home-path leaks.
- **Pin check:** `function:scripts/validate-agent-assets.py:validate_assets`, lines 1270–1388, "Validates every pinned asset in the manifest." This is the most likely place the reason requirement is enforced.
- **Pin reader:** `function:scripts/validate-agent-assets.py:asset_pin_values`, lines 1252–1267, "Reads the pinned values an asset declares in the manifest." It feeds `validate_assets`.
- **Manifest validation:** `function:scripts/validate-agent-assets.py:validate_agent_manifest`, lines 1458–1537, checks the manifest's required keys.
- **Where it runs in CI:** `pipeline:.github/workflows/agent-assets.yml` runs the agent-asset manifest validation on PRs, main pushes, manual runs and a weekly schedule.

**What the graph does not show:**

- No node exists for the constant, so I can't name it or give its line.
- The graph has no call edge from the workflow or `main` to `validate_assets`. It only records that the file contains the function, so the exact call site is also unconfirmed.
- The graph has no node for the pinned-source list in `assets.security-audit-skill` or the reason field.

I haven't read the source. A grep of `scripts/validate-agent-assets.py` for the reason-related constant and its call sites would settle both points. I made no changes to any file and ran no git write commands.

exit=0 seconds=41
```

## Q3 In the brief checker, which function decides whether a line is a section heading, and which section names does it accept?

```text
**Short answer:** The graph names `heading()` as the function that recognizes a section heading, but it does not list which section names are accepted. The graph does not answer the second part.

**Which function decides a heading**
- `heading()` returns the section name when a line is a recognized brief heading, and `None` otherwise. Its node is in the installed copy of the checker, `home/dot_local/bin/common/executable_brief-check.py:264-271`.
- `sections()` uses that rule to split a brief into a name-to-body mapping. It raises `BriefError` when a heading appears twice. That node is at `home/dot_local/bin/common/executable_brief-check.py:274-291`, and the repo copy at `scripts/orchestrator/brief-check.py:274-291` has the same line range.
- The repo copy `scripts/orchestrator/brief-check.py` has no `heading` node in the graph. Its `sections()` is the only heading-splitting node it lists. The graph therefore does not show whether the repo copy calls a separate `heading()`.

**Which section names it accepts**
- The graph does not say. The `heading` summary only says "a recognized brief heading," and the node has no list of names.
- Section names the graph does mention in summaries are `TRUST` and `SCOPE`. The `judge` node's summary says the checks cover trigger terms, `CLOSURE`, `TRUST`, a denylist-dressed-as-form check, and `SCOPE`. The test node `tests/unit/test_brief_check.py` covers "the TRUST section shape" and "lever-count scope rules." These are evidence the checker uses those names, not the complete accepted list.
- To get the exact list, read the `heading()` body at `home/dot_local/bin/common/executable_brief-check.py:264-271`. Then check whether the repo copy at `scripts/orchestrator/brief-check.py` matches it. I did not read the source because the skill asks me to answer from the graph.

**Graph freshness:** Current. `project.gitCommitHash` is `182fbaa2`, which equals `HEAD`. No project files differ from that commit, staged, unstaged, or untracked. Only `.ua/` files show as modified, and those are excluded from the check.

exit=0 seconds=26
```

## Q4 Which Makefile target runs the runtime doctor, and which scripts does it call?

```text
**Short answer:** The graph does not identify the `make` target or its full set of scripts. It only shows that `make doctor` runs `scripts/check-sleep.sh` after a tools check. Reading the `doctor` recipe in the Makefile is the way to get the full list.

**Graph freshness:** Current. `project.gitCommitHash` (`182fbaa2`) equals `git rev-parse HEAD`, and the only working-tree changes are under `.ua/`, which is ignored.

**What the graph says:**

- **Makefile:** `service:Makefile` (`Makefile`) is described as a developer task runner exposing setup, update, apply, doctor, drift, shellcheck, docs and Docker test targets. The graph notes that its 27 targets are not emitted as separate nodes. It has no line range, and no edge links it to any doctor script.
- **Doctor → `scripts/check-sleep.sh`:** `file:scripts/check-sleep.sh` (`scripts/check-sleep.sh`) fails when the Mac may sleep, requiring `pmset -g` to report `SleepDisabled 1`. Its summary says `make doctor` runs it after the tools check. This is the only script the graph ties to `make doctor`.
- **Tools check:** The graph names `file:scripts/check-tools.sh` in the scripts layer, but its summary is not in the graph, so I can't say from it what that check covers.
- **Possible "runtime doctor" candidate:** `file:scripts/check-agent-runtime.py` (`scripts/check-agent-runtime.py`) audits the deployed agent runtime against the chezmoi source: generated-output drift, skill audiences, plugin and extension pins, gh login state, and suggested or applied repair actions. No edge connects it to the Makefile or to `make doctor`, so the graph does not confirm that doctor calls it.
- **Tests:** `tests/unit/test_runtime_health.py` (`RuntimeHealthTest`) covers doctor and runtime-health output, and `tests/unit/test_apply_check.py` covers `make apply-check`, a separate target. Neither file is linked to the Makefile by an edge.

**Layer:** `scripts/check-sleep.sh`, `scripts/check-agent-runtime.py`, `scripts/check-tools.sh` and `scripts/apply-check.sh` all sit in the repository-scripts layer, described as "orchestration, CI helpers, agent runtime checks, usage reporting, and doc generation".

**Next step:** Read the `doctor` recipe in `Makefile` to confirm the exact script calls. The graph can't settle that, and I did not read the Makefile here because the skill's workflow is graph-first.

exit=0 seconds=29
```

## Q5 Where does the runtime doctor decide which skill directories under ~/.agents/skills are installer-owned rather than from home/dot_agents/skills?

```text
The graph does not record a node that decides "installer-owned" directly, so this answer is a best inference from the nearest nodes. The graph is current: its `gitCommitHash` is `182fbaa2`, which matches HEAD, and the project-scoped diff is empty.

**Likely location: `scripts/check-agent-runtime.py`**, the runtime checker that the `make doctor` target runs. Its file node is at `.ua/knowledge-graph.json` line 22265. The graph describes it as auditing the deployed agent runtime against the chezmoi source, including skill audiences. Its `check` function (lines 1328–1402) runs every audit section, and `main` (lines 1412–1461) handles the exit status.

The skill-directory decision is most likely in **`skill_audience_findings`** (`scripts/check-agent-runtime.py:594-645`). The graph summary says it checks that each skill is installed only for its declared audience (Claude, Codex or omp) and reports skills in the wrong place.

Related nodes that feed or mirror that check:
- `skill_audiences` in `scripts/generate-agent-configs.py:1991-2027` maps each skill to the runtimes that should receive it.
- `validate_skill_audience` in `scripts/validate-agent-assets.py:534-582` checks the same audience rule at validation time.
- `compare_tree_contents` (`scripts/check-agent-runtime.py:491-532`) flags "unmanaged top-level entries" in a deployed tree. That is the closest node to "a directory not sourced from `home/`", but I have not confirmed it is the code path that treats `~/.agents/skills` entries as installer-owned.

Tests: `tests/unit/test_check_agent_runtime.py` (node `CheckAgentRuntimeTest`) covers this checker, and `tests/unit/test_runtime_health.py` covers doctor output.

The graph has no node for `~/.agents/skills` installer ownership, and the installer-side summaries I found (`scripts/update-agent-assets.sh` and the vendor-installer nodes) do not mention it. To settle it, read the body of `skill_audience_findings` at `scripts/check-agent-runtime.py:594-645`, and check whether `compare_tree_contents` skips directories the installer manages.

exit=0 seconds=37
```

## Q6 Which steps can scripts/update-agent-assets.sh run alone, and where is that dispatch?

```text
**Short answer:** The graph does not record how `scripts/update-agent-assets.sh` selects steps, so I can't confirm from it which steps run alone. The dispatch point is `main`. Its summary says it "installs and refreshes the managed agent plugin assets in order."

**Freshness:** The graph's `gitCommitHash` (182fbaa2) equals `HEAD`, and the only working-tree changes are under `.ua/`. The graph is current.

**Dispatch:** `function:scripts/update-agent-assets.sh:main`, `scripts/update-agent-assets.sh` lines 2294–2339, tagged `entry-point`. The graph has no call edges out of `main`, so it doesn't show which step functions `main` invokes or in what order.

**Step functions:** Each step is its own function in the same file, and several are shaped to stand alone. These are candidates for running alone, but that is my inference from their names and summaries, not something the graph states:
- Claude plugin steps: `update_claude_superpowers`, `update_claude_crit`, `update_claude_ponytail`, `update_claude_understand_anything`, plus the generic `converge_claude_plugins`.
- Codex plugin steps: `update_codex_superpowers`, `update_codex_ponytail`, `update_codex_crit`, `update_codex_understand_anything`.
- Tool updates: `update_terminal_code`, `update_terminal_browser`, `update_omp`, `update_hcom`, `update_pi_claude_bridge`, `update_compactiondb`.
- Checks: `check_pi_claude_bridge`, `check_pstack`.
- Other maintenance: `ensure_gh_extensions`, `ensure_crit_cli`, `ensure_herdr_integrations`, `refresh_codex_hook_trust`.

The graph also records one step that is explicitly narrow: `refresh_codex_hook_trust` (lines 905–934) "re-applies only the managed Codex config files so their modify scripts re-hash the trusted hooks." `run_pinned_installer` (lines 1492–1511) is a shared helper that downloads and runs an upstream installer after checksum verification, so it is not a user-facing step.

**Gap:** To settle the "run alone" question, read the argument parsing in `main` (lines 2294–2339) or run `/understand --full` so the graph captures call edges. I did not read the script, since this task was limited to the graph.

exit=0 seconds=33
```

## Q7 Which validator function checks the manifest's MCP servers, and what three conditions must a server meet?

```text
The knowledge graph does not contain a validator that checks MCP servers, so I can't name one or the three conditions from it.

**Closest graph matches:**

- **`scripts/validate-agent-assets.py`** (file node, no line range in the graph): its summary says it validates "the Codex, Claude Code, MCP, plugin, skill, omp policy and git-config assets". This is the only graph node that mentions MCP validation, and it is a file-level summary, not a per-server check.
- **`validate_agent_manifest`** (`function:scripts/validate-agent-assets.py:validate_agent_manifest`, lines 1458–1537): "Validates the agent asset manifest and its required keys." Likely the manifest-level entry point, but the summary doesn't mention MCP servers.
- **`validate_assets`** (`function:scripts/validate-agent-assets.py:validate_assets`, lines 1270–1388): "Validates every pinned asset in the manifest." Also not MCP-specific.

The manifest itself is `config:home/dot_agents/agent-config.yaml`. Its summary lists "MCP servers" among its contents, but no node records the server fields or the checks applied to them.

**Graph freshness:** The graph's `gitCommitHash` (182fbaa2) equals HEAD, and the only uncommitted changes are under `.ua/`, so the graph is current. The gap is in the graph's coverage, not its staleness.

**Next step:** The three conditions would need to be read from the source, starting at `scripts/validate-agent-assets.py` around lines 1458–1537 and wherever the MCP check is called. I answered from the graph only, as the skill directs, so I haven't checked the source. I can do that if you want.

exit=0 seconds=21
```

## Q8 Which manifest lines give the nine understand-* skills their audience, and which agents are in it?

```text
The knowledge graph can't answer the specific question. It has the manifest and the code that reads it, but not the nine `understand-*` entries or their audience lines, so I can't name the manifest lines or the agents from it.

**Graph freshness:** `.ua/meta.json` `gitCommitHash` matches `HEAD` (`182fbaa2`). The only changes are uncommitted `.ua/` artifacts, which are ignored, so the graph is current for project source.

**What the graph does have:**

- **The manifest:** `config:home/dot_agents/agent-config.yaml`, at `home/dot_agents/agent-config.yaml`. Its summary says it covers "standing rules, skill audiences, omp seats, command policy, model profiles, plugins, MCP servers and third-party assets." The graph gives no line range for it, and no node for its skill-audience section.
- **The code that maps audiences:** `function:scripts/generate-agent-configs.py:skill_audiences`, lines 1991–2027. Its summary says it "maps each skill to the set of agent runtimes that should receive it."
- **The check on audiences:** `function:scripts/validate-agent-assets.py:validate_skill_audience`, lines 534–582. It "checks that each skill is installed for the audience its manifest names."
- **Runtime audit:** `function:scripts/check-agent-runtime.py:skill_audience_findings` flags skills installed for the wrong runtime (Claude, Codex or omp).

**What the graph lacks:** no node is named `understand-*` or `skill:*`. The understand-anything documents are only `document:home/dot_config/claude/rules/understand-anything.md` and its `.tmpl`. Nothing in the graph lists the nine skills, their audiences, or the agents.

To get the answer, grep `home/dot_agents/agent-config.yaml` for `understand-` and read the audience values on those entries. That is a file read outside the graph, so I haven't done it here. I can run it if you want the exact lines.

exit=0 seconds=28
```

## Q9 Which unit test pins one manifest_record call per install step of the updater, and what count does it assert?

```text
The knowledge graph can't answer this. It has no test-method nodes and no assertion data, so it doesn't name the test or the count it asserts.

The graph is current. Its `gitCommitHash` is `182fbaa2`, which matches `HEAD`, and the only changes since then are under `.ua/`.

What the graph does show, as candidates to check:

- **The updater:** `scripts/update-agent-assets.sh` (file-level node, no line range). Its `record_claude_plugin_step` function (lines 477–490) "records a converged Claude Code plugin step in the installed asset manifest."
- **The manifest writer:** `function:scripts/lib/asset-manifest.sh:_manifest_record` (lines 45–123) "atomically replaces one step entry in the installed asset manifest using jq."
- **Likely test files and classes:**
  - `tests/unit/test_update_agent_assets.py`, `UpdateAgentAssetsTest` (lines 79–460), "covers the main artifact update flow with fake downloads and digests."
  - The same file's `SecurityAuditSkillTest` (463–664), `ProducerFailureTest` (667–2270), and `MaskedStatusTest` (2273–2326).
  - `tests/unit/test_asset_manifest.py`, `AssetManifestTest` (lines 36–399), "verifies that agent asset installs record a manifest with the expected files, modes and content."

None of these summaries mentions counting `manifest_record` calls. To get the answer, grep the test bodies for `manifest_record` (or `_manifest_record`) and check the asserted count in the class ranges above. I haven't read the source, so I can't say which test asserts it or what the count is.

exit=0 seconds=24
```

## Q10 How does the tool doctor report a missing hcom binary, and which function says it?

```text
**Answer:** `check_hcom` in `scripts/check-tools.sh` reports a missing hcom. It prints `hcom not installed; run make update` as a warning and returns 0, so a missing hcom does not fail the check.

**Graph node:** `function:scripts/check-tools.sh:check_hcom`, lines 227–237. It is contained by `file:scripts/check-tools.sh`, which is the health-summary script described at `file:scripts/check-tools.sh`. Its graph summary is only "Reports hcom's installed version beside its manifest pin." It does not mention the missing case, so the graph alone doesn't show that behaviour. I confirmed it by reading the source:

- `check_hcom` tests `${HOME}/.local/bin/hcom` for executability (line 228). If the file is not executable, it calls `warn_optional "hcom not installed; run make update"` and returns 0 (lines 229–231).
- If it is present, it reads the pin from `lib/installer-pins.sh` and prints `found: hcom -> <path> (pin <version>)`, then runs `hcom --version`. A failing version call gives another `warn_optional` (line 236).
- The function is called from line 448 of the same file.

**Why not `check_command`:** `function:scripts/check-tools.sh:check_command` (lines 28–58) prints `required missing: <name>` and increments `required_failures`, which is the hard-failure path. It is not used for hcom. hcom goes through `warn_optional`, so the missing case is a soft warning.

**Graph freshness:** The graph's `gitCommitHash` (`182fbaa2…`) equals `HEAD`, so the committed diff is empty. The only working-tree changes are under `.ua/`, which is ignored, so the graph is current for project files. I did not run the full set of freshness commands, because several Python calls were blocked by a hook; I used `grep` and `sed` instead.

I made no file changes and ran no git writes.

exit=0 seconds=25
```
