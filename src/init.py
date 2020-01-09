import os
import subprocess
import pexpect

print('Initializing Container')

if os.getenv('VPN_ENABLE', True):
    vpnAuth = os.getenv('VPN_AUTH', "/config/auth.conf")

    with open(vpnAuth) as f:
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

    child.wait()

    child = pexpect.spawn('windscribe connect')
    cond = child.expect(['Please login to use Windscribe', 'Service communication error', pexpect.EOF])
    if cond == 0:
        raise Exception(f"Unable to properly connect to Windscribe. Make sure username/password is correct in the {vpnAuth} file.")
    elif cond == 1:
        raise Exception(f"Unable to properly connect to Windscribe service. Please restart docker.")

    child.wait()

    child = pexpect.spawn('windscribe firewall on')
    cond = child.expect(['Please login to use Windscribe', 'Service communication error', pexpect.EOF])
    if cond == 0:
        raise Exception(f"Unable to properly connect to Windscribe. Make sure username/password is correct in the {vpnAuth} file.")
    elif cond == 1:
        raise Exception(f"Unable to properly connect to Windscribe service. Please restart docker.")

# Sleep to allow for VPN to connect before trying to init python
print('Initializing Deluge')
subprocess.run(["/usr/bin/python3", "/usr/bin/run.py"])
