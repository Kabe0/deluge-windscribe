import os
import subprocess
import pexpect
import time

print('Initializing Container')

with open('/config/auth.conf') as f:
    lines = f.read().splitlines()
    if len(lines) < 2:
        raise Exception("auth.conf is malformed. Please ensure that the file is configured correctly so that "
                        "windscribe can login.")
    username = lines[0]
    password = lines[1]

subprocess.run(["windscribe", "start"])

child = pexpect.spawn('windscribe login')
child.expect('Windscribe Username: ')
# time.sleep(0.5)
child.sendline(username)
child.expect('Windscribe Password: ')
# time.sleep(0.5)
child.sendline(password)

subprocess.run(["windscribe", "connect"])

print('Initializing Deluge')

subprocess.run(["/usr/bin/python3", "/usr/bin/run.py"])
