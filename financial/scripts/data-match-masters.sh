#!/bin/bash
lily matcher-master-full --dna-entity-type customer --input type=itx
# lily master-record-sync --dna-entity-type customer --input "${hdfsMasterRecordSyncFile}"
lily master-batch-update-factual --dna-entity-type customer