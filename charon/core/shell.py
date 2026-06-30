import os

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

from charon.core.command import CommandRegistry

class CharonShell:
    def __init__(self):
        history_path = os.path.expanduser("~/.local/share/charon/charon_history")
        os.makedirs(os.path.dirname(history_path), exist_ok=True)
        self.session = PromptSession(history=FileHistory(history_path))
        self.running = True
        self.style = Style.from_dict({
            "bracket": "#666666",
            "brand": "#cc0000 bold",
            "module": "#ff8800 bold",
            "separator": "#666666",
        })
        self.registry = CommandRegistry()
        self.current_module = None
        self.modules: dict = {}

    def _get_prompt(self):
        tokens = [
            ("class:bracket", "["),
            ("class:brand", "charon"),
            ("class:bracket", "]"),
        ]
        if self.current_module:
            tokens.append(("class:bracket", "["))
            tokens.append(("class:module", self.current_module.name))
            tokens.append(("class:bracket", "]"))
        tokens.append(("class:bracket", "> "))
        return FormattedText(tokens)

    def run(self):
        while self.running:
            try:
                line = self.session.prompt(self._get_prompt(), style=self.style)
                self.dispatch(line.strip())
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        
    def dispatch(self, line):
        if not line:
            return
        self.registry.dispatch(line, self)