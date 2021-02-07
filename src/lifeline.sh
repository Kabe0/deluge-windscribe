#!/usr/bin/env bash

/usr/bin/python3 -u /usr/bin/init.py

_kill() {
  echo "Ending Windscribe connection"
  windscribe firewall off
  windscribe disconnect
  windscribe logout
  windscribe stop
}

trap _kill SIGTERM
while true; do :; done
