from recon.core.module import BaseModule
import xml.etree.ElementTree as ET
import subprocess
import tempfile
import shlex

class Module(BaseModule):
    meta = {
        'name': 'Network Mapper (Nmap)',
        'author': 'Nihaal Prasad',
        'description': 'Uses the network mapper (nmap) to probe known hosts one at a time for open ports and protocols.',
        'comments': (
            'Only hosts with known ip addresses will be probed.',
            'The ports table will be updated to include the following: ip address, host, port, protocol, and module.',
            'This module temporarily outputs nmap XML files in the /tmp directory while running, but deletes them immidiately afterwards.',
        ),
        'query': 'SELECT DISTINCT host, ip_address FROM hosts WHERE ip_address IS NOT NULL',
        'options': (
            ('flags', '-sS', True, 'Scan options used for Nmap.'),
        ),
    }

    # Saves the output to the ports table
    def save_scan(self, host, ip, f):
        # Open the xml file outputted from the nmap scan
        tree = ET.parse(f)
        root = tree.getroot()

        # Parse the xml file outputted from the nmap scan
        for port in root.iter("port"):
            # Parse the portid
            portid = port.get('portid')
            
            # Parse the service running on the port
            for service in port.iter('service'):
                service = service.get('name')

                # Add the port to the ports table
                self.add_ports(ip_address=ip, host=host, port=portid, protocol=service)

        # Delete the xml file
        proc = subprocess.Popen(shlex.split("sudo rm " + f))

    # Runs the module
    def module_run(self, hosts):
        # Loop through each host
        for host, ip in hosts:
            # Make sure that there is an ip address associated with that host
            if(ip != None):
                # Create a temporary xml file to output to
                f = tempfile.gettempdir() + "/" + ip + ".xml"

                # Create the command to run
                cmd = "sudo nmap " + self.options['flags'] + " -oX " + f + " " + ip

                # Start the process to run the command
                proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
                # Print the output to the screen
                for line in proc.stdout:
                    self.output(line)

                # Alert the user that the scan for the current ip address has finished
                self.alert("Scan for " + host + " finished.")
        
                # Save output in the ports table when the nmap scan is finished
                self.save_scan(host, ip, f)