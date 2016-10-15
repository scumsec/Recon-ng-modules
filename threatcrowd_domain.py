from recon.core.module import BaseModule
import time


class Module(BaseModule):

    meta = {
        'name': 'ThreatCrowd API Reverse Whois',
        'author': 'ScumSec 0x1414',
        'description': 'Harvests email address of domain registrant and then crawls all domains registered by this registrant. Updates the \'domains\' table with the results.',
        'query': 'SELECT DISTINCT domain FROM domains WHERE domain IS NOT NULL',
        'comments': (
            'One request \ 10 seconds'
        ),
    }

    def module_run(self, domains):

        for domain in domains:
            self.heading(domain, level=0)
            base_url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/'
            payload = {'domain': domain}
            resp = self.request(base_url, payload=payload)
            registrant_emails = []
            if resp.status_code == 200:
                if resp.json['response_code'] == '1':
                    if resp.json['emails']:
                        for email in resp.json['emails']:
                            if email.endswith(domain):
                                self.output('%s => Registrant email found!' % email)
                                registrant_emails.append(email)
                    else:
                        self.alert('%s => No registrant emails found!' % domain)
                else:
                    self.alert('%s => No data about this domain!' % domain)
            else:
                self.alert('%s => Bad request!' % domain)
            # "Please limit all requests to no more than one request every ten seconds."
            # https://github.com/threatcrowd/ApiV2#limits
            time.sleep(10)
            for registrant_email in registrant_emails:
                self.heading(registrant_email, level=0)
                base_url = 'https://www.threatcrowd.org/searchApi/v2/email/report/'
                payload = {'email': registrant_email}
                resp = self.request(base_url, payload=payload)
                if resp.status_code == 200:
                    if resp.json['response_code'] == '1':
                        if resp.json['domains']:
                            for new_domain in resp.json['domains']:
                                if new_domain:
                                    self.add_domains(new_domain)
                        else:
                            self.alert('%s => No new domains by registrant email!' % registrant_email)
                    else:
                        self.alert('%s => No data about this registrant email!' % registrant_email)
                else:
                    self.alert('%s => Bad request!' % registrant_email)
                time.sleep(10)

