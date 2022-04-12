#!/bin/bash

remote_host=${1}
script_dir=$(cd $(dirname $0); pwd)
rsync_opts="-ar --progress"

if [[ -z "${remote_host}" ]]
then
    echo "usage: $0 host"
    exit 1
fi

mkdir -p download

rsync ${rsync_opts} \
      --include-from=${script_dir}/include.txt --exclude='*.*' \
      ${remote_host}:/mdsim/project2/ \
      download
