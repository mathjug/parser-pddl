import os
import sys

# Get the absolute path to the directory containing conf.py
_project_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root) and src directory to the path
sys.path.insert(0, os.path.join(_project_dir, '..', '..'))
sys.path.insert(0, os.path.abspath(os.path.join(_project_dir, '..', '..', 'src')))

# -- Project information -----------------------------------------------------

project = 'Parser PDDL to BDDs'
copyright = '2024, André Nogueira Ribeiro, Henri Michel França Oliveira, João Guilherme Alves Santos, Matheus Sanches Jurgensen.'
author = 'André Nogueira Ribeiro, Henri Michel França Oliveira, João Guilherme Alves Santos, Matheus Sanches Jurgensen.'
release = '0.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_default_options = {
    'members': True,
    'private-members': True,
}

# Tell sphinx what the primary document is
master_doc = 'index'
