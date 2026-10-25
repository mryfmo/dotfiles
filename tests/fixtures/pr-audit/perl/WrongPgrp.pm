# Loaded by tests/unit/test_pr_audit.py into the lever's codex supervisor: setpgrp succeeds but the group is not the
# child's own (getpgrp names group 1).
package WrongPgrp;
BEGIN { *CORE::GLOBAL::getpgrp = sub { return 1 }; }
1;
