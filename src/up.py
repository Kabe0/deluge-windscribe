import os
import re
import subprocess
import socket
import netifaces
import netaddr
# import pyufw
import pprint

# Based on the following documentation
# https://www.linode.com/docs/networking/vpn/vpn-firewall-killswitch-for-linux-and-macos-clients/

UseUFW = bool(os.getenv('USE_UFW', False))

# Used for some of the print outputs
pp = pprint.PrettyPrinter(indent=4)

dnss = os.getenv('VPN_DNS', '8.8.8.8,8.8.4.4').split(",")

addrs = netifaces.ifaddresses('eth0')
ipinfo = addrs[socket.AF_INET][0]
address = ipinfo['addr']
netmask = ipinfo['netmask']

# Create ip object and get 
dockeraddress = netaddr.IPNetwork('%s/%s' % (address, netmask))

vpnname = None
vpnport = None

# Find the matching remote config in the config.ovpn file.
# for line in open('/config/config.ovpn'):
#     match = re.search('remote\s*([\w.-]*)\s*(\d*)', line)
#     if match:
#         vpnname = match.group(1)
#         vpnport = match.group(2)
#         break

# Configure the UFW default details


# Set the DNS configs
with open("/etc/resolv.conf", "w") as myfile:
    myfile.truncate()
    for dns in dnss:
        myfile.write(f"nameserver {dns}\n")
    myfile.close()

# Grab all the domain ip addresses
# result = socket.getaddrinfo(vpnname, None, socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP, socket.AI_CANONNAME)
# list = [x[4][0] for x in result]

# if UseUFW:
    # pyufw.reset(True)
    # pyufw.default("deny", "deny", "allow")
    # pyufw.add("allow in on tun0")
    # pyufw.add("allow out on tun0")
    #
    # # Assign the docker cidr to the firewall
    # pyufw.add(f"allow in on eth0 from {dockeraddress.cidr}")
    # pyufw.add(f"allow out on eth0 to {dockeraddress.cidr}")
# else:
# subprocess.run(["/sbin/iptables", "--flush"])
# subprocess.run(["/sbin/iptables", "--delete-chain"])
# subprocess.run(["/sbin/iptables", "-t", "nat", "--flush"])
# subprocess.run(["/sbin/iptables", "-t", "nat", "--delete-chain"])
# subprocess.run(["/sbin/iptables", "-P", "OUTPUT", "DROP"])
subprocess.run(["/sbin/iptables", "-A", "INPUT", "-j", "ACCEPT", "-i", "lo"])
subprocess.run(["/sbin/iptables", "-A", "OUTPUT", "-j", "ACCEPT", "-o", "lo"])

# Assign the docker cidr to the firewall
subprocess.run(["/sbin/iptables", "-A", "INPUT", "--src", f"{dockeraddress.cidr}", "-j", "ACCEPT", "-i", "eth0"])
subprocess.run(["/sbin/iptables", "-A", "OUTPUT", "-d", f"{dockeraddress.cidr}", "-j", "ACCEPT", "-o", "eth0"])

subprocess.run(
    ["/sbin/iptables", "-A", "OUTPUT", "-j", "ACCEPT", "-p", "tcp", "-m", "conntrack",
     "--ctstate", "NEW,ESTABLISHED", "--dport", f"8112"])
subprocess.run(
    ["/sbin/iptables", "-A", "INPUT", "-j", "ACCEPT", "-p", "tcp", "-m", "conntrack",
     "--ctstate", "ESTABLISHED", "--sport", f"8112"])

# Assign each IP to the UFW firewall list
# for vpnip in list:
#
#     # if UseUFW:
#     #     pyufw.add(f"allow out on eth0 to {vpnip} port {vpnport}")
#     #     pyufw.add(f"allow in on eth0 from {vpnip} port {vpnport}")
#     # else:
#     subprocess.run(
#         ["/sbin/iptables", "-A", "OUTPUT", "-j", "ACCEPT", "-d", f"{vpnip}", "-o", "eth0", "-p", "udp", "-m",
#          "udp", "--dport", f"{vpnport}"])
#     subprocess.run(
#         ["/sbin/iptables", "-A", "INPUT", "-j", "ACCEPT", "-s", f"{vpnip}", "-i", "eth0", "-p", "udp", "-m",
#          "udp", "--sport", f"{vpnport}"])


# Turn on the firewall
# if UseUFW:
#     pyufw.enable()
#     pp.pprint(pyufw.status())
# else:
subprocess.run(["/sbin/iptables", "-A", "INPUT", "-j", "ACCEPT", "-i", "tun0"])
subprocess.run(["/sbin/iptables", "-A", "OUTPUT", "-j", "ACCEPT", "-o", "tun0"])

# Run the processes
# subprocess.Popen(["/usr/bin/python3", "/usr/bin/run.py"])
