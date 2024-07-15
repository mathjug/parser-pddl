import pytest
import pddl
from src import Domain

@pytest.mark.parametrize("domain_filename,expected", [
    ("./tests/examples/gripper3.pddl", {"gripper": ["left","right"]}),
    ("./tests/examples/triangle-tire.pddl", {}),
    ])
def test_constants_storage(domain_filename, expected):
    domain = pddl.parse_domain(domain_filename)
    domain = Domain(domain)
    answer = domain.constants
    for key in answer:
        answer[key] = [i.name for i in sorted(answer[key])]

    assert answer == expected

@pytest.mark.parametrize("domain_filename,expected", [
    ("./tests/examples/gripper3.pddl", {"at-robby": ["room"],"at-ball": ["ball", "room"], "free": ["gripper"], "carry": ["ball", "gripper"], "whole": ["ball"],}),
    ("./tests/examples/triangle-tire.pddl", {'vehicle-at': ['location'], 'not-flattire': [], 'road': ['location', 'location'], 'spare-in': ['location']}),
    ])
def test_predicates_storage(domain_filename, expected):
    domain = pddl.parse_domain(domain_filename)
    domain = Domain(domain)
    predicates = domain.predicates
    answer = {}
    for name, predicate in predicates.items():
        answer[predicate.name] = sorted(predicate.variable_types)

    assert answer == expected

@pytest.mark.parametrize("domain_filename,expected", [
    ("./tests/examples/gripper3.pddl", ["drop","move","pick"]),
    ("./tests/examples/triangle-tire.pddl", ["changetire","move-car"]),
    ])
def test_actions_storage(domain_filename, expected):
    domain = pddl.parse_domain(domain_filename)
    domain = Domain(domain)
    actions = domain.actions
    answer = []
    for action in actions:
        answer.append(action.name)
    answer.sort()
    assert answer == expected


@pytest.mark.parametrize("domain_filename,expected", [
    ("./tests/examples/gripper3.pddl", {"move" : ['from', 'to'],"pick" : ['gripper', 'obj', 'room'],"drop" : ['gripper', 'obj', 'room']}),
    ("./tests/examples/triangle-tire.pddl", {"move-car" : ['from', 'to'], "changetire" : ['loc'] }),
    ])
def test_actions_parameters(domain_filename, expected):
    domain = pddl.parse_domain(domain_filename)
    domain = Domain(domain)
    actions = domain.actions
    answer = {}
    for action in actions:
        answer[action.name] = sorted([obj.name for obj in action.parameters])
    assert answer == expected


@pytest.mark.parametrize("domain_filename,expected", [
    ("./tests/examples/gripper3.pddl", {'pick': [('at-ball_obj_room', 'True'), ('at-robby_room', 'True'), ('free_gripper', 'True'), ('whole_obj', 'True')], 'drop': [('at-robby_room', 'True'), ('carry_obj_gripper', 'True')], 'move': [('at-robby_from', 'True')]}),
    ("./tests/examples/triangle-tire.pddl", {'changetire': [('spare-in_loc', 'True'), ('vehicle-at_loc', 'True')], 'move-car': [('not-flattire', 'True'), ('road_from_to', 'True'), ('vehicle-at_from', 'True')]}),
    ])
def test_actions_preconditions(domain_filename, expected):
    domain = pddl.parse_domain(domain_filename)
    domain = Domain(domain)
    actions = domain.get_actions()
    answer = {}
    for action in actions:
        answer[action.name] = sorted([(str(obj[0]), str(obj[1])) for obj in action.preconditions])
    assert answer == expected



@pytest.mark.parametrize("domain_filename,expected", [
    ("./tests/examples/gripper3.pddl", {'drop': [[('at-ball_obj_room', 'True'), ('carry_obj_gripper', 'False'), ('free_gripper', 'True')]], 'pick': [[('at-ball_obj_room', 'False'), ('carry_obj_gripper', 'True'), ('free_gripper', 'False')], [('whole_obj', 'False')]], 'move': [[('at-robby_from', 'False'), ('at-robby_to', 'True')]]}),
    ("./tests/examples/triangle-tire.pddl", {'move-car': [[('not-flattire', 'False'), ('vehicle-at_from', 'False'), ('vehicle-at_to', 'True')], [('vehicle-at_from', 'False'), ('vehicle-at_to', 'True')]], 'changetire': [[('not-flattire', 'True'), ('spare-in_loc', 'False')]]}),
    ])
def test_actions_effects(domain_filename, expected):
    domain = pddl.parse_domain(domain_filename)
    domain = Domain(domain)
    actions = domain.get_actions()
    answer = {}
    for action in actions:
        ans_effects = []
        for effect in action.effects:
            ans_effects.append(sorted([(str(obj[0]), str(obj[1])) for obj in effect])) 
        answer[action.name] = sorted(ans_effects)
    assert answer == expected