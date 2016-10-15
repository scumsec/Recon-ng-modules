from recon.core.module import BaseModule
from recon.mixins.resolver import ResolverMixin
import dns.resolver
import dns.query
import dns.zone
import re

class Module(BaseModule):

    meta = {
        'name': 'DNS Zone Transfer',
        'author': 'Zach Grace (@ztgrace)',
        'description': 'Perform Zone Transfers against each NS record for a domain',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def get_NS_records(self, domain):
        ns = list()
        answers = dns.resolver.query(domain, 'NS')
        for a in answers:
            res = re.sub('\.$', '', a.to_text())
            self.verbose('Found name server : %s' % res)
            ns.append(res)

        return ns

    def parse_record(self, r):
        if re.match("^@", r):
            return None
    
        (name, ttl, rclass, rtype, rdata) = r.split(' ', 4)
        record = {
            'name'  : name,
            'ttl'   : ttl,
            'rlcass': rclass,
            'rtype' : rtype,
            'rdata' : rdata
        }

        return record
        

    def module_run(self, domains):
        for domain in domains:
            self.heading(domain, level=0)

            name_servers = self.get_NS_records(domain)

            for ns in name_servers:
                self.verbose('Attempting zone transfer from : %s' % ns)
                
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(ns, domain))
                except:
                    self.error("%s does not allow zone transfers" % ns)
                    continue

                names = zone.nodes.keys()
                names.sort()
                for n in names:
                    record = zone[n].to_text(n)
                    self.output("Received: %s" % record)
                    parsed = self.parse_record(record)
                    if parsed:
                        if parsed['rtype'] in ("A", "AAAA", "CNAME"):
                            fqdn = ".".join((parsed['name'], domain))
                            self.output(fqdn)
                            self.add_hosts(host=fqdn)
