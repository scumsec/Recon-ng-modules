from recon.core.module import BaseModule
from urlparse import urlparse
import re
# TODO CHECK

class Module(BaseModule):
    meta = {
        'name': 'IP -> Netblock',
        'author': 'Zach Grace (@ztgrace)',
        'description': 'Uses the ARIN Whois RWS to get the netblock and company for an IP address',
        'query': 'SELECT DISTINCT ip_address FROM hosts WHERE ip_address IS NOT NULL',
    }

    def get_orgRef(self, resp):
        try:
            handle = resp.json['ns4:pft']['net']['orgRef']['@handle']
        except KeyError:
            return None

        return handle

    def add_columns(self, ):
        try:
            self.query("ALTER TABLE hosts ADD COLUMN netblock TEXT")
        except Exception as e:
            print("[*] Column most likely exists.  Error returned: " + str(e))
        try:
            self.query("ALTER TABLE hosts ADD COLUMN company TEXT")
        except Exception as e:
            print("[*] Column most likely exists. Error returned: " + str(e))

    def module_run(self, ips):
        self.add_columns()
        headers = {'Accept': 'application/json'}
        for ip in ips:
            self.heading(ip, level=0)
            payload = {'flushCache': 'false', 'q': ip}
            urls = [
                'http://whois.arin.net/ui/query.do'
            ]
            for url in urls:
                self.verbose('URL: %s' % url)
                resp = self.request(url, headers=headers, payload=payload)

                if self.get_orgRef(resp) == 'APNIC' or self.get_orgRef(resp) == 'RIPE' or self.get_orgRef(
                        resp) == 'LACNIC' or self.get_orgRef(resp) == 'AFRINIC':
                    self.output('Error, %s is %s.' % (ip, resp.json['ns4:pft']['net']['orgRef']['@name']))
                    continue

                try:  # Reallocated IP space
                    org = resp.json['ns4:pft']['customer']['name']['$']
                    handle = resp.json['ns4:pft']['customer']['handle']['$']
                except KeyError, ke:
                    try:  # Direct allocation
                        org = resp.json['ns4:pft']['net']['orgRef']['@name']
                        handle = resp.json['ns4:pft']['net']['orgRef']['@handle']
                    except KeyError, ke:
                        self.output("Error querying %s" % ip)
                        continue

                self.add_companies(company=org, description=handle)
                self.query('UPDATE hosts SET company=? WHERE ip_address=?', (org, ip))

                netblocks = resp.json['ns4:pft']['net']['netBlocks']['netBlock']
                if type(netblocks) == dict:  # single net block
                    netblock = resp.json['ns4:pft']['net']['netBlocks']['netBlock']
                    cidr = netblock['cidrLength']['$']
                    description = netblock['description']['$']
                    endAddress = netblock['endAddress']['$']
                    startAddress = netblock['startAddress']['$']
                    nb = "%s/%s" % (startAddress, cidr)
                    self.output("%s is in netblock %s and belongs to %s" % (ip, nb, org))
                    self.add_netblocks(nb)
                    host_nb = nb

                elif type(netblocks) == list:  # multiple netblocks

                    host_nb = ""
                    for netblock in netblocks:
                        cidr = netblock['cidrLength']['$']
                        description = netblock['description']['$']
                        endAddress = netblock['endAddress']['$']
                        startAddress = netblock['startAddress']['$']
                        nb = "%s/%s" % (startAddress, cidr)
                        self.output("%s is in netblock %s and belongs to %s" % (ip, nb, org))
                        self.add_netblocks(nb)
                        host_nb += "%s, " % nb

                    host_nb = re.sub(r', *$', '', host_nb)

                self.query('UPDATE hosts SET netblock=? WHERE ip_address=?', (host_nb, ip))
