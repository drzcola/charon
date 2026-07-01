from binascii import unhexlify

from impacket.krb5.kerberosv5 import getKerberosTGT
from impacket.krb5.types import Principal
from impacket.krb5 import constants
from impacket.krb5.ccache import CCache

from charon.core.kerberos_module import KerberosModule
from charon.core.module import Option

class GetTGTModule(KerberosModule):
    name = "kerberos/get_tgt"
    description = "Request a TGT for a user account"

    # Requests a fresh TGT from credentials, so an existing ccache is not
    # valid input; the base validate() enforces this.
    requires_credentials = True

    def __init__(self):
        super().__init__()
        self.options["OUTPUT"] = Option(
            "Output ccache path (default: /tmp/<username>.ccache)",
            required=False
        )

    def run(self, shell) -> None:
        errors = self.validate()
        if errors:
            for e in errors:
                print(f"[!] {e}")
            return

        auth        = self.resolve_auth()
        username    = auth.get("username")
        domain      = auth.get("domain")
        password    = auth.get("password", "")
        lmhash, nthash, aeskey = "", "", ""

        if auth["method"] == "hash":
            lmhash, nthash = auth["hashes"].split(":")
        elif auth["method"] == "aes":
            aeskey = auth["aes_key"]

        client = Principal(username, type=constants.PrincipalNameType.NT_PRINCIPAL.value)
        tgt, cipher, oldSessionKey, sessionKey = getKerberosTGT(
            client, password, domain,
            unhexlify(lmhash) if lmhash else b"",
            unhexlify(nthash) if nthash else b"",
            aeskey,
            self.options["DC_IP"].value,
            kdcOptions=self.resolve_kdc_options(),
        )

        output = self.options["OUTPUT"].value or f"/tmp/{username}.ccache"
        ccache = CCache()
        ccache.fromTGT(tgt, oldSessionKey, sessionKey)
        ccache.saveFile(output)
        print(f"[+] TGT saved to {output}")
        print(f"[*] export KRB5CCNAME={output}")