#!/usr/bin/env bash
DEL_PORT="$1"
DEL_INT="$2"

su deluge -c "/usr/bin/deluged -U deluge --do-not-daemonize -o ${DEL_INT} -p ${DEL_PORT}"
