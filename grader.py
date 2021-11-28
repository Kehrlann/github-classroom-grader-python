# Useful date when copying to other projects:
# 2021-11-28 13:38

import json
import unittest
from unittest.mock import patch
from dataclasses import dataclass
from inspect import cleandoc
from io import StringIO
from pathlib import Path
import sys

SUCCESS = "success"
FAILURE = "failure"
ERROR = "error"


def main(verbose: bool = False) -> None:
    autograding_file = Path.cwd() / ".github" / "classroom" / "autograding.json"
    with open(autograding_file, 'r') as f:
        contents = json.loads(f.read())
        test: dict
        total_score = 0
        max_points = 0
        for test in contents["tests"]:
            result = run_test(test, verbose=verbose)
            total_score += result.points
            max_points += result.max_points
            print(result, "\n", sep="")
        print(f"Total score: {total_score}/{max_points}")


@dataclass()
class TestResult:
    verbose: bool
    command: str
    name: str
    points: int
    max_points: int
    output: str
    status: str
    STATUS_MESSAGES = {
        SUCCESS: "\033[32m SUCCESS \033[0m",
        FAILURE: "\033[31m FAILURE \033[0m",
        ERROR: "\033[31m TEST RAISED ERROR \033[0m"
    }

    @property
    def score(self) -> str:
        return f"{self.points}/{self.max_points}"

    def __repr__(self) -> str:
        result = f"""[{self.name}] - RUNNING ...
            [{self.name}] -{self.STATUS_MESSAGES[self.status]}
            [{self.name}] - Score: {self.score}

            """
        if self.status != SUCCESS:
            result += f"""To get the full error message, run:

            {self.command.replace("python3", "python")}

            """
        result = cleandoc(result)
        if self.status != SUCCESS and self.verbose:
            result += "\n\n"
            result += "Full error message:\n\n"
            result += self.output
        result += "\n\n~~~~~~~~~"
        return result


def run_test(test_def: dict, verbose: bool = False) -> TestResult:
    test_output = StringIO()
    with patch("sys.stdout", new=test_output):
        run = test_def["run"].replace("python3 -m unittest ", "")
        suite = unittest.TestLoader().loadTestsFromName(run)
        result = unittest.TextTestRunner(stream=test_output).run(suite)
        status = SUCCESS
        if result.errors:
            status = ERROR
        elif not result.wasSuccessful():
            status = FAILURE
        return TestResult(
            command=test_def["run"],
            name=test_def["name"],
            points=test_def["points"] if result.wasSuccessful() else 0,
            max_points=test_def["points"],
            output=test_output.getvalue(),
            status=status,
            verbose=verbose
        )


if __name__ == "__main__":
    main(verbose=("-v" in sys.argv))


# TODO:
# - test.run should start with "python3 -m unittest"
