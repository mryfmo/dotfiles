# T30 validation — dot-codex-apparmor-userns-T30-a01

All blocks are verbatim command output (test runners may leave ANSI codes).

## task_rev verification
```
$ git show c326c73:.orchestration/tasks/dot-codex-apparmor-userns-T30-a01.md | sha256sum
469797747c33379e7d296ac9f0e9810ffcc9b6254ebf852b76c4699cc601c682  -
$ git merge-base --is-ancestor c326c73 HEAD && echo base-contains-task-commit
base-contains-task-commit
```

## 1. Investigation (read-only)
```
$ lsb_release -ds; uname -r
Ubuntu 24.04.5 LTS
7.0.0-1019-nvidia
$ sysctl kernel.apparmor_restrict_unprivileged_userns kernel.unprivileged_userns_clone user.max_user_namespaces
kernel.apparmor_restrict_unprivileged_userns = 1
kernel.unprivileged_userns_clone = 1
user.max_user_namespaces = 512927
$ cat /sys/module/apparmor/parameters/enabled
Y
$ aa-status (non-root)
You do not have enough privilege to read the profile set.
apparmor module is loaded.
$ grep -iE "bwrap|unpriv|codex" /sys/kernel/security/apparmor/profiles
ugrep: warning: cannot read /sys/kernel/security/apparmor/profiles: Permission denied
$ ls /etc/apparmor.d | grep -iE "bwrap|userns|unpriv|codex"
lxc-usernsexec
unprivileged_userns
$ command -v bwrap; bwrap --version
/usr/bin/bwrap
bubblewrap 0.9.0
$ bwrap --ro-bind / / true
bwrap: setting up uid map: Permission denied
exit=1
```
Codex binary resolution (mise noise lines about unrelated projects elided):
```
$ command -v codex; mise which codex
/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/bin/codex
/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/bin/codex
$ readlink -f "$(mise which codex)"
/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/lib/node_modules/@openai/codex/bin/codex.js
$ find <codex npm pkg> -type f \( -name '*bwrap*' -o -name 'codex*' -o -name '*sandbox*' \) -perm -u+x
/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/lib/node_modules/@openai/codex/bin/codex.js
/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-arm64/vendor/aarch64-unknown-linux-musl/codex-resources/bwrap
/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-arm64/vendor/aarch64-unknown-linux-musl/bin/codex-code-mode-host
/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-arm64/vendor/aarch64-unknown-linux-musl/bin/codex
```
Which bwrap codex executes: a PATH-first logging shim was never invoked:
```
$ PATH=<shim>:$PATH codex sandbox true
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
exit=0
$ cat shim.log
$ command -v strace
/usr/bin/strace
```
strace execve trace of `codex sandbox true` (non-ENOENT execs; env and args truncated):
```
$ strace -f -qq -e trace=execve -e signal=none -o strace.txt codex sandbox true
1475623 execve("/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/bin/codex", ["codex", "sandbox", "true"], 0xffffc97c78a0 /* 71 vars */) = 0
1475623 execve("/home/moriya/.local/share/mise/installs/node/26.9.0/bin/node", ["node", "/home/moriya/.local/share/mise/i"..., "sandbox", "true"], 0xffffc4168fe8 /* 71 vars */) = 0
1475630 execve("/home/moriya/.local/share/mise/installs/npm-openai-codex/0.157.1/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-arm64/vendor/aarch64-unknown-linux-musl/bin/codex", ["/home/moriya/.local/share/mise/i"..., "sandbox", "true"], 0x4
1475675 execve("/home/moriya/.codex/tmp/arg0/codex-arg0Dsp6Cy/codex-linux-sandbox", ["codex-linux-sandbox", "--sandbox-policy-cwd", "/home/moriya/Workspace/dotfiles/"..., "--command-cwd", "/home/moriya/Workspace/dotfiles/"..., "--permission-profile", "{\"type\
1475677 execve("/usr/bin/bwrap", ["/usr/bin/bwrap", "--help"], 0xffffd93a6a18 /* 7 vars */) = 0
1475676 execve("/usr/bin/bwrap", ["bwrap", "--as-pid-1", "--new-session", "--die-with-parent", "--tmpfs", "/", "--dev", "/dev", "--ro-bind", "/bin", "/bin", "--ro-bind", "/etc", "/etc", "--ro-bind", "/lib", "/lib", "--ro-bind", "/sbin", "/sbin", "--ro-bind", "
1475679 execve("/usr/bin/bwrap", ["/usr/bin/bwrap", "--help"], 0xffffd93a6a18 /* 7 vars */) = 0
1475675 execve("/usr/bin/bwrap", ["bwrap", "--as-pid-1", "--new-session", "--die-with-parent", "--ro-bind", "/", "/", "--dev", "/dev", "--perms", "000", "--tmpfs", "/tmp/codex-daemon-1000", "--remount-ro", "/tmp/codex-daemon-1000", "--unshare-user", "--unshare
```
Conclusion: codex-linux-sandbox execs `/usr/bin/bwrap` by absolute path, so the narrowest working level is (b), a profile on `/usr/bin/bwrap`. Level (a), codex-shipped `codex-resources/bwrap`, is never executed while `/usr/bin/bwrap` exists. The orchestrator approved (b) and option A in PING 2026-09-27T04:53:46Z.

