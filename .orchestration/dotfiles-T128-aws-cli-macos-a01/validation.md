---
task_id: dotfiles-T128-aws-cli-macos-a01
seat: claude-standard-dot-a002
code_commit: fe392450
---

# Validation: dotfiles-T128-aws-cli-macos-a01

Every command ran from the worktree `.claude/worktrees/worker-f`, inside the sandbox. `MAIN` names the main checkout, and `S` a scratch directory under `/tmp/claude-501` that holds the mutation runner and, for §5 only, a scratch worktree of `origin/main`. `UV_OFFLINE=1` was set, since uv cannot reach pypi from the sandbox. The output is verbatim, with the main checkout's path removed, and each block ends with the exit status of its command line's last command. §1 to §8 were captured at `fe392450`, before the PR was marked ready. §9 ran outside the sandbox after the Bot's answer on `c2638b32`, and `scratchpad/` there names the session scratchpad.

Premises 1 and 2 need the network: the orchestrator replayed them outside the sandbox, and their output is in the task file's front matter. §2 replays premises 3 and 4.

## 1. Task file and task copy

```console
$ shasum -a 256 "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md"; cmp "$MAIN/.orchestration/tasks/$T.md" ".orchestration/$T/task.md" && echo byte-identical
b51b8bfba2d259b710917f5ea0cb333b83768c129da66c38bc3cdddbfd48a585  .orchestration/tasks/dotfiles-T128-aws-cli-macos-a01.md
b51b8bfba2d259b710917f5ea0cb333b83768c129da66c38bc3cdddbfd48a585  .orchestration/dotfiles-T128-aws-cli-macos-a01/task.md
byte-identical
[exit 0]
```
```console
$ uv run --no-project --with pyyaml python -I scripts/orchestrator/task-consistency-check.py --root "$PWD" "$MAIN/.orchestration/tasks/$T.md"
dotfiles-T128-aws-cli-macos-a01.md: OK
[exit 0]
```

## 2. Branch and the replayable premises (3 and 4; 1 and 2 need the network, the orchestrator's paste)

```console
$ git log --oneline origin/main..HEAD; git rev-parse origin/main
fe392450 feat(macos): install the AWS CLI from AWS's signed install.sh under the XDG roots instead of Homebrew (T128 aws-cli-macos a01)
5c3f8dd09eed15445f1c5f04d53f185c20f71ea2
[exit 0]
```
```console
$ git show origin/main:install/macos/common/dependencies.sh | /usr/bin/grep -nE "^\s+(awscli|gpg)$"
17:    awscli
21:    gpg
[exit 0]
```
```console
$ git show origin/main:tests/unit/test_aws_cli_acquisition.py | /usr/bin/grep -c "def test_"
16
[exit 0]
```

## 3. The change

