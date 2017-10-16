#!/bin/bash
set -e

# remove all interactions from hdfs
hadoop fs -rm -r -f -skipTrash /lily/interactions/default/mapped/ngdata_lily_atm/year*;
hadoop fs -rm -r -f -skipTrash /lily/interactions/default/mapped/ngdata_lily_branch/year*;
hadoop fs -rm -r -f -skipTrash /lily/interactions/default/mapped/ngdata_lily_callcenter/year*;
hadoop fs -rm -r -f -skipTrash /lily/interactions/default/mapped/ngdata_lily_email/year*;
hadoop fs -rm -r -f -skipTrash /lily/interactions/default/mapped/ngdata_lily_mobileapp/year*;
hadoop fs -rm -r -f -skipTrash /lily/interactions/default/mapped/ngdata_lily_paymentsystem/year*;
hadoop fs -rm -r -f -skipTrash /lily/interactions/default/mapped/ngdata_lily_web/year*;
hadoop fs -rm -r -f -skipTrash /lily/interactions/default/augmented/*;

# clear data from VCE cache
lily script ./clearVCE.groovy;
