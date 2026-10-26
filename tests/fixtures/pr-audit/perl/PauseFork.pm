# Loaded by tests/unit/test_pr_audit.py into the lever's codex supervisor for the `codex exec` run only: after fork
# returns in the parent, and before the caller can store the child's pid, it writes the supervisor's pid to the file
# named on import (`-MPauseFork=<file>`) and sleeps 2 seconds, the window a signal must not open.
package PauseFork;
my $file;
my $exec = grep { $_ eq 'exec' } @ARGV;
sub import { $file = $_[1] }
BEGIN {
    *CORE::GLOBAL::fork = sub {
        my $pid = CORE::fork();
        if ($exec && defined $pid && $pid) {
            if (open(my $out, '>', "$file.tmp")) { print {$out} "$$\n"; close $out; rename "$file.tmp", $file }
            sleep 2;
        }
        return $pid;
    };
}
1;