```console
$ git diff origin/main...HEAD -- install/ubuntu/common/aws_cli.sh install/macos/common/dependencies.sh home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl
diff --git a/home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl b/home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl
new file mode 100644
index 00000000..4071b612
--- /dev/null
+++ b/home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl
@@ -0,0 +1,3 @@
+{{ if eq .chezmoi.os "darwin" -}}
+{{   include "../install/ubuntu/common/aws_cli.sh" }}
+{{- end }}
diff --git a/install/macos/common/dependencies.sh b/install/macos/common/dependencies.sh
index 267346ad..b77d6da6 100644
--- a/install/macos/common/dependencies.sh
+++ b/install/macos/common/dependencies.sh
@@ -14,7 +14,6 @@ if [ "${DOTFILES_DEBUG:-}" ]; then
 fi
 
 readonly BREW_PACKAGES=(
-    awscli
     cmake
     git
     gawk
diff --git a/install/ubuntu/common/aws_cli.sh b/install/ubuntu/common/aws_cli.sh
index 2edabe8f..942e3f9e 100644
--- a/install/ubuntu/common/aws_cli.sh
+++ b/install/ubuntu/common/aws_cli.sh
@@ -1,7 +1,10 @@
 #!/usr/bin/env bash
 
 # @file install/ubuntu/common/aws_cli.sh
-# @brief Install the current AWS CLI from its official Linux archive, verified with AWS's GPG signature.
+# @brief Install the current AWS CLI from AWS's official distribution, verified with AWS's GPG signature.
+# @description
+#   On Linux the archive is verified and installed. On macOS AWS's install.sh is verified, then run under the
+#   XDG roots; it downloads the pkg and checks its Apple Developer team id before Apple's installer runs.
 
 set -Eeuo pipefail
 
@@ -18,13 +21,18 @@ readonly AWS_CLI_BIN_DIR="${HOME}/.local/bin"
 readonly AWS_CLI_ETAG_FILE="${XDG_STATE_HOME:-${HOME}/.local/state}/dotfiles/aws-cli-archive.etag"
 
 #
-# @description Print the AWS CLI archive URL for the current supported architecture.
-#   The unversioned archive is AWS's current release; its .sig is checked against the pinned key.
-# @stdout The official x86_64 or aarch64 archive URL.
+# @description Print the URL of AWS's current release: the archive for the current supported architecture
+#   on Linux, whose .sig is checked against the pinned key, and the pkg on macOS, whose ETag main reads.
+# @stdout The official x86_64 or aarch64 archive URL, or the macOS pkg URL.
 #
 function aws_cli_url() {
     local architecture
 
+    # The macOS pkg serves every architecture.
+    if [ "$(uname -s)" = Darwin ]; then
+        printf 'https://awscli.amazonaws.com/AWSCLIV2.pkg\n'
+        return
+    fi
     architecture="$(uname -m)"
     case "${architecture}" in
     x86_64 | aarch64)
@@ -79,6 +87,7 @@ function verify_aws_cli_install() {
 
 #
 # @description Verify and install the current AWS CLI without modifying a working install on verification failure.
+#   On macOS the verified file is install.sh, and version.txt names the release the postcondition expects.
 # @exitcode 3 A download failed, so nothing was installed.
 #
 function install_aws_cli() (
@@ -95,18 +104,30 @@ function install_aws_cli() (
     local temporary_dir
     local staged_version
     local same_version_dir
+    local macos=""
 
-    archive_url="$(aws_cli_url)" || return
+    if [ "$(uname -s)" = Darwin ]; then
+        macos=1
+        archive_url="https://awscli.amazonaws.com/v2/install.sh"
+    else
+        archive_url="$(aws_cli_url)" || return
+    fi
     temporary_dir="$(mktemp -d)" || return
     trap 'rm -rf "${temporary_dir}"' EXIT
 
     archive_path="${temporary_dir}/awscliv2.zip"
+    [ -z "${macos}" ] || archive_path="${temporary_dir}/install.sh"
     signature_path="${archive_path}.sig"
     inspection_home="${temporary_dir}/gnupg-inspection"
     keyring_path="${temporary_dir}/aws-cli-keyring.gpg"
 
     curl --fail --location --silent --show-error "${archive_url}" --output "${archive_path}" || return 3
     curl --fail --location --silent --show-error "${archive_url}.sig" --output "${signature_path}" || return 3
+    if [ -n "${macos}" ]; then
+        # install.sh installs the release version.txt names, so the postcondition expects that one.
+        staged_version="$(curl --fail --location --silent --show-error https://awscli.amazonaws.com/v2/version.txt)" || return 3
+        staged_version="${staged_version//[[:space:]]/}"
+    fi
 
     mkdir -m 700 "${inspection_home}" || return
     key_data="$(gpg --homedir "${inspection_home}" --batch --with-colons --import-options show-only --import "${AWS_CLI_KEY_PATH}")" || return
@@ -122,6 +143,12 @@ function install_aws_cli() (
     gpg --batch --yes --dearmor --output "${keyring_path}" "${AWS_CLI_KEY_PATH}" || return
     gpgv --keyring "${keyring_path}" "${signature_path}" "${archive_path}" || return
 
+    if [ -n "${macos}" ]; then
+        mkdir -p "${AWS_CLI_BIN_DIR}" "$(dirname "${AWS_CLI_INSTALL_DIR}")" || return
+        XDG_DATA_HOME="$(dirname "${AWS_CLI_INSTALL_DIR}")" XDG_BIN_HOME="${AWS_CLI_BIN_DIR}" bash "${archive_path}" || return
+        verify_aws_cli_install "${staged_version}"
+        return
+    fi
     unzip -q "${archive_path}" -d "${temporary_dir}" || return
     staged_version="$(verify_aws_cli_version "${temporary_dir}/aws/dist/aws" "AWS CLI staged artifact verification failed")" || return
     staged_version="${staged_version#aws-cli/}"
[exit 0]
```

## 4. The Check: the test module in the sandbox

