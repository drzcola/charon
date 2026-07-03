import importlib
from pathlib import Path

from charon.core.base import BaseCommand
from charon.core.base import BaseModule

COMMANDS: dict[str, BaseCommand] = {}
MODULES: dict[str, BaseModule] = {}


def register(cls):
    instance = cls()
    COMMANDS[instance.name] = instance

    return cls


def discover():
    commands_base_path = Path(__file__).parent.parent / "commands"
    for command_file in commands_base_path.glob("*/command.py"):
        module_name = f"charon.commands.{command_file.parent.name}.command"
        importlib.import_module(module_name)
