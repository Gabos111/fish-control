"""
CLI wrapper around FishController.
Run:
  python -m fish_control start   # run controller
  python -m fish_control gui     # launch web GUI
"""
import typer
from .controller import FishController

cli = typer.Typer(help="Fish robot controller")

@cli.command()
def start():
    """Start the fish control loop (Ctrl-C to stop)."""
    FishController().run()

@cli.command()
def gui():
    """Launch the web-based parameter editor."""
    from .ui import app
    app.run(host="0.0.0.0", port=5000)