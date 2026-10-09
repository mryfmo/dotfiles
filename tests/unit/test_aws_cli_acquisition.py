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

    def run_postcondition(self, aws_fixture):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / "home"
            aws = home / ".local/bin/aws"
            aws.parent.mkdir(parents=True)
            if aws_fixture is not None:
                aws.write_text(aws_fixture)
                aws.chmod(0o755)
            return self.run_shell(
                "exit_zero_installer() { return 0; }\nexit_zero_installer\nverify_aws_cli_install",
                {"HOME": str(home)},
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

    def test_exit_zero_install_of_any_aws_cli_version_passes_and_reports_it(self):
        # No version is pinned: whatever release AWS serves is accepted and reported.
        for version in (AWS_CLI_VERSION, "2.35.20"):
            with self.subTest(version=version):
                result = self.run_postcondition(f"#!/bin/sh\nprintf 'aws-cli/{version} Python/3.13 Linux/6\\n'\n")
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(f"Installed aws-cli/{version}.\n", result.stdout)

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
