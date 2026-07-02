from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style


class Shell:
    def __init__(self):
        self.session = PromptSession()
        self.style = Style.from_dict({"bracket": "#34ebc3 bold", "brand": "#042d7a"})

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
        print(f"got: {line}")
