from recon.core.module import BaseModule

import os
import json
import re

class Module(BaseModule):
    meta = {
        'name': 'Import SimplyEmail JSON',
        'author': 'ScumSec 0x1414',
        'description': 'Imports emails from SimplyEmail JSON',
        'options': (
            ('filename', None, True, 'Path and filename for SimplyEmail JSON input'),
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
        filename = self.options['filename']
        if not os.path.exists(filename):
            raise RuntimeError("File does not exist {}".format(filename))
        with open(filename) as fh:
            data = fh.read()
            json_data = json.loads(data)
            domain = json_data['domain_of_collection']
            emails_data = json_data['emails']
            for element in emails_data:
                email = element['email']
                title = 'SimplyEmail ' + element['module_name']
                # fix for google parser errors and emailhunter trial
                if '..' in email or '**' in email:
                    continue
                else:
                    user_data = self.get_name(email, title)
                    self.add_contacts(**user_data)
