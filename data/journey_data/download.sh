#!/bin/bash

data_files_path=$1

jq -r .journeys.file_names[] $data_files_path | while read file; do
  curl -s https://cycling.data.tfl.gov.uk/usage-stats/$file --output $file
  echo "Downloaded: "$file
done
