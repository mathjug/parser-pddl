import pytest
import pddl
import sys
sys.path.append("../src/")
from domain import Domain
sys.path.append("../tests/")

@pytest.mark.parametrize("domain_filename,expected", [
    ("./examples/gripper3.pddl", {"gripper": ["left","right"]})
    ])
def test_constants_storage(domain_filename, expected):
    domain = Domain(domain_filename)
    answer = domain.constants
    for key in answer:
        answer[key] = [i.name for i in sorted(answer[key])]
    
    assert answer == expected

@pytest.mark.parametrize("domain_filename,expected", [
    ("./examples/gripper3.pddl", {"at-robby": ["room"],"at-ball": ["ball", "room"], "free": ["gripper"], "carry": ["ball", "gripper"], "whole": ["ball"],})
    ])
def test_predicates_storage(domain_filename, expected):
    domain = Domain(domain_filename)
    predicates = domain.predicates
    answer = {}
    for item in predicates:
        answer[item.name] = sorted(item.variable_types)

    assert answer == expected
