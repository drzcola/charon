from charon.core.command import Command

class UseCommand(Command):
    name = "use"
    help = "Load a module (e.g. use kerberos/get_tgt)"

    def execute(self, args: list[str], shell) -> None:
        if not args:
            print("[!] Usage: use <module>")
            return
        module_name = args[0]
        module_class = shell.modules.get(module_name)
        if not module_class:
            print(f"[!] Unknown module: {module_name}")
            return
        shell.current_module = module_class()