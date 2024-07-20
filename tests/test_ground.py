import pytest
from src import Parser

@pytest.mark.parametrize("domain_filename, problem_filename, expected", [
    ("tests/examples/gripper3.pddl", "tests/examples/gripper3_3_balls.pddl", 
     ['ball1', 'ball1', 'ball1', 'ball1', 'ball1', 'ball1', 'ball1', 'ball1', 'ball2', 'ball2', 'ball2', 'ball2', 'ball2', 'ball2', 'ball2', 'ball2', 'ball3', 'ball3', 'ball3', 'ball3', 'ball3', 'ball3', 'ball3', 'ball3', 'drop', 'drop', 'drop', 'drop', 'drop', 'drop', 'drop', 'drop', 'drop', 'drop', 'drop', 'drop', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'move', 'move', 'pick', 'pick', 'pick', 'pick', 'pick', 'pick', 'pick', 'pick', 'pick', 'pick', 'pick', 'pick', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'rooma', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb', 'roomb']),
    ])
def test_ground(domain_filename, problem_filename, expected):
    domain_path = domain_filename
    problem_path = problem_filename
    parser = Parser(domain_path, problem_path)
    reachable_actions = parser.get_reachable_actions()

    actions = []
    for action in reachable_actions:
        actions.append(str(action[0]))
        for object in action[1]:
            actions.append(str(object))
    
    actions.sort()
    assert actions == expected
