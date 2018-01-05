mkdir -p ~/.recon-ng/modules/import
cp nmap_xml.py ~/.recon-ng/modules/import
cp theharvester_xml.py ~/.recon-ng/modules/import
cp simplyemail_json.py ~/.recon-ng/modules/import

mkdir -p ~/.recon-ng/modules/recon/companies-contacts
cp vk_companies.py ~/.recon-ng/modules/recon/companies-contacts
cp xing_employees.py ~/.recon-ng/modules/recon/companies-contacts

mkdir -p ~/.recon-ng/modules/recon/domains-contacts
cp vk_news.py ~/.recon-ng/modules/recon/domains-contacts
cp email_format.py ~/.recon-ng/modules/recon/domains-contacts
cp emailhunter.py ~/.recon-ng/modules/recon/domains-contacts

mkdir -p ~/.recon-ng/modules/recon/companies-hosts
cp shodan_org.py ~/.recon-ng/modules/recon/companies-hosts
cp censys_org.py ~/.recon-ng/modules/recon/companies-hosts

mkdir -p ~/.recon-ng/modules/recon/contacts-credentials
cp hacked_emails.py  ~/.recon-ng/modules/recon/contacts-credentials

mkdir -p ~/.recon-ng/modules/recon/contacts-profiles
cp vibeapp.py ~/.recon-ng/modules/recon/contacts-profiles

mkdir -p ~/.recon-ng/modules/recon/domains-hosts
cp baidu_site.py ~/.recon-ng/modules/recon/domains-hosts
cp axfr.py ~/.recon-ng/modules/recon/domains-hosts
cp mx-ip.py ~/.recon-ng/modules/recon/domains-hosts
cp spf-ip.py ~/.recon-ng/modules/recon/domains-hosts
cp threatcrowd_api.py ~/.recon-ng/modules/recon/domains-hosts
cp censys_mx.py ~/.recon-ng/modules/recon/domains-hosts
cp zoomeye_hostname.py ~/.recon-ng/modules/recon/domains-hosts
cp dnsdumpster-query.py ~/.recon-ng/modules/recon/domains-hosts

mkdir -p ~/.recon-ng/modules/recon/hosts-netblocks
cp arin.py ~/.recon-ng/modules/recon/hosts-netblocks

mkdir -p ~/.recon-ng/modules/recon/domains-domains
cp threatcrowd_domain.py ~/.recon-ng/modules/recon/domains-domains

mkdir -p ~/.recon-ng/modules/recon/hosts-ports
cp censys_a.py ~/.recon-ng/modules/recon/hosts-ports

mkdir -p ~/.recon-ng/modules/recon/hosts-hosts
cp zoomeye_ip.py ~/.recon-ng/modules/recon/hosts-hosts

mkdir -p ~/.recon-ng/modules/recon/netblocks-hosts
cp zoomeye_net.py ~/.recon-ng/modules/recon/netblocks-hosts

for key in `echo "censysio_id
censysio_secret
emailhunter_key
vibeapp_key
vk_key
zoomeye_key"`; do
	echo "INSERT INTO keys (name) VALUES (\"$key\");" | sqlite3 ~/.recon-ng/keys.db
done
