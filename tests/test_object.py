import pytest
import pddl
import object

@pytest.mark.parametrize("problem_filename,expected", [
    ("gripper3_2_balls.pddl", {"room": ["rooma","roomb"], "ball" : ["ball1","ball2"]})
    ])
def test_objects_storage(problem_filename, expected):
    problem = pddl.parse_problem(problem_filename)
    assert object.store_objects(problem) == expected


