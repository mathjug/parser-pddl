import pytest
import pddl
from src import Domain

@pytest.mark.parametrize("domain_filename,expected", [
    ("./tests/examples/gripper3.pddl", {"gripper": ["left","right"]}),
    ("./tests/examples/triangle-tire.pddl", {}),
    ("./tests/examples/triangle-tire.pddl", {}),
    ("./tests/examples/gripper3.pddl", {'gripper': ['left', 'right']})
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
    ("./tests/examples/triangle-tire.pddl", {'road': ['location', 'location'], 'vehicle-at': ['location'], 'not-flattire': [], 'spare-in': ['location']}),
    ("./tests/examples/gripper3.pddl", {'free': ['gripper'], 'at-ball': ['ball', 'room'], 'carry': ['ball', 'gripper'], 'at-robby': ['room'], 'whole': ['ball']})
    ])
def test_predicates_storage(domain_filename, expected):
    domain = pddl.parse_domain(domain_filename)
    domain = Domain(domain)
    predicates = domain.predicates
    answer = {}
    for name, predicate in predicates.items():
        answer[predicate.name] = sorted(predicate.variable_types)

    assert answer == expected
