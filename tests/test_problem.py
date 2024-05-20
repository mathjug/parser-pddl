import pytest
import pddl
from src.problem import Problem

@pytest.mark.parametrize("problem_filename,expected", [
    ("./tests/examples/gripper3_2_balls.pddl", {"room": ["rooma","roomb"], "ball" : ["ball1","ball2"]})
    ])
def test_objects_storage(problem_filename, expected):
    problem = pddl.parse_problem(problem_filename)
    problem = Problem(problem)
    answer = problem.objects
    for key in answer:
        answer[key] = [i.name for i in sorted(answer[key])]

    assert answer == expected


