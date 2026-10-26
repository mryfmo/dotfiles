# Loaded by tests/unit/test_pr_audit.py into the lever's codex supervisor: the first sigprocmask (the block) works,
# every later one (the unblock, in the parent and in the child) fails.
package FailUnblock;
use POSIX ();
my $calls = 0;
my $real = \&POSIX::sigprocmask;
{
    no warnings 'redefine';
    *POSIX::sigprocmask = sub { return ++$calls == 1 ? $real->(@_) : 0 };
}
1;
