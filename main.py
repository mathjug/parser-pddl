from src.domain import Domain
from pddl import parse_domain

def main():
    parsed_domain = parse_domain("tests/examples/triangle-tire.pddl")
    domain = Domain(parsed_domain)
    actions, _ = domain.get_actions()
    for i, action in enumerate(actions):
            print(action.get_name())
            print(action.get_effects())



if __name__ == "__main__":
    main()