from src import Parser

def main():
    domain_path = "tests/examples/gripper3.pddl"
    problem_path = "tests/examples/gripper3_3_balls.pddl"
    parser = Parser(domain_path, problem_path)
    reachable_actions = parser.get_reachable_actions()
    print(reachable_actions)

if __name__ == "__main__":
    main()