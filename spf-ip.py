from recon.core.module import BaseModule
from recon.mixins.resolver import ResolverMixin
import dns.resolver

class Module(BaseModule, ResolverMixin):

    meta = {
        'name': 'Sender Policy Framework (SPF) Record Retriever',
        'author': 'Jim Becher (@jimbecher, jbecher@korelogic.com)',
        'description': 'Retrieves the SPF IPv4 records for a domain. Updates the \'hosts\' and/or \'netblocks\' tables with the results.',
        'comments': (
            'This module reads domains from the domains table and retrieves the IP addresses and/or netblocks',
            'of the SPF records associated with each domain. The addresses are then stored in the hosts',
            'and/or netblocks table.'
        ),
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def module_run(self, domains):
        max_attempts = 3
        resolver = self.get_resolver()
        answers = ""
        for domain in domains:
            attempt = 0
            while attempt < max_attempts:
                try:
                    answers = resolver.query(domain, 'TXT')
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    self.verbose('%s => No record found.' % (domain))
                except dns.resolver.Timeout:
                    self.verbose('%s => Request timed out.' % (domain))
                    attempt += 1
                    continue
                except (dns.resolver.NoNameservers):
                    self.verbose('%s => Invalid nameserver.' % (domain))
                else:
                    for txtrecord in answers:
                        if "v=spf" in txtrecord.to_text():
                            resp = txtrecord.to_text()
                            words = resp.split()
                            for item in words:
                                if "ip4" in item:
                                    ipaddr = item.split(':', 1)[1]
                                    if "/" in ipaddr:
                                        self.output(ipaddr)
                                        self.add_netblocks(ipaddr)
                                    else:
                                        self.output(ipaddr)
                                        self.add_hosts(ip_address=ipaddr)
                                elif "a:" in item:
                                    spfhost = item.split(':', 1)[1]
                                    self.output(spfhost)
                                    self.add_hosts(host=spfhost)
                # break out of the loop
                attempt = max_attempts
