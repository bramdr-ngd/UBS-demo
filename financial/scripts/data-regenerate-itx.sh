#!/usr/bin/bash
set -e

[[ -z "$1" ]] && echo "Usage: data-load-itx.sh /path/to_folder_where_to_generate_files_without_trailing_slash" && exit 1;
[[ $1 =~ .*/$ ]] && echo "Usage: data-load-itx.sh /path/to_folder_where_to_generate_files_without_trailing_slash" && exit 1;

# remove previously generated interactions
# -f to ignore if files do not exist
echo 'remove old itx files'
rm -f $1/ItxData_*.{csv,hdr}

# generate new interactions
echo 'generate new itx files'
./data-generate-itx.py -n 6 -o $1 -m ./data-generate-model --no-progress;
./data-generate-itx-DemoPersona.py -o $1 --no-progress;
