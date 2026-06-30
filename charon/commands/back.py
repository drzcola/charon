from charon.core.command import Command

class BackCommand(Command):
    name = "back"
    help = "Unload the current module"

    def execute(self, args: list[str], shell) -> None:
        if shell.current_module is None:
            print("[!] No module loaded")
            return
        shell.current_module = None