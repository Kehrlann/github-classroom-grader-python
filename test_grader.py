from io import StringIO
from pathlib import Path
import os
from unittest import TestCase
import unittest
from unittest.mock import patch

from grader import main


class TestMultipleTests(TestCase):
    def setUp(self) -> None:
        self.start_dir = Path.cwd()
        os.chdir(Path.cwd() / "fixtures" / "multi_test")

    def tearDown(self) -> None:
        os.chdir(self.start_dir)

    def test_finds_tests_cases(self):
        out = StringIO()
        with patch("sys.stdout", new=out):
            main()

        output: str = out.getvalue()
        self.assertIn("a test that works", output)
        self.assertIn("a test that fails", output)
        self.assertIn("a test that raises", output)

    def test_runs_tests(self):
        out = StringIO()
        with patch("sys.stdout", new=out):
            main()

        output: str = out.getvalue()
        self.assertIn("Score: 1/1", output)
        self.assertIn("Score: 0/2", output)
        self.assertIn("Score: 0/4", output)
        self.assertIn("Total score: 1/7", output)


if __name__ == "__main__":
    unittest.main()
