# Validation: dotfiles-T133-install-ppa-resilience-a01

- **What follows:** every block is the command as run, then its verbatim output. The producer is the worker (Claude seat, worktree worker-f).
- **Output forms:** `gh … --json` output stays JSON, with no `--jq`.
- **Path forms:** home paths are written `~`, and the sandbox temporary directory `$TMPDIR`.
- **Bats:** it ran only in GitHub Actions, job `test (ubuntu-24.04, client)`.
- **Log lines:** they are filtered to the ghostty tests, with the filter named on the command line.

## 1. Round 1 red at 24210a2b (the round-1 tests on main's installer)

```text
$ gh run view 39689531953 --repo mryfmo/dotfiles --json headSha,conclusion   # round-1 red at 24210a2b, worker (Claude seat)
{"conclusion":"failure","headSha":"24210a2b67e334693c472ec7e11f6a96c60247e0"}
$ gh run view --repo mryfmo/dotfiles --job 119532238630 --log | grep -E '<the ghostty test result, branch, location and assertion lines>'   # https://github.com/mryfmo/dotfiles/actions/runs/39689531953/job/119532238630
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
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:04:43.2292949Z ok 32 [ubuntu-client] an unreachable release API never fails the apply, with or without an installed zed
```

## 2. Round 1 green at dc1ee465

```text
$ gh run view 39692046991 --repo mryfmo/dotfiles --json headSha,conclusion   # round-1 green at dc1ee465, worker (Claude seat)
{"conclusion":"success","headSha":"dc1ee465c86312a7ed67bf8269b56b0933701879"}
$ gh run view --repo mryfmo/dotfiles --job 119540330184 --log | grep -E '<the ghostty test result, branch, location and assertion lines>'   # https://github.com/mryfmo/dotfiles/actions/runs/39692046991/job/119540330184
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:20:36.1330834Z ok 6 [ubuntu-client] PACKAGES for ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:20:36.3500158Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:42.6089506Z # branch: the PPA answered; ghostty must be installed
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:44.5216867Z ok 8 [ubuntu-client] ghostty
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:44.9580742Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:45.4294278Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:21:45.8813954Z ok 11 [ubuntu-client] a non-PPA apt failure still fails the apply
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:23:50.6674073Z ok 32 [ubuntu-client] an unreachable release API never fails the apply, with or without an installed zed
```

## 3. The lint red at 74b3a2d9 (the first fix's `grep -E` on the interpolated host; fixed by `grep -F` in dc1ee465)

```text
$ gh run view 39691074124 --repo mryfmo/dotfiles --json headSha,conclusion   # the lint red, worker (Claude seat)
{"conclusion":"failure","headSha":"74b3a2d9a4b98f3bd88adee4febab0a3075df5d5"}
$ gh run view --repo mryfmo/dotfiles --job 119537107327 --log | grep -E -A12 "FAIL: test_the_changed_files_are_clean"   # https://github.com/mryfmo/dotfiles/actions/runs/39691074124/job/119537107327
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9459501Z FAIL: test_the_changed_files_are_clean_against_the_baseline (test_lint_comparisons.LintComparisonsTest.test_the_changed_files_are_clean_against_the_baseline)
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9460894Z ----------------------------------------------------------------------
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9461429Z Traceback (most recent call last):
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9470577Z   File "~/work/dotfiles/dotfiles/tests/unit/test_lint_comparisons.py", line 333, in test_the_changed_files_are_clean_against_the_baseline
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9471426Z     self.assertEqual((0, ""), (result.returncode, result.stderr), result.stdout)
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9471884Z AssertionError: Tuples differ: (0, '') != (1, '')
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9472099Z 
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9472204Z First differing element 0:
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9472441Z 0
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9472608Z 1
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9472703Z 
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9472777Z - (0, '')
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9472962Z ?  ^
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9473066Z 
test (ubuntu-24.04, client)	UNKNOWN STEP	2026-10-21T23:11:57.9473144Z + (1, '')
$ git show 74b3a2d9:install/ubuntu/client/ghostty.sh > $TMPDIR/g74.sh; python3.15 -I scripts/lint-comparisons.py --baseline /dev/null $TMPDIR/g74.sh --changed $TMPDIR/g74.sh
$TMPDIR/g74.sh:53: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
exit 1
```

## 4. Revise 2 red at ae120581 (the four revise fixtures on the round-1 installer)

