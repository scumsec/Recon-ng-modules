from recon.core.module import BaseModule
import json

# via https://github.com/PaulSec/API-dnsdumpster.com
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI

class Module(BaseModule):

    meta = {
        'name': 'DNSDumpster Record Retriever',
        'author': 'jose nazario @jnazario',
        'description': 'Retrieves the DNS records for a domain using the DNSDumpster site. Updates the \'hosts\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def module_run(self, domains):
        for domain in domains:
            res = DNSDumpsterAPI(False).search(domain)
            for entry in res['dns_records']['dns']:
                self.add_hosts(host=entry['domain'].rstrip('.'), ip_address=entry['ip'])
            for entry in res['dns_records']['mx']:
                # get rid of MX pref
                self.add_hosts(host=entry['domain'].split()[1].rstrip('.'), ip_address=entry['ip'])
            for entry in res['dns_records']['host']:
                if entry['reverse_dns']:
                    self.add_hosts(ip_address=entry['ip'], host=entry['reverse_dns'])
                else:
                    self.add_hosts(host=entry['domain'].rstrip('.'), ip_address=entry['ip'])
            