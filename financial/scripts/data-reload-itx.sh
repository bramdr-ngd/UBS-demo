#!/bin/bash
set -e;

[[ -z "$1" ]] && echo "Usage: data-load-itx.sh /path/to_files_to_load_without_trailing_slash" && exit 1;
[[ $1 =~ .*/$ ]] && echo "Usage: data-load-itx.sh /path/to_files_to_load_without_trailing_slash" && exit 1;

./data-clean-itx.sh;
#!./data-regenerate-itx.sh $1;
./data-load-itx.sh $1;
./data-batch-calc.sh -f;

lily coprocessor-admin vcecache --dna-entity-type customer --truncate
sleep 10
lily coprocessor-admin vcecache --dna-entity-type customer --init
