from src.domain import Domain
from src.problem import Problem
from pddl import parse_domain, parse_problem

def main():
    parsed_domain = parse_domain("tests/examples/gripper3.pddl")
    parsed_problem = parse_problem("tests/examples/gripper3_3_balls.pddl")
    print(type(parse_problem))
    domain = Domain(parsed_domain)
    problem = Problem(parsed_problem)
    #actions = domain.get_actions()
    #for i, action in enumerate(actions):
    #    print(action.get_name())
    objects = problem.get_objects()
    for object in objects:
        print(type(object))
        print(object, end=': ')
        for instance in objects[object]:
            print(instance, end=' ')
        print()

if __name__ == "__main__":
    main()