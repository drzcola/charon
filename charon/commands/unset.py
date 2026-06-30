from charon.core.command import Command

class UnsetCommand(Command):
    name = "unset"
    help = "Clear a module option (e.g. unset PASSWORD)"

    def execute(self, args: list[str], shell) -> None:
        if shell.current_module is None:
            print("[!] No module loaded")
            return
        if not args:
            print("[!] Usage: unset <option>")
            return
        key = args[0].upper()
        if key not in shell.current_module.options:
            print(f"[!] Unknown option: {key}")
            return
        shell.current_module.options[key].value = None
        print(f"[*] {key} cleared")