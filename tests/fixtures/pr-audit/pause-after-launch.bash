# shellcheck shell=bash
# BASH_ENV for tests/unit/test_pr_audit.py: pauses pr-audit.sh for 2 seconds just before the
# PR_AUDIT_TEST_PAUSE_AT-th (default 3rd) run of the command PR_AUDIT_TEST_PAUSE_COMMAND (default `codex_pid=$!`, the
# assignment after a supervisor's background launch, the third being the `codex exec` run), after writing the lever's
# pid to PR_AUDIT_TEST_PAUSE_FILE, so a test can deliver a signal inside that window. A DEBUG trap, inherited by
# functions (set -T), sees the command about to run.
set -T
pause_seen=0
pause_at() {
    if [[ ${BASH_COMMAND} == "${PR_AUDIT_TEST_PAUSE_COMMAND:-codex_pid=\$!}" ]]; then
        pause_seen=$((pause_seen + 1))
        if ((pause_seen == ${PR_AUDIT_TEST_PAUSE_AT:-3})); then
            printf '%s\n' "$$" > "${PR_AUDIT_TEST_PAUSE_FILE}.tmp" && mv "${PR_AUDIT_TEST_PAUSE_FILE}.tmp" "${PR_AUDIT_TEST_PAUSE_FILE}"
            sleep 2
        fi
    fi
    return 0
}
trap pause_at DEBUG
