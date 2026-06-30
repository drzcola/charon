from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class Option:
    description: str
    required: bool = True
    value: Any = None

class Module(ABC):
    name: str
    description: str

    def __init__(self):
        self.options: dict[str, Option] = {}

    def set(self, key: str, value: str) -> bool:
        key = key.upper()
        if key not in self.options:
            return False
        self.options[key].value = value
        return True

    def validate(self) -> list[str]:
        return [k for k, o in self.options.items() if o.required and o.value is None]

    @abstractmethod
    def run(self, shell) -> None:
        ...