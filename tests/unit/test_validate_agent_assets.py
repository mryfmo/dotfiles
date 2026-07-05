#!/usr/bin/env python3
"""Exercise focused checks in validate-agent-assets.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import tempfile
import textwrap
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
            textwrap.dedent(
                f"""\
                #:schema https://developers.openai.com/codex/config-schema.json
                model = "gpt-5.5"
                model_reasoning_effort = "high"
                sandbox_mode = "workspace-write"

                [sandbox_workspace_write]
                {sandbox_workspace_write}

                [features]
                plugins = true
                hooks = true
                plugin_hooks = true

                [shell_environment_policy]
                inherit = "core"
                set = {{ PATH = "{{{{ .chezmoi.homeDir }}}}/.local/bin:/usr/bin:/bin" }}
                """
            )
        )

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


if __name__ == "__main__":
    unittest.main()
