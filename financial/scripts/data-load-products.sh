#!/bin/bash
set -e;

[[ -z "$1" ]] && echo "Usage: data-load-products.sh /path/to/file_to_load.csv" && exit 1;

lily csv-bulk-loader -i file://$1  -t customer_product -d ';' -s 2014-01-01T00:00:00.000Z -c customer_product_id,customer_id,name,start_date,end_date,category,sub_category,active,flag_loanpayment,flag_transactionpayment;

