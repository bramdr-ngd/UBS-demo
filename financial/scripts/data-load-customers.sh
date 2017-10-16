#!/bin/bash
set -e;

[[ -z "$1" ]] && echo "Usage: data-load-customers.sh /path/to/file_to_load.csv" && exit 1;
headers=$(cat ${1/.csv/.hdr} | tr ';' ',')
lily csv-bulk-loader -i file://$1 -t customer_crm -s 2014-01-01T00:00:00.000Z -d ';' -c ${headers}

## Removed columns:
# total_referrals
# score_churn

## Original columns
# id,segment,segnr,age_category,age,gender,OCCUPATION,LIFESTAGE,FLAG_STUDENT,FLAG_RETIRED,EDUCATION,MARITAL_STATUS,MONTHLY_INCOME,MONTHLY_INCOME_REAL,NBR_CHILDREN,FLAG_HOUSE_OWNER,FLAG_HOME_TENANT,FLAG_VALUE_PROPERTY,NBR_PROPERTIES_OWNED,FLAG_LANDLORD,FLAG_WEALTHY_REGION,SHARE_OF_WALLET,SHARE_OF_WALLET_HOLDINGS,SHARE_OF_WALLET_SIZE,TOTAL_BANK_PRODUCTS,FLAG_PFSP,SATISFACTION,FLAG_ONLINE_BANKING,FLAG_ONLINE_BILL_PAYMENT,FLAG_MOBILE_PAYMENT,FLAG_RELOADABLE_PREPAID_CARDS,TOTAL_ASSETS,AFF_NIGHT_LIFE,AFF_SPORT,AFF_HEALTH_FITNESS,AFF_OUTDOOR,AFF_LUXURY_SHOPPER,AFF_MOVIE,AFF_PET_LOVERS,AFF_FAST_FOOD,AFF_VALUE_SHOPPER,AFF_TECHNOPHILES,AFF_GREEN_LIVING,AFF_MUSIC,title,first_name,middle_name,last_name,street_address,res_city,state,zipcode,res_country,email_address,phone_number