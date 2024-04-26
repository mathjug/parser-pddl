import pytest
import pddl
import sys
sys.path.append("../src/")
from domain import store_constants
sys.path.append("../tests/")

@pytest.mark.parametrize("domain_filename,expected", [
    ("./examples/gripper3.pddl", {"gripper": ["left","right"]})
    ])
def test_constants_storage(domain_filename, expected):
    domain = pddl.parse_domain(domain_filename)
    ans = store_constants(domain)
    for key in ans:
        ans[key] = sorted(ans[key])
    assert ans == expected