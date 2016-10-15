from recon.core.module import BaseModule
import csv
import json
from string import ascii_uppercase
from lxml import html
from urllib2 import HTTPError

class Module(BaseModule):
    meta = {
        'name': 'XING employee grabber',
        'author': 'Michael Helwig (@c0dmtr1x)',
		'description': 'Imports employee list from a XING company page to contacts and profiles tables. Iterates through the alphabet and grabs data for each letter with up to LIMIT results.',
        'options': (
            ('cookie', None, False, 'Cookie data from your current XING login. You might get more data when logged in. At least "_session_id" and "login" parameters are needed.'),
            ('limit', 500, True, 'Limit of employees per letter'),
         ),
        'query': 'SELECT DISTINCT company FROM companies WHERE company IS NOT NULL',
    }

    __xing_cookie = None
    __limit = None
    __titles = ['Dr.','Prof.']
    __xing_url = 'https://www.xing.com'
    __url_variants = ['companies', 'company'] #url for company pages varies, so we query both
    
    def __init__(self, *args, **kwargs):
        result = BaseModule.__init__(self, *args, **kwargs)
        return result
    
    def do_set(self, *args, **kwargs):
        BaseModule.do_set(self, *args, **kwargs)

    def module_run(self, companies):
        self.__init_options()
        for company in companies:
            for slug in self.__url_variants:
                self.__query_xing(company,slug)

    def __parse_data(self,jsondata):
        if not jsondata or len(jsondata) == 0:    
            return
        k = list(jsondata["contacts"].keys())
        htmlstring = jsondata["contacts"][k[0]]["html"]
        for htmlentry in htmlstring:
            tree = html.fromstring(htmlentry)
            employee = tree.xpath('//a[@class="user-name-link"]/text()')
            position = tree.xpath('//ul[@class="user-card-information"]/li[3]/text()')

            if(len(employee) == 0):
                continue

            employee_names = employee[0].split(' ')
            employee_first = None
            employee_middle = None
            employee_last = None
            title_idx = -1

            for name in employee_names:
                name_is_title = False
                for title in self.__titles:
                    if name.find(title) != -1:
                        name_is_title = True
                if name_is_title:
                    continue
                else:               
                    employee_first = name
                    break

            idx = employee_names.index(employee_first)
            employee_names = employee_names[idx:]
            if(len(employee_names) > 2):
                employee_middle = " ".join(employee_names[1:len(employee_names)-1])
            if(len(employee_names) > 1):
                employee_last = employee_names[len(employee_names) - 1]     
            employee_profile = tree.xpath('//a[@class="user-name-link"]/@href')
            employee_profile_link = self.__xing_url +"/" + employee_profile[0];            
            employee_username = employee_profile[0][len('/profile/'):]
            employee_username = employee_username.split('/')
            employee_profile_link = self.__xing_url  + "/profile/" + employee_username[0];
            
            self.add_profiles(username=employee_username[0], url=employee_profile_link, resource='Xing', category='social')            
            if employee_middle:
                self.add_contacts(first_name=self.__normalize_name(employee_first), middle_name =self. __normalize_name(employee_middle), last_name=self.__normalize_name(employee_last), title=self.__normalize_name(position[0]))
            else:
                self.add_contacts(first_name=self.__normalize_name(employee_first), last_name=self.__normalize_name(employee_last), title=self.__normalize_name(position[0]))


    def __init_options(self):
        self.__xing_cookie = self.options['cookie']
        self.__limit = self.options['limit']
        return

    # try to normalize (capitalize) names
    def __normalize_name(self,name):
        if name == None:
            return None
        normalized_name = name.capitalize()
        if normalized_name.find('-') != -1:
            idx = normalized_name.find('-')
            if(len(normalized_name) > idx):
                normalized_name = normalized_name[0:idx+1] + normalized_name[idx+1].capitalize() + normalized_name[idx+2:]
        return normalized_name


    def __query_xing(self,company,slug):
        headers = {}
        if self.__xing_cookie is not None:
            headers['Cookie'] = self.__xing_cookie
        for c in ascii_uppercase:
            data = []
            url = self.__xing_url + '/' + slug + '/' + company.replace(" ","").lower() + '/employees.json?filter=all&letter=' + c +'&limit=500&offset=0'
            self.debug("Retrieving url: " + url)
            try:
                r = self.request(url=url,headers=headers)
            except HTTPError as exception:
                self.debug("Could not retrieve url.")
                continue
            if r.status_code != 200:
                self.debug("No data retrieved.")
                continue
            else:
                self.__parse_data(r.json)
