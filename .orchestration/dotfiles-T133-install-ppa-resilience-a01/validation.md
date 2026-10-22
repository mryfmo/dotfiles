# Validation: dotfiles-T133-install-ppa-resilience-a01

- **What follows:** each block holds only commands that were executed, each printed as `$ <command>` exactly as it ran, then its verbatim output and `exit <status>`. The producer is the worker (Claude seat, worktree worker-f).
- **Path forms:** home paths are written `~`, and the sandbox temporary directory `$TMPDIR`.
- **Bats:** it ran only in GitHub Actions, job `test (ubuntu-24.04, client)`; `smoke.sh` beside this file runs the fakes in plain bash.

## 1. Round 1 red at 24210a2b (the round-1 tests on main's installer)

```text
$ gh run view 39689531953 --repo mryfmo/dotfiles --json headSha,conclusion
{"conclusion":"failure","headSha":"24210a2b67e334693c472ec7e11f6a96c60247e0"}
exit 0
$ XDG_CACHE_HOME="$TMPDIR/ghcache" gh run view --repo mryfmo/dotfiles --job 119532238630 --log | cut -f3- | grep -E 'ok [0-9]+ \[ubuntu-client\] (PACKAGES for ghostty|DEPENDENCY_PACKAGES for ghostty|ghostty$|an unreachable PPA|a failed PPA|a non-PPA|an apt-get update|a fetch failure|an installed ghostty|a non-fetch|a half-configured|the ghostty step)|# branch|ghostty\.bats, line|#   `'
2026-10-21T23:00:26.8640635Z ok 6 [ubuntu-client] PACKAGES for ghostty
2026-10-21T23:00:27.2086469Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
2026-10-21T23:02:11.6723089Z # branch: the PPA answered; ghostty must be installed
2026-10-21T23:02:13.9373481Z ok 8 [ubuntu-client] ghostty
2026-10-21T23:02:14.4700187Z not ok 9 [ubuntu-client] an unreachable PPA never fails the apply
2026-10-21T23:02:14.4714366Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 75)
2026-10-21T23:02:14.4756215Z #   `[ "${status}" -eq 0 ]' failed
2026-10-21T23:02:14.9920422Z not ok 10 [ubuntu-client] a failed PPA package download never fails the apply
2026-10-21T23:02:14.9953168Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 85)
2026-10-21T23:02:14.9978902Z #   `[ "${status}" -eq 0 ]' failed
2026-10-21T23:02:15.5237701Z ok 11 [ubuntu-client] a non-PPA apt failure still fails the apply
exit 0
```

## 2. Round 1 green at dc1ee465

```text
$ gh run view 39692046991 --repo mryfmo/dotfiles --json headSha,conclusion
{"conclusion":"success","headSha":"dc1ee465c86312a7ed67bf8269b56b0933701879"}
exit 0
$ XDG_CACHE_HOME="$TMPDIR/ghcache" gh run view --repo mryfmo/dotfiles --job 119540330184 --log | cut -f3- | grep -E 'ok [0-9]+ \[ubuntu-client\] (PACKAGES for ghostty|DEPENDENCY_PACKAGES for ghostty|ghostty$|an unreachable PPA|a failed PPA|a non-PPA|an apt-get update|a fetch failure|an installed ghostty|a non-fetch|a half-configured|the ghostty step)|# branch|ghostty\.bats, line|#   `'
2026-10-21T23:20:36.1330834Z ok 6 [ubuntu-client] PACKAGES for ghostty
2026-10-21T23:20:36.3500158Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
2026-10-21T23:21:42.6089506Z # branch: the PPA answered; ghostty must be installed
2026-10-21T23:21:44.5216867Z ok 8 [ubuntu-client] ghostty
2026-10-21T23:21:44.9580742Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
2026-10-21T23:21:45.4294278Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
2026-10-21T23:21:45.8813954Z ok 11 [ubuntu-client] a non-PPA apt failure still fails the apply
exit 0
```

## 3. The lint red at 74b3a2d9 (`grep -E` on the interpolated host; dc1ee465 uses `grep -F`)

```text
$ gh run view 39691074124 --repo mryfmo/dotfiles --json headSha,conclusion
{"conclusion":"failure","headSha":"74b3a2d9a4b98f3bd88adee4febab0a3075df5d5"}
exit 0
$ XDG_CACHE_HOME="$TMPDIR/ghcache" gh run view --repo mryfmo/dotfiles --job 119537107327 --log | cut -f3- | grep -E -A14 'FAIL: test_the_changed_files_are_clean'
2026-10-21T23:11:57.9459501Z FAIL: test_the_changed_files_are_clean_against_the_baseline (test_lint_comparisons.LintComparisonsTest.test_the_changed_files_are_clean_against_the_baseline)
2026-10-21T23:11:57.9460894Z ----------------------------------------------------------------------
2026-10-21T23:11:57.9461429Z Traceback (most recent call last):
2026-10-21T23:11:57.9470577Z   File "~/work/dotfiles/dotfiles/tests/unit/test_lint_comparisons.py", line 333, in test_the_changed_files_are_clean_against_the_baseline
2026-10-21T23:11:57.9471426Z     self.assertEqual((0, ""), (result.returncode, result.stderr), result.stdout)
2026-10-21T23:11:57.9471884Z AssertionError: Tuples differ: (0, '') != (1, '')
2026-10-21T23:11:57.9472099Z 
2026-10-21T23:11:57.9472204Z First differing element 0:
2026-10-21T23:11:57.9472441Z 0
2026-10-21T23:11:57.9472608Z 1
2026-10-21T23:11:57.9472703Z 
2026-10-21T23:11:57.9472777Z - (0, '')
2026-10-21T23:11:57.9472962Z ?  ^
2026-10-21T23:11:57.9473066Z 
2026-10-21T23:11:57.9473144Z + (1, '')
exit 0
$ git show 74b3a2d9:install/ubuntu/client/ghostty.sh > "$TMPDIR/g74.sh" && "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I scripts/lint-comparisons.py --baseline /dev/null "$TMPDIR/g74.sh" --changed "$TMPDIR/g74.sh"
$TMPDIR/g74.sh:53: R6 an identifier is interpolated into a regex (grep -E on $name; re.* on an f-string)
exit 1
```

## 4. Revise 2 red at ae120581 (the revise-2 tests on the round-1 installer)

```text
$ gh run view 39712193558 --repo mryfmo/dotfiles --json headSha,conclusion
{"conclusion":"failure","headSha":"ae120581852baabefb2488b489b8ff4c743882b0"}
exit 0
$ XDG_CACHE_HOME="$TMPDIR/ghcache" gh run view --repo mryfmo/dotfiles --job 119605866501 --log | cut -f3- | grep -E 'ok [0-9]+ \[ubuntu-client\] (PACKAGES for ghostty|DEPENDENCY_PACKAGES for ghostty|ghostty$|an unreachable PPA|a failed PPA|a non-PPA|an apt-get update|a fetch failure|an installed ghostty|a non-fetch|a half-configured|the ghostty step)|# branch|ghostty\.bats, line|#   `'
2026-10-22T02:41:21.3356997Z ok 6 [ubuntu-client] PACKAGES for ghostty
2026-10-22T02:41:21.5480555Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
2026-10-22T02:41:35.9265036Z # branch: the PPA answered; ghostty must be installed
2026-10-22T02:41:37.3196392Z ok 8 [ubuntu-client] ghostty
2026-10-22T02:41:37.6423792Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
2026-10-22T02:41:37.9624772Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
2026-10-22T02:41:38.2772181Z not ok 11 [ubuntu-client] an apt-get update that reports a failed PPA index without a non-zero exit is an outage
2026-10-22T02:41:38.2786824Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 105)
2026-10-22T02:41:38.2825899Z #   `[ "${status}" -eq 0 ]' failed
2026-10-22T02:41:38.5930475Z not ok 12 [ubuntu-client] a fetch failure from another host stays fatal even when the PPA also failed
2026-10-22T02:41:38.5943054Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 116)
2026-10-22T02:41:38.5969874Z #   `[ "${status}" -eq 100 ]' failed
2026-10-22T02:41:38.9070881Z not ok 13 [ubuntu-client] an installed ghostty is left as it is
2026-10-22T02:41:38.9081015Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 126)
2026-10-22T02:41:38.9111668Z #   `[ ! -e "${BATS_TEST_TMPDIR}/calls.log" ]' failed
2026-10-22T02:41:39.2138240Z not ok 14 [ubuntu-client] the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it
2026-10-22T02:41:39.2147722Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 131)
2026-10-22T02:41:39.2177940Z #   `[ -f "${template}" ]' failed
2026-10-22T02:41:39.5371970Z ok 15 [ubuntu-client] a non-PPA apt failure still fails the apply
exit 0
```

## 5. Revise 2 green at ed76b740

```text
$ gh run view 39713244770 --repo mryfmo/dotfiles --json headSha,conclusion
{"conclusion":"success","headSha":"ed76b740cc981299fbdc9b0a282c8fe1a8191744"}
exit 0
$ XDG_CACHE_HOME="$TMPDIR/ghcache" gh run view --repo mryfmo/dotfiles --job 119609262517 --log | cut -f3- | grep -E 'ok [0-9]+ \[ubuntu-client\] (PACKAGES for ghostty|DEPENDENCY_PACKAGES for ghostty|ghostty$|an unreachable PPA|a failed PPA|a non-PPA|an apt-get update|a fetch failure|an installed ghostty|a non-fetch|a half-configured|the ghostty step)|# branch|ghostty\.bats, line|#   `'
2026-10-22T02:54:29.7191498Z ok 6 [ubuntu-client] PACKAGES for ghostty
2026-10-22T02:54:30.0689128Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
2026-10-22T02:54:48.3981615Z # branch: the PPA answered; ghostty must be installed
2026-10-22T02:54:50.7798103Z ok 8 [ubuntu-client] ghostty
2026-10-22T02:54:51.3532196Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
2026-10-22T02:54:51.9242491Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
2026-10-22T02:54:52.4845733Z ok 11 [ubuntu-client] an apt-get update that reports a failed PPA index without a non-zero exit is an outage
2026-10-22T02:54:53.0731156Z ok 12 [ubuntu-client] a fetch failure from another host stays fatal even when the PPA also failed
2026-10-22T02:54:53.6241916Z ok 13 [ubuntu-client] an installed ghostty is left as it is
2026-10-22T02:54:54.1587148Z ok 14 [ubuntu-client] the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it
2026-10-22T02:54:54.6891815Z ok 15 [ubuntu-client] a non-PPA apt failure still fails the apply
exit 0
```

## 6. Revise 3 red at 4ecf2f00 (the revise-3 tests on the revise-2 installer)

```text
$ gh run view 39721076552 --repo mryfmo/dotfiles --json headSha,conclusion
{"conclusion":"failure","headSha":"4ecf2f00e915cabe133aca396c6b144c5e3aa414"}
exit 0
$ XDG_CACHE_HOME="$TMPDIR/ghcache" gh run view --repo mryfmo/dotfiles --job 119634392423 --log | cut -f3- | grep -E 'ok [0-9]+ \[ubuntu-client\] (PACKAGES for ghostty|DEPENDENCY_PACKAGES for ghostty|ghostty$|an unreachable PPA|a failed PPA|a non-PPA|an apt-get update|a fetch failure|an installed ghostty|a non-fetch|a half-configured|the ghostty step)|# branch|ghostty\.bats, line|#   `'
2026-10-22T04:19:20.0905934Z ok 6 [ubuntu-client] PACKAGES for ghostty
2026-10-22T04:19:20.3266542Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
2026-10-22T04:19:36.9980675Z # branch: the PPA answered; ghostty must be installed
2026-10-22T04:19:38.6044178Z ok 8 [ubuntu-client] ghostty
2026-10-22T04:19:38.9849750Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
2026-10-22T04:19:39.3672002Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
2026-10-22T04:19:39.7436136Z ok 11 [ubuntu-client] an apt-get update that reports a failed PPA index without a non-zero exit is an outage
2026-10-22T04:19:40.1503608Z ok 12 [ubuntu-client] a fetch failure from another host stays fatal even when the PPA also failed
2026-10-22T04:19:40.5473095Z ok 13 [ubuntu-client] an installed ghostty is left as it is
2026-10-22T04:19:40.9518238Z not ok 14 [ubuntu-client] a non-fetch apt error after a PPA warning stays fatal
2026-10-22T04:19:40.9530296Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 141)
2026-10-22T04:19:40.9565353Z #   `[ "${status}" -eq 100 ]' failed
2026-10-22T04:19:41.3524977Z not ok 15 [ubuntu-client] a half-configured ghostty is installed, not skipped
2026-10-22T04:19:41.3539963Z # (in test file tests/install/ubuntu/client/ghostty.bats, line 150)
2026-10-22T04:19:41.3573562Z #   `grep -q 'installed ghostty' "${BATS_TEST_TMPDIR}/calls.log"' failed with status 2
2026-10-22T04:19:41.7585717Z ok 16 [ubuntu-client] the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it
2026-10-22T04:19:42.1245588Z ok 17 [ubuntu-client] a non-PPA apt failure still fails the apply
exit 0
```

## 7. Revise 3 green at 9d268181

```text
$ gh run view 39722151453 --repo mryfmo/dotfiles --json headSha,conclusion
{"conclusion":"success","headSha":"9d26818177aa61b5be2cda360070c697b047a8fd"}
exit 0
$ XDG_CACHE_HOME="$TMPDIR/ghcache" gh run view --repo mryfmo/dotfiles --job 119637834329 --log | cut -f3- | grep -E 'ok [0-9]+ \[ubuntu-client\] (PACKAGES for ghostty|DEPENDENCY_PACKAGES for ghostty|ghostty$|an unreachable PPA|a failed PPA|a non-PPA|an apt-get update|a fetch failure|an installed ghostty|a non-fetch|a half-configured|the ghostty step)|# branch|ghostty\.bats, line|#   `'
2026-10-22T04:31:23.4187754Z ok 6 [ubuntu-client] PACKAGES for ghostty
2026-10-22T04:31:23.7074036Z ok 7 [ubuntu-client] DEPENDENCY_PACKAGES for ghostty
2026-10-22T04:31:40.9347813Z # branch: the PPA answered; ghostty must be installed
2026-10-22T04:31:42.8642544Z ok 8 [ubuntu-client] ghostty
2026-10-22T04:31:43.3082877Z ok 9 [ubuntu-client] an unreachable PPA never fails the apply
2026-10-22T04:31:43.7487590Z ok 10 [ubuntu-client] a failed PPA package download never fails the apply
2026-10-22T04:31:44.1984553Z ok 11 [ubuntu-client] an apt-get update that reports a failed PPA index without a non-zero exit is an outage
2026-10-22T04:31:44.6597701Z ok 12 [ubuntu-client] a fetch failure from another host stays fatal even when the PPA also failed
2026-10-22T04:31:45.1116642Z ok 13 [ubuntu-client] an installed ghostty is left as it is
2026-10-22T04:31:45.5552972Z ok 14 [ubuntu-client] a non-fetch apt error after a PPA warning stays fatal
2026-10-22T04:31:46.0010532Z ok 15 [ubuntu-client] a half-configured ghostty is installed, not skipped
2026-10-22T04:31:46.4438377Z ok 16 [ubuntu-client] the ghostty step is a guarded run_after_ script and the misc run_once_ script no longer includes it
2026-10-22T04:31:46.8815555Z ok 17 [ubuntu-client] a non-PPA apt failure still fails the apply
exit 0
```

## 8. At 9d268181: bash -n, shellcheck, shfmt, the comparison lint, the caps from the merge-base

```text
$ git rev-parse HEAD
9d26818177aa61b5be2cda360070c697b047a8fd
exit 0
$ bash -n install/ubuntu/client/ghostty.sh
exit 0
$ shellcheck install/ubuntu/client/ghostty.sh
exit 0
$ shfmt -i 4 -sr -d install/ubuntu/client/ghostty.sh
exit 0
$ "$HOME/.local/share/mise/installs/python/3.15.0/bin/python3" -I scripts/lint-comparisons.py --changed install/ubuntu/client/ghostty.sh home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl
exit 0
$ git merge-base origin/main HEAD
d06d94fd8eedcd0770c1c80c2b1596ec36109ef8
exit 0
$ git diff --numstat $(git merge-base origin/main HEAD) HEAD
4	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/autoskill.md
7	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/learning.md
89	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/report.md
2	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/result.txt
7	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/revise.yaml
9	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/sandbox.md
23	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/smoke.sh
71	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/task.md
171	0	.orchestration/dotfiles-T133-install-ppa-resilience-a01/validation.md
13	0	home/.chezmoiscripts/ubuntu/run_after_06-client-install-ghostty.sh.tmpl
0	3	home/.chezmoiscripts/ubuntu/run_once_50-client-install-misc.sh.tmpl
45	4	install/ubuntu/client/ghostty.sh
129	2	tests/install/ubuntu/client/ghostty.bats
exit 0
$ git diff --numstat $(git merge-base origin/main HEAD) HEAD | awk -F'\t' '$3 !~ /^(tests|\.orchestration)\// {o+=$1+$2} $3 ~ /^tests\// {t+=$1+$2} END {print "changed_non_tests=" o " changed_tests=" t}'
changed_non_tests=65 changed_tests=131
exit 0
```

## 9. smoke.sh (the fakes in plain bash, not Bats) against the installers of 9d268181, 930a76a0 and 44134e36

```text
$ bash .orchestration/dotfiles-T133-install-ppa-resilience-a01/smoke.sh ./install/ubuntu/client/ghostty.sh
update exit=0 install-attempted=0 installed=0 retry-line=1
pool exit=0 install-attempted=1 installed=0 retry-line=1
archive exit=100 install-attempted=0 installed=0 retry-line=0
none exit=0 install-attempted=1 installed=1 retry-line=0
warn exit=0 install-attempted=0 installed=0 retry-line=1
mixed exit=100 install-attempted=0 installed=0 retry-line=0
otherppa exit=100 install-attempted=0 installed=0 retry-line=0
hook exit=100 install-attempted=0 installed=0 retry-line=0
status=installed exit=0 install-attempted=0 installed=0 retry-line=0
status=half-configured exit=0 install-attempted=1 installed=1 retry-line=0
exit 0
$ git show 930a76a0:install/ubuntu/client/ghostty.sh > "$TMPDIR/g930.sh" && bash .orchestration/dotfiles-T133-install-ppa-resilience-a01/smoke.sh "$TMPDIR/g930.sh"
update exit=0 install-attempted=0 installed=0 retry-line=1
pool exit=0 install-attempted=1 installed=0 retry-line=1
archive exit=100 install-attempted=0 installed=0 retry-line=0
none exit=0 install-attempted=1 installed=1 retry-line=0
warn exit=0 install-attempted=0 installed=0 retry-line=1
mixed exit=100 install-attempted=0 installed=0 retry-line=0
otherppa exit=100 install-attempted=0 installed=0 retry-line=0
hook exit=0 install-attempted=0 installed=0 retry-line=1
status=installed exit=0 install-attempted=0 installed=0 retry-line=0
status=half-configured exit=0 install-attempted=0 installed=0 retry-line=0
exit 0
$ git show 44134e36:install/ubuntu/client/ghostty.sh > "$TMPDIR/g441.sh" && bash .orchestration/dotfiles-T133-install-ppa-resilience-a01/smoke.sh "$TMPDIR/g441.sh"
update exit=0 install-attempted=0 installed=0 retry-line=1
pool exit=0 install-attempted=1 installed=0 retry-line=1
archive exit=100 install-attempted=0 installed=0 retry-line=0
none exit=0 install-attempted=1 installed=1 retry-line=0
warn exit=1 install-attempted=1 installed=0 retry-line=0
mixed exit=0 install-attempted=0 installed=0 retry-line=1
otherppa exit=0 install-attempted=0 installed=0 retry-line=1
hook exit=0 install-attempted=0 installed=0 retry-line=1
status=installed exit=0 install-attempted=1 installed=1 retry-line=0
status=half-configured exit=0 install-attempted=1 installed=1 retry-line=0
exit 0
```
