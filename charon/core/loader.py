import importlib
import inspect
import pkgutil

import charon.commands
import charon.modules
from charon.core.command import Command
from charon.core.module import Module

def load_commands(shell) -> None:
    for _, modname, _ in pkgutil.iter_modules(charon.commands.__path__):
        module = importlib.import_module(f"charon.commands.{modname}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Command) and obj is not Command:
                shell.registry.register(obj())

def load_modules(shell) -> None:
    for _, modname, _ in pkgutil.iter_modules(charon.modules.__path__):
        module = importlib.import_module(f"charon.modules.{modname}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Module) and obj is not Module and hasattr(obj, "name"):
                shell.modules[obj.name] = obj