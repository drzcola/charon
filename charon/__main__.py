import argparse

from charon.core.shell import CharonShell
from charon.core.loader import load_commands, load_modules

def main():
    parser = argparse.ArgumentParser(
        prog="charon",
        description="A swiss army knife framework for Kerberos post-exploitation",
    )
    parser.add_argument("--no-banner", action="store_true", help="Skip the startup banner")
    parser.add_argument("--version", action="version", version="Charon 0.1.0")
    args = parser.parse_args()

    if not args.no_banner:
        print_banner()

    shell = CharonShell()
    load_commands(shell)
    load_modules(shell)
    shell.run()

def print_banner():
    pass

if __name__ == "__main__":
    main()