# The baseline's rows: every hit of the lint on origin/main 35ab0e95 after Amendment 1 (per file, with the source line)

Generated from `scripts/lint-comparisons.py` run with no baseline over the default file set at 2026-10-17T11:25:33Z (after the worker review's fixes: the test word anywhere on the line, jq programs anchored at the `jq` word); the committed `scripts/lint-comparisons-baseline.tsv` holds one content-hashed row per line below (one row per hit since round 2: remove-agent-asset's two identical lines are two rows). Rows in files an in-flight task owns are that lineage's; the rest are for the orchestrator to assign owners at acceptance (Amendment 1).

## Rows per rule

```
  33 R1
   2 R2
   6 R3
  41 R4
   4 R6
```

## Rows per file

```
  16 scripts/validate-agent-assets.py
  12 home/dot_local/bin/common/executable_herdr-agents
  10 home/dot_local/bin/common/executable_ua-symbol-coverage
   5 scripts/require-crit-review.py
   5 scripts/orchestrator/dispatch.sh
   4 scripts/check-agent-runtime.py
   3 scripts/generate-docs.sh
   3 install/ubuntu/common/aws_cli.sh
   3 home/dot_local/bin/common/executable_remove-agent-asset
   2 scripts/orchestrator/task-consistency-check.py
   2 scripts/orchestrator/local-review.sh
   2 scripts/agent-stop-gate.sh
   2 home/dot_claude/hooks/executable_project-map-reload.sh
   2 home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py
   1 scripts/upgrade-tools.sh
   1 scripts/update-agent-assets.sh
   1 scripts/orchestrator/resolve-threads.sh
   1 scripts/orchestrator/pr-cost.sh
   1 scripts/orchestrator/orch-gate.sh
   1 scripts/orchestrator/local-advisory.sh
   1 scripts/orchestrator/ledger-check.py
   1 scripts/orchestrator/chain-integrate.sh
   1 scripts/lib/github-release.sh
   1 scripts/lib/asset-manifest.sh
   1 scripts/gh-auth.sh
   1 scripts/generate-agent-configs.py
   1 scripts/check-regime-boundary.sh
   1 install/ubuntu/client/default_shell.sh
   1 home/dot_local/bin/common/executable_agent-session-staleness
```

## Every row (rule, file:line, the source line)

