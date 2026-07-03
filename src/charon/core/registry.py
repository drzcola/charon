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


def register_module(cls):
    instance = cls()
    MODULES[instance.name] = instance

    return cls


def discover_modules():
    modules_base_path = Path(__file__).parent.parent / "modules"
    for module_file in modules_base_path.glob("*/module.py"):
        module_name = f"charon.modules.{module_file.parent.name}.module"
        importlib.import_module(module_name)
