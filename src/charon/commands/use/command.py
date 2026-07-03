from charon.core.base import BaseCommand
from charon.core.registry import MODULES
from charon.core.registry import register
from charon.core.session import session
from charon.io.console import console


@register
class UseCommand(BaseCommand):
    name = "use"
    help = "Load a specific module. Usage: use <module>"

    def run(self, args):
        module = MODULES.get(args)
        if module is None:
            console.print(f"Unknown module: {args}")
            return
        session.current_module = module
        console.print(f"Loaded module: {args}")
