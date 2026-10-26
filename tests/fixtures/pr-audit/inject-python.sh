#!/bin/sh
# @file inject-python.sh
# @brief `python3` for tests/unit/test_pr_audit.py: runs the lever's codex supervisor with injected code before it.
# @description
#   Linked as `python3` first on PATH. When called as the lever's supervisor (`-I -S -c <source>` whose source holds
#   `start_new_session`), it runs PR_AUDIT_TEST_REAL_PYTHON with the same flags and the code in the file
#   PR_AUDIT_TEST_INJECT placed before that source, so a test can replace a library call (Popen, os.killpg,
#   signal.signal) and watch the supervisor fail closed. Any other call runs the real python3 unchanged.
real=${PR_AUDIT_TEST_REAL_PYTHON:?}
if [ "$#" -ge 4 ] && [ "$1" = -I ] && [ "$2" = -S ] && [ "$3" = -c ]; then
    case $4 in
    *start_new_session*)
        source=$4
        shift 4
        inject=$(cat -- "${PR_AUDIT_TEST_INJECT:?}") || exit 97
        exec "$real" -I -S -c "$inject
$source" "$@"
        ;;
    esac
fi
exec "$real" "$@"
