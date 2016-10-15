from recon.core.module import BaseModule
from recon.mixins.resolver import ResolverMixin
import dns.resolver

class Module(BaseModule, ResolverMixin):

    meta = {
        'name': 'Mail eXchange Record Retriever',
        'author': 'Jim Becher (@jimbecher, jbecher@korelogic.com)',
        'description': 'Retrieves the MX records for a domain. Updates the \'hosts\' table with the results.',
        'comments': (
            'This module reads domains from the domains table and retrieves the hostnames of the MX records',
            'associated with each domain. The hostnames are then stored in the hosts table.'
        ),
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def module_run(self, domains):
        max_attempts = 3
        resolver = self.get_resolver()
        answers = ""
        for domain in domains:
            attempt = 0
            self.heading(domain, level=0)
            while attempt < max_attempts:
                try:
                    answers = resolver.query(domain, 'MX')
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    self.verbose('%s => No record found.' % (domain))
                except dns.resolver.Timeout:
                    self.verbose('%s => Request timed out.' % (domain))
                    attempt += 1
                    continue
                except (dns.resolver.NoNameservers):
                    self.verbose('%s => Invalid nameserver.' % (domain))
                else:
                    for rdata in answers:
                        host = rdata.exchange
                        host = str(host)
                        host = host[:-1]
                        self.output(host)
                        self.add_hosts(host)
                # break out of the loop
                attempt = max_attempts
