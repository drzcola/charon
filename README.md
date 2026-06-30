# Charon

A modular Kerberos post-exploitation framework. Think Metasploit but focused entirely on Kerberos abuse — interactive shell, swappable modules, and a patched Impacket that doesn't scream "attacker tool" at your EDR.

> Named after the ferryman of the dead. You're just helping tickets cross the river.

---

## Install

```bash
git clone <repo>
cd charon

pip install -e .
pip install -e vendor/impacket   # patched impacket, do this every time you patch it
```

Then just run:

```bash
charon
# or
python -m charon
```

---

## Usage

The shell works like Metasploit. Load a module, set your options, run it.

```
[charon]> use kerberos/get_tgt
[charon][kerberos/get_tgt]> set USERNAME john.doe
[charon][kerberos/get_tgt]> set DOMAIN CORP.LOCAL
[charon][kerberos/get_tgt]> set PASSWORD Summer2024!
[charon][kerberos/get_tgt]> set DC_IP 10.10.10.1
[charon][kerberos/get_tgt]> run

[+] TGT saved to /tmp/john.doe.ccache
[*] export KRB5CCNAME=/tmp/john.doe.ccache
```

Tickets land in `/tmp` by default. Export `KRB5CCNAME` and any Kerberos-aware tool picks them up automatically.

---

## Commands

| Command   | Description                              |
|-----------|------------------------------------------|
| `use`     | Load a module                            |
| `back`    | Unload current module                    |
| `set`     | Set a module option                      |
| `unset`   | Clear a module option                    |
| `options` | Show current module options and values   |
| `info`    | Show module description and presets      |
| `run`     | Execute the current module               |
| `help`    | List all available commands              |
| `exit`    | Exit Charon                              |

---

## Auth methods

Every module supports four mutually exclusive auth methods:

| Method   | Options needed                  |
|----------|---------------------------------|
| Password | `USERNAME` `DOMAIN` `PASSWORD`  |
| Hash     | `USERNAME` `DOMAIN` `HASHES`    |
| AES key  | `USERNAME` `DOMAIN` `AES_KEY`   |
| Ticket   | `CCACHE` (or `KRB5CCNAME` env)  |

For hashes, use the `LM:NT` format. If you only have an NT hash, pad the LM part: `aad3b435b51404eeaad3b435b51404ee:<nthash>`.

---

## KDC options

Impacket's default KDC options (`forwardable, renewable, proxiable`) are a well-known fingerprint. Charon patches this and defaults to Windows-like behavior instead.

You can tune it per-module:

```
[charon][kerberos/get_tgt]> info

  Name:        kerberos/get_tgt
  Description: Request a TGT for a user account

  KDC_OPTIONS presets:
  ┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃ Preset   ┃ Flags                                   ┃
  ┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
  │ windows  │ forwardable,renewable,canonicalize,...  │  ← default
  │ impacket │ forwardable,renewable,proxiable         │  ← noisy
  │ minimal  │ forwardable                             │
  └──────────┴─────────────────────────────────────────┘

[charon][kerberos/get_tgt]> set KDC_OPTIONS forwardable,renewable,canonicalize,renewable_ok
```

---

## Modules

| Module              | Description             |
|---------------------|-------------------------|
| `kerberos/get_tgt`  | Request a TGT           |

More coming.

---

## Adding a module

Drop a file in `charon/modules/`. It gets picked up automatically on next launch.

```python
from charon.core.kerberos_module import KerberosModule
from charon.core.module import Option

class MyModule(KerberosModule):
    name = "kerberos/my_module"
    description = "Does something useful"

    def __init__(self):
        super().__init__()
        # add module-specific options here

    def run(self, shell) -> None:
        auth = self.resolve_auth()
        kdc_opts = self.resolve_kdc_options()
        # do the thing
```

You get auth resolution, KDC option handling, and all the standard options for free from `KerberosModule`.

---

## Project layout

```
charon/
├── charon/
│   ├── commands/       # shell commands (one file each, auto-loaded)
│   ├── core/           # shell, registry, module base classes
│   └── modules/        # attack modules (one file each, auto-loaded)
├── vendor/
│   └── impacket/       # patched impacket
├── LICENSE
├── NOTICE
└── pyproject.toml
```

---

## License & attribution

Charon is licensed under the Apache License 2.0. See `LICENSE`.

This product includes software developed by SecureAuth Corporation
(https://www.secureauth.com/) and Fortra (https://www.fortra.com) — specifically
a modified copy of [Impacket](https://github.com/fortra/impacket), vendored under
`vendor/impacket/` and distributed under its own license (`vendor/impacket/LICENSE`).
See `NOTICE` for details of the modifications made.
