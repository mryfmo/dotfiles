# plan 025 round 4: orchestrator-side mechanical checks (2026-10-22T16:00Z)

Read-only checks run by the orchestrator while reviewers J and K were still running; they complement, not replace, the independent reviews.

- srt JSON schema (jq): srt-worker.json, srt-audit.json, srt-orchestrator.json each carry `network.allowedDomains`, `network.deniedDomains`, `filesystem.denyRead`, `filesystem.allowWrite`, `filesystem.denyWrite` as arrays and `network.allowLocalBinding` as a boolean; no `allowPty` key at the checked paths (verify against srt-facts whether it is required or optional).
- Placeholders in the handouts: only the documented forms `__MAIN__`, `__SEAT__`, `__TMP__`, `__SRT__`, `__SETTINGS__`, `__OMP__`, `__LOG__`; one literal `$TMPDIR` in leg2.md line 48 (host-side command context pasted below for the reviewer).
- No home-directory paths and no account name in the seven handout files (grep).
- events.ts: `session_stop` handled with a per-task counter (`PILOT_STOP_N`, default 1, cap marker at 3) and try/catch on handlers; the tool_call block fires only on the probe token `--pilot-hook-probe`.
- Plan v4: §1.10 and W0 carry the GitHub identity split with the ruleset approval rule; §2 keep row records strict=false and thread resolution=false (D-024-01/02).

leg2.md 46-49:
```
{ sleep 20; grep -l -- "--dir $PILOT/clone" ~/.hcom/.tmp/launch/*.sh | xargs grep -h -o -- '--hcom-tool-path [^ ]*'; sqlite3 -readonly ~/.hcom/hcom.db "select name,pid,launch_args from instances where
# 4b 席内の環境（TASK 1 本）
{ hcom send --from orch @pilot2- --json -- 'AGMSG-TASK v1 task_id=pilot-env instruction: run each command with your bash tool and report its full output: env | cut -d= -f1 | sort; echo TMPDIR=$TMPDIR;
# 4c allowLocalBinding: false（判定。listening が立てば worker/audit の既定は false）
```