## Profile parse check (non-root, no kernel load) with negative control
```
$ apparmor_parser -Q -K -I /etc/apparmor.d install/ubuntu/common/apparmor/bwrap-userns
exit=0
$ apparmor_parser -Q -K broken-profile   # negative control: missing trailing comma
AppArmor parser error for /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/broken-profile in profile /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/broken-profile at line 3: Lexer found unexpected character: '}' (0x7d) in state: USERNS_MODE
exit=1
```

## Rendered chezmoi wrapper tail and profile hash
```
$ chezmoi execute-template --source "$PWD/home" < home/.chezmoiscripts/ubuntu/run_onchange_after_07-apparmor-bwrap-userns.sh.tmpl | tail -5
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi

# Re-run when the profile changes. bwrap-userns sha256sum: 40fa331c27d032df5ea7c0abc130c80cc2b44af139d55b8883f89c4cf9148c3a
$ sha256sum install/ubuntu/common/apparmor/bwrap-userns
40fa331c27d032df5ea7c0abc130c80cc2b44af139d55b8883f89c4cf9148c3a  install/ubuntu/common/apparmor/bwrap-userns
```

## Doctor check on this host (profile not yet deployed)
```
$ bash -c 'source scripts/check-tools.sh; check_apparmor_userns; echo "req=$required_failures opt=$optional_warnings"'
required failed: bwrap user-namespace probe; AppArmor profile /etc/apparmor.d/bwrap-userns is missing, so sandboxed codex runs fail (chezmoi apply installs it)
req=1 opt=0
```

## AGENTS.md operator text is verbatim
```
$ diff <task-file operator block> <AGENTS.md from "## Code Review Rules" to EOF>
exit=0
```

