#!/bin/bash
die() {
  local message="$1"
  local code="${2:-1}"
  if [[ -n "$message" ]] ; then
    echo "ERROR: ${message}"
  else
    echo "ERROR: Execution failed"
  fi
  exit "${code}"
}
trap 'die "Execution failed near line ${LINENO}"' ERR

show_help() {
cat << EOF
Usage: ${0##*/} [-h] [-f]
Run batch calculations

  -h  Display this message
  -f  Do a full rebuild of batch jobs where possible
EOF
}
OPTIND=1
FULL_REBUILD=""
START_DATE=""
while getopts "hf" opt; do
  case "${opt}" in
    h)
      show_help
      exit 0
      ;;
    f)
      FULL_REBUILD="--full-rebuild"
      START_DATE="--start-date $(date -d '-6 months' +%Y-%m-%d)"
      ;;
    '?')
      show_help
      exit 0
      ;;
  esac
done

shift "$((OPTIND-1))"

echo "Calculating entity aggregates on CUSTOMER_CRM"
lily dna-entity-batch-calc --dna-entity-type CUSTOMER_CRM ${START_DATE}

echo 'Calculating itx aggregates'
lily fs -mkdir -p /lily/interactions/default/augmented/.temp/dontdelete ||:
lily fs -chmod 777 /lily/interactions/default/augmented/.temp
lily itx-batch-augmentation ${FULL_REBUILD}
lily dna-itx-batch-calc --dna-entity-type customer ${FULL_REBUILD} ||:  #fails if there are no new interaction to process
lily dna-itx-batch-calc --dna-entity-type metric ${FULL_REBUILD} ||:  #fails if there are no new interaction to process

echo '=== MASTER/SOURCE ==='
lily fs -touchz masterRecordSyncFile #create empty file
lily master-record-sync --dna-entity-type customer --input masterRecordSyncFile ${FULL_REBUILD}
lily master-batch-update-factual --dna-entity-type customer

echo '=== SETS ==='
lily set-membership-calc --dna-entity-type customer ${START_DATE}
lily dna-set-batch-calc --dna-entity-type customer ${START_DATE}

echo '=== VIEWS ==='
lily itx-view-batch-calc --dna-entity-type=customer ${FULL_REBUILD}
lily alert-active-count-calc --dna-entity-type customer

#should not be necessary
#echo '=== INDEXING ==='
#lily-batch-index-build.sh direct-write lilyindexer_entity_CUSTOMER_SET
#lily-batch-index-build.sh direct-write lilyindexer_entity_CUSTOMER

echo '=== FINISHED ==='
