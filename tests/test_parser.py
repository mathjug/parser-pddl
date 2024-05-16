import pytest
import pddl
import sys
sys.path.append("../src/")
from parser_pddl import Parser
sys.path.append("../tests/")

@pytest.mark.parametrize("filenames,expected", [
    (["./examples/gripper3.pddl","./examples/gripper3_2_balls.pddl"],
    ['at-ball_ball1_rooma', 'at-ball_ball1_roomb', 'at-ball_ball2_rooma', 'at-ball_ball2_roomb', 'at-robby_rooma', 'at-robby_roomb', 'carry_ball1_left', 'carry_ball1_right', 'carry_ball2_left', 'carry_ball2_right', 'free_left', 'free_right', 'whole_ball1', 'whole_ball2']
     )
    ])
def test_prepositions_storage(filenames, expected):
    parser = Parser(filenames[0],filenames[1])
    ans = sorted([ str(i) for i in parser.propositions])
    assert ans == expected

@pytest.mark.parametrize("filenames,expected", [
    (["./examples/gripper3.pddl","./examples/gripper3_2_balls.pddl"],
    ['at-ball_ball1_rooma', 'at-ball_ball2_rooma', 'at-robby_rooma', 'free_left', 'free_right', 'whole_ball1', 'whole_ball2']
     )
    ])
def test_initial_state_storage(filenames, expected):
    parser = Parser(filenames[0],filenames[1])
    initial_state = parser.get_initial_state()
    ans = sorted([str(parser.propositions[i]) for i in range(len(parser.propositions)) if initial_state[i]])
    assert ans==expected

