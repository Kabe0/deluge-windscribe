#!/usr/bin/env bash
DEL_PORT="$1"
DEL_INT="$2"

su deluge -c "/usr/bin/deluged --do-not-daemonize -U deluge -g deluge -o ${DEL_INT} -p ${DEL_PORT}"
