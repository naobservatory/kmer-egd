#!/usr/bin/env bash

while true; do
    echo $(date +%s) $(cat /proc/meminfo | grep MemAvailable)
    sleep 10
done >> mem.log
