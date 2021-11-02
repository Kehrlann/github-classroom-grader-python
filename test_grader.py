import os
import unittest
from inspect import cleandoc
from io import StringIO
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from grader import main, run_test


class TestOutput(TestCase):
    def test_successful_output(self):
        actual = run_test({
            "name": "a successful test",
            "points": 1,
            "run": "python3 -m unittest fixtures.test_sample.TestSample.test_works"
        })

        expected = cleandoc(""" [a successful test] - RUNNING ...
                                [a successful test] - SUCCESS 👍
                                [a successful test] - Score: 1/1

                                ~~~~~~~~~""")

        self.assertEqual(expected, str(actual))




class TestMultipleTests(TestCase):
    SUCCESSFUL_OUTPUT = cleandoc("""[a test that works] - RUNNING ...
        [a test that works] - SUCCESS 👍
        [a test that works] - Score: 1/1

        ~~~~~~~~~""")

    FAILED_OUTPUT = cleandoc("""[a test that fails] - RUNNING ...
        [a test that fails] - FAILURE 😱
        [a test that fails] - Score: 0/2

        ~~~~~~~~~""")

    ERRORING_OUTPUT = cleandoc("""[a test that raises] - RUNNING ...
        [a test that raises] - TEST RAISED ERROR 💥
        [a test that raises] - Score: 0/4

        ~~~~~~~~~""")

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

    def test_full_output(self):
        out = StringIO()
        with patch("sys.stdout", new=out):
            main()

        output: str = out.getvalue()
        expected = f"""{TestMultipleTests.SUCCESSFUL_OUTPUT}

{TestMultipleTests.FAILED_OUTPUT}

{TestMultipleTests.ERRORING_OUTPUT}

Total score: 1/7
"""
        self.assertEqual(expected, output)


if __name__ == "__main__":
    unittest.main()
