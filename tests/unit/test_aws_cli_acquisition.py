import os
import re
import subprocess
import tempfile
import time
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "install/ubuntu/common/aws_cli.sh"
# The archive is unversioned (AWS's current release), so any reported version is a fixture value.
AWS_CLI_VERSION = "2.37.6"
FINGERPRINT = re.search(r'^readonly AWS_CLI_FINGERPRINT="([0-9A-F]{40})"$', INSTALLER.read_text(), re.MULTILINE).group(
    1
)


class AwsCliAcquisitionTest(unittest.TestCase):
    def run_shell(self, body, env=None):
        return subprocess.run(
            ["bash", "-c", 'source "$1"\n' + body, "_", str(INSTALLER)],
            env={**os.environ, **(env or {})},
            check=False,
            text=True,
            capture_output=True,
        )

    def run_postcondition(self, aws_fixture, staged=AWS_CLI_VERSION):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            aws = home / ".local/bin/aws"
            aws.parent.mkdir(parents=True)
            if aws_fixture is not None:
                aws.write_text(aws_fixture)
                aws.chmod(0o755)
            return self.run_shell(
                'exit_zero_installer() { return 0; }\nexit_zero_installer\nverify_aws_cli_install "${STAGED}"',
                {"HOME": str(home), "STAGED": staged},
            )

    def test_linux_urls_are_the_unversioned_current_archive_and_unknown_architecture_fails(self):
        for architecture in ("x86_64", "aarch64"):
            with self.subTest(architecture=architecture):
                result = self.run_shell(
                    'uname() { printf "%s\\n" "$ARCH"; }\naws_cli_url',
                    {"ARCH": architecture},
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(
                    f"https://awscli.amazonaws.com/awscli-exe-linux-{architecture}.zip\n",
                    result.stdout,
                )

        result = self.run_shell('uname() { printf "riscv64\\n"; }\naws_cli_url')
        self.assertNotEqual(0, result.returncode)
        self.assertIn("Unsupported AWS CLI architecture: riscv64", result.stderr)

    def test_gpgv_failure_preserves_existing_aws_and_skips_unzip(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home = root / "home"
            temp = root / "tmp"
            key = root / "key.asc"
            gpgv_marker = root / "gpgv-ran"
            marker = root / "unzip-ran"
            aws = home / ".local/bin/aws"
            aws.parent.mkdir(parents=True)
            temp.mkdir()
            key.write_text("fixture\n")
            aws.write_text("existing\n")

            result = self.run_shell(
                r"""
uname() { printf 'x86_64\n'; }
curl() {
    local output
    while [ "$#" -gt 0 ]; do
        if [ "$1" = --output ]; then output="$2"; shift 2; else shift; fi
    done
    printf payload > "${output}"
}
gpg() {
    case " $* " in
        *" --with-colons "*)
            printf 'pub:-:4096:1:A6310ACC4672475C:1568845749:1814472778::::::sc::::::23::0:\n'
            printf 'fpr:::::::::@FINGERPRINT@:\n'
            ;;
        *" --dearmor "*)
            while [ "$#" -gt 0 ]; do
                if [ "$1" = --output ]; then printf keyring > "$2"; return; else shift; fi
            done
            ;;
    esac
}
gpgv() { touch "${GPGV_MARKER}"; return 1; }
unzip() { touch "${MARKER}"; }
install_aws_cli
""".replace("@FINGERPRINT@", FINGERPRINT),
                {
                    "AWS_CLI_KEY_PATH": str(key),
                    "GPGV_MARKER": str(gpgv_marker),
                    "HOME": str(home),
                    "MARKER": str(marker),
                    "TMPDIR": str(temp),
                },
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("existing\n", aws.read_text())
            self.assertTrue(gpgv_marker.exists())
            self.assertFalse(marker.exists())
            self.assertEqual([], list(temp.iterdir()))

    def test_key_metadata_failures_stop_before_dearmor_and_gpgv(self):
        valid_pub = "pub:-:4096:1:A6310ACC4672475C:1568845749:1814472778::::::sc::::::23::0:"
        valid_fpr = f"fpr:::::::::{FINGERPRINT}:"
        cases = {
            "fingerprint": f"{valid_pub}\nfpr:::::::::{'0' * 40}:\n",
            "expired": f"pub:-:4096:1:A6310ACC4672475C:1568845749:1::::::sc::::::23::0:\n{valid_fpr}\n",
            "multiple": f"{valid_pub}\n{valid_fpr}\n{valid_pub}\n{valid_fpr}\n",
        }
        for name, key_data in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                home = root / "home"
                temp = root / "tmp"
                marker = root / "unsafe-command-ran"
                home.mkdir()
                temp.mkdir()
                result = self.run_shell(
                    r"""
uname() { printf 'x86_64\n'; }
curl() {
    while [ "$#" -gt 0 ]; do
        if [ "$1" = --output ]; then printf payload > "$2"; return; else shift; fi
    done
}
gpg() {
    case " $* " in
        *" --with-colons "*) printf '%s\n' "${KEY_DATA}" ;;
        *" --dearmor "*) touch "${MARKER}" ;;
    esac
}
gpgv() { touch "${MARKER}"; }
unzip() { touch "${MARKER}"; }
install_aws_cli
""",
                    {
                        "AWS_CLI_KEY_PATH": str(root / "key.asc"),
                        "HOME": str(home),
                        "KEY_DATA": key_data,
                        "MARKER": str(marker),
                        "TMPDIR": str(temp),
                    },
                )
                self.assertNotEqual(0, result.returncode)
                self.assertFalse(marker.exists())
                self.assertEqual([], list(temp.iterdir()))

    def test_verified_archive_runs_installer_with_user_local_update_arguments(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home = root / "home"
            temp = root / "tmp"
            key = root / "key.asc"
            args = root / "args"
            gpgv_args = root / "gpgv-args"
            urls = root / "urls"
            home.mkdir()
            temp.mkdir()
            key.write_text("fixture\n")

            result = self.run_shell(
                r"""
uname() { printf 'aarch64\n'; }
curl() {
    local output url
    while [ "$#" -gt 0 ]; do
        if [ "$1" = --output ]; then output="$2"; shift 2; else url="$1"; shift; fi
    done
    printf '%s\n' "${url}" >> "${URLS_PATH}"
    printf payload > "${output}"
}
gpg() {
    case " $* " in
        *" --with-colons "*)
            printf 'pub:-:4096:1:A6310ACC4672475C:1568845749:1814472778::::::sc::::::23::0:\n'
            printf 'fpr:::::::::@FINGERPRINT@:\n'
            ;;
        *" --dearmor "*)
            while [ "$#" -gt 0 ]; do
                if [ "$1" = --output ]; then printf keyring > "$2"; return; else shift; fi
            done
            ;;
    esac
}
gpgv() { printf '%s\n' "$@" > "${GPGV_ARGS_PATH}"; }
unzip() {
    local destination
    while [ "$#" -gt 0 ]; do
        if [ "$1" = -d ]; then destination="$2"; shift 2; else shift; fi
    done
    mkdir -p "${destination}/aws"
    cat > "${destination}/aws/install" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$@" > "${ARGS_PATH}"
EOF
    chmod +x "${destination}/aws/install"
    mkdir -p "${destination}/aws/dist"
    cat > "${destination}/aws/dist/aws" <<'EOF'
#!/usr/bin/env bash
printf 'aws-cli/@AWS_CLI_VERSION@ Python/3.13 Linux/6\n'
EOF
    chmod +x "${destination}/aws/dist/aws"
    mkdir -p "${HOME}/.local/bin"
    cat > "${HOME}/.local/bin/aws" <<'EOF'
#!/usr/bin/env bash
printf 'aws-cli/@AWS_CLI_VERSION@ Python/3.13 Linux/6\n'
EOF
    chmod +x "${HOME}/.local/bin/aws"
}
install_aws_cli
""".replace("@FINGERPRINT@", FINGERPRINT).replace("@AWS_CLI_VERSION@", AWS_CLI_VERSION),
                {
                    "ARGS_PATH": str(args),
                    "AWS_CLI_KEY_PATH": str(key),
                    "GPGV_ARGS_PATH": str(gpgv_args),
                    "HOME": str(home),
                    "TMPDIR": str(temp),
                    "URLS_PATH": str(urls),
                },
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn(f"Installed aws-cli/{AWS_CLI_VERSION}.", result.stdout)
            self.assertEqual(
                [
                    "--install-dir",
                    str(home / ".local/share/aws-cli"),
                    "--bin-dir",
                    str(home / ".local/bin"),
                    "--update",
                ],
                args.read_text().splitlines(),
            )
            base = "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"
            self.assertEqual([base, f"{base}.sig"], urls.read_text().splitlines())
            verified = gpgv_args.read_text().splitlines()
            self.assertEqual("--keyring", verified[0])
            self.assertTrue(verified[1].endswith("/aws-cli-keyring.gpg"))
            self.assertTrue(verified[2].endswith("/awscliv2.zip.sig"))
            self.assertTrue(verified[3].endswith("/awscliv2.zip"))
            self.assertEqual([], list(temp.iterdir()))

    def test_staged_binary_that_is_not_aws_cli_preserves_existing_aws_and_skips_installer(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            home = root / "home"
            temp = root / "tmp"
            key = root / "key.asc"
            installer_marker = root / "installer-ran"
            aws = home / ".local/bin/aws"
            aws.parent.mkdir(parents=True)
            temp.mkdir()
            key.write_text("fixture\n")
            sentinel = b"existing aws sentinel\n"
            aws.write_bytes(sentinel)

            result = self.run_shell(
                r"""
uname() { printf 'x86_64\n'; }
curl() {
    while [ "$#" -gt 0 ]; do
        if [ "$1" = --output ]; then printf payload > "$2"; return; else shift; fi
    done
}
gpg() {
    case " $* " in
        *" --with-colons "*)
            printf 'pub:-:4096:1:A6310ACC4672475C:1568845749:1814472778::::::sc::::::23::0:\n'
            printf 'fpr:::::::::@FINGERPRINT@:\n'
            ;;
        *" --dearmor "*)
            while [ "$#" -gt 0 ]; do
                if [ "$1" = --output ]; then printf keyring > "$2"; return; else shift; fi
            done
            ;;
    esac
}
gpgv() { return 0; }
unzip() {
    local destination
    while [ "$#" -gt 0 ]; do
        if [ "$1" = -d ]; then destination="$2"; shift 2; else shift; fi
    done
    mkdir -p "${destination}/aws/dist"
    cat > "${destination}/aws/install" <<'EOF'
#!/usr/bin/env bash
touch "${INSTALLER_MARKER}"
printf mutated > "${HOME}/.local/bin/aws"
EOF
    chmod +x "${destination}/aws/install"
    cat > "${destination}/aws/dist/aws" <<'EOF'
#!/usr/bin/env bash
printf 'not-aws 1.0\n'
EOF
    chmod +x "${destination}/aws/dist/aws"
}
install_aws_cli
""".replace("@FINGERPRINT@", FINGERPRINT),
                {
                    "AWS_CLI_KEY_PATH": str(key),
                    "HOME": str(home),
                    "INSTALLER_MARKER": str(installer_marker),
                    "TMPDIR": str(temp),
                },
            )
            self.assertNotEqual(0, result.returncode)
            self.assertFalse(installer_marker.exists())
            self.assertEqual(sentinel, aws.read_bytes())
            self.assertEqual([], list(temp.iterdir()))

    def test_exit_zero_partial_install_without_binary_fails_postcondition(self):
        result = self.run_postcondition(None)
        self.assertNotEqual(0, result.returncode)

    def test_exit_zero_install_without_an_aws_cli_banner_fails_postcondition(self):
        result = self.run_postcondition("#!/bin/sh\nprintf 'not-aws 1.0\\n'\n")
        self.assertNotEqual(0, result.returncode)

    def test_exit_zero_install_passes_only_when_the_staged_version_is_active(self):
        # No version is pinned: whatever release AWS serves is accepted, but it must be the one now active.
        for version in (AWS_CLI_VERSION, "2.35.20"):
            with self.subTest(version=version):
                result = self.run_postcondition(
                    f"#!/bin/sh\nprintf 'aws-cli/{version} Python/3.13 Linux/6\\n'\n", staged=version
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(f"Installed aws-cli/{version}.\n", result.stdout)
        # An installer that skipped can leave an older CLI active: that is a failure, not an install.
        result = self.run_postcondition("#!/bin/sh\nprintf 'aws-cli/2.35.20 Python/3.13 Linux/6\\n'\n")
        self.assertNotEqual(0, result.returncode)
        self.assertIn(f"aws-cli/2.35.20 is active, not the staged aws-cli/{AWS_CLI_VERSION}", result.stderr)

    def run_main(self, home, head_etag, recorded_etag=None, installed=True):
        """Run main with a fake HEAD response and install; returns the result and the install marker."""
        state = home / ".local/state/dotfiles/aws-cli-archive.etag"
        marker = home / "install-ran"
        if installed:
            aws = home / ".local/bin/aws"
            aws.parent.mkdir(parents=True, exist_ok=True)
            aws.write_text("#!/bin/sh\nprintf 'aws-cli/2.37.6 Python/3.13 Linux/6\\n'\n")
            aws.chmod(0o755)
        if recorded_etag is not None:
            state.parent.mkdir(parents=True, exist_ok=True)
            state.write_text(f"{recorded_etag}\n")
        result = self.run_shell(
            r"""
uname() { printf 'x86_64\n'; }
curl() {
    [ -n "${HEAD_ETAG}" ] || return 6
    printf 'HTTP/2 200\r\nETag: %s\r\ncontent-length: 1\r\n\r\n' "${HEAD_ETAG}"
}
install_aws_cli() { touch "${HOME}/install-ran"; }
main
""",
            {"HOME": str(home), "HEAD_ETAG": head_etag, "XDG_STATE_HOME": ""},
        )
        return result, marker, state

    def test_main_skips_when_the_archive_etag_is_the_recorded_one(self):
        with tempfile.TemporaryDirectory() as directory:
            result, marker, _state = self.run_main(Path(directory), '"abc-1"', recorded_etag='"abc-1"')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertFalse(marker.exists())

    def test_main_reinstalls_a_broken_aws_cli_even_when_the_etag_matches(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            aws = home / ".local/bin/aws"
            aws.parent.mkdir(parents=True)
            aws.write_text("#!/bin/sh\nexit 42\n")
            aws.chmod(0o755)
            result, marker, _state = self.run_main(home, '"abc-1"', recorded_etag='"abc-1"', installed=False)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(marker.exists())

    def test_main_repairs_a_same_version_directory_the_upstream_update_would_skip(self):
        # aws/install --update exits 0 without copying when the version directory exists, so the repair
        # must remove that tree first, whether the active CLI is broken or an older one an interrupted
        # update left behind; a GPG-verified archive comes first.
        for case in ("broken active CLI", "older version active"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                home = root / "home"
                temp = root / "tmp"
                key = root / "key.asc"
                for path in (home, temp, root / "shim"):
                    path.mkdir()
                # macOS mktemp -d ignores TMPDIR; the shim keeps every temporary directory under the test.
                (root / "shim/mktemp").write_text(
                    '#!/bin/sh\nif [ "$*" = -d ]; then exec /usr/bin/mktemp -d "$TMPDIR/tmp.XXXXXX"; fi\nexec /usr/bin/mktemp "$@"\n'
                )
                (root / "shim/mktemp").chmod(0o755)
                key.write_text("fixture\n")
                version_dir = home / ".local/share/aws-cli/v2" / AWS_CLI_VERSION
                (version_dir / "bin").mkdir(parents=True)
                (version_dir / "bin/aws").write_text("#!/bin/sh\nexit 42\n")
                (version_dir / "bin/aws").chmod(0o755)
                (home / ".local/bin").mkdir(parents=True)
                active = version_dir / "bin/aws"
                if case == "older version active":
                    # An interrupted update: the new version directory exists, an older CLI still works.
                    active = home / ".local/share/aws-cli/v2/2.35.20/bin/aws"
                    active.parent.mkdir(parents=True)
                    active.write_text("#!/bin/sh\nprintf 'aws-cli/2.35.20 Python/3.13 Linux/6\\n'\n")
                    active.chmod(0o755)
                (home / ".local/bin/aws").symlink_to(active)
                state = home / ".local/state/dotfiles/aws-cli-archive.etag"
                state.parent.mkdir(parents=True)
                # A broken CLI behind the current ETag; or the older install's ETag, which the stricter
                # postcondition keeps, because the interrupted update never recorded the new one.
                state.write_text('"abc-1"\n' if case == "broken active CLI" else '"abc-0"\n')

                result = self.run_shell(
                    r"""
uname() { printf 'x86_64\n'; }
curl() {
    local output="" head=""
    while [ "$#" -gt 0 ]; do
        case "$1" in --output) output="$2"; shift 2 ;; --head) head=1; shift ;; *) shift ;; esac
    done
    if [ -n "${head}" ]; then printf 'HTTP/2 200\r\nETag: "abc-1"\r\n\r\n'; else printf payload > "${output}"; fi
}
gpg() {
    case " $* " in
        *" --with-colons "*)
            printf 'pub:-:4096:1:A6310ACC4672475C:1568845749:1814472778::::::sc::::::23::0:\n'
            printf 'fpr:::::::::@FINGERPRINT@:\n'
            ;;
        *" --dearmor "*)
            while [ "$#" -gt 0 ]; do
                if [ "$1" = --output ]; then printf keyring > "$2"; return; else shift; fi
            done
            ;;
    esac
}
gpgv() { return 0; }
unzip() {
    local destination
    while [ "$#" -gt 0 ]; do
        if [ "$1" = -d ]; then destination="$2"; shift 2; else shift; fi
    done
    mkdir -p "${destination}/aws/dist"
    printf '#!/bin/sh\nprintf "aws-cli/@AWS_CLI_VERSION@ Python/3.13 Linux/6\\n"\n' > "${destination}/aws/dist/aws"
    chmod +x "${destination}/aws/dist/aws"
    # Mimics upstream: --update with an existing version directory skips without copying.
    cat > "${destination}/aws/install" <<'EOF'
#!/usr/bin/env bash
while [ "$#" -gt 0 ]; do
    case "$1" in --install-dir) install_dir="$2"; shift 2 ;; --bin-dir) bin_dir="$2"; shift 2 ;; *) shift ;; esac
done
if [ -d "${install_dir}/v2/@AWS_CLI_VERSION@" ]; then
    echo "Found same AWS CLI version: ${install_dir}/v2/@AWS_CLI_VERSION@. Skipping install."
    exit 0
fi
mkdir -p "${install_dir}/v2/@AWS_CLI_VERSION@/bin" "${bin_dir}"
printf '#!/bin/sh\nprintf "aws-cli/@AWS_CLI_VERSION@ Python/3.13 Linux/6\\n"\n' > "${install_dir}/v2/@AWS_CLI_VERSION@/bin/aws"
chmod +x "${install_dir}/v2/@AWS_CLI_VERSION@/bin/aws"
ln -snf "${install_dir}/v2/@AWS_CLI_VERSION@" "${install_dir}/v2/current"
ln -sf "${install_dir}/v2/current/bin/aws" "${bin_dir}/aws"
EOF
    chmod +x "${destination}/aws/install"
}
main
""".replace("@FINGERPRINT@", FINGERPRINT).replace("@AWS_CLI_VERSION@", AWS_CLI_VERSION),
                    {
                        "AWS_CLI_KEY_PATH": str(key),
                        "HOME": str(home),
                        "TMPDIR": str(temp),
                        "XDG_STATE_HOME": "",
                        "PATH": f"{root / 'shim'}:{os.environ['PATH']}",
                    },
                )

                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn(f"Installed aws-cli/{AWS_CLI_VERSION}.", result.stdout)
                self.assertEqual(
                    f"aws-cli/{AWS_CLI_VERSION} Python/3.13 Linux/6\n",
                    subprocess.run([str(home / ".local/bin/aws")], text=True, capture_output=True, check=False).stdout,
                )
                self.assertEqual('"abc-1"\n', state.read_text())

    def test_main_installs_and_records_a_new_archive_etag(self):
        for recorded, installed in (('"abc-1"', True), (None, False)):
            with self.subTest(recorded=recorded, installed=installed), tempfile.TemporaryDirectory() as directory:
                result, marker, state = self.run_main(Path(directory), '"abc-2"', recorded, installed)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertTrue(marker.exists())
                self.assertEqual('"abc-2"\n', state.read_text())

    def test_main_keeps_an_installed_aws_cli_offline_and_fails_a_fresh_install(self):
        with tempfile.TemporaryDirectory() as directory:
            result, marker, _state = self.run_main(Path(directory), "", recorded_etag='"abc-1"')
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("could not reach the AWS CLI archive; the installed AWS CLI stays", result.stderr)
            self.assertFalse(marker.exists())
        with tempfile.TemporaryDirectory() as directory:
            result, marker, _state = self.run_main(Path(directory), "", installed=False)
            self.assertNotEqual(0, result.returncode)
            self.assertFalse(marker.exists())
        # Offline with a CLI that no longer runs: a failure, never "the installed AWS CLI stays".
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            aws = home / ".local/bin/aws"
            aws.parent.mkdir(parents=True)
            aws.write_text("#!/bin/sh\nexit 42\n")
            aws.chmod(0o755)
            result, marker, _state = self.run_main(home, "", recorded_etag='"abc-1"', installed=False)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("no working AWS CLI is installed", result.stderr)
            self.assertNotIn("stays", result.stderr)
            self.assertFalse(marker.exists())

    def test_main_keeps_a_working_aws_cli_when_the_download_fails_and_never_on_a_bad_signature(self):
        # The archive changed (a new ETag) but cannot be downloaded: a working CLI stays and its old ETag
        # stays recorded, so the next apply retries; with no CLI it fails; a bad signature always fails.
        for name, installed, env, expected_status, message in (
            (
                "download fails, working CLI",
                True,
                {"DOWNLOAD_FAIL": "1"},
                0,
                "could not download the AWS CLI archive; the installed AWS CLI stays",
            ),
            ("download fails, no CLI", False, {"DOWNLOAD_FAIL": "1"}, 3, ""),
            ("bad signature, working CLI", True, {}, 1, ""),
        ):
            with self.subTest(case=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                home = root / "home"
                tmp = root / "tmp"
                shim = root / "shim"
                for path in (home / ".local/bin", tmp, shim):
                    path.mkdir(parents=True)
                # macOS mktemp -d ignores TMPDIR; the shim keeps every temporary directory under the test.
                (shim / "mktemp").write_text(
                    '#!/bin/sh\nif [ "$*" = -d ]; then exec /usr/bin/mktemp -d "$TMPDIR/tmp.XXXXXX"; fi\nexec /usr/bin/mktemp "$@"\n'
                )
                (shim / "mktemp").chmod(0o755)
                aws = home / ".local/bin/aws"
                if installed:
                    aws.write_text("#!/bin/sh\nprintf 'aws-cli/2.35.20 Python/3.13 Linux/6\\n'\n")
                    aws.chmod(0o755)
                state = home / ".local/state/dotfiles/aws-cli-archive.etag"
                state.parent.mkdir(parents=True)
                state.write_text('"abc-1"\n')
                key = root / "key.asc"
                key.write_text("fixture\n")

                result = self.run_shell(
                    r"""
uname() { printf 'x86_64\n'; }
curl() {
    local output="" head=""
    while [ "$#" -gt 0 ]; do
        case "$1" in --output) output="$2"; shift 2 ;; --head) head=1; shift ;; *) shift ;; esac
    done
    if [ -n "${head}" ]; then printf 'HTTP/2 200\r\nETag: "abc-2"\r\n\r\n'; return; fi
    [ -z "${DOWNLOAD_FAIL:-}" ] || return 22
    printf payload > "${output}"
}
gpg() {
    case " $* " in
        *" --with-colons "*)
            printf 'pub:-:4096:1:A6310ACC4672475C:1568845749:1814472778::::::sc::::::23::0:\n'
            printf 'fpr:::::::::@FINGERPRINT@:\n'
            ;;
        *" --dearmor "*)
            while [ "$#" -gt 0 ]; do
                if [ "$1" = --output ]; then printf keyring > "$2"; return; else shift; fi
            done
            ;;
    esac
}
gpgv() { return 1; }
unzip() { touch "${HOME}/unzip-ran"; }
main
""".replace("@FINGERPRINT@", FINGERPRINT),
                    {
                        "AWS_CLI_KEY_PATH": str(key),
                        "HOME": str(home),
                        "TMPDIR": str(tmp),
                        "XDG_STATE_HOME": "",
                        "PATH": f"{shim}:{os.environ['PATH']}",
                        **env,
                    },
                )

                self.assertEqual(expected_status, result.returncode, result.stdout + result.stderr)
                self.assertIn(message, result.stderr)
                self.assertEqual('"abc-1"\n', state.read_text())
                self.assertFalse((home / "unzip-ran").exists())

    def test_repository_key_has_expected_current_fingerprint(self):
        key = ROOT / "home/dot_local/share/aws-cli-keys/aws-cli-public-key.asc"
        with tempfile.TemporaryDirectory() as directory:
            Path(directory).chmod(0o700)
            listed = subprocess.run(
                [
                    "gpg",
                    "--homedir",
                    directory,
                    "--batch",
                    "--with-colons",
                    "--import-options",
                    "show-only",
                    "--import",
                    str(key),
                ],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, listed.returncode, listed.stderr)

        records = [line.split(":") for line in listed.stdout.splitlines()]
        public_keys = [record for record in records if record[0] == "pub"]
        fingerprints = [record[9] for record in records if record[0] == "fpr"]
        self.assertEqual(1, len(public_keys))
        self.assertEqual([FINGERPRINT], fingerprints)
        self.assertEqual("-", public_keys[0][1])
        self.assertGreater(int(public_keys[0][6]), int(time.time()))

    def test_platform_package_managers_and_wrapper_own_aws_cli(self):
        mac_dependencies = (ROOT / "install/macos/common/dependencies.sh").read_text()
        self.assertIn("readonly BREW_PACKAGES=(\n    awscli\n", mac_dependencies)
        self.assertNotIn("awscli.amazonaws.com", mac_dependencies)
        for forbidden in (".pkg", "brew tap", "git clone", "make install"):
            self.assertNotIn(forbidden, mac_dependencies)

        wrapper = (ROOT / "home/.chezmoiscripts/ubuntu/run_after_04-install-aws-cli.sh.tmpl").read_text()
        self.assertIn('include "../install/ubuntu/common/aws_cli.sh"', wrapper)
        self.assertNotIn(".system", wrapper)

        with (ROOT / "home/dot_mise/config.toml").open("rb") as config_file:
            config = tomllib.load(config_file)
        self.assertNotIn("aws-cli", config["tools"])

        ownership = (ROOT / "docs/history/nix-first-architecture.md").read_text()
        migration = (ROOT / "docs/history/nix-migration.md").read_text()
        for statement in (
            "Default macOS: Homebrew owns the AWS CLI version and installation integrity.",
            "Repository snapshot pinning for Homebrew is outside Plan004's scope.",
            "Default Ubuntu: the signed AWS archive installer owns the user-local installation.",
            "Opt-in Nix activation: `awscli2` owns the active AWS CLI on `PATH`.",
            "Deactivating Nix returns AWS CLI ownership to the operating-system default.",
            "Chezmoi never mutates the Nix store.",
        ):
            self.assertIn(statement, ownership)
        for statement in (
            "Homebrew owns the default macOS installation",
            "signed user-local installer owns the default Ubuntu installation",
            "opt-in Nix activation puts Nix `awscli2` first on `PATH`",
            "chezmoi never mutates the Nix store",
            "Homebrew repository snapshot pinning remains outside Plan004's scope",
        ):
            self.assertIn(statement, migration)


if __name__ == "__main__":
    unittest.main()
