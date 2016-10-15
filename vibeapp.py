from recon.core.module import BaseModule
import time


class Module(BaseModule):

    meta = {
        'name': 'VibeApp Profile Enumerator',
        'author': 'ScumSec 0x1414',
        'description': 'Harvests profiles from the VibeApp API using email addresses as input. Updates the \'profiles\' tables with the results.',
        'query': 'SELECT DISTINCT email FROM contacts WHERE email IS NOT NULL',
    }

    def module_run(self, emails):
        api_key = self.get_key('vibeapp_key')
        base_url = 'https://vibeapp.co/api/v1/profile_lookup/'

        for email in emails:
            payload = {'key': api_key, 'person_email': email}
            # host = base_url % (api_key, email)
            resp = self.request(base_url, payload=payload)
            if resp.status_code == 200:
                #print resp.json
                #print resp.json['profile']['person_data'].keys()
                #if 'social_profiles' not in resp.json:
                #    continue
                person_data = resp.json['profile']['person_data']
                if u'social_profiles' in person_data.keys() and person_data['social_profiles'] is not None:
                    #print person_data['social_profiles']
                    self.output('%s - Found profiles!' % email)
                    for profile in person_data['social_profiles']:
                        if 'username' in profile:
                            username = profile['username']
                        elif profile['url'][-1] != '/':
                            username = profile['url'].split('/')[-1]
                        else:
                            username = None
                        url = profile['url']
                        resource = profile['typeName']
                        category = 'social'
                        self.add_profiles(username=username, resource=resource, url=url, category=category)
                else:
                    self.output('%s - No results found for this Id.' % email)
            time.sleep(1)
