import pytest
import pddl
from src import Problem

@pytest.mark.parametrize("problem_filename,expected", [
    ("./tests/examples/gripper3_2_balls.pddl", {"room": ["rooma","roomb"], "ball" : ["ball1","ball2"]}),
    ("./tests/examples/triangle-tire-1.pddl", {'location': ['l-1-1', 'l-1-2', 'l-1-3', 'l-2-1', 'l-2-2', 'l-2-3', 'l-3-1', 'l-3-2', 'l-3-3']}),
    ("./tests/examples/triangle-tire-2.pddl", {'location': ['l-1-1', 'l-1-2', 'l-1-3', 'l-1-4', 'l-1-5', 'l-2-1', 'l-2-2', 'l-2-3', 'l-2-4', 'l-2-5', 'l-3-1', 'l-3-2', 'l-3-3', 'l-3-4', 'l-3-5', 'l-4-1', 'l-4-2', 'l-4-3', 'l-4-4', 'l-4-5', 'l-5-1', 'l-5-2', 'l-5-3', 'l-5-4', 'l-5-5']}),
    ("./tests/examples/gripper3_3_balls.pddl", {'room': ['rooma', 'roomb'], 'ball': ['ball1', 'ball2', 'ball3']})
    ])
def test_objects_storage(problem_filename, expected):
    problem = pddl.parse_problem(problem_filename)
    problem = Problem(problem)
    answer = problem.objects
    for key in answer:
        answer[key] = [i.name for i in sorted(answer[key])]

    assert answer == expected


