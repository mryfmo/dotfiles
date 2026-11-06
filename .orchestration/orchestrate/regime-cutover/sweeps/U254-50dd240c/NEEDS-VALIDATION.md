# Needs validation: dotfiles at 50dd240c43f6984ffc9c8b9c6aafd09fda4bb2ba

No unresolved record exists in this run, and run-5 carried none.

Both environment-dependent branches were settled from source:
- whether a host can be made to look like a runner and skip the zone;
- whether a crafted `/etc/localtime` target can make the suffix test lie.

Each needs either control of the operator's own bootstrap environment or root ownership of `/etc/localtime`, which is the authority the step already runs with. Each can only leave the timezone as it was, and the timezone is not a security control. So there is no lower-trust principal and no lead. The idempotence gap (a dangling link skips the `tzdata` install) is a robustness note in `REPORT.md` section 6.
