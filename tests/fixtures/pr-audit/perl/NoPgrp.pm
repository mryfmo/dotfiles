# Loaded by tests/unit/test_pr_audit.py into the lever's codex supervisor: setpgrp fails as it does without permission.
package NoPgrp;
BEGIN { *CORE::GLOBAL::setpgrp = sub { $! = 1; return 0 }; }
1;