```text
$ gh run view 39712193558 --repo mryfmo/dotfiles --json headSha,conclusion   # revise-2 red at ae120581, worker (Claude seat)
{"conclusion":"failure","headSha":"ae120581852baabefb2488b489b8ff4c743882b0"}
$ gh run view --repo mryfmo/dotfiles --job 119605866501 --log | grep -E '<the ghostty test result, branch, location and assertion lines>'   # https://github.com/mryfmo/dotfiles/actions/runs/39712193558/job/119605866501
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:21.3356997Z ok 6 [ubuntu-client] PACKAGES for ghostty
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:21.5480555Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:35.9265036Z # branch: the PPA answered; ghostty must be installed
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:37.3196392Z ok 8 [ubuntu-client] ghostty
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:37.6423792Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:37.9624772Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.2772181Z not ok 11 [ubuntu-client] an apt-get update that reports a failed PPA index without a non-zero exit is an outage
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.2786824Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 105)
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.2825899Z #   `[ "${status}" -eq 0 ]' failed
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.5930475Z not ok 12 [ubuntu-client] a fetch failure from another host stays fatal even when the PPA also failed
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.5943054Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 116)
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.5969874Z #   `[ "${status}" -eq 100 ]' failed
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.9070881Z not ok 13 [ubuntu-client] an installed ghostty is left as it is
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.9081015Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 126)
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:38.9111668Z #   `[ ! -e "${BATS_TEST_TMPDIR}/calls.log" ]' failed
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:39.2138240Z not ok 14 [ubuntu-client] the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:39.2147722Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 131)
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:39.2177940Z #   `[ -f "${template}" ]' failed
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:41:39.5371970Z ok 15 [ubuntu-client] a non-PPA apt failure still fails the apply
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:43:34.6934376Z ok 36 [ubuntu-client] an unreachable release API never fails the apply, with or without an installed zed
```

## 5. Revise 2 green at ed76b740

```text
$ gh run view 39713244770 --repo mryfmo/dotfiles --json headSha,conclusion   # revise-2 green at ed76b740, worker (Claude seat)
{"conclusion":"success","headSha":"ed76b740cc981299fbdc9b0a282c8fe1a8191744"}
$ gh run view --repo mryfmo/dotfiles --job 119609262517 --log | grep -E '<the ghostty test result, branch, location and assertion lines>'   # https://github.com/mryfmo/dotfiles/actions/runs/39713244770/job/119609262517
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:29.7191498Z ok 6 [ubuntu-client] PACKAGES for ghostty
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:30.0689128Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:48.3981615Z # branch: the PPA answered; ghostty must be installed
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:50.7798103Z ok 8 [ubuntu-client] ghostty
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:51.3532196Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:51.9242491Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:52.4845733Z ok 11 [ubuntu-client] an apt-get update that reports a failed PPA index without a non-zero exit is an outage
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:53.0731156Z ok 12 [ubuntu-client] a fetch failure from another host stays fatal even when the PPA also failed
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:53.6241916Z ok 13 [ubuntu-client] an installed ghostty is left as it is
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:54.1587148Z ok 14 [ubuntu-client] the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:54:54.6891815Z ok 15 [ubuntu-client] a non-PPA apt failure still fails the apply
test (ubuntu-24.04, client)	Run unit test	2026-10-22T02:57:06.9729064Z ok 36 [ubuntu-client] an unreachable release API never fails the apply, with or without an installed zed
```

## 6. At ed76b740: bash -n, shellcheck, shfmt, the comparison lint, the caps from the merge-base

```text
$ git rev-parse HEAD   # worker (Claude seat)
ed76b740cc981299fbdc9b0a282c8fe1a8191744
$ bash -n install/ubuntu/client/ghostty.sh
exit 0
$ shellcheck install/ubuntu/client/ghostty.sh
exit 0
$ shfmt -i 4 -sr -d install/ubuntu/client/ghostty.sh
exit 0
$ python3.15 -I scripts/lint-comparisons.py --changed install/ubuntu/client/ghostty.sh home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl
exit 0
$ git merge-base origin/main HEAD
7b21659eb2e86198bde458136d9e31b3e836cdb0
$ git diff --numstat 7b21659eb2e86198bde458136d9e31b3e836cdb0 HEAD
4	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/autoskill.md
7	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/learning.md
68	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/report.md
2	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/result.txt
9	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/sandbox.md
62	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/task.md
72	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/validation.md
13	0	home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl
0	3	home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl
39	4	install/ubuntu/client/ghostty.sh
105	2	tests/install/ubuntu/client/ghostty.bats
$ git diff --numstat 7b21659eb2e86198bde458136d9e31b3e836cdb0 HEAD | awk (outside tests/ and .orchestration/; under tests/)
changed_non_tests=59 of 110; changed_tests=107 of 160
```

## 7. The fakes run in plain bash (not Bats) against the revise and round-1 installers

```text
$ the APT_FAKES snippet run in plain bash (not Bats) against the installer at ed76b740   # worker (Claude seat)
FAIL=update exit=0 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=1
FAIL=pool exit=0 calls.log=yes install-attempted=1 installed-ghostty=0 retry-line=1
FAIL=archive exit=100 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=0
FAIL=none exit=0 calls.log=yes install-attempted=1 installed-ghostty=1 retry-line=0
FAIL=warn exit=0 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=1
FAIL=mixed exit=100 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=0
FAIL=otherppa exit=100 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=0
FAIL=installed exit=0 calls.log=no install-attempted=0 installed-ghostty=0 retry-line=0
$ the same against the round-1 installer at 44134e36
FAIL=update exit=0 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=1
FAIL=pool exit=0 calls.log=yes install-attempted=1 installed-ghostty=0 retry-line=1
FAIL=archive exit=100 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=0
FAIL=none exit=0 calls.log=yes install-attempted=1 installed-ghostty=1 retry-line=0
FAIL=warn exit=1 calls.log=yes install-attempted=1 installed-ghostty=0 retry-line=0
FAIL=mixed exit=0 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=1
FAIL=otherppa exit=0 calls.log=yes install-attempted=0 installed-ghostty=0 retry-line=1
FAIL=installed exit=0 calls.log=yes install-attempted=1 installed-ghostty=1 retry-line=0
```
