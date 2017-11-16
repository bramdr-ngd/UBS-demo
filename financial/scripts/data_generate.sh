#!/bin/bash

python data-generate-customers.py -n 50000 -o /disk1/current/tmp/scripts/.data 
python data-generate-productsv2.py -o /disk1/current/tmp/scripts/.data  
python data-generate-account.py -o /disk1/current/tmp/scripts/.data  
python data-generate-account_role.py  -o /disk1/current/tmp/scripts/.data  
python data-generate-itx.py -n 6 -o /disk1/current/tmp/scripts/.data 

python data-generate-DemoPersona.py -o /disk1/current/tmp/scripts/.data 
python data-generate-DemoPersona-products.py -o /disk1/current/tmp/scripts/.data 
python data-generate-DemoPersona-Account.py -o /disk1/current/tmp/scripts/.data 
python data-generate-DemoPersona-AccountRole.py -o /disk1/current/tmp/scripts/.data 
python data-generate-itx-DemoPersona.py -o /disk1/current/tmp/scripts/.data 


