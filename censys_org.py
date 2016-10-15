from recon.core.module import BaseModule
import json

class Module(BaseModule):

    meta = {
        'name': 'Censys.io Org Enumerator',
        'author': 'ScumSec 0x1414',
        'description': 'Harvests hosts from the Censys.IO API by using the \'autonomous_system.organization\' search operator. Updates the \'hosts\' and the \'ports\' tables with the results.',
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
    }

    def module_run(self, companies):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        base_url = 'https://censys.io/api/v1/search/ipv4'
        for company in companies:
            self.heading(company, level=0)
            payload = json.dumps({'query': 'autonomous_system.organization:"%s"' % company})
            resp = self.request(base_url, payload=payload, auth=(api_id, api_secret), method='POST', content='JSON')
            # print resp.json
            if resp.status_code == 200:
                pages = resp.json['metadata']['pages']

                for element in resp.json['results']:
                    ip_address = element['ip']
                    self.add_hosts(ip_address=ip_address)
                    for protocol in element['protocols']:
                        port, service = protocol.split('/')
                        self.add_ports(ip_address=ip_address, port=port, protocol=service)
                if pages > 1:
                    for i in range(pages)[1:]:
                        page_id = i + 1
                        payload = json.dumps({'page': page_id, 'query': 'autonomous_system.organization:"%s"' % company})
                        resp = self.request(base_url, payload=payload, auth=(api_id, api_secret), method='POST', content='JSON')
                        if resp.status_code == 200:
                            for element in resp.json['results']:
                                ip_address = element['ip']
                                self.add_hosts(ip_address=ip_address)
                                for protocol in element['protocols']:
                                    port, service = protocol.split('/')
                                    self.add_ports(ip_address=ip_address, port=port, protocol=service)

            else:
                self.output('%s => Bad request!' % company)