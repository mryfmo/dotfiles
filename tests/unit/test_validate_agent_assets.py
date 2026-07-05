#!/usr/bin/env python3
"""Exercise focused checks in validate-agent-assets.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts/validate-agent-assets.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_agent_assets", VALIDATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateAgentAssetsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_validator()
        self.old_root = self.module.ROOT
        self.temp_dir = Path(tempfile.mkdtemp(prefix="validate-agent-assets-test-"))
        self.module.ROOT = self.temp_dir
        (self.temp_dir / "home/dot_codex").mkdir(parents=True)

    def tearDown(self) -> None:
        self.module.ROOT = self.old_root
        shutil.rmtree(self.temp_dir)

    def write_codex_config(self, sandbox_workspace_write: str) -> None:
        (self.temp_dir / "home/dot_codex/private_config.toml.tmpl").write_text(
            "\n".join(
                [
                    "#:schema https://developers.openai.com/codex/config-schema.json",
                    'model = "gpt-5.5"',
                    'model_reasoning_effort = "high"',
                    'sandbox_mode = "workspace-write"',
                    "",
                    "[sandbox_workspace_write]",
                    sandbox_workspace_write,
                    "",
                    "[features]",
                    "plugins = true",
                    "hooks = true",
                    "plugin_hooks = true",
                    "",
                    "[shell_environment_policy]",
                    'inherit = "core"',
                    'set = { PATH = "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin" }',
                    "",
                ]
            )
        )

    def write_agmsg_script(self, relative_path: str, executable: bool = True) -> None:
        path = self.temp_dir / "home/dot_agents/skills/agmsg/scripts" / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("#!/bin/sh\n")
        path.chmod(0o755 if executable else 0o644)

    def test_codex_sandbox_workspace_write_must_match_manifest(self) -> None:
        self.write_codex_config("network_access = false")
        manifest = {
            "codex": {
                "model": "gpt-5.5",
                "model_reasoning_effort": "high",
                "sandbox_workspace_write": {
                    "network_access": False,
                    "writable_roots": ["{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db"],
                },
                "shell_environment_policy": {
                    "inherit": "core",
                    "set": {"PATH": "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin"},
                },
                "tui": {},
                "plugins": {},
                "marketplaces": {},
                "hooks": {},
                "projects": {},
            }
        }

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_codex_config(manifest)

    def test_codex_sandbox_workspace_write_accepts_matching_manifest(self) -> None:
        self.write_codex_config(
            'network_access = false\nwritable_roots = ["{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db"]'
        )
        manifest = {
            "codex": {
                "model": "gpt-5.5",
                "model_reasoning_effort": "high",
                "sandbox_workspace_write": {
                    "network_access": False,
                    "writable_roots": ["{{ .chezmoi.homeDir }}/.agents/skills/agmsg/db"],
                },
                "shell_environment_policy": {
                    "inherit": "core",
                    "set": {"PATH": "{{ .chezmoi.homeDir }}/.local/bin:/usr/bin:/bin"},
                },
                "tui": {},
                "plugins": {},
                "marketplaces": {},
                "hooks": {},
                "projects": {},
            }
        }

        self.module.validate_codex_config(manifest)

    def test_agmsg_script_modes_accept_prefixed_entrypoints_and_lib_helpers(self) -> None:
        self.write_agmsg_script("executable_send.sh")
        self.write_agmsg_script("release/executable_sync-version.sh")
        self.write_agmsg_script("lib/storage.sh", executable=False)

        self.module.validate_agmsg_script_modes()

    def test_agmsg_script_modes_reject_unprefixed_direct_entrypoint(self) -> None:
        self.write_agmsg_script("send.sh")

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_agmsg_script_modes()

    def test_agmsg_script_modes_reject_non_executable_prefixed_entrypoint(self) -> None:
        self.write_agmsg_script("executable_send.sh", executable=False)

        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.module.validate_agmsg_script_modes()


if __name__ == "__main__":
    unittest.main()
