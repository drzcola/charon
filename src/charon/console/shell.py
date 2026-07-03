from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

from charon.core.registry import COMMANDS
from charon.core.registry import discover


class Shell:
    def __init__(self):
        self.style = Style.from_dict({"bracket": "#34ebc3 bold", "brand": "#4a9eff"})
        self.session = PromptSession()
        discover()

    def _get_prompt(self):
        tokens = [
            ("class:bracket", "["),
            ("class:brand", "charon"),
            ("class:bracket", "] "),
        ]
        return FormattedText(tokens)

    def run(self):
        while True:
            try:
                line = self.session.prompt(self._get_prompt, style=self.style)
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            self.dispatch(line)

    def dispatch(self, line):
        line = line.strip()
        if not line:
            return
        if line in ("exit", "quit"):
            raise EOFError
        cmd, _, args = line.partition(" ")
        command = COMMANDS.get(cmd)
        if command is None:
            print(f"Unknown command: {command}")
            return
        command.run(args)
