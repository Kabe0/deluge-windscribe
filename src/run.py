import subprocess
import os

DEL_UID = os.getenv("DEL_UID", 1000)
DEL_GID = os.getenv("DEL_GID", 1000)
DEL_PORT = os.getenv("DEL_PORT", 58846)
DEL_INT = os.getenv('DEL_INT', 'tun0')

print("Configuring firewall settings")
os.popen("ip route del 128.0.0.0/1")

if DEL_UID != 1000:
    subprocess.run(["/usr/sbin/usermod", "-u", f"{DEL_UID}", "deluge"])
if DEL_GID != 1000:
    subprocess.run(["/usr/sbin/groupmod", "-g", f"{DEL_GID}", "deluge"])

if not os.path.exists("/config/.config/deluge"):
    print("Making config directory.")
    os.makedirs("/config/.config/deluge")
    subprocess.run(["cp", "/usr/local/etc/core.conf", "/config/.config/deluge/"])
    subprocess.run(["chown", "-R", f"{DEL_UID}:{DEL_GID}", "/config/.config"])

webCmd = ["su", "deluge", "-c", "/usr/bin/deluge-web"]
webPort = os.getenv("WEB_PORT", None)

if webPort:
    webCmd.append("-p")
    webCmd.append(webPort)

subprocess.Popen(webCmd)
print("Deluged Init")
# subprocess.run(["/usr/bin/deluged", "--do-not-daemonize", "-U", "deluge", "-g", "deluge", "-o", DEL_INT])
subprocess.run(["/usr/bin/run.sh", DEL_PORT, DEL_INT])
