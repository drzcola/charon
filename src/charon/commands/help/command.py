from rich.table import Table

from charon.core.base import BaseCommand
from charon.core.registry import COMMANDS
from charon.core.registry import register
from charon.io.console import console


@register
class HelpCommand(BaseCommand):
    name = "help"
    help = "Display this help."

    def _create_table(self, entries: dict):
        table = Table()

        table.add_column("Command")
        table.add_column("Description", no_wrap=True)

        for name, cmd in entries:
            table.add_row(f"{name}", f"{cmd.help}")

        return table

    def run(self, args):
        console.print(self._create_table(COMMANDS.items()))
