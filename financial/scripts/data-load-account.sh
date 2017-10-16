#!/bin/bash
set -e;

[[ -z "$1" ]] && echo "Usage: data-load-account.sh /path/to/file_to_load.csv" && exit 1;
headers=$(cat ${1/.csv/.hdr} | tr ';' ',')
lily csv-bulk-loader -i file://$1 -t account -s 2014-01-01T00:00:00.000Z -d ';' -c ${headers}
