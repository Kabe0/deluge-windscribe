import subprocess
import os
import shutil

if not os.path.exists("~/.config/deluge"):
    os.makedirs("~/.config/deluge")


# shutil.copyfile("/root/.bashrc", "")
# os.path.c

DEL_UID = os.getenv("DEL_UID", 1000)
DEL_GID = os.getenv("DEL_GID", 1000)
DEL_PORT = os.getenv("DEL_PORT", 58846)

if DEL_UID != 1000:
    subprocess.run(["/usr/sbin/usermod", "-u", f"{DEL_UID}", "deluge"])
if DEL_GID != 1000:
    subprocess.run(["/usr/sbin/groupmod", "-g", f"{DEL_GID}", "deluge"])

webCmd = ["su", "deluge", "-c", "/usr/bin/deluge-web"]
webPort = os.getenv("WEB_PORT", None)

if webPort:
    webCmd.append("-p")
    webCmd.append(webPort)

subprocess.Popen(webCmd)
subprocess.run(["su", "deluge", "-c", f"\"/usr/bin/deluged --do-not-daemonize -p {DEL_PORT}\""], shell=True)
