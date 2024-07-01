from src.domain import Domain
from src.problem import Problem
from pddl import parse_domain, parse_problem

def main():
    parsed_domain = parse_domain("tests/examples/triangle-tire.pddl")
    parsed_problem = parse_problem("tests/examples/triangle-tire-1.pddl")
    domain = Domain(parsed_domain)
    problem = Problem(parsed_problem)
    actions = domain.get_actions()
    for i, action in enumerate(actions):
        print(action.get_name())

if __name__ == "__main__":
    main()