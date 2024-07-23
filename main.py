from src import Parser
import sys

def main():
    arguments = sys.argv[1:]
    if len(arguments) != 2:
        raise Exception("Wrong input format.\nUse: python3 main.py <domain_path> <problem_path>")
    
    domain_path = arguments[0]
    problem_path = arguments[1]
    problem_name = problem_path.split(".")[0].split('/')[-1]
    output_path = problem_name + '.out'
    parser = Parser(domain_path, problem_path)
    parser.print_bdds(output_path)

if __name__ == "__main__":
    main()