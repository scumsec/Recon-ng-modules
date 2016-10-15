from recon.core.module import BaseModule
import json
import urllib
import netaddr

class Module(BaseModule):

    meta = {
        'name': 'ARIN WHOIS Organization Netblocks',
        'author': 'Tom Steele',
        'version': 'v1.0.0',
        'description': 'Searches ARIN Whois data for netblocks using a propriatry application.',
        'comments': (
        ),
        'options': (
            ('api_url', '', 'yes', 'root URL of HTTP API'),
            ('organization', '', 'yes', 'organization to search for, this can often be found by performing a whois lookup on their main site, e.g. `whois optiv.com` would return Optiv Security Inc.'),
        ),
    }

    def module_run(self):
        url = '{}/search_by_name?name={}'.format(self.options['api_url'], urllib.quote_plus(self.options['organization']))
        self.alert('Sending request: {}'.format(url))
        resp = self.request(url, timeout=1000000)
        if resp.status_code is not 200:
            self.error('Got non 200 response code. Status Code: {}'.format(resp.status_code))
            return
        if resp.json['netblocks'] is None:
            self.alert('Got no results from the API.')
            return
        for netblock in resp.json['netblocks']:
            cidr = netaddr.iprange_to_cidrs(netblock['start_address'], netblock['end_address'])
            self.add_netblocks(str(cidr[0]))

