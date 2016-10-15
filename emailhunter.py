from recon.core.module import BaseModule
from random import choice
import re


class Module(BaseModule):

    meta = {
        'name': 'EmailHunter Contact Enumerator',
        'author': 'ScumSec @0x1414',
        'description': 'Harvests contacts from emailhunter.co API using domain as input. Updates the \'contacts\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
    }

    def get_name(self, email, title):

        def up(name_part):
            return name_part[0].upper() + name_part[1:]

        answer = {}
        parts = re.findall('[a-z]+', email.lower().split('@')[0])
        if len(parts) == 2:
            answer.update({'first_name': up(parts[0]), 'middle_name': None, 'last_name': up(parts[1]), 'email': email,
                           'title': title})
        elif len(parts) == 3:
            answer.update(
                {'first_name': up(parts[0]), 'middle_name': up(parts[1]), 'last_name': up(parts[2]), 'email': email,
                 'title': title})
        else:
            answer.update({'first_name': None, 'middle_name': None, 'last_name': None, 'email': email, 'title': title})
        return answer

    def module_run(self, domains):
        base_url = 'https://api.emailhunter.co/v1/search'
        api_key = self.get_key('emailhunter_key')

        for domain in domains:
            payload = {'domain': domain, 'api_key': api_key}
            resp = self.request(base_url, payload=payload)
            if resp.status_code == 200:
                amount = resp.json['results']
                if amount == 0:
                    self.output('No emails found.')
                    continue
                for email in resp.json['emails']:
                    email_user_data = self.get_name(email=email['value'], title='EmailHunter contact')
                    self.add_contacts(**email_user_data)
                    #emails.append(email['value'])
                if amount > 100:
                    all_offsets = amount // 100
                    for i in range(1, all_offsets + 1):
                        payload = {'domain': domain, 'api_key': api_key, 'offset': str(i * 100)}
                        resp = self.request(base_url, payload=payload)
                        if resp.status_code == 200:
                            for email in resp.json['emails']:
                                email_user_data = self.get_name(email=email['value'], title='EmailHunter contact')
                                self.add_contacts(**email_user_data)
