import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class FilesFixtureTest(unittest.TestCase):
    def test_fixture_uses_chezmoi_binary_outside_mise_shims(self):
        workflow = (ROOT / ".github/workflows/test.yaml").read_text()
        helpers = (ROOT / "tests/files/helpers.bash").read_text()

        self.assertIn('files_test_chezmoi="$(command -v chezmoi)"', workflow)
        self.assertIn('/*/mise/shims/*|"")', workflow)
        self.assertIn('test -x "${files_test_chezmoi}"', workflow)
        self.assertEqual(2, workflow.count('"${FILES_TEST_CHEZMOI}"'))
        self.assertEqual(1, helpers.count('"${FILES_TEST_CHEZMOI'))
        for name in ("FILES_TEST_SOURCE", "FILES_TEST_CONFIG"):
            self.assertIn(f"{name}=", workflow)
            self.assertIn(f'${{{name}:?{name} is required}}', helpers)
        self.assertIn('--destination "${HOME}"', helpers)
        self.assertNotIn("run chezmoi", helpers)

    def test_coverage_gems_are_compatible_and_exact(self):
        workflow = (ROOT / ".github/workflows/test.yaml").read_text()

        self.assertIn("bashcov --version 3.3.0", workflow)
        self.assertIn("simplecov-cobertura --version 3.1.0", workflow)


if __name__ == "__main__":
    unittest.main()
