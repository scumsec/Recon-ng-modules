from recon.core.module import BaseModule
import re


class Module(BaseModule):

    meta = {
        'name': 'ZoomEye Networks Enumerator',
        'author': 'ScumSec 0x1414',
        'description': 'Harvests hosts and ports from the ZoomEye API by converting netblock to IPs list and using the \'ip\' search operator. Updates the \'hosts\' anf the \'ports\' tables with the results.',
        'query': 'SELECT DISTINCT netblock FROM netblocks WHERE netblock IS NOT NULL',
    }

    def module_run(self, netblocks):
        access_token = self.get_key('zoomeye_key')
        headers = {'Authorization': 'JWT ' + access_token}

        for netblock in netblocks:
            self.heading(netblock, level=0)
            ip_addreses = self.cidr_to_list(netblock)
            for ip_address in ip_addreses:
                self.heading(ip_address, level=0)
                query = 'ip:%s' % ip_address
                payload = {'query': query}
                resp = self.request('https://api.zoomeye.org/host/search', method='GET', headers=headers, payload=payload)
                if resp.status_code == 200:
                    if 'matches' in resp.json.keys():
                        for match in resp.json['matches']:
                            port_info = match['portinfo']
                            geo_info = match['geoinfo']
                            if port_info['hostname']:
                                host = port_info['hostname']
                            else:
                                host = None
                            ip_address = match['ip']
                            port = port_info['port']
                            protocol = port_info['service']
                            region = geo_info['continent']['names']['en']
                            country = geo_info['country']['names']['en']
                            latitude = geo_info['location']['lat']
                            longitude = geo_info['location']['lon']
                            self.add_ports(ip_address=ip_address, host=host, port=port, protocol=protocol)
                            self.add_hosts(host=host, ip_address=ip_address, region=region, country=country, latitude=latitude, longitude=longitude)
                    else:
                        self.output('%s => No matches!' % ip_address)
                else:
                    self.output('%s => Bad request!' % ip_address)
