# PACTL-Sym: PDDL Parser

## Introduction
This repository contains the code for the **PDDL parser** of the PACTL-Sym system, an automated planning system in Artificial Intelligence.

PACTL-Sym is part of the PhD thesis of Viviane M. Bonadia dos Santos, a doctorate student at IME-USP. The system employs symbolic model-checking techniques to select and execute actions that transform the environment from an initial state to a goal state.

For more detailed information about this project, please visit our official [project website](https://pactl-sym-labxp-ime-usp-2024-1-pactl-6e30bbe1f76ac247ed32d018b5.gitlab.io).

## Authors
- Matheus Sanches Jurgensen [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue)](https://www.linkedin.com/in/matheusjurgensen/)
- André Nogueira Ribeiro [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue)](https://www.linkedin.com/in/andré-nogueira-ribeiro-0172ba24b/)
- Henri Michel França Oliveira [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue)](https://www.linkedin.com/in/henri-michel-5763612ba/)
- João Guilherme Alves Santos [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue)](https://www.linkedin.com/in/joao-guilherme-santos-8312a5208/)

## Installation
This parser is fully developed in Python. Therefore, `Python (>=3.8)` is required. After that, the following procedure
must be followed:
1. Clone the repository:

    ```bash
    git clone https://gitlab.com/labxp-ime-usp/2024.1/pactl/parser_pddl_to_bdds.git
    ```
2. Navigate to the project directory:

    ```bash
    cd parser_pddl_to_bdds
    ```
3. Create and activate a virtual environment:

    ```bash
    python -m venv venv # Create the environment
    source venv/bin/activate  # Activate the environment on macOS/Linux
    ```
4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

Following these steps will install all dependencies in the created virtual environment. You only need to perform these steps once. However, you must always activate the virtual environment (using the command listed above from the cloned directory) before using the parser. After use, you can deactivate the environment using the `deactivate` command.

## Usage
You can use the package by running the `main.py` file from inside the package directory:

```bash
python3 main.py <domain_path> <problem_path>
```

You can also use the package from outside of the cloned directory by importing the `Parser` module in a `Python` script as follows:

```python
# Replace `your.file.structure` with the correct path to the `src` folder
from your.file.structure.src import Parser

# Replace "path_to_domain_file" with the path to your PDDL domain file
domain_path = "path_to_domain_file"
# Replace "path_to_problem_file" with the path to your PDDL problem file
problem_path = "path_to_problem_file"
# Replace "parser_output.out" with the desired output file name
output_file = "parser_output.out"

parser = Parser(domain_path, problem_path)
parser.print_bdds(output_file)
```

For both procedures above, the output file will be created in the directory from which the script is executed.