```console
$ uv run python -m unittest tests/unit/test_aws_cli_acquisition.py -v 2>&1 | /usr/bin/grep -E "\.\.\. |^Ran|^OK|^FAILED|mkdtemp failed"
test_exit_zero_install_passes_only_when_the_staged_version_is_active (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_passes_only_when_the_staged_version_is_active) ... ok
test_exit_zero_install_without_an_aws_cli_banner_fails_postcondition (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_install_without_an_aws_cli_banner_fails_postcondition) ... ok
test_exit_zero_partial_install_without_binary_fails_postcondition (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_exit_zero_partial_install_without_binary_fails_postcondition) ... ok
test_gpgv_failure_preserves_existing_aws_and_skips_unzip (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip) ... FAIL
test_key_metadata_failures_stop_before_dearmor_and_gpgv (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_key_metadata_failures_stop_before_dearmor_and_gpgv) ... ok
test_linux_urls_are_the_unversioned_current_archive_and_unknown_architecture_fails (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_linux_urls_are_the_unversioned_current_archive_and_unknown_architecture_fails) ... ok
test_macos_download_failure_keeps_a_working_aws_and_runs_no_gpgv (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_macos_download_failure_keeps_a_working_aws_and_runs_no_gpgv) ... ok
test_macos_etag_skip_uses_the_pkg_url (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_macos_etag_skip_uses_the_pkg_url) ... ok
test_macos_signature_failure_preserves_existing_aws_and_runs_no_installer (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_macos_signature_failure_preserves_existing_aws_and_runs_no_installer) ... ok
test_macos_verified_install_runs_install_sh_with_xdg_roots (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_macos_verified_install_runs_install_sh_with_xdg_roots) ... ok
test_main_installs_and_records_a_new_archive_etag (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_main_installs_and_records_a_new_archive_etag) ... ok
test_main_keeps_a_working_aws_cli_when_the_download_fails_and_never_on_a_bad_signature (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_main_keeps_a_working_aws_cli_when_the_download_fails_and_never_on_a_bad_signature) ... ok
test_main_keeps_an_installed_aws_cli_offline_and_fails_a_fresh_install (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_main_keeps_an_installed_aws_cli_offline_and_fails_a_fresh_install) ... ok
test_main_reinstalls_a_broken_aws_cli_even_when_the_etag_matches (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_main_reinstalls_a_broken_aws_cli_even_when_the_etag_matches) ... ok
test_main_repairs_a_same_version_directory_the_upstream_update_would_skip (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_main_repairs_a_same_version_directory_the_upstream_update_would_skip) ... ok
test_main_skips_when_the_archive_etag_is_the_recorded_one (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_main_skips_when_the_archive_etag_is_the_recorded_one) ... ok
test_platform_package_managers_and_wrapper_own_aws_cli (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_platform_package_managers_and_wrapper_own_aws_cli) ... ok
test_repository_key_has_expected_current_fingerprint (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_repository_key_has_expected_current_fingerprint) ... ok
test_staged_binary_that_is_not_aws_cli_preserves_existing_aws_and_skips_installer (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_staged_binary_that_is_not_aws_cli_preserves_existing_aws_and_skips_installer) ... ok
test_verified_archive_runs_installer_with_user_local_update_arguments (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments) ... FAIL
AssertionError: 0 != 1 : mktemp: mkdtemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.4lX7tfdjLI: Operation not permitted
Ran 20 tests in 2.945s
FAILED (failures=2)
[exit 0]
```

## 5. The two sandbox failures on origin/main

```console
$ git worktree add -q --detach "$S/base" origin/main && (cd "$S/base" && uv run python -m unittest tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments 2>&1 | /usr/bin/grep -E "^FAIL:|mkdtemp failed|^Ran|^FAILED|^OK"); git worktree remove "$S/base"
FAIL: test_gpgv_failure_preserves_existing_aws_and_skips_unzip (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_gpgv_failure_preserves_existing_aws_and_skips_unzip)
FAIL: test_verified_archive_runs_installer_with_user_local_update_arguments (tests.unit.test_aws_cli_acquisition.AwsCliAcquisitionTest.test_verified_archive_runs_installer_with_user_local_update_arguments)
AssertionError: 0 != 1 : mktemp: mkdtemp failed on /var/folders/py/p9bt7jvj2g7_hh3cvsgcv6600000gn/T/tmp.n19zUbd6yN: Operation not permitted
Ran 2 tests in 0.062s
FAILED (failures=2)
[exit 0]
```

## 6. The Check: shellcheck, with bash -n, shfmt and ruff

