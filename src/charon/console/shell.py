from prompt_toolkit import PromptSession


class Shell:
    def __init__(self):
        self.session = PromptSession()

    def run(self):
        while True:
            try:
                line = self.session.prompt("[charon] ")
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
