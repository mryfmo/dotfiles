import os
import re
import subprocess
import tempfile
import tomllib
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class SupplyChainPolicyTest(unittest.TestCase):
    def test_installer_cleanup_survives_mock_function_returns(self):
        cases = {
            "install/common/mise.sh": r'''
uname() { [ "$1" = -s ] && printf Linux || printf x86_64; }
curl() {
    local output
    while [ "$#" -gt 0 ]; do
        if [ "$1" = -o ]; then output="$2"; shift 2; else shift; fi
    done
    printf payload > "${output}"
}
verify_mise_archive() { :; }
tar() {
    local destination
    while [ "$#" -gt 0 ]; do
        if [ "$1" = -C ]; then destination="$2"; shift 2; else shift; fi
    done
    mkdir -p "${destination}/mise/bin"
    printf '#!/bin/sh\nprintf ":\\n"\n' > "${destination}/mise/bin/mise"
    chmod +x "${destination}/mise/bin/mise"
}
install() { cp "$3" "$4"; chmod 0755 "$4"; }
mv() { command mv "$@"; }
install_mise
''',
            "install/common/sheldon.sh": r'''
cargo() {
    mkdir -p "${CARGO_INSTALL_ROOT}/bin"
    printf '#!/bin/sh\n' > "${CARGO_INSTALL_ROOT}/bin/sheldon"
    chmod +x "${CARGO_INSTALL_ROOT}/bin/sheldon"
}
install() { cp "$3" "$4"; chmod 0755 "$4"; }
mv() { command mv "$@"; }
install_sheldon
''',
            "install/ubuntu/server/starship.sh": r'''
uname() { printf x86_64; }
curl() {
    local output
    while [ "$#" -gt 0 ]; do
        if [ "$1" = -o ]; then output="$2"; shift 2; else shift; fi
    done
    if [ -n "${output:-}" ]; then printf archive > "${output}"; else printf checksum; fi
}
sha256sum() { printf 'checksum  %s\n' "$1"; }
tar() {
    local destination
    while [ "$#" -gt 0 ]; do
        if [ "$1" = -C ]; then destination="$2"; shift 2; else shift; fi
    done
    printf '#!/bin/sh\n' > "${destination}/starship"
    chmod +x "${destination}/starship"
}
install() { cp "$3" "$4"; chmod 0755 "$4"; }
mv() { command mv "$@"; }
install_starship
''',
        }
        for relative, body in cases.items():
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                home = root / "home"
                temp = root / "tmp"
                home.mkdir()
                temp.mkdir()
                result = subprocess.run(
                    [
                        "bash",
                        "-c",
                        'set -Eeuo pipefail\nsource "$1"\n' + body + '\n[ -z "$(trap -p RETURN)" ]\n',
                        "_",
                        str(ROOT / relative),
                    ],
                    env={**os.environ, "HOME": str(home), "TMPDIR": str(temp)},
                    check=False,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertTrue((home / ".local/bin" / Path(relative).stem).is_file())
                self.assertEqual([], list(temp.iterdir()))

    def test_installer_cleanup_preserves_failure_status(self):
        cases = {
            "install/common/mise.sh": ("mise_artifact() { return 42; }", "install_mise"),
            "install/common/sheldon.sh": ("cargo() { return 42; }", "install_sheldon"),
            "install/ubuntu/server/starship.sh": ("starship_artifact() { return 42; }", "install_starship"),
        }
        for relative, (mock, function) in cases.items():
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / "home").mkdir()
                (root / "tmp").mkdir()
                result = subprocess.run(
                    ["bash", "-c", f'source "$1"\nset +e\n{mock}\n{function}\n[ "$?" -eq 42 ]\n', "_", str(ROOT / relative)],
                    env={**os.environ, "HOME": str(root / "home"), "TMPDIR": str(root / "tmp")},
                    check=False,
                )
                self.assertEqual(0, result.returncode)
                self.assertEqual([], list((root / "tmp").iterdir()))

    def test_executable_downloads_are_verified_and_not_piped_to_shell(self):
        paths = [ROOT / "setup.sh", *sorted((ROOT / "install").rglob("*.sh"))]
        executable = "\n".join(
            line
            for path in paths
            for line in path.read_text().splitlines()
            if not line.lstrip().startswith("#")
        )
        self.assertNotRegex(executable, r"curl[^\n]*\|\s*(?:sh|bash|dash)")
        for path in (
            ROOT / "setup.sh",
            ROOT / "install/common/mise.sh",
            ROOT / "install/common/sheldon.sh",
            ROOT / "install/macos/common/brew.sh",
            ROOT / "install/ubuntu/server/starship.sh",
        ):
            self.assertRegex(path.read_text().lower(), r"checksum|sha-256", path)

    def test_binary_installers_replace_from_same_directory_stages(self):
        expected = {
            "setup.sh": "${bin_dir}/chezmoi.tmp.XXXXXX",
            "install/common/mise.sh": "${MISE_INSTALL_PATH}.tmp.XXXXXX",
            "install/common/sheldon.sh": "${BIN_DIR}/sheldon.tmp.XXXXXX",
            "install/ubuntu/server/starship.sh": "${BIN_DIR}/starship.tmp.XXXXXX",
        }
        for relative, stage in expected.items():
            text = (ROOT / relative).read_text()
            self.assertIn(stage, text, relative)
            self.assertIn("mv -f", text, relative)

    def test_mise_versions_are_exact_and_locking_is_enforced(self):
        config = (ROOT / "home/dot_mise/config.toml").read_text()
        self.assertNotRegex(config, r'=\s*"(?:latest|lts)"|version\s*=\s*"latest"')
        self.assertIn("locked = true", config)
        self.assertIn("lockfile = true", config)
        self.assertTrue((ROOT / "home/dot_mise/mise.lock").is_file())
        self.assertTrue((ROOT / "home/dot_config/mise/symlink_mise.lock.tmpl").is_file())

    def test_mise_lock_matches_config_and_supported_platforms(self):
        with (ROOT / "home/dot_mise/config.toml").open("rb") as config_file:
            config = tomllib.load(config_file)
        with (ROOT / "home/dot_mise/mise.lock").open("rb") as lock_file:
            lock = tomllib.load(lock_file)
        versions = {name: entries[0]["version"] for name, entries in lock["tools"].items()}
        for name, request in config["tools"].items():
            version = request if isinstance(request, str) else request["version"]
            self.assertEqual(version, versions.get(name), name)

        expected = {
            "platforms.linux-arm64",
            "platforms.linux-x64",
            "platforms.macos-arm64",
            "platforms.macos-x64",
        }
        for name in ("fd", "github:mikefarah/yq"):
            platforms = {key for key in lock["tools"][name][0] if key.startswith("platforms.")}
            self.assertEqual(expected, platforms, name)
        self.assertEqual("cargo:eza", lock["tools"]["cargo:eza"][0]["backend"])
        self.assertFalse(config["settings"]["cargo"]["binstall"])

    def test_sheldon_uses_locked_crates_io_source(self):
        script = (ROOT / "install/common/sheldon.sh").read_text()
        for token in (
            "cargo install",
            "--locked --features vendored --registry crates-io",
            '--version "=${SHELDON_VERSION}" sheldon',
        ):
            self.assertIn(token, script)
        self.assertNotIn("crate.sh", script)
        self.assertNotIn("github.com/rossmacarthur/sheldon/releases", script)

    def test_sheldon_git_sources_have_revisions(self):
        for path in sorted((ROOT / "home/dot_config/sheldon/plugin_sources").rglob("*.toml")):
            text = path.read_text()
            github_count = len(re.findall(r"^github\s*=", text, re.MULTILINE))
            revision_count = len(re.findall(r"^rev\s*=\s*\"[0-9a-f]{40}\"", text, re.MULTILINE))
            self.assertEqual(github_count, revision_count, path)

    def test_externals_use_fixed_urls_and_checksums(self):
        text = (ROOT / "home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl").read_text()
        self.assertNotIn("gitHubLatestReleaseAssetURL", text)
        self.assertEqual(2, text.count("  checksum:\n    sha256:"))
        self.assertNotIn("CHEZMOI_OFFLINE", text)

    def test_externals_render_without_network_discovery(self):
        env = os.environ.copy()
        env.update(
            HTTPS_PROXY="http://127.0.0.1:9",
            HTTP_PROXY="http://127.0.0.1:9",
            ALL_PROXY="http://127.0.0.1:9",
        )
        result = subprocess.run(
            [
                "chezmoi",
                "execute-template",
                "--source",
                str(ROOT / "home"),
                "--override-data",
                '{"system":"client"}',
                "--file",
                str(ROOT / "home/.chezmoitemplates/chezmoiexternal.d/common.yaml.tmpl"),
            ],
            cwd=ROOT,
            env=env,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("nerd-fonts/releases/download/v3.4.0", result.stdout)
        self.assertNotIn("api.github.com", result.stdout)

    def test_external_checksum_failure_preserves_destination(self):
        with tempfile.TemporaryDirectory(prefix="chezmoi-checksum-") as directory:
            root = Path(directory)
            source = root / "source"
            destination = root / "home"
            target = destination / "Fonts/Test"
            source.mkdir()
            target.mkdir(parents=True)
            (target / "sentinel").write_text("preserve\n")
            archive = root / "font.zip"
            with zipfile.ZipFile(archive, "w") as fixture:
                fixture.writestr("font.txt", "untrusted\n")
            (source / ".chezmoiexternal.yaml").write_text(
                '"Fonts/Test":\n'
                '  type: "archive"\n'
                f'  url: "{archive.as_uri()}"\n'
                '  checksum:\n'
                f'    sha256: "{"0" * 64}"\n'
            )
            result = subprocess.run(
                [
                    "chezmoi",
                    "--source",
                    str(source),
                    "--destination",
                    str(destination),
                    "--cache",
                    str(root / "cache"),
                    "--persistent-state",
                    str(root / "state.boltdb"),
                    "--config",
                    "/dev/null",
                    "--config-format",
                    "none",
                    "apply",
                    "--force",
                ],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("preserve\n", (target / "sentinel").read_text())
            self.assertFalse((target / "font.txt").exists())

    def test_nix_inputs_and_ci_use_2605(self):
        flake = (ROOT / "flake.nix").read_text()
        self.assertNotIn("25.05", flake)
        self.assertEqual(3, flake.count("26.05"))
        workflow = (ROOT / ".github/workflows/test.yaml").read_text()
        self.assertIn("should_nix:", workflow)
        self.assertIn("nix:", workflow)
        self.assertIn("macos-14", workflow)
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("Require committed Nix lock", workflow)

    def test_dependabot_owns_github_action_updates(self):
        config = (ROOT / ".github/dependabot.yml").read_text()
        self.assertIn('package-ecosystem: "github-actions"', config)
        self.assertIn('directory: "/"', config)


if __name__ == "__main__":
    unittest.main()
