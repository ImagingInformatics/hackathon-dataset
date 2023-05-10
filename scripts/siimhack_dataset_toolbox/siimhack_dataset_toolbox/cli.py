# Find the root of the project to add it to the python path for resolving imports
import pyrootutils

path = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml", "requirements.txt"],
    pythonpath=True,
    dotenv=True,
)
import os
import click
context_settings = dict(help_option_names=["-h", "--help"])