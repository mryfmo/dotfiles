# M-13 comparison questions (corpus: this repository at 182fbaa2)

Each question is put verbatim to both tools. The ground truth is the file and line a reader finds today (line numbers re-checked by grep on 2026-11-04 against 182fbaa2, whose code is byte-identical to c92078d0: sync 33 changed records only); a correct answer names that file and line or the exact symbol, a partial answer names the file or the symbol with one element wrong or missing, a wrong answer names neither. Questions marked `(new since 2026-10-02)` concern code that did not exist at the committed Understand-Anything graph's commit (940a3a2b); they are fair only after the refresh in the scratch clone.

## Q1 Which function installs the security-audit skill, and into which directory?
Ground truth: `update_security_audit_skill`, scripts/update-agent-assets.sh:1830; install_dir `~/.agents/skills/security-audit` (:1831). (new since 2026-10-02)

## Q2 Which validator constant lists the asset sources that must carry a reason when pinned, and where is that check applied?
Ground truth: `PINNED_RELEASE_SOURCES`, scripts/validate-agent-assets.py:1228-1234; the check at :1301 inside `validate_assets` (:1270).

## Q3 In the brief checker, which function decides whether a line is a section heading, and which section names does it accept?
Ground truth: `heading`, scripts/orchestrator/brief-check.py:264-271; the names are `SECTIONS` at :156-169 plus the `WORKER RULES (...)` line (`WORKER_RULES`, :171). (new since 2026-10-02)

## Q4 Which Makefile target runs the runtime doctor, and which scripts does it call?
Ground truth: `doctor`, Makefile:167-180: scripts/check-tools.sh, scripts/check-sleep.sh, scripts/update-agent-assets.sh check_pi_claude_bridge and check_pstack (when omp is installed), scripts/check-agent-runtime.py, scripts/lint-retired-terms.py.

## Q5 Where does the runtime doctor decide which skill directories under ~/.agents/skills are installer-owned rather than from home/dot_agents/skills?
Ground truth: `installer_owned_skill_names`, scripts/check-agent-runtime.py:535-553.

## Q6 Which steps can scripts/update-agent-assets.sh run alone, and where is that dispatch?
Ground truth: scripts/update-agent-assets.sh:2296-2303, in `main` (:2294): update_pi_claude_bridge, update_security_audit_skill, check_pi_claude_bridge, check_pstack, retire_shared_pstack_copies, retire_marketplace_dev_workflows, retire_agmsg_shim.

## Q7 Which validator function checks the manifest's MCP servers, and what three conditions must a server meet?
Ground truth: `validate_agent_manifest` (def scripts/validate-agent-assets.py:1458), the checks at :1512-1521: disabled by default, not targeted at Claude, exposed to Codex alone.

## Q8 Which manifest lines give the nine understand-* skills their audience, and which agents are in it?
Ground truth: home/dot_agents/agent-config.yaml:104-112; `[codex, omp, omp-orchestrator, omp-worker]`.

## Q9 Which unit test pins one manifest_record call per install step of the updater, and what count does it assert?
Ground truth: `test_updater_has_one_recording_call_for_each_install_step`, tests/unit/test_asset_manifest.py:257-289; the count 15 (:281). (count new since 2026-10-02)

## Q10 How does the tool doctor report a missing hcom binary, and which function says it?
Ground truth: `check_hcom`, scripts/check-tools.sh:227-231: `warn_optional "hcom not installed; run make update"` (:230) when `~/.local/bin/hcom` is not executable.

