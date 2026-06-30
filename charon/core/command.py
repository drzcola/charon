from abc import ABC, abstractmethod

class Command(ABC):
    name: str
    help: str

    @abstractmethod
    def execute(self, args: list[str], shell) -> None:
        ...

class CommandRegistry:
    def __init__(self):
        self._commands: dict[str, Command] = {}

    def register(self, command: Command) -> None:
        self._commands[command.name] = command

    def dispatch(self, line: str, shell) -> None:
        parts = line.split()
        name, args = parts[0], parts[1:]
        cmd = self._commands.get(name)
        if cmd:
            cmd.execute(args, shell)
        else:
            print(f"Unknown command: {name}. Type 'help' for a list of commands.")

    def commands(self) -> dict[str, Command]:
        return self._commands