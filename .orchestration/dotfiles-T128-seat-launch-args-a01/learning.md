---
task_id: dotfiles-T128-seat-launch-args-a01
status: final
revise_round: 5
result_round: 2
---

No promotion requested. The approved parent-PID check detects a nonempty list hiding the caller as unknown4 before seat selection; parent-present absence still means unlaunched3. It is a visibility proxy, not proof that arbitrary workers/host namespaces are visible. The code comment and report retain that residual; earlier failed/empty fixes did not close it generally.

Shell command substitution can introduce an intermediate parent. A boundary test fixture must capture PPID immediately before exec of the checker, rather than assuming the outer boundary shell PID is the parent. A temporary exec shim preserves the true relationship without modifying the production checker bytes or querying ps. The full suite caught the wrong fixture and passed after correction.

Splitting the first equals sign in a managed token preserves the remaining value and all-occurrence mismatch latching. Empty and additional-equals values differ; observed values stay absent from diagnostics, as independently tested with synthetic markers.
