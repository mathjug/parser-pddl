import pytest
import pddl
import sys
sys.path.append("../")
import object

@pytest.mark.parametrize("problem_filename,expected", [
    ("gripper3_2_balls.pddl", {"room": ["rooma","roomb"], "ball" : ["ball1","ball2"]})
    ])
def test_objects_storage(problem_filename, expected):
    problem = pddl.parse_problem(problem_filename)
    ans = object.store_objects(problem)
    for key in ans:
        ans[key] = sorted(ans[key])
    assert ans == expected


