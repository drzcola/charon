class BaseCommand:
    name: str = ""
    help: str = ""

    def run(self, args: str):
        raise NotImplementedError


class BaseModule:
    name: str = ""
    description: str = ""
    options: dict = {}
