from charon.core.command import Command

class ExitCommand(Command):
    name = "exit"
    help = "Exit Charon"

    def execute(self, args: list[str], shell) -> None:
        shell.running = False