from charon.core.base import BaseModule
from charon.core.registry import register_module


@register_module
class GetTGTModule(BaseModule):
    name = "gettgt"
    description = "Request a Kerberos ticket and save it to disk."
    options = {
        "USERNAME": {"value": "", "description": "Target username.", "required": True},
        "PASSWORD": {"value": "", "description": "Target password.", "required": False},
        "DOMAIN": {"value": "", "description": "Target domain.", "required": True},
        "HASHES": {"value": "", "description": "LM:NT hashes.", "required": False},
        "AESKEY": {
            "value": "",
            "description": "AES key for Kerberos auth.",
            "required": False,
        },
        "DC_IP": {
            "value": "",
            "description": "Domain controller IP.",
            "required": False,
        },
    }

    def run(self, args): ...
