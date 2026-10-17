---
task_id: dotfiles-T128-seat-launch-args-a01
status: final
revise_round: 6
result_round: 3
---

All commands stayed in the managed workspace-write sandbox without escalation, permission-gated actions or persistent configuration changes. Main task/acceptance inputs remain read only; task copy hash unchanged. Only allowed seat source/test and task records are edited, while other branches and untracked logs are preserved.

uv uses UV_CACHE_DIR=/tmp/codex-worker-e-uv-cache. Tests execute copied scripts with synthetic ps/lsof, temporary HOME/profile and fake boundary inputs. New ps stub records only probe option argv, prints the known fixture caller PID and truncates synthetic commands unless ww is present. No real ps/lsof, prompt, secret, pane, browser, daemon or re-seat is probed. Independent review is read only with a /tmp transcript.

Unsigned commit and HTTPS push identity rewrite are per-command; shared git config is untouched and emitted packed-refs/credential-store warnings retained. Authorized GitHub actions are this PR push/body update, CI observation and final-head Bot re-review. No local Bats, Crit browser/server, Plan Mode, human review request, graph update or main write. Orchestrator retains integration/merge.
