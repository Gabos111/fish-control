"""
Allow `python -m fish_control [...]` to invoke the CLI commands.
"""
from .main import cli

if __name__ == "__main__":
    cli()
