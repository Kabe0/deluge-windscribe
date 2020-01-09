import os
import subprocess
import pexpect
import time

print('Initializing Container')

if os.getenv('VPN_ENABLE', True):
    vpnAuth = os.getenv('VPN_AUTH', "/config/auth.conf")

    with open('/config/auth.conf') as f:
        lines = f.read().splitlines()
        if len(lines) < 2:
            raise Exception("auth.conf is malformed. Please ensure that the file is configured correctly so that "
                            "windscribe can login.")
        username = lines[0]
        password = lines[1]

    subprocess.run(["windscribe", "start"])

    child = pexpect.spawn('windscribe login')

    cond = child.expect(['Already Logged in', 'Windscribe Username: ', pexpect.EOF])
    if cond == 1:
        child.sendline(username)
        child.expect(['Windscribe Password: ', pexpect.EOF])
        child.sendline(password)

    subprocess.run(["windscribe", "connect"])
    subprocess.run(["windscribe", "firewall", "on"])

# Sleep to allow for VPN to connect before trying to init python
print('Initializing Deluge')
subprocess.run(["/usr/bin/python3", "/usr/bin/run.py"])
