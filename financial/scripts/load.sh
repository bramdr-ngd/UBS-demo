#!/bin/bash

date > /var/log/lily-demo-financial/load.log 2>&1

echo 'DATA-GENERATE-CUSTOMERS' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-customers.py -n 50000 -o /disk1/current/ -m ./data-generate-model/ >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-GENERATE-PRODUCTSV2' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-productsv2.py -o /disk1/current/ -m ./data-generate-model -c /disk1/current/CrmDataToFilter.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-GENERATE-ACCOUNT' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-account.py -o /disk1/current/ -m ./data-generate-model -c /disk1/current/EntityDataAll.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-GENERATE-ACCOUNT-ROLE' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-account_role.py  -o /disk1/current/ -m ./data-generate-model -c /disk1/current/EntityDataAll.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-GENERATE-ITX' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-itx.py -n 6 -o /disk1/current -m ./data-generate-model/ >> /var/log/lily-demo-financial/load.log 2>&1

echo 'DATA-GENERATE-DEMOPERSONA' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-DemoPersona.py -o /disk1/current/ >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-GENERATE-DEMOPERSONA-PRODUCTS' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-DemoPersona-products.py -o /disk1/current/ >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-GENERATE-DEMOPERSONA-ACCOUNT' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-DemoPersona-Account.py -o /disk1/current/ >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-GENERATE-DEMOPERSONA-ACCOUNT-ROLE' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-DemoPersona-AccountRole.py -o /disk1/current/ >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-GENERATE-DEMOPERSONA-ITX' >> /var/log/lily-demo-financial/load.log 2>&1
./data-generate-itx-DemoPersona.py -o /disk1/current >> /var/log/lily-demo-financial/load.log 2>&1

echo 'DATA-LOAD-CUSTOMERS' >> /var/log/lily-demo-financial/load.log 2>&1
./data-load-customers.sh /disk1/current/CrmDataToLoad.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-LOAD-PRODUCTS' >> /var/log/lily-demo-financial/load.log 2>&1
./data-load-products.sh /disk1/current/EntityDataToLoad.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-LOAD-ACCOUNT' >> /var/log/lily-demo-financial/load.log 2>&1
./data-load-account.sh /disk1/current/AccountData.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-LOAD-ACCOUNT-ROLE' >> /var/log/lily-demo-financial/load.log 2>&1
./data-load-account_role.sh /disk1/current/AccountRoleData.csv >> /var/log/lily-demo-financial/load.log 2>&1

echo 'DATA-LOAD-DEMOPERSONA-CUSTOMERS' >> /var/log/lily-demo-financial/load.log 2>&1
./data-load-customers.sh /disk1/current/DemoPersonaDataToLoad.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-LOAD-DEMOPERSONA-PRODUCTS' >> /var/log/lily-demo-financial/load.log 2>&1
./data-load-products.sh /disk1/current/DemoPersonaEntityDataToLoad.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-LOAD-DEMOPERSONA-ACCOUNT' >> /var/log/lily-demo-financial/load.log 2>&1
./data-load-account.sh /disk1/current/DemoPersonaAccountData.csv >> /var/log/lily-demo-financial/load.log 2>&1
echo 'DATA-LOAD-DEMOPERSONA-ACCOUNT-ROLE' >> /var/log/lily-demo-financial/load.log 2>&1
./data-load-account_role.sh /disk1/current/DemoPersonaAccountRoleData.csv >> /var/log/lily-demo-financial/load.log 2>&1

echo 'DATA-RELOAD-ITX' >> /var/log/lily-demo-financial/load.log 2>&1
./data-reload-itx.sh /disk1/current >> /var/log/lily-demo-financial/load.log 2>&1
