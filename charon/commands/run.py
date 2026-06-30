from charon.core.command import Command

class RunCommand(Command):
    name = "run"
    help = "Execute the current module"

    def execute(self, args: list[str], shell) -> None:
        if shell.current_module is None:
            print("[!] No module loaded")
            return
        shell.current_module.run(shell)