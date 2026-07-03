class BaseCommand:
    name: str = ""
    help: str = ""

    def run(self, args: str):
        raise NotImplementedError
