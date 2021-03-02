#!/usr/bin/env bash
DEL_PORT="$1"
DEL_INT="$2"
su deluge -c "/usr/bin/deluged -U deluge -o ${DEL_INT} -p ${DEL_PORT}"
[[ ! -f /opt/tinyproxy/start.sh ]] || /opt/tinyproxy/start.sh