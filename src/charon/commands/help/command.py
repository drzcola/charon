from charon.core.base import BaseCommand
from charon.core.registry import COMMANDS
from charon.core.registry import register
from charon.io.console import console
from charon.io.table import build_table


@register
class HelpCommand(BaseCommand):
    name = "help"
    help = "Display this help."

    def _create_table(self, entries: dict):
        table = build_table("Command", "Description")

        for name, cmd in entries:
            table.add_row(f"{name}", f"{cmd.help}")

        return table

    def run(self, args):
        console.print(self._create_table(COMMANDS.items()))
