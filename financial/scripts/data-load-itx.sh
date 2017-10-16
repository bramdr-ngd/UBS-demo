#!/bin/bash
set -e;

[[ -z "$1" ]] && echo "Usage: data-load-itx.sh /path/to_files_to_load_without_trailing_slash" && exit 1;
[[ $1 =~ .*/$ ]] && echo "Usage: data-load-itx.sh /path/to_files_to_load_without_trailing_slash" && exit 1;

hdfsTargetPath=/tmp/interactions
lily fs -mkdir -p $hdfsTargetPath
lily fs -rm -r -f $hdfsTargetPath/*;
lily fs -copyFromLocal $1/ItxData_*.{csv,hdr} $hdfsTargetPath/;

lily itx-batch-ingest --interaction-type ngdata.lily.atm --source-path hdfs://$hdfsTargetPath/ItxData_AT_ATM_*.csv --script ./itx-import-mapping-at.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.branch --source-path hdfs://$hdfsTargetPath/ItxData_AT_Branch_*.csv --script ./itx-import-mapping-at.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.callcenter --source-path hdfs://$hdfsTargetPath/ItxData_AT_CallCenter_*.csv --script ./itx-import-mapping-at.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.mobileapp --source-path hdfs://$hdfsTargetPath/ItxData_AT_MobileApp_*.csv --script ./itx-import-mapping-at.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.web --source-path hdfs://$hdfsTargetPath/ItxData_AT_Web_*.csv --script ./itx-import-mapping-at.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.atm --source-path hdfs://$hdfsTargetPath/ItxData_CA_ATM_*.csv --script ./itx-import-mapping-ca.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.branch --source-path hdfs://$hdfsTargetPath/ItxData_CA_Branch_*.csv --script ./itx-import-mapping-ca.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.callcenter --source-path hdfs://$hdfsTargetPath/ItxData_CA_CallCenter_*.csv --script ./itx-import-mapping-ca.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.mobileapp --source-path hdfs://$hdfsTargetPath/ItxData_CA_MobileApp_*.csv --script ./itx-import-mapping-ca.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.web --source-path hdfs://$hdfsTargetPath/ItxData_CA_Web_*.csv --script ./itx-import-mapping-ca.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.branch --source-path hdfs://$hdfsTargetPath/ItxData_CE_Branch_*.csv --script ./itx-import-mapping-ce.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.callcenter --source-path hdfs://$hdfsTargetPath/ItxData_CE_CallCenter_*.csv --script ./itx-import-mapping-ce.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.email --source-path hdfs://$hdfsTargetPath/ItxData_CE_Email_*.csv --script ./itx-import-mapping-ce.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.mobileapp --source-path hdfs://$hdfsTargetPath/ItxData_CE_MobileApp_*.csv --script ./itx-import-mapping-ce.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.web --source-path hdfs://$hdfsTargetPath/ItxData_CE_Web_*.csv --script ./itx-import-mapping-ce.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.atm --source-path hdfs://$hdfsTargetPath/ItxData_CW_ATM_*.csv --script ./itx-import-mapping-cw.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.branch --source-path hdfs://$hdfsTargetPath/ItxData_CW_Branch_*.csv --script ./itx-import-mapping-cw.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.branch --source-path hdfs://$hdfsTargetPath/ItxData_OF_Branch_*.csv --script ./itx-import-mapping-of.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.callcenter --source-path hdfs://$hdfsTargetPath/ItxData_OF_CallCenter_*.csv --script ./itx-import-mapping-of.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.email --source-path hdfs://$hdfsTargetPath/ItxData_OF_Email_*.csv --script ./itx-import-mapping-of.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.mobileapp --source-path hdfs://$hdfsTargetPath/ItxData_OF_MobileApp_*.csv --script ./itx-import-mapping-of.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.web --source-path hdfs://$hdfsTargetPath/ItxData_OF_Web_*.csv --script ./itx-import-mapping-of.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.branch --source-path hdfs://$hdfsTargetPath/ItxData_PM_Branch_*.csv --script ./itx-import-mapping-pm.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.callcenter --source-path hdfs://$hdfsTargetPath/ItxData_PM_CallCenter_*.csv --script ./itx-import-mapping-pm.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.web --source-path hdfs://$hdfsTargetPath/ItxData_PM_Web_*.csv --script ./itx-import-mapping-pm.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.paymentsystem --source-path hdfs://$hdfsTargetPath/ItxData_PU_Purchases_*.csv --script ./itx-import-mapping-pu.groovy;

lily itx-batch-ingest --interaction-type ngdata.lily.mobileapp --source-path hdfs://$hdfsTargetPath/ItxData_MobileApp_*.csv --script ./itx-import-mapping-mobile.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.web --source-path hdfs://$hdfsTargetPath/ItxData_CarC*.csv --script ./itx-import-mapping-web.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.web --source-path hdfs://$hdfsTargetPath/ItxData_CarL*.csv --script ./itx-import-mapping-web.groovy;
lily itx-batch-ingest --interaction-type ngdata.lily.web --source-path hdfs://$hdfsTargetPath/ItxData_CarSim*.csv --script ./itx-import-mapping-sim.groovy;

lily itx-batch-ingest --interaction-type ngdata.lily.LocationUpdate --source-path hdfs://$hdfsTargetPath/ItxData_Loc*.csv --script ./itx-import-mapping-loc.groovy;

echo 'DO NOT FORGET:'
echo 'lily matcher-master-full --input type=itx --dna-entity-type customer'