```console
$ shellcheck install/ubuntu/common/aws_cli.sh && echo shellcheck-clean; shellcheck install/macos/common/dependencies.sh && echo "shellcheck dependencies.sh: clean"; bash -n install/ubuntu/common/aws_cli.sh && echo "bash -n: ok"; shfmt -i 4 -sr -d install/ubuntu/common/aws_cli.sh install/macos/common/dependencies.sh && echo shfmt-clean
shellcheck-clean
shellcheck dependencies.sh: clean
bash -n: ok
shfmt-clean
[exit 0]
```
```console
$ ruff --version; ruff format --check tests/unit/test_aws_cli_acquisition.py; ruff check tests/unit/test_aws_cli_acquisition.py | tail -2; git show origin/main:tests/unit/test_aws_cli_acquisition.py | ruff check --stdin-filename tests/unit/test_aws_cli_acquisition.py - | tail -2
ruff 0.17.0
1 file already formatted
Found 1 error.
[*] 1 fixable with `--fix`.
Found 1 error.
[*] 1 fixable with `--fix`.
[exit 0]
```

## 7. Caps

```console
$ git diff --numstat origin/main...HEAD
3	0	home/.chezmoiscripts/macos/run_after_04-install-aws-cli.sh.tmpl
0	1	install/macos/common/dependencies.sh
32	5	install/ubuntu/common/aws_cli.sh
147	1	tests/unit/test_aws_cli_acquisition.py
[exit 0]
```
```console
$ git diff --numstat origin/main...HEAD | awk '$3 !~ /^(tests|\.orchestration)\// {o += $1 + $2; f++} $3 ~ /^tests\// {t += $1} END {printf "outside tests/ and .orchestration/: %d changed lines (cap 200), %d files; under tests/: %d added lines (cap 1000)\n", o, f, t}'
outside tests/ and .orchestration/: 41 changed lines (cap 200), 3 files; under tests/: 147 added lines (cap 1000)
[exit 0]
```

## 8. Mutation pass on the macOS branch

```console
$ shasum -a 256 install/ubuntu/common/aws_cli.sh > "$S/before.sha"; uv run --no-project python -I "$S/mutate.py" "$PWD"; shasum -a 256 -c "$S/before.sha"
N1 no Darwin pkg URL: caught
N2 install.sh URL: caught
N3 path not install.sh: caught
N4 version.txt failure not 3: caught
N5 no trim: caught
N6 installer before gpgv: caught
N7 XDG_DATA_HOME wrong: caught
N8 XDG_BIN_HOME unset: caught
N9 installer status lost: caught
N10 no postcondition: caught
N11 macOS runs the Linux path: caught
N12 Darwin not detected in install: caught
mutations: 12, caught 12, survived 0
install/ubuntu/common/aws_cli.sh: OK
[exit 0]
```

## 9. CI and the Bot on `c2638b32`, and the real macOS install

Run outside the sandbox through the permission gate (sandbox record, rows 4, 5, 7 and 8).

```console
$ bash scratchpad/bot-wait.sh 363 c2638b329277dc1fe1ec51419c9532bd64af4387 1792027418
error connecting to api.github.com
check your internet connection or https://githubstatus.com
https://github.com/mryfmo/dotfiles/pull/363#issuecomment-6182834286
posted @codex review at 2741s
elapsed=2741s bot: none
[exit 0]
```
```console
$ gh api --paginate repos/mryfmo/dotfiles/issues/363/comments --jq '.[]|[.id,.user.login,.created_at,(.body|split("\n")[0])]|@tsv'; echo reviews:; gh api --paginate repos/mryfmo/dotfiles/pulls/363/reviews --jq '.[]|[.id,.user.login,.commit_id[0:8],.submitted_at,.state]|@tsv'; echo comments:; gh api --paginate repos/mryfmo/dotfiles/pulls/363/comments --jq '.[]|[.id,.user.login,.original_commit_id[0:8],.path,.line]|@tsv'; gh pr view 363 --repo mryfmo/dotfiles --json headRefOid,mergeStateStatus --jq '[.headRefOid,.mergeStateStatus]|@tsv'
6182195957	coderabbitai[bot]	2026-10-15T01:22:08Z	<!-- This is an auto-generated comment: summarize by coderabbit.ai -->
6182215280	chatgpt-codex-connector[bot]	2026-10-15T01:23:47Z	<!-- codex-pull-request-review-summary -->
6182834286	moriya-fumio-thd	2026-10-15T02:12:59Z	@codex review
6182875026	chatgpt-codex-connector[bot]	2026-10-15T02:16:04Z	Codex Review: Didn't find any major issues. :tada:
reviews:
comments:
c2638b329277dc1fe1ec51419c9532bd64af4387	UNKNOWN
[exit 0]
```
```console
$ gh api repos/mryfmo/dotfiles/issues/comments/6182875026 --jq '.body' | head -4
Codex Review: Didn't find any major issues. :tada:

**Reviewed commit:** `c2638b3292`

[exit 0]
```

