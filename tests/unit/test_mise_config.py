import re
import tomllib
import unittest
from pathlib import Path


class MiseConfigTest(unittest.TestCase):
    def test_python_is_exact_version(self):
        path = Path(__file__).resolve().parents[2] / "home/dot_mise/config.toml"
        value = tomllib.loads(path.read_text())["tools"]["python"]
        self.assertIsNotNone(re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value, re.ASCII))
        for value in ("3.15.0\n", "３.15.0", "latest", "3.15"):
            with self.subTest(value=value):
                self.assertIsNone(re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value, re.ASCII))


if __name__ == "__main__":
    unittest.main()
