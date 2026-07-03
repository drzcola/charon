from charon.core.base import BaseCommand
from charon.core.registry import register
from charon.io.console import console


@register
class ExitCommand(BaseCommand):
    name = "exit"
    help = "Exit charon shell."

    def run(self, args):
        console.print("[grey50]Exiting...")
        raise EOFError
