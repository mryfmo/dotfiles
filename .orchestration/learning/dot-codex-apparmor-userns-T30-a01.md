# T30 learning triage

## Candidates

1. codex-cli 0.157.1 (Linux) runs the **system `/usr/bin/bwrap` by absolute
   path** from `codex-linux-sandbox`. It does not look bwrap up on PATH, and
   the bundled `codex-resources/bwrap` went unused while the system binary
   was present. To find which executable creates a namespace, run
   `strace -f -e trace=execve codex sandbox true`, and also put a logging
   shim first in PATH. An AppArmor userns grant must target the executable
   that strace shows.
2. Under `apparmor_restrict_unprivileged_userns=1`, a non-root user cannot
   read `/sys/kernel/security/apparmor/profiles` or `aa-status`. A doctor
   check must use an effective probe (`bwrap --ro-bind / / true`), not
   "is the profile loaded".
3. `apparmor_parser -Q -K -I /etc/apparmor.d <file>` parse-checks a profile
   without root and without loading it. A missing trailing comma makes it
   exit 1, so it works as a CI-free syntax gate.
4. Tests that run the real `scripts/check-tools.sh` inherit host kernel
   state. Any new host-reading doctor check needs an env seam, and the shared
   `doctor_environment` fixture must pin it, or results depend on the host.
5. `test_permgate.PermgateTest.test_bench_runs_five_layer_two_fixtures`
   failed once in a full `make unit-test` run (`successful_classifications`
   0 != 5), then passed 3/3 in isolation and in a full rerun. It is
   timing-flaky and unrelated to T30.

## Disposition

Candidates only. Do not promote automatically. Candidate 5 may deserve its
own task: de-flake the permgate bench test.
