from recon.core.module import BaseModule
import json

class Module(BaseModule):

    meta = {
        'name': 'Censys.io MX Record Retriever',
        'author': 'ScumSec 0x1414',
        'description': 'Retrieves the MX records for a domain. Updates the \'hosts\' and the \'ports\' tables with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def module_run(self, domains):
        api_id = self.get_key('censysio_id')
        api_secret = self.get_key('censysio_secret')
        base_url = 'https://censys.io/api/v1/search/ipv4'
        for domain in domains:
            self.heading(domain, level=0)
            payload = json.dumps({'query': 'mx:%s' % domain})
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
                        payload = json.dumps({'page': page_id, 'query': 'mx:%s' % domain})
                        resp = self.request(base_url, payload=payload, auth=(api_id, api_secret), method='POST', content='JSON')
                        if resp.status_code == 200:
                            for element in resp.json['results']:
                                ip_address = element['ip']
                                self.add_hosts(ip_address=ip_address)
                                for protocol in element['protocols']:
                                    port, service = protocol.split('/')
                                    self.add_ports(ip_address=ip_address, port=port, protocol=service)

            else:
                self.output('%s => Bad request!' % domain)