## Mutation baseline (new tests vs origin/main export), then branch
```
$ (origin/main export + new test file) python3 -m unittest -v tests.unit.test_apparmor_userns
test_doctor_fails_when_the_bwrap_probe_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) ... 
  test_doctor_fails_when_the_bwrap_probe_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) [profile missing] ... [31mFAIL[0m
  test_doctor_fails_when_the_bwrap_probe_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) [profile not loaded] ... [31mERROR[0m
test_doctor_is_not_applicable_without_the_restriction (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_is_not_applicable_without_the_restriction) ... [31mFAIL[0m
test_doctor_passes_when_the_bwrap_probe_succeeds (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_passes_when_the_bwrap_probe_succeeds) ... [31mFAIL[0m
test_doctor_warns_optionally_when_codex_is_missing (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_warns_optionally_when_codex_is_missing) ... [31mFAIL[0m
test_installer_copies_and_reloads_the_profile_with_sudo (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) ... 
  test_installer_copies_and_reloads_the_profile_with_sudo (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) [repo checkout] ... [31mFAIL[0m
  test_installer_copies_and_reloads_the_profile_with_sudo (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) [chezmoi source dir] ... [31mFAIL[0m
test_installer_fails_when_loading_the_profile_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_fails_when_loading_the_profile_fails) ... [31mFAIL[0m
test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) ... 
  test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) [restriction off] ... [31mFAIL[0m
  test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) [no parser] ... [31mFAIL[0m
  test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) [no bwrap] ... [31mFAIL[0m

======================================================================
[31mERROR[0m[1;31m: test_doctor_fails_when_the_bwrap_probe_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) [profile not loaded][0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m166[0m, in [35mtest_doctor_fails_when_the_bwrap_probe_fails[0m
    self.profile_target.write_text([31mPROFILE.read_text[0m[1;31m()[0m)
                                   [31m~~~~~~~~~~~~~~~~~[0m[1;31m^^[0m
  File [35m"/home/moriya/.local/share/mise/installs/python/3.14.7/lib/python3.14/pathlib/__init__.py"[0m, line [35m787[0m, in [35mread_text[0m
    with [31mself.open[0m[1;31m(mode='r', encoding=encoding, errors=errors, newline=newline)[0m as f:
         [31m~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
  File [35m"/home/moriya/.local/share/mise/installs/python/3.14.7/lib/python3.14/pathlib/__init__.py"[0m, line [35m771[0m, in [35mopen[0m
    return [31mio.open[0m[1;31m(self, mode, buffering, encoding, errors, newline)[0m
           [31m~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mFileNotFoundError[0m: [35m[Errno 2] No such file or directory: '/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/install/ubuntu/common/apparmor/bwrap-userns'[0m

======================================================================
[31mFAIL[0m[1;31m: test_doctor_fails_when_the_bwrap_probe_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) [profile missing][0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m169[0m, in [35mtest_doctor_fails_when_the_bwrap_probe_fails[0m
    [31mself.assertIn[0m[1;31m(message, result.stderr)[0m
    [31m~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m'is missing, so sandboxed codex runs fail' not found in '_: line 1: check_apparmor_userns: command not found\n'[0m

======================================================================
[31mFAIL[0m[1;31m: test_doctor_is_not_applicable_without_the_restriction (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_is_not_applicable_without_the_restriction)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m138[0m, in [35mtest_doctor_is_not_applicable_without_the_restriction[0m
    [31mself.assertIn[0m[1;31m("not applicable: AppArmor userns restriction", result.stdout)[0m
    [31m~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m'not applicable: AppArmor userns restriction' not found in ''[0m

======================================================================
[31mFAIL[0m[1;31m: test_doctor_passes_when_the_bwrap_probe_succeeds (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_passes_when_the_bwrap_probe_succeeds)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m152[0m, in [35mtest_doctor_passes_when_the_bwrap_probe_succeeds[0m
    [31mself.assertIn[0m[1;31m("found:   bwrap user namespaces allowed", result.stdout)[0m
    [31m~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m'found:   bwrap user namespaces allowed' not found in ''[0m

======================================================================
[31mFAIL[0m[1;31m: test_doctor_warns_optionally_when_codex_is_missing (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_warns_optionally_when_codex_is_missing)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m145[0m, in [35mtest_doctor_warns_optionally_when_codex_is_missing[0m
    [31mself.assertIn[0m[1;31m("codex is not installed", result.stderr)[0m
    [31m~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m'codex is not installed' not found in '_: line 1: check_apparmor_userns: command not found\n'[0m

======================================================================
[31mFAIL[0m[1;31m: test_installer_copies_and_reloads_the_profile_with_sudo (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) [repo checkout][0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m113[0m, in [35mtest_installer_copies_and_reloads_the_profile_with_sudo[0m
    [31mself.assertEqual[0m[1;31m(0, result.returncode, result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m0 != 127 : bash: /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/install/ubuntu/common/apparmor_userns.sh: No such file or directory
[0m

======================================================================
[31mFAIL[0m[1;31m: test_installer_copies_and_reloads_the_profile_with_sudo (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) [chezmoi source dir][0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m113[0m, in [35mtest_installer_copies_and_reloads_the_profile_with_sudo[0m
    [31mself.assertEqual[0m[1;31m(0, result.returncode, result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m0 != 127 : bash: /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/install/ubuntu/common/apparmor_userns.sh: No such file or directory
[0m

======================================================================
[31mFAIL[0m[1;31m: test_installer_fails_when_loading_the_profile_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_fails_when_loading_the_profile_fails)[0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m129[0m, in [35mtest_installer_fails_when_loading_the_profile_fails[0m
    [31mself.assertEqual[0m[1;31m([0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^[0m
        [1;31m[f"sudo install -m 0644 {PROFILE} {self.profile_target}"], self.calls()[0m
        [1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
    [1;31m)[0m
    [1;31m^[0m
[1;35mAssertionError[0m: [35mLists differ: ['sudo install -m 0644 /tmp/claude-1000/-h[195 chars]rns'] != []

First list contains 1 additional elements.
First extra element 0:
'sudo install -m 0644 /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/install/ubuntu/common/apparmor/bwrap-userns /tmp/apparmor-userns-test-1_c7q52p/etc/apparmor.d/bwrap-userns'

+ []
- ['sudo install -m 0644 '
-  '/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/install/ubuntu/common/apparmor/bwrap-userns '
-  '/tmp/apparmor-userns-test-1_c7q52p/etc/apparmor.d/bwrap-userns'][0m

======================================================================
[31mFAIL[0m[1;31m: test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) [restriction off][0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m93[0m, in [35mtest_installer_is_a_no_op_when_the_host_does_not_need_the_profile[0m
    [31mself.assertEqual[0m[1;31m(0, result.returncode, result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m0 != 127 : bash: /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/install/ubuntu/common/apparmor_userns.sh: No such file or directory
[0m

======================================================================
[31mFAIL[0m[1;31m: test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) [no parser][0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m93[0m, in [35mtest_installer_is_a_no_op_when_the_host_does_not_need_the_profile[0m
    [31mself.assertEqual[0m[1;31m(0, result.returncode, result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m0 != 127 : bash: /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/install/ubuntu/common/apparmor_userns.sh: No such file or directory
[0m

======================================================================
[31mFAIL[0m[1;31m: test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) [no bwrap][0m
----------------------------------------------------------------------
Traceback (most recent call last):
  File [35m"/tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/tests/unit/test_apparmor_userns.py"[0m, line [35m93[0m, in [35mtest_installer_is_a_no_op_when_the_host_does_not_need_the_profile[0m
    [31mself.assertEqual[0m[1;31m(0, result.returncode, result.stderr)[0m
    [31m~~~~~~~~~~~~~~~~[0m[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[0m
[1;35mAssertionError[0m: [35m0 != 127 : bash: /tmp/claude-1000/-home-moriya-Workspace-dotfiles/3e54f9a0-f011-4421-9a8a-a9eb113df7ad/scratchpad/t30/base.pMhV/install/ubuntu/common/apparmor_userns.sh: No such file or directory
[0m

----------------------------------------------------------------------
Ran 7 tests in 0.025s

[1;31mFAILED[0m ([1;31mfailures=10[0m, [1;31merrors=1[0m)
$ (branch) python3 -m unittest -v tests.unit.test_apparmor_userns
test_doctor_fails_when_the_bwrap_probe_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_fails_when_the_bwrap_probe_fails) ... [32mok[0m
test_doctor_is_not_applicable_without_the_restriction (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_is_not_applicable_without_the_restriction) ... [32mok[0m
test_doctor_passes_when_the_bwrap_probe_succeeds (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_passes_when_the_bwrap_probe_succeeds) ... [32mok[0m
test_doctor_warns_optionally_when_codex_is_missing (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_doctor_warns_optionally_when_codex_is_missing) ... [32mok[0m
test_installer_copies_and_reloads_the_profile_with_sudo (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_copies_and_reloads_the_profile_with_sudo) ... [32mok[0m
test_installer_fails_when_loading_the_profile_fails (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_fails_when_loading_the_profile_fails) ... [32mok[0m
test_installer_is_a_no_op_when_the_host_does_not_need_the_profile (tests.unit.test_apparmor_userns.AppArmorUsernsTest.test_installer_is_a_no_op_when_the_host_does_not_need_the_profile) ... [32mok[0m

----------------------------------------------------------------------
Ran 7 tests in 0.039s

[32mOK[0m
```

