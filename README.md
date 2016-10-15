# Recon-ng additional modules
Based on [Recon-ng](bitbucket.org/LaNMaSteR53/recon-ng) project.

This project includes some modules from multiple sources and projects such as [Pentestly](https://github.com/praetorian-inc/pentestly) by @praetorian-inc. Modules without hyperlinks are my own. The main goal of this project is to make search with Recon-ng more useful, add alternative data sources and put all extra modules in one place.

## New import modules
 
##### [import/nmap_xml](https://github.com/praetorian-inc/pentestly/blob/master/modules/import/nmap_xml.py)
Import from [nmap](http://nmap.org/) XML output. Module updates `hosts` and `ports` tables with the results.
##### import/theharvester_xml
Import from [theHarvester](https://github.com/laramies/theHarvester) (by @laramies) XML output. Module updates `contacts` table with emails, found by theHarvester and try to resolve name of contact:
>john.smith@example.com -> John Smith

>john.d.smith@example.com -> John D Smith
 

Additionaly, module updates `hosts` table with hosts and virtual hosts, found by theHarvester. If theHarvester resolved hostname to IP address, module adds them both. Otherwise, module adds only the hostname.
##### import/simplyemail_json
Import from [SimplyEmail](https://github.com/killswitch-GUI/SimplyEmail) (by @killswitch-GUI) JSON output. Module updates `contacts` table with emails, found by SimplyEmail and try to resolve name of contact.

## Modules based on vk.com API
Website: https://vk.com/dev
##### recon/companies-contacts/vk_companies
Find employees by company name on vk.com. Module uses [users.search](https://vk.com/dev/users.search) method of VK API with `company` parameter to find all employees by company name.

##### recon/domains-contacts/vk_news
Find emails by company domain on vk.com in 1000 last posts. Module uses [newsfeed.search](https://vk.com/dev/newsfeed.search) method of VK API with `q` parameter to find email addresses by domain and try to resolve name of contact.
>Example

>domain: mysite.com

>search query: @mysite.com

### Some random modules
##### [recon/companies-contacts/xing_employees](https://github.com/mhelwig/xing_employees/blob/master/xing_employees.py) by @mhelwig
Website: 
##### recon/companies-hosts/shodan_org
Find hosts and open ports by `org` search operator using Shodan API. Updates `hosts` and `ports` tables with the results.
##### recon/contacts-credentials/hacked_emails
Module uses hacked-emails.com API to find compromised credentials. Website: http://hacked-emails.com/
##### recon/contacts-profiles/vibeapp
Module works with VibeApp API which is the same as FullContact API. Module finds profiles. Website: http://vibeapp.co
##### recon/domains-contacts/email_format
Module scrapes email-format.com for emails and try to resolve name of contact. Website: http://email-format.com
##### recon/domains-contacts/emailhunter
Module harvests emails using EmailHunter API and try to resolve name of contact. Website: https://emailhunter.co/
##### [recon/domains-hosts/baidu_site](https://github.com/F4l13n5n0w/recon-ng-baidu_site-module-rewrite/blob/master/baidu_site.py) by @F4l13n5n0w
Module scrapes hosts from Baidu Search Engine. Website: 
##### [recon/hosts-netblocks/arin](https://github.com/ztgrace/recon_scripts/blob/master/arin.py) by @ztgrace
Module uses ARIN API to search for netblocks and companies by IP address.

## DNS-based modules
##### [recon/domains-hosts/axfr](https://github.com/ztgrace/recon_scripts/blob/master/axfr.py) by @ztgrace
AXFR (DNS Zone Transfer)
##### [recon/domains-hosts/mx-ip](https://bitbucket.org/KoreLogicSecurity/recon-ng/src/493ada1d7f77bd10989e380bd4bf217614eb0855/modules/recon/hosts-hosts/mx-ip.py)
MX record (Mail eXchanger)
##### [recon/domains-hosts/spf-ip](https://bitbucket.org/KoreLogicSecurity/recon-ng/src/458bcc977fd009bbfe3b68c916b7d9f33ff33daf/modules/recon/hosts-hosts/spf-ip.py)
SPF record (Sender Policy Framework)

## ThreatCrowd API modules
Website: https://www.threatcrowd.org/
##### recon/domains-domains/threatcrowd_domain
Search for domains registered by same email address of registrant
##### recon/domains-hosts/threatcrowd_api
Renamed module from standard repository

## Censys API modules
Website: https://censys.io/
##### recon/companies-hosts/censys_org
Module searchs for hosts and ports using `autonomous_system.organization` search filter. Updates the `hosts` and the `ports` tables with the results.
##### recon/domains-hosts/censys_mx
Module retrieves MX record for each domain using `mx` search filter and updates the `hosts` table with the results.!!!!!
##### recon/hosts-ports/censys_a
Module retrieves A record for each host using `a` search filter and updates the `ports` with the results. !!!!!!!!!!!!!! 

## ZoomEye API modules
Website: https://www.zoomeye.org/
##### recon/hosts-hosts/zoomeye_ip
Find ports by IP address using ZoomEye API
##### recon/netblocks-hosts/zoomeye_net
Find hosts and ports using ZoomEye API
##### recon/domains-hosts/zoomeye_hostname
Find hosts by hostname using ZoomEye API

>#### How to get access_token?
>
>~~~
>curl -XPOST https://api.zoomeye.org/user/login -d '{"username": "your@mail.com", "password": "Pa55w0rd"}'
>~~~

# Keys
For solving keys file problem just add manualy these keys:
- `zoomeye_key`
- `vibeapp_key`
- `vk_key`
- `emailhunter_key`


# Thanks

# TODO
- [ ] Fix domainbigdata modules

