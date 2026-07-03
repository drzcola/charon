from charon.core.base import BaseCommand
from charon.core.registry import register
from charon.core.session import session
from charon.io.console import console
from charon.io.table import build_table


@register
class OptionsCommand(BaseCommand):
    name = "options"
    help = "Display available options for the loaded module."

    def _create_table(self, entries: dict):
        table = build_table("Option", "Value", "Description", "Required")

        for name, opt in entries:
            table.add_row(name, opt["value"], opt["description"], str(opt["required"]))

        return table

    def run(self, args):
        if session.current_module is None:
            console.print("No module loaded. Use `use <module>` first.")
            return
        console.print(self._create_table(session.current_module.options.items()))
