#!/bin/bash

./data-generate-customers.py -n 50000 -o /disk1/current/ -m ./data-generate-model/
./data-generate-products.py -o /disk1/current/ -m ./data-generate-model -c /disk1/current/CrmDataToFilter.csv
./data-generate-account.py -o /disk1/current/ -m ./data-generate-model -c /disk1/current/EntityDataAll.csv
./data-generate-account_role.py  -o /disk1/current/ -m ./data-generate-model -c /disk1/current/EntityDataAll.csv 
./data-generate-itx.py -n 6 -o /disk1/current -m ./data-generate-model/

./data-generate-DemoPersona.py -o /disk1/current/
./data-generate-DemoPersona-products.py -o /disk1/current/
./data-generate-DemoPersona-Account.py -o /disk1/current/
./data-generate-DemoPersona-AccountRole.py -o /disk1/current/
./data-generate-itx-DemoPersona.py -o /disk1/current

./data-load-customers.sh /disk1/current/CrmDataToLoad.csv
./data-load-products.sh /disk1/current/EntityDataToLoad.csv
./data-load-account.sh /disk1/current/AccountData.csv
./data-load-account_role.sh /disk1/current/AccountRoleData.csv

./data-load-customers.sh /disk1/current/DemoPersonaDataToLoad.csv
./data-load-products.sh /disk1/current/DemoPersonaEntityDataAll.csv
./data-load-account.sh /disk1/current/DemoPersonaAccountData.csv
./data-load-account_role.sh /disk1/current/DemoPersonaAccountRoleData.csv

./data-reload-itx.sh /disk1/current
