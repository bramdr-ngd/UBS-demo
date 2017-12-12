#!/bin/bash

rsync -avr ~/ubs/git ubs1.demo.ngdata.com:~
ssh ubs1.demo.ngdata.com 'lily dna-upload-conf --dna-entity-type customer --custom-dna ~/git/lily-demo/financial/config/VIEWS/standard/DNA_ENTITY_TYPES/CUSTOMER/CUSTOM_METRICS.xml'