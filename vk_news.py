from recon.core.module import BaseModule
import time
import re


class Module(BaseModule):

    meta = {
        'name': 'VK.com newsfeed API contacts enumerator',
        'author': 'ScumSec @0x1414',
        'description': 'Harvests emails from VK.com newsfeed using @domain.com as input. Updates the \'contacts\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'comments': (
            'Three requests per second.',
        )
    }

    def get_emails(self, text):
        """Function to get list of email addresses from text"""
        email_pattern = re.compile('[a-zA-Z_.+-]+@[a-zA-Z-]+\.[a-zA-Z-.]+')
        try:
            return re.findall(email_pattern, text)
        except Exception as e:
            return []

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

    def module_run(self, domains):
        access_token = self.get_key('vk_key')
        base_url = 'https://api.vk.com/method/newsfeed.search'

        for domain in domains:
            self.heading(domain, level=0)
            payload = {'v': '5.12', 'access_token': access_token, 'lang': 3, 'count': 200, 'q': '@' + domain}
            resp = self.request(base_url, payload=payload)
            # print resp.json
            if resp.status_code == 200:
                count = resp.json['response']['count']
                # print len(resp.json['response']['items'])
                for post in resp.json['response']['items']:
                    text = post['text']
                    emails = self.get_emails(text)
                    for email in emails:
                        if email.split('@')[0]:
                            if email.endswith(domain):
                                user_info = self.get_name(email, 'VK.com newsfeed')
                                self.add_contacts(**user_info)
                if count > 200:
                    iterations = count // 200
                    if iterations > 4:
                        iterations = 4
                    for i in range(1, iterations + 1):
                        payload = {'v': '5.12', 'access_token': access_token, 'lang': 3, 'count': 200,
                                   'q': '@' + domain, 'offset': 200*i}
                        # print 'OFFSET' + str(200*i)
                        resp = self.request(base_url, payload=payload)
                        # print resp.json
                        if resp.status_code == 200:
                            # print len(resp.json['response']['items'])
                            for post in resp.json['response']['items']:

                                text = post['text']
                                emails = self.get_emails(text)
                                for email in emails:
                                    if email.split('@')[0]:
                                        if email.endswith(domain):
                                            user_info = self.get_name(email, 'VK.com newsfeed')
                                            self.add_contacts(**user_info)
                        time.sleep(0.34)
            time.sleep(0.34)
