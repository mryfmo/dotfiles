# Validation: dotfiles-T133-install-ppa-resilience-a01

Verbatim outputs (worker, Claude seat). Home paths are written `~` and the sandbox temporary directory `$TMPDIR`. Bats ran only in GitHub Actions.

## 1. Red: `test (ubuntu-24.04, client)` at 24210a2b (the tests on main's installer)

```text
$ gh run view 39689531953 --json headSha,conclusion   # red run, worker (Claude seat)
24210a2b67e334693c472ec7e11f6a96c60247e0	failure
$ gh run view --job 119532238630 --log | the ghostty lines (https://github.com/mryfmo/dotfiles/actions/runs/39689531953/job/119532238630)
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:00:26.8640635Z ok 6 [ubuntu-client] PACKAGES for ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:00:27.2086469Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:11.6723089Z # branch: the PPA answered; ghostty must be installed
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:13.9373481Z ok 8 [ubuntu-client] ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:14.4700187Z not ok 9 [ubuntu-client] an unreachable PPA never fails the apply
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:14.4714366Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 75)
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:14.4756215Z #   `[ "${status}" -eq 0 ]' failed
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:14.9920422Z not ok 10 [ubuntu-client] a failed PPA package download never fails the apply
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:14.9953168Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 85)
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:14.9978902Z #   `[ "${status}" -eq 0 ]' failed
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:02:15.5237701Z ok 11 [ubuntu-client] a non-PPA apt failure still fails the apply
```

## 2. Green: `test (ubuntu-24.04, client)` at dc1ee465

```text
$ gh run view 39692046991 --json headSha,conclusion   # green run, worker (Claude seat)
dc1ee465c86312a7ed67bf8269b56b0933701879	success
$ gh run view --job 119540330184 --log | the ghostty lines (https://github.com/mryfmo/dotfiles/actions/runs/39692046991/job/119540330184)
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:20:36.1330834Z ok 6 [ubuntu-client] PACKAGES for ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:20:36.3500158Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:42.6089506Z # branch: the PPA answered; ghostty must be installed
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:44.5216867Z ok 8 [ubuntu-client] ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:44.9580742Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:45.4294278Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:45.8813954Z ok 11 [ubuntu-client] a non-PPA apt failure still fails the apply
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:23:50.6674073Z ok 32 [ubuntu-client] an unreachable release API never fails the apply, with or without an installed zed
```

## 3. Static checks, the comparison lint, the caps from the merge-base

```text
$ git rev-parse HEAD   # worker (Claude seat)
dc1ee465c86312a7ed67bf8269b56b0933701879
$ bash -n install/ubuntu/client/ghostty.sh
exit 0
$ shellcheck install/ubuntu/client/ghostty.sh
exit 0
$ shfmt -i 4 -sr -d install/ubuntu/client/ghostty.sh
exit 0
$ python3.15 -I scripts/lint-comparisons.py --changed install/ubuntu/client/ghostty.sh
exit 0
$ git merge-base origin/main HEAD; git diff --numstat <merge-base> HEAD
7da0cdfab9de9fbea673b82379acd4e317115065
31	4	install/ubuntu/client/ghostty.sh
56	2	tests/install/ubuntu/client/ghostty.bats
```

## 4. The fakes in plain bash against both installers (no Bats)

```text
$ the APT_FAKES snippet in plain bash (not Bats) with the fixed installer at dc1ee465   # worker (Claude seat)
FAIL=update exit=0 installed-ghostty=0 retry-line=1
FAIL=pool exit=0 installed-ghostty=0 retry-line=1
FAIL=archive exit=100 installed-ghostty=0 retry-line=0
FAIL=none exit=0 installed-ghostty=1 retry-line=0
$ the same with main's installer (7da0cdfa)
FAIL=update exit=100 installed-ghostty=0 retry-line=0
FAIL=pool exit=100 installed-ghostty=0 retry-line=0
FAIL=archive exit=100 installed-ghostty=0 retry-line=0
FAIL=none exit=0 installed-ghostty=1 retry-line=0
```
