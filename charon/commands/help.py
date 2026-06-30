from rich.console import Console
from rich.table import Table

from charon.core.command import Command

class HelpCommand(Command):
    name = "help"
    help = "Show available commands"

    def execute(self, args: list[str], shell) -> None:
        console = Console()
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Command")
        table.add_column("Description")

        for cmd in shell.registry.commands().values():
            table.add_row(cmd.name, cmd.help)

        console.print(table)