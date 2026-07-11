import json
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
    cat > "${destination}/mise/bin/mise" <<'EOF'
#!/bin/sh
printf 'export MISE_ACTIVATED=1\nexport PATH="%s:$PATH"\nmise() { printf activated; }\n' "$(dirname "$0")"
EOF
    chmod +x "${destination}/mise/bin/mise"
}
install() { cp "$3" "$4"; chmod 0755 "$4"; }
mv() { command mv "$@"; }
install_mise
[ "${MISE_ACTIVATED}" = 1 ]
[ "$(type -t mise)" = function ]
[ "$(mise)" = activated ]
case ":${PATH}:" in *":${HOME}/.local/bin:"*) ;; *) exit 1 ;; esac
''',
            "install/common/sheldon.sh": r'''
mkdir -p "${HOME}/.local/bin"
cat > "${HOME}/.local/bin/mise" <<'EOF'
#!/bin/sh
[ "$1" = exec ] && [ "$2" = --locked ] && [ "$3" = -- ] && [ "$4" = cargo ] || exit 98
    mkdir -p "${CARGO_INSTALL_ROOT}/bin"
    printf '#!/bin/sh\n' > "${CARGO_INSTALL_ROOT}/bin/sheldon"
    chmod +x "${CARGO_INSTALL_ROOT}/bin/sheldon"