## Required validation commands
```
$ make validate-agent-assets
uv run --with pyyaml scripts/validate-agent-assets.py
agent asset validation ok
exit=0
```
First full `make unit-test` run hit an unrelated flaky permgate bench test:
```
FAIL: test_bench_runs_five_layer_two_fixtures (test_permgate.PermgateTest.test_bench_runs_five_layer_two_fixtures)
AssertionError: 0 != 5
Ran 469 tests in 43.469s
FAILED (failures=1, skipped=1)
exit=2
```
```
$ for i in 1 2 3; do uv run python -m unittest tests.unit.test_permgate.PermgateTest.test_bench_runs_five_layer_two_fixtures 2>&1 | tail -1; done
OK
OK
OK
```
Full rerun:
```
$ make unit-test
uv run python -m unittest discover -s tests/unit -v
test_asset_repair_invokes_only_the_detected_step (test_check_agent_runtime.CheckAgentRuntimeTest.test_asset_repair_invokes_only_the_detected_step) ... <frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08040>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813d5bd30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08130>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813d5bf10>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08220>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c084f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08400>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c085e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c086d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c087c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c088b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c089a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08a90>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44814048310>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08c70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08e50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08f40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08d60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09030>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09120>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09210>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09300>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c093f0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c094e0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c095d0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c096c0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c097b0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c098a0>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c08b80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09a80>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09b70>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09990>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09c60>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09e40>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09d50>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c09f30>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
<frozen importlib._bootstrap>:488: ResourceWarning: unclosed database in <sqlite3.Connection object at 0xf44813c0a110>
ResourceWarning: Enable tracemalloc to get the object allocation traceback
ok
test_current_session_start_order_is_preserved (test_claude_settings_merge.ClaudeSettingsMergeTest.test_current_session_start_order_is_preserved)
test_managed_session_start_replacement_keeps_hook_order (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replacement_keeps_hook_order)
test_managed_session_start_replaces_stale_hard_coded_home_hook (test_claude_settings_merge.ClaudeSettingsMergeTest.test_managed_session_start_replaces_stale_hard_coded_home_hook)
test_model_profiles_reject_incomplete_or_unsafe_entries (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_incomplete_or_unsafe_entries) ... ERROR: model profile standard is missing codex
ERROR: model profile standard.claude.model must be a launcher-safe string
ERROR: model_profiles must define the express profile
ok
test_model_profiles_reject_unsafe_advisor (test_generate_agent_configs.GenerateAgentConfigsTest.test_model_profiles_reject_unsafe_advisor) ... ERROR: model profile standard.claude.advisor must be a launcher-safe string
ok
test_unknown_interactive_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_interactive_profile_fails) ... ERROR: interactive_profile must name a model profile: 'missing'
ok
test_unknown_worker_kind_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_kind_fails) ... ERROR: worker_kind must be one of ('codex', 'claude'): 'banana'
ok
test_unknown_worker_profile_fails (test_generate_agent_configs.GenerateAgentConfigsTest.test_unknown_worker_profile_fails) ... ERROR: worker_profile must name a model profile: 'missing'
ok
test_cli_workspace_resolves_macos_var_alias_identically (test_permgate.PermgateTest.test_cli_workspace_resolves_macos_var_alias_identically) ... skipped 'macOS /var alias only'
test_upgrade_uses_current_mise_node_after_runtime_replacement (test_runtime_health.RuntimeHealthTest.test_upgrade_uses_current_mise_node_after_runtime_replacement)
test_repo_claude_settings_reject_machine_specific_interpreter (test_validate_agent_assets.ValidateAgentAssetsTest.test_repo_claude_settings_reject_machine_specific_interpreter) ... ERROR: /tmp/validate-agent-assets-test-naoc_r8u/.claude/settings.json hook SessionEnd must not hard-code a machine-specific home path: /Users/mryfmo/.local/share/mise/installs/python/3.14.7/bin/python3.14
ok

----------------------------------------------------------------------
Ran 469 tests in 42.192s

OK (skipped=1)
exit=0
```
(Per-test `... ok` lines are elided. The remaining `ERROR:` lines are expected stderr from passing negative tests.)
```
$ git -C /home/moriya/Workspace/dotfiles/.claude/worktrees/worker-c diff origin/main --stat
 .../tasks/dot-mosh-and-asset-bumps-T31-a01.md      | 157 -------------------
 AGENTS.md                                          |   8 +
 README.md                                          |  10 ++
 ...onchange_after_07-apparmor-bwrap-userns.sh.tmpl |   6 +
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   4 +-
 home/dot_mise/config.toml                          |   2 +-
 home/dot_mise/mise.lock                            |  26 +--
 install/ubuntu/common/apparmor/bwrap-userns        |  17 ++
 install/ubuntu/common/apparmor_userns.sh           |  78 +++++++++
 scripts/check-tools.sh                             |  38 +++++
 tests/unit/test_apparmor_userns.py                 | 174 +++++++++++++++++++++
 tests/unit/test_runtime_health.py                  |   2 +
 12 files changed, 349 insertions(+), 173 deletions(-)
$ git diff origin/main...HEAD --stat
 AGENTS.md                                          |   8 +
 README.md                                          |  10 ++
 ...onchange_after_07-apparmor-bwrap-userns.sh.tmpl |   6 +
 .../dot_agents/skills/agmsg-orchestration/SKILL.md |   4 +-
 install/ubuntu/common/apparmor/bwrap-userns        |  17 ++
 install/ubuntu/common/apparmor_userns.sh           |  78 +++++++++
 scripts/check-tools.sh                             |  38 +++++
 tests/unit/test_apparmor_userns.py                 | 174 +++++++++++++++++++++
 tests/unit/test_runtime_health.py                  |   2 +
 9 files changed, 335 insertions(+), 2 deletions(-)
$ git log --oneline -1
74b517b feat(ubuntu): ship bwrap AppArmor userns profile for sandboxed codex
$ gh pr view 192 --json number,url,headRefOid
[1;37m{[m
  [1;34m"headRefOid"[m[1;37m:[m [32m"74b517b4331a7283b165610ceb89895dff14845c"[m[1;37m,[m
  [1;34m"number"[m[1;37m:[m 192[1;37m,[m
  [1;34m"url"[m[1;37m:[m [32m"https://github.com/mryfmo/dotfiles/pull/192"[m
[1;37m}[m
$ gh pr checks 192
CodeRabbit	pass	0		Review skipped: manual review required for this OSS repository
build (client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36295830779/job/108554375171	
build (server)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/36295830779/job/108554375276	
changes	pass	7s	https://github.com/mryfmo/dotfiles/actions/runs/36295830808/job/108554375260	
private-bootstrap (macos-14, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36295830783/job/108554375285	
private-bootstrap (ubuntu-latest, client)	pass	6s	https://github.com/mryfmo/dotfiles/actions/runs/36295830783/job/108554375293	
private-bootstrap (ubuntu-latest, server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/36295830783/job/108554375289	
public-bootstrap (macos-14, client)	pass	7m39s	https://github.com/mryfmo/dotfiles/actions/runs/36295830783/job/108554375277	
test (ubuntu-latest, client)	pass	4m55s	https://github.com/mryfmo/dotfiles/actions/runs/36295830808/job/108554393772	
nix	skipping	0	https://github.com/mryfmo/dotfiles/actions/runs/36295830808/job/108554394299	
public-bootstrap (ubuntu-latest, client)	pass	8m43s	https://github.com/mryfmo/dotfiles/actions/runs/36295830783/job/108554375178	
public-bootstrap (ubuntu-latest, server)	pass	7m1s	https://github.com/mryfmo/dotfiles/actions/runs/36295830783/job/108554375313	
test (macos-14, client)	pass	1m55s	https://github.com/mryfmo/dotfiles/actions/runs/36295830808/job/108554393796	
test (ubuntu-latest, server)	pass	2m13s	https://github.com/mryfmo/dotfiles/actions/runs/36295830808/job/108554393782	
validate	pass	10s	https://github.com/mryfmo/dotfiles/actions/runs/36295830776/job/108554375120	
exit=0
```

## Install step in CI bootstrap (restriction on, bwrap absent → skip)
```
$ gh run view --job 108554375178 --log | grep 'Skipping bwrap AppArmor userns profile:'
$ gh run view --job 108554375313 --log | grep 'Skipping bwrap AppArmor userns profile:'
```

## CompactionDB
```
$ python3 .claude/hooks/contextdb_cli.py memory add --kind decision --scope project --content "T30: dotfiles ships an AppArmor userns profile restoring sandboxed codex under apparmor_restrict_unprivileged_userns=1 (narrowest executable-scoped grant, managed install step + doctor probe); global sysctl relaxation rejected; OpenSandbox rejected for this fleet (CLIs cannot delegate built-in sandboxes; containerization incompatible with the herdr/worktree/agmsg regime) and its vocabulary removed from the orchestration skill (operator 2026-09-27)"
891736ee-64fb-41ff-b9be-37616b2ffd8e
```
