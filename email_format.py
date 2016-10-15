from recon.core.module import BaseModule
import time
import re


class Module(BaseModule):

    meta = {
        'name': 'Email-format.com contacts enumerator',
        'author': 'ScumSec @0x1414',
        'description': 'Crawls email-format.com for contacts based on search by domain. Updates the \'contacts\' table.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
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

    def get_emails(self, domain):
        emails = []
        host = 'http://www.email-format.com/d/%s' % domain
        resp = self.request(host)
        for element in resp.raw.split("<div class='fl'>")[1:]:
            emails.append(re.sub('[ \n\t]+', '', element.split('</div>')[0]))
        return emails

    def module_run(self, domains):
        for domain in domains:
            self.heading(domain, level=0)
            new_emails = self.get_emails(domain)
            for new_email in new_emails:
                contact = self.get_name(new_email, 'Email-Format contact')
                self.add_contacts(**(contact))
            time.sleep(1)
