#!/bin/bash

output_file=/tmp/diag-$(date +%Y-%m-%d).json
lily dna-diagnostics --dna-entity-type customer --skip-cluster-status --skip-content-stats --output ${output_file};
lily script ./diagnostics-import.groovy ${output_file};
