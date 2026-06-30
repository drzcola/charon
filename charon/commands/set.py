from charon.core.command import Command

class SetCommand(Command):
    name = "set"
    help = "Set a module option (e.g. set USERNAME john)"

    def execute(self, args: list[str], shell) -> None:
        if shell.current_module is None:
            print("[!] No module loaded")
            return
        if len(args) < 2:
            print("[!] Usage: set <option> <value>")
            return
        key, value = args[0], " ".join(args[1:])
        if not shell.current_module.set(key, value):
            print(f"[!] Unknown option: {key}")
        else:
            print(f"[*] {key.upper()} => {value}")