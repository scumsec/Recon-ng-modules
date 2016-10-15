from recon.core.module import BaseModule
from bs4 import BeautifulSoup
import re
import os


class Module(BaseModule):

    meta = {
        'name': 'Import theHarvester XML',
        'author': 'ScumSec 0x1414',
        'description': 'Imports emails, hosts and virtual hosts from theHarvester XML. Updates the \'contacts\' and \'hosts\' tables.',
        'options': (
            ('filename', None, True, 'Path and filename for theHarvester XML input'),
            ('domain', None, True, 'Filter all data endswith domain name'),
        ),
    }

    def get_name(self, email, title):

        def up(name_part):
            return name_part[0].upper() + name_part[1:]

        answer = {}
        parts = re.findall('[a-z]+', email.lower().split('@')[0])
        if len(parts) == 2:
            answer.update({'first_name': up(parts[0]), 'middle_name': None, 'last_name': up(parts[1]), 'email': email, 'title': title})
        elif len(parts) == 3:
            answer.update({'first_name': up(parts[0]), 'middle_name': up(parts[1]), 'last_name': up(parts[2]), 'email': email, 'title': title})
        else:
            answer.update({'first_name': None, 'middle_name': None, 'last_name': None, 'email': email, 'title': title})
        return answer

    def module_run(self):
        domain = self.options['domain']
        filename = self.options['filename']
        if domain:
            if os.path.exists(filename):
                with open(filename) as xml_file:
                    xml_data = xml_file.read()
                    soup = BeautifulSoup(xml_data, 'xml')
                    for host in soup.find_all('host'):
                        hostname = host.find('hostname')
                        ip = host.find('ip')
                        if hostname and ip:
                            if hostname.string.endswith(domain):
                                self.add_hosts(ip_address=ip.string, host=hostname.string)
                        else:
                            if host.string.endswith(domain):
                                self.add_hosts(host.string)

                    for vhost in soup.find_all('vhost'):
                        hostname = host.find('hostname')
                        ip = host.find('ip')
                        if hostname and ip:
                            if hostname.string.endswith(domain):
                                self.add_hosts(ip_address=ip.string, host=hostname.string)
                        else:
                            if vhost.string.endswith(domain):
                                self.add_hosts(vhost.string)

                    for email in soup.find_all('email'):
                        if email.string.split('@')[0]:
                            if email.string.endswith(domain):
                                user_data = self.get_name(email.string, 'theHarvester import')
                                self.add_contacts(**user_data)
