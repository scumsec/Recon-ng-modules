from recon.core.module import BaseModule
import re

class Module(BaseModule):

    meta = {
        'name': 'Shodan Org Enumerator',
        'author': 'ScumSec 0x1414',
        'description': 'Harvests hosts from the Shodan API by using the \'org\' search operator. Updates the \'hosts\' and the \'ports\' tables with the results.',
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
        'options': (
            ('limit', 1, True, 'limit number of api requests per input source (0 = unlimited)'),
        ),
    }

    def module_run(self, companies):
        limit = self.options['limit']
        for company in companies:
            self.heading(company, level=0)
            query = 'org:"%s"' % company
            results = self.search_shodan_api(query, limit)
            for host in results:
                address = host['ip_str']
                port = host['port']

                if not host['hostnames']:
                    host['hostnames'] = [None]

                for hostname in host['hostnames']:
                    self.add_ports(ip_address=address, port=port, host=hostname)
                    self.add_hosts(host=hostname, ip_address=address)
