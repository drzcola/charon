from rich.console import Console
from rich.table import Table
from charon.core.command import Command
from charon.core.kerberos_module import KerberosModule

class InfoCommand(Command):
    name = "info"
    help = "Show module description and available presets"

    def execute(self, args: list[str], shell) -> None:
        if shell.current_module is None:
            print("[!] No module loaded")
            return

        console = Console()
        module  = shell.current_module

        console.print(f"\n  [bold]Name:[/bold]        {module.name}")
        console.print(f"  [bold]Description:[/bold] {module.description}\n")

        if isinstance(module, KerberosModule):
            table = Table(show_header=True, header_style="bold red", title="KDC_OPTIONS presets")
            table.add_column("Preset")
            table.add_column("Flags")
            table.add_column("Notes")

            notes = {
                "windows":  "Mimics Windows default AS-REQ — least detectable",
                "impacket": "Unpatched impacket default — noisy, easily fingerprinted",
                "minimal":  "Bare minimum — only forwardable flag set",
            }
            for preset, flags in KerberosModule.PRESETS.items():
                table.add_row(preset, flags, notes.get(preset, ""))

            console.print(table)
            console.print(f"\n  [dim]Usage: set KDC_OPTIONS <preset or comma-separated flags>[/dim]\n")