EOF
chmod +x "${HOME}/.local/bin/mise"
cargo() { return 99; }
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
            "install/common/sheldon.sh": (
                'mkdir -p "$(dirname "${MISE_BIN}")"; '
                'printf "#!/bin/sh\\nexit 42\\n" > "${MISE_BIN}"; chmod +x "${MISE_BIN}"',
                "install_sheldon",
            ),
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

    def test_mise_main_preserves_install_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "run-mise-install"
            result = subprocess.run(
                [
                    "bash",
                    "-c",
                    'source "$1"\nset +e\ninstall_mise() { return 42; }\n'
                    'run_mise_install() { touch "$2"; }\nmain\nstatus=$?\n'
                    '[ "$status" -eq 42 ] && [ ! -e "$2" ]\n',
                    "_",
                    str(ROOT / "install/common/mise.sh"),
                    str(marker),
                ],
                check=False,
            )
            self.assertEqual(0, result.returncode)

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

        bats = config["tools"]["http:bats"]
        self.assertEqual("bin", bats["bin_path"])
        self.assertEqual(1, bats["strip_components"])
        gcloud = config["tools"]["http:gcloud"]
        self.assertEqual("google-cloud-sdk/bin", gcloud["bin_path"])
        expected_gcloud = {
            "linux-x64": {
                "url": "https://storage.googleapis.com/cloud-sdk-release/google-cloud-cli-575.0.1-linux-x86_64.tar.gz",
                "checksum": "sha256:38198fa76b1aa64a332fadca7dba45f96c6dbb5cd9e77f173f9d6a65443e37ab",
            },
            "linux-arm64": {
                "url": "https://storage.googleapis.com/cloud-sdk-release/google-cloud-cli-575.0.1-linux-arm.tar.gz",
                "checksum": "sha256:e5c3a354d4c5775eccede626746547d6d3dc3f59db350f62f05dbc604eec5e3f",
            },
            "macos-x64": {
                "url": "https://storage.googleapis.com/cloud-sdk-release/google-cloud-cli-575.0.1-darwin-x86_64.tar.gz",
                "checksum": "sha256:0f9b0f45e5dff30d8c67c0f9ceb4d64b03497efa9135849b80ecf0cd0706009c",
            },
            "macos-arm64": {
                "url": "https://storage.googleapis.com/cloud-sdk-release/google-cloud-cli-575.0.1-darwin-arm.tar.gz",
                "checksum": "sha256:055892517a1101903938bbc1006c02feb639ec7efff8b25509c72e9a20351b3c",
            },
        }
        self.assertEqual(expected_gcloud, gcloud["platforms"])
        locked_gcloud = {
            key.removeprefix("platforms."): {"url": value["url"], "checksum": value["checksum"]}
            for key, value in lock["tools"]["http:gcloud"][0].items()
            if key.startswith("platforms.")
        }
        self.assertEqual(expected_gcloud, locked_gcloud)
        self.assertNotIn("channels/rapid", (ROOT / "home/dot_mise/config.toml").read_text())
        self.assertNotIn("channels/rapid", (ROOT / "home/dot_mise/mise.lock").read_text())
        for name in ("http:bats", "http:gcloud"):
            self.assertEqual(name, lock["tools"][name][0]["backend"])

    def test_mise_lock_url_entries_have_checksums(self):
        with (ROOT / "home/dot_mise/mise.lock").open("rb") as lock_file:
            lock = tomllib.load(lock_file)
        missing = []
        for name, entries in lock["tools"].items():
            for entry in entries:
                for key, platform in entry.items():
                    if key.startswith("platforms.") and "url" in platform and "checksum" not in platform:
                        missing.append(f"{name}:{key}")
        self.assertEqual([], missing)

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
        self.assertNotIn('type: "git-repo"', text)
        self.assertEqual(3, text.count("  checksum:\n    sha256:"))
        self.assertIn("spacemacs/archive/530c17d62e4ccca09087a2f142752b21000658fb.tar.gz", text)
        self.assertIn("ba040a5d04a6d37c821274eea1f1e4c26d146e2f65057b4d15f4741159071260", text)
        self.assertIn("stripComponents: 1", text)
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
        self.assertIn("spacemacs/archive/530c17d62e4ccca09087a2f142752b21000658fb.tar.gz", result.stdout)
        self.assertIn("ba040a5d04a6d37c821274eea1f1e4c26d146e2f65057b4d15f4741159071260", result.stdout)
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

    def test_nix_inputs_lock_and_ci_use_2605(self):
        flake = (ROOT / "flake.nix").read_text()
        self.assertNotIn("25.05", flake)
        self.assertEqual(3, flake.count("26.05"))
        with (ROOT / "flake.lock").open() as lock_file:
            lock = json.load(lock_file)
        expected_refs = {
            "home-manager": "release-26.05",
            "nix-darwin": "nix-darwin-26.05",
            "nixpkgs": "nixos-26.05",
        }
        actual_refs = {
            name: lock["nodes"][name]["original"]["ref"] for name in expected_refs
        }
        workflow = (ROOT / ".github/workflows/test.yaml").read_text()
        self.assertIn("should_nix:", workflow)
        self.assertIn("nix:", workflow)
        self.assertIn("macos-14", workflow)
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("fail-fast: false", workflow)
        self.assertNotIn("workflow_dispatch:", workflow)
        self.assertEqual(4, workflow.count("--no-update-lock-file"))
        if actual_refs == expected_refs:
            self.assertNotIn("nix flake lock", workflow)
            self.assertNotIn("Upload generated lock", workflow)
            self.assertNotIn("Require committed Nix lock", workflow)
        else:
            self.assertEqual(
                {
                    "home-manager": "release-25.05",
                    "nix-darwin": "nix-darwin-25.05",
                    "nixpkgs": "nixos-25.05",
                },
                actual_refs,
            )
            self.assertIn("nix flake lock", workflow)
            self.assertIn("git status --short -- flake.lock", workflow)
            self.assertIn("Upload generated lock", workflow)
            self.assertIn("Require committed Nix lock", workflow)

    def test_dependabot_owns_github_action_updates(self):
        self.assertFalse((ROOT / ".github/dependabot.yaml").exists())
        config = (ROOT / ".github/dependabot.yml").read_text()
        self.assertIn('package-ecosystem: "github-actions"', config)
        self.assertIn('interval: "weekly"', config)
        self.assertIn('directory: "/"', config)

    def test_setup_ci_rejects_and_preserves_local_drift(self):
        for workflow_name in ("macos.yaml", "ubuntu.yaml"):
            workflow = (ROOT / ".github/workflows" / workflow_name).read_text()
            self.assertIn('before_local_change="$(cksum "${HOME}/.zprofile")"', workflow)
            self.assertIn("if printf ", workflow)
            self.assertIn('after_local_change="$(cksum "${HOME}/.zprofile")"', workflow)
            self.assertIn('[ "${after_local_change}" = "${before_local_change}" ]', workflow)


if __name__ == "__main__":
    unittest.main()
