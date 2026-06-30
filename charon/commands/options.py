from rich.console import Console
from rich.table import Table
from charon.core.command import Command

class OptionsCommand(Command):
    name = "options"
    help = "Show current module options"

    def execute(self, args: list[str], shell) -> None:
        if shell.current_module is None:
            print("[!] No module loaded")
            return
        console = Console()
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Option")
        table.add_column("Value")
        table.add_column("Required")
        table.add_column("Description")

        for name, opt in shell.current_module.options.items():
            table.add_row(
                name,
                str(opt.value) if opt.value is not None else "",
                "yes" if opt.required else "no",
                opt.description,
            )
        console.print(table)