Comment 6182215280, the Bot's summary table, lists the Code Review as completed at 02:16:05Z on `c2638b3` (a manual request) and the Security Review as completed at 01:28:01Z on `c2638b3` (draft marked ready).

```console
$ gh pr checks 363 --repo mryfmo/dotfiles --watch --interval 30 > /dev/null 2>&1; echo "checks-watch-exit=$?"; gh pr checks 363 --repo mryfmo/dotfiles
checks-watch-exit=1
CodeRabbit	pass	0		Review skipped: automatic reviews are disabled
GitGuardian Security Checks	pass	1s	https://dashboard.gitguardian.com	
build	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/38665395276/job/116196068641	
build (client)	pass	5s	https://github.com/mryfmo/dotfiles/actions/runs/38665395288/job/116196068993	
build (server)	pass	4s	https://github.com/mryfmo/dotfiles/actions/runs/38665395288/job/116196068684	
private-bootstrap (macos-14, client)	pass	14s	https://github.com/mryfmo/dotfiles/actions/runs/38665395268/job/116196069202	
private-bootstrap (ubuntu-24.04, client)	pass	8s	https://github.com/mryfmo/dotfiles/actions/runs/38665395268/job/116196069018	
private-bootstrap (ubuntu-24.04, server)	pass	11s	https://github.com/mryfmo/dotfiles/actions/runs/38665395268/job/116196069211	
public-bootstrap (macos-14, client)	pass	8m44s	https://github.com/mryfmo/dotfiles/actions/runs/38665395268/job/116196069142	
public-bootstrap (ubuntu-24.04, client)	pass	10m27s	https://github.com/mryfmo/dotfiles/actions/runs/38665395268/job/116196069268	
public-bootstrap (ubuntu-24.04, server)	pass	8m5s	https://github.com/mryfmo/dotfiles/actions/runs/38665395268/job/116196069093	
test (macos-14, client)	pass	7m6s	https://github.com/mryfmo/dotfiles/actions/runs/38665395303/job/116196069126	
test (ubuntu-24.04, client)	pass	8m49s	https://github.com/mryfmo/dotfiles/actions/runs/38665395303/job/116196068735	
test (ubuntu-24.04, server)	pass	5m46s	https://github.com/mryfmo/dotfiles/actions/runs/38665395303/job/116196069045	
test (ubuntu-26.04, client)	pass	8m33s	https://github.com/mryfmo/dotfiles/actions/runs/38665395303/job/116196068943	
validate	pass	1m48s	https://github.com/mryfmo/dotfiles/actions/runs/38665395298/job/116196068543	
[exit 0]
```

The job log of `public-bootstrap (macos-14, client)` (job 116196069142), saved with `gh run view --repo mryfmo/dotfiles --job 116196069142 --log`, has 178259 lines. Line 176266 starts the rendered wrapper, `diff --git a/.chezmoiscripts/macos/04-install-aws-cli.sh b/.chezmoiscripts/macos/04-install-aws-cli.sh`. The excerpt below is the script's run, cut to the time of day: the runner's `HOME` is written `$HOME`, its user directory `<runner home>`, and the installer's temporary directory `<tmp>`.

```text
T01:34:05.6684640Z gpgv: Signature made Wed Oct 14 18:12:39 2026 UTC
T01:34:05.6686000Z gpgv:                using RSA key FB5DB77FD5C118B80511ADA8A6310ACC4672475C
T01:34:05.6690390Z gpgv: Good signature from "AWS CLI Team <aws-cli@amazon.com>"
T01:34:05.8537350Z Installing AWS CLI 2.38.1
T01:34:05.8589160Z Downloading AWS CLI installer from https://awscli.amazonaws.com/AWSCLIV2-2.38.1.pkg?src=script-exe
T01:34:13.8645260Z installer: Package name is AWS Command Line Interface
T01:34:13.8666240Z installer: choices changes file '<tmp>/choices.xml' applied
T01:34:13.8728790Z installer: Upgrading at base path <runner home>
T01:34:13.8729240Z installer: The upgrade was successful.
T01:34:14.5058060Z AWS CLI 2.38.1 installed to $HOME/.local/share/aws-cli
T01:34:14.5060190Z Ensure $HOME/.local/bin is on your PATH. When multiple installs exist, PATH order determines which 'aws' runs.
T01:34:14.8302790Z Installed aws-cli/2.38.1.
```
