from recon.core.module import BaseModule
import time


class Module(BaseModule):

    meta = {
        'name': 'VK API Contact Enumerator',
        'author': 'ScumSec 0x1414',
        'description': 'Crawls VK.com API using company name as input. Updates the \'profiles\' and the \'contacts\' tables with the results.',
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
        'comments': (
            'Three requests per second.',
        )

    }

    def module_run(self, companies):
        access_token = self.get_key('vk_key')
        base_url = 'https://api.vk.com/method/users.search'
        for company in companies:
            self.heading(company, level=0)
            payload = {'v': '5.53', 'access_token': access_token, 'lang': 3, 'count': 1000, 'company': company}
            resp = self.request(base_url, payload=payload)
            # print resp.json
            if resp.status_code == 200:
                for employee in resp.json['response']['items']:
                    first_name = employee['first_name']
                    last_name = employee['last_name']
                    id = str(employee['id'])
                    vk_page = 'http://vk.com/id' + id
                    self.output('User %s %s - %s' % (first_name, last_name, vk_page))
                    self.add_contacts(first_name=first_name, last_name=last_name, title=company)
                    self.add_profiles(username=id, resource='VK.com', url=vk_page, category='Social')
            time.sleep(0.34)
