import json
import os
import re
import shutil
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
            "install/common/mise.sh": r"""
uname() { [ "$1" = -s ] && printf Linux || printf x86_64; }
curl() {
    local output
    while [ "$#" -gt 0 ]; do
        if [ "$1" = -o ]; then output="$2"; shift 2; else shift; fi
    done
    printf payload > "${output}"
}
verify_mise_archive() { :; }
# The fake downloads are not signed; the GPG path is taken on every host, its check stubbed.
mise_gpg_ready() { return 0; }
verify_mise_shasums_signature() { :; }
github_release_tag() { printf 'v2026.10.3\n'; }
github_release_attestation() { return 2; }
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
""",
            "install/common/sheldon.sh": r"""
mkdir -p "${HOME}/.local/bin"
cat > "${HOME}/.local/bin/mise" <<'EOF'
#!/bin/sh
[ "$1" = exec ] && [ "$2" = -- ] && [ "$3" = cargo ] || exit 98
    mkdir -p "${CARGO_INSTALL_ROOT}/bin"
    printf '#!/bin/sh\n' > "${CARGO_INSTALL_ROOT}/bin/sheldon"
    chmod +x "${CARGO_INSTALL_ROOT}/bin/sheldon"
EOF
chmod +x "${HOME}/.local/bin/mise"
cargo() { return 99; }
install() { cp "$3" "$4"; chmod 0755 "$4"; }
mv() { command mv "$@"; }
install_sheldon
""",
            "install/ubuntu/server/starship.sh": r"""
# The fakes below hash every download to "checksum", so that is the reviewed sha256 here too.
starship_artifact() { printf 'starship-x86_64-unknown-linux-musl.tar.gz checksum\n'; }
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
""",
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
            "install/common/mise.sh": (
                "github_release_tag() { printf 'v1\\n'; }; mise_artifact() { return 42; }",
                "install_mise",
            ),
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
                    [
                        "bash",
                        "-c",
                        f'source "$1"\nset +e\n{mock}\n{function}\n[ "$?" -eq 42 ]\n',
                        "_",
                        str(ROOT / relative),
                    ],
                    env={**os.environ, "HOME": str(root / "home"), "TMPDIR": str(root / "tmp")},
                    check=False,
                )
                self.assertEqual(0, result.returncode)
                self.assertEqual([], list((root / "tmp").iterdir()))

    def run_with_tmpdir(self, script, relative, home, **env):
        """Run main of an installer with HOME and a mktemp that honours TMPDIR (macOS mktemp -d does not)."""
        tmp = home / "tmp"
        shim = home / "shim"
        tmp.mkdir(parents=True, exist_ok=True)
        shim.mkdir(parents=True, exist_ok=True)
        (shim / "mktemp").write_text(
            '#!/bin/sh\nif [ "$*" = -d ]; then exec /usr/bin/mktemp -d "$TMPDIR/tmp.XXXXXX"; fi\nexec /usr/bin/mktemp "$@"\n'
        )
        (shim / "mktemp").chmod(0o755)
        if shutil.which("sha256sum") is None:
            # The Ubuntu installers call sha256sum; a macOS runner has only shasum.
            (shim / "sha256sum").write_text('#!/bin/sh\nexec shasum -a 256 "$@"\n')
            (shim / "sha256sum").chmod(0o755)
        return subprocess.run(
            ["bash", "-c", f'source "$1"\n{script}', "_", str(ROOT / relative)],
            env={**os.environ, "HOME": str(home), "TMPDIR": str(tmp), "PATH": f"{shim}:{os.environ['PATH']}", **env},
            check=False,
            text=True,
            capture_output=True,
        )

    def test_a_failed_download_keeps_a_working_tool_and_a_failed_check_never_does(self):
        # The Zed rule: acquisition failure with a working install warns and exits 0; with none it fails;
        # a verification failure always fails and installs nothing.
        starship_curl = r"""
uname() { printf 'x86_64\n'; }
curl() {
    local output=""
    [ -z "${DOWNLOAD_FAIL:-}" ] || return 22
    while [ "$#" -gt 0 ]; do if [ "$1" = -o ]; then output="$2"; shift 2; else shift; fi; done
    if [ -n "${output}" ]; then printf archive > "${output}"; else printf '%064d\n' 0; fi
}
main
"""
        sheldon_lookup = 'sheldon_newest_version() { printf "9.9.9\\n"; }\nmain\n'
        sheldon_mise = (
            "#!/bin/sh\n"
            '[ "$1 $2 $3 $4" = "exec -- cargo install" ] || exit 98\n'
            'if [ -n "${CHECKSUM_FAIL:-}" ]; then\n'
            "  printf 'error: failed to download replaced source registry `crates-io`\\n\\nCaused by:\\n  failed to verify the checksum of `sheldon v9.9.9`\\n' >&2\n"
            "else\n"
            "  printf 'error: failed to download from `https://static.crates.io/api/v1/crates/sheldon/9.9.9/download`\\n\\nCaused by:\\n  [6] Could not resolve host: static.crates.io\\n' >&2\n"
            "fi\n"
            "exit 101\n"
        )
        for tool, relative, script, banner, cases in (
            (
                "starship",
                "install/ubuntu/server/starship.sh",
                starship_curl,
                "printf 'starship 1.25.0\\n'",
                (
                    (
                        "download fails, older starship installed",
                        True,
                        {"DOWNLOAD_FAIL": "1"},
                        0,
                        "warning: could not download Starship v1.26.0; Starship 1.25.0 stays.",
                    ),
                    ("download fails, nothing installed", False, {"DOWNLOAD_FAIL": "1"}, 3, ""),
                    ("checksum mismatch, older starship installed", True, {}, 1, "Checksum mismatch"),
                ),
            ),
            (
                "sheldon",
                "install/common/sheldon.sh",
                sheldon_lookup,
                "printf 'sheldon 0.8.5\\n'",
                (
                    (
                        "download fails, older sheldon installed",
                        True,
                        {},
                        0,
                        "warning: could not download the sheldon 9.9.9 crate; sheldon 0.8.5 stays.",
                    ),
                    ("download fails, nothing installed", False, {}, 3, ""),
                    (
                        "checksum fails, older sheldon installed",
                        True,
                        {"CHECKSUM_FAIL": "1"},
                        101,
                        "failed to verify the checksum",
                    ),
                ),
            ),
        ):
            for name, installed, env, expected_status, message in cases:
                with self.subTest(tool=tool, case=name), tempfile.TemporaryDirectory() as directory:
                    home = Path(directory)
                    (home / ".local/bin").mkdir(parents=True)
                    if tool == "sheldon":
                        (home / ".local/bin/mise").write_text(sheldon_mise)
                        (home / ".local/bin/mise").chmod(0o755)
                    binary = home / ".local/bin" / tool
                    if installed:
                        binary.write_text(f"#!/bin/sh\n{banner}\n")
                        binary.chmod(0o755)
                    before = binary.read_bytes() if installed else None

                    result = self.run_with_tmpdir(script, relative, home, **env)

                    self.assertEqual(expected_status, result.returncode, result.stderr)
                    self.assertIn(message, result.stderr)
                    self.assertEqual(before, binary.read_bytes() if binary.exists() else None)

    def test_every_apply_installers_skip_when_current_and_keep_the_tool_offline(self):
        # starship and sheldon run on every chezmoi apply (run_after_*) and install only when not current:
        # starship against its pin (v1.26.0 in assets.starship), sheldon against the newest crate.
        starship = (
            "install/ubuntu/server/starship.sh",
            "starship",
            ":",
            'install_starship() { touch "${HOME}/install-ran"; }',
        )
        sheldon = (
            "install/common/sheldon.sh",
            "sheldon",
            'sheldon_newest_version() { [ -z "${LOOKUP_FAIL:-}" ] || return 1; printf \'%s\\n\' "${NEWEST}"; }',
            'install_sheldon() { touch "${HOME}/install-ran"; }',
        )
        # The installed binary's script (None: not installed); a non-zero exit is broken whatever it printed.
        for (relative, tool, lookup, install), name, binary_body, newest, lookup_fail, expect_install in (
            (starship, "pinned release installed", "printf 'starship 1.26.0\\nbranch:\\n'", "", "", False),
            (starship, "older release (a pin bump)", "printf 'starship 1.25.0\\n'", "", "", True),
            (starship, "not installed", None, "", "", True),
            (starship, "pinned banner, exits 42", "printf 'starship 1.26.0\\n'\nexit 42", "", "", True),
            (sheldon, "current", "printf 'sheldon 0.8.5\\n'", "0.8.5", "", False),
            (sheldon, "newer release", "printf 'sheldon 0.8.5\\n'", "9.9.9", "", True),
            (sheldon, "not installed", None, "0.8.5", "", True),
            (sheldon, "lookup fails, installed", "printf 'sheldon 0.8.5\\n'", "", "1", False),
            (sheldon, "current banner, exits 42", "printf 'sheldon 0.8.5\\n'\nexit 42", "0.8.5", "", True),
        ):
            with self.subTest(relative=relative, case=name), tempfile.TemporaryDirectory() as directory:
                home = Path(directory)
                if binary_body is not None:
                    binary = home / ".local/bin" / tool
                    binary.parent.mkdir(parents=True)
                    binary.write_text(f"#!/bin/sh\n{binary_body}\n")
                    binary.chmod(0o755)
                result = subprocess.run(
                    ["bash", "-c", f'source "$1"\n{lookup}\n{install}\nmain', "_", str(ROOT / relative)],
                    env={**os.environ, "HOME": str(home), "NEWEST": newest, "LOOKUP_FAIL": lookup_fail},
                    check=False,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(expect_install, (home / "install-ran").exists())
                if lookup_fail:
                    self.assertIn("stays", result.stderr)
        for wrapper in (
            "home/.chezmoiscripts/ubuntu/run_after_10-install-starship.sh.tmpl",
            "home/.chezmoiscripts/common/run_after_03-install-sheldon.sh.tmpl",
            "home/.chezmoiscripts/ubuntu/run_after_04-install-aws-cli.sh.tmpl",
            "home/.chezmoiscripts/ubuntu/run_after_05-client-install-zed.sh.tmpl",
        ):
            self.assertTrue((ROOT / wrapper).is_file(), wrapper)

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
            line for path in paths for line in path.read_text().splitlines() if not line.lstrip().startswith("#")
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

    def test_mise_tools_track_latest_behind_the_cooldown(self):
        text = (ROOT / "home/dot_mise/config.toml").read_text()
        config = tomllib.loads(text)
        settings = config["settings"]
        for retired in ("lockfile", "locked", "lockfile_platforms"):
            self.assertNotIn(retired, settings)
        self.assertEqual("72h", settings["minimum_release_age"])
        self.assertEqual("72h", settings["self_update"]["minimum_release_age"])
        # npm's own age gate must equal mise's cooldown, or npm refuses the release mise chose.
        hours = int(settings["minimum_release_age"].removesuffix("h"))
        self.assertEqual(0, hours % 24)
        npmrc = (ROOT / "home/dot_npmrc").read_text().splitlines()
        self.assertIn(f"min-release-age={hours // 24}", npmrc)
        for script in ("scripts/upgrade-tools.sh", "install/common/mise.sh"):
            self.assertNotIn("npm_config_min_release_age=", (ROOT / script).read_text(), script)
        self.assertFalse((ROOT / "home/dot_mise/mise.lock").exists())
        self.assertFalse((ROOT / "home/dot_config/mise/mise.lock.tmpl").exists())
        self.assertIn(".config/mise/mise.lock", (ROOT / "home/.chezmoiremove").read_text().splitlines())

        lines = text.splitlines()
        held = {"fd": "fd = ", "npm:pnpm": '"npm:pnpm" = ', "http:bats": '[tools."http:bats"]'}
        held["http:gcloud"] = '[tools."http:gcloud"]'
        for name, request in config["tools"].items():
            version = request if isinstance(request, str) else request["version"]
            if name not in held:
                self.assertEqual("latest", version, name)
                continue
            self.assertRegex(version, r"^\d+(\.\d+)+$", name)
            line = next(index for index, line in enumerate(lines) if line.startswith(held[name]))
            self.assertTrue(lines[line - 1].startswith("# "), f"{name} needs a one-line reason above it")
        self.assertEqual(set(held), {name for name in config["tools"] if name in held})

        self.assertFalse((ROOT / "home/dot_config/mise/symlink_config.toml.tmpl").exists())
        template = ROOT / "home/dot_config/mise/config.toml.tmpl"
        with tempfile.TemporaryDirectory() as temporary:
            chezmoi_config = Path(temporary) / "chezmoi.toml"
            chezmoi_config.write_text("")
            result = subprocess.run(
                [
                    "chezmoi",
                    "--config",
                    str(chezmoi_config),
                    "--source",
                    str(ROOT / "home"),
                    "execute-template",
                    template.read_text(),
                ],
                check=True,
                capture_output=True,
            )
        self.assertEqual(result.stdout, text.encode())

    def test_lifecycle_runs_the_upgrade_through_make_update_without_locked_installs(self):
        for relative in ("install/common/mise.sh", "Makefile", "scripts/update-agent-assets.sh"):
            self.assertNotIn("--locked", (ROOT / relative).read_text(), relative)
        makefile = (ROOT / "Makefile").read_text()
        self.assertNotRegex(makefile, r"(?m)^upgrade:")
        # The pull runs alone, then a second make reads the Makefile it fetched.
        update = makefile.split("\nupdate:\n", 1)[1].split("\n.PHONY:", 1)[0]
        self.assertTrue(update.rstrip("\n").endswith("\t@$(MAKE) --no-print-directory update-tree"), update)
        self.assertLess(update.index("git pull --ff-only"), update.index("update-tree"))
        self.assertNotIn("chezmoi apply", update)
        tree = makefile.split("\nupdate-tree:\n", 1)[1].split("\n.PHONY:", 1)[0]
        upgrade = tree.index("\t./scripts/upgrade-tools.sh $(if $(filter 1 true yes,$(SYSTEM)),--system,)\n")
        self.assertLess(tree.index("\tchezmoi apply --verbose\n"), upgrade)
        self.assertLess(upgrade, tree.index("\t./scripts/update-agent-assets.sh\n"))
        self.assertIn("\t$(MAKE) agmsg-bootstrap", tree)

    def test_mise_apply_replaces_live_symlinks_with_independent_copies(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            source = fixture / "source"
            destination = fixture / "home"
            managed = source / "dot_config/mise"
            applied = destination / ".config/mise"
            pins = source / "dot_mise"
            for directory in (managed, applied, pins):
                directory.mkdir(parents=True)
            name = "config.toml"
            (pins / name).write_bytes((ROOT / f"home/dot_mise/{name}").read_bytes())
            (managed / f"{name}.tmpl").write_text((ROOT / f"home/dot_config/mise/{name}.tmpl").read_text())
            (applied / name).symlink_to(pins / name)
            config = fixture / "chezmoi.toml"
            config.write_text("")
            subprocess.run(
                [
                    "chezmoi",
                    "--config",
                    str(config),
                    "--source",
                    str(source),
                    "--destination",
                    str(destination),
                    "--persistent-state",
                    str(fixture / "state.boltdb"),
                    "apply",
                    "--force",
                ],
                check=True,
                capture_output=True,
            )
            self.assertFalse((applied / name).is_symlink())
            self.assertEqual((applied / name).read_bytes(), (pins / name).read_bytes())
            (applied / name).write_text("runtime-only change\n")
            self.assertEqual((pins / name).read_bytes(), (ROOT / f"home/dot_mise/{name}").read_bytes())

    def test_mise_npm_backend_uses_npm_and_limits_lifecycle_scripts(self):
        with (ROOT / "home/dot_mise/config.toml").open("rb") as config_file:
            config = tomllib.load(config_file)

        self.assertEqual("npm", config["settings"]["npm"]["package_manager"])
        # Claude Code comes from Anthropic's signed native distribution (ensure_claude_code), not npm.
        self.assertNotIn("npm:@anthropic-ai/claude-code", config["tools"])
        codex = config["tools"]["npm:@openai/codex"]
        self.assertNotIn("allow_builds", codex)

    def test_codex_alone_takes_releases_on_day_one_and_npm_provenance_is_checked(self):
        with (ROOT / "home/dot_mise/config.toml").open("rb") as config_file:
            config = tomllib.load(config_file)
        # Day one needs both cooldowns lifted for Codex only: mise's through the excludes list and npm's
        # (~/.npmrc, which the npm package manager reads) through Codex's own install_env.
        self.assertEqual(["npm:@openai/codex"], config["settings"]["minimum_release_age_excludes"])
        overrides = {
            name: request["install_env"]
            for name, request in config["tools"].items()
            if isinstance(request, dict) and "install_env" in request
        }
        self.assertEqual({"npm:@openai/codex": {"npm_config_min_release_age": "0"}}, overrides)

        upgrade = (ROOT / "scripts/upgrade-tools.sh").read_text()
        main = upgrade.split("\nfunction main() {\n", 1)[1]
        self.assertLess(
            main.index('run_required_phase "mise inventory/install/upgrade" upgrade_mise_tools'),
            main.index('run_required_phase "npm provenance" verify_npm_provenance'),
        )
        self.assertIn("npm audit signatures --include-attestations", upgrade)
        self.assertIn("npm install --ignore-scripts", upgrade)
        # The audit's scratch install lifts npm's window only for a tool mise's excludes list names.
        self.assertEqual(1, upgrade.count("--min-release-age=0"))
        check = upgrade.split("\nfunction check_npm_tool_provenance() {\n", 1)[1].split("\n}\n", 1)[0]
        self.assertIn('*"\\"${mise_tool}\\""*) window="--min-release-age=0" ;;', check)

    def test_mise_config_backends_and_http_tools(self):
        with (ROOT / "home/dot_mise/config.toml").open("rb") as config_file:
            config = tomllib.load(config_file)
        self.assertEqual("latest", config["tools"]["cargo:eza"])
        self.assertFalse(config["settings"]["cargo"]["binstall"])

        bats = config["tools"]["http:bats"]
        self.assertEqual("bin", bats["bin_path"])
        self.assertEqual(1, bats["strip_components"])
        self.assertRegex(bats["checksum"], r"^sha256:[0-9a-f]{64}$")
        self.assertIn(f"/v{bats['version']}.tar.gz", bats["url"])
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
        self.assertNotIn("channels/rapid", (ROOT / "home/dot_mise/config.toml").read_text())
        # The bootstrap takes the newest cooled-down mise release instead of a pin;
        # test_rolling_installers_resolve_through_the_release_helper covers it.
        self.assertNotIn("MISE_VERSION=", (ROOT / "install/common/mise.sh").read_text())

    def test_rolling_installers_resolve_through_the_release_helper(self):
        # Each rolling GitHub-release installer names its repository once and resolves the
        # newest release at least 72 hours old; none carries a version constant.
        for path, repo_line, call, prefix in (
            (
                "install/common/mise.sh",
                'readonly MISE_RELEASE_REPO="jdx/mise"',
                'github_release_tag "${MISE_RELEASE_REPO}"',
                "MISE",
            ),
            (
                "install/ubuntu/client/zed.sh",
                'readonly ZED_RELEASE_REPO="zed-industries/zed"',
                'github_release_tag "${ZED_RELEASE_REPO}"',
                "ZED",
            ),
            (
                "setup.sh",
                'readonly CHEZMOI_RELEASE_REPO="twpayne/chezmoi"',
                'github_release_tag "${CHEZMOI_RELEASE_REPO}"',
                "CHEZMOI",
            ),
        ):
            with self.subTest(path=path):
                text = (ROOT / path).read_text()
                self.assertIn(repo_line, text)
                self.assertIn(call, text)
                # The only version a rolling installer carries is its reviewed fallback (Amendment 8), rendered.
                versions = re.findall(rf'(?m)^(?:readonly |declare -r )?({prefix}[A-Z_]*_VERSION)="v?[0-9]', text)
                self.assertEqual([f"{prefix}_FALLBACK_VERSION"] if prefix in ("MISE", "CHEZMOI") else [], versions)
        self.assertIn("GITHUB_RELEASE_MIN_AGE_HOURS=72\n", (ROOT / "scripts/lib/github-release.sh").read_text())
        config = tomllib.loads((ROOT / "home/dot_mise/config.toml").read_text())
        self.assertEqual("72h", config["settings"]["minimum_release_age"])
        installer_pins = (ROOT / "scripts/lib/installer-pins.sh").read_text()
        for retired in ("CHEZMOI_BOOTSTRAP_PIN_VERSION", "ZED_PIN_VERSION"):
            self.assertNotIn(retired, installer_pins)
        # Crit and starship have mutable releases with only same-release checksums: reviewed pins (Amendment 7).
        self.assertRegex(installer_pins, r'(?m)^CRIT_PIN_VERSION="v[0-9]')
        self.assertRegex(
            (ROOT / "install/ubuntu/server/starship.sh").read_text(), r'(?m)^readonly STARSHIP_PIN_VERSION="v[0-9]'
        )

    def test_sheldon_uses_locked_crates_io_source(self):
        script = (ROOT / "install/common/sheldon.sh").read_text()
        for token in (
            "cargo install",
            "--locked --features vendored --registry crates-io sheldon",
        ):
            self.assertIn(token, script)
        # cargo takes the newest crate and checks it against the registry index.
        self.assertNotIn('--version "=', script)
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
        self.assertEqual(5, text.count("  checksum:\n    sha256:"))
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
                "  checksum:\n"
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

    def test_renovate_owns_dependency_update_notifications(self):
        for name in ("dependabot.yml", "dependabot.yaml"):
            self.assertFalse((ROOT / ".github" / name).exists())
        config = json.loads((ROOT / "renovate.json").read_text())
        self.assertEqual({"github-actions", "mise", "custom.regex"}, set(config["enabledManagers"]))
        self.assertTrue(
            any(
                re.search(pattern.strip("/"), "home/dot_mise/config.toml")
                for pattern in config["mise"]["managerFilePatterns"]
            )
        )
        manifest_rules = [rule for rule in config["packageRules"] if "custom.regex" in rule.get("matchManagers", [])]
        self.assertEqual(1, len(manifest_rules))
        self.assertIs(True, manifest_rules[0]["dependencyDashboardApproval"])
        self.assertNotIn("automerge", json.dumps(config))
        # No mise.lock is left to regenerate, so no mise rule waits on lock fidelity; fd stays held like config.toml.
        mise_rules = [rule for rule in config["packageRules"] if rule.get("matchManagers") == ["mise"]]
        self.assertFalse([rule for rule in mise_rules if "mise.lock" in rule.get("description", "")])
        self.assertTrue(
            any(rule.get("matchDepNames") == ["fd"] and rule.get("enabled") is False for rule in mise_rules)
        )
        # The held npm:pnpm must not come back through a Renovate PR either.
        self.assertTrue(
            any(rule.get("matchDepNames") == ["npm:pnpm"] and rule.get("enabled") is False for rule in mise_rules)
        )

    def test_setup_ci_rejects_and_preserves_local_drift(self):
        for workflow_name in ("macos.yaml", "ubuntu.yaml"):
            workflow = (ROOT / ".github/workflows" / workflow_name).read_text()
            self.assertIn('before_local_change="$(cksum "${HOME}/.zprofile")"', workflow)
            self.assertIn("if printf ", workflow)
            self.assertIn('after_local_change="$(cksum "${HOME}/.zprofile")"', workflow)
            self.assertIn('[ "${after_local_change}" = "${before_local_change}" ]', workflow)


if __name__ == "__main__":
    unittest.main()
