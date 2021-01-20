import os
import subprocess
import pexpect

print('Initializing Container')
if os.getenv('VPN_ENABLE', True).lower() in ['true', '1']:
    vpnAuth = os.getenv('VPN_AUTH', "/config/auth.conf")

    username = os.getenv('VPN_USERNAME')
    password = os.getenv('VPN_PASSWORD')
    location = os.getenv('VPN_LOCATION', 'best')

    if not username and not password:
        print('Using config file /config/auth.conf.')
        with open(vpnAuth, 'rU') as f:
            lines = f.read().splitlines()
            lineCount = len(lines)

            if lineCount < 2:
                raise Exception("auth.conf is malformed. Please ensure that the file is configured correctly so that "
                                "windscribe can login.")
            username = lines[0]
            password = lines[1]

            if lineCount >= 3:
                location = lines[2]
    else:
        print('Using VPN_USERNAME and VPN_PASSWORD to login.')

    subprocess.run(["windscribe", "start"])

    child = pexpect.spawn('windscribe login')

    cond = child.expect(['Already Logged in', 'Windscribe Username: ', pexpect.EOF], timeout=50)
    if cond == 1:
        child.sendline(username)
        child.expect(['Windscribe Password: ', pexpect.EOF])
        child.sendline(password)

    child.wait()

    child = pexpect.spawn(f"windscribe connect {location}")
    cond = child.expect(['Please login to use Windscribe', 'Service communication error', pexpect.EOF], timeout=50)
    if cond == 0:
        raise Exception(f"Unable to properly connect to Windscribe. Make sure username/password is correct in the {vpnAuth} file.")
    elif cond == 1:
        raise Exception(f"Unable to properly connect to Windscribe service. Please restart docker.")

    child.wait()

    child = pexpect.spawn('windscribe firewall on')
    cond = child.expect(['Please login to use Windscribe', 'Service communication error', pexpect.EOF], timeout=50)
    if cond == 0:
        raise Exception(f"Unable to properly connect to Windscribe. Make sure username/password is correct in the {vpnAuth} file.")
    elif cond == 1:
        raise Exception(f"Unable to properly connect to Windscribe service. Please restart docker.")

# Sleep to allow for VPN to connect before trying to init python
print('Initializing Deluge')
subprocess.run(["/usr/bin/python3", "-u", "/usr/bin/run.py"])
