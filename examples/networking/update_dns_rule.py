import os

from staxapp.config import Config
from staxapp.openapi import StaxClient

Config.access_key = os.getenv("STAX_ACCESS_KEY")
Config.secret_key = os.getenv("STAX_SECRET_KEY")

networks = StaxClient("networking")

body = {
    "Name": "my-dns-rule"
}

response = networks.UpdateDnsRule(dns_rule_id="<dns_rule_uuid>", **body)

print(response.json())