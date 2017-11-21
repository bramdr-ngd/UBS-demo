#!/bin/bash
set -e;

[[ -z "$1" ]] && echo "Usage: data-load-account_role.sh /path/to/file_to_load.csv" && exit 1;
#headers=$(cat ${1/.csv/.hdr} | tr ';' ',')
#lily csv-bulk-loader -i file://$1 -t account_role -s 2014-01-01T00:00:00.000Z -d ';' -c ${headers}
lily csv-bulk-loader -i file://$1  -t account_role -d ';' -s 2014-01-01T00:00:00.000Z -c customer_id,account_id,role;