```
R4 home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py:559 | new_urls = [item["url"] for item in after_links if item["url"] not in before_urls]
R4 home/dot_agents/skills/gh-comment-attach-files/scripts/attach_comment_files.py:575 | if not any(hint in url for hint in ATTACHMENT_URL_HINTS):
R1 home/dot_claude/hooks/executable_project-map-reload.sh:13 | [[ "$file_path" == */.project-map/index.html ]] || exit 0
R3 home/dot_claude/hooks/executable_project-map-reload.sh:21 | | select(.url | strings | endswith("/.project-map/index.html"))
R4 home/dot_local/bin/common/executable_agent-session-staleness:71 | if any(part in EXCLUDED_DIR_NAMES for part in relative.parts):
R1 home/dot_local/bin/common/executable_herdr-agents:415 | [[ ${git_dir} == "${common}/worktrees/"* ]] || return 0
R1 home/dot_local/bin/common/executable_herdr-agents:538 | [[ ${git_dir} == "${common_dir}" ]]
R3 home/dot_local/bin/common/executable_herdr-agents:757 | | ($processes | length) == 1
R3 home/dot_local/bin/common/executable_herdr-agents:759 | or (($processes[0].argv[0] // $processes[0].name // "") | test("(^|/)-?(ba|z|fi)?sh$")))' > /dev/null &&
R1 home/dot_local/bin/common/executable_herdr-agents:991 | [[ ${worktree} == "$1/.claude/worktrees/"* ]] || continue
R1 home/dot_local/bin/common/executable_herdr-agents:1185 | [[ ${seat_dir} != "${workdir}" ]] || return 0
R1 home/dot_local/bin/common/executable_herdr-agents:1232 | [[ ${common} == */.git && -d ${common%/.git} ]]; then
R3 home/dot_local/bin/common/executable_herdr-agents:1308 | '.result.panes[]? | select(.cwd == $cwd and ($workspace_label == $label or .label == "claude-orchestrator"))' > /dev/null; then
R1 home/dot_local/bin/common/executable_herdr-agents:1394 | [[ ${hook} == "${common_dir}"/* && -f ${hook} ]] || return 0
R1 home/dot_local/bin/common/executable_herdr-agents:1716 | if [[ $# -eq 0 && -n ${seat_worktree} && ${seat_worktree} != .claude/worktrees/* ]]; then
R1 home/dot_local/bin/common/executable_herdr-agents:2025 | [[ ${audit_out} == /* ]] || audit_out="${workdir}/${audit_out}"
R6 home/dot_local/bin/common/executable_herdr-agents:2092 | } | grep -oE "${audit_marker}:[0-9]+" | tail -n 1 | cut -d: -f2 || true)"
R1 home/dot_local/bin/common/executable_remove-agent-asset:82 | [ "$1" = "$2" ] || [[ "$1" == "$2/"* ]]
R1 home/dot_local/bin/common/executable_remove-agent-asset:100 | if [ "${candidate}" != "${root}" ] && path_has_prefix "${candidate}" "${root}"; then
R1 home/dot_local/bin/common/executable_remove-agent-asset:209 | if [ "${candidate}" != "${root}" ] && path_has_prefix "${candidate}" "${root}"; then
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:90 | if path.endswith(".py") or "python" in first or "uv run" in first:
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:92 | if path.endswith(".rb") or "ruby" in first:
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:94 | if path.endswith((".sh", ".bash", ".zsh", ".bats")) or re.search(
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:170 | if path in old or path in new or posixpath.dirname(path) not in covered:
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:172 | if not path.endswith(GRAMMAR_SUFFIXES):
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:218 | if defs is None and path in moved
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:230 | if path in successors:
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:236 | deleted = defs is None and args.old_ref is not None and path not in successors
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:239 | if path in old_blobs and old_blobs[path][1] == new_blobs.get(source, ("", ""))[1]:
R4 home/dot_local/bin/common/executable_ua-symbol-coverage:241 | elif path not in old and path not in judged and isinstance(defs, int) and defs and not after:
R1 install/ubuntu/client/default_shell.sh:17 | if [ "${current_shell}" = "${zsh_path}" ]; then
R1 install/ubuntu/common/aws_cli.sh:66 | if [[ "${version_token}" != aws-cli/* ]]; then
R1 install/ubuntu/common/aws_cli.sh:81 | if [ "${version}" != "aws-cli/$1" ]; then
R1 install/ubuntu/common/aws_cli.sh:161 | [ "$(verify_aws_cli_version "${AWS_CLI_BIN_DIR}/aws" "AWS CLI check" 2> /dev/null)" != "aws-cli/${staged_version}" ]; then
R1 scripts/agent-stop-gate.sh:114 | elif [[ ${top} == */.claude/worktrees/* && "$(git -C "${top%/.claude/worktrees/*}" rev-parse --path-format=absolute --git-dir 2> /dev/null)"
R1 scripts/agent-stop-gate.sh:126 | exempt() { [[ $1 == .orchestration/* || $1 == .agents/worklog/* ]]; }
R4 scripts/check-agent-runtime.py:133 | return rel in AGMSG_LEGACY_RUNTIME_FILES or any(
R4 scripts/check-agent-runtime.py:134 | rel == ignored or ignored in rel.parents or (ignored == Path("agmsg/db") and str(rel).startswith("agmsg/db-"))
R4 scripts/check-agent-runtime.py:677 | if value == "~":
R4 scripts/check-agent-runtime.py:679 | if value.startswith("~/"):
R3 scripts/check-regime-boundary.sh:191 | jq -e --arg main "${main}" '.result.panes[]? | (.cwd // "") | select(. == $main or startswith($main + "/"))' > /dev/null 2>&1; then
R4 scripts/generate-agent-configs.py:1369 | and path not in output_set
R1 scripts/generate-docs.sh:129 | if [[ "${output_path}" == *.sh ]]; then
R2 scripts/generate-docs.sh:145 | case "${source_path}" in
R1 scripts/generate-docs.sh:518 | if [[ "${source_path}" == home/dot_config/alias/* ]]; then
R1 scripts/gh-auth.sh:50 | if [[ ${source} == */hosts.yml ]]; then
R1 scripts/lib/asset-manifest.sh:75 | [[ "${path}" == /* ]] || return 1
R1 scripts/lib/github-release.sh:28 | [ "${GITHUB_SERVER_URL:-https://github.com}" != https://github.com ] || [ "${GH_HOST:-github.com}" != github.com ]
R1 scripts/orchestrator/chain-integrate.sh:67 | [[ ${found} == /* && ${found} != */shims/* ]] || refuse 10 "no binary outside a shims directory: ${found:-none}"
R1 scripts/orchestrator/dispatch.sh:109 | [[ ${home} == /* ]] || {
R1 scripts/orchestrator/dispatch.sh:190 | [[ ${path} == /* ]] || path="${root}/${path}"
R1 scripts/orchestrator/dispatch.sh:202 | tf="$(value_of task_file)" && [[ ${tf} == /* ]] || tf="${root}/${tf}"
R1 scripts/orchestrator/dispatch.sh:209 | [[ ${py} == /* ]] || {
R1 scripts/orchestrator/dispatch.sh:334 | [[ ${record} == /* ]] || record="${PWD}/${record}"
R4 scripts/orchestrator/ledger-check.py:24 | if item["source"] == "review_comment" and item.get("author") == BOT and "discussion_r" in url:
R6 scripts/orchestrator/local-advisory.sh:81 | row=$(/usr/bin/grep -E "^(${ids%|})	" "$A" | /usr/bin/grep -v '	advisory-p2$' | tail -1 || true)
R1 scripts/orchestrator/local-review.sh:82 | [[ $found == /* ]] || found=$R/$found
R1 scripts/orchestrator/local-review.sh:83 | [[ $found != */shims/* ]] || {
R1 scripts/orchestrator/orch-gate.sh:72 | [[ ${found} == /* && ${found} != */shims/* ]] || refuse "no binary for ${name} outside a shims directory ('${found}')"
R6 scripts/orchestrator/pr-cost.sh:49 | local_n=$({ /usr/bin/grep -l -E "^pr: ${pr}\$" .orchestration/validation/*local-review-*.md 2> /dev/null || true; } |
R3 scripts/orchestrator/resolve-threads.sh:45 | 'first(.items[] | select((.url // "") | endswith($suffix)) | .disposition // "") // ""' "${sweep}")
R4 scripts/orchestrator/task-consistency-check.py:56 | if not any(a.startswith(own_dir) for a in allowed):
R4 scripts/orchestrator/task-consistency-check.py:118 | if probe.startswith("scripts/"):
R4 scripts/require-crit-review.py:155 | if path.startswith(IGNORED_PREFIXES):
R4 scripts/require-crit-review.py:247 | all(path.endswith(LOW_RISK_SUFFIXES) for path in paths)
R4 scripts/require-crit-review.py:254 | if path in HIGH_RISK_FILES:
R4 scripts/require-crit-review.py:256 | if path.startswith(HIGH_RISK_PREFIXES):
R4 scripts/require-crit-review.py:1055 | if head is not None and not all(path.startswith(".orchestration/") for path in paths):
R2 scripts/update-agent-assets.sh:269 | case "$(uname -s)/$(uname -m)" in
R1 scripts/upgrade-tools.sh:283 | [[ -n "${version}" && "${install_dir}" == /* ]] || return 1
R4 scripts/validate-agent-assets.py:109 | data = tomllib.loads(text) if file_type == "toml" else json.loads(text)
R4 scripts/validate-agent-assets.py:262 | if plugin.get("name") == "crit" and path_value == "./.codex/plugins/crit":
R4 scripts/validate-agent-assets.py:311 | extra = [path for path in allow_write if path not in writable_roots]
R4 scripts/validate-agent-assets.py:315 | if not isinstance(path, str) or not path.startswith(("/", "~/")) or any(char in path for char in "*?[]{}")
R4 scripts/validate-agent-assets.py:346 | if settings.get("$schema") != "https://json.schemastore.org/claude-code-settings.json":
R4 scripts/validate-agent-assets.py:371 | if not crit_rule.exists() or "/crit" not in crit_rule.read_text():
R4 scripts/validate-agent-assets.py:441 | if not text.startswith("#:schema https://developers.openai.com/codex/config-schema.json"):
R4 scripts/validate-agent-assets.py:470 | if "<old-home-prefix>" in shell_path:
R4 scripts/validate-agent-assets.py:472 | if "{{ .chezmoi.homeDir }}" not in shell_path:
R4 scripts/validate-agent-assets.py:475 | if "<old-home-prefix>" in project_path:
R4 scripts/validate-agent-assets.py:477 | if "{{ .chezmoi.workingTree }}" not in project_path:
R4 scripts/validate-agent-assets.py:789 | if canonical_dir != "~/.agents/skills":
R4 scripts/validate-agent-assets.py:1025 | codex.get("marketplaces", {}).get("ponytail", {}).get("source")
R4 scripts/validate-agent-assets.py:1296 | if directory == ROOT:
R4 scripts/validate-agent-assets.py:1371 | if home and home != "<root-home>":
R6 scripts/validate-agent-assets.py:1374 | return re.compile(rf"(?:{'|'.join(forms)})(?![\w.-])")
```
