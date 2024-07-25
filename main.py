from src.parser_pddl import Parser
import sys,os

def main():
    arguments = sys.argv[1:]
    if len(arguments) != 2:
        raise Exception("Wrong input format.\nUse: python3 main.py <domain_path> <problem_path>")
    
    domain_path = arguments[0]
    problem_path = arguments[1]
    problem_name = problem_path.split('/')[-1].split(".")[0]
    output_dir = "output"
    output_path = output_dir + "/" + problem_name + '.out'
    os.makedirs(output_dir, exist_ok=True)
    parser = Parser(domain_path, problem_path)
    parser.print_bdds(output_path)

if __name__ == "__main__":
    main()