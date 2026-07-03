from charon.core.base import BaseCommand
from charon.core.registry import MODULES
from charon.core.registry import register
from charon.io.console import console
from charon.io.table import build_table


@register
class ModulesCommand(BaseCommand):
    name = "modules"
    help = "List available modules."

    def _create_table(self, entries: dict):
        table = build_table("Module", "Description")

        for name, module in entries:
            table.add_row(f"{name}", f"{module.description}")

        return table

    def run(self, args):
        console.print(self._create_table(MODULES.items()))
