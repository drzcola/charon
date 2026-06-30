import os
from abc import ABC
from impacket.krb5 import constants
from charon.core.module import Module, Option

# KerberosModule sits between Module and concrete attack modules.
# It pre-populates the four mutually exclusive auth options so every
# Kerberos module gets them for free without repeating the definitions.
class KerberosModule(Module, ABC):
    # Named KDC options presets. "windows" mimics a real Windows AS-REQ
    # and is the least detectable. "impacket" is the unpatched default.
    PRESETS: dict[str, str] = {
        "windows":  "forwardable,renewable,canonicalize,renewable_ok",
        "impacket": "forwardable,renewable,proxiable",
        "minimal":  "forwardable",
    }

    def __init__(self):
        # Initialise self.options = {} in the parent before we populate it.
        super().__init__()
        self.options.update({
            "USERNAME":    Option("Username to authenticate as", required=False),
            "DOMAIN":      Option("Target domain (FQDN or NETBIOS)", required=False),
            "PASSWORD":    Option("Plaintext password", required=False),
            "HASHES":      Option("NTLM hashes (LM:NT)", required=False),
            "AES_KEY":     Option("AES128 or AES256 key", required=False),
            "CCACHE":      Option("Path to .ccache file (or set KRB5CCNAME)", required=False),
            "DC_IP":       Option("Domain controller IP", required=True),
            "KDC_OPTIONS": Option("KDC options flags, comma-separated. See 'info' for presets.", required=False,
                                  value=KerberosModule.PRESETS["windows"]),
        })

    def resolve_auth(self) -> dict:
        # Ticket auth: explicit CCACHE path wins, then fall back to the
        # KRB5CCNAME environment variable (standard Unix ccache location).
        ccache = self.options["CCACHE"].value or os.environ.get("KRB5CCNAME")
        if ccache:
            return {"method": "ticket", "ccache": ccache}

        # For the credential-based methods, USERNAME and DOMAIN are always needed.
        username = self.options["USERNAME"].value
        domain   = self.options["DOMAIN"].value

        # Priority: AES > hashes > password (strongest first).
        if self.options["AES_KEY"].value:
            return {"method": "aes", "username": username, "domain": domain, "aes_key": self.options["AES_KEY"].value}
        if self.options["HASHES"].value:
            return {"method": "hash", "username": username, "domain": domain, "hashes": self.options["HASHES"].value}
        if self.options["PASSWORD"].value:
            return {"method": "password", "username": username, "domain": domain, "password": self.options["PASSWORD"].value}

        # No auth method configured.
        return {}

    def resolve_kdc_options(self) -> list:
        raw = self.options["KDC_OPTIONS"].value or ""
        flags = []
        for name in raw.split(","):
            name = name.strip()
            try:
                flags.append(constants.KDCOptions[name].value)
            except KeyError:
                pass
        return flags