import json
import unittest
from dataclasses import dataclass
from inspect import cleandoc
from io import StringIO
from pathlib import Path


def main() -> None:
    autograding_file = Path.cwd() / ".github" / "classroom" / "autograding.json"
    with open(autograding_file, 'r') as f:
        contents = json.loads(f.read())
        test: dict
        total_score = 0
        max_points = 0
        for test in contents["tests"]:
            result = run_test(test)
            total_score += result.points
            max_points += result.max_points
            print(result, "\n", sep="")
        print(f"Total score: {total_score}/{max_points}")


@dataclass()
class TestResult:
    name: str
    points: int
    max_points: int
    output: str
    status: str

    @property
    def score(self) -> str:
        return f"{self.points}/{self.max_points}"

    def __repr__(self) -> str:
        return cleandoc(f"""[{self.name}] - RUNNING ...
            [{self.name}] - {self.status}
            [{self.name}] - Score: {self.score}

            ~~~~~~~~~""")


def run_test(test_def: dict) -> TestResult:
    run = test_def["run"].replace("python3 -m unittest ", "")
    suite = unittest.TestLoader().loadTestsFromName(run)
    test_output = StringIO()
    result = unittest.TextTestRunner(stream=test_output).run(suite)
    status = "SUCCESS 👍"
    if result.errors:
        status = "TEST RAISED ERROR 💥"
    elif not result.wasSuccessful():
        status = "FAILURE 😱"
    return TestResult(
        name=test_def["name"],
        points=test_def["points"] if result.wasSuccessful() else 0,
        max_points=test_def["points"],
        output=test_output.getvalue(),
        status=status
    )


if __name__ == "__main__":
    main()


# TODO:
# - test.run should start with "python3 -m unittest"